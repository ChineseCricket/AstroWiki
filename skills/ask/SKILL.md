---
name: ask
description: Answer questions against the wiki using search/get/graph tools. Answers are query-derived and stay in outputs/.
---

# llm-wiki Ask

Answers are `query-derived` and must stay in `outputs/queries/`.

```bash
printf '{"method":"search","params":{"query":"your topic","limit":5}}\n' | python tools/server.py
printf '{"method":"get","params":{"slug":"page-slug"}}\n' | python tools/server.py
printf '{"method":"graph_neighbors","params":{"slug":"page-slug"}}\n' | python tools/server.py
```

Answer from approved `wiki/` pages first; cite slugs for every claim; distinguish fact from inference; never silently resolve contradictions; never write query answers into `wiki/`/`inbox/`/`raw/`.
