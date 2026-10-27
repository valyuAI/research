# Integer weights never give a sound Colless-like balance index

Mir, Rotger and Rossello (PLoS ONE 13(9): e0203401, 2018; arXiv:1805.01329) introduced Colless-like balance indices C_{D,f} for multifurcating rooted trees and ended with the conjecture: "there is no function f taking values in the set of natural numbers that satisfies this property" (soundness: C_{D,f} = 0 exactly on fully symmetric trees). The arXiv v2 text of the 2023 survey by Fischer, Herbst, Kersting, Kuehn and Wicke (arXiv:2109.12281v2, Section 9.7) lists it as open.

## Claim

**Theorem (proved).** For a nonnegative weight function f on nonnegative integer outdegrees, if f(2), f(3), f(4) lie in gamma*Z for one real gamma > 0 (for example if they are rational, in particular natural numbers), then two non-isomorphic fully symmetric trees have the same f-size, so C_{D,f} is not sound for any dissimilarity D. This proves the conjecture.

Proof: words with m letters each of 2, 3, 4 give about 27^m fully symmetric trees with 24^m leaves; their internal f-sizes are integers (in units of gamma) between 0 and M*24^m; 27 > 24 and pigeonhole. Two pages in the [public PDF](../../../../public-release/papers/colless-like-integer-weights.pdf).

Status: theorem with a complete hand proof. Small explicit collisions (e.g. f(n) = n+1: FS(2,2) and FS(6) both have f-size 13) are checked by `verification/check_colless.py` (standard library). Not formalised in Lean.

## Confidence

- Correctness: high. Short pigeonhole proof; checked by a DeepResearch review (`phylo-colless-prior`, DR-082), which also suggested dropping f(0) from the hypothesis (adopted).
- Originality: moderate. No source found that proves, disproves or discusses the conjecture after 2018; the 2023 survey lists it as open. The argument is elementary, so a passing remark elsewhere cannot be excluded.
- Significance: modest. It closes an explicitly stated conjecture; the open question that remains (weights with values in a rank-two group such as Z + Z*sqrt(2)) is not addressed by the method.

## Priority checks performed (26 October 2026)

- DeepResearch audit `phylo-colless-prior`: Mir-Rotger-Rossello paper and bioRxiv preprint, the survey (arXiv v2 and book metadata), treebalance.wordpress.com fact sheet, the treebalance and CollessLike R packages, Rotger's 2019 thesis (accessible parts), later tree-balance papers 2019-2026: no resolution found.
- arXiv full-text search for "Colless-like" (newest first): only unrelated or already-cited papers.
- Zenodo API exact-phrase search "Colless-like": 0 records.
- GitHub API issue search "Colless-like" and "Colless conjecture Rossello": only software issues (hstrat, phylotrackpy, tskit) about computing the index.
- These searches are not exhaustive.

## Reproduce

```sh
sh build.sh     # runs verification/check_colless.py and builds paper.pdf
```

## Files

`paper.tex`, `references.bib`, [public PDF](../../../../public-release/papers/colless-like-integer-weights.pdf), `build.sh`, `verification/` (checker and README), `video-brief.md`.

## Final review scope

The review's main refinement, dropping any arithmetic restriction on f(0), is retained: all words in the proof have the same number of leaves, so that contribution cancels. The paper now explicitly counts internal contributions after scaling. The rank-two discussion is limited to this fixed-alphabet counting argument; no theorem ruling out all rank-two sound weights or all possible counting methods is claimed.

The original review is preserved in `verification/reviews/phylo-colless-prior.md`. It is a heavy priority/correctness audit, not a separate max-mode final review or external peer review. No formal proof assistant is used. Final commands, review responses and artifact links: [readiness.md](readiness.md).
