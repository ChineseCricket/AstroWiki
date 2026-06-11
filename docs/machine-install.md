# Machine Installation

AstroWiki V1 requires Python 3.10+ and uses only the Python standard library for core tools.

## Optional Environment

Create `.env` from `.env.example` and set:

```bash
ADS_API_TOKEN=...
```

The ADS token enables live ADS metadata sync. Without it, `ads_sync.py --dry-run` still works.

## Smoke Test

```bash
python tools/astrowiki_lint.py --quiet
python tools/ads_sync.py search "supernova remnants" --limit 1 --dry-run
printf '{"method":"search","params":{"query":"astro","limit":3}}\n' | python tools/astrowiki_mcp_server.py
```

## Optional Document Parsing

For `astro-doc-parse`, install `xparse-cli` separately if your workflow needs PDF/OCR parsing.

Large PDF splitting may additionally use `qpdf` or `pypdf`.
