[← Back to README](../README.md)

**[한국어](MCP-GUIDE.ko.md)** · **English**

# MCP Server Guide

Every tool in this project (`snippet`, `claude-handoff`, `claude-cost`, `claude-lessons`, …) is a CLI you run manually and, usually, pipe into `claude`. An **MCP server** removes that manual step: it exposes the same functionality as tools Claude can call directly, in the middle of a conversation, without you running a command and pasting the output back in.

---

## Slash command vs. manual pipe vs. MCP — when to use which

| | You run it | Claude calls it | Best for |
|---|---|---|---|
| **Slash command** (`/lessons add`) | Yes, inside Claude Code | No | You decide *when* it runs — explicit, one-off actions |
| **Manual pipe** (`claude-lessons context \| claude`) | Yes, in your shell | No | Feeding output into a *fresh* session (context does not exist yet) |
| **MCP server** | No | Yes, mid-conversation | Claude should decide *when* it needs this — recurring lookups inside a task it's already running |

**Rule of thumb:** if you find yourself running the same CLI command and pasting its output into Claude more than a couple of times per session, that's a candidate for an MCP server. If it's a deliberate checkpoint action (save a handoff, log a lesson), a slash command is more honest about who's in control — don't automate away human checkpoints (see [Autonomy Levels](HARNESS-GUIDE.md#autonomy-levels-l0-l4)).

`claude-lessons` is the clearest candidate in this project: recalling past failures is exactly the kind of lookup Claude should trigger itself when it's about to touch a risky area, not something a human should have to remember to run first.

---

## Minimal anatomy of an MCP server

The [Python MCP SDK](https://modelcontextprotocol.io) gives you a decorator-based server (`FastMCP`) — define a function, decorate it, the docstring becomes the tool description the model sees:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(arg: str) -> str:
    """One line the model reads to decide when to call this."""
    return do_something(arg)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

That's the whole shape: a `FastMCP` instance, one `@mcp.tool()` function per capability, `stdio` transport for local use with Claude Code.

> **Version note:** `pip install mcp` currently installs a **2.x** release that reworked this API (`FastMCP` moved/renamed). This guide and [`examples/mcp-lessons-server.py`](../examples/mcp-lessons-server.py) target the well-established **1.x** line — pin `pip install "mcp>=1.2,<2"` unless you've read the 2.x migration guide.

---

## Worked example: `claude-lessons` as an MCP server

[`examples/mcp-lessons-server.py`](../examples/mcp-lessons-server.py) wraps `tools/claude-lessons.py` and exposes three tools:

- `add_lesson(title, symptom, cause, fix, tags)`
- `search_lessons(query)`
- `recent_lessons(limit, tag)` — the one worth calling automatically, before touching an area with a known failure history

It loads `tools/claude-lessons.py` by file path (its filename has a hyphen, so it can't be `import`ed directly) and reuses its storage functions rather than re-implementing the lesson file format — so the CLI and the MCP server always agree on where lessons live and what they look like.

It lives in `examples/`, not `tools/`, because `docs/CONTRIBUTING.md` requires everything under `tools/` to stay dependency-free (stdlib only), and the `mcp` package is an external dependency.

### Try it

```bash
pip install "mcp>=1.2,<2"
python3 examples/mcp-lessons-server.py   # starts a stdio server, waits for a client
```

### Register it with Claude Code

```bash
claude mcp add lessons -- python3 /path/to/examples/mcp-lessons-server.py
```

Once registered, Claude can call `recent_lessons` itself when it's about to work in an area with recorded failures — no `claude-lessons context | claude` needed.

---

## Applying this to other tools in this project

The same pattern works for any tool here that Claude should query rather than a human piping in:

| Tool | Worth wrapping as MCP? | Why / why not |
|---|---|---|
| `claude-lessons` | Yes (see above) | Recurring lookup, low-stakes, read path especially |
| `claude-remind` | Maybe | Useful as a tool Claude calls at task start; still fine as `/remind` |
| `claude-cost` | Maybe, read-only tools only | Letting Claude read spend is fine; keep `set-budget` a manual/slash action |
| `claude-handoff save` | No | Saving a handoff is a deliberate human checkpoint — keep it a slash command |
| `claude-pipeline` | No | Stage transitions should stay explicit and reviewable, not auto-triggered |

When in doubt, default to **not** wrapping a write/mutating action as an MCP tool — an agent that can silently call it mid-conversation is a higher autonomy level (see [Autonomy Levels](HARNESS-GUIDE.md#autonomy-levels-l0-l4)) than a slash command the human explicitly types.

---

*See also:*
- *[`examples/mcp-lessons-server.py`](../examples/mcp-lessons-server.py) — the runnable example*
- *[`tools/claude-lessons.py`](../tools/claude-lessons.py) — the CLI it wraps*
- *[HARNESS-GUIDE.md](HARNESS-GUIDE.md) — autonomy levels and harness design*
