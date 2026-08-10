# /lessons — Failure / Lessons-Learned Log

Record why something failed and how it was fixed, so the next session doesn't repeat it. Complements `/handoff` (session state) and `/remind` (pending tasks) — `/lessons` is for accumulated knowledge, not session snapshots.

## Usage

```
/lessons add                 # record a new lesson (prompts for missing fields)
/lessons list                 # recent lessons
/lessons list --tag db        # filter by tag
/lessons search QUERY         # keyword search
/lessons show                 # most recent lesson (or --id ID)
/lessons context               # print matching lessons, pipeable into claude
```

## Recording a lesson

```bash
claude-lessons add \
  --title "Migration timed out" \
  --tags db,migration \
  --symptom "ALTER TABLE locked prod for 4min" \
  --cause "no lock_timeout set" \
  --fix "added SET lock_timeout='2s' before DDL"
```

Any field left out is prompted for interactively.

## Recalling lessons at session start

```bash
claude-lessons context | claude          # last 5 lessons, any tag
claude-lessons context --tag db | claude # only db-tagged lessons
```

## Typical workflow

```bash
# During/after debugging a tricky failure
claude-lessons add

# Start of a new session touching the same area
claude-lessons context --tag db | claude
```

## Tool

Runs `python tools/claude-lessons.py` (or `claude-lessons` if installed globally).

Install: `make install-tools`

Unlike `claude-handoff`, lessons are **not** pruned automatically — they're meant to accumulate as long-term project memory.
