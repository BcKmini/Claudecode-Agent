"""
Shared fixtures for the tools/*.py test suite.

These CLI tools store all state under ~/.claude/ (or, for claude-remind /
claude-review-diff, the current git repo). Every test runs them as a real
subprocess against an isolated HOME (and, where needed, an isolated git
repo) so tests never touch the machine's actual ~/.claude/ directory and
can run in parallel / repeatedly without interfering with each other.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"


@pytest.fixture
def repo_root():
    return REPO_ROOT


@pytest.fixture
def home(tmp_path):
    """An isolated $HOME for a single test."""
    h = tmp_path / "home"
    h.mkdir()
    return h


@pytest.fixture
def run_tool(home, monkeypatch):
    """
    run_tool("claude-lessons", "add", "--title", "x", ...) -> CompletedProcess

    Runs tools/<name>.py as a real subprocess with HOME pointed at an
    isolated tmp directory and NO_COLOR set (so stdout has no ANSI codes
    to strip in assertions).
    """

    def _run(tool_name, *args, cwd=None, input=None, extra_env=None):
        script = TOOLS_DIR / f"{tool_name}.py"
        assert script.exists(), f"tool script not found: {script}"

        env = dict(os.environ)
        env["HOME"] = str(home)
        env["NO_COLOR"] = "1"
        if extra_env:
            env.update(extra_env)

        return subprocess.run(
            [sys.executable, str(script), *args],
            capture_output=True,
            text=True,
            cwd=str(cwd) if cwd else None,
            input=input,
            env=env,
        )

    return _run


@pytest.fixture
def git_repo(tmp_path):
    """An isolated, initialized git repo with one commit, for tools that shell out to git."""
    repo = tmp_path / "repo"
    repo.mkdir()

    def _git(*args):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)

    _git("init", "-q")
    _git("config", "user.email", "test@example.com")
    _git("config", "user.name", "Test")

    (repo / "README.md").write_text("hello\n", encoding="utf-8")
    _git("add", "README.md")
    _git("commit", "-q", "-m", "initial")

    return repo
