# Referee audit: ACR and multistability in at-most-bimolecular mass-action networks

Task DR-035 | mode max | completed 2026-10-26T09:41:32.198Z | cost 15.625

# Referee audit: ACR and multistability in at-most-bimolecular mass-action networks

## Executive summary

**Theorem A.** I found no failing step and no counterexample. Every step re-derives under my own check: the factorisation in Step 1, the determinant identity in Step 2, the constant-sign claim in Step 4, and the concavity argument in Steps 5–8. The problems are presentational. The letters P and p are each used for two objects, E′ in Step 8 is undefined, and several analytic facts are used silently.

The proof actually gives more than is stated. For a dimension-two ACR system, every class with two nondegenerate positive steady states contains exactly these two, and they have determinants of opposite sign. In the case e′₁ ≠ 0, one of the two is a saddle with a positive real eigenvalue. In the case e′₁ = 0 the same conclusion holds, because either a positive eigenvalue appears or the determinants again have opposite signs.

**Corollary B.** The argument is valid, but its stated bounds are not the strongest available. The "≥ 4 reactant complexes" bound is already Kaihnsa–Nguyen–Shiu (KNS) Theorem 5.5 once Theorem A gives dimension ≥ 3. For three species it is superseded by KNS Theorem 1.2(4), which requires ≥ 5 reactant complexes.

**Proposition C.** My recomputation reproduces the steady states, the characteristic polynomials and the network counts, so the example stands. It leaves the species and dimension bounds attained, but not the reactant-complex or complex bounds.

**The KNS conjecture, as it bears on these results.**
- The conjecture says all four bounds are strictly larger. Proposition C attains three species, which equals KNS's species bound, so the species part is false. The dimension part is consistent: dimension 3 > 2.
- The conjecture also says the lower bound on reactant complexes is strictly larger than KNS's bound of 3. Corollary B gives at least 4 in general and at least 5 for three species, consistent with this.
- The conjecture also says the lower bound on all complexes is strictly larger than KNS's bound of 5. Corollary B gives at least 6, consistent with this.

**Prior art.** No retrieved source states Theorem A, Corollary B, or a three-species ACR-plus-bistability example. This is absence in what was retrieved, not proof of absence.

## 1. Theorem A: step-by-step audit

### Step 0
Step 0 is sound. It is essentially KNS's own argument for two species. There, if X₁ is catalyst-only, classes are defined by x₁ = T, so two positive steady states in one class would have the form (T,y) and (T,z), contradicting ACR [[1]](https://arxiv.org/html/2307.04186). Here the implicit-function version shows that the level of x₁ moves along the manifold of steady states.

### Step 1 (global factor)
- **Dimension count.** The count is right. With dim S = 2, the map (g₁, g₂, Wx) has invertible derivative at p exactly when p is nondegenerate. So {g₁ = g₂ = 0} is locally an (n−2)-manifold, and ACR places it inside H.
- **Coprime case.** Coprime polynomials in n−1 variables cut out a set of dimension ≤ n−3, so M_p ⊂ V(h₁,h₂) forces a common factor.
- **gcd of degree 1.** The argument is correct. The cofactor set has dimension ≤ n−3, so M_p and M_p′ lie in V(D). Both p and p′ lie on the line L = P ∩ H. L is a line because e₁ ∉ S^⊥ (from Step 0), so P ⊄ H. An affine D vanishing at two points of L vanishes on L, so every point of L is a steady state, contradicting isolation.
- **gcd of degree 2.** The cofactors are constants, so G = b g₁ − a g₂ vanishes on H and equals (x₁−α) l with l affine.
- **Case h₁ ≡ 0 or h₂ ≡ 0.** This is covered by taking G = g₁ or g₂. If both vanish, every ∇gᵢ is a multiple of e₁ᵀ and rank Df ≤ 1.
- **Unwritten facts.** Two facts should be stated. M_p can be shrunk to be connected. A closed analytic subset of a connected manifold that has full dimension there is the whole manifold.

### Step 2 (determinant identity)
I re-derived it. Df·e = (l e₁)e + (∇G′·e)e′ and Df·e′ = (l e′₁)e + (∇G′·e′)e′. Hence det = −l·∇G′·v. Since v₁ = 0, v is parallel to L, and on H we have f = G′e′, so the roots of γ are exactly the steady states in the class. Nondegeneracy makes p and p′ simple roots, and γ has degree exactly 2. Consecutive simple roots have opposite derivative signs, giving sign(det(p)·det(p′)) = −sign(l(p)·l(p′)). As a by-product, the class has exactly two positive steady states.

### Step 3 (case e′₁ = 0)
Correct. The matrix is triangular with eigenvalue l·e₁. Here e₁ ≠ 0, because e and e′ are independent and e₁ ∉ S^⊥.

### Step 4 (constant sign of f₁ on Π₊ \ H)
This is the step the question flags, and it holds. Write f = (x₁−α) l E + f₁ w, where E and w are independent. A positive point off H is a steady state iff l = 0 and f₁ = 0, so ACR forces f₁ ≠ 0 on Π₊ \ H. That set is two convex pieces, hence connected, so f₁ has constant sign on each. Both pieces touch q, because Π ∋ q, Π ≠ H and Π is a hyperplane, so x₁ is nonconstant on Π. Also f₁(q) ≠ 0 because q is not a root of γ. The two pieces therefore share the sign σ = sign f₁(q).

The edge cases are exhausted:
- l depending only on x₁ would be constant on L, so it has no sign change.
- Π parallel to H is impossible because q ∈ Π ∩ H.
- q on the boundary is impossible because q lies strictly between p and p′ in the convex set L₊.

### Step 5 ("at most bimolecular" is used correctly)
- Negative monomials of f₁ are divisible by x₁ (KNS Lemma 2.3 [[1]](https://arxiv.org/html/2307.04186)), so P(x′) = f₁(0, x′) has nonnegative coefficients.
- The only x₁² monomial in f₁ comes from reactions 2X₁ → y′, with coefficient Σk(y′₁−2). This is ≤ 0 only because products have molecularity ≤ 2. With trimolecular products the sign could be positive and concavity would fail.
- Concavity plus f₁(0) ≥ 0 gives persistence: if f₁(t₀) < 0 for some t₀ > 0, then f₁(t) < 0 for all t ≥ t₀.

KNS Lemma 3.11 uses the same three ingredients, namely degree ≤ 2, nonpositive x_i² coefficient and nonnegative constant term, to prove at most one sign change [[1]](https://arxiv.org/html/2307.04186). That lemma is stated for fixed positive values of the other species. Steps 6 and 8 also need P at boundary points, which uses coefficient nonnegativity instead. Cite KNS Lemma 3.11 for the polynomial constraints and state sign persistence separately.

### Steps 6–8 (case analysis)
Steps 6–8 are valid and exhaustive: σ = −1 with any b₁, σ = +1 with b₁ ≠ 0, and σ = +1 with b₁ = 0.
- **Step 6, case b₁ = 0.** It is absorbed. If Π avoids {x₁ = 0, x′ > 0}, then l(0,·) has constant sign and B > 0, so a sign change of l on L forces b₁ < 0.
- **Step 7.** The point (φ(z′), z′) has φ > α > 0, so it lies in Π₊, and concavity propagates upward from α.
- **Step 8.** L₊ is bounded because Q has nonnegative coefficients and Q(v′) < 0, so v′ has entries of both signs. At the endpoints f₁ < 0 strictly, and P ≥ 0 on the closed orthant, so M < 0 there. Affineness then gives M(q′) < 0, contradicting M(q′) ≥ 0.

### What to fix in the write-up
- Use different letters for the class, the polynomial P(x′) and the points p, p′.
- Define E′ in Step 8; it should be v′, the x′-projection of v.
- State the analytic facts listed under Step 1.
- Note that only nondegeneracy of p and p′ is needed. Exponentially stable states are automatically nondegenerate.
- Sharpen the theorem to the conclusion that one of the two states has det < 0.
- Stability needs no change: the eigenvalues of the full Jacobian are those of Df|_S together with zeros, because Df maps into S.

I tested the sharpened conclusion on KNS Example 4.10 as a consistency check, not a proof. All κ = 1 gives C = 1/2 and AB = 1/2. The reduced determinant is B − A, and the two steady states have (A,B) swapped, so one is a saddle and one a stable node. This agrees with KNS, who note only that their minimal networks are not multistable and give no eigenvalues [[1]](https://arxiv.org/html/2307.04186).

## 2. Corollary B

| Claim | Status |
|---|---|
| dim ≥ 3 | Follows from Theorem A plus KNS's dim ≥ 2 [[1]](https://arxiv.org/html/2307.04186) |
| ≥ 4 reactant complexes | Valid. Since Df = N·DΨ and NΨ(p) = 0, we get dim S ≤ (reactant complexes) − 1. This equals KNS Theorem 5.5's n−k+1 = dim+1 [[1]](https://arxiv.org/html/2307.04186) |
| n = 3, dim 3 (full-dimensional) | KNS Theorem 1.2(4) gives ≥ n+2 = 5 reactant complexes [[1]](https://arxiv.org/html/2307.04186), stronger than 4 |
| ≥ 6 complexes | Sound |

For n = 3 the full-dimensional bound is also stated, without ACR, for general (n,m,n) networks with multiple positive nondegenerate equilibria (arXiv:2409.06877 [[2]](https://arxiv.org/abs/2409.06877)). Corollary B should therefore be split by species count: ≥ 5 reactant complexes for n = 3, and ≥ 4 for n ≥ 4 with dim 3.

**Complexes.**
- **Deficiency-zero exclusion.** Unconditionally valid. KNS Lemma 2.4 says deficiency-zero networks are not multistationary, and its first sentence needs no weak reversibility [[1]](https://arxiv.org/html/2307.04186).
- **Counting.** δ ≥ 1 gives m ≥ s + l + 1 ≥ 5, and m = 5 forces s = 3, l = 1, δ = 1.
- **Kinetic-subspace step.** I re-derived it. rank(Y·A_k) = s gives dim(ker Y ∩ im A_k) = m − t − s = δ + l − t, so t ≤ δ + l − 1 = 1.
- **Deficiency One Theorem without weak reversibility.** Feinberg's 1987 Theorem 6.2.1 requires only one terminal strong linkage class per linkage class, δ_θ ≤ 1 and Σδ_θ = δ. It gives at most one steady state per positive class for all positive rate constants [[3]](https://web.mit.edu/~jadbabai/www/ESE680/Fei87a.pdf). Feinberg states that it "replaces the weak reversibility condition by the far milder condition" of at most one terminal strong linkage class per linkage class [[3]](https://web.mit.edu/~jadbabai/www/ESE680/Fei87a.pdf). A restatement attributed to the 1995 paper agrees [[4]](https://reaction-networks.net/wiki/Deficiency_theory); a 2026 paper summarises the theorem as assuming existence of a positive equilibrium, with weak reversibility ensuring existence [[5]](https://pubmed.ncbi.nlm.nih.gov/PMC13230314). KNS's own Lemma 2.5 is stated only for weakly reversible networks [[1]](https://arxiv.org/html/2307.04186), so Corollary B should cite Feinberg directly.
- **Gaps.** The 1995 proof was not read directly. The argument does not show that 6 complexes, or 4 reactant complexes, is attainable, and KNS(4) already excludes the latter for n = 3.

## 3. Proposition C and the status of the conjecture

**Verification.** I recomputed the following by hand, so it is not from a published source.
- The rate equations are ẋ_B = 2x_B(x_A − 1), ẋ_A = −2AB + 60 + C² − 13AC, and ẋ_C = 60 − C² + 13AC − 2BC.
- At A = 1, B = (60 + C² − 13C)/2 and the C-equation reduces to −(C−3)(C−4)(C−5), giving (1,15,3), (1,12,4), (1,10,5).
- The traces are −92, −95 and −102, and the determinants are −120, 48 and −80. The characteristic polynomials match those stated.
- Routh–Hurwitz holds at the outer two states (92·1920 > 120 and 102·1680 > 80). The middle one has negative constant term, so it is a saddle.
- The network has 6 reactions, 7 complexes and 6 reactant complexes, and its reaction vectors span ℝ³.

**What it settles.**
- Three species is attained, and so is dimension 3.
- The network is not tight for Corollary B: 6 reactant complexes exceeds 5, and 7 complexes exceeds 6.
- Whether 5 reactant complexes or 6 complexes is achievable for three species is unestablished.

**The "trivial route" is sound, but the reasoning above it needs repair.** Banaji–Boros–Hofbauer Lemma 27 covers only the 30 bimolecular (2,4,2) networks; for the 10 with an orange bullet, one stable state is the origin [[6]](https://arxiv.org/abs/2406.13451)[[7]](https://arxiv.org/pdf/2406.13451). It says nothing about planar networks with five or more reactions, and the authors themselves point to (2,5,2) networks as a route to two stable positive equilibria [[8]](https://pubmed.ncbi.nlm.nih.gov/PMC11466909). A direct two-species example is the following, recomputed here and not taken from a source. Take 0→X and 0→Y with rate ε, X→2X, 2X→X, Y→2Y and 2Y→Y with rate 1, and X+Y→Y and X+Y→X with rate 2. Then ẋ = ε + x − x² − 2xy and ẏ = ε + y − y² − 2xy. At ε = 0 the points (1,0) and (0,1) have eigenvalues −1, −1. For small ε > 0 they persist as exponentially stable positive steady states, for instance y ≈ ε near (1,0). This network has six reactant complexes, consistent with the planar requirement of at least four [[6]](https://arxiv.org/abs/2406.13451). Adding a disjoint 0 ⇌ C block gives ACR in C and keeps both stable states, because the dynamics decouple. Treat this as an unpublished verification.

**Conjecture status.** KNS Section 6 conjectures that all four bounds are strictly larger [[1]](https://arxiv.org/html/2307.04186); the published version is word-for-word the same [[9]](https://www.cambridge.org/core/journals/european-journal-of-applied-mathematics/article/absolute-concentration-robustness-and-multistationarity-in-reaction-networks-conditions-for-coexistence/BEABF13EA90E50ED45F64650BDEAC003). The species part is refuted by Proposition C. The dimension, reactant-complex and complex parts are consistent with Theorem A and Corollary B, not refuted. The tight KNS example matches the one in the problem statement (Example 4.10) [[9]](https://www.cambridge.org/core/journals/european-journal-of-applied-mathematics/article/absolute-concentration-robustness-and-multistationarity-in-reaction-networks-conditions-for-coexistence/BEABF13EA90E50ED45F64650BDEAC003).

## 4. Counterexample search

- **Dimension-two ACR networks with two stable states.** None found. The only explicit dimension-two ACR plus nondegenerate-multistationarity example in the sources is KNS Example 4.10, and KNS call such minimal networks not multistable [[1]](https://arxiv.org/html/2307.04186).
- **Planar analogues without ACR.** For the 30 bimolecular (2,4,2) networks that admit a fold bifurcation, whenever there are two positive equilibria one is a saddle and the other linearly stable [[6]](https://arxiv.org/abs/2406.13451). This is the same pattern as Theorem A, but without ACR.
- **Five-complex networks.** The argument in Corollary B excludes them: m = 5 forces s = 3, l = 1, δ = 1, and the Deficiency One Theorem then bars multistationarity.
- **Joshi–Nguyen–Johnston (arXiv:2605.11389) tests nothing here.** The (E,E,C2,C2) network has ACR in S₂ and, for chosen rate constants, two stable positive steady states [[10]](https://arxiv.org/abs/2605.11389)[[11]](https://arxiv.org/html/2605.11389). It has 8 species (s₀,s₁,s₂,e,c₁–c₄) [[11]](https://arxiv.org/html/2605.11389) and 2 conservation laws [[11]](https://arxiv.org/html/2605.11389), so dimension 6. The paper's ACR definition requires ACR for every choice of rate constants [[11]](https://arxiv.org/html/2605.11389), stronger than the per-system definition used here. The printed mass-action terms are products of at most two species, so it appears at most bimolecular, though the full reaction list was not inspected.

## 5. Prior art (2015 to October 2026)

| Source | What it gives | Relation |
|---|---|---|
| KNS, arXiv:2307.04186, EJAM 35(4):566–600 | Theorem 1.2 [[1]](https://arxiv.org/html/2307.04186), Theorem 5.5 [[1]](https://arxiv.org/html/2307.04186), conjecture [[1]](https://arxiv.org/html/2307.04186) | Source of the problem; proves only the multistationarity bounds |
| Jiao–Tang–Zeng, arXiv:2406.11586 | Zero-one networks: two-dimensional with ≤ 3 species gives at most one stable positive state or only degenerate ones [[12]](https://arxiv.org/abs/2406.11586); smallest multistable zero-one networks are 3 species, 6 reactions, dim 3 [[12]](https://arxiv.org/abs/2406.11586); cites KNS only as background [[12]](https://arxiv.org/abs/2406.11586) | Consistent with Theorem A for zero-one networks; no ACR |
| Tang–Zhang, arXiv:2608.01116 | Consecutive determinants alternate in sign for (3,m,3) quadratic zero-one networks [[13]](https://arxiv.org/abs/2608.01116); 373 bistable (3,6,3) networks [[13]](https://arxiv.org/abs/2608.01116) | Dimension-three analogue of the sign result; no ACR; Proposition C has coefficient-2 complexes, so it lies outside the zero-one class [[13]](https://arxiv.org/abs/2608.01116) |
| Joshi–Nguyen–Johnston, arXiv:2605.11389 | Concrete ACR plus bistability, dimension 6 | Prior art for the phenomenon only |
| Banaji–Boros–Hofbauer, arXiv:2406.13451 | Planar bimolecular (2,4,2) networks [[6]](https://arxiv.org/abs/2406.13451) | No ACR |
| arXiv:2409.06877 | n+2 distinct sources needed for multiple nondegenerate equilibria [[2]](https://arxiv.org/abs/2409.06877) | Overlaps KNS(4) without ACR |
| arXiv:2608.18509 | A 3-dimensional zero-one ACR network with at most two positive steady states per class [[14]](https://arxiv.org/abs/2608.18509) | Not at most bimolecular (it contains X₁+X₂+Z reactants [[14]](https://arxiv.org/abs/2608.18509)); stability not addressed |
| Joshi–Kaihnsa–Nguyen–Shiu, arXiv:2301.10337 | ACR and multistationarity together are highly atypical in random reversible networks [[15]](https://arxiv.org/html/2301.10337) | Background |
| arXiv:2604.14592; arXiv:2507.09272 | ACR generic existence and degeneracy for zero-one networks [[16]](https://arxiv.org/abs/2604.14592)[[17]](https://arxiv.org/html/2507.09272) | No multistability |

Tang–Xu (arXiv:2008.03846) show multistable networks need at least three positive steady states [[18]](https://arxiv.org/abs/2008.03846), which supports the structure of Theorem A but is not a prior statement of it. Wilhelm's "smallest bistable system" [[19]](https://pubmed.ncbi.nlm.nih.gov/19737387) is two-species, and its stable states are not both positive in the sense needed here [[7]](https://arxiv.org/pdf/2406.13451).

## 6. Synthesis and open points

1. **Theorem A should be presented as proved, in the strengthened form** (exactly two positive steady states per class, with determinants of opposite sign), after the notation and analytic-fact fixes.
2. **Corollary B should be restated** with the n = 3 versus n ≥ 4 split and credit to KNS Theorem 5.5 and Theorem 1.2(4). The new content is dimension ≥ 3 (from Theorem A) and complexes ≥ 6 (from Feinberg plus a kinetic-subspace argument).
3. **The KNS conjecture** is refuted for species and supported, at least by lower bounds, for the other three bounds.
4. **Unestablished:**
   - whether a three-species ACR plus multistable network exists with 5 reactant complexes or with 6 complexes;
   - whether any of Tang–Zhang's 373 zero-one networks has ACR;
   - whether any post-2024 paper proves Theorem A or Corollary B, since the search was not exhaustive;
   - Feinberg 1995, which was not read directly.

## Sources

[1] Absolute concentration robustness and multistationarity in reaction networks: Conditions for coexistence - https://arxiv.org/html/2307.04186
[2] Some bounds on positive equilibria in mass action networks - https://arxiv.org/abs/2409.06877
[3] PII: 0009-2509(87)80099-4 - https://web.mit.edu/~jadbabai/www/ESE680/Fei87a.pdf
[4] Deficiency theory - Mathematics of Reaction Networks - https://reaction-networks.net/wiki/Deficiency_theory
[5] Decomposable and Essentially Univariate Mass-Action Systems: Extensions of the Deficiency One Theorem - https://pubmed.ncbi.nlm.nih.gov/PMC13230314
[6] Bifurcations in planar, quadratic mass-action networks with few reactions and low molecularity - https://arxiv.org/abs/2406.13451
[7] Bifurcations in planar, quadratic mass-action networks with few reactions and low molecularity - https://arxiv.org/pdf/2406.13451
[8] Bifurcations in planar, quadratic mass-action networks with few reactions and low molecularity - https://pubmed.ncbi.nlm.nih.gov/PMC11466909
[9] Absolute concentration robustness and multistationarity in reaction networks: Conditions for coexistence | European Journal of Applied Mathematics | Cambridge Core - https://www.cambridge.org/core/journals/european-journal-of-applied-mathematics/article/absolute-concentration-robustness-and-multistationarity-in-reaction-networks-conditions-for-coexistence/BEABF13EA90E50ED45F64650BDEAC003
[10] Bistability, Absolute Concentration Robustness, and Hysteresis in Dual-Site Futile Cycles with Bifunctional Enzymes - https://arxiv.org/abs/2605.11389
[11] Bistability, Absolute Concentration Robustness, and Hysteresis in Dual-Site Futile Cycles with Bifunctional Enzymes - https://arxiv.org/html/2605.11389
[12] Multistability of Small Zero-One Reaction Networks - https://arxiv.org/abs/2406.11586
[13] The Ubiquity of Three Steady States: Minimal Multistable Zero-One Reaction Networks - https://arxiv.org/abs/2608.01116
[14] Characterization of Minimal Degenerate Zero-One Reaction Networks - https://arxiv.org/abs/2608.18509
[15] Prevalence of multistationarity and absolute concentration robustness in reaction networks - https://arxiv.org/html/2301.10337
[16] Absolute Concentration Robustness of Non-Redundant Zero-One Networks with Conservation Laws - https://arxiv.org/abs/2604.14592
[17] Degeneracy of Zero-one Reaction Networks - https://arxiv.org/html/2507.09272
[18] Multistability of Small Reaction Networks - https://arxiv.org/abs/2008.03846
[19] The smallest chemical reaction system with bistability - https://pubmed.ncbi.nlm.nih.gov/19737387
