"""Tests for tools/claude-handoff.py."""


def test_save_creates_a_handoff(run_tool):
    r = run_tool("claude-handoff", "save", "--note", "OAuth done, next: email verification")
    assert r.returncode == 0
    assert "Handoff saved" in r.stdout


def test_load_returns_most_recent_by_default(run_tool):
    run_tool("claude-handoff", "save", "--note", "first note")
    loaded = run_tool("claude-handoff", "load")
    assert loaded.returncode == 0
    assert "first note" in loaded.stdout
    assert "Resume Prompt" in loaded.stdout


def test_load_with_no_handoffs_fails_clearly(run_tool):
    r = run_tool("claude-handoff", "load")
    assert r.returncode == 1
    assert "No handoffs found" in r.stderr


def test_list_shows_saved_handoffs(run_tool):
    run_tool("claude-handoff", "save", "--note", "note A")
    listed = run_tool("claude-handoff", "list")
    assert listed.returncode == 0
    assert "note A" in listed.stdout


def test_show_specific_id(run_tool):
    save = run_tool("claude-handoff", "save", "--note", "note B")
    hid = save.stdout.splitlines()[0].split(":")[-1].strip()

    shown = run_tool("claude-handoff", "show", "--id", hid)
    assert shown.returncode == 0
    assert "note B" in shown.stdout


def test_clean_with_no_old_handoffs_deletes_nothing(run_tool):
    run_tool("claude-handoff", "save", "--note", "fresh")
    r = run_tool("claude-handoff", "clean", "--days", "30", "--force")
    assert r.returncode == 0
    assert "No handoffs older than" in r.stdout

    still_there = run_tool("claude-handoff", "list")
    assert "fresh" in still_there.stdout
