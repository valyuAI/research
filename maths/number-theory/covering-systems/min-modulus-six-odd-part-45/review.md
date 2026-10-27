# Review record

## Adversarial review (Valyu DeepResearch, max mode)

Task `DR-073`, completed 26 Oct 2026 11:29 UTC. The reviewer received the full statement, the lemma, the reduction and a description of the search, but not the code.

| Point raised | Verdict | Response |
|---|---|---|
| Coordinates, price function, doubling lemma, corollary, symmetry reductions and pruning bound | No error found | None needed |
| Moduli below 6 and the "LCM exactly 2^a 3^2 5" condition | Do not affect the argument; the claim is slightly stronger than Problem 2 | Agreed |
| The abstract's "b = c = 1" exception contradicts the source paper's Theorem 1.8(i) (b ≥ 2) | The open case is b = 2, c = 1 | Agreed; stated in the paper and README |
| Vector (1,1,1,1,1,1) can never certify at level 2, since Q_2 ≤ 4 < 6 | Correct | Explained in the paper (Table 1). Removing it leaves the `dfs2.c` node count unchanged (498,464), so the other ten suffice |
| Hand check: the level-2 part of the source paper's infinite covering (columns 8, 16, 0, 36) has Q_2 = 37 = R for ρ = (15,6,5,6,3,2) | Consistent with tightness | Reproduced exactly by our code. It also gives equality for vectors 9 and 10; now a remark in the paper |
| Step 4 (the computation) could not be checked from the text alone | The theorem is conditional on the search | The package contains the price file, three implementations (two C, one standard-library Python), node counts that agree across implementations, run logs, negative controls and a calibration on known cases |
| Suggested sanity test on a case with known negative answer, e.g. m = 4 with odd part 9 | Useful | Done (`verification/calib.py`): the method proves (9, 4) and (15, 5) negative, and reports alive states for (9, 3) and (27, 4), where coverings exist |
| Prior art | Nothing found that settles Problem 2 or states the quantitative recursion Q' ≥ 2Q - R. The closest earlier tool is Krukenberg's qualitative reduction (Dalton-Trifonov Lemma 6 / Corollary 7; Klein Lemma 2) | Cited as related work |
| Side note: the source paper's proof of Theorem 1.7(i) cites "Lemma 5.2", but the lemma is numbered 5.1 | Cosmetic | Not used |

## Earlier priority audit

Task `DR-090` (heavy, completed 26 Oct 2026 10:00 UTC). It found no resolution of Problems 1 or 2 of arXiv:2605.18644, no erratum and no later version. It checked arXiv, erdosproblems.com forum threads 2, 7, 273, 586, 1188 and 1189, the erdosproblems.ai wiki, GitHub (trureturing, We-Solve, Foundation-0, formal-conjectures), Zenodo, MathOverflow and the USC repository.

## Remaining uncertainty

* The computational step is checked by independent re-implementation, not by a proof assistant.
* Priority rests on searches up to 26 Oct 2026. A note or repository that is not indexed cannot be excluded.

## Finish review, 26 October 2026

The build driver contained two evidence-handling defects: `./` was prepended to absolute temporary paths, and pipelines only displayed the last line instead of enforcing the expected result. These are repaired. A new driver requires exact totals, exit codes, price-order agreement and survivor-file lengths; cover self-test and finite-covering controls now fail nonzero on disagreement. Fresh primary/control C runs match the recorded counts. The three long Python slices remain the original completed runs.

The classification corollary was compared with the stored source fulltext of Theorem 1.8: four existence seeds (4,3,2), (5,2,2), (5,4,1), (6,3,1), and the stated exclusions support the corollary under a >= b >= c >= 1. The narration now retains that hypothesis. The concrete 12-residue warm-up and price example were checked exactly. The first price vector is inert, so the brief no longer says eleven useful vectors are necessary.

No optional odd135/min8 theorem is claimed. No new external task was launched; the earlier completed reports remain the literature evidence.
