#!/usr/bin/env python3
"""
mcp-lessons-server.py — Example MCP server exposing claude-lessons as MCP tools.

Wraps tools/claude-lessons.py (see ../docs/MCP-GUIDE.md) so Claude Code can call
add_lesson / search_lessons / recent_lessons directly, instead of a human running
the CLI and pasting output back in.

This lives in examples/, not tools/, because it needs the optional `mcp` package.
Everything under tools/ must stay stdlib-only (see docs/CONTRIBUTING.md).

Setup:
    pip install "mcp>=1.2,<2"
    # `mcp` 2.x is a breaking rewrite (FastMCP moved/renamed) — pin <2 for this API.

Register with Claude Code:
    claude mcp add lessons -- python3 /path/to/examples/mcp-lessons-server.py

Quick manual check (starts a stdio server, waits for a client — Ctrl+C to stop):
    python3 examples/mcp-lessons-server.py
"""

import importlib.util
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# tools/claude-lessons.py has a hyphen in its filename, so it can't be
# `import`ed normally — load it by path and reuse its storage functions
# directly instead of re-implementing the lesson file format here.
_TOOL_PATH = Path(__file__).resolve().parent.parent / "tools" / "claude-lessons.py"
_spec = importlib.util.spec_from_file_location("claude_lessons", _TOOL_PATH)
claude_lessons = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(claude_lessons)

mcp = FastMCP("claude-lessons")


@mcp.tool()
def add_lesson(title: str, symptom: str, cause: str, fix: str, tags: str = "") -> str:
    """Record a lesson: what failed, why it happened, and how it was fixed."""
    claude_lessons.LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    doc = claude_lessons._build_lesson_doc(title, tags, symptom, cause, fix)
    lid = claude_lessons._lesson_id()
    claude_lessons._lesson_path(lid).write_text(doc, encoding="utf-8")
    return f"Saved lesson {lid}"


@mcp.tool()
def search_lessons(query: str) -> str:
    """Search past lessons by keyword. Returns matches, most recent first."""
    items = claude_lessons._list_lessons()
    matches = [i for i in items if query.lower() in i["content"].lower()]
    if not matches:
        return f"No lessons matching '{query}'."
    return "\n---\n".join(i["content"] for i in matches[:10])


@mcp.tool()
def recent_lessons(limit: int = 5, tag: str = "") -> str:
    """Get the most recent lessons, optionally filtered by tag.

    Call this before starting work in an unfamiliar area, so past failures
    and their fixes are in context before you repeat them.
    """
    items = claude_lessons._list_lessons()
    if tag:
        items = [i for i in items if tag.lower() in i["tags"].lower()]
    items = items[:limit]
    if not items:
        return "No lessons recorded yet."
    return "\n---\n".join(i["content"] for i in items)


if __name__ == "__main__":
    mcp.run(transport="stdio")
