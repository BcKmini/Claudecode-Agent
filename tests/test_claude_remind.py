"""Tests for tools/claude-remind.py."""


def test_no_task_files_found(run_tool, tmp_path):
    r = run_tool("claude-remind", cwd=tmp_path)
    assert r.returncode == 0
    assert "No task files found" in r.stderr


def test_finds_pending_checkboxes(run_tool, tmp_path):
    (tmp_path / "TODO.md").write_text(
        "# TODO\n\n- [ ] Add email verification endpoint\n- [x] Set up OAuth\n",
        encoding="utf-8",
    )
    r = run_tool("claude-remind", cwd=tmp_path)
    assert r.returncode == 0
    assert "Add email verification endpoint" in r.stdout
    assert "Pending Tasks (1 incomplete)" in r.stdout


def test_quiet_flag_prints_count_only(run_tool, tmp_path):
    (tmp_path / "TODO.md").write_text("- [ ] one\n- [ ] two\n", encoding="utf-8")
    r = run_tool("claude-remind", "--quiet", cwd=tmp_path)
    assert r.returncode == 0
    assert "2 pending task(s)" in r.stdout


def test_no_pending_tasks(run_tool, tmp_path):
    (tmp_path / "TODO.md").write_text("- [x] already done\n", encoding="utf-8")
    r = run_tool("claude-remind", cwd=tmp_path)
    assert r.returncode == 0
    assert "No pending tasks found" in r.stderr
