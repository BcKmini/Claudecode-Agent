"""Tests for tools/claude-harness.py."""


def test_validate_a_known_good_agent(run_tool, repo_root):
    agent = repo_root / "agents" / "09-harness-designer.md"
    r = run_tool("claude-harness", "validate", str(agent))
    assert r.returncode == 0
    assert "Autonomy level (L0-L4) is declared" in r.stdout


def test_validate_missing_file_fails(run_tool):
    r = run_tool("claude-harness", "validate", "/nonexistent/agent.md")
    assert r.returncode == 1


def test_check_all_runs_against_every_agent(run_tool):
    r = run_tool("claude-harness", "check-all")
    # exit 0 regardless of individual agent pass/fail (check-all always
    # completes cleanly); the important thing is it finds and reports on
    # all agents without crashing.
    assert r.returncode == 0
    for n in range(11):
        assert f"{n:02d}-" in r.stdout


def test_template_includes_autonomy_field(run_tool):
    r = run_tool("claude-harness", "template", "tight", "my-specialist")
    assert r.returncode == 0
    assert "autonomy: L2" in r.stdout
    assert "name: my-specialist" in r.stdout


def test_autonomy_subcommand_prints_all_five_levels(run_tool):
    r = run_tool("claude-harness", "autonomy")
    assert r.returncode == 0
    for level in ("L0", "L1", "L2", "L3", "L4"):
        assert level in r.stdout
