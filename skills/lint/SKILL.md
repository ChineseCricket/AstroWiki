---
name: lint
description: Run deterministic health checks on the wiki. Mandatory before synthesis or release.
---

# llm-wiki Lint

```bash
python tools/lint.py --quiet                # wiki/ only
python tools/lint.py --quiet --include-inbox  # include drafts
python tools/lint.py --json                 # machine-readable
```

Checks: frontmatter, type, provenance, claims (source pages), synthesis structure, wikilink resolution, index references, `.kb/manifest.json`. Fix all FAIL before approval.
