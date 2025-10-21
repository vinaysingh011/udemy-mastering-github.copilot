#!/usr/bin/env python3
"""Print system uptime (reads /proc/uptime) with improved security and reliability."""

from __future__ import annotations

import argparse
import logging
import os
import platform
import sys
from typing import Optional


def _read_uptime_seconds(path: str = "/proc/uptime") -> float:
    """Read and return the uptime in seconds from the given uptime file.

    Raises FileNotFoundError, PermissionError, ValueError on invalid contents.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"uptime file does not exist: {path}")
    # Open with explicit encoding and no buffering surprises
    with open(path, "rt", encoding="utf-8") as f:
        data = f.read().strip()
    if not data:
        raise ValueError("uptime file is empty")
    token = data.split()[0]
    try:
        secs = float(token)
    except ValueError as exc:
        raise ValueError(f"unexpected uptime value: {token!r}") from exc
    if secs < 0:
        raise ValueError("uptime value is negative")
    return secs


def _format_uptime(seconds: float, show_days: bool = True) -> str:
    total = int(seconds)
    days, rem = divmod(total, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    time_part = f"{hours:02d}:{minutes:02d}:{secs:02d}"
    if show_days and days:
        return f"{days} day{'s' if days != 1 else ''}, {time_part}"
    return time_part


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Print system uptime (reads /proc/uptime).")
    p.add_argument(
        "--seconds",
        action="store_true",
        help="print raw uptime seconds instead of formatted H:M:S",
    )
    p.add_argument(
        "--path",
        default="/proc/uptime",
        help="path to uptime file (default: /proc/uptime)",
    )
    p.add_argument(
        "--debug",
        action="store_true",
        help="enable debug logging",
    )
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )
    logger = logging.getLogger(__name__)

    if platform.system() != "Linux":
        logger.error("This script expects a Linux /proc/uptime file.")
        return 2

    try:
        secs = _read_uptime_seconds(args.path)
        if args.seconds:
            # printing raw seconds is useful for scripts; use repr to avoid locale surprises
            print(f"{secs:.3f}")
        else:
            print(_format_uptime(secs, show_days=True))
        return 0
    except FileNotFoundError as e:
        logger.error("uptime file not found: %s", e)
        return 3
    except PermissionError as e:
        logger.error("permission denied reading uptime file: %s", e)
        return 4
    except ValueError as e:
        logger.error("invalid uptime file contents: %s", e)
        logger.debug("raw path contents may be malformed; path=%s", args.path)
        return 5
    except Exception as e:  # pragma: no cover - unexpected errors
        logger.exception("unexpected error reading uptime: %s", e)
        return 10


if __name__ == "__main__":
    raise SystemExit(main())