# Documentation

Start with the [findings gallery](../FINDINGS.md): one entry per finding, with the paper, video, checks and formal coverage.

## Reading the collection

| Document | What it records |
|---|---|
| [Collection index](collection.md) | Every retained package with its result, boundary and evidence links |
| [collection.json](collection.json) | Machine-readable inventory that defines the retained findings |
| [Significance](significance.md) | Editorial assessment of correctness, originality and importance |
| [Review ledger](review-ledger.md) | Consequential review findings and corrections, and the limits of each review |
| [Formal coverage](formal-coverage.md) | Exactly which statements are checked in Lean, and which are not |
| [Research provenance](research-provenance.md) | How literature search, DeepResearch reviews and coding-agent proof work divided the labour |
| [Taxonomy](taxonomy.md) | Directory layout and why each finding sits where it does |

## Reproducing and verifying

| Document | What it records |
|---|---|
| [Reproduction guide](reproduce.md) | Commands for the Lean library, package checkers, papers and videos |
| [Verification records](verification/) | Dated integration, formal-library, media and release checks |
| [Release checks](verification/release-20261026/README.md) | The 26 October release, including the source scan and navigation audit |
| [artifact-hashes.json](artifact-hashes.json) | SHA-256 of every file in the 26 October release (commit `f09202d`), excluding itself |

`artifact-hashes.json` is a frozen release record and is not regenerated for later edits. `python3 tools/catalog.py check` checks the retained files against it, accounting for documented [public-release changes](../public-release/release-changes.json) and [export exclusions](../public-release/export-exclusions.json). The [path-redaction record](../public-release/path-redactions.json) separately records transformations of historical paths and identifiers. Historical hashes identify the original artifacts, not their edited public copies.

## Campaign records

- [17 October: physics and mechanics](campaigns/2026-10-17-physics-mechanics.md)
- [18 October: chemistry, biology and physics](campaigns/2026-10-18-chemistry-biology-physics.md)
- [18 October: genetics and mechanisms](campaigns/2026-10-18-genetics-and-mechanisms.md)
- [25-26 October: discoveries](campaigns/2026-10-25-discoveries.md)

Campaign records are dated working notes. Each package's README and readiness file give its current status.
