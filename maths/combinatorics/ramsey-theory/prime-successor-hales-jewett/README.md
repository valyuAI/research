# Exact off-diagonal Hales-Jewett numbers at prime successors

[Up to topic](../README.md)

For every prime p, the off-diagonal number HJ(p+1,2) equals p+1. The three-page paper gives an explicit coloring and a complete proof; the entire main theorem is formalized in Lean. Correctness confidence is high. Priority remains provisional after the recorded literature review.

- The [public PDF](../../../../public-release/papers/prime-successor-hales-jewett.pdf) lists the human author and records the contribution and review status. The earlier archival `paper.pdf` is omitted from the public export; its hash is retained in the release records.
- `paper.tex` and `references.bib`: editable mathematical source and bibliography.
- [public paper](../../../../public-release/papers/prime-successor-hales-jewett.pdf): human-author presentation with a research-assistance statement.
- `journal.tex`: small wrapper around the same mathematical source.
- `paper.bbl` and `journal.bbl`: generated bibliographies for source portability.

Run `./build.sh` with a standard TeX Live or MacTeX installation. The script compiles both presentations and leaves the full build logs locally. These are research drafts, not externally peer-reviewed publications. See the repository's [formal coverage](../../../../docs/formal-coverage.md), [review ledger](../../../../docs/review-ledger.md), and [reproduction guide](../../../../docs/reproduce.md).

## Evidence

[Computational verifier and results](verification/README.md) · [Lean source](../../../../formal/ValyuResearch/HalesJewett.lean)

[Readiness](readiness.md) · [Author proof walkthrough](author-walkthrough.md)
