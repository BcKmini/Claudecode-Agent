"""Tests for tools/claude-pipeline.py."""


def test_init_and_status(run_tool):
    r = run_tool("claude-pipeline", "init", "demo-workflow")
    assert r.returncode == 0
    assert "initialized" in r.stdout

    status = run_tool("claude-pipeline", "status")
    assert status.returncode == 0
    assert "demo-workflow" in status.stdout


def test_stage_lifecycle_and_report(run_tool):
    run_tool("claude-pipeline", "init", "slow-query-fix")
    run_tool("claude-pipeline", "stage", "detection", "start")
    result = run_tool("claude-pipeline", "stage", "detection", "pass", "--note", "found 3 issues")
    assert result.returncode == 0

    report = run_tool("claude-pipeline", "report")
    assert report.returncode == 0
    assert "detection" in report.stdout
    assert "PASS" in report.stdout
    assert "found 3 issues" in report.stdout


def test_list_renders_created_date(run_tool):
    """Regression test: `list` used to be a SyntaxError (nested f-string
    with an escaped quote) and would crash on import, breaking every
    subcommand including --help."""
    run_tool("claude-pipeline", "init", "workflow-a")
    run_tool("claude-pipeline", "init", "workflow-b")

    listed = run_tool("claude-pipeline", "list")
    assert listed.returncode == 0
    assert "workflow-a" in listed.stdout
    assert "workflow-b" in listed.stdout
    assert "stages · created" in listed.stdout
    assert "active" in listed.stdout  # marker on the currently-active pipeline


def test_help_does_not_crash(run_tool):
    r = run_tool("claude-pipeline", "--help")
    assert r.returncode == 0
