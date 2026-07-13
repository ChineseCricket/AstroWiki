# Tooling reference

All tools are **dependency-free Python (stdlib only)** — runnable on Windows/Unix
without `pip install`. Run from the `llm-wiki/` root.

## `tools/lint.py` — health gate

```bash
python tools/lint.py --quiet                 # wiki/ only; exit 1 on any FAIL
python tools/lint.py --quiet --include-inbox # include drafts
python tools/lint.py --json                  # machine-readable issues
```

Checks: frontmatter present; `type` ∈ valid set; `provenance` ∈ valid set;
`query-derived` not in `wiki/`; source pages have ≥3 valid claims (text/citekey/
locator/type/confidence); synthesis pages have `## Thesis`, ≥2 sources, and
`provenance: llm-derived`; every `[[wikilink]]` resolves; approved pages referenced
in `wiki/index.md` (WARN); `.kb/manifest.json` well-formed.

## `tools/queue.py` — approval queue

```bash
python tools/queue.py list
python tools/queue.py approve <slug>        # inbox -> wiki, updates index + log + manifest
python tools/queue.py reject <slug> --reason "..."
python tools/queue.py archive <slug>
```

## `tools/server.py` — local knowledge service

JSON-RPC over stdin (MCP-compatible). Methods: `search`, `get`, `list_concepts`,
`graph_neighbors`.

```bash
printf '{"method":"search","params":{"query":"detector readout","limit":5}}\n' | python tools/server.py
printf '{"method":"get","params":{"slug":"page-slug"}}\n' | python tools/server.py
printf '{"method":"graph_neighbors","params":{"slug":"page-slug"}}\n' | python tools/server.py
```

## `tools/common.py`

Shared: page-type registry (incl. `entity`), provenance/claim vocabularies,
YAML-subset frontmatter parser, page discovery, JSON helpers.
