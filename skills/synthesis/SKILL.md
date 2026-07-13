---
name: synthesis
description: Generate or update a thesis-bearing synthesis page from approved wiki sources.
---

# llm-wiki Synthesis

Synthesis writes to `inbox/synthesis/` first, then is approved into `wiki/synthesis/`.

## Workflow

1. `python tools/lint.py --quiet`.
2. Read relevant sources/concepts/methods/instruments.
3. Check whether an existing synthesis page covers the thesis.
4. Create/update a draft in `inbox/synthesis/`.
5. Write the complete English version first. Sections: `## Thesis`, `## Evidence`,
   `## Contradictions` (when needed), `## Open Questions`, `## Related`.
6. Append a complete `## 中文对照（Chinese）` version. Mirror every substantive
   English section, table, caveat, open question, wikilink, and citation; do not
   replace the translation with a shortened Chinese summary.

## Rules

- `provenance: llm-derived`.
- Cite ≥2 trusted (`source-derived`) sources.
- No `query-derived` material.
- One thesis per page. Comparison values go in tables.
- All synthesis pages are English-Chinese bilingual. English comes first; Chinese
  uses `## 中文对照（Chinese）` and includes at least `### 论点（Thesis）` and
  `### 证据（Evidence）`.
- Keep citekeys and locators identical across both language versions.
- Optional frontmatter: `role`, `parent`, `scope`.
