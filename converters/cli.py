"""Command line entry-point for the converters toolkit."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, Mapping

from . import (
    ConversionResult,
    convert_csv_to_json,
    convert_images_to_webp,
    convert_markdown_to_html,
    convert_text_to_pdf,
)


@dataclass
class ConverterSpec:
    """Description of a CLI-accessible converter."""

    func: Callable[..., ConversionResult]
    help: str
    options: Callable[[argparse.ArgumentParser], None]
    namespace_to_kwargs: Callable[[argparse.Namespace], Dict[str, object]]


def _img_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("source", help="Folder containing image files")
    parser.add_argument("--quality", type=int, default=80, help="WebP quality (0-100)")
    parser.add_argument("--lossless", action="store_true", help="Force lossless encoding")
    parser.add_argument("--overwrite", action="store_true", help="Re-create files even if they already exist")
    parser.add_argument("--output-folder", default="webp", help="Name of the output directory (default: webp)")


def _img_kwargs(ns: argparse.Namespace) -> Dict[str, object]:
    return {
        "source_folder": ns.source,
        "quality": ns.quality,
        "lossless": True if ns.lossless else None,
        "skip_existing": not ns.overwrite,
        "output_folder_name": ns.output_folder,
    }


def _csv_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("source", help="Folder containing CSV files")
    parser.add_argument("--no-pretty", action="store_true", help="Disable pretty-printed JSON output")
    parser.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")
    parser.add_argument("--output-folder", default="json", help="Name of the output directory (default: json)")


def _csv_kwargs(ns: argparse.Namespace) -> Dict[str, object]:
    return {
        "source_folder": ns.source,
        "pretty_print": not ns.no_pretty,
        "encoding": ns.encoding,
        "output_folder_name": ns.output_folder,
    }


def _md_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("source", help="Folder containing Markdown files")
    parser.add_argument("--theme", default="default", choices=["default", "github", "dark"], help="CSS theme to use")
    parser.add_argument("--extra-css", help="Inline CSS appended to the selected theme")
    parser.add_argument("--output-folder", default="html", help="Name of the output directory (default: html)")


def _md_kwargs(ns: argparse.Namespace) -> Dict[str, object]:
    return {
        "source_folder": ns.source,
        "theme": ns.theme,
        "extra_css": ns.extra_css,
        "output_folder_name": ns.output_folder,
    }


def _text_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("source", help="Folder containing text files")
    parser.add_argument("--font-name", default="Courier", help="Name of the font to use")
    parser.add_argument("--font-path", help="Path to a TTF font to register")
    parser.add_argument("--font-size", type=int, default=12, help="Font size in points")
    parser.add_argument("--margin", type=float, default=1.0, help="Page margin in inches")
    parser.add_argument("--output-folder", default="pdf", help="Name of the output directory (default: pdf)")


def _text_kwargs(ns: argparse.Namespace) -> Dict[str, object]:
    return {
        "source_folder": ns.source,
        "font_name": ns.font_name,
        "font_path": ns.font_path,
        "font_size": ns.font_size,
        "margin": ns.margin,
        "output_folder_name": ns.output_folder,
    }


CONVERTERS: Mapping[str, ConverterSpec] = {
    "img2webp": ConverterSpec(
        func=convert_images_to_webp,
        help="Convert bitmap images to WebP format",
        options=_img_options,
        namespace_to_kwargs=_img_kwargs,
    ),
    "csv2json": ConverterSpec(
        func=convert_csv_to_json,
        help="Convert CSV files into JSON documents",
        options=_csv_options,
        namespace_to_kwargs=_csv_kwargs,
    ),
    "md2html": ConverterSpec(
        func=convert_markdown_to_html,
        help="Render Markdown documents as HTML",
        options=_md_options,
        namespace_to_kwargs=_md_kwargs,
    ),
    "text2pdf": ConverterSpec(
        func=convert_text_to_pdf,
        help="Generate PDF files from plain text",
        options=_text_options,
        namespace_to_kwargs=_text_kwargs,
    ),
}


def _add_subcommands(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="command")
    for name, spec in CONVERTERS.items():
        sub = subparsers.add_parser(name, help=spec.help)
        spec.options(sub)
        sub.set_defaults(_converter=name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A swiss-army knife for common file format conversions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--list", action="store_true", help="List available converters")
    _add_subcommands(parser)
    return parser


def _print_available() -> None:
    print("Available converters:\n")
    for name, spec in CONVERTERS.items():
        print(f"  {name:<10} {spec.help}")


def _render_result(result: ConversionResult) -> None:
    if result.output_directory:
        print(f"\nOutput directory: {result.output_directory}")
    print(f"Converted {result.total_converted} file(s)")
    if result.total_skipped:
        print(f"Skipped {result.total_skipped} file(s)")
    if result.total_errors:
        print(f"Encountered {result.total_errors} error(s):")
        for path, message in result.errors:
            print(f"  - {path}: {message}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list or not getattr(args, "_converter", None):
        _print_available()
        return 0

    spec = CONVERTERS[args._converter]
    kwargs = spec.namespace_to_kwargs(args)

    try:
        result = spec.func(**kwargs)
    except Exception as exc:
        parser.error(str(exc))
        return 1

    _render_result(result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
