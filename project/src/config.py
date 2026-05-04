from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    project_root: Path
    raw_input_dirs: list[Path]
    raw_dir: Path
    interim_dir: Path
    processed_dir: Path


DEFAULT_PATHS = Paths(
    project_root=Path(__file__).resolve().parents[1],
    raw_input_dirs=[
        Path(__file__).resolve().parents[1] / "data" / "raw",
        Path(__file__).resolve().parents[2] / "raw_datasets",
    ],
    raw_dir=Path(__file__).resolve().parents[1] / "data" / "raw",
    interim_dir=Path(__file__).resolve().parents[1] / "data" / "interim",
    processed_dir=Path(__file__).resolve().parents[1] / "data" / "processed",
)
