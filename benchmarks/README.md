# Private Benchmarks

Real benchmark fixtures are intentionally not tracked in this public template.

Recommended local path:

`/Users/jing-yizhang/Documents/Research/AstroWiki-private-benchmarks/`

Run with:

```bash
python tools/benchmark.py --fixture /path/to/private-fixture
```

Local fixtures can also live under ignored `benchmarks/private/` directories:

```bash
python tools/benchmark.py --fixture benchmarks/private/s2fitting-noria
python tools/benchmark.py --fixture benchmarks/private/final-project-scaling
```

For one-off checks, point the runner at a read-only knowledge base directly:

```bash
python tools/benchmark.py --kb-root /path/to/astrowiki-project --profile astrowiki --name s2fitting-noria
python tools/benchmark.py --kb-root /path/to/legacy-project --profile legacy-wiki --name final-project-scaling
```

Supported fixture keys include `kb_root`, `profile`, `expected_min_score`,
`checks`, `min_pages`, `required_pages`, `required_searches`, and
`required_terms`.
