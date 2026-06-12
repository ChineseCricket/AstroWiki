# AstroWiki

AstroWiki is a portable LLM-maintained research knowledge-base template for long-running astrophysics projects.

It combines:

- a strict `raw -> inbox -> wiki` approval pipeline inspired by NORIA;
- astrophysics-specific source claims with Table/Figure/Section/Equation locators;
- reusable agent skills for ADS sync, document parsing, web capture, linting, synthesis, and benchmark review;
- a lightweight MCP-compatible search service for downstream agents.

AstroWiki is designed to be copied into a new project, used by multiple agents, and kept auditable over months or years.

## Quick Start

```bash
git clone https://github.com/ChineseCricket/AstroWiki.git
cd AstroWiki

python tools/install.py --target /path/to/my-astro-project
cd /path/to/my-astro-project

python tools/astrowiki_lint.py --quiet
python tools/ads_sync.py search "galaxy cluster scaling relations" --limit 5 --dry-run
```

## Core Workflow

```text
raw/                 user-owned source material
  -> inbox/          agent-generated drafts for review
  -> wiki/           approved, linted knowledge base
  -> outputs/        reports, reviews, queries, exports
```

Rules:

- agents may stage source material in `raw/`;
- agents may compile drafts into `inbox/`;
- only the controlling agent or a human approval step may promote `inbox/` pages into `wiki/`;
- reviewer agents write to `outputs/reviews/`, never to `wiki/`;
- `query-derived` content never enters `wiki/`.

## Directory Layout

| Path | Purpose |
|---|---|
| `wiki/sources/` | Approved source pages derived from papers, documents, web captures, or catalogs |
| `wiki/concepts/` | Cross-source astrophysics concepts |
| `wiki/methods/` | Analysis, modeling, and observation methods |
| `wiki/objects/` | Astronomical objects with SIMBAD/NED-style identifiers |
| `wiki/datasets/` | Surveys, catalogs, samples, or observation sets |
| `wiki/instruments/` | Telescope, detector, mission, and pipeline pages |
| `wiki/synthesis/` | Thesis-bearing synthesis pages |
| `raw/` | Original inputs; never rewritten by compilation |
| `inbox/` | Draft wiki pages awaiting approval |
| `.kb/` | Manifest, relations, sync state, benchmark manifests |
| `outputs/` | Queries, reviews, exports, benchmark reports |
| `skills/` | Agent-readable operating procedures |
| `tools/` | Portable Python tooling |

## Included Tools

- `tools/ads_sync.py` stages ADS search results or bibcodes into `raw/ads/`.
- `tools/astrowiki_lint.py` checks schema, provenance, claims, links, synthesis, and leakage.
- `tools/astrowiki_queue.py` lists, diffs, approves, rejects, and archives inbox pages.
- `tools/astrowiki_mcp_server.py` exposes simple JSON-RPC tools over stdin or HTTP-like text responses.
- `tools/export_wiki.py` exports approved wiki knowledge to Markdown bundles or JSONL.
- `tools/run_benchmark.py` validates the template against fixture corpora.
- `tools/install.py` copies AstroWiki into a target project.

## Skills

The `skills/` directory contains reusable agent procedures:

- `astro-kb-sync`
- `astro-kb-ingest`
- `astro-kb-compile`
- `astro-kb-approve`
- `astro-kb-lint`
- `astro-kb-gap-scan`
- `astro-kb-synthesis`
- `astro-doc-parse`
- `astro-web-pack`
- `astro-md-table-export`

These are written as generic `SKILL.md` files so they can be adapted to Claude Code, Codex, Cursor, Gemini CLI, or other agent runners.

## External Services

V1 formally supports NASA ADS metadata through `ADS_API_TOKEN`.

SIMBAD and NED are represented in schema as optional object identifiers, but their APIs are not required in V1.

## License

MIT.
