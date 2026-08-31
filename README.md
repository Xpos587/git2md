

# 🔄 git2md

![PyPI](https://img.shields.io/pypi/v/git2md)
![Python Version](https://img.shields.io/pypi/pyversions/git2md)
![Build Status](https://img.shields.io/github/actions/workflow/status/xpos587/git2md/.github/workflows/release.yaml)
![License](https://img.shields.io/github/license/xpos587/git2md)
![AUR version](https://img.shields.io/aur/version/git2md-git)

🚀 A powerful command-line tool for converting Git repository contents into Markdown format.
This tool is perfect for developers and documentation specialists who need to create
structured Markdown files based on repository contents, including directory trees and file contents.

Read README in Russian [here](https://github.com/Xpos587/git2md/blob/main/README_RU.md)

---

## ✨ Features

- **🌳 Repository Directory Tree Generation**: outputs repository structure in `tree` block format.
- **📝 File to Markdown Conversion**:
  - Supports syntax highlighting for code files.
  - ~~Converts Jupyter Notebook (`.ipynb`) and PDF (`.pdf`) to Markdown.~~
- **🎯 Support for `.gitignore`, `.globalignore` and `.mdignore` for local projects**:
  - Automatically excludes files/directories specified in `.gitignore`, `.globalignore` or `.mdignore`.
- **🔍 Custom Exclusion Patterns**: use regular expressions to exclude specific files or directories.
- **🗑️ Skip Empty Files**: ignores files without content.
- **📋 Copy Results to Clipboard**: simplifies using generated Markdown.

---

## 🎬 Demonstration

Below is a demonstration of how `git2md` works:

![Demo of git2md](https://raw.githubusercontent.com/Xpos587/git2md/refs/heads/main/assets/demo.gif)

---

## 📋 Requirements

- **🐍 Python 3.10 or newer**
- **🐧 ~~Linux Operating System~~ Now supports Windows, MacOS, Linux (X11 and Wayland)**
- **📦 Dependencies**:
  - `pathspec` (for `.gitignore`, `.mdignore`, `.globalignore` support)
  - ~~`nbconvert` (for Jupyter Notebook conversion)~~ (support temporarily limited)
  - ~~`PyMuPDF4LLM` (for PDF conversion)~~ (support discontinued, will be replaced with better alternatives)
  - `wl-copy/xsel/xclip` (optional, Linux-only for clipboard functionality)

---

## 📥 Installation

### 📦 Install via PyPI

You can install `git2md` directly through PyPI using pip:

```bash
pip install git2md
```

### 🏗️ Install via AUR (Arch Linux)

For Arch Linux users, the package is available in AUR as [python-git2md](https://aur.archlinux.org/packages/python-git2md). It can be installed using AUR helpers like `paru` or `yay`:

```bash
paru -S python-git2md
```

### 🔨 Install from Source

1. Clone the repository:

   ```bash
   git clone https://github.com/xpos587/git2md.git
   cd git2md
   ```

2. Build and install:

   ```bash
   python setup.py build
   pip install .
   ```

---

## 🚀 Usage

### 💻 Basic Command

```bash
git2md [path] [options]
```

If path is not specified, the current directory will be used.

### ⚙️ Options

| Option           | Description                                                     |
| ---------------- | --------------------------------------------------------------- |
| `path`           | Path to project directory or Git file (default: current folder) |
| `-o`, `--output` | Path to save generated Markdown                                 |
| `-c`, `--copy`   | Copy result to clipboard                                        |
| `--ignore`       | List of patterns to exclude files or directories                |

---

## 📝 Examples

### 📂 Generate Markdown for Entire Repository

```bash
git2md /path/to/repo -o output.md
```

### 🔍 Exclude Specific Files Using Patterns

```bash
git2md --ignore "./assets/style-*.css" "*.log" "*.tmp" -o output.md
```

### 🗑️ Copy Result to Clipboard

```bash
git2md --copy
```

---

## 📄 Output Format

### 🌳 Directory Tree

The directory tree is included as a code block with language identifier `tree`. For example:

```tree
src/
├── main.py
├── utils/
│   ├── helper.py
│   └── __init__.py
└── README.md
```

### 📑 File Contents

Each file is included with its relative path in the header, followed by its contents in a code block.

#### 🐍 Example for Python File (`main.py`)

````markdown
# File: src/main.py

```
print("Hello, world!")
```

# End of file: src/main.py
````

#### 📓 Example for Jupyter Notebook (`notebook.ipynb`)

Content is converted from `.ipynb` to Markdown and included directly:

```markdown
# File: notebook.ipynb

# Converted content from Jupyter Notebook...

# End of file: notebook.ipynb
```

#### 📄 Example for PDF (`document.pdf`)

Text is extracted in Markdown format:

```markdown
# File: document.pdf

# Extracted content from PDF...

# End of file: document.pdf
```

---

## 🔧 Global Exclusion Patterns

You can create a `.mdignore` file in the same directory as the script to specify patterns that should be excluded for all repositories. The format is identical to `.gitignore`.

#### 📝 Example `.mdignore`

```plaintext
__pycache__/
*.pyc
.mypy_cache/
.env
*.log
```

---

## 👨‍💻 Development

To set up the development environment:

1. Create a virtual environment:

   ```bash
   micromamba create -p ./.micromamba/ -f environment.yml
   micromamba activate -p ./.micromamba/
   ```

2. Install the project in development mode:

   ```bash
   pip install -e .
   ```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Create a Pull Request.

---

## 👥 Authors

Michael (<x30827pos@gmail.com>)

---

## 🙏 Acknowledgments

Thanks to the developers of [repomix](https://github.com/yamadashy/repomix) and [git2txt](https://github.com/mrauter1/git2txt).

The idea emerged from the need for universal and simplified repository documentation
for LLM-based workflows.
