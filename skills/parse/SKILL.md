---
name: parse
description: Parse PDFs, Office files, HTML into Markdown for raw staging.
---

# llm-wiki Parse

Preferred: use a document parser to extract text + structure, write a Markdown sidecar into `raw/documents/`. For large PDFs (>5 MB or >100 pages) split into ~50-page chunks, parse serially, merge in page order.

## Fallback

If no parser available: stage the original in `raw/documents/`, write a short metadata sidecar, report parsing pending. Do not discard originals. Do not write parsed output to `wiki/`.
