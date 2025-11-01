# Images to WebP converter

Batch-convert common bitmap image formats to WebP. Existing WebP files can be
re-encoded to adjust the quality or to convert animated GIFs into animated WebP
files.

## Command line

```bash
file-converters img2webp assets/images \
  --quality 85 \
  --output-folder exports/webp
```

Flags:

- `--quality` &mdash; quality slider between 0 and 100. Higher numbers mean larger
  files with better visual fidelity.
- `--lossless` &mdash; force lossless encoding (disables the quality parameter).
- `--overwrite` &mdash; regenerate files even if the WebP counterpart already exists.
- `--output-folder` &mdash; customise the output directory.

## Python API

```python
from converters import convert_images_to_webp

result = convert_images_to_webp("assets/images", quality=90, skip_existing=False)
print(result.total_converted)
```

## Tips

- Animated GIFs preserve their animation when converted to WebP.
- Unsupported formats raise an error for that specific file while the rest of the
  batch continues to process.
- Use `skip_existing=False` to refresh previously generated WebP files.
