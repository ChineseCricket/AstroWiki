# Migration Guide

Use this guide to move an existing research project into AstroWiki.

## 1. Install

```bash
python tools/install.py --target /path/to/project
```

If installing from a cloned template into a non-empty project, review conflicts before using `--force`.

## 2. Place Existing Material

| Existing material | AstroWiki target |
|---|---|
| Literature PDFs | `raw/documents/` |
| ADS/arXiv/S2 metadata markdown | `raw/ads/` or `raw/notes/` |
| Existing approved literature summaries | `wiki/sources/` |
| Existing concept notes | `wiki/concepts/` |
| Project reports or generated Q&A | `outputs/` |

Do not put ad hoc query answers into `wiki/`.

## 3. Normalize Provenance

Run:

```bash
python tools/astrowiki_lint.py --include-inbox
```

Fix pages until there are no FAIL issues.

## 4. Use Inbox for Uncertain Pages

If a migrated page is not yet verified, place it under `inbox/` and approve later:

```bash
python tools/astrowiki_queue.py list
python tools/astrowiki_queue.py approve <slug>
```

## 5. Validate Search

```bash
printf '{"method":"search","params":{"query":"your topic","limit":5}}\n' | python tools/astrowiki_mcp_server.py
```
