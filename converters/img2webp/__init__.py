"""Image → WebP converter."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from ..utils import ConversionResult, ensure_directory, find_source_files, normalise_source


DEFAULT_PATTERNS: Sequence[str] = (
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.gif",
    "*.bmp",
    "*.tif",
    "*.tiff",
    "*.webp",
)


def _load_pillow() -> tuple[Any, Any]:
    """Import Pillow lazily to keep the dependency optional."""

    try:
        from PIL import Image, ImageSequence  # type: ignore import  # pylint: disable=import-outside-toplevel
    except ImportError as exc:  # pragma: no cover - import failure is handled at runtime
        raise RuntimeError(
            "Pillow is required for img2webp. Install it with 'pip install pillow'."
        ) from exc
    return Image, ImageSequence


def _save_image(
    source: Path,
    destination: Path,
    quality: int,
    lossless: bool,
    pillow_modules: tuple[Any, Any],
) -> None:
    """Transcode ``source`` to WebP and write to ``destination``."""

    image_cls, sequence_cls = pillow_modules

    with image_cls.open(source) as image:  # type: ignore[call-arg,attr-defined]
        if source.suffix.lower() == ".gif" and getattr(image, "is_animated", False):
            iterator = sequence_cls.Iterator(image)  # type: ignore[attr-defined]
            frames = [frame.copy() for frame in iterator]
            frames[0].save(
                destination,
                format="WEBP",
                save_all=True,
                append_images=frames[1:],
                loop=image.info.get("loop", 0),
                duration=image.info.get("duration", 100),
                lossless=lossless,
                quality=quality,
                method=6,
            )
            return

        if image.mode in {"P", "LA", "CMYK"}:
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        elif image.mode == "RGBA" and source.suffix.lower() not in {".png", ".webp"}:
            image = image.convert("RGB")

        image.save(destination, "WEBP", quality=quality, method=6, lossless=lossless)


def convert_images_to_webp(
    source_folder: str | Path,
    *,
    quality: int = 80,
    lossless: bool | None = None,
    skip_existing: bool = True,
    output_folder_name: str = "webp",
) -> ConversionResult:
    """Convert images inside ``source_folder`` to WebP.

    Parameters
    ----------
    quality:
        Target quality (0-100). Ignored for lossless conversions.
    lossless:
        Force lossless encoding. ``None`` lets Pillow pick the best mode based on
        the source image.
    skip_existing:
        If ``True`` the converter will not re-create WebP files that already
        exist in the destination folder.
    output_folder_name:
        Name of the folder created inside ``source_folder`` where the WebP files
        are written.
    """

    if not 0 <= quality <= 100:
        raise ValueError("quality must be between 0 and 100")

    source = normalise_source(source_folder)
    output_dir = ensure_directory(source / output_folder_name)
    result = ConversionResult(output_directory=output_dir)

    image_files = find_source_files(source, DEFAULT_PATTERNS)

    if not image_files:
        return result

    image_module, sequence_module = _load_pillow()

    for image_path in image_files:
        destination = output_dir / f"{image_path.stem}.webp"
        if destination.resolve() == image_path.resolve():
            result.add_skipped(image_path)
            continue
        if skip_existing and destination.exists():
            result.add_skipped(image_path)
            continue

        try:
            _save_image(
                image_path,
                destination,
                quality=quality,
                lossless=lossless or False,
                pillow_modules=(image_module, sequence_module),
            )
        except (OSError, ValueError, RuntimeError) as exc:
            result.add_error(image_path, f"failed to convert image: {exc}")
            if destination.exists():
                destination.unlink(missing_ok=True)
            continue

        result.add_converted(image_path, destination)

    return result


__all__ = ["convert_images_to_webp", "ConversionResult"]
