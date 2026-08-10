#!/usr/bin/env python3
"""
claude-lessons v1.0 -- Failure / lessons-learned log for Claude Code

Handoffs capture session state; lessons capture WHY something failed and
HOW it was fixed, so the next session (or the next agent) doesn't repeat
the same mistake. Unlike handoffs, lessons are meant to accumulate
indefinitely and be searched by tag or keyword.

Homepage: https://github.com/BcKmini/claude-code-use
"""

VERSION = "1.0.0"

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

LESSONS_DIR = Path.home() / ".claude" / "lessons"

# ---------------------------------------------------------------------------
# Color support
# ---------------------------------------------------------------------------

def _enable_win_vt() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        k = ctypes.windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 7)
    except Exception:
        pass


_enable_win_vt()
_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _COLOR else text


def green(s):   return _c("32", s)
def yellow(s):  return _c("33", s)
def cyan(s):    return _c("36", s)
def red(s):     return _c("31", s)
def bold(s):    return _c("1",  s)
def dim(s):     return _c("2",  s)


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

def _lesson_id() -> str:
    """Timestamp-based ID, disambiguated on collision so rapid adds never overwrite."""
    base = datetime.now().strftime("%Y%m%d-%H%M%S")
    if not _lesson_path(base).exists():
        return base
    n = 2
    while _lesson_path(f"{base}-{n}").exists():
        n += 1
    return f"{base}-{n}"


def _lesson_path(lid: str) -> Path:
    return LESSONS_DIR / f"{lid}.md"


def _prompt(label: str) -> str:
    sys.stdout.write(f"{label}: ")
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def _build_lesson_doc(title, tags, symptom, cause, fix) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Lesson — {ts}",
        "",
        f"**Title:** {title}",
        f"**Tags:**  {tags or '(none)'}",
        "",
        "## Symptom",
        symptom or "(not recorded)",
        "",
        "## Root Cause",
        cause or "(not recorded)",
        "",
        "## Fix",
        fix or "(not recorded)",
        "",
    ]
    return "\n".join(lines)


def _parse_lesson(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    title = ""
    tags = ""
    for line in content.splitlines():
        if line.startswith("**Title:**"):
            title = line.replace("**Title:**", "").strip()
        elif line.startswith("**Tags:**"):
            tags = line.replace("**Tags:**", "").strip()
    return {"id": path.stem, "path": path, "title": title, "tags": tags, "content": content}


def _list_lessons() -> list:
    if not LESSONS_DIR.exists():
        return []
    files = sorted(LESSONS_DIR.glob("*.md"), reverse=True)
    items = []
    for f in files:
        try:
            items.append(_parse_lesson(f))
        except Exception:
            pass
    return items


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_add(args):
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)

    title = args.title or _prompt("Title (what went wrong, one line)")
    if not title:
        print(red("[!] Title is required."), file=sys.stderr)
        sys.exit(2)

    tags = args.tags or _prompt("Tags (comma-separated, optional)")
    symptom = args.symptom or _prompt("Symptom (what you observed)")
    cause = args.cause or _prompt("Root cause (why it happened)")
    fix = args.fix or _prompt("Fix (how it was resolved)")

    doc = _build_lesson_doc(title, tags, symptom, cause, fix)
    lid = _lesson_id()
    path = _lesson_path(lid)
    path.write_text(doc, encoding="utf-8")

    print(green(f"[OK] Lesson saved: {lid}"))
    print(dim(f"     {path}"))


def cmd_list(args):
    items = _list_lessons()
    if args.tag:
        needle = args.tag.lower()
        items = [i for i in items if needle in i["tags"].lower()]

    if not items:
        print(yellow("No lessons recorded yet."))
        print(dim("  Run: claude-lessons add"))
        return

    n = args.limit or 20
    items = items[:n]

    print(f"\n  {bold('id'):<22}  {bold('tags'):<24}  {bold('title')}")
    print("  " + dim("-" * 90))
    for item in items:
        print(f"  {cyan(item['id']):<{22+9}}  "
              f"{dim(item['tags'] or '-'):<{24+9}}  "
              f"{item['title']}")
    print(f"\n  {dim(str(len(items)) + ' lesson(s)')}\n")


def cmd_show(args):
    items = _list_lessons()
    if not items:
        print(yellow("No lessons recorded yet."))
        return

    if args.id:
        matches = [i for i in items if i["id"] == args.id]
        if not matches:
            print(red(f"[!] Lesson '{args.id}' not found."), file=sys.stderr)
            sys.exit(1)
        item = matches[0]
    else:
        item = items[0]

    print(item["content"])


def cmd_search(args):
    items = _list_lessons()
    needle = args.query.lower()
    matches = [i for i in items if needle in i["content"].lower()]

    if not matches:
        print(yellow(f"No lessons matching '{args.query}'."))
        return

    print(f"\n  {bold('id'):<22}  {bold('tags'):<24}  {bold('title')}")
    print("  " + dim("-" * 90))
    for item in matches:
        print(f"  {cyan(item['id']):<{22+9}}  "
              f"{dim(item['tags'] or '-'):<{24+9}}  "
              f"{item['title']}")
    print(f"\n  {dim(str(len(matches)) + ' match(es)')}\n")


def cmd_context(args):
    items = _list_lessons()
    if args.tag:
        needle = args.tag.lower()
        items = [i for i in items if needle in i["tags"].lower()]

    n = args.limit or 5
    items = items[:n]

    if not items:
        if sys.stdout.isatty():
            print(dim("No lessons recorded yet. Run: claude-lessons add"), file=sys.stderr)
        return

    print("# Lessons Learned — Context")
    print()
    print("Before proceeding, note the following past failures and their fixes")
    print("so you don't repeat them:")
    print()
    for item in items:
        print(f"---\n{item['content']}")

    if sys.stdout.isatty():
        print(dim("\n-- Tip: pipe to claude:  claude-lessons context | claude"),
              file=sys.stderr)


def cmd_version(args):
    print(f"claude-lessons {bold(VERSION)}")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="claude-lessons",
        description="Failure / lessons-learned log for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  claude-lessons add --title "Migration timed out" --tags db,migration \\
      --symptom "ALTER TABLE locked prod for 4min" \\
      --cause "no lock_timeout set" \\
      --fix "added SET lock_timeout='2s' before DDL"
  claude-lessons list --tag db
  claude-lessons search "lock_timeout"
  claude-lessons context | claude
""",
    )
    p.add_argument("--version", action="version", version=f"claude-lessons {VERSION}")

    sub = p.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    s = sub.add_parser("add", help="Record a new lesson (what failed, why, how it was fixed)")
    s.add_argument("--title", "-t", help="Short title — what went wrong")
    s.add_argument("--tags", help="Comma-separated tags")
    s.add_argument("--symptom", help="What you observed")
    s.add_argument("--cause", help="Root cause")
    s.add_argument("--fix", help="How it was resolved")
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("list", help="List recorded lessons")
    s.add_argument("--limit", "-n", type=int, default=20, help="Max entries to show (default: 20)")
    s.add_argument("--tag", help="Filter by tag substring")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("show", help="Show full lesson content")
    s.add_argument("--id", help="Lesson ID (default: most recent)")
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("search", help="Search lessons by keyword")
    s.add_argument("query", help="Keyword to search for")
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("context",
                       help="Print matching lessons  (pipe to claude for session-start context)")
    s.add_argument("--limit", "-n", type=int, default=5, help="Max lessons to include (default: 5)")
    s.add_argument("--tag", help="Only include lessons matching this tag")
    s.set_defaults(func=cmd_context)

    s = sub.add_parser("version", help="Print version")
    s.set_defaults(func=cmd_version)

    return p


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
