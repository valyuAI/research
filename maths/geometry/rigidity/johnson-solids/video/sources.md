# Evidence ledger

Reviewed 2026-10-26. Scientific claims follow the final local paper and readiness document, not earlier numerical searches. Input hashes and displayed-motion checks are in `qa/geometry-check.json`.

| Claim or visual | Primary evidence | Scope |
| --- | --- | --- |
| Fixed lengths, planar faces; squares may shear | `../paper.tex`, Introduction; `../readiness.md` | Regular convex starting realisations; local rigidity only |
| J3, nine vertices, fifteen edges, triangle + tetrahedron | `../verification/data/J03.json`, `results/flex_finite.json`, paper Continuous flexes | Exact `minkflex.check` replay performed by `prepare_assets.py`; display geometry frozen in `geometry.json` |
| J3 motion, face flatness, alternating 115/125 degrees | Same accepted edge partition and admissible axis | All visualised angles within +/-8 degrees; 161 numerical display checks supplement the exact certificate |
| J1 rigidity | Paper Scope/prior work and elementary Pythagoras argument | Existing result; illustrative failed rhombus deformation is not a valid flex |
| 41 first-order rigid, 45 flexible, 6 second-order rigid | `results/classification.json`, `results/second_order.json` | Local rigidity total 47; first-order dimension is not a motion-family dimension |
| 38 component rotations and 7 prism constructions | Paper Continuous flexes; `results/flex_finite.json` | Complete list, not every possible flex |
| Six exceptional solids; J60/J82 prestress stable | `../readiness.md`, `results/second_order.json`, `results/prestress_replay.json` | J58/J59/J81/J83 exactly not prestress stable; no reliance on old failed J81 numerical attempt |
| 17-stage successful replay | `../readiness.md`, `results/replay/20261026T125315Z/` | Reported research replay; this video worker did not rerun every stage |
| Novelty limits | Paper Scope, readiness Correctness/originality | No earlier full classification found in recorded search; no proof of priority, no new general criterion |

Background retrieved through `valyu contents` on 2026-10-26. Citation metadata is retained in `qa/background-sources.json`; the full responses remain outside the repository:

- [Rigidity of polytopes with edge length and coplanarity constraints](https://arxiv.org/abs/2505.00874), abstract confirms the model and flexible cube.
- [Deformations and second-order rigidity of polytopes](https://arxiv.org/abs/2607.09252), the prior study referenced by the package. The final package, not an abstract alone, supplies theorem-specific claims.

Teaching simplifications: vector addition uses a generic two-arrow diagram before actual J3 component geometry. The straight two-bar example illustrates the loss of a first-order direction through a squared term; its equation is not claimed to be one of the Johnson certificates. Antiprism theorem, large determinants, and J80/J81 comparison are omitted to avoid rushing the central mechanism.

Internal reviews and replay are not external peer review. The independent coordinator audit remains separate.
