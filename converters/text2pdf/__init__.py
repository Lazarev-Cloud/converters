"""Plain text → PDF converter."""
from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Iterable, Sequence, Tuple

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from ..utils import ConversionResult, ensure_directory, find_source_files, normalise_source


DEFAULT_PATTERNS: Sequence[str] = ("*.txt", "*.md", "*.markdown")


def _register_font(font_name: str, font_path: str | None) -> None:
    if font_path:
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    else:
        # Ensure the font is available. ReportLab raises an exception if the
        # font is unknown when used, so we trigger a measurement as a check.
        pdfmetrics.getAscentDescent(font_name)


def _wrap_lines(text: str, font_name: str, font_size: int, width: float) -> Iterable[str]:
    char_width = pdfmetrics.stringWidth("M", font_name, font_size)
    max_chars = max(10, int(width // char_width))
    wrapper = textwrap.TextWrapper(width=max_chars, replace_whitespace=False, drop_whitespace=False)
    for paragraph in text.splitlines():
        if not paragraph:
            yield ""
            continue
        for line in wrapper.wrap(paragraph):
            yield line


def convert_text_to_pdf(
    source_folder: str | Path,
    *,
    font_name: str = "Courier",
    font_path: str | None = None,
    font_size: int = 12,
    margin: float = 1.0,
    page_size: Tuple[float, float] = A4,
    output_folder_name: str = "pdf",
    patterns: Sequence[str] = DEFAULT_PATTERNS,
) -> ConversionResult:
    """Convert text files within ``source_folder`` to PDF documents."""

    if font_size <= 0:
        raise ValueError("font_size must be positive")
    if margin < 0:
        raise ValueError("margin must be zero or positive")

    source = normalise_source(source_folder)
    output_dir = ensure_directory(source / output_folder_name)
    result = ConversionResult(output_directory=output_dir)

    text_files = find_source_files(source, patterns)
    if not text_files:
        return result

    margin_points = margin * inch
    page_width, page_height = page_size
    text_width = page_width - 2 * margin_points
    try:
        _register_font(font_name, font_path)
    except Exception as exc:
        raise RuntimeError(f"Unable to register font '{font_name}': {exc}") from exc

    for text_path in text_files:
        destination = output_dir / f"{text_path.stem}.pdf"
        try:
            text = text_path.read_text(encoding="utf-8")
        except Exception as exc:
            result.add_error(text_path, f"failed to read file: {exc}")
            continue

        try:
            document = canvas.Canvas(str(destination), pagesize=page_size)
            document.setFont(font_name, font_size)
            cursor_y = page_height - margin_points
            line_height = font_size * 1.2

            for line in _wrap_lines(text, font_name, font_size, text_width):
                if cursor_y < margin_points + line_height:
                    document.showPage()
                    document.setFont(font_name, font_size)
                    cursor_y = page_height - margin_points
                if line:
                    document.drawString(margin_points, cursor_y, line)
                cursor_y -= line_height

            document.save()
        except Exception as exc:
            destination.unlink(missing_ok=True)
            result.add_error(text_path, f"failed to write PDF: {exc}")
            continue

        result.add_converted(text_path, destination)

    return result


__all__ = ["convert_text_to_pdf", "ConversionResult"]
