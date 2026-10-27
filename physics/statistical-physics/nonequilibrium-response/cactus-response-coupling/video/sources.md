# Evidence ledger

Audited 26 October 2026 UTC against the final [paper](../paper.tex), [README](../README.md),
video brief, stored verification and campaign reviews. Audit-time hashes are in
audit/source-hashes.json. The running example has clockwise rates 2 and reverse rates 1.

| Scenes | Evidence | Scope and limits |
|---|---|---|
| Hook, Hopping | check_numbers.py, sections 1-2; numbers.json | Seeded illustrative simulation, not a molecular experiment. Exact stationary law is (1/3,1/3,1/3). Net clockwise hops total 1 per unit time across three edges, or 1/3 per edge. |
| Trees, TreeTheorem | Paper Section 1; check_numbers.py, section 1 | Tree weights 4,2,1, totals 7,7,7. The classical tree theorem is stated and demonstrated, not proved in the film. |
| Knob | Paper Eq. (5); check_numbers.py, section 3 | Finite 1% nudge gives totals 7,7.06,7.04 and relative percentage changes approximately -0.474,+0.379,+0.095. Exact (-10,8,2)/21 is the infinitesimal relative response per relative nudge. Unweighted averaging uses the uniform starting law. |
| Families, Conjecture, Reframe | Paper definition and coupling lemma; check_numbers.py, section 4 | Exactly 27 families, 18 arrow multisets, 11 UC. Independent draws choose non-UC with probability 152/343. Bags preserve direction and multiplicity. Plot illustrates one knob. |
| Staircase, Tokens | Paper cycle theorem; check_numbers.py, sections 5-6 | Windows of 2^(-k) give exact root lotteries. Seven family probabilities are exactly 1/7 by rational cone integration; the 400,000-draw tally is only an illustration. |
| WhyUC | Paper cycle theorem and dominant-family lemma; Fancher-Horowitz Lemma 4 | Gumbel bonuses scaled by 1/log(2) match doubling-scale bars. Divide both rates on each edge by its positive multiplier. The cancellation w/(bc)=wa/(abc) preserves winner ordering for all roots. Equal bags imply equal family product, contradicting a strictly lighter tree. |
| Cactus | Paper block factorization, gluing, limits and main theorem | Block weights multiply and root laws factor. Animation shows bidirected simple graphs; missing arcs and parallel arcs require the paper's extra arguments. |
| K4 | verification/k4_no_coupling_certificate.json; check_numbers.py, section 7 | Exact: 16 trees/root, 65536 families, 5955 multisets, 346 UC. UC scores are 0,2,4. Expected score is -74467043099669441/1314877998480476367. Excludes full tree-law coupling, not the response conjecture. |
| K4 extension | Paper minor lemma/theorem; verification/k4_subdivision_results.json | Connected graph with a K4 minor, both directions on every link: some positive rates have no coupling. Not every rate choice, and not arbitrary orientations. Subdivision check has 984 UC families. |
| Status, Ending | Paper scope; verification/numerical_evidence_results.json | 150 K4 searches found no response violation; not a proof. Diamond error about 0.061 is a stored-seed Monte Carlo discrepancy. Feasible sampled couplings do not give a general construction. |

## Primary sources checked

- Fancher and Horowitz, *Topological building blocks of nonequilibrium response*,
  [arXiv:2607.12096](https://arxiv.org/abs/2607.12096), Eqs. (5),(6),(8), Lemma 4 and
  discussion. Retrieved through valyu contents from /html/2607.12096 on 26 October 2026.
  Read the response formulation, UC definition, dominant-family argument and request
  for a proof of Eq. (6).
- Classical tree theorem, Gumbel-max and related sampling work are cited in
  [references.bib](../references.bib) and the final paper. These are background tools,
  not claimed as new. The exact joint cycle construction is narrower than general
  perturb-and-MAP sampling.

Fetched content remains in ignored audit/private-cache/, not for distribution.
The paper, source verification and existing review artifacts were not edited.

## Campaign reviews reused

- statphys-cactus-review: DR-066.
- statphys-cactus-max: DR-036.
- statphys-k4minor-review: DR-028.

Consulted the statphys LOG and reread the completed max and minor reviews. No new task
was launched. Correctness confidence is high after internal review; originality remains
less certain. Not finding a prior result does not establish priority. No external peer
review, Lean verification, listening review or first-time audience test is claimed.

The film omits full proofs of the classical Gumbel-max identity, compactness limit and
graph-minor lifting. It explicitly distinguishes the strong coupling from the weaker
response conjecture, which remains open beyond the covered family. See README.md and
audit/validation.json for reproduction and actual media checks.
