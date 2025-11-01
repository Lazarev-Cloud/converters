"""Plain text → PDF converter."""
from __future__ import annotations

import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence, Tuple

from ..utils import ConversionResult, ensure_directory, find_source_files, normalise_source


DEFAULT_PATTERNS: Sequence[str] = ("*.txt", "*.md", "*.markdown")
DEFAULT_PAGE_SIZE: Tuple[float, float] = (595.2755905511812, 841.8897637795277)  # A4 in points
POINTS_PER_INCH = 72.0


@dataclass
class TextToPdfLayout:
    """Layout options for :func:`convert_text_to_pdf`."""

    font_name: str = "Courier"
    font_path: str | None = None
    font_size: int = 12
    margin: float = 1.0
    page_size: Tuple[float, float] = DEFAULT_PAGE_SIZE


@dataclass
class _PdfContext:
    """Execution context shared across conversions."""

    pdfmetrics: Any
    canvas: Any
    margin_points: float
    page_dimensions: Tuple[float, float]


def _load_reportlab() -> tuple[Any, Any, Any]:
    """Import ReportLab lazily to keep the dependency optional."""

    try:
        from reportlab.pdfbase import pdfmetrics  # type: ignore import  # pylint: disable=import-outside-toplevel
        from reportlab.pdfbase.ttfonts import TTFont  # type: ignore import  # pylint: disable=import-outside-toplevel
        from reportlab.pdfgen import canvas  # type: ignore import  # pylint: disable=import-outside-toplevel
    except ImportError as exc:  # pragma: no cover - import failure handled at runtime
        raise RuntimeError(
            "reportlab is required for text2pdf. Install it with 'pip install reportlab'."
        ) from exc
    return pdfmetrics, TTFont, canvas


def _register_font(
    font_name: str,
    font_path: str | None,
    pdfmetrics_module: Any,
    ttfont_cls: Any,
) -> None:
    """Ensure ``font_name`` is available for rendering."""

    if font_path:
        pdfmetrics_module.registerFont(ttfont_cls(font_name, font_path))
    else:
        pdfmetrics_module.getAscentDescent(font_name)


def _wrap_lines(
    text: str,
    font_name: str,
    font_size: int,
    width: float,
    pdfmetrics_module: Any,
) -> Iterable[str]:
    """Yield wrapped lines that fit into ``width``."""

    char_width = pdfmetrics_module.stringWidth("M", font_name, font_size)
    max_chars = max(10, int(width // max(char_width, 1)))
    wrapper = textwrap.TextWrapper(
        width=max_chars,
        replace_whitespace=False,
        drop_whitespace=False,
    )
    for paragraph in text.splitlines():
        if not paragraph:
            yield ""
            continue
        yield from wrapper.wrap(paragraph)


def _convert_single(
    text_path: Path,
    layout: TextToPdfLayout,
    output_dir: Path,
    context: _PdfContext,
    result: ConversionResult,
) -> None:
    """Convert ``text_path`` to PDF and record the outcome."""

    destination = output_dir / f"{text_path.stem}.pdf"
    page_width, page_height = context.page_dimensions
    text_width = page_width - 2 * context.margin_points

    try:
        text = text_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        result.add_error(text_path, f"failed to read file: {exc}")
        return

    try:
        document = context.canvas.Canvas(str(destination), pagesize=layout.page_size)
        document.setFont(layout.font_name, layout.font_size)
        cursor_y = page_height - context.margin_points
        line_height = layout.font_size * 1.2

        for line in _wrap_lines(
            text,
            layout.font_name,
            layout.font_size,
            text_width,
            context.pdfmetrics,
        ):
            if cursor_y < context.margin_points + line_height:
                document.showPage()
                document.setFont(layout.font_name, layout.font_size)
                cursor_y = page_height - context.margin_points
            if line:
                document.drawString(context.margin_points, cursor_y, line)
            cursor_y -= line_height

        document.save()
    except (OSError, ValueError) as exc:
        destination.unlink(missing_ok=True)
        result.add_error(text_path, f"failed to write PDF: {exc}")
        return

    result.add_converted(text_path, destination)


def convert_text_to_pdf(
    source_folder: str | Path,
    *,
    output_folder_name: str = "pdf",
    layout: TextToPdfLayout | None = None,
) -> ConversionResult:
    """Convert text files within ``source_folder`` to PDF documents."""

    layout = layout or TextToPdfLayout()
    if layout.font_size <= 0:
        raise ValueError("font_size must be positive")
    if layout.margin < 0:
        raise ValueError("margin must be zero or positive")

    source = normalise_source(source_folder)
    output_dir = ensure_directory(source / output_folder_name)
    result = ConversionResult(output_directory=output_dir)

    text_files = find_source_files(source, DEFAULT_PATTERNS)
    if not text_files:
        return result

    pdfmetrics_module, ttfont_cls, canvas_module = _load_reportlab()

    margin_points = layout.margin * POINTS_PER_INCH
    page_dimensions = layout.page_size
    try:
        _register_font(layout.font_name, layout.font_path, pdfmetrics_module, ttfont_cls)
    except (OSError, ValueError, FileNotFoundError) as exc:
        raise RuntimeError(f"Unable to register font '{layout.font_name}': {exc}") from exc

    context = _PdfContext(
        pdfmetrics=pdfmetrics_module,
        canvas=canvas_module,
        margin_points=margin_points,
        page_dimensions=page_dimensions,
    )

    for text_path in text_files:
        _convert_single(
            text_path,
            layout,
            output_dir,
            context,
            result,
        )

    return result


__all__ = ["convert_text_to_pdf", "ConversionResult", "TextToPdfLayout"]
