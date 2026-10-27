# Adversarial review and responses

Valyu DeepResearch task `tilings-review-marked` (max, DR-031, completed 26 October 2026) refereed a draft of the paper. It recommended a major revision and found no fatal flaw in the encoding. Below, each point and what we did.

| # | Objection | Response |
|---|---|---|
| 1.1 | Draft tables had TBD rows; exactness claimed before all runs finished. | Accepted. All runs are now complete for root review; every value in `results.json` has a witness and a DRAT-verified upper bound at k = h + 1 (enforced by `check_ledger.py`). |
| 1.2 | An exact-imbalance-1 run is not evidence for imbalance >= 1. | Accepted. The sentence was removed; the k = 6 bar results rest only on the imbalance >= 1 base formulas. |
| 1.3 | "Optimal" conflates lattice and geometric numbers, unbalanced and all markings, and conventions. | Accepted. "Lattice", "unbalanced", "one centred mark per edge" and "strict" now appear in the abstract, results and theorems. The paper states that balanced non-tilers are outside the method and that the realized figures may admit more coronas off the grid. |
| 1.4 | Cannot claim to match Mann's specific markings without showing them. | Accepted. We report our optimal markings explicitly (block of bumps, one flat, block of nicks). We say we could not compare with Mann's Figure 5 in detail, and that they coincide with the Atlas entries up to swapping bumps and nicks. The comparison is about values, not markings. |
| 1.5 | Smith attribution should be credited to Džuklevski. | Accepted; reworded. |
| 2.1 | Proposition 3.1(2) used the converse of (1) without proof. | Accepted. The proof now uses an injection of interior bumps into nicks and the inequality d·|S_R| <= nu·|E_R|. |
| 2.2-2.3 | Wording of (1); notation clash for delta; O(R) needs an area argument. | Accepted; fixed (S_R, E_R defined, area argument given). |
| 2.4 | "Neighbouring midpoints at least sqrt2/2 apart" is false for hexagons. | Accepted. The proof now gives per-grid constants: midpoints of a cell's edges are at least 1/2 apart, and the distance from an edge midpoint to any other grid edge is sqrt3/6 (hexagons) or 1/2 (squares). So r < 1/4 suffices. |
| 2.5 | The proposition needs "one centred mark per edge"; the m = 2 remark is off-centre. | Accepted; stated as a hypothesis, and the m = 2 remark says it is not covered. |
| 2.6 | Finiteness via the extension theorem: cite exactly. | Accepted; cited as Grünbaum-Shephard Section 3.8. |
| 2.7 | Part (3) needs the interior-containment line. | Accepted; added. |
| 2.8 | The counting idea is classical. | Accepted; credited to Epstein and Mann, with Džuklevski's density form. |
| 3.2-3.3 | The relaxed notion is neither Kaplan's H_h nor Day's void-permitting convention; "even if holes are allowed" misleads. | Accepted. Removed from the theorem. The remark now says explicitly that the relaxation keeps the compatibility rule and is neither H_h nor Day's convention. The definitions section cites Day's convention (Eppstein), under which Ammann's hexagon reaches 4. |
| 3.4 | Grid alignment matters for upper bounds; abstract should say "lattice". | Accepted. |
| 3.5 | Contact constraint uses "level <= j-1". | Accepted; noted as a sound relaxation for UNSAT, with witnesses checked against the definition. |
| 4 | Weak points: two encoders share a specification; reproducing Mann's values tests mostly lower bounds. Suggested a comparison with `heesch-sat` on unmarked shapes. | Accepted and done. With all edges flat and no imbalance constraint, our encoder's Hc agrees with Kaplan's `heesch-sat` on the unmarked non-tiling polyhexes listed in the paper. This tests the corona encoding, including its UNSAT side, against an independent implementation of the specification. |
| 4 | Proofs not retained. | Partly accepted. One small formula produced bit-identical proofs on repetition; this was not tested on every formula. Original hashes and regeneration/replay commands are recorded. The two largest proofs (hundreds of MB) are not in the repository. No verified checker (cake_lpr) was used; this is stated. |
| 5 | Atlas already lists the hexapillar rows at H = 5 exact, apparently with 6 refuted, for specific markings. | Accepted; this is the most important prior-art point. We checked the Atlas inventory data: deltille words `BBCBCBCBBBBCBCBCBB` (18 edges, marks 8 up, 9 down, 1 flat) and `BBCBCBCBCBBBBCBCBCBCBB` (22 edges, 11 up, 10 down, 1 flat) are the straight 4- and 5-rows, listed with H = 5. The paper and README now say this, and limit our novelty to the maximum over all markings. |
| 6 | Mann-Thomas enumerated all assignments for a small family; overlap unknown. | Accepted. Kaplan's wording is verified in the arXiv text and quoted. Originality for the small tables is now rated moderate to low. |
| 6 | "First machine-checked" for Bašić is unsafe; the Commons file is a third-party upload; Bašić did his own computer check; the radius-38 sentence is a non-result. | Accepted on all points. Reworded to "independent, replayable exact check". The Commons provenance and Bašić's computer statement are given, and the radius sentence is removed. |
| 7 | The Atlas authorship is inferred; it is unreviewed and AI-assisted. | Accepted. It is cited by title as a website associated with Anton Bakker, and marked as not peer reviewed. |

Points not adopted:

- "Run the encoder on the Atlas's marked words" and "with the hexapillar marking fixed, expect UNSAT at 6". These runs are implied by the all-markings results (each is a sub-case of the imbalance >= 1 formula). The Atlas uses a different lattice, so a direct comparison would test a different model.
- Citing Mann (2005, Discrete Comput. Geom.). We did not read it and kept the counting credit to sources we read.
