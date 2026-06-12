---
name: astro-md-table-export
description: Export Markdown tables from wiki pages or reports to Excel workbooks under outputs/exports. Inspired by z-md-excel.
---

# Astro Markdown Table Export

Use when the user wants wiki comparison tables or review tables as spreadsheets.

## Workflow

```bash
python tools/export_wiki.py tables wiki/concepts/example.md --output outputs/exports/example.xlsx
```

If XLSX support is unavailable, export CSV files under `outputs/exports/`.

## Rules

- Read from `wiki/`, `inbox/`, or `outputs/`.
- Write only to `outputs/exports/`.
- Do not modify source Markdown files.
- Strip inline Markdown formatting when exporting cells.
