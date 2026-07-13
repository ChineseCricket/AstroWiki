---
name: ingest
description: Stage local PDFs, notes, tables, web captures into raw/. Use for new source material not yet ready for wiki compilation.
---

# llm-wiki Ingest

Stage into `raw/` only. Do not update `wiki/`, `inbox/`, or `.kb/manifest.json`.

| Input | Target |
|---|---|
| ADS/arXiv records | `raw/ads/` |
| PDFs / Office docs | `raw/documents/` |
| Web captures | `raw/web/` |
| Freeform notes | `raw/notes/` |
| CSV / Markdown tables | `raw/tables/` |

Preserve provenance, URLs, dates, local paths. `raw/` is user-owned — do not rewrite unless asked.
