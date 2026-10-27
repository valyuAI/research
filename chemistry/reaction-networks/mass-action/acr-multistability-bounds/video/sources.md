# Source and claim ledger

Locked package read locally on 26 October 2026. No new research or checker run was undertaken for production. `scientific-input-sha256.json` freezes all 30 non-video package files before production. The final QA rechecks every frozen digest.

- [Paper](../paper.tex), definitions and Dimension two section: both reactants and products at most bimolecular; ACR at positive steady states; stability within a class; two distinct nondegenerate positive equilibria in the same class; factorisation, opposite slope and concavity arguments. Clips a03-a08, a16-a29.
- [Paper, constructions](../paper.tex), six-complex example: the exact eight directed reactions, vector field, three states and characteristic polynomials. Clips a09, a11-a15, a30, a32. `trajectory-data.json` contains illustrative numerical solutions from (1,2.5,2.4) and (1,3.5,1.7), produced with solve_ivp at rtol=1e-10, atol=1e-12. Those curves illustrate outcomes; they do not certify stability.
- [Exact certificates](../verification/examples-certificate.json), [standard-library checker log](../verification/verify_examples.log), [independent checker log](../verification/independent_check.log): exact reconstruction, positivity, roots and stability. Clips a15 and a34.
- [Readiness](../readiness.md), [review](../review.md), [completion manifest](../verification/results/completion-manifest-20261026.json), [final review](../verification/reviews/chem-acr-final-review.md): final retained claims, review coverage and novelty limits. Clips a30-a37.
- [Video brief](../video-brief.md): worked KNS two-dimensional example. In this example C, not A, is the robust species; both states have c=1/2. Clips a16-a18.
- [Paper, lower bounds and decoupled remark](../paper.tex): exact minima 3 dimensions, 6 complexes, 3 species; species conclusion follows from a separate Z regulator added to a two-species switch. Clips a30-a33.
- [Formal source](../../../../../formal/ValyuResearch/AcrMultistability.lean): example vector fields, positive equilibria and ACR only. Stability, minima and dimension-two theorem are not formalised. Clip a35. The research completion manifest records the formal source hash.
- Kaihnsa, Nguyen and Shiu, *Absolute concentration robustness and multistationarity in reaction networks: conditions for coexistence*, EJAM 35(4), 566-600 (2024), [DOI](https://doi.org/10.1017/S0956792523000335). Prior minima and conjecture are quoted and discussed in the locked paper and reference bibliography; no fresh priority search is claimed.
- Feinberg's deficiency one theorem is credited in the paper bibliography. The animation cites its role in the six-complex lower bound without pretending to display its full proof.

The quadratic in the obstruction scene and the concave graph are schematic mathematical examples of the proved sign properties. They are not fitted trajectories or an additional network. The valley/hill picture is explicitly an analogy. The six-complex network is a mathematical witness, not an experimentally validated device.

Production provenance: built-in Cedar narration through the existing secure toolkit; model, voice and text digest in `audio/manifest.json`. Credentials are never included. The user did not request publication. No audio listening, audience test or external peer review is implied by machine QA.

Validated checker update after media production: the assertion-mode guard is recorded in `scientific-input-supplement.json`. Original scientific snapshots and run evidence remain intact. Root's full normal check passed, while normal negative, `-O` and environment-optimization controls reject. Media, narration and scenes are unchanged.
