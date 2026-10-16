# big-files-finder

  A small Python CLI that walks a directory tree and prints the largest files
  it finds, sorted by size, with human-readable formatting.

  Built as a sysadmin practice project — the kind of tool you reach for when a
  disk is filling up and you need to find what's eating the space.

  ## Requirements

  • Python 3.10+ (uses `list[tuple[Path, int]]` and `Path | None` syntax)
  • Standard library only — no `pip install` needed
  • Read access to the directory you scan

  ## Usage

  Option A — run with Python (works everywhere):

    python big_files.py <path> [--top N]

  Option B — run as an executable (Unix only):

    chmod +x big_files.py
    ./big_files.py <path> [--top N]

  Examples:

    python big_files.py .
    python big_files.py /var/log --top 20
    ./big_files.py /etc

  `--top` defaults to 5.

  ## Demo

    $ python big_files.py /var/log --top 3

    Top 3 files for /var/log are:
        128.4 MB  /var/log/syslog.1
         42.1 MB  /var/log/journal/abc.journal
         12.0 MB  /var/log/nginx/access.log

  Sizes are formatted with human-readable units (B, KB, MB, GB, TB) using
  1024-based conversion, matching `ls -h` and `du -h`.

  ## How it works

    path ──rglob("*")──► every file ──stat().st_size──► (path, size)
         ──sort by size desc──► slice [:top] ──human_size──► print

  • **Walk the tree** — `Path.rglob("*")` yields every file and directory
    under the given path, recursively.
  • **Filter** — only keep files (`is_file()`), skip anything that raises a
    `PermissionError` or `OSError` when stat'd.
  • **Collect** — build a list of `(path, size_in_bytes)` tuples.
  • **Sort** — by size, descending.
  • **Slice** — take the first N.
  • **Format** — convert bytes to a human-readable string.

  ## Output columns

  | Column | Meaning |
  |---|---|
  | Size   | Human-readable file size, right-aligned |
  | Path   | Full path to the file |

  ## Exit codes

  | Code | Meaning |
  |---|---|
  | 0    | Success (including "no files found") |
  | 1    | Path does not exist |
  | 2    | Path is not a directory |

  ## Notes

  • **Read-only.** Never writes, moves, or deletes anything.
  • **Safe under cron.** No interactive prompts — takes all input from argv.
  • **Graceful on permissions.** Skips files it can't `stat` instead of
    crashing. Run as root to see restricted files like `/var/log/auth.log`.
  • **1024-based units.** 1 KB = 1024 bytes, matching `ls -h`. If you want
    1000-based, change the divisor in `human_size`.
  • **Symlinks are followed.** A symlink to a large file counts as a file.

  ## Files

  | File            | Purpose                    |
  |---|---|
  | `big_files.py`  | The script                 |
  | `README.md`     | This file                  |

  ## Author

  tamilore-dev
