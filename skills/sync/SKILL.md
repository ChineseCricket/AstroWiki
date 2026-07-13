---
name: sync
description: Discover and stage literature metadata (ADS/arXiv) into raw/. Use when asked to search papers or import bibcodes.
---

# llm-wiki Sync

Stage bibliographic metadata into `raw/ads/`. Do not write to `wiki/`.

```bash
# (requires ADS_API_TOKEN for live search; otherwise stage from arXiv/known bibcodes)
```

## Workflow

1. Read `AGENTS.md`, `wiki/schema.md`.
2. Dry-run search first unless exact bibcodes given.
3. Stage selected records into `raw/ads/`.
4. Deduplicate by bibcode/DOI/arXiv. Leave compilation to `compile`.
5. If credentials missing, report the limitation and stage from public metadata only.
