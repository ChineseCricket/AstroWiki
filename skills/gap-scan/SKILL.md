---
name: gap-scan
description: Identify knowledge gaps in an AstroWiki project: missing coverage, shallow sources, orphan pages, and synthesis opportunities.
---

# Astro KB Gap Scan

This is read-only analysis.

## Gap Types

- Depth: sources with abstract-only or weak locators.
- Coverage: important topics or objects not represented in concepts/objects.
- Structure: orphan sources not linked by concepts or synthesis.
- Synthesis: topics spanning three or more sources without a synthesis page.
- Benchmark: fixture pages that fail comparison metrics.

## Workflow

1. Run `python tools/lint.py --quiet`.
2. Read `wiki/index.md`, source claims, and concept pages.
3. Identify high-impact gaps.
4. Write the report to `outputs/reviews/`.

## Priority

- HIGH: gaps that affect current research conclusions.
- MEDIUM: missing links, shallow locators, missing concept pages.
- LOW: cosmetic or archival organization issues.
