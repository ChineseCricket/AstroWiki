---
name: pack
description: Export an approved knowledge bundle (Markdown + relations) for downstream agents or sibling wikis (e.g. fdm-wiki).
---

# llm-wiki Pack

Bundle selected `wiki/` pages (by tag, e.g. `domain:simulation`) plus their `[[wikilink]]` targets and `.kb/relations.jsonl` entries into a self-contained Markdown + JSONL export under `outputs/exports/`. Tag the bundle with provenance so the downstream wiki can re-stage it as `raw/` and re-compile without trust inflation.
