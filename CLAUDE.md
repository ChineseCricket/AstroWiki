# llm-wiki — Agent Instructions

> Lean instruction file. Full schema: `schema.md`. Domain focus: X-ray TES + FDM
> readout **simulator** research and our own full-pipeline simulator design.
> This is the simulator-focused sibling of the broader `fdm-wiki/`.

## Ownership (hard boundaries)

| Directory | Owner | Rule |
|---|---|---|
| `raw/` | User | **NEVER modify, delete, or reorganize** |
| `inbox/` | Worker agent | Drafts awaiting approval |
| `wiki/` | Controller (LLM) | Promote via `tools/queue.py approve`; preserve `user-verified` |
| `outputs/` | LLM | Reviews/queries. **NEVER feed back into `wiki/`** |
| `tools/` | Shared | Modify with user approval |

## Forbidden Operations

- Never overwrite `raw/`.
- Never write directly to `wiki/`; stage in `inbox/` then `python tools/queue.py approve <slug>`.
- Never feed `outputs/` back into `wiki/`.
- Never create a wiki page without provenance frontmatter.
- Never fabricate citations or locators — mark `[UNVERIFIED]` / `confidence: low`.

## Pipeline

```
raw/  ->  inbox/  ->  wiki/  ->  outputs/
```

1. `/sync` or `/ingest` — stage sources into `raw/` (papers, web, notes).
2. `/compile` — `raw/` → `inbox/` draft pages with claims + provenance.
3. `/lint` — `python tools/lint.py --quiet` (mandatory before synthesis).
4. `/approve` — `python tools/queue.py approve <slug>` promotes inbox → wiki.
5. `/synthesis` — write thesis-bearing synthesis to `inbox/synthesis/`, then approve.

## Conventions

- Every synthesis is fully bilingual: English first, then a complete
  `## 中文对照（Chinese）` section with matching claims, tables, caveats, and citations.

- Filenames / slugs: kebab-case. Source slugs: `<author><year>-<keyword>` (e.g. `dauser2019-sixte`).
- Dates ISO 8601. Wikilinks Obsidian-style `[[slug]]` / `[[slug|Label]]`.
- In-text citation: `[source: <citekey>, <locator>]`.
- Tags carry the domain: `domain:tes`, `domain:fdm`, `domain:readout`, `domain:simulation`, `tool:sixte`, `mission:athena`, `mission:dixe`.

## Tooling

- `tools/lint.py` — schema/provenance/claims/wikilink/synthesis checks.
- `tools/queue.py` — inbox approval queue (list / approve / reject / archive).
- `tools/server.py` — local JSON-RPC search (`search`, `get`, `list_concepts`, `graph_neighbors`).
- All dependency-free Python (stdlib only).
