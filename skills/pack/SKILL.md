---
name: pack
description: Capture topic-related web pages into raw/web as local research packs. Inspired by z-web-pack but portable and path-neutral.
---

# Astro Web Pack

Capture web sources as local material under `raw/web/<topic>/`.

## Output

```text
raw/web/YYYY-MM-DD-topic/
  README.md
  00-research-brief.md
  01-link-inventory.md
  02-image-inventory.md
  03-reading-map.md
  MAIN-01-entry.md
  LINKED-02-related.md
  assets/
```

## Capture Rules

- Capture article body, tables, code, equations, source links, images, and direct videos when relevant.
- Skip sidebars, ads, footers, social share links, login pages, privacy pages, and decorative assets.
- Record failed and restricted URLs.
- Use local relative asset paths.

## Jina Fallback

Use `r.jina.ai` only after normal fetch fails or returns unusable content.

## Final Check

No external image URLs should remain in generated Markdown unless explicitly documented in `02-image-inventory.md`.
