---
name: ask
description: Answer questions against an AstroWiki knowledge base using approved wiki pages, search/get/graph tools, and query-derived outputs.
---

# Astro KB Ask

Use this for question answering over an existing AstroWiki project. Answers are `query-derived` and must stay in `outputs/`.

## Workflow

1. Run `python tools/lint.py --quiet` unless the user only needs a quick lookup.
2. Search for candidate pages:

   ```bash
   printf '{"method":"search","params":{"query":"your topic","limit":5}}\n' | python tools/server.py
   ```

3. Fetch the most relevant pages by slug or path:

   ```bash
   printf '{"method":"get","params":{"slug":"page-slug"}}\n' | python tools/server.py
   ```

4. Check nearby context when links matter:

   ```bash
   printf '{"method":"graph_neighbors","params":{"slug":"page-slug"}}\n' | python tools/server.py
   ```

5. Answer from approved `wiki/` pages first. Use `outputs/queries/` only as prior query context, not as evidence for new wiki claims.
6. If saving the answer, write Markdown to `outputs/queries/YYYYMMDD-topic.md`.

## Answer Rules

- Cite page slugs or paths for every substantive claim.
- Distinguish established facts from inference.
- Preserve uncertainty and source limits.
- Never silently resolve contradictions; include `## Contradictions` when sources disagree.
- Do not write query-derived answers into `wiki/`, `inbox/`, or `raw/`.
- Do not edit `raw/` while answering questions.

## Output Shape

Prefer:

- Direct answer
- Evidence
- Contradictions, if any
- Open questions or follow-up searches
