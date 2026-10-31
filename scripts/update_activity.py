#!/usr/bin/env python3
"""Refresh only the marked README activity block using committed repository history."""
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- activity:start -->"
END = "<!-- activity:end -->"
BOT_SUBJECT = "chore: refresh repository activity"
REPO_URL = "https://github.com/Maulenos/MauLab"


def read_commits():
    output = subprocess.check_output(
        ["git", "log", "--format=%H%x09%cI%x09%s"], cwd=ROOT,
        text=True, encoding="utf-8",
    )
    commits = []
    for line in output.splitlines():
        sha, timestamp, subject = line.split("\t", 2)
        if subject == BOT_SUBJECT:
            continue
        commits.append((sha, datetime.fromisoformat(timestamp), subject))
    return commits


def safe_title(subject):
    # Render commit subjects as text, never active Markdown/HTML.
    text = escape(subject, quote=True)
    return re.sub(r"([\\`*_{}\[\]()#+.!|~>-])", r"\\\1", text)


def render_activity(commits, now):
    local = now.astimezone(ZoneInfo("America/Chicago"))
    recent = sum(now - timedelta(hours=24) <= date <= now for _, date, _ in commits)
    summary = (f"**{recent} substantive commit{'s' if recent != 1 else ''} in the last 24 hours.**"
               if recent else "**No new substantive commits in the last 24 hours.**")
    lines = [f"**Last refreshed:** {local:%Y-%m-%d %H:%M %Z}", "", summary, "",
             "Latest changes on the main branch (automated activity refreshes excluded):", ""]
    if not commits:
        lines.append("No substantive commits found.")
    for sha, date, subject in commits[:5]:
        day = date.astimezone(ZoneInfo("America/Chicago")).strftime("%b %d, %Y")
        lines.append(f"- **{day}** · {safe_title(subject)} · [`{sha[:7]}`]({REPO_URL}/commit/{sha})")
    return "\n".join(lines)


def replace_activity(content, block):
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError("README must contain exactly one pair of activity markers")
    before, rest = content.split(START)
    _, after = rest.split(END)  # Also fails if markers are out of order.
    return before + START + "\n" + block + "\n" + END + after


def main():
    readme = ROOT / "README.md"
    current = readme.read_text(encoding="utf-8")
    updated = replace_activity(current, render_activity(read_commits(), datetime.now(timezone.utc)))
    if updated != current:
        readme.write_text(updated, encoding="utf-8", newline="\n")
    print("Repository activity refreshed from Git history.")


if __name__ == "__main__":
    main()
