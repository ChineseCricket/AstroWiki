# AstroWiki Agent Policy

AstroWiki uses a strict ownership model.

## Roles

| Role | May Write | Must Not Write |
|---|---|---|
| Source worker | `raw/`, `inbox/` | `wiki/` |
| Compiler worker | `inbox/`, `.kb/manifest.json` | approved `wiki/` pages |
| Reviewer | `outputs/reviews/` | `wiki/`, `raw/` |
| Controller | `wiki/`, `.kb/`, `outputs/` | `raw/` rewrites |

## Rules

1. `raw/` is user-owned. Do not rewrite raw source material during compilation.
2. Draft pages go to `inbox/`.
3. Approved pages go to `wiki/` only via `tools/astrowiki_queue.py approve`.
4. `query-derived` content stays in `outputs/`.
5. Run `python tools/astrowiki_lint.py --quiet` before synthesis or release.
6. Never silently resolve contradictions. Add a `## Contradictions` section.
