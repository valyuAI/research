# All qudit stabilizer codes of distance three

**Claim (theorem).** Let q ≥ 3 be a prime power. An F_q-linear stabilizer code [[n, k, 3]]_q with k ≥ 1 exists if and only if r = n − k ≥ 4 and n ≤ μ_q(r). Here μ_q(r) is the largest partial line spread of PG(r−1, q):

- μ_q(r) = (q^r − 1)/(q^2 − 1) for even r;
- μ_q(r) = (q^r − q^3)/(q^2 − 1) + 1 for odd r.

Every admissible parameter set is attained by a code that is pure to distance three. For prime q every stabilizer code is F_q-linear. For odd r the maximum length is q − 1 below the ordinary quantum Hamming bound; for r = 5 it is q^3 + 1. Against the strengthened Hamming bound of Yu, Lai and Oh (arXiv:1005.4758, Theorem 2(ii), valid for impure codes of distance 3 and 4) the gap is smaller: for q = 3, r = 5 the maxima are 30 (Hamming), 29 (strengthened) and 28 (this theorem); for q = 4, r = 5 they are 68, 66 and 65.

For qubits the corresponding classification is Yu, Bierbrauer, Dong, Chen and Oh (IEEE TIT 2013). For q ≥ 3 the even-redundancy maximum (quantum Hamming codes) and the case r = 4 were known, and Bierbrauer and Edel (J. Combin. Des. 2000, Theorems 9, 11, 12) already constructed pure codes of length μ_q(r) − 1 for every odd r ≥ 5. The support-removal idea behind our impure reduction goes back to Gottesman (1997 thesis, Section 7.3) and is reused by Nemec and Tansuwannont (arXiv:2306.00048, Section IV, Lemma 1). What is new here: the geometric refinement of that reduction for all q and all distances d ≥ 3, attaining the endpoint μ_q(r) for general q, and covering every admissible length. For q = 3 the endpoint also follows by pasting the tabulated [[28,23,3]]_3 code into the Bierbrauer-Edel family.

[Paper](../../../../public-release/papers/distance-three-qudit-codes.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md)

## Consequences for codetables.de (snapshot 25 October 2026, live pages re-checked)

| Entry | Table | New | Reason |
|---|---|---|---|
| [[59,54]]_4, [[61,56]]_4, [[62,57]]_4, [[65,60]]_4 | 2–3 | **3** (exact) | new F_4-linear codes (certificates) |
| [[29,24]]_3, [[66,61]]_4 | 2–3 | **2** (exact) | Theorem 3.4; Proposition 5.3 (additive ququart) |
| [[30,23]]_3, [[67,60]]_4 | 3–4 | **3** (exact) | reduction + projection; Prop. 5.3 |
| [[27,21]]_5, [[51,45]]_7 | 3–4 | **3** (exact) | reduction + Thas's generalized-arc bound |
| [[52,44]]_7 | 4–5 | **4** (exact) | reduction + projection + Thas |
| [[53,43]]_7 | 4–6 | 4–**5** | reduction + projection + Thas |

Twelve entries improve and eleven become exact. These are bounds on stabilizer codes, as in the tables.

## Ingredients

1. **Geometry.** A code pure to distance three is a set of pairwise skew lines in F_q^r, with isotropy given by a weighted Plücker relation Σ λ_i u_i ∧ v_i = 0.
2. **Impure reduction (Lemma 3.1, any distance d ≥ 3).** A geometric form of Gottesman's support-removal and packing argument. Let t be the dimension of the span of the stabilizer elements of weight below d. Positions outside their supports carry planes in a space of dimension r − t, and any d − 1 of them are independent. Hence n ≤ (d−1)t + m_q(d, r−t).
3. **Partial spread bound** (Beutelspacher 1975; a self-contained hole-counting proof is given), plus an inequality showing that impure codes never beat μ_q(r) for q ≥ 3.
4. **Constructions.** The lines L_a = ⟨(1,0,a), (0,1,aω)⟩ for a ∈ GF(q^{r−2}) have Plücker vectors quadratic in a. Balanced weighted blocks of them (affine lines, planes, Lagrange 4-sets, line pairs), an explicit absorption of the extra line for r = 4, 5, and a sumset induction give every length. Base cases q ∈ {3, 4, 5} come from 245 stored certificates.
5. **Higher distance.** Projection from a line and Thas's bound q^2 + 1 for generalized arcs of PG(5, q), q odd.

## Status and confidence

- **Correctness: high.** The written proofs are short. The 255 certificates pass an independent standard-library checker and seven corrupted inputs are rejected. The four new ququart codes and the q^3 + 1 codes pass a third, hand-written rank-based check. The inductive recipe was replayed with no search over line configurations (some line-block weights are chosen by seeded random coefficient trials, so the replay is reproducible but not a deterministic transcription of the proof): q = 3 to r ≤ 8, q = 4 to r ≤ 7, q = 5, 7, 8 to r ≤ 6, q = 9, 11 to r ≤ 5, q = 13 at r = 4. A max-mode DeepResearch adversarial review found no error affecting any statement. Its minor corrections are incorporated, and its gap on additive ququart codes is closed by Proposition 5.3. A CP-SAT solver confirms that the largest partial line spread of PG(4,2) has 9 lines. For PG(4,3) it found 28 lines but did not close the gap to its bound of 30 within 50 minutes, so that case rests on the written proof. Not formalized in Lean.
- **Originality: moderate** (for the full spectrum as well as the table values). Two DeepResearch audits, an independent referee and our own searches found no earlier statement of the odd-r maximum for q ≥ 3, of the full spectrum, or of the twelve table values. The search was bounded. Not new: the support-removal and packing method (Gottesman 1997; Nemec-Tansuwannont 2023), pure codes one short of the odd-r maximum for every q (Bierbrauer-Edel 2000), and a strengthened Hamming bound for impure distance-3 codes (Yu-Lai-Oh 2010). The instance [[28,23,3]]_3 of the extremal family was already in the tables, and pasting it into the Bierbrauer-Edel family gives the q = 3 endpoints for all odd r.
- **Significance: modest.** This is a complete answer to a natural finite-geometry question about qudit codes, the q ≥ 3 analogue of a known qubit classification, together with a batch of table corrections. It is not a new error-correction scheme. Distance four with odd redundancy remains open: for q = 3, r = 7 the lengths known to us run up to 16, against our bound of 29. A concurrent dataset (Zenodo 23295497) works on that case.
- **Scope.** The theorem concerns F_q-linear stabilizer codes, which for prime q are all stabilizer codes. Merely additive codes over non-prime fields are covered only by Proposition 5.3, for the two q = 4 entries. Non-stabilizer codes are not covered.

## Independent review

An independent referee report (26 October 2026) confirmed the classification with high confidence: it re-derived the geometry, the impure reduction for d ≥ 3, the hyperplane count, the constructions and the additive ququart argument, rechecked all 255 certificates with its own exact-arithmetic program (each has exact distance 3), replayed the full induction (7,224 configurations) and re-read all twelve live table entries. Priority confidence: moderate. Revisions applied:

1. `check_codes.py` now exits nonzero in its default run when required base-case coverage is incomplete (explicit-file mode is unchanged), `build.sh` stops on any verification failure, and `verification/missing_certificate_check.py` (run by `build.sh`) deletes a required base certificate in a temporary copy and confirms the checker fails.
2. Prior art: Bierbrauer-Edel 2000 Theorems 9, 11, 12 (pure codes of length μ_q(r) − 1 at every odd r ≥ 5), Gottesman 1997 Section 7.3 and Nemec-Tansuwannont 2023 Lemma 1 (support-removal and packing), and Yu-Lai-Oh 2010 Theorem 2(ii) (strengthened Hamming bound for impure d = 3, 4) are now cited and discussed. The novelty claims are narrowed to the all-q, all-distance geometric refinement, the endpoint μ_q(r) for general q, and the full set of lengths.
3. The Hamming comparison above now distinguishes the ordinary bound (q − 1 above our maximum) from the strengthened one (30/29/28 for q = 3, r = 5; 68/66/65 for q = 4, r = 5).
4. Lemma 3.1 is stated for d ≥ 3, the domain of m_q(d, s). At d = 2 the column planes may repeat (the referee's pure [[3,1,2]]_3 example).
5. The replay is described as free of search over line configurations but using seeded random trials for some line-block weights.

## Priority checks performed (25-26 October 2026)

- **Literature and DeepResearch.** A heavy priority audit and a max-mode adversarial review (task IDs below) found no earlier odd-redundancy classification for q ≥ 3 and no record of the twelve parameter sets. Bierbrauer–Edel's twisted-code tables for q = 3, 4, 5, read directly, stop at length q^3 for redundancy five; their 2000 paper (Theorem 12) gives length μ_q(r) − 1 for every odd r ≥ 5. The independent referee identified Gottesman (1997), Nemec-Tansuwannont (2023) and Yu-Lai-Oh (2010) as further predecessors; all three were read at the cited locations and are now cited.
- **arXiv from 2026-09-01.** API searches for "partial spread" with "quantum", "distance three" with "stabilizer", "distance 3" with "qudit", "quantum Hamming bound" with "qudit", "impure" with "stabilizer codes", and "codetables" found no overlap. Two recent preprints prove Hamming-type bounds for general codes: arXiv:2606.22538 (Zhang–Chen) proves the ordinary quantum Hamming bound for q ≥ 3, which for odd r is weaker than ours by q − 1; arXiv:2610.30088 (Grishin–Zabokritskiy) extends the strengthened bounds of Yu, Lai and Oh to all codes; at distance three the strengthened bound (already proved for impure codes by Yu-Lai-Oh 2010) allows 29 for q = 3, r = 5 and 66 for q = 4, r = 5, one more than our maxima 28 and 65.
- **Zenodo.** API searches for qudit, qutrit and ququart stabilizer codes, partial spreads and codetables found only record 23295497 (distance four, including [[16,9,4]]_3), which is cited and does not overlap.
- **GitHub.** Issue searches on the-omega-institute/trureturing, Naixu-Guo/quantum-open-problems and google-deepmind/formal-conjectures, plus global searches for "codetables", "qudit stabilizer" and "partial spread", found nothing on distance-three qudit codes. Foundation-0/gfq-codes (19 October 2026) targets the classical linear-code tables, not quantum codes.
- **Source pages.** The codetables.de updates page shows no qudit quantum-code update after 24 May 2024. The twelve entries were re-read live on 25 October 2026 with the bounds listed above. Simeon Ball's home page shows no newer result on this question.

None of this proves novelty; it records what was checked.

## Reproduce

```sh
sh build.sh                                      # checker, negative checks, bounds, PDFs (about 1 minute)
python3 -B -O verification/replay_recipe.py      # induction replay (about 20 minutes)
python3 -B verification/generate_certificates.py # regenerate certificates (deterministic seeds)
```

Python 3 standard library only; LaTeX via pdflatex and bibtex.

## Provenance

DeepResearch tasks: scout-quantum-information `DR-062`; priority audit `DR-003`; adversarial max review `DR-008`. Coding agents parsed the tables, found the arguments and constructions, and wrote the generator, checkers and paper. These are internal checks, not external peer review.
