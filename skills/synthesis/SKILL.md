---
name: synthesis
description: Generate or update a thesis-bearing synthesis page from approved AstroWiki sources.
---

# Astro KB Synthesis

Synthesis writes to `inbox/synthesis/` first.

## Workflow

1. Run `python tools/lint.py --quiet`.
2. Read relevant sources, concepts, methods, objects, datasets, and instruments.
3. Check whether an existing synthesis page covers the topic.
4. Create or update a draft in `inbox/synthesis/`.
5. Include `## Thesis`, `## Evidence`, `## Contradictions` when needed, `## Open Questions`, and `## Related`.

## Rules

- Use `provenance: llm-derived`.
- Cite at least two trusted sources.
- Do not use `query-derived` material.
- Keep one thesis per page.
- Put numerical values in tables when comparison matters.
