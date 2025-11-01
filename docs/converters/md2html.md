# Markdown to HTML converter

Convert Markdown documents to self-contained HTML pages with optional themes and
inline CSS overrides.

## Command line

```bash
file-converters md2html docs/articles \
  --theme github \
  --output-folder public/html
```

Flags:

- `--theme` &mdash; pick one of `default`, `github` or `dark`.
- `--extra-css` &mdash; append additional CSS rules to the selected theme.
- `--output-folder` &mdash; customise where the HTML files are written.

## Python API

```python
from converters import convert_markdown_to_html

result = convert_markdown_to_html("docs/articles", theme="dark")
for source, destination in result.converted:
    print(source, "→", destination)
```

## Tips

- The Markdown renderer enables fenced code blocks, tables, sane lists, table of
  contents generation and “smart” typography.
- The generated HTML is formatted using BeautifulSoup for readability.
- Use the `extra_css` parameter to inject custom styling without editing the
  converter.
