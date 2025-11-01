"""CSV → JSON converter."""
from __future__ import annotations

import csv
import json
from csv import Dialect, DictReader, Sniffer
from pathlib import Path
from typing import Sequence

from ..utils import ConversionResult, ensure_directory, find_source_files, normalise_source


DEFAULT_PATTERNS: Sequence[str] = ("*.csv", "*.CSV")


def _detect_dialect(csv_path: Path, encoding: str, sample_size: int = 4096) -> Dialect:
    """Best-effort dialect detection with a safe fallback."""

    with csv_path.open("r", encoding=encoding, newline="") as stream:
        sample = stream.read(sample_size)
        stream.seek(0)
        try:
            return Sniffer().sniff(sample)
        except csv.Error:
            return csv.get_dialect("excel")


def _load_rows(csv_path: Path, encoding: str, dialect: Dialect) -> list[dict[str, object]]:
    with csv_path.open("r", encoding=encoding, newline="") as stream:
        reader = DictReader(stream, dialect=dialect)
        rows: list[dict[str, object]] = []
        for row in reader:
            clean_row: dict[str, object] = {}
            for key, value in row.items():
                if key is None:
                    continue
                key = key.strip()
                if value is None or value == "":
                    clean_row[key] = None
                    continue
                value = value.strip()
                if value == "":
                    clean_row[key] = None
                    continue
                if value.isdigit():
                    clean_row[key] = int(value)
                    continue
                try:
                    numeric = float(value)
                except ValueError:
                    numeric = None
                if numeric is not None:
                    clean_row[key] = int(numeric) if numeric.is_integer() else numeric
                    continue
                if value.lower() in {"true", "false"}:
                    clean_row[key] = value.lower() == "true"
                else:
                    clean_row[key] = value
            rows.append(clean_row)
        return rows


def _convert_file(
    csv_path: Path,
    *,
    encoding: str,
    pretty_print: bool,
    output_dir: Path,
    result: ConversionResult,
) -> None:
    """Convert ``csv_path`` and record the outcome in ``result``."""

    dialect = _detect_dialect(csv_path, encoding)
    try:
        rows = _load_rows(csv_path, encoding, dialect)
    except (csv.Error, UnicodeDecodeError) as exc:
        result.add_error(csv_path, f"failed to read file: {exc}")
        return

    json_path = output_dir / f"{csv_path.stem}.json"
    try:
        with json_path.open("w", encoding=encoding) as stream:
            json.dump(
                rows,
                stream,
                indent=2 if pretty_print else None,
                ensure_ascii=False,
            )
    except OSError as exc:
        result.add_error(csv_path, f"failed to write JSON: {exc}")
        json_path.unlink(missing_ok=True)
        return

    result.add_converted(csv_path, json_path)


def convert_csv_to_json(
    source_folder: str | Path,
    *,
    pretty_print: bool = True,
    encoding: str = "utf-8",
    output_folder_name: str = "json",
    patterns: Sequence[str] = DEFAULT_PATTERNS,
) -> ConversionResult:
    """Convert all CSV files within ``source_folder`` to JSON.

    Parameters
    ----------
    source_folder:
        Directory containing CSV files.
    pretty_print:
        If ``True`` JSON output is indented.
    encoding:
        Encoding used when reading and writing files.
    output_folder_name:
        Name of the directory created inside ``source_folder`` that will hold
        the generated JSON files.
    patterns:
        Glob patterns that identify CSV files.
    """

    source = normalise_source(source_folder)
    output_dir = ensure_directory(source / output_folder_name)

    result = ConversionResult(output_directory=output_dir)
    csv_files = find_source_files(source, patterns)

    if not csv_files:
        return result

    for csv_path in csv_files:
        _convert_file(
            csv_path,
            encoding=encoding,
            pretty_print=pretty_print,
            output_dir=output_dir,
            result=result,
        )

    return result


__all__ = ["convert_csv_to_json", "ConversionResult"]
