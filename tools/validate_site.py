#!/usr/bin/env python3
"""Validate internal links and required static metadata files for Pages deploy."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote


def resolve_target(root: Path, html_file: Path, raw_target: str) -> Path:
    target = raw_target.split("#", 1)[0].split("?", 1)[0].strip()
    target = unquote(target)
    if target.startswith("/"):
        return root / target.lstrip("/")
    return (html_file.parent / target).resolve().relative_to(root.resolve())


def main() -> int:
    root = Path(".")
    errors: list[str] = []

    attr_pattern = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
    skip_prefixes = ("http://", "https://", "//", "mailto:", "tel:", "javascript:", "data:")

    # Add intentional exceptions here if a path should not be treated as a broken link.
    ignored_refs = {
        # '/favicon.ico',
        # '/apple-touch-icon.png',
    }
    ignored_prefixes = (
        # '/external/',
    )

    for html_file in root.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        for ref in attr_pattern.findall(content):
            ref = ref.strip()
            if not ref or ref.startswith(skip_prefixes) or ref.startswith("#"):
                continue
            if ref in ignored_refs or any(ref.startswith(prefix) for prefix in ignored_prefixes):
                continue
            try:
                target = resolve_target(root, html_file, ref)
            except Exception:
                errors.append(f"{html_file}: invalid link format '{ref}'")
                continue
            target_path = root / target
            if target_path.exists():
                continue
            if target_path.is_dir() and (target_path / "index.html").exists():
                continue
            errors.append(f"{html_file}: broken local link '{ref}'")

    robots = root / "robots.txt"
    if not robots.exists():
        errors.append("robots.txt is missing")
    else:
        robots_text = robots.read_text(encoding="utf-8", errors="ignore")
        if "Sitemap:" not in robots_text:
            errors.append("robots.txt should include a 'Sitemap:' line")

    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        errors.append("sitemap.xml is missing")
    else:
        try:
            tree = ET.parse(sitemap)
            xml_root = tree.getroot()
            if not xml_root.tag.endswith("urlset"):
                errors.append("sitemap.xml root node should be <urlset>")
            loc_nodes = [
                n
                for n in xml_root.iter()
                if n.tag.endswith("loc") and (n.text or "").strip()
            ]
            if not loc_nodes:
                errors.append("sitemap.xml should contain at least one <loc> URL entry")
        except Exception as exc:
            errors.append(f"sitemap.xml parse error: {exc}")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed: internal links, robots.txt, and sitemap.xml look good.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
