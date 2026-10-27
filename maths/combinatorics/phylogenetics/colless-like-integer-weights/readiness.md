# Final research readiness: integer Colless-like weights

Status: research package complete; proof, package build and visual inspection of both PDF pages passed. Harvey Yorke has not yet completed a line-by-line review of every proof.

## Exact statement

Let f map nonnegative integer outdegrees to nonnegative real weights. If f(2), f(3), f(4) belong to gamma Z for one real gamma > 0, then two non-isomorphic fully symmetric rooted trees have equal f-size. Hence no Colless-like index C(D,f) is sound, for any dissimilarity D. In particular every natural-number-valued f fails, resolving the stated Mir-Rotger-Rossello conjecture under the paper's definitions.

There is no arithmetic restriction on f(0): the trees in the counting family have the same number of leaves, so their leaf contributions cancel. The proof compares `(3m)!/(m!)^3` distinct level words against at most `M 24^m+1` scaled internal sums. Since 27 > 24, a collision is forced for sufficiently large m.

## Review response and scope

The correctness/priority review `DR-082` confirmed the argument and suggested dropping f(0), which is incorporated. Its original report is preserved in `verification/reviews/phylo-colless-prior.md`. The primary paper's Lemma 10 supplies the collision-to-unsoundness implication; the manuscript also spells it out by joining the two equal-size symmetric trees under a new root.

The resume corrected the abstract: only scaled internal sums are integer-valued, not full f-sizes with arbitrary irrational f(0). It replaced an overbroad finite-rank lattice discussion with the precise limitation of this fixed-alphabet count: rank-two coordinate boxes can have O(24^(2m)) points, exceeding the roughly 27^m words. This does not settle existence of sound rank-two weights or rule out other methods.

No Lean formalisation, finite search proof of the universal theorem, or new final review is claimed. Small collision checks illustrate the hand proof. The 2023 open-status statement is read from the survey's arXiv v2, not directly from the Springer book body.

## Commands and results

`nice -n 10 sh build.sh` exited **0** during the resume. `verification/check_colless.py` finished with `OK`; LaTeX/BibTeX completed without warnings.

Examples checked by both the level formula and explicit trees include:

- f(n)=n+1: FS(2,2) and FS(6) each have size 13.
- f(n)=2^n: FS(2,3) and FS(3,2) each have size 26; this collision is already in the original paper.
- f(n)=n!+1: FS(2,2,2,2) and FS(4,3) each have size 77.

For each, joining the two subtrees produces a non-symmetric tree with zero tested dissimilarity score. Random integer-weight examples also satisfy the explicit counting threshold for sufficiently large m. These checks are examples, not the universal proof.

The resume build log and final artifact hashes are preserved in `verification/results/resume-20261026/`.

## Confidence and deliverables

Correctness: **high**, from a complete short hand proof and the reviewed definitions. Originality: **moderate**, because the recorded searches found no later resolution, while an elementary argument can be missed in an unindexed source. Rank-two weights remain outside the result. No required computation remains pending. No additional independent final review is recorded here.

- [Paper PDF](../../../../public-release/papers/colless-like-integer-weights.pdf), [editable LaTeX](paper.tex).
- [Narrated-video brief](video-brief.md): the 13-versus-13 example, exact counting formula and proof boundaries. No video was produced in this research task.

Final PDF inspection: both pages rendered and visually checked. Final LaTeX log has no warnings, overfull boxes or undefined references. Source/PDF SHA-256 hashes are recorded in `verification/results/resume-20261026/completion-manifest.json`.
