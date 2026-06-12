---
name: ingest
description: Stage local PDFs, notes, tables, and web captures into raw/. Use for new source material that is not yet ready for wiki compilation.
---

# Astro KB Ingest

Stage source material into `raw/` only.

## Targets

| Input | Target |
|---|---|
| ADS records | `raw/ads/` |
| PDFs or Office documents | `raw/documents/` |
| Web captures | `raw/web/` |
| Freeform notes | `raw/notes/` |
| CSV/Markdown tables | `raw/tables/` |

## Workflow

1. Decide the source type.
2. Use stable descriptive names.
3. Preserve provenance, URLs, dates, and local paths.
4. Do not update `wiki/`, `inbox/`, or `.kb/manifest.json`.

## Rules

- `raw/` is user-owned. Do not rewrite existing files unless explicitly requested.
- If the source is a PDF, prefer staging the original PDF and a parsed Markdown sidecar.
- If the source is web-derived, include capture URL and capture date.
