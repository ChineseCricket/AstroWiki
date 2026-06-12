---
name: sync
description: Discover and stage astrophysics literature metadata into raw/ using ADS. Use when the user asks to search papers, refresh literature, inspect citations, or import bibcodes.
---

# Astro KB Sync

Stage bibliographic source metadata into `raw/`. Do not write to `wiki/`.

## Default Source

Use NASA ADS through `tools/sync.py`.

Examples:

```bash
python tools/sync.py search "galaxy cluster scaling relations" --limit 20 --dry-run
python tools/sync.py search "galaxy cluster scaling relations" --limit 20
python tools/sync.py bibcode "2010MNRAS.406.1759M"
```

## Workflow

1. Read `AGENTS.md` and `wiki/schema.md`.
2. Run ADS search in `--dry-run` mode first unless the user provided exact bibcodes.
3. Stage selected records into `raw/ads/`.
4. Do not summarize or synthesize here.
5. Leave compilation to `compile`.

## Rules

- Preserve ADS bibcode, DOI, arXiv ID, title, authors, abstract, citation count, references, and citations when available.
- Deduplicate by ADS bibcode, DOI, and arXiv ID.
- If ADS credentials are missing, report the limitation and use dry-run/example mode only.
