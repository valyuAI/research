# Final research readiness: common quartets

Status: sharp-constant update complete. The written proof passed a fresh review; the sharp inequality and equality example compile in Lean with standard axioms only. The updated executable proof checks and all nine final PDF pages pass. The previous full `--game` replay remains the evidence for unchanged finite computations. Harvey Yorke has not yet completed a line-by-line review of every proof.

## Exact statements

- h(3) = 14. An explicit triple on 13 leaves has no common quartet; exhaustive 14-leaf colourings establish the upper bound.
- For every integer k >= 1,
  `2^k + 2 <= h(k) <= floor(3 ((1+sqrt(13))/2)^(k-1)) + 1`.
- `23 <= h(4) <= 28`, `34 <= h(5) <= 61`, `66 <= h(6) <= 125`.
- The lower bound `2^k+2` is already stated by Snir and Yuster. The contribution is an explicit construction and proof, not discovery of that bound.
- The new contributions, subject to the documented priority search, are the exact h(3) value, the checkable finite upper-bound proofs, the single-exponential upper bound, the certified small-k upper bounds and the 22-leaf four-tree witness.

## Review response

Original reports are preserved in `verification/reviews/`. Final review `DR-007` completed 2026-10-26 12:25:40 UTC, finding no mathematical error in the 3/16 inequality, caterpillar proof or 22-leaf witness. Its requests are addressed: relabel the smaller retained set, explain d >= 2 at each step, use exact threshold arithmetic, distinguish general from sharper small-k bounds, and handle the empty same-side subcase at k=2. The already published caterpillar bound is credited explicitly.

Additional corrections: caterpillar orders are not unique merely up to reversal; the end-cherry swaps are now acknowledged. A claim of global one-pair-strategy optimality was removed: the verifier establishes the safe pairs used, not every possible strategy's optimum. The count checkers now fail on unexpected results instead of merely printing them. A second quartet algorithm using edge splits was added; it shares only the Newick parser with the distance algorithm.

## Commands and evidence

`nice -n 10 sh build.sh --game` exited **0** at 2026-10-26 13:08:16 UTC. At that audit all 34 non-manuscript input hashes matched. That original build manifest and `completion-manifest.json` are preserved as historical evidence. The sharper update below changes the manuscript, proof executor and Lean file; its new manifest records those current inputs and outputs.

- Distance checker: 13-, 12-, 11-leaf triples and the 22-leaf four-tree family have zero common quartets.
- Edge-split checker: independently confirms 0/715 for the 13-leaf triple and 0/7315 for the 22-leaf family.
- Enumeration: all 135 shapes and all 5-, 6-, 7-subsets at 14 leaves, 1,138,995 cases, zero failures. At 13 leaves: 66 shapes; 891 failures for size 5 and zero for size 6.
- Independent safe-pair verifier: upper bounds 7, 14, 28, 61, 125 for k=2..6 pass.
- Caterpillar construction: exhaustive checks through k=6, including 677,040 four-sets at k=6, pass.
- Fresh K=5 generator output matches the saved table byte for byte; the recursion agrees with exhaustive labelled trees on all 1,075 tested colour-count instances for 5..8 leaves.
- Historical SAT records cover exactly shapes 0..134: 135 UNSAT and 135 DRAT VERIFIED; independent Kissat encoding also has 135 UNSAT. Those expensive solver/proof runs were not repeated in this resume. Original proofs had been removed after the earlier verification; logs, CNF hashes and replay scripts survive. The fresh exhaustive proof does not depend on replaying them.

Full resume log, input manifest, final typesetting log, Lean output and negative-control results are preserved in `verification/results/resume-20261026/`.

## Formal scope, confidence and pending work

Lean now covers the sharp real-variable inequality (`potential_step_sharp`) and equality example (`potential_step_sharp_witness`), plus the older 3/16 theorem (`potential_step`). The supplied file does not formalise trees, the iteration, the caterpillar proof, SAT/DP or h(3)=14.

Correctness confidence: high. Originality confidence: moderate-high for the new exact value and upper bounds, with a limited negative literature search. The journal version of Snir-Yuster was not directly accessible to the final reviewer, so expansion of its omitted construction is unverified. Internal reviews are not external peer review. The sharp update received a fresh review.

Three exploratory 23-leaf searches, with cycle types `4^5 2 1`, `4^5 1^3` and `4^5 3`, produced no recorded witness or UNSAT certificate. They are **unresolved**, not a proof of h(4)>=24 or its negation. They are not needed for any retained claim.

## Deliverables

- [Paper PDF](../../../../public-release/papers/common-quartet-number.pdf), [editable LaTeX](paper.tex).
- [Narrated-video brief](video-brief.md), with exact trees, counts and the 16/32 potential example.
- [Verification guide](verification/README.md).

## Earlier full-package audit

- `nice -n 10 ~/.elan/bin/lake env lean ValyuResearch/CommonQuartetPotential.lean`, from the existing formal directory: exit 0. The package copy is byte-identical to that file; both were extended during the sharper-constant update below.
- A second Lean invocation appending `#print axioms ValyuResearch.CommonQuartet.potential_step` also exited 0. The only dependencies reported are `propext`, `Classical.choice` and `Quot.sound`.
- The [recorded negative-control results](verification/results/resume-20261026/negative-controls.log) report that all four controls rejected their altered inputs. Both quartet algorithms reject three identical trees, the colouring checker rejects an incorrect expected failure count, and the safe-pair verifier rejects a table altered to claim h(4)<=27. The last rejection concerns that supplied certificate, not the mathematical possibility of h(4)<=27.
- The earlier PDF had eight inspected pages. The sharp update produces nine pages; its inspection is recorded below.

No computation required for the retained claims is pending. The optional 23-leaf searches above remain explicitly unresolved. The earlier artifact hashes are in `verification/results/resume-20261026/completion-manifest.json`; use the sharp-update manifest below for current files.

## Sharper constant accepted, 26 October 2026

Review `DR-017` found no error in the exact c=(7-sqrt(13))/18 lemma, real-variable sharpness example or derived upper bound. It executed symbolic identities and finite numeric/integer scans; its proposed tree simulation did not complete and is not counted as evidence. The paper now includes the full two-case proof. The weighted cut is on the larger retained set and that set is re-identified at every iteration. The general thresholds for k=1..8 are 4,7,16,37,85,195,448,1031, while the stronger small-k bounds remain unchanged.

Formal scope at this update: the sharp inequality and its equality example are now Lean checked, as well as proved in writing and independently reviewed. Its optimality is only for the stated real-variable inequality, not all potentials, tree strategies, or the growth base of h(k). The original completion manifest records the earlier package; `verification/results/sharp-potential-completion-20261026.json` records the sharper update.


## Sharp update verification

- `verification/iterate_check.py`: exit 0. The sharp iteration passed on 613 families for k=1..6 at n=4,7,16,37,85,195. Each step checks the sharp factor using exact rational/integer comparisons, separation in every processed tree and potential above 2. Final quartets are checked by distances. The rational grid minimum is 17/90, above the sharp real constant. Simulations corroborate the bookkeeping; they do not prove the universal theorem.
- Exact threshold table through k=8: 4,7,16,37,85,195,448,1031. The integer-square-root calculation avoids floating-point threshold errors.
- Lean: `potential_step_sharp` and `potential_step_sharp_witness` compile. A separate axiom audit reports only `propext`, `Classical.choice`, `Quot.sound` for both. The package copy matches the formal-project source byte for byte. Logs: `verification/results/sharp-potential-lean-20261026.log` and `sharp-potential-axioms-20261026.log`.
- Final LaTeX build passes with no warnings, overfull boxes or undefined references. All nine pages rendered at 110 dpi and visually inspected, including the sharp proof and revised threshold paragraph. Render hashes and final inputs are recorded in `verification/results/sharp-potential-completion-20261026.json`.
- The unchanged family enumerations, dynamic programme, SAT records and caterpillar construction retain their earlier complete audit. The sharp update does not claim a fresh replay of those expensive checks.
