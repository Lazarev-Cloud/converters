# File Converters Collection

A comprehensive collection of simple and efficient file format converters implemented in Python. This project provides easy-to-use tools for converting between various file formats.

## Features

- **Modular Design**: Each converter is self-contained and can be used independently
- **Simple CLI**: Unified command-line interface for all converters
- **Batch Processing**: Convert multiple files at once
- **Detailed Output**: Statistics and progress information during conversion
- **Customizable Options**: Quality settings, themes, and other format-specific options

## Available Converters

| Converter | Description | Input Formats | Output Format |
|-----------|-------------|---------------|--------------|
| img2webp | Convert images to WebP format | JPG, PNG, GIF, BMP, TIFF, etc. | WebP |
| text2pdf | Convert text files to PDF documents | TXT, MD, etc. | PDF |
| md2html | Convert Markdown to HTML with themes | MD, Markdown | HTML |
| csv2json | Convert CSV files to JSON format | CSV | JSON |

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Lazarev-Cloud/converters/file-converters.git
   cd file-converters
   ```

2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

Use the included CLI tool to access all converters:

```bash
# List all available converters
python cli.py --list

# Convert all images in a folder to WebP
python cli.py img2webp /path/to/images --quality 85

# Convert all text files to PDF
python cli.py text2pdf /path/to/textfiles

# Convert Markdown files to HTML
python cli.py md2html /path/to/markdown --theme github

# Convert CSV files to JSON
python cli.py csv2json /path/to/csvfiles --pretty
```

### Using Converters Directly

Each converter can also be used as a standalone module:

```python
from converters.img2webp.main import convert_images_to_webp

# Convert all images in a folder to WebP
convert_images_to_webp('/path/to/images', quality=85)
```

## Converter-Specific Options

### img2webp
- `quality`: WebP quality (0-100), lower means smaller file size (default: 80)

### text2pdf
- `font_name`: Name of the font to use (default: "Courier")
- `font_size`: Font size in points (default: 12)
- `margin`: Margin in inches (default: 0.5)

### md2html
- `theme`: CSS theme to apply (options: "default", "github", "dark")

### csv2json
- `pretty_print`: Whether to format the JSON with indentation (default: True)
- `encoding`: Encoding to use when reading CSV files (default: 'utf-8')

## Requirements

- Python 3.7+
- Pillow (for image processing)
- ReportLab (for PDF generation)
- Markdown (for Markdown processing)
- BeautifulSoup4 (for HTML formatting)

See `requirements.txt` for complete dependencies.

## Adding New Converters

To add a new converter:

1. Create a new directory in the `converters` folder
2. Add a `main.py` file with a function named `convert_X_to_Y`
3. Add a `README.md` with converter-specific documentation
4. Update the main `requirements.txt` if needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-converter`)
3. Commit your changes (`git commit -m 'Add some amazing converter'`)
4. Push to the branch (`git push origin feature/amazing-converter`)
5. Open a Pull Request