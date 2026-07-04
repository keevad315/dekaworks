#!/usr/bin/env python3
"""Keep shared service-page head block in sync across service pages.

Usage:
  python tools/sync_service_head.py --check
  python tools/sync_service_head.py --write
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER_START = "<!-- shared-service-head:start -->"
MARKER_END = "<!-- shared-service-head:end -->"

SOURCE_FILE = ROOT / "app-development.html"
TARGET_FILES = [
    ROOT / "web-development.html",
    ROOT / "ai-solutions.html",
    ROOT / "consulting.html",
]


def extract_block(text: str) -> str:
    start = text.find(MARKER_START)
    end = text.find(MARKER_END)
    if start == -1 or end == -1 or end < start:
        raise ValueError("missing or invalid shared-service-head markers")
    return text[start : end + len(MARKER_END)]


def replace_block(text: str, block: str) -> str:
    start = text.find(MARKER_START)
    end = text.find(MARKER_END)
    if start == -1 or end == -1 or end < start:
        raise ValueError("missing or invalid shared-service-head markers")
    return text[:start] + block + text[end + len(MARKER_END) :]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Exit non-zero if files are out of sync")
    parser.add_argument("--write", action="store_true", help="Rewrite target files to match source block")
    args = parser.parse_args()

    if not args.check and not args.write:
        parser.error("Specify one of --check or --write")

    source_text = SOURCE_FILE.read_text(encoding="utf-8")
    shared_block = extract_block(source_text)

    out_of_sync = []

    for target in TARGET_FILES:
        target_text = target.read_text(encoding="utf-8")
        updated = replace_block(target_text, shared_block)
        if updated != target_text:
            out_of_sync.append(target.name)
            if args.write:
                target.write_text(updated, encoding="utf-8")

    if out_of_sync and args.check:
        print("Service pages are out of sync for shared-service-head block:")
        for name in out_of_sync:
            print(f"- {name}")
        print("Run: python tools/sync_service_head.py --write")
        return 1

    if out_of_sync and args.write:
        print("Updated shared-service-head block in:")
        for name in out_of_sync:
            print(f"- {name}")
    else:
        print("Shared service head block is in sync.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
