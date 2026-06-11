---
name: astro-kb-compile
description: Compile staged raw material into inbox pages with provenance, claims, and wikilinks. Use after raw sources have been staged.
---

# Astro KB Compile

Compile `raw/` files into `inbox/`. Never write directly to `wiki/`.

## Workflow

1. Read `AGENTS.md`, `wiki/schema.md`, and `.kb/manifest.json`.
2. Identify uncompiled raw files.
3. For each selected source, create a draft source page in `inbox/sources/`.
4. Extract 3-8 locator-backed claims.
5. Create or update concept/method/object/dataset/instrument drafts in `inbox/` when needed.
6. Update `.kb/manifest.json` with draft paths.
7. Run `python tools/astrowiki_lint.py --quiet --include-inbox`.

## Source Page Requirements

Every draft source page must include:

- `type: source`
- `provenance: source-derived`, `catalog-derived`, or `web-derived`
- `verification_status: pending`
- bibliographic or source metadata
- 3-8 claims with `text`, `citekey`, `locator`, `type`, `confidence`
- citations in body text using `[source: citekey, locator]`

## Rules

- Do not fabricate locators.
- Mark uncertain claims `confidence: low`.
- Put contradictions in `## Contradictions`.
- Use `[[wikilinks]]` for related pages.
