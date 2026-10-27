# Linear equivalence of Lotka-Volterra tree systems

[Up to topic](../README.md)

A five-page self-contained reconstruction proof for generic Lotka-Volterra tree systems. This is an independent verification note with **no priority claim**: an earlier withdrawn preprint announces a closely matching result. Lean checks the three-vertex path algebra; the full reconstruction theorem remains a written proof.

- The [public PDF](../../../../public-release/papers/tree-equivalence.pdf) lists Harvey Yorke and Valyu DeepResearch as co-authors and records the contribution and review status. The earlier archival `paper.pdf` is omitted from the public export; its hash is retained in the release records.
- `paper.tex` and `references.bib`: editable mathematical source and bibliography.
- [public paper](../../../../public-release/papers/tree-equivalence.pdf): shared byline with a research-assistance statement.
- `journal.tex`: small wrapper around the same mathematical source.
- `paper.bbl` and `journal.bbl`: generated bibliographies for source portability.

Run `./build.sh` with a standard TeX Live or MacTeX installation. The script compiles both presentations and leaves the full build logs locally. These are research drafts, not externally peer-reviewed publications. See the repository's [formal coverage](../../../../docs/formal-coverage.md), [review ledger](../../../../docs/review-ledger.md), and [reproduction guide](../../../../docs/reproduce.md).

## Evidence

[Computational verifier and results](verification/README.md) · [Lean source](../../../../formal/ValyuResearch/LotkaVolterra.lean)
