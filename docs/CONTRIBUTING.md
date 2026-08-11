**[한국어](CONTRIBUTING.ko.md)** · **English**

# Contributing Guide

Thank you for helping improve this project!

---

## Ways to Contribute

| Type | How |
|------|-----|
| Bug fix | Open a bug report → submit a PR with the fix |
| New snippet | Add to `snippets/defaults.json` → PR |
| New agent | Add `.md` file to `agents/` → update README tables → PR |
| New tool | Add Python tool to `tools/` + slash command to `.claude/commands/` → PR |
| Documentation | Edit any `.md` file → PR (update both EN and KO versions) |
| Translation | Improve `README.md` (EN) or `README.ko.md` (KO) |
| Feature idea | Open a Feature Request issue first |

---

## Development Setup

```bash
git clone https://github.com/BcKmini/Claudecode-Agent.git
cd Claudecode-Agent
python --version   # 3.8+ required
make status        # check what's installed
```

`snippet.py`, `claude-handoff.py`, `claude-cost.py`, `claude-review-diff.py`, `claude-remind.py`, `claude-harness.py`, `claude-pipeline.py`, `claude-lessons.py` all use only the Python standard library — no `pip install` needed to *run* them. Testing them does need dev dependencies:

```bash
pip install tox
tox              # full matrix: py38-py313 (skips interpreters you don't have) + lint + fmt-check
tox -e py        # just run tests/ on your current interpreter
tox -e lint      # ruff check tools/ tests/
```

Ruff's config lives in `pyproject.toml` — it's scoped to `E`/`F`/`I`/`UP` (real bugs, unused imports, import order, modernization), not the full default ruleset, and `E402` is ignored because every tool deliberately puts its `VERSION` constant right after the docstring, before imports. `fmt-check` only covers `tools/claude-lessons.py` and `tests/` — the older tools use a deliberate hand-aligned style that `ruff format` would flatten, so it isn't enforced repo-wide.

For the Rust binary:

```bash
cd rust
cargo check   # verify build
cargo build --release

cargo install cargo-msrv --locked
cd claude-tools && cargo msrv verify   # confirm it still builds on the declared rust-version
```

---

## Adding a New Snippet

1. Open `snippets/defaults.json`
2. Add your entry:

```json
"my-snippet": {
  "prompt": "Your prompt here. Use {{VARIABLE}} for template vars.",
  "tags": ["tag1", "tag2"],
  "created": "YYYY-MM-DD",
  "uses": 0
}
```

3. Test locally:
```bash
python tools/snippet.py import snippets/defaults.json --overwrite
python tools/snippet.py show my-snippet
python tools/snippet.py run my-snippet --dry-run
```

4. Update the snippet table in both `README.md` and `README.ko.md`

---

## Adding a New Agent

1. Create `agents/NN-agent-name.md` following the format of existing agents
2. Add a row to the agent table in `README.md` and `README.ko.md`
3. Update both install scripts if they hardcode agent names

---

## Adding a New Tool

1. Add `tools/claude-<name>.py` following the style of existing tools
   - stdlib only, no external deps
   - Python 3.8+ compatible
   - Respect `NO_COLOR` environment variable
2. Add `.claude/commands/<name>.md` slash command doc
3. Add the tool to `Makefile` → `install-tools` target and `status` target
4. Add `tests/test_<name>.py` (subprocess-based, using the `run_tool`/`home`/`git_repo` fixtures in `tests/conftest.py`) and confirm `tox -e py,lint` passes
5. If adding a Rust implementation, add `rust/claude-tools/src/<name>.rs` and wire it into `main.rs`
6. Update `README.md` and `README.ko.md` tool sections, slash command table, and repo layout
7. Update `docs/AGENT-CHEATSHEET.md` and `docs/AGENT-CHEATSHEET.ko.md`

---

## Code Style

### Python tools
- Standard library only — no external dependencies
- Python 3.8+ compatible
- All user-visible strings in English
- `NO_COLOR` environment variable must be respected
- Exit codes: `0` success, `1` not found / exists, `2` usage error

`examples/` is the one exception to "no external dependencies" — it's for runnable integration
examples (e.g. an MCP server) that legitimately need a third-party package. Keep those out of
`tools/`; state the dependency clearly in the example's docstring and in `docs/MCP-GUIDE.md` if relevant.

### Rust (claude-tools)
- `cargo check` must pass with no errors
- Minimize `cargo clippy` warnings
- New subcommands follow the pattern of existing modules in `rust/claude-tools/src/`
- Use `crate::colors` functions (`green()`, `red()`, etc.) for colored output

---

## Pull Request Checklist

- [ ] `python tools/snippet.py --help` still works
- [ ] All existing commands still work
- [ ] `snippet import snippets/defaults.json` still works
- [ ] `cargo check` passes (Rust changes)
- [ ] `make test` passes
- [ ] `tox` passes — at minimum `tox -e py,lint` (Python changes)
- [ ] `cargo msrv verify` passes (Rust changes — confirms the declared `rust-version` still builds)
- [ ] README tables updated if new snippets / agents / tools added
- [ ] **Both EN and KO docs updated** (README, CHEATSHEET, SETUP, INTEGRATION as applicable)
- [ ] Slash command `.md` added if new tool introduced
- [ ] `Makefile` updated if new tool added
- [ ] No new external dependencies introduced in `tools/` (an `examples/` script may declare one — see Code Style)

---

## License

By contributing, you agree your contributions will be released under the [MIT License](../LICENSE).
