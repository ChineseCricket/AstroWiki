---
name: parse
description: Parse PDFs, images, Office files, and HTML into Markdown or JSON for AstroWiki raw staging. Inspired by z-smart-xparse.
---

# Astro Document Parse

Use this skill when a local document must be prepared for downstream AstroWiki compilation.

## Preferred Parser

Use `xparse-cli` when available:

```bash
xparse-cli parse path/to/file.pdf --view markdown --output raw/documents/file.md
```

For large PDFs, split before parsing:

- split if file size exceeds 5 MB or page count exceeds 100;
- default chunk size: 50 pages;
- parse chunks serially;
- merge Markdown chunks in page order.

## Fallback

If `xparse-cli` is unavailable:

- stage the original file in `raw/documents/`;
- create a short metadata sidecar;
- report that parsing remains pending.

## Rules

- Do not discard the original document.
- Do not write parsed output directly to `wiki/`.
- Never silently skip failed chunks.
