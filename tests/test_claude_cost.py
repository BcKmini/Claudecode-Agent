"""Tests for tools/claude-cost.py."""


def test_estimate_with_literal_prompt(run_tool):
    r = run_tool("claude-cost", "estimate", "Implement OAuth 2.0 login")
    assert r.returncode == 0
    assert "Cost Estimate" in r.stdout
    assert "Total estimate" in r.stdout


def test_estimate_requires_prompt_or_snippet(run_tool):
    r = run_tool("claude-cost", "estimate")
    assert r.returncode == 2


def test_estimate_with_custom_agent_list(run_tool):
    r = run_tool("claude-cost", "estimate", "fix bug", "--agents", "implementer,reviewer")
    assert r.returncode == 0
    assert "implementer" in r.stdout
    assert "reviewer" in r.stdout
    assert "planner" not in r.stdout


def test_month_with_no_data(run_tool):
    r = run_tool("claude-cost", "month")
    assert r.returncode == 0
    assert "No data for" in r.stdout


def test_set_budget_then_month_reflects_it(run_tool):
    set_result = run_tool("claude-cost", "set-budget", "20.00")
    assert set_result.returncode == 0
    assert "$20.0000" in set_result.stdout

    month = run_tool("claude-cost", "month")
    assert month.returncode == 0
