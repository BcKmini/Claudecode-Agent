"""Tests for tools/claude-review-diff.py."""


def test_requires_git_repo(run_tool, tmp_path):
    r = run_tool("claude-review-diff", cwd=tmp_path)
    assert r.returncode == 1
    assert "Not inside a git repository" in r.stderr


def test_no_diff_found(run_tool, git_repo):
    r = run_tool("claude-review-diff", cwd=git_repo)
    assert r.returncode == 0
    assert "No diff found" in r.stderr


def test_generates_review_prompt_for_unstaged_changes(run_tool, git_repo):
    (git_repo / "README.md").write_text("hello world, changed\n", encoding="utf-8")

    r = run_tool("claude-review-diff", cwd=git_repo)
    assert r.returncode == 0
    assert "code review" in r.stdout.lower()
    assert "## Diff" in r.stdout
    assert "hello world, changed" in r.stdout


def test_focus_option_changes_the_hint(run_tool, git_repo):
    (git_repo / "README.md").write_text("changed\n", encoding="utf-8")

    r = run_tool("claude-review-diff", "--focus", "security", cwd=git_repo)
    assert r.returncode == 0
    assert "security vulnerabilities" in r.stdout.lower()


def test_staged_only_reviews_staged_changes(run_tool, git_repo):
    (git_repo / "README.md").write_text("unstaged change\n", encoding="utf-8")
    r = run_tool("claude-review-diff", "--staged", cwd=git_repo)
    assert r.returncode == 0
    assert "No diff found" in r.stderr
