# Converters documentation

This directory complements the project README and provides practical guidance
for each converter. Every document includes an overview, command line examples
and notes on the Python API.

- [CSV to JSON](converters/csv2json.md)
- [Images to WebP](converters/img2webp.md)
- [Markdown to HTML](converters/md2html.md)
- [Text to PDF](converters/text2pdf.md)

## Shared concepts

### ConversionResult

All conversion functions return a [`ConversionResult`](../converters/utils.py)
instance. Besides the number of converted files it also exposes lists of skipped
files and encountered errors. The object can be serialised with
`ConversionResult.as_dict()` which returns JSON-friendly data.

### Output folders

Each converter creates an output folder inside the source directory. Use the
`--output-folder` option (or the `output_folder_name` keyword argument when
calling the API) to customise the location when integrating into automated
workflows.
