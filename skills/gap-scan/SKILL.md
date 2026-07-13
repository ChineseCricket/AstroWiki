---
name: gap-scan
description: Identify knowledge gaps — shallow sources, missing coverage, orphans, synthesis opportunities. Read-only analysis.
---

# llm-wiki Gap Scan

Write the report to `outputs/reviews/`.

## Gap types

- **Depth**: sources with abstract-only / weak locators (e.g. low-confidence TES-physics claims).
- **Coverage**: important topics not represented (e.g. our FDM readout chain has no method page yet).
- **Structure**: orphan sources not linked by concepts/synthesis.
- **Synthesis**: ≥3 sources spanning a theme with no synthesis page.

Priority: HIGH (affects design conclusions) / MEDIUM / LOW.
