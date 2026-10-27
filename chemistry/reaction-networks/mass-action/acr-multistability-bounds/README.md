# ACR with multistability: minimal dimension and minimal number of complexes

An at-most-bimolecular mass-action system with absolute concentration robustness (ACR) in two dimensions is never multistable. If a stoichiometric class contains two nondegenerate positive steady states, they are the only ones in the class and one of them has a real positive eigenvalue. Consequently ACR with multistability needs **dimension at least 3** and **at least 6 complexes**, and both minima are attained by explicit three-species networks. Three species suffice, so the species part of the Kaihnsa-Nguyen-Shiu conjecture is false.

- [Paper](../../../../public-release/papers/acr-multistability-bounds.pdf) with [LaTeX source](paper.tex) and [references](references.bib).
- [Verification scripts and certificate](verification/README.md).
- [Video brief](video-brief.md).

## The question

Kaihnsa, Nguyen and Shiu, *Absolute concentration robustness and multistationarity in reaction networks: conditions for coexistence*, European Journal of Applied Mathematics 35(4):566-600 (2024), [DOI 10.1017/S0956792523000335](https://doi.org/10.1017/S0956792523000335), arXiv:2307.04186v1 (KNS). They proved that ACR with nondegenerate multistationarity in an at-most-bimolecular network needs at least 3 species, 3 reactant complexes, 5 complexes and dimension 2, all sharp. Section 6 conjectures, verbatim in arXiv v1 and the journal version:

> the lower bounds (on dimension and the numbers of species, reactant complexes, and all complexes) for the coexistence of ACR and multistability are strictly larger than the bounds proven here for ACR and multistationarity.

## Answer

| quantity | ACR + multistationarity (KNS) | ACR + multistability (this package) | conjecture part |
|---|---|---|---|
| dimension | 2 | **3, exact** | true |
| complexes | 5 | **6, exact** | true |
| reactant complexes | 3 | between 4 and 6 (between 5 and 6 for three species); 4 would need at least 5 species | true |
| species | 3 | **3, exact** | **false** |

## Status

| statement | type | where | correctness confidence |
|---|---|---|---|
| Theorem 3.1: dim 2 + ACR, two nondegenerate positive steady states in a class are the only ones there and one has a real positive eigenvalue | theorem, hand proof | paper Section 3 | high |
| Corollary 4.1: dimension at least 3 | theorem (Thm 3.1 + KNS) | Section 4 | high |
| Corollary 4.2: at least 4 reactant complexes; at least 5 for three species | theorem (Cor 4.1 + KNS Thm 5.5 and 1.2(4)) | Section 4 | high |
| Theorem 4.3: at least 6 complexes | theorem (Cor 4.1 + kinetic-subspace count + Feinberg 1987 Deficiency One Theorem, Cor 6.2.2) | Section 4 | high |
| Proposition 4.4: exactly 4 reactant complexes forces at least 5 species | theorem, hand proof; its combinatorial step is also confirmed by an exhaustive exact enumeration (1365 complex sets) in two implementations | Section 4 | high |
| Example 5.1 (6 reactions, 7 complexes) and Example 5.2 (8 reactions, 6 complexes): ACR in A and bistability | exact computation, two implementations; field, ACR and exact steady-state list also proved in Lean 4 (`formal/ValyuResearch/AcrMultistability.lean`, no `sorry`, standard axioms only); stability not in Lean | Section 5 | high |
| Remark 5.3: decoupled three-species example | exact computation | Section 5 | high |
| minimum reactant complexes (4, 5 or 6?) and minimum reactions (6 or fewer?) | open | Section 6 | - |

Originality confidence: moderate-high. No prior statement of Theorem 3.1, of the minimal dimension or complex counts, or of a three-species ACR plus bistability network was found (searches listed below). The only published ACR plus bistability network found has eight species and dimension six (Joshi-Nguyen-Johnston, arXiv:2605.11389). The species part of the conjecture also fails for a trivial reason (Remark 5.3: a bistable two-species network plus a decoupled `0 <-> Z`), which the paper states openly; the substantive content is the dimension-two obstruction and the exact minima for dimension and complexes.

What the result is not: it is not a generic-rates statement (Theorem 3.1 holds for each fixed rate vector), it does not settle the minimum number of reactant complexes or reactions, and the theorems are not formalized in Lean (only the example computations listed above).

## Examples

Example 5.1, species A, B, C, rate constants in brackets:

```text
A+B -[2]-> 2B,  B -[2]-> 0,  0 -[60]-> A+C,  2C -[1]-> A+C,  A+C -[13]-> 2C,  B+C -[2]-> B
db/dt = 2b(a - 1)                     (ACR: a = 1 at every positive steady state)
at a = 1:  b = (c^2 - 13c + 60)/2,   dc/dt = -(c - 3)(c - 4)(c - 5)
steady states (1,15,3) stable, (1,12,4) saddle, (1,10,5) stable
```

Example 5.2 (six complexes `A, C, A+C, B, 2B, B+C`):

```text
C <-[1]/[1]-> A+C,  A -[6]-> A+C,  B <-[11]/[1]-> 2B,  C <-[6]/[6]-> B+C,  B+C -[1]-> B
da/dt = c(1 - a);  at a = 1:  c = 6/b,  b db/dt = -(b - 2)(b - 3)(b - 6)
steady states (1,2,3) stable, (1,3,2) saddle, (1,6,1) stable
```

## Prior work and priority checks

- KNS (above): source of the conjecture; proves the multistationarity bounds, Theorem 5.5 (`>= dim + 1` reactant complexes) and Theorem 1.2(4) (`>= n + 2` reactant complexes when full dimensional). These are used and credited.
- Feinberg, Chem. Eng. Sci. 42 (1987) 2229-2268, Theorem 6.2.1 and Corollary 6.2.2 (Deficiency One Theorem; requires one terminal strong linkage class per linkage class, not weak reversibility). Text checked directly.
- Joshi-Nguyen-Johnston, arXiv:2605.11389v1: ACR plus bistability in an 8-species dual-site futile cycle with bifunctional enzymes (Michaelis-Menten steps, so at most bimolecular; dimension 6); no minimality.
- Jiao-Tang-Zeng, J. Math. Biol. 91(6):82 (2025), arXiv:2406.11586, and Tang-Zhang, arXiv:2608.01116: minimal multistable zero-one networks, no ACR. Our examples have stoichiometric coefficient 2, so they are outside the zero-one class.
- Banaji-Boros-Hofbauer, arXiv:2406.13451: planar quadratic networks, no ACR.

Searches (26 October 2026): Valyu paper and web search from 2026-08-15 for ACR with multistability or bistability, the KNS conjecture and dimension-two ACR; arXiv 2610.32739, 2610.05242, 2610.11970 read (no overlap); Zenodo API for "absolute concentration robustness" (3 records, unrelated), "Kaihnsa" (1 record, unrelated) and bistability with robustness; GitHub and Lean projects; author pages of Kaihnsa and Shiu. DeepResearch audits: `chem-acr-priority` (heavy, DR-033: no prior resolution), `chem-acr-review` (max, DR-035: no error in Theorem 3.1; fixes adopted, listed below), `chem-acr-final-review` (max, DR-049: no fatal error; recomputed both examples, Theorem 4.3 and Proposition 4.4; supplied the hand proof now used in Proposition 4.4; flagged the Table 1 cell, the framing of the trivial species counterexample and a citation update, all adopted. Its one 'unverified' item, the main case analysis of Theorem 3.1, had been omitted from its prompt for length and was audited by `chem-acr-review`). An absence of hits is not proof of novelty.

Review fixes adopted from `chem-acr-review`: notation for the class, explicit density argument in Lemma 3.2, sharpened conclusion of Theorem 3.1, credit to KNS Theorem 5.5 and 1.2(4) for the reactant-complex bound and the three-species row, direct citation of Feinberg 1987 Corollary 6.2.2, and replacement of an ambiguous example in Remark 5.3 by an exact one. Fixes adopted from an independent adversarial check (all claims held): Table 1 row label for three species, explicit non-vanishing of `phi - T` in Proposition 4.4, KNS Theorem 1.2(4) cited specifically for n = 3, corrected scope sentence on ACR for all rate vectors. The citation labels Theorem 6.2.1 and Corollary 6.2.2 were checked against the text of Feinberg 1987.

## Reproduce

From this directory:

```sh
sh build.sh
```

This runs `verification/verify_examples.py` (standard library, exact rationals), `verification/four_reactant_exponents.py` (standard library, exhaustive enumeration), `verification/independent_check.py` (SymPy, Groebner bases; skipped with a message if SymPy is missing) and compiles the Lean file `formal/ValyuResearch/AcrMultistability.lean` when `lake` is on the path (output in `verification/lean_check.log`; empty means no errors or warnings), and builds `paper.pdf` with `pdflatex` and `bibtex`. Runtime is about a minute, mostly Lean.

## Final research audit

The [readiness report](readiness.md) records the completed build, exact stability replay in both implementations, review coverage, negative controls and eight-page PDF inspection. ACR concerns positive steady states, not universal convergence; stability is relative to the stoichiometric class. The optional prior-network screen is bounded and does not establish absence or priority.
