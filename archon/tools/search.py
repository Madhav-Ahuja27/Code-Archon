"""Search tools: ripgrep and ctags."""

from __future__ import annotations

import logging
import re
import subprocess
from pathlib import Path

from pydantic import BaseModel

log = logging.getLogger(__name__)


class SearchMatch(BaseModel):
    file: str
    line: int
    text: str


_LINE_RX = re.compile(r"^(.+?):(\d+):(.*)$")


def _parse_rg_output(lines: list[str]) -> list[SearchMatch]:
    """Parse `file:lineno:text` lines. The file part is non-greedy so Windows
    drive letters ("C:\\dir\\f.py:12:text") are not split at the first colon."""
    out = []
    for line in lines:
        m = _LINE_RX.match(line)
        if m:
            out.append(SearchMatch(file=m.group(1), line=int(m.group(2)),
                                   text=m.group(3).strip()))
    return out


def ripgrep(pattern: str, path: str | Path, max_results: int = 100,
            ignore_case: bool = False) -> list[SearchMatch]:
    """Search for pattern using ripgrep (rg); pure-Python fallback if rg is missing."""
    p = Path(path)
    matches: list[SearchMatch] = []

    # Try rg first. Decode as UTF-8 explicitly: Windows would otherwise use cp1252
    # and crash the subprocess reader thread on non-ASCII source files.
    try:
        result = subprocess.run(
            ["rg", "--line-number", "--no-heading"] + (["-i"] if ignore_case else [])
            + [pattern, str(p)],
            capture_output=True, encoding="utf-8", errors="replace", timeout=30,
        )
        if result.returncode in (0, 1):
            matches = _parse_rg_output((result.stdout or "").strip().splitlines())
            return matches[:max_results]
    except FileNotFoundError:
        log.info("rg not found, using pure-Python search")
    except Exception as e:
        log.warning("ripgrep error: %s", e)

    # Fallback: pure-Python search (works on Windows with no rg/grep)
    try:
        rx = re.compile(pattern, re.I if ignore_case else 0)
    except re.error:
        rx = re.compile(re.escape(pattern), re.I if ignore_case else 0)
    skip = {".git", "__pycache__", "venv", ".venv", "node_modules"}
    files = [p] if p.is_file() else [
        f for f in p.rglob("*") if f.is_file() and not (skip & set(f.parts))
    ]
    for f in files:
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if rx.search(line):
                    matches.append(SearchMatch(file=str(f), line=i, text=line.strip()))
                    if len(matches) >= max_results:
                        return matches
        except OSError:
            continue
    return matches


def ctags_index(path: str | Path) -> list[dict]:
    """Run universal-ctags on path, return tag entries."""
    p = Path(path)
    tags: list[dict] = []
    try:
        result = subprocess.run(
            ["ctags", "--output-format=json", "-R", str(p)],
            capture_output=True, encoding="utf-8", errors="replace", timeout=60,
        )
        if result.returncode == 0:
            import json
            for line in result.stdout.strip().splitlines():
                try:
                    tags.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    except FileNotFoundError:
        log.info("ctags not installed — skipping")
    except Exception as e:
        log.warning("ctags error: %s", e)
    return tags
