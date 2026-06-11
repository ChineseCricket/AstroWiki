# AstroWiki Schema

AstroWiki is a provenance-first LLM wiki for astrophysics research.

## Page Types

| Type | Directory | Purpose |
|---|---|---|
| `source` | `wiki/sources/` | Approved summary of a paper, document, web page, or catalog entry |
| `concept` | `wiki/concepts/` | Cross-source concept explanation |
| `method` | `wiki/methods/` | Analysis, modeling, calibration, or observational method |
| `object` | `wiki/objects/` | Astronomical object or object class |
| `dataset` | `wiki/datasets/` | Survey, catalog, sample, observation set, or data release |
| `instrument` | `wiki/instruments/` | Mission, telescope, detector, pipeline, or software system |
| `synthesis` | `wiki/synthesis/` | Thesis-bearing cross-source analysis |
| `note` | `wiki/notes/` | Approved project note, used sparingly |

## Provenance

| Level | Meaning | Wiki Use |
|---|---|---|
| `user-verified` | Human-confirmed content | Highest trust; do not overwrite automatically |
| `source-derived` | Directly extracted from papers or primary documents | Valid evidence for synthesis |
| `catalog-derived` | Derived from ADS, SIMBAD, NED, VizieR, or other catalogs | Valid evidence when catalog source is cited |
| `llm-derived` | Agent synthesis or interpretation | Must cite source-derived or catalog-derived evidence |
| `web-derived` | Web captures, docs, release notes, gray literature | Useful lead; do not overclaim |
| `query-derived` | Ad hoc answers, reviews, or feedback | Must stay in `outputs/`; never enters `wiki/` |

## Required Frontmatter

Every wiki page must start with YAML frontmatter.

```yaml
---
title: "Page title"
type: source
provenance: source-derived
created: 2026-06-11
updated: 2026-06-11
---
```

Source pages must also include:

```yaml
citekey: firstauthor2026-topic
source_type: paper
authors: [First Author, Second Author]
year: 2026
venue: "ApJ"
ads_bibcode: "2026ApJ..."
doi: ""
arxiv: ""
claims:
  - text: "Short, checkable claim"
    citekey: firstauthor2026-topic
    locator: "Table 2"
    type: empirical_result
    confidence: high
```

## Claim Types

- `empirical_result`
- `method_claim`
- `physical_insight`
- `definition`
- `comparison`
- `catalog_fact`
- `software_or_pipeline`

## Locator Rules

Use the most specific available locator:

- `abstract`
- `sec.X`
- `Table X`
- `Figure Y`
- `Eq.N`
- `Appendix`
- `page N`
- `catalog record`

Never fabricate locators. If the source cannot support a locator, use `locator: "unverified"` and `confidence: low`.

## Synthesis Rules

Every `synthesis` page must include:

- `## Thesis`
- `## Evidence`
- at least two trusted source references in `sources: [...]`
- explicit treatment of contradictions when sources disagree

Synthesis pages use `provenance: llm-derived`.

## Wikilinks

Use Obsidian-compatible links:

```markdown
[[source-slug]]
[[concept-slug|Display label]]
```

All links must resolve to pages in `wiki/` or `inbox/` during lint.
