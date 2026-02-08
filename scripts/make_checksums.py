"""Generate/verify SHA256 checksums for dataset files.

Default scope: CSV/Parquet/JSON files under ./data

Why:
- Lets users verify the *data payload* they downloaded matches what you published.
- Keeps integrity checks stable even if docs/scripts change.

Usage:
  python scripts/make_checksums.py
  python scripts/make_checksums.py --check
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Iterable


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUT_FILE = Path(__file__).resolve().parents[1] / "checksums.sha256"
INCLUDE_SUFFIXES = {".csv", ".parquet", ".json"}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_data_files(data_dir: Path) -> Iterable[Path]:
    for p in sorted(data_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in INCLUDE_SUFFIXES:
            yield p


def render_lines(files: Iterable[Path]) -> list[str]:
    lines: list[str] = []
    repo_root = Path(__file__).resolve().parents[1]
    for p in files:
        rel = p.relative_to(repo_root).as_posix()
        lines.append(f"{sha256_file(p)}  {rel}")
    return lines


def read_existing(out_file: Path) -> dict[str, str]:
    if not out_file.exists():
        return {}
    mapping: dict[str, str] = {}
    for line in out_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        checksum = parts[0]
        relpath = parts[1]
        mapping[relpath] = checksum
    return mapping


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check",
        action="store_true",
        help="Verify checksums.sha256 instead of writing it",
    )
    args = ap.parse_args()

    if not DATA_DIR.exists():
        raise SystemExit(f"data/ folder not found: {DATA_DIR}")

    files = list(iter_data_files(DATA_DIR))
    if not files:
        raise SystemExit("No dataset files found under data/")

    lines = render_lines(files)

    if args.check:
        existing = read_existing(OUT_FILE)
        expected = {line.split()[1]: line.split()[0] for line in lines}

        mismatched: list[str] = []
        for rel, chk in expected.items():
            if existing.get(rel) != chk:
                mismatched.append(rel)

        extra = sorted(set(existing.keys()) - set(expected.keys()))

        if mismatched or extra or (not existing):
            if mismatched:
                print(
                    f"Mismatched checksums for {len(mismatched)} files (example: {mismatched[:1]})"
                )
            if extra:
                print(f"Extra entries in checksums.sha256 (example: {extra[:1]})")
            print("checksums.sha256 does not match current data files.")
            print("Re-generate with: python scripts/make_checksums.py")
            return 1

        print("checksums.sha256 matches current data files")
        return 0

    OUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote checksums.sha256 with {len(lines)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
