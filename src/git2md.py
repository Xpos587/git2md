from __future__ import annotations

import argparse
import importlib
import logging
import pkgutil
import sys
from pathlib import Path
from types import ModuleType
from pathspec import PathSpec

from converters.base import BaseConverter
from exporters.base import BaseExporter
from utils.ignore import (
    should_ignore,
    load_ignore,
)
from utils.tree import build_tree, TreeNode
from utils.clipboard import copy_content

logger = logging.getLogger(__name__)


def load_converters() -> list[BaseConverter]:
    import converters  # the "converters" package

    converters_module: ModuleType = converters
    converter_paths: list[str] = list(converters_module.__path__)
    result: list[BaseConverter] = []

    for module_info in pkgutil.iter_modules(converter_paths):
        module_name = f"converters.{module_info.name}"
        module = importlib.import_module(module_name)
        conv = getattr(module, "converter", None)
        if isinstance(conv, BaseConverter):
            result.append(conv)

    return result


def load_exporters() -> list[BaseExporter]:
    import exporters  # the "exporters" package

    exporters_module: ModuleType = exporters
    exporter_paths: list[str] = list(exporters_module.__path__)
    result: list[BaseExporter] = []

    for module_info in pkgutil.iter_modules(exporter_paths):
        module_name = f"exporters.{module_info.name}"
        module = importlib.import_module(module_name)
        exp = getattr(module, "exporter", None)
        if isinstance(exp, BaseExporter):
            result.append(exp)

    return result


def get_converter(
    file_path: Path,
    converters_list: list[BaseConverter],
    default_converter: BaseConverter,
) -> BaseConverter:
    for conv in converters_list:
        if conv.supports(file_path):
            return conv
    return default_converter


TreeDict = dict[str, dict[str, object]]


def format_tree(node: TreeNode, prefix: str = "") -> str:
    """
    Превращает `TreeNode` в красиво оформленное дерево строк.
    """
    lines: list[str] = []
    entries = list(node.children.items()) if node.children else []

    for index, (name, child) in enumerate(entries):
        connector: str = "└── " if index == len(entries) - 1 else "├── "
        line: str = prefix + connector + name
        if child.is_dir:
            line += "/"
        lines.append(line)

        if child.is_dir and child.children:
            extension: str = "    " if index == len(entries) - 1 else "│   "
            deeper: str = format_tree(child, prefix + extension)
            lines.append(deeper)

    return "\n".join(lines)


def process_file(
    file_path: Path,
    converters_list: list[BaseConverter],
    default_converter: BaseConverter,
) -> str:
    """
    Обрабатывает один файл с использованием подходящего конвертера.
    """
    conv = get_converter(file_path, converters_list, default_converter)
    return conv.convert(file_path)


def process_directory(
    directory: Path,
    gitignore_spec: PathSpec | None,
) -> str:
    """
    Обрабатывает директорию, создавая текстовое представление дерева.
    """
    tree = build_tree(directory, directory, gitignore_spec)
    return format_tree(tree)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert files or directories with modular converters and exporters."
    )
    parser.add_argument(
        "input", type=Path, nargs="?", default="./", help="Path to file or directory"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional output file to save results",
    )
    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copy output to clipboard",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "--ignore",
        nargs="+",
        default=[],
        help="Ignore specific files (supports wildcards, e.g., '*.css' 'assets/*.html')",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    input_path: Path = args.input
    if not input_path.exists():
        logger.error("Input path '%s' not found.", input_path)
        sys.exit(1)

    converters_list: list[BaseConverter] = load_converters()
    exporters_list: list[BaseExporter] = load_exporters()

    if not converters_list or not exporters_list:
        logger.error("No converters or exporters found. Exiting.")
        sys.exit(1)

    default_converter: BaseConverter | None = next(
        (c for c in converters_list if c.__class__.__name__ == "DefaultConverter"), None
    )

    if default_converter is None:
        from converters.default import converter as default_conv

        default_converter = default_conv

    exporter: BaseExporter = exporters_list[0]

    gitignore_spec = load_ignore(input_path, args.ignore)

    output: str = ""

    if input_path.is_file():
        conv = get_converter(input_path, converters_list, default_converter)
        content = conv.convert(input_path)
        language = conv.get_language(input_path)
        output += exporter.format(input_path, content, language)
    elif input_path.is_dir():
        tree_output = process_directory(input_path, gitignore_spec)
        output += f"## Tree for {input_path.name}\n```\n{tree_output}\n```\n\n"

        for file_path in input_path.rglob("*"):
            if not should_ignore(
                str(file_path), [], str(input_path), gitignore_spec
            ) and file_path.is_file():
                # Скип пустых файлов
                if file_path.stat().st_size == 0:
                    logger.debug("Skipping empty file: %s", file_path)
                    continue

                conv = get_converter(file_path, converters_list, default_converter)
                content = conv.convert(file_path)
                language = conv.get_language(file_path)
                rel_path = file_path.relative_to(input_path)
                output += exporter.format(rel_path, content, language)
    else:
        logger.error("Unsupported path type.")
        sys.exit(1)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
        logger.info("Output written to %s", args.output)

    if args.copy:
        copy_content(output)
        logger.info("Output copied to clipboard")


if __name__ == "__main__":
    main()
