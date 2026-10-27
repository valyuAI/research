# Evidence ledger

Audited 26 October 2026 UTC against the final [paper](../paper.tex), [README](../README.md),
video brief and exact verification code. Audit-time hashes are in audit/source-hashes.json.
The film is an accessible proof outline, not a formal proof.

| Scenes | Evidence | Scope and limits |
|---|---|---|
| Hook, Rule | check_numbers.py, sections 1 and 4; verification/symplectic_billiard.py | Exact period 92 and rectangle period 4. Repetition refers to the ordered pair, not just one endpoint. |
| Billiards | check_numbers.py, section 2 | Exact 14-bounce rectangle example. The irrational slope claim follows by unfolding: a return with the same direction requires a rational displacement ratio. The stale ordinary-triangle claim was removed. |
| Octagon | Paper definition and normalization lemma; check_numbers.py, section 3 | Lattice corners, four specified directions, mirror parallel to a side. Arbitrary incommensurable real parameters are not covered. |
| Corners, Boxes | Paper critical-set definition and criterion; check_numbers.py, sections 5, 6, 8 | C has 20 points. The displayed box returns in 16 hops. General side-sequence regions contain cells; two return laps separate coordinates, four undo flips. Every path means a bi-infinite well-defined orbit. |
| Naive | verification/filled_set_results.txt; paper filled-set remark | Exploration has not closed after 20,000 sampled points, denominators reach 16384. This does not prove infinity. Only the first 1200 points are drawn; the 20,000 statement reports the saved computation. |
| Dots, Why | Paper half-lattice lemma; check_numbers.py, sections 5-7 | S has 16 whole-coordinate, 6 diagonal half-coordinate and 4 horizontal half-coordinate points; C is a subset. The odd-side condition blocks the dangerous move. Exact examples include (7/2,1/2), (7/2,6), and hypothetical (5/4,3/4). |
| Conclude | Paper theorem and computations; check_numbers.py, sections 4, 11 | N=26 gives 4(N²-N)=2600. Recorded sample periods are 4,16,32,44,68,92, without claiming exhaustive exact periods. Other octagons have other finite N. |
| Lopsided | Paper asymmetric proposition; verification/asymmetric_octagon_check.py; check_numbers.py, section 10 | Exact six-cycle and local multipliers -2,-1/2. Animation demonstrates forward contraction. The paper separately proves backward existence outside a countable exceptional set; the displayed rational nudge does not certify that whole backward argument. |
| Status, Ending | Package README and paper scope; symmetric-Hexhouse corollary | 1484 parameter tuples, counting rescaled and mirror copies separately. High correctness confidence after internal review, originality less certain. No external peer review or Lean formalization. |

## Primary sources checked

- Albers, Banhatti, Sadlo, Schwartz and Tabachnikov, *Polygonal symplectic billiards*,
  [arXiv:1912.09404v1](https://arxiv.org/abs/1912.09404v1), Section 6, Conjectures 6.1/6.2,
  Figures 18/23 and Question 7.1. Retrieved through valyu contents on 26 October 2026.
  Definition, conjecture and reported periods were read directly. Old ordinary-billiard
  open-problem wording is not treated as current.
- Albers, Lander and Westermann, *Symplectic billiards for pairs of polygons*,
  [arXiv:2402.12244](https://arxiv.org/abs/2402.12244). Requested /html/2402.12244v2 with
  valyu contents on 26 October 2026. The extracted text numbers the finite-critical-set
  criterion 3.5(III), whereas the package's v2 audit numbers it 3.4(III). The statement
  agrees in substance; this fetch does not independently establish the version numbering.
  The video attributes the criterion without a theorem number.
- The package cites Albers and Tabachnikov, *Introducing symplectic billiards*,
  [arXiv:1708.07395](https://arxiv.org/abs/1708.07395), published 2018. Historical
  attribution retained from the campaign's verification, not re-fetched for this edit.

Full extracts remain locally in ignored audit/private-cache/, not for distribution.
The source documents and prior reviews were not edited.

## Campaign reviews reused

- dynamics-symp-priority: DR-019.
- dynamics-octagon-review: DR-085.
- dynamics-hexhouse-review: DR-058.

Consulted the dynamics LOG and completed reports. No new DeepResearch task was started.
These records are internal review, not external refereeing. Search non-discovery does
not establish novelty. The video names its remaining open cases: asymmetric Hexhouses,
Penthouses, incommensurable octagons and the general convex-polygon symplectic question.
Reproduction and actual media checks are in README.md and audit/validation.json.
Narration uses a synthetic voice. No listening review or audience test is claimed.
