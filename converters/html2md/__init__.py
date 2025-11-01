"""HTML → Markdown converter."""
from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Callable, Sequence, cast

from ..utils import ConversionResult, ensure_directory, find_source_files, normalise_source


DEFAULT_PATTERNS: Sequence[str] = ("*.html", "*.htm")


def _load_markdownify() -> Callable[..., str]:
    """Import markdownify lazily to keep the dependency optional."""

    try:
        module = import_module("markdownify")
    except ImportError as exc:  # pragma: no cover - import failure handled at runtime
        raise RuntimeError(
            "markdownify is required for html2md. Install it with 'pip install markdownify'."
        ) from exc

    markdownify = getattr(module, "markdownify", None)
    if not callable(markdownify):  # pragma: no cover - defensive programming
        raise RuntimeError("markdownify package is missing the 'markdownify' callable")

    return cast(Callable[..., str], markdownify)


def convert_html_to_markdown(
    source_folder: str | Path,
    *,
    heading_style: str = "ATX",
    bullets: str = "-",
    wrap_width: int = 0,
    output_folder_name: str = "markdown",
) -> ConversionResult:
    """Convert HTML documents inside ``source_folder`` to Markdown files."""

    source = normalise_source(source_folder)
    output_dir = ensure_directory(source / output_folder_name)
    result = ConversionResult(output_directory=output_dir)

    html_files = find_source_files(source, DEFAULT_PATTERNS)
    if not html_files:
        return result

    markdownify = _load_markdownify()

    for html_path in html_files:
        destination = output_dir / f"{html_path.stem}.md"
        try:
            html = html_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            result.add_error(html_path, f"failed to read file: {exc}")
            continue

        try:
            markdown_text = markdownify(
                html,
                heading_style=heading_style,
                bullets=bullets,
                wrap_width=None if wrap_width <= 0 else wrap_width,
            )
        except (TypeError, ValueError) as exc:
            result.add_error(html_path, f"failed to convert HTML: {exc}")
            continue

        try:
            destination.write_text(markdown_text.strip() + "\n", encoding="utf-8")
        except OSError as exc:
            result.add_error(html_path, f"failed to write Markdown: {exc}")
            destination.unlink(missing_ok=True)
            continue

        result.add_converted(html_path, destination)

    return result


__all__ = ["convert_html_to_markdown", "ConversionResult"]
