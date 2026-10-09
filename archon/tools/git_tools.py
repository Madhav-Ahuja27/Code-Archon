"""Git tools: log, blame, diff via gitpython."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

log = logging.getLogger(__name__)


class Commit(BaseModel):
    sha: str
    author: str
    date: str
    message: str
    files_changed: list[str] = []


def git_log(repo_path: str | Path, n: int = 20) -> list[Commit]:
    """Return last n commits from repo."""
    try:
        import git
        repo = git.Repo(str(repo_path), search_parent_directories=True)
        commits = []
        for c in list(repo.iter_commits(max_count=n)):
            commits.append(Commit(
                sha=c.hexsha[:10],
                author=str(c.author),
                date=str(c.authored_datetime),
                message=c.message.strip().splitlines()[0][:120],
                files_changed=list(c.stats.files.keys()),
            ))
        return commits
    except Exception as e:
        log.warning("git_log error: %s", e)
        return []


def git_blame(file_path: str | Path, line: int) -> Optional[str]:
    """Return author of a specific line."""
    try:
        import git
        repo = git.Repo(str(file_path), search_parent_directories=True)
        blame = repo.blame("HEAD", str(file_path))
        current_line = 1
        for commit, lines in blame:
            for _ in lines:
                if current_line == line:
                    return str(commit.author)
                current_line += 1
    except Exception as e:
        log.warning("git_blame error: %s", e)
    return None


def git_diff(
    repo_path: str | Path,
    sha1: str,
    sha2: str = "HEAD",
) -> str:
    """Return unified diff between two commits."""
    try:
        import git
        repo = git.Repo(str(repo_path), search_parent_directories=True)
        diff = repo.git.diff(sha1, sha2)
        return diff
    except Exception as e:
        log.warning("git_diff error: %s", e)
        return ""
