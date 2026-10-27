# Referee report: "ACR with multistability in at-most-bimolecular mass-action networks"

Task DR-049 | mode max | completed 2026-10-26T11:22:23.612Z | cost 15.625

# Referee report: "ACR with multistability in at-most-bimolecular mass-action networks"

## Summary of the audit

I found no FATAL error in any part I could check. Three points do need action:

- **The core dimension-two theorem is not verifiable from the submission.** The case e′₁ ≠ 0 is omitted. Everything else rests on it: Corollary 4.1, Theorem 4.3 (six complexes) and Theorem 5.1.
- **Table 1 contains a factual error** in the KNS column.
- **The framing of the species result is misleading.** The species bound is overturned by a decoupled union, as Remark 5.3 itself concedes.

The six-complex bound, the four-reactant-complex proposition, both examples and the decoupled remark all survive my recomputation. I recomputed by hand and did not run code; the authors' scripts were not available to me. I found no prior statement of the paper's three main claims (dimension two, three-species bistability with ACR, minimal complexes) in anything retrievable as of 26 Oct 2026. Absence from a search is not proof of absence.

## Numbered objections

**1. Theorem 3.1, case e′₁ ≠ 0 (omitted) — MAJOR (unverified).**
- I cannot check the main case analysis, and the statement that an earlier review of the same team audited it is not independent evidence.
- Lemma 3.3 gives det Df|_S(p)·det Df|_S(p′) of sign −sign(ℓ(p)ℓ(p′)). So the lemma alone settles only the case ℓ(p)ℓ(p′) > 0.
- A proof must therefore exclude the sign pattern ℓ(p)ℓ(p′) < 0 with both points exponentially stable, using only (F1) and (F2). This also requires a trace or sign argument at p and p′.
- My hand checks of the e′₁ = 0 case, and of one explicit three-species family, are consistent with the theorem. They do not prove it.
- The paper should include the case analysis, or at least state precisely the inequality that closes the sign pattern ℓ(p)ℓ(p′) < 0.
- The theorem is consistent with KNS's remark that their minimal networks have two positive steady states and are not multistable [[1]](https://arxiv.org/pdf/2307.04186).

**2. Lemmas 3.2 and 3.3 — NOT AN ISSUE.**
- I re-derived both.
- Lemma 3.2: the implicit-function step, the gcd/dimension argument, the deg D = 1 contradiction (D vanishing at p ≠ p′ ∈ L forces h₁ = h₂ = 0 on L, so p is not isolated), and the final non-vanishing of λ·f.
- Lemma 3.3: the determinant formula det = −ℓ·DG′·v. On H one has DG = ℓ e₁ᵀ, and v has first coordinate zero.
- The theorem's conclusion (a real positive eigenvalue at p or p′) also excludes two Lyapunov-stable nondegenerate states, as claimed.

**3. Theorem 4.3, kinetic-subspace step (t ≤ 1) — NOT AN ISSUE.**
- With m = 5, s = 3, l = 1, δ = 1, I get dim(ker Y ∩ im A_κ) = m − t − s ≥ 1 at a nondegenerate p. This uses rank(Y A_κ) = s, which follows from Df(p)|_S = Y A_κ DΨ(p) with image in S.
- A_κΨ(p) is nonzero when the network is not weakly reversible. A positive kernel vector would make every complex terminal, and (F3) says kernel vectors are supported on terminal classes. Hence t ≤ 1.
- If the network is weakly reversible, t = l = 1.
- Minor: (F3) is taken from Feinberg 2019, whose text I did not have. The paper should say where the nonvanishing claim uses non-weak-reversibility.
- The enumeration m = 5 ⇒ s = 3, l = 1, δ = 1 is correct, given s ≥ 3, l ≥ 1 and δ ≥ 1.
- Deficiency zero is excluded legitimately. Deficiency-zero systems that are not weakly reversible have no positive steady state [[2]](https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=osu1307122057&disposition=inline)[[3]](https://arxiv.org/abs/2108.05546), and weakly reversible ones have a unique one per class [[1]](https://arxiv.org/pdf/2307.04186).

**4. Application of Feinberg's Deficiency One Theorem — NOT AN ISSUE.**
- Hypotheses of Theorem 6.2.1: each linkage class has one terminal strong linkage class; each δ_θ ≤ 1; Σδ_θ = δ.
- Conclusion: "no matter what (positive) values the rate constants take … no more than one steady state within a positive stoichiometric compatibility class." Weak reversibility is used only for the "precisely one" clause [[4]](https://web.mit.edu/~jadbabai/www/ESE680/Fei87a.pdf).
- Corollary 6.2.2: with one linkage class, multiple steady states require deficiency > 1 or more than one terminal strong linkage class [[4]](https://web.mit.edu/~jadbabai/www/ESE680/Fei87a.pdf). This matches the paper's use.
- Definition: in that paper a steady state is any composition in the closed orthant and a positive steady state one in the open orthant [[4]](https://web.mit.edu/~jadbabai/www/ESE680/Fei87a.pdf). So the conclusion covers boundary points too, which is stronger than needed.
- Existence of a positive steady state is assumed only in later formulations [[5]](https://arxiv.org/abs/1602.08396)[[6]](https://arxiv.org/abs/2303.09445)[[7]](https://pubmed.ncbi.nlm.nih.gov/PMC13230314). The paper's use is valid either way, since existence is given.
- The paper is right not to use KNS Lemma 2.5, which is stated only for weakly reversible networks [[1]](https://arxiv.org/pdf/2307.04186).
- Not weakly reversible networks that satisfy the Deficiency One hypotheses are nondegenerate whenever they are consistent [[8]](https://arxiv.org/abs/2412.17798). This is not needed here.

**5. Proposition 4.4: toric curve, ACR forcing b_i = 0, exhaustive enumeration — NOT AN ISSUE (MINOR: replace the enumeration).**
- Counts: 1 + 4 + 6 + 4 = 15 at-most-bimolecular complexes in four species, and C(15,4) = 1365.
- Rank M = 3 follows from isolation of nondegenerate steady states in a three-dimensional class, and ACR forces b_i = 0.
- A short hand proof of "at most three distinct coordinates of b" is available and I verified it. Write b·y = κ for all four reactant complexes.
  - **κ = 0.** The only complexes of value 0 are 0, X_i, 2X_i, plus at most one X_a + X_b with b_a = −b_b. The first three are collinear, so rank M ≤ 2.
  - **κ ≠ 0.** Partners are unique when the values are distinct. This allows at most one 2X_j, at most one monomer X_j with b_j = κ, and the remaining pairs. The total is at most 3 < 4.
- This replaces the 922-set computer replay and removes the dependence on code.

**6. "At most two real zeros" for φ(t) − T — NOT AN ISSUE (MINOR).**
- The distinct exponents are the distinct values of b. Since b_i = 0, the constant −T merges with exponent 0, so there are at most three.
- The Descartes-type bound for exponential sums is standard but uncited in the paper. Add a citation.

**7. Determinant identity det Df|_S = μc³φ′(t)/(x₁x₂x₃x₄) — NOT AN ISSUE.**
- I re-derived it. Facts used: Df = c·K·diag(1/x), Kb = 0, wᵀK = 0; det(A + wwᵀ) = |w|²·det A|_S for A with image in S; adj K = μ b wᵀ with μ ≠ 0 constant; and the matrix determinant lemma.
- Two consecutive simple zeros give opposite signs of φ′, so one det is positive. In dimension 3 a positive determinant forces a positive real eigenvalue, which contradicts exponential stability.

**8. n = 3 dispatch and the KNS citations — MINOR.**
- The citation should be to part (4): a full-dimensional network needs at least n + 2 reactant complexes [[1]](https://arxiv.org/pdf/2307.04186)[[9]](https://arxiv.org/abs/2307.04186).
- A more elementary route exists. KNS Proposition 3.1(3) says a full-dimensional network with exactly n + 1 reactant complexes and a nondegenerate steady state is not multistationary. Proposition 3.5(2) excludes j ≤ n reactant complexes. Neither needs ACR [[1]](https://arxiv.org/pdf/2307.04186).
- So "even without stability" in the Table 1 caption is true, but the ACR-free reason is Proposition 3.1(3).
- KNS Theorem 5.5 is stated for n ≥ 3 and k ≥ 1 conservation laws, giving at least n − k + 1 reactant complexes [[1]](https://arxiv.org/pdf/2307.04186). The paper's parenthetical "for networks with a conservation law" is acceptable, but the proof of Corollary 4.2 is self-contained, so the citation is not load-bearing.

**9. Example 5.1 (six reactions) — NOT AN ISSUE (recomputed).**
- Reduction: ḃ = 2b(a − 1), so a = 1. At a = 1, b = (c² − 13c + 60)/2, and ċ = −c³ + 12c² − 47c + 60 = −(c − 3)(c − 4)(c − 5).
- Steady states: (1,15,3), (1,12,4), (1,10,5).
- Characteristic polynomials (I recomputed each trace, principal-minor sum and determinant):
  - λ³ + 92λ² + 1920λ + 120;
  - λ³ + 95λ² + 1752λ − 48;
  - λ³ + 102λ² + 1680λ + 80.
- Routh–Hurwitz holds for the outer two: 92·1920 > 120 and 102·1680 > 80. The middle one has constant term −48, so it has a positive real eigenvalue.
- Counts: six reactions; reactant complexes A+B, B, 0, 2C, A+C, B+C; seven complexes (adding 2B); dimension 3.

**10. Example 5.2 (six complexes) — NOT AN ISSUE (recomputed).**
- ȧ = c(1 − a); ḃ = 11b − b² + 6c − 6bc; ċ = 6a − bc. At a = 1, c = 6/b and b·ḃ = −(b³ − 11b² + 36b − 36) = −(b − 2)(b − 3)(b − 6).
- Steady states: (1,2,3), (1,3,2), (1,6,1).
- The Jacobian's first row is (−c, 0, 1 − a), so the characteristic polynomial is (λ + c) times that of the (b,c) block. Results:
  - (λ + 3)(λ² + 13λ + 4) = λ³ + 16λ² + 43λ + 12;
  - (λ + 2)(λ² + 10λ − 3) = λ³ + 12λ² + 17λ − 6;
  - (λ + 1)²(λ + 12).
- Counts: eight reactions; six complexes, all reactant complexes; one linkage class; deficiency 6 − 1 − 3 = 2; dimension 3. The network is not weakly reversible, with one terminal strong linkage class {B, 2B}. This is consistent with Theorem 4.3: δ = 2, so the Deficiency One Theorem does not apply.

**11. Remark 5.3 (ε = 6/49) — NOT AN ISSUE arithmetically; framing is MAJOR for presentation.**
- Recomputed:
  - Subtracting the two equations gives (x − y)(1 − x − y) = 0.
  - x = y gives x = 3/7; x + y = 1 gives x = 6/7 or 1/7.
  - At (6/7, 1/7) the Jacobian has trace −2 and determinant 25/49. At (3/7, 3/7) the determinant is −11/49.
- The species bound fails by disjoint union with 0 ⇌ Z. This is trivially true and does not depend on the new examples.
- It should be stated in the abstract and introduction, and the "species: false" cell of Table 1 should say "trivially". The sentence "the only published network … has eight species" should read "non-decoupled".
- KNS's conjecture lists species among the bounds [[1]](https://arxiv.org/pdf/2307.04186), so the refutation is legitimate. It is not an insight about coupled networks.

**12. Table 1, KNS column, row "(three species)" = 5 — MAJOR (factual error).**
- KNS's tight network {A+B → 2C → 2B, C → A} has three species and three reactant complexes [[1]](https://arxiv.org/pdf/2307.04186)[[9]](https://arxiv.org/abs/2307.04186). The value for three-species networks is therefore 3, not 5.
- The n + 2 = 5 bound applies only to full-dimensional networks [[1]](https://arxiv.org/pdf/2307.04186). That belongs in the multistability column and in the caption, not in the KNS column.

**13. Theorem 5.1 and the conjecture column — NOT AN ISSUE.**
- The three minima and the two ranges are exactly what is proved.
- Example 5.2 attains dimension 3, six complexes and three species simultaneously.
- The reactant-complex ranges follow from m_R ≥ dim S + 1, Corollary 4.1, Proposition 4.4 and the examples.
- The quote of the KNS conjecture is verbatim [[1]](https://arxiv.org/pdf/2307.04186). Dimension (3 > 2), complexes (6 > 5) and reactant complexes (at least 4 > 3) are strictly larger lower bounds. Species (3 = 3) is not.
- Attribution to KNS Theorem 1.2(4) and Theorem 5.5 is correct, with the refinements in objection 8.
- Caution: "true" for reactant complexes means only that the proved lower bound exceeds KNS's. The exact minimum is open between 4 and 6.

**14. Scope paragraph and reproducibility — MINOR.**
- "ACR for every rate vector in which the two motif rates have the stated ratio" is muddled. In Example 5.1, ḃ = k₁ab − k₂b forces a = k₂/k₁ at every positive steady state. In Example 5.2, ȧ = c(k₁ − k₂a) forces a = k₁/k₂. So ACR holds for every rate vector admitting a positive steady state, with that value.
- The two randomized searches reported (five reactant complexes; six-complex motif family) are not evidence of absence and should be labelled as such.
- The scripts cited could not be audited by me.

**15. Citation hygiene — MINOR.**
- Jiao–Tang–Zeng (arXiv:2406.11586, v1 17 Jun 2024, v2 19 Dec 2024) is published as J. Math. Biol. 91(6):82 (2025) [[10]](https://arxiv.org/abs/2406.11586)[[11]](https://pubmed.ncbi.nlm.nih.gov/41254364/). Cite the published version.
- The Tang–Zhang paper is arXiv:2608.01116v1, submitted 2 Aug 2026 [[12]](https://arxiv.org/abs/2608.01116). The Feliu–Henriksson–Pascual-Escudero paper is arXiv:2412.17798, v1 Dec 2024, v2 Feb 2025, v3 14 May 2026, published as SIAM J. Appl. Algebra Geom. 10 (2026) 519–548 [[13]](https://arxiv.org/abs/2412.17798v2)[[14]](https://arxiv.org/html/2608.18509v1).
- KNS exists only as arXiv:2307.04186v1 (9 Jul 2023), Eur. J. Appl. Math. 35 (2024) 566–600 [[9]](https://arxiv.org/abs/2307.04186)[[15]](https://arxiv.org/abs/2307.04186v1). The HTML copy is stamped 24 Aug 2026 [[16]](https://arxiv.org/html/2307.04186); that is a rendering date, not a new version.
- arXiv:2409.06877 is Banaji–Feliu (v5, 19 Aug 2026; J. Math. Biol. 93:37, 2026), not Banaji–Boros–Hofbauer [[17]](https://arxiv.org/abs/2409.06877). The brief that framed this review mislabels it.

**16. The Chen–Tang remark on ACR (arXiv:2608.18509) — NOT AN ISSUE as a threat to the examples.**
- Chen–Tang write that, for full-dimensional networks, a rank criterion "[18, Theorem B]" shows that a necessary condition for ACR is that removing the species yields a degenerate network. They also cite "[29, Theorem 3.1]" for the conservation-law case [[14]](https://arxiv.org/html/2608.18509v1).
- FHP Theorem B concerns generic local ACR for a nondegenerate network. Its condition is rk((N diag(w)Mᵀ) with column i removed) < rk(N) for all w ∈ ker N [[8]](https://arxiv.org/abs/2412.17798). It says nothing about a degenerate reduced network.
- FHP note that full rank trivially implies generic local ACR [[8]](https://arxiv.org/abs/2412.17798). For rank N = n the criterion is therefore automatic.
- Si–Tang's criterion is Theorem 7, not "Theorem 3.1". It requires r < s, a conservation law, and a nondegenerate reduced network of the same dimension [[18]](https://arxiv.org/html/2604.14592v5). It does not apply to the paper's full-dimensional three-species examples.
- Do not read Chen–Tang as an objection to Examples 5.1–5.2.

## Priority section

**(a) Dimension-two ACR at-most-bimolecular systems cannot be multistable — no prior statement found.**
- KNS prove only dimension ≥ 2 for ACR with nondegenerate multistationarity [[1]](https://arxiv.org/pdf/2307.04186). They remark that their minimal networks are not multistable [[1]](https://arxiv.org/pdf/2307.04186).
- Jiao–Tang–Zeng prove that two-dimensional zero-one networks with ≤ 3 species admit no nondegenerate multistationarity. There is no ACR hypothesis and the class is zero-one [[10]](https://arxiv.org/abs/2406.11586).
- Chen–Tang (arXiv:2608.18509v1, 19 Aug 2026) classify degenerate two-dimensional zero-one networks. Their abstract says every ACR network contains a degenerate subnetwork [[19]](https://arxiv.org/abs/2608.18509)[[20]](https://arxiv.org/abs/2608.18509v1).
- Neither covers the paper's class (at-most-bimolecular, any n, ACR, multistable). Position the new theorem against JTZ Theorem 3.

**(b) A three-species at-most-bimolecular network with ACR and bistability — not found, apart from the disclosed decoupled union.**
- Joshi–Nguyen–Johnston (arXiv:2605.11389v1, 12 May 2026) show that (E,E,C2,C2) has two stable positive steady states and ACR in S₂ [[21]](https://arxiv.org/abs/2605.11389)[[22]](https://pith.science/paper/2605.11389).
  - The detailed model has eight species (s₀, s₁, s₂, e, c₁, c₂, c₃, c₄) [[21]](https://arxiv.org/abs/2605.11389).
  - The ACR value is k₂/k₃* [[21]](https://arxiv.org/abs/2605.11389).
  - Bistability is verified by eigenvalues at one explicit rate vector [[21]](https://arxiv.org/abs/2605.11389).
  - "First" is claimed only for the first systematic dynamical analysis of these four networks, not for ACR with bistability globally [[21]](https://arxiv.org/abs/2605.11389).
  - Judging by its Figure 1 reaction list [[23]](https://arxiv.org/html/2605.11389), its complexes appear at-most-bimolecular. The paper under review should say so, since this would make it an eight-species data point in the paper's own class.
- Tang–Zhang (arXiv:2608.01116v1) identify 373 (3,6,3) quadratic zero-one networks with two stable and one unstable positive steady state. They impose no ACR condition and do not report whether any has ACR [[12]](https://arxiv.org/abs/2608.01116).
  - Quadratic zero-one networks have at-most-bimolecular reactant complexes.
  - The paper under review does not state whether any of the 373 has ACR; their data are public [[12]](https://arxiv.org/abs/2608.01116). Check them before claiming priority for three species. The status is unestablished.
- Banaji–Boros–Hofbauer (arXiv:2406.13451) concern planar two-species networks. Their "simplest bistable bimolecular networks" have one positive and one origin equilibrium, with no ACR [[24]](https://arxiv.org/abs/2406.13451).
- Chen–Tang Example 3.8 gives ACR in a three-dimensional zero-one network with at most two positive steady states. This is multistationarity, not bistability [[19]](https://arxiv.org/abs/2608.18509).

**(c) Minimal complexes or reactant complexes for ACR with multistability — no determination found.**
- KNS leave the question as a conjecture [[1]](https://arxiv.org/pdf/2307.04186).
- The 2026 papers checked address zero-one degeneracy, bistability without ACR, or ACR-obstruction criteria. None addresses the conjecture [[12]](https://arxiv.org/abs/2608.01116)[[25]](https://arxiv.org/abs/2610.32739)[[18]](https://arxiv.org/html/2604.14592v5)[[14]](https://arxiv.org/html/2608.18509v1).
- Banaji–Feliu (arXiv:2409.06877v5) bound positive equilibria and say nothing about ACR [[17]](https://arxiv.org/abs/2409.06877).
- Peng, arXiv:2610.32739v1 (23 Oct 2026), classifies two-species networks with inflows and linear removal. 27 of 681 admit two positive hyperbolic attractors. There is no ACR, and the networks are open [[25]](https://arxiv.org/abs/2610.32739).

**Papers citing KNS.**
- Combinatorics of degeneracy in vertical systems (arXiv:2610.14803, 10 Oct 2026) cites KNS for ACR in vertically parametrized systems [[26]](https://arxiv.org/abs/2610.14803).
- Tang–Wang–Zhang (arXiv:2507.09272) lists KNS only among its references [[27]](https://pith.science/paper/2507.09272).
- None addresses ACR with multistability. I could not search the citation graph directly, so this is not proof of absence.

**Not found.** No Zenodo or GitHub record of the paper's results turned up. The one Zenodo item seen concerns Kaihnsa–Wang connectivity of multistationarity regions, not this topic [[28]](https://zenodo.org/records/22858244).

## Synthesis

The mathematics I could audit holds. That covers the complexes bound via the kinetic-subspace argument and Feinberg's theorem, the four-reactant-complex proposition, both examples and the decoupled remark. The one load-bearing gap is the omitted case e′₁ ≠ 0 of Theorem 3.1. The authors should include that proof, or the precise inequality closing the sign pattern ℓ(p)ℓ(p′) < 0, before the dimension and six-complex claims can be accepted. The paper should also:

- correct the KNS "(three species)" cell in Table 1;
- state the triviality of the species counterexample up front;
- replace the enumeration in Proposition 4.4 with the hand proof;
- check the Tang–Zhang and JNJ examples for ACR before claiming priority at three species.

The reactant-complex minimum remains open between 4 and 6, and between 5 and 6 for three species.

## Sources

[1] Absolute Concentration Robustness and Multistationarity in Reaction Networks: Conditions for Coexistence - https://arxiv.org/pdf/2307.04186
[2] UNIQUENESS OF EQUILIBRIA FOR COMPLEX CHEMICAL REACTION NETWORKS DISSERTATION - https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=osu1307122057&disposition=inline
[3] Independent, Incidence Independent and Weakly Reversible Decompositions of Chemical Reaction Networks - https://arxiv.org/abs/2108.05546
[4] PII: 0009-2509(87)80099-4 - https://web.mit.edu/~jadbabai/www/ESE680/Fei87a.pdf
[5] A Linear Programming Approach to Dynamical Equivalence, Linear Conjugacy, and the Deficiency One Theorem - https://arxiv.org/abs/1602.08396
[6] Weakly reversible deficiency one realizations of polynomial dynamical systems: an algorithmic perspective - https://arxiv.org/abs/2303.09445
[7] Decomposable and Essentially Univariate Mass-Action Systems: Extensions of the Deficiency One Theorem - https://pubmed.ncbi.nlm.nih.gov/PMC13230314
[8] The generic geometry of steady state varieties - https://arxiv.org/abs/2412.17798
[9] Absolute Concentration Robustness and Multistationarity in Reaction Networks: Conditions for Coexistence - https://arxiv.org/abs/2307.04186
[10] [2406.11586] Multistability of small zero-one reaction networks - https://arxiv.org/abs/2406.11586
[11] Multistability of small zero-one reaction networks - PubMed - https://pubmed.ncbi.nlm.nih.gov/41254364/
[12] The Ubiquity of Three Steady States: Minimal Multistable Zero-One Reaction Networks - https://arxiv.org/abs/2608.01116
[13] [2412.17798v2] The generic geometry of steady state varieties - https://arxiv.org/abs/2412.17798v2
[14] Characterization of Minimal Degenerate Zero-One Reaction Networks - https://arxiv.org/html/2608.18509v1
[15] [2307.04186v1] Absolute Concentration Robustness and Multistationarity in Reaction Networks: Conditions for Coexistence - https://arxiv.org/abs/2307.04186v1
[16] Absolute concentration robustness and multistationarity in reaction networks: Conditions for coexistence - https://arxiv.org/html/2307.04186
[17] [2409.06877] Positive equilibria in mass action networks: geometry and bounds - https://arxiv.org/abs/2409.06877
[18] Absolute Concentration Robustness of Non-Redundant Zero-One Networks with Conservation Laws - https://arxiv.org/html/2604.14592v5
[19] [2608.18509] Characterization of Minimal Degenerate Zero-One Reaction Networks - https://arxiv.org/abs/2608.18509
[20] [2608.18509v1] Characterization of Minimal Degenerate Zero-One Reaction Networks - https://arxiv.org/abs/2608.18509v1
[21] Bistability, Absolute Concentration Robustness, and Hysteresis in Dual-Site Futile Cycles with Bifunctional Enzymes - https://arxiv.org/abs/2605.11389
[22] Bistability, Absolute Concentration Robustness, and Hysteresis in Dual-Site Futile Cycles with Bifunctional Enzymes · Pith - https://pith.science/paper/2605.11389
[23] Bistability, Absolute Concentration Robustness, and Hysteresis in Dual-Site Futile Cycles with Bifunctional Enzymes - https://arxiv.org/html/2605.11389
[24] [2406.13451] Bifurcations in planar, quadratic mass-action networks with few reactions and low molecularity - https://arxiv.org/abs/2406.13451
[25] [2610.32739] Bistability with equal and independent removal in small bimolecular networks - https://arxiv.org/abs/2610.32739
[26] Combinatorics of degeneracy in vertical systems - https://arxiv.org/abs/2610.14803
[27] Degeneracy of Two-Dimensional Zero-One Reaction Networks with Up to Three Species · Pith - https://pith.science/paper/2507.09272
[28] Path connectedness of multistationarity in a two-layer phosphorylation cascade with a shared phosphatase | Zenodo - https://zenodo.org/records/22858244
