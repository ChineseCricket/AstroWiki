---
name: approve
description: Review and promote inbox pages into wiki using the approval queue.
---

# llm-wiki Approve

```bash
python tools/queue.py list
python tools/queue.py diff <slug>
python tools/queue.py approve <slug>
python tools/queue.py reject <slug> --reason "..."
python tools/queue.py archive <slug>
```

## Workflow

1. `python tools/queue.py list`.
2. Inspect draft + provenance.
3. `python tools/lint.py --quiet --include-inbox`.
4. Approve only if no FAIL for that draft.
5. After approval, `python tools/lint.py --quiet`.

Only the controller / human workflow may approve. Never approve `query-derived` pages.
