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
from converters import convert_text_to_pdf

result = convert_text_to_pdf("notes", font_size=10, output_folder_name="exports/pdf")
print(result.total_converted, "files written")
```

## Tips

- Custom fonts must be supplied as `.ttf` files and are registered on the fly.
- Empty lines in the source text are preserved.
- Set `patterns` to a tuple of glob patterns when you need to restrict the
  converter to a specific subset of files.
