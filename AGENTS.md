# llm-wiki Agent Policy

## Project Language Policy

Every synthesis page is bilingual. Write the complete English version first,
followed by a complete `## 中文对照（Chinese）` section. The Chinese version must
mirror the English thesis, evidence, contradictions, open questions, tables,
wikilinks, citekeys, and locators; a shortened Chinese summary is not sufficient.

llm-wiki uses a strict ownership model (same as AstroWiki / fdm-wiki).

## Roles

| Role | May Write | Must Not Write |
|---|---|---|
| Source worker | `raw/`, `inbox/` | `wiki/` |
| Compiler worker | `inbox/`, `.kb/manifest.json` | approved `wiki/` pages |
| Reviewer | `outputs/reviews/` | `wiki/`, `raw/` |
| Controller | `wiki/`, `.kb/`, `outputs/` | `raw/` rewrites |

## Rules

1. `raw/` is user-owned. Do not rewrite raw source during compilation.
2. Draft pages go to `inbox/`.
3. Approved pages reach `wiki/` **only** via `python tools/queue.py approve <slug>`.
4. `query-derived` content stays in `outputs/` — never in `wiki/`.
5. Run `python tools/lint.py --quiet` before synthesis or release.
6. Never silently resolve contradictions — add a `## Contradictions` section.
7. Every claim carries a citekey + locator + confidence. Low-confidence items are marked, not hidden.
