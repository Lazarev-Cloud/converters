# File Converters Collection

A curated set of Python utilities for converting between common file formats. The
project focuses on reliability, helpful command line output and clean, reusable
APIs for automation scripts.

## Key features

- **Unified CLI** &mdash; one entry point that exposes every converter with
  dedicated options.
- **Reusable Python API** &mdash; each converter returns a structured
  `ConversionResult` describing what happened.
- **Batch-friendly** &mdash; point the CLI at any folder and the appropriate
  output directory is created automatically.
- **Extensible** &mdash; it is straightforward to add new converters or adjust
  existing ones thanks to the shared utility layer.

## Installation

The package targets Python 3.9 and newer. Install the runtime dependencies and
(optional) the command line entry point in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Command line usage

List all available converters:

```bash
file-converters --list
```

Run one of the converters (the CLI names match the directory names inside the
`converters/` package):

```bash
# Convert every Markdown document in the folder to HTML
file-converters md2html docs/content --theme github

# Transcode images to WebP while keeping existing results intact
file-converters img2webp assets/images --quality 85
```

Every command prints a short summary that includes the output directory and
counts of converted, skipped and failed files.

### Exposed converters

| Name       | Description | Key options |
|------------|-------------|-------------|
| `img2webp` | Convert bitmap images (PNG, JPG, GIF, BMP, TIFF, etc.) to WebP | `--quality`, `--lossless`, `--overwrite`, `--output-folder` |
| `csv2json` | Transform CSV spreadsheets into JSON documents | `--encoding`, `--no-pretty`, `--output-folder` |
| `md2html`  | Render Markdown documents as styled HTML pages | `--theme`, `--extra-css`, `--output-folder` |
| `html2md`  | Convert HTML content into Markdown for further editing | `--heading-style`, `--bullets`, `--wrap-width`, `--output-folder` |
| `text2pdf` | Typeset plain text files into PDF documents | `--font-name`, `--font-path`, `--font-size`, `--margin`, `--output-folder` |

Refer to the [documentation](docs/index.md) for in-depth explanations and
workflow tips for each converter.

## Programmatic usage

All conversion functions can be imported and executed directly. Each function
returns a `ConversionResult` with detailed information that can be inspected or
serialised to JSON.

```python
from pathlib import Path

from converters import convert_markdown_to_html

result = convert_markdown_to_html(Path("./notes"), theme="github")

print("Converted", result.total_converted, "files")
print("Errors:", result.errors)
```

## Contributing

Issues and pull requests are welcome! If you plan a larger contribution please
open an issue first so we can discuss the approach.

1. Fork the repository and create a feature branch.
2. Install the project in editable mode (`pip install -e .`).
3. Add or update tests/documentation alongside your changes.
4. Run the test suite before submitting (`pytest`).

## License

This project is released under the MIT License. See the `LICENSE` file for
further details.
