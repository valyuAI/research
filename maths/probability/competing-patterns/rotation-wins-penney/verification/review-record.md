# Adversarial review and responses

This is the response record for the mathematical argument, separate from the bounded priority audit. A favorable review is not used as a substitute for a proof or an executed checker.

## Independent mathematical reviews

The first review found no fatal issue in the uniform proof for lengths at least eight. It required an explicit finite bound on the avoidance series at 1 and an argument counting only anchors inside the root clump. The paper now gives the disjoint-window bound `P(1) <= k/(2/k!)`, defines anchor ending-time stopping times, and proves the root-clump geometric bound with conditional necessary events.

The second review passed the refined cancellation lemma, finite tail, complete path coverage, both closure/counting procedures, mask and integer ranges, complement symmetry, and all finite rational comparisons. It requested that the tail index `q` be explicitly a nonnegative integer. The paper now says so. The reviewer independently checked small controls and all saved outputs; the full fresh executions were performed separately during the campaign.

## Max review

Task `DR-044`, completed 26 October 2026 at 11:47 UTC, found no fatal mathematical error, counterexample or prior proof. It independently reproduced all length-4-through-7 inequalities, re-derived the large-length argument and checked the overlap estimates. It withheld a packaging recommendation pending exposition, execution records and a rigorous length-three comparison.

The responses are:

1. **First-occurrence sign.** The revised proof assigns one negative sign per mark, forces a terminal mark, and obtains a signed sum of minus one exactly when no earlier occurrence exists. This directly gives `-F_i=P C_i`. It no longer uses the potentially ambiguous description of a positively marked terminal component.
2. **Half-binomial bound.** The paper states the exact gap-boundary prefix lengths and prescribed counts. Complementation changes a prescribed count at a boundary where the private rank sets differ, proving disjointness.
3. **Monotone pattern.** The proof explicitly assumes that the rotation `b` is monotone and identifies the corresponding original pattern. It does not confuse the two patterns.
4. **Stopping times.** The ending times, rather than the start positions, are stopping times in the observation filtration. The paper explicitly defines that filtration, places the root event in it, and applies the tower bound with the root event included. A suggested description of the starts themselves as stopping times is unnecessary and would use the wrong time index.
5. **Executed C++.** The real C++ program was compiled and run for every required representative. The four actual JSONL outputs are archived under `independent/`, with hashes. Every integer coefficient matches the standard-library Python reconstruction. The max review's Python port of the C++ algorithm is additional evidence and is not described as a real C++ execution.
6. **Length three.** The source gives exact recurrences, but its displayed table is rounded. A supplementary horizon-18 certificate now makes the strict inequalities independent of rounded values. Two different integer recurrences agree at every length and on the final resolved/unresolved counts. Assigning all unresolved cases against the rotation still gives a first-player upper bound below `47/100`. The case is credited to prior work, with no new-discovery claim.
7. **Direct length-nine control.** The campaign's direct enumeration actually reproduces first-hit counts `7383,9479` for `2341` versus `1234`. The max reviewer did not run that control; the build does. It supports sign conventions and is not substituted for the main proof.
8. **Infinite range.** No finite exhaustion at lengths at least eight is claimed. That range is the written uniform theorem, whose logic the reviews re-derived. Finite spot checks are additional controls only.
9. **Priority.** The audit is expressly bounded and originality confidence remains moderate. No specific prior resolution was identified. An exhaustive search of all possibly related material is not asserted; unavailable code-search coverage and database limits are recorded in `priority-audit.md`.

## Follow-up audit

Task `DR-014`, heavy with code execution, completed 26 October 2026 at 12:21 UTC. It found no material mathematical or computational gap in the new length-three certificate. It read both recurrences, hand-checked length four and verified the saved integer arithmetic. Its execution attempts did not produce output, so it did not claim to have run the code. That operational limitation is separate from our successful executions.

A third independent mathematical review actually ran both recurrences, checked every internal state and first-hit count against direct enumeration through length eight, and passed the conditional global-rank model and the infinite-horizon bound with high confidence. We then added a direct C++ permutation oracle at horizons eight, nine and ten, covering all six ordered races. Every horizon count, unresolved count and first-hit-time count matches both recurrences. The raw oracle output and an actual execution log are archived with the package. The requested reproduction item is therefore closed locally, without describing the remote review as an execution.

## Execution evidence

- All 2,952 coefficient arrays reconstructed in standard-library Python and independently in compiled C++.
- Exact representative coverage and all rational partial-sum/tail comparisons passed.
- Direct first-hit counts through length nine passed.
- Pointwise cancellation controls passed for every subset of starts through span 13 at lengths three through eight.
- All three horizon-18 length-three representatives passed both independent integer recurrences.
- Direct exhaustive C++ checks at horizons eight, nine and ten passed all six length-three races, including every first-hit-time extension count.
- The PDF build preserves the default TeX output restrictions by compiling inside its own temporary directory.
