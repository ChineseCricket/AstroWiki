# Release Checklist

Before tagging a release:

- [ ] `python tools/lint.py --quiet`
- [ ] `python tools/sync.py search "galaxy cluster" --limit 1 --dry-run`
- [ ] `python tools/server.py --smoke`
- [ ] private benchmark fixtures pass locally when available
- [ ] README quick start still matches tool behavior
- [ ] no credentials or local absolute paths are committed

Release notes should mention:

- schema changes;
- tool interface changes;
- benchmark score changes;
- known limitations.
