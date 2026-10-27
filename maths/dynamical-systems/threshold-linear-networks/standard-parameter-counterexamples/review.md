# Internal reviews and responses

These are internal adversarial reviews (Valyu DeepResearch), not external peer review.

## Review 1: `modelling-ctln-review1` (heavy; task DR-029)

Subject: the 100-vertex, 7-class example G100 at eps = 1/4, delta = 1/2.

The reviewer independently reproduced by hand:
- the conventions and K = I + 3N + 3J;
- the 174 deleted arcs;
- the permission vector (1, 4, 1, 1, 4, 1, 1)/16 of I + 3M, and det(I+3M) = 352;
- K^{-1}1 with minimum 1/1009, and det K = 22198;
- the coefficient c_2(K) = 33084, computed two ways (Geneson's formula and the reduction);
- a proof of the identical-row reduction det(zI+K) = (z+1)^{n-k} det(zI+Q).

The reviewer found no error.

| Point raised | Response |
|---|---|
| Positive stability of the 7x7 quotient Q was not reproduced by the reviewer | The paper and README list all seven Hurwitz determinants. Two independent exact programs check the full 100 x 100 matrix: `check_ctln.py` uses a multimodular characteristic polynomial and confirms the quotient factorisation, and `check_flint.py` computes all 100 Hurwitz determinants. |
| Nondegeneracy over all 2^100 subsets was not established; the conjecture is stated for nondegenerate CTLNs | Resolved for every graph by Lemma 1: at eps = 1/4, delta = 1/2, K_sigma = I (mod 3), so every principal and Cramer determinant is 1 (mod 3). |
| Priority: no counterexample at the standard parameters found | This was a limited search result, superseded by the later repository discovery. hturcotte1/CLTN already implied standard-point counterexamples, including W_4. Credited throughout. |

## Review 2: `modelling-ctln-review2` (max; task DR-074)

Subject: G11, the mod-3 lemma, the n <= 7 exhaustive scan, and the W_4 observation.

The reviewer verified the conventions, the mod-3 lemma, the full-support criterion and the restriction-to-support argument. It noted that an off-support neuron exactly at threshold cannot occur, because nondegeneracy makes the inequalities strict. By hand it checked these facts about G11: the permission vector Y/163 row by row, det K = 1168, tr K = 44, the z^9 coefficient 196, and p(-1) = p'(-1) = p''(-1) = 0. It also re-derived from the repository's formulas that W_4 is stable at t = 3 and W_3 is not. It found no mathematical error.

| Point raised | Response |
|---|---|
| Vertices 4, 6, 9 are in-twins (identical rows of N), not closed twins; only 7 and 10 are closed twins | Correct. Wording fixed in the video brief. The paper makes no twin claim. |
| The credit for W_k is understated. The repository's `notes/theorem_A_fixed/` files (commit `3744200`, 15 Oct 2026) contain exact stable t-intervals at beta = 3 (k = 4: t > 2.0932) and a "Theorem B" (k >= 6 stable at every legal point with beta <= 3), so standard-point counterexamples on 23 and 31+ vertices are implied | Accepted. We fetched and read both files. The README, paper and video brief now state this, and the novelty is scoped to the 11-vertex example, vertex-minimality, the mod-3 lemma and the n >= 8 bound. |
| The n <= 7 scan was not reproduced; the positive control is weak | The scan's exactness argument is documented in `verification/README.md`, and `scan.sh` replays it. The control at (21/10, 50) gives exactly the two graphs the repository's n = 6 map predicts there, Geneson's graph and one other. The repository's n <= 7 map independently implies the same exclusion; we cite it but do not rely on it. |
| Check the induced subgraphs of G11 | Done exactly (`check_induced.py`): none of the 2035 proper induced subgraphs works, so G11 is minimal under vertex deletion. |
| Conjecture numbering: 1.2 in the journal, 1.3 in the 2019 arXiv version | Both now stated. |
| "Standard parameters" wording not confirmed by the reviewer | The phrase appears in a figure caption of the extended arXiv version of Curto-Morrison (arXiv:2301.12638); the paper now says so. |
| Report the stability neighbourhood; say the margin is thin | Done: `region.pdf` shows a band 0.02 < eps < 0.44, and the README and paper state the decay rate of about 0.009 (Jacobian) and the simulation results. |
| Contact Geneson, the repository owner and the Zenodo author | Not done. The campaign rules forbid contacting anyone; this is left to the authors' discretion. |

## Final completion audit (26 October 2026)

All three original n7 shards completed. Their totals sum to 882,033,440; the original logs, candidate files and scanner source are preserved unchanged in `verification/recovery/`. All 35,842 coefficient-positive candidates were freshly replayed over rational arithmetic. Both Routh and Lienard-Chipart reject every candidate, with no disagreement. The final result binds the input files by SHA-256. The original permission filter uses a residual error bound; its IEEE arithmetic assumption and inverse/rounding bounds are documented explicitly. It is not an unchecked floating eigenvalue sign test, nor do we claim that 882 million rational solves were rerun during final completion.

Fresh scans of all n=2..6 graphs used no permission prefilter and enabled signed-overflow sanitization. Their counts match A000273, and their 0, 0, 2, 15 and 372 coefficient-positive candidates all fail exact stability. The six-vertex positive control checks 1,540,944 graphs and 2,322 candidates and finds exactly two stable graphs. The actual prefilter constants were independently compared with the Hadamard bound by exact squared rational comparisons for every n=2..7. Candidate replay rejects wrong counts, missing candidates, duplicates and wrong expected outcomes; those negative tests pass.

The two independent example checkers passed G11, W4, G27 and G100. The exact G11 deletion check accounts for all 2,035 proper subsets of sizes 2..10: 90 cliques, 1,778 nonpermitted and 167 permitted but unstable. Thus it proves vertex-minimality among nonclique supports, not that every proper subgraph is unstable. Orders 8, 9 and 10 are unsearched globally.

The written audit checks the positive-denominator rank-one identity, restriction to support, the mod-3 proof for principal and Cramer determinants, exclusion of exact off-support thresholds, and strict inequalities needed for a local parameter neighbourhood. The numerical region and trajectory plots are illustrations only. Sampled 30% perturbations do not prove a uniform basin bound.

Correctness confidence is high, subject to the documented enumeration and IEEE arithmetic model for the recovered n7 rejection filter. Originality confidence is moderate for G11 and the mod-3 lemma; the small-order exclusion is an independent verification of a consequence already implied by the prior repository's map. No first-ever standard-point failure or globally minimum eleven-vertex claim is retained.

All six final PDF pages were rendered and visually inspected. No clipping, overlap or unresolved reference was found. Underfull reference-line warnings are cosmetic; there are no overfull boxes. `readiness.md` records final hashes and replay commands.
