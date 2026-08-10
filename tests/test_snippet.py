"""Tests for tools/snippet.py."""


def test_list_when_empty(run_tool):
    r = run_tool("snippet", "list")
    assert r.returncode == 0
    assert "No snippets saved yet." in r.stdout


def test_save_and_list(run_tool):
    save = run_tool("snippet", "save", "myfix", "Fix {{BUG}} in {{FILE}}", "--tags", "bug,auth")
    assert save.returncode == 0
    assert "saved" in save.stdout

    listed = run_tool("snippet", "list")
    assert "myfix" in listed.stdout


def test_save_duplicate_without_force_fails(run_tool):
    run_tool("snippet", "save", "myfix", "first version")
    dup = run_tool("snippet", "save", "myfix", "second version")
    assert dup.returncode == 1
    assert "already exists" in dup.stdout


def test_run_fills_template_vars(run_tool):
    run_tool("snippet", "save", "myfix", "Fix {{BUG}} in {{FILE}}")
    r = run_tool(
        "snippet", "run", "myfix", "--var", "BUG=null ref", "--var", "FILE=src/auth.ts", "--dry-run"
    )
    assert r.returncode == 0
    assert "Fix null ref in src/auth.ts" in r.stdout


def test_run_warns_on_missing_vars(run_tool):
    run_tool("snippet", "save", "myfix", "Fix {{BUG}} in {{FILE}}")
    r = run_tool("snippet", "run", "myfix", "--var", "BUG=null ref", "--dry-run")
    assert "Unfilled template vars: FILE" in r.stderr


def test_delete(run_tool):
    run_tool("snippet", "save", "throwaway", "content")
    deleted = run_tool("snippet", "delete", "throwaway", "--force")
    assert deleted.returncode == 0

    listed = run_tool("snippet", "list")
    assert "throwaway" not in listed.stdout


def test_import_defaults(run_tool, repo_root):
    defaults = repo_root / "snippets" / "defaults.json"
    r = run_tool("snippet", "import", str(defaults))
    assert r.returncode == 0
    assert "added" in r.stdout

    listed = run_tool("snippet", "list")
    assert "full-pipeline" in listed.stdout
