# Text to PDF converter

Typeset plain text or Markdown files into paginated PDF documents. The converter
wraps long lines according to the selected font metrics and handles page breaks
automatically.

## Command line

```bash
file-converters text2pdf notes \
  --font-name "Helvetica" \
  --font-size 11 \
  --margin 0.75
```

Flags:

- `--font-name` &mdash; name of the font registered with ReportLab.
- `--font-path` &mdash; register and use a custom TTF font.
- `--font-size` &mdash; font size in points.
- `--margin` &mdash; page margin in inches.
- `--output-folder` &mdash; customise the destination directory.

## Python API

```python
from converters import TextToPdfLayout, convert_text_to_pdf

layout = TextToPdfLayout(font_name="Helvetica", font_size=10, margin=0.75)
result = convert_text_to_pdf("notes", layout=layout, output_folder_name="exports/pdf")
print(result.total_converted, "files written")
```

## Tips

- Custom fonts must be supplied as `.ttf` files and are registered on the fly.
- Empty lines in the source text are preserved.
- Instantiate `TextToPdfLayout` when you need to customise fonts, margins or
  the page size for your workflow.
