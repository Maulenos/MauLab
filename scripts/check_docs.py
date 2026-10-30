#!/usr/bin/env python3
"""Check the documentation portfolio for basic broken links and formatting.

This is documentation-only validation, not an infrastructure deployment test.
Uses only the Python standard library.
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
FILES = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]


def check_file(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.is_file():
        return [f"{path}: missing file"]
    content = path.read_text(encoding="utf-8")
    if not re.search(r"^#{1,6} \S", content, re.MULTILINE):
        failures.append(f"{path}: missing Markdown heading")

    fences = [
        line for line in content.splitlines()
        if line.lstrip().startswith("```")
    ]
    if len(fences) % 2:
        failures.append(f"{path}: unbalanced fenced code blocks")

    for match in LINK.finditer(content):
        target = match.group(1).strip().split(" ", 1)[0].strip("<>")
        if not target or target.startswith(("#", "https://", "http://", "mailto:", "tel:")):
            continue
        local_path = unquote(target.split("#", 1)[0])
        if not local_path:
            continue
        destination = (path.parent / local_path).resolve()
        if not destination.is_file():
            failures.append(f"{path.relative_to(ROOT)}: broken link: {target}")

    return failures


def main() -> int:
    failures = [error for path in FILES for error in check_file(path)]
    for error in failures:
        print(f"ERROR: {error}")
    if failures:
        print(f"Documentation validation failed: {len(failures)} issue(s)")
        return 1
    print(f"Documentation validation passed: {len(FILES)} Markdown files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
