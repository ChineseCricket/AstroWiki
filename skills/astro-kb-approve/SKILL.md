---
name: astro-kb-approve
description: Review and promote inbox pages into wiki using the approval queue. Use when the user asks to approve, reject, or inspect drafts.
---

# Astro KB Approve

Promote reviewed `inbox/` pages into `wiki/`.

## Commands

```bash
python tools/astrowiki_queue.py list
python tools/astrowiki_queue.py diff <slug>
python tools/astrowiki_queue.py approve <slug>
python tools/astrowiki_queue.py reject <slug> --reason "reason"
python tools/astrowiki_queue.py archive <slug>
```

## Workflow

1. Run `python tools/astrowiki_queue.py list`.
2. Inspect the draft and source provenance.
3. Run `python tools/astrowiki_lint.py --quiet --include-inbox`.
4. Approve only if there are no FAIL issues for that draft.
5. After approval, run `python tools/astrowiki_lint.py --quiet`.

## Rules

- Only the controller or human-approved workflow may approve pages.
- Never approve `query-derived` pages.
- If a page conflicts with existing wiki content, require a `## Contradictions` section.
