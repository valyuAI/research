# Review response and final mathematical audit

Internal reviews are evidence, not external peer review. Original campaign reports remain unchanged in the lab task directories.

## Reviews used

- `socialchoice-snm-priority`, heavy, `DR-080`.
- `socialchoice-snm-review`, max, `DR-040`.

## Resolved objections

1. **Eight-team equality was unsupported.** Accepted for the earlier draft. The old exactly-three-team floating solution is not evidence for the standard definition. The final CC and MT certificates cover every coalition of size 2 or 3 and every nontrivial internal reorientation. Both pass exact replay over 2,889,600 manipulations; the MT rule also passes 192,640 monotonicity checks and all top-cycle support checks.
2. **SSW17's general question is already refuted.** Accepted. Only the finite k=3 cases and (k,n)=(4,7) are retained. There is no all-n or small-k threshold theorem.
3. **LP row counts differed from manipulation counts.** Resolved: 2,667,216 distinct nonzero inequalities after deduplication versus 2,889,600 unmerged manipulation checks. The exact replay enumerates the latter.
4. **Source wording.** Verified directly through Valyu Contents on 26 October 2026: SSW17 Theorem 3.2 gives the lower bound for n>=2k-1; SWZZ20's introduction contains 939 and 1878; MSS24 Theorem 3 requires TCC and Section 5 proposes small-n LPs. The latter attributes the LP to SSW17; we report that attribution without claiming that we located the LP there. The 31/60 bound belongs to randomized death match, and SignificantOnly is defined for n>=6.
5. **Shard-merging integrity.** Certificate hashes are checked, every worker exit is checked, and each sharded run uses fresh files. A final audit binds every result to its certificate, exact count, standard le definition and claimed properties.
6. **Weak-strategyproofness side result.** Excluded: Brandt-Lederer Remark 3 already contains it.

## Final audit

- Symmetrization is a convex average on a finite, permutation-invariant feasible set. It applies at each n separately and does not couple tournament sizes.
- The lower-bound averaging argument also works with arbitrary matches among the extra teams, provided all extra teams lose to the regular core. The wording is explicit now.
- Orbit invariance makes the certificate a well-defined labelled rule. Recomputing isomorphism classes and transporting lotteries then checks the full set of relabelled constraints. The independent labelled implementation confirms both CC and MT rules at every n=3..6 without relying on canonical forms.
- For n=5..8, the plain CC certificates have positive slack on every manipulation outside the identified lower-bound configurations. This proves the finite optimal-face observation; it does not prove an all-n structural rule.
- Correctness confidence: high. Originality confidence: moderate after bounded searches, with unpublished computations remaining a priority risk. This is a finite computational research note.

## Primary sources checked

- https://arxiv.org/html/1605.09733
- https://arxiv.org/html/1906.03324v2
- https://arxiv.org/html/2407.17569v1

All six pages of the final paper were rendered at 100 dpi and visually inspected. The results table and five-team table are legible; no overlap, clipping, unresolved citation or LaTeX warning remains.
