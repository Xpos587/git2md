# git2md

A command-line tool for converting Git repository contents to Markdown format. This tool helps you create documentation by generating a Markdown file containing the repository structure and the contents of all files.

## Features

- Generate repository file structure tree
- Convert files to Markdown with proper syntax highlighting
- Support for .gitignore patterns
- Custom file/directory ignore patterns
- Include specific files/directories only
- Copy output to clipboard (requires wl-copy)
- Skip empty files
- Supports custom global ignore patterns via .globalignore

## Requirements

- Python 3.12 or higher
- Linux operating system
- wl-copy (for clipboard functionality)
- pathspec>=0.12.1 (for .gitignore support)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/xpos587/git2md.git
cd git2md
```

2. Run the installation script:
```bash
python install.py
```

The script will:
- Install the package in your Python environment
- Create a symlink in /usr/local/bin for global access (requires sudo)

## Usage

Basic usage:
```bash
git2md <path> [options]
```

Options:
```
positional arguments:
  path                  Path to the git project directory.

optional arguments:
  -h, --help              Show this help message and exit
  -o, --output            Output file path
  -exc, --exclude         List of files/directories to ignore (glob patterns)
  -inc, --include         List of files/directories to include (glob patterns)
  -se, --skip-empty       Skip empty files
  -cp, --clipboard        Copy output to clipboard
  -igi, --ignoregitignore Ignore .gitignore and .globalignore files
```

## Examples

1. Generate markdown for entire repository:
```bash
git2md /path/to/repo -o output.md
```

2. Include only specific files/directories:
```bash
git2md /path/to/repo -inc "src/*.py" "docs/*" -o output.md
```

3. Ignore specific patterns:
```bash
git2md /path/to/repo -exc "*.pyc" "__pycache__" -o output.md
```

4. Copy output to clipboard:
```bash
git2md /path/to/repo -cp
```

5. Ignore .gitignore rules:
```bash
git2md -igi -o output.md /path/to/repo
```

## Global Ignore Patterns

You can create a `.globalignore` file in the same directory as the script to specify patterns that should be ignored across all repositories. The format is the same as `.gitignore`.

Example `.globalignore`:
```
__pycache__/
*.pyc
.git/
.env
.venv
```

## Development

To set up the development environment:

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install in editable mode:
```bash
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Authors

- Michael (x30827pos@gmail.com)

## Acknowledgments

- Thanks to the pathspec library for .gitignore support
- Inspired by the need to easily document Git repositories for LLM
