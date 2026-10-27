# Global optimality of conjugate restart laws

[Up to topic](../README.md)

A five-page paper on global optimality and uniqueness of conjugate renewal restart laws for one-dimensional Brownian search, together with a finite-state reversibility characterization. Lean covers the finite-kernel inequality and exact counterexample. The analytic theorem and converse have written proofs; priority remains provisional.

- The [public PDF](../../../../public-release/papers/conjugate-restart.pdf) lists Harvey Yorke and Valyu DeepResearch as co-authors and records the contribution and review status. The earlier archival `paper.pdf` is omitted from the public export; its hash is retained in the release records.
- `paper.tex` and `references.bib`: editable mathematical source and bibliography.
- [public paper](../../../../public-release/papers/conjugate-restart.pdf): shared byline with a research-assistance statement.
- `journal.tex`: small wrapper around the same mathematical source.
- `paper.bbl` and `journal.bbl`: generated bibliographies for source portability.

Run `./build.sh` with a standard TeX Live or MacTeX installation. The script compiles both presentations and leaves the full build logs locally. These are research drafts, not externally peer-reviewed publications. See the repository's [formal coverage](../../../../docs/formal-coverage.md), [review ledger](../../../../docs/review-ledger.md), and [reproduction guide](../../../../docs/reproduce.md).

## Evidence

[Computational verifier and results](verification/README.md) · [Lean source](../../../../formal/ValyuResearch/Resetting.lean)
