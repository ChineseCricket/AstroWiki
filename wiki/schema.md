# llm-wiki Schema

> Full schema definition. Loaded by skills on demand. `CLAUDE.md` references this
> file but does NOT inline its content. Domain: X-ray TES microcalorimeter + FDM
> readout **simulation** — research and full-pipeline simulator design.

## Page Types

| Type | Directory | Purpose |
|---|---|---|
| `source` | `wiki/sources/` | Approved summary of a paper, doc, web page, or catalog entry |
| `concept` | `wiki/concepts/` | Cross-source concept (physics, electronics, simulation) |
| `method` | `wiki/methods/` | Analysis, modeling, or simulation method |
| `instrument` | `wiki/instruments/` | Simulator / software / instrument / mission page |
| `dataset` | `wiki/datasets/` | Simulated data, response files (RMF/ARF), calibration data |
| `object` | `wiki/objects/` | Target X-ray sources, calibration line sources |
| `entity` | `wiki/entities/` | Lab / group / mission / project profile |
| `synthesis` | `wiki/synthesis/` | Thesis-bearing cross-source analysis |
| `note` | `wiki/notes/` | Approved project note (used sparingly) |

## Provenance Levels

| Level | Meaning | Wiki use |
|---|---|---|
| `user-verified` | Human-confirmed | Highest trust; do not overwrite |
| `source-derived` | Extracted from papers / primary docs | Valid evidence for synthesis |
| `catalog-derived` | From ADS/arXiv/NIST-pub catalog records | Valid evidence when catalog cited |
| `llm-derived` | Agent synthesis / interpretation | Must cite ≥2 trusted sources |
| `web-derived` | Web captures, docs, release notes | Lead only; do not overclaim |
| `query-derived` | Ad hoc answers | `outputs/` only; never in `wiki/` |

Hard rule: `query-derived` **never** enters `wiki/`. Synthesis needs ≥2 trusted sources.

## Required Frontmatter

```yaml
---
title: "Page title"
type: source            # one of the page types above
provenance: source-derived
created: 2026-06-28
updated: 2026-06-28
tags: [domain:tes, domain:simulation]
---
```

### Source pages also include

```yaml
citekey: dauser2019-sixte
source_type: paper      # paper | thesis | docs | web | catalog
authors: [Dauser, T., Falkner, S.]
year: 2019
venue: "Astronomy & Astrophysics"
ads_bibcode: "2019A&A...630A..66D"
doi: "10.1051/0004-6361/201935978"
arxiv: "1908.00781"
url: "https://..."
github_url: ""
domain: simulation      # tes | fdm | readout | squid | simulation | instrumentation | multiplexing | other
mission: athena         # athena | dixe | xrism | hitomi | chandra | generic | none
claims:
  - text: "Short, checkable claim"
    citekey: dauser2019-sixte
    locator: "sec.2.1"
    type: software_or_pipeline
    confidence: high
```

## Claim Types

`empirical_result` · `method_claim` · `physical_insight` · `definition` · `comparison` · `catalog_fact` · `software_or_pipeline`

## Confidence

`high` (verified against fetched primary source) · `medium` (secondary/citation-grounded) · `low` (plausible, not directly verified — mark, never fabricate).

## Locator Rules

Use the most specific available: `abstract` · `sec.X` · `Table X` · `Figure Y` · `Eq.N` · `Appendix` · `page N` · `catalog record` · `docs:<page>`. Never fabricate. If unsupported, use `locator: "unverified"` with `confidence: low`.

## Synthesis Rules

All synthesis pages are fully bilingual. Write the complete English page first,
then append `## 中文对照（Chinese）`. The Chinese version must mirror the English
thesis, evidence, tables, contradictions, open questions, related links,
citekeys, and locators; a shortened Chinese abstract does not satisfy the schema.

Every `synthesis` page must include:

- `## Thesis`
- `## Evidence`
- `provenance: llm-derived`
- `sources: [...]` with **≥2** entries
- `## Contradictions` when sources disagree
- Optional `role: umbrella | child | bridge | decision | domain`, `parent`, `scope`

## Wikilinks

Obsidian-compatible: `[[slug]]`, `[[slug|Display label]]`. All links must resolve to a page in `wiki/` (or `inbox/` while drafting).

## Citation format

```
SIXTE's pipeline has three functional blocks [source: dauser2019-sixte, sec.2.1].
```

## Document Placement

| Location | Content |
|---|---|
| `CLAUDE.md` | Lean agent instructions |
| `schema.md` | This file — full schema |
| `ARCHITECTURE.md` | System design, directory tree, data flow, the TES+FDM signal chain |
| `wiki/log.md` | Approval log (append-only) |
| `docs/` | Reference docs, guides |
| `raw/` | Original sources (user-owned) |
| `outputs/` | Queries / reviews (never fed back) |
