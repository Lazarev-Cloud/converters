# HTML to Markdown converter

The HTML to Markdown converter helps clean up HTML exports by turning them into
Markdown files that are easier to edit and track in version control.

## Command line usage

```bash
file-converters html2md path/to/html --heading-style ATX --bullets "-"
```

Options:

- `--heading-style` &mdash; choose between `ATX`, `ATX_CLOSED` and `SETEXT`
  heading styles.
- `--bullets` &mdash; pick the bullet character for unordered lists.
- `--wrap-width` &mdash; set a soft line width (use `0` to keep existing line
  lengths).
- `--output-folder` &mdash; customise the destination directory (default: `markdown`).

## Python API

```python
from converters import convert_html_to_markdown

result = convert_html_to_markdown("./exports", heading_style="SETEXT")
print(result.total_converted)
```

The function reads every `.html`/`.htm` file inside the source folder, converts
it to Markdown and stores the result inside an output directory. Each invocation
returns a [`ConversionResult`](../../converters/utils.py) with details about the
run.

### Dependencies

The converter relies on [`markdownify`](https://github.com/matthewwithanm/python-markdownify)
for the HTML-to-Markdown transformation. Install it via
`pip install markdownify` (already listed in `requirements.txt`).
