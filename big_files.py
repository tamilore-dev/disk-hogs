#!/usr/bin/env python3
# Name:        big_files.py
# Description: Finds the largest files in a directory tree and prints
#              the top N results, sorted by size (largest first).
# Usage:       python big_files.py <path> [--top N]
#              ./big_files.py <path> [--top N]   (after chmod +x)
# Input:       A directory path (positional). Optional --top N (default 5).
# Output:      Ranked list of files with human-readable sizes to stdout.
# Exit codes:  0 = success
#              1 = path does not exist
#              2 = path is not a directory
# Author:      tamilore-dev
# Created:     2026-10-16
# Notes:       Skips files it cannot stat (permission errors, broken
#              symlinks). Read-only — never writes or deletes anything.
#              Safe under cron (no interactive prompts).

import argparse
from pathlib import Path


def human_size(num_bytes: float) -> str:
    """Convert bytes to a human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"


def find_big_files(folder: Path, top: int) -> list[tuple[Path, int]]:
    """Find the largest files in a directory."""
    files: list[tuple[Path, int]] = []
    for file in folder.rglob("*"):
        if not file.is_file():
            continue
        try:
            size = file.stat().st_size
        except (PermissionError, OSError):
            continue  # skip files we can't read
        files.append((file, size))

    files.sort(key=lambda pair: pair[1], reverse=True)
    return files[:top]


def get_directory(path: Path) -> Path:
    """Check that the path exists and is a directory. Return the path if valid, else raise an exception."""
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path.resolve()}")
    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path.resolve()}")
    return path


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Find the largest files in a directory",
        epilog="Example: big_files.py /var/log --top 10",
    )
    parser.add_argument("path", type=Path, help="Directory to scan")
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="How many files to show (default: 5)",
    )
    args = parser.parse_args()

    try:
        target_dir = get_directory(args.path)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(e)
        return

    files = find_big_files(target_dir, top=args.top)
    if not files:
        print(f"No files found under {target_dir}.")
        return

    print(f"Top {args.top} files for {target_dir.resolve()} are:\n")
    for file, size in files:
        print(f"{human_size(size):>10}  {file}")


if __name__ == "__main__":
    main()
