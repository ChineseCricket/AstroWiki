---
name: approve
description: Review and promote inbox pages into wiki using the approval queue. Use when the user asks to approve, reject, or inspect drafts.
---

# Astro KB Approve

Promote reviewed `inbox/` pages into `wiki/`.

## Commands

```bash
python tools/queue.py list
python tools/queue.py diff <slug>
python tools/queue.py approve <slug>
python tools/queue.py reject <slug> --reason "reason"
python tools/queue.py archive <slug>
```

## Workflow

1. Run `python tools/queue.py list`.
2. Inspect the draft and source provenance.
3. Run `python tools/lint.py --quiet --include-inbox`.
4. Approve only if there are no FAIL issues for that draft.
5. After approval, run `python tools/lint.py --quiet`.

## Rules

- Only the controller or human-approved workflow may approve pages.
- Never approve `query-derived` pages.
- If a page conflicts with existing wiki content, require a `## Contradictions` section.
