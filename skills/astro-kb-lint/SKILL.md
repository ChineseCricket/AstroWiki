---
name: astro-kb-lint
description: Check AstroWiki health and provenance. Use before synthesis, release, migration, or approval.
---

# Astro KB Lint

Run deterministic checks first:

```bash
python tools/astrowiki_lint.py --quiet
python tools/astrowiki_lint.py --json
python tools/astrowiki_lint.py --include-inbox
```

## Checks

- frontmatter
- page type
- provenance
- claims
- locator presence
- wikilinks
- index coverage
- manifest consistency
- synthesis `## Thesis`
- `query-derived` leakage

## Semantic Review

After deterministic checks pass, sample pages for:

- numerical consistency against source pages;
- unsupported claims;
- vague claims;
- missing contradictions;
- important keywords lacking concept pages.

Reviewer outputs go to `outputs/reviews/`.
