"""Tests for tools/claude-lessons.py."""


def test_no_lessons_yet(run_tool):
    r = run_tool("claude-lessons", "list")
    assert r.returncode == 0
    assert "No lessons recorded yet." in r.stdout


def test_add_and_show(run_tool):
    r = run_tool(
        "claude-lessons",
        "add",
        "--title",
        "Migration timed out",
        "--tags",
        "db,migration",
        "--symptom",
        "ALTER TABLE locked prod for 4min",
        "--cause",
        "no lock_timeout set",
        "--fix",
        "added SET lock_timeout='2s' before DDL",
    )
    assert r.returncode == 0
    assert "Lesson saved" in r.stdout

    shown = run_tool("claude-lessons", "show")
    assert shown.returncode == 0
    assert "Migration timed out" in shown.stdout
    assert "no lock_timeout set" in shown.stdout


def test_rapid_add_does_not_collide(run_tool):
    """Regression test: two adds in the same second must not overwrite each other."""
    first = run_tool(
        "claude-lessons", "add", "--title", "first", "--symptom", "s", "--cause", "c", "--fix", "f"
    )
    second = run_tool(
        "claude-lessons", "add", "--title", "second", "--symptom", "s", "--cause", "c", "--fix", "f"
    )
    assert first.returncode == 0
    assert second.returncode == 0

    listed = run_tool("claude-lessons", "list")
    assert "first" in listed.stdout
    assert "second" in listed.stdout
    assert "2 lesson(s)" in listed.stdout


def test_list_filters_by_tag(run_tool):
    run_tool(
        "claude-lessons",
        "add",
        "--title",
        "db one",
        "--tags",
        "db",
        "--symptom",
        "s",
        "--cause",
        "c",
        "--fix",
        "f",
    )
    run_tool(
        "claude-lessons",
        "add",
        "--title",
        "ci one",
        "--tags",
        "ci",
        "--symptom",
        "s",
        "--cause",
        "c",
        "--fix",
        "f",
    )

    db_only = run_tool("claude-lessons", "list", "--tag", "db")
    assert "db one" in db_only.stdout
    assert "ci one" not in db_only.stdout


def test_search_by_keyword(run_tool):
    run_tool(
        "claude-lessons",
        "add",
        "--title",
        "x",
        "--tags",
        "db",
        "--symptom",
        "lock_timeout missing",
        "--cause",
        "c",
        "--fix",
        "f",
    )

    found = run_tool("claude-lessons", "search", "lock_timeout")
    assert "1 match(es)" in found.stdout

    not_found = run_tool("claude-lessons", "search", "nonexistent-xyz")
    assert "No lessons matching" in not_found.stdout


def test_context_pipeable_output(run_tool):
    run_tool(
        "claude-lessons",
        "add",
        "--title",
        "x",
        "--tags",
        "db",
        "--symptom",
        "s",
        "--cause",
        "c",
        "--fix",
        "f",
    )

    ctx = run_tool("claude-lessons", "context", "--limit", "1")
    assert ctx.returncode == 0
    assert "Lessons Learned" in ctx.stdout
    assert "x" in ctx.stdout


def test_show_missing_id_exits_nonzero(run_tool):
    run_tool(
        "claude-lessons", "add", "--title", "x", "--symptom", "s", "--cause", "c", "--fix", "f"
    )
    r = run_tool("claude-lessons", "show", "--id", "does-not-exist")
    assert r.returncode == 1


def test_add_requires_title(run_tool):
    r = run_tool(
        "claude-lessons", "add", "--symptom", "s", "--cause", "c", "--fix", "f", input="\n"
    )  # empty title when prompted
    assert r.returncode == 2
