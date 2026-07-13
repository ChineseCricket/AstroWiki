# AstroWiki Framework Upgrade Notes

Comparison baseline: `ChineseCricket/AstroWiki` commit
`d9df64ee9da8b82b577b35ef53b373891a9aa04e` (2026-06-18).

## Upgrade Summary

The fork changes AstroWiki from a portable, general-purpose astrophysics
knowledge-base template into a detector-oriented research framework for X-ray
TES microcalorimeters, FDM readout, and full signal-chain simulation.

### 1. Detector-oriented architecture

- Adds `ARCHITECTURE.md` with a six-stage source-to-metrics signal chain.
- Defines the TES-current waveform as the detector/readout boundary contract.
- Adds a two-tier fidelity model: a fast response/template path and a detailed
  nonlinear ODE/SDE plus FDM path.
- Maps the knowledge base to the project's TES, LC, SQUID, DAQ, BBFB,
  reconstruction, calibration, and validation subsystems.
- Adds `CLAUDE.md` as a compact operating guide for agents.

### 2. Stronger schema and provenance controls

- Adds the `entity` page type for laboratories, groups, missions, and projects.
- Adds detector-domain metadata such as `domain`, `mission`, `url`, and
  `github_url` to source records.
- Expands locator guidance with documentation-page locators and explicit
  confidence semantics.
- Requires every claim to retain citekey, locator, and confidence information.
- Requires complete English-Chinese synthesis pages with mirrored evidence,
  tables, caveats, wikilinks, citekeys, and locators.

### 3. Agent governance and workflow specialization

- Keeps the strict `raw -> inbox -> wiki -> outputs` ownership model while
  making controller, worker, and reviewer routing explicit.
- Specializes review toward citation and detector-physics correctness.
- Makes lint mandatory before synthesis or release.
- Prevents query-derived output from flowing back into approved knowledge.

### 4. Domain-specific skills

- Adapts all eleven skills to the TES/FDM simulation workflow.
- Extends compilation to concept, method, instrument, and entity drafts.
- Changes `pack` from web capture to provenance-preserving knowledge bundles
  for downstream agents and sibling wikis.
- Changes `tables` from spreadsheet export to cross-source parameter and
  simulator-feature comparison.
- Adds ADS/arXiv fallback guidance and detector-specific gap examples.
- Requires bilingual output in the synthesis skill.

### 5. Tooling changes

- Adds `tools/reindex.py` to rebuild `wiki/index.md` and `.kb/manifest.json`.
- Adds `entity` discovery to shared page tooling.
- Raises the recommended source-claim range from 3-8 to 3-10.
- Adds deterministic checks for the Chinese synthesis section and thesis.
- Improves search ranking with title and tag weighting and returns explicit
  incoming/outgoing graph relations.
- Retains approval-queue diff support and fixes the fork's missing dispatch
  branch for that command.

## Deliberate Narrowing From Upstream

The fork removes several portable-template facilities from AstroWiki:

- template installer (`tools/install.py`);
- built-in ADS client (`tools/sync.py`);
- generic JSONL/ZIP/table exporter (`tools/export.py`);
- private benchmark runner and fixtures interface (`tools/benchmark.py`);
- upstream CI workflow, examples, migration guide, release checklist, and
  machine-install guide.

These removals reduce portability and automation, but keep the local framework
small and focused on the detector-simulation knowledge base. The corresponding
capabilities should be restored if this fork is later distributed as a general
template.

## Compatibility Notes

- The local JSON service is a one-request stdin service rather than upstream's
  line-oriented long-running loop.
- The local service intentionally omits upstream `submit_feedback`.
- Literature synchronization is currently a skill-level workflow; the upstream
  executable ADS client is not included.
- Knowledge content, raw source material, generated query outputs, and the
  bundled SIXTE source tree are project data, not framework upgrades.
