"""Utility helpers shared between converter modules."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Sequence, Tuple


@dataclass
class ConversionResult:
    """Structured summary returned by converter functions.

    Attributes
    ----------
    converted:
        List of ``(source, destination)`` pairs that were successfully converted.
    skipped:
        Files that were intentionally ignored (for example because the output
        already existed).
    errors:
        Tuples containing a path and a human-readable error message.
    output_directory:
        Directory that contains the converted files.
    """

    converted: List[Tuple[Path, Path]] = field(default_factory=list)
    skipped: List[Path] = field(default_factory=list)
    errors: List[Tuple[Path, str]] = field(default_factory=list)
    output_directory: Path | None = None

    def add_converted(self, source: Path, destination: Path) -> None:
        self.converted.append((source, destination))

    def add_skipped(self, path: Path) -> None:
        self.skipped.append(path)

    def add_error(self, path: Path, message: str) -> None:
        self.errors.append((path, message))

    @property
    def total_converted(self) -> int:
        return len(self.converted)

    @property
    def total_skipped(self) -> int:
        return len(self.skipped)

    @property
    def total_errors(self) -> int:
        return len(self.errors)

    def as_dict(self) -> dict:
        """Return a JSON-serialisable summary of the conversion."""

        return {
            "converted": [
                {"source": str(src), "destination": str(dst)}
                for src, dst in self.converted
            ],
            "skipped": [str(path) for path in self.skipped],
            "errors": [{"path": str(path), "message": message} for path, message in self.errors],
            "output_directory": str(self.output_directory) if self.output_directory else None,
        }


def ensure_directory(path: Path) -> Path:
    """Create ``path`` (including parents) if it does not exist and return it."""

    path.mkdir(parents=True, exist_ok=True)
    return path


def find_source_files(source: Path, patterns: Sequence[str]) -> List[Path]:
    """Collect input files matching ``patterns`` within ``source``.

    Parameters
    ----------
    source:
        Directory to search in.
    patterns:
        Glob patterns relative to ``source``.
    """

    files = set()
    for pattern in patterns:
        files.update(source.glob(pattern))
    return sorted(path for path in files if path.is_file())


def normalise_source(source_folder: str | Path) -> Path:
    """Return the canonical :class:`~pathlib.Path` for ``source_folder``.

    Raises
    ------
    FileNotFoundError
        If the provided folder does not exist or is not a directory.
    """

    path = Path(source_folder).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Source folder '{source_folder}' was not found")
    if not path.is_dir():
        raise NotADirectoryError(f"'{source_folder}' is not a directory")
    return path
