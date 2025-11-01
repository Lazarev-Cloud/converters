"""Markdown → HTML converter."""
from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import markdown
from bs4 import BeautifulSoup

from ..utils import ConversionResult, ensure_directory, find_source_files, normalise_source


DEFAULT_PATTERNS: Sequence[str] = ("*.md", "*.markdown")

_THEME_STYLES: Mapping[str, str] = {
    "default": """
        body { font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem auto; max-width: 60rem; line-height: 1.6; color: #222; padding: 0 1.5rem; }
        h1, h2, h3, h4, h5, h6 { font-weight: 600; line-height: 1.2; margin-top: 2rem; }
        h1 { font-size: 2.2rem; border-bottom: 2px solid #eee; padding-bottom: .5rem; }
        h2 { font-size: 1.8rem; border-bottom: 1px solid #eee; padding-bottom: .4rem; }
        pre { background: #f6f8fa; padding: 1rem; border-radius: .5rem; overflow: auto; }
        code { background: rgba(27,31,35,.05); padding: .2rem .4rem; border-radius: .35rem; font-family: ui-monospace, SFMono-Regular, SFMono, Menlo, Consolas, Liberation Mono, monospace; }
        table { border-collapse: collapse; margin: 1.5rem 0; width: 100%; }
        th, td { border: 1px solid #d0d7de; padding: .6rem; text-align: left; }
        blockquote { border-left: .25rem solid #d0d7de; margin: 1rem 0; padding: 0 1rem; color: #57606a; }
    """,
    "github": """
        body { font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem auto; max-width: 60rem; line-height: 1.6; color: #24292f; padding: 0 1.5rem; background: #fff; }
        h1, h2, h3, h4, h5, h6 { font-weight: 600; line-height: 1.25; margin-top: 2rem; }
        h1 { font-size: 2rem; border-bottom: 1px solid #d0d7de; padding-bottom: .5rem; }
        h2 { font-size: 1.6rem; border-bottom: 1px solid #d0d7de; padding-bottom: .4rem; }
        a { color: #0969da; text-decoration: none; }
        a:hover { text-decoration: underline; }
        code { background: rgba(175,184,193,.2); padding: .2rem .4rem; border-radius: .35rem; font-family: ui-monospace, SFMono-Regular, SFMono, Menlo, Consolas, Liberation Mono, monospace; }
        pre { background: #f6f8fa; padding: 1rem; border-radius: .5rem; overflow: auto; }
        table { border-collapse: collapse; margin: 1.5rem 0; width: 100%; }
        th, td { border: 1px solid #d0d7de; padding: .6rem; text-align: left; }
        blockquote { border-left: .25rem solid #d0d7de; margin: 1rem 0; padding: 0 1rem; color: #57606a; }
    """,
    "dark": """
        body { font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem auto; max-width: 60rem; line-height: 1.6; color: #c9d1d9; padding: 0 1.5rem; background: #0d1117; }
        a { color: #58a6ff; }
        h1, h2, h3, h4, h5, h6 { font-weight: 600; line-height: 1.25; margin-top: 2rem; color: #f0f6fc; }
        h1 { font-size: 2rem; border-bottom: 1px solid #21262d; padding-bottom: .5rem; }
        h2 { font-size: 1.6rem; border-bottom: 1px solid #21262d; padding-bottom: .4rem; }
        code { background: rgba(110,118,129,.4); padding: .2rem .4rem; border-radius: .35rem; font-family: ui-monospace, SFMono-Regular, SFMono, Menlo, Consolas, Liberation Mono, monospace; color: #e6edf3; }
        pre { background: #161b22; padding: 1rem; border-radius: .5rem; overflow: auto; }
        table { border-collapse: collapse; margin: 1.5rem 0; width: 100%; }
        th, td { border: 1px solid #30363d; padding: .6rem; text-align: left; }
        blockquote { border-left: .25rem solid #30363d; margin: 1rem 0; padding: 0 1rem; color: #8b949e; }
    """,
}


def convert_markdown_to_html(
    source_folder: str | Path,
    *,
    theme: str = "default",
    extra_css: str | None = None,
    output_folder_name: str = "html",
    patterns: Sequence[str] = DEFAULT_PATTERNS,
) -> ConversionResult:
    """Convert Markdown documents to HTML files."""

    source = normalise_source(source_folder)
    output_dir = ensure_directory(source / output_folder_name)
    result = ConversionResult(output_directory=output_dir)

    markdown_files = find_source_files(source, patterns)
    if not markdown_files:
        return result

    css = _THEME_STYLES.get(theme.lower(), _THEME_STYLES["default"])
    if extra_css:
        css = f"{css}\n{extra_css}"

    extensions = [
        "fenced_code",
        "tables",
        "codehilite",
        "toc",
        "sane_lists",
        "smarty",
    ]

    for md_path in markdown_files:
        destination = output_dir / f"{md_path.stem}.html"
        try:
            text = md_path.read_text(encoding="utf-8")
            html = markdown.markdown(text, extensions=extensions)
            document = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>{md_path.stem}</title>
    <style>
{css}
    </style>
</head>
<body>
{html}
</body>
</html>
"""
            soup = BeautifulSoup(document, "html.parser")
            destination.write_text(soup.prettify(), encoding="utf-8")
        except Exception as exc:
            result.add_error(md_path, str(exc))
            if destination.exists():
                destination.unlink(missing_ok=True)
            continue

        result.add_converted(md_path, destination)

    return result


__all__ = ["convert_markdown_to_html", "ConversionResult"]
