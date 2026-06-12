# Release Checklist

Before tagging a release:

- [ ] `python tools/astrowiki_lint.py --quiet`
- [ ] `python tools/ads_sync.py search "galaxy cluster" --limit 1 --dry-run`
- [ ] `python tools/run_benchmark.py --fixture benchmarks/fixtures/s2fitting-noria`
- [ ] `python tools/run_benchmark.py --fixture benchmarks/fixtures/final-project-scaling`
- [ ] MCP smoke test returns JSON for `search`
- [ ] README quick start still matches tool behavior
- [ ] no credentials or local absolute paths are committed

Release notes should mention:

- schema changes;
- tool interface changes;
- benchmark score changes;
- known limitations.
