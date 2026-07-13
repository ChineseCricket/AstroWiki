---
name: compile
description: Compile staged raw material into inbox pages with provenance, claims, and wikilinks. Use after raw sources have been staged.
---

# llm-wiki Compile

Compile `raw/` files into `inbox/`. Never write directly to `wiki/`.

## Workflow

1. Read `AGENTS.md`, `wiki/schema.md`, `.kb/manifest.json`.
2. Identify uncompiled raw files.
3. For each source, create a draft source page in `inbox/sources/`.
4. Extract 3–8 locator-backed claims (each with text, citekey, locator, type, confidence).
5. Create/update concept/method/instrument/entity drafts as needed.
6. Update `.kb/manifest.json`.
7. `python tools/lint.py --quiet --include-inbox`.

## Source page requirements

`type: source`; `provenance: source-derived|catalog-derived|web-derived`; bibliographic metadata; 3–8 claims; body cites as `[source: citekey, locator]`.

## Rules

- Do not fabricate locators. Mark uncertain claims `confidence: low`.
- Put contradictions in `## Contradictions`.
- Use `[[wikilinks]]` for related pages.
