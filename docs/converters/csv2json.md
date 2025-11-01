# CSV to JSON converter

The CSV converter parses spreadsheets and exports each file as JSON. The tool
performs light data cleaning (trimming whitespace, converting numeric values and
booleans) while preserving empty cells as `null`.

## Command line

```bash
file-converters csv2json data/surveys \
  --encoding utf-8 \
  --output-folder exports/json
```

Flags:

- `--no-pretty` &mdash; write JSON without indentation (useful for very large
  files).
- `--encoding` &mdash; specify the character encoding of the CSV files.
- `--output-folder` &mdash; name of the folder created inside the source directory.

## Python API

```python
from converters import convert_csv_to_json

result = convert_csv_to_json("data/surveys", pretty_print=False)
print(result.as_dict())
```

## Tips

- The dialect is auto-detected using `csv.Sniffer`. If detection fails the
  standard Excel dialect (comma-separated, quoted with `"`) is used.
- Files are processed independently so one malformed spreadsheet does not block
  the rest of the batch.
