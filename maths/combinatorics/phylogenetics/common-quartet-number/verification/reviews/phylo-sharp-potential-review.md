# Audit of the exact sharp constant c = (7−√13)/18 for the common-quartet potential step

Task DR-017 | mode max | completed 2026-10-26T14:12:07.854Z | cost 15.725

# Audit of the exact sharp constant c = (7−√13)/18 for the common-quartet potential step

## Executive summary

I found no error in the lemma, in its sharpness example, or in the derived bound h(k) ≤ ⌊3β^(k−1)⌋+1 with β = (1+√13)/2. The inequality, with c = t² = (7−√13)/18 and t = (√13−1)/6, holds for all real inputs in the stated domain. The sharpness example gives ratio exactly c, so c is the best constant for the real-variable inequality.

Status of the evidence:

- **Executed:** exact symbolic identities (sympy), a grid minimisation, an integer scan, and the threshold table. These corroborate the algebra and the arithmetic. They do not prove the lemma.
- **Reasoned:** the case-by-case proof of the lemma, the balanced-edge lemma, the cross-pairing, the iteration, integrality and k=1.
- **Not done:** a formal (Lean) check, and an end-to-end tree simulation for k≥3. The research notes mention a partial simulation, but no output from it is on record, so I treat it as unverified.

The audit also found wording gaps in the stated reduction that should be fixed before the result is integrated:

1. The weighted balanced edge must use weights equal to the normalised indicator of the larger set Y.
2. The pair must be re-ordered so that Y is the larger set at every step.
3. "Attained" and "sharp" hold only over the reals.

The bound is not an improvement over the published small-k values. It improves only on the 4/√3-based version, and only for some k (table below).

## 1. What was executed and what was reasoned

| Item | Method | Result |
|---|---|---|
| t, c identities: c = (7−√13)/18, 3t²+t = 1, c = (1−t)/3 | sympy, exact | residuals 0 [[1]] |
| β = 1/t, β² = β+3, 1/β² = c | sympy, exact | residuals 0 [[1]] |
| Sharpness: Ψ(t,4/3) − 2c and Ψ(1−t,2/3) − 2c | sympy, exact | residuals 0; floating point gives 0.37716096939289 for both outputs [[1]] |
| c − 3/16 and β − 4/√3 | 20-digit numerics | +0.00108048… and −0.00662543… [[1]] |
| Grid minimum of the ratio (a=1, r∈[[1]][[2]](https://arxiv.org/abs/2608.00987), 2001×1001 grid in x,y) | numeric | 0.188667 at about (x,y,r) = (0.434, 1/3, 2), against c = 0.188580 [[1]] |
| Integer scan (a ≤ d ≤ 60, Ψ(a,d) > 2, all admissible splits) | exhaustive | minimum 0.188889 at (a,d,i,j) = (30,60,13,20) [[1]] |
| Threshold table k=1..8 | numeric | see section 4 [[1]] |
| Case proof of the lemma, balanced-edge lemma, iteration | reasoned only | see sections 2–3 |

The grid minimum sits just above c because the grid does not hit x = t exactly. That is consistent with c being the infimum but is not a proof. The scan finds no integer instance below c. I checked the extremal integer instance by hand: Ψ(30,60) = 1800, Ψ(13,40) = 338 and Ψ(17,20) = 340, so the ratio is 340/1800 ≈ 0.1889.

## 2. Line-by-line audit of the lemma

**Constants.** t² = (14−2√13)/36 = (7−√13)/18, so 3t²+t = (7−√13)/6 + (√13−1)/6 = 1. Then t ≈ 0.4343 < 1/2, c ≈ 0.18858 < 2/9, and 1−t = 3c. The numerics agree [[1]].

**Properties of Ψ.** Ψ(p,q) = min(pq, 2p², 2q²) is symmetric, homogeneous of degree 2, and nondecreasing in each argument, because it is a minimum of nondecreasing functions. For a ≤ d it equals min(ad, 2a²).

**Reflection.** The map (x,y) → (1−x,1−y) swaps the two outputs and keeps y in [1/3,2/3]. So x+y ≤ 1 is without loss of generality, which gives 1−y ≥ x. Homogeneity reduces the problem to a=1, d=r ≥ 1.

**Reduction r>2 to r=2.** For r ≥ 2, Ψ(1,r) = min(r,2,2r²) = 2. Both outputs are nondecreasing in r, so they only decrease when r is lowered to 2. If the maximum is at least 2c at r=2, it is at least c·Ψ(1,r) = 2c for every r>2. The reduction is valid.

**Case x ≥ t, with 1 ≤ r ≤ 2.** All three entries of Ψ(x,(1−y)r) are at least cr:

- x(1−y)r ≥ x²r ≥ cr, using 1−y ≥ x.
- 2x² ≥ 2c ≥ cr, using r ≤ 2.
- 2(1−y)²r² ≥ 2r²/9 ≥ cr, which needs r ≥ 9c/2 ≈ 0.85; this holds because r ≥ 1.

**Case x < t.** All three entries of Ψ(1−x,yr) are at least cr:

- (1−x)yr > (1−t)r/3 = cr.
- 2(1−x)² > 2(1−t)² ≥ 2t² = 2c ≥ cr. The middle step needs t ≤ 1/2 and the last needs r ≤ 2.
- 2y²r² ≥ 2r²/9 ≥ cr.

The two cases cover all x in [0,1], and the boundary x = t falls in the first case.

**Boundaries.** I re-ran the cases by hand at x=0, x=1, x=t, y∈{1/3,2/3}, x+y=1, r∈{1,2} and a=d. Each passes. The minimum is approached only at x=t, y=1/3, r=2 (and its reflection).

**Sharpness.** Take a=1, d=2, x=t, y=1/3.

- First output: (1−y)d = 4/3, not 2/3. Ψ(t,4/3) = min(4t/3, 2t², 32/9) = 2t² = 2c, since 4t/3 > 2t² when t < 2/3.
- Second output: Ψ(1−t,2/3) = min(2(1−t)/3, 2(1−t)², 8/9) = 2(1−t)/3 = 2c, which uses 1−t = 3t².
- Input: Ψ(1,2) = 2.

The ratio is exactly c, so no larger constant works for the real inequality. The exact sympy residuals confirm both outputs equal 2c [[1]].

**Caveat on "attained".** The extremal x = t is irrational, whereas in the tree setting x = |X∩A|/|X| is rational. So the optimum is attained only in the real relaxation. For integer inputs with a,d ≤ 60 the scan minimum is 0.18889, above c [[1]]. The integer infimum is plausibly c, approached by taking a large with d = 2a and x close to t, but I have not proved this.

## 3. Audit of the reductions around the lemma

**Balanced edge (reasoned).** Take non-negative leaf weights summing to 1, each at most 1/2, on a trivalent tree.

1. Root the tree at any leaf r. The root's only child has subtree weight 1−w(r) ≥ 1/2.
2. Let v be a node of minimal subtree weight subject to W(v) ≥ 1/2, so every child of v has weight below 1/2.
3. If W(v) ≤ 2/3, the edge above v splits the weight into W(v) ∈ [1/2,2/3] and 1−W(v) ∈ [1/3,1/2].
4. Otherwise the two children's weights sum to more than 2/3 and each is below 1/2. So the larger child has weight in (1/3,1/2), and the edge above it works.
5. If v is a leaf, then W(v) = 1/2 exactly and the edge above it splits 1/2 | 1/2.

The bound of 1/2 on leaf weights is used only to guarantee step 1. A single leaf of weight above 1/2 is the case that can fail. Spencer-type 1/3–2/3 edges are also stated for the unweighted case in the literature [[3]](https://arxiv.org/abs/2607.12778).

**Weights must be the normalised indicator of Y (wording gap).**

- The lemma needs y ∈ [1/3,2/3] for the fraction of Y cut by the new edge.
- An edge that is balanced for uniform weights on all n leaves does not control how Y is cut; Y could lie entirely on one side.
- The edge must therefore be balanced for weights 1/|Y| on the leaves of Y and 0 elsewhere. These weights sum to 1 and are at most 1/2 exactly when |Y| ≥ 2.
- This is where the condition d ≥ 2 enters, and why the remark that intermediate potentials exceed 2 matters.
- Because the constraint is on the larger set, the pair must be re-ordered so that Y is the larger set after every step. Ψ is symmetric, so the potential itself is unaffected. The research notes record that an earlier simulation without the re-ordering failed at k=3, but no output from that run is on record. I treat this as a likely cause, not a confirmed one.

**Cross-pairing (reasoned).** Keeping (X∩A, Y∩B) or (X∩B, Y∩A) preserves separation in earlier trees, because subsets of separated sets remain separated. It also gives separation in the new tree, because the chosen edge has them on opposite sides. Keeping same-side pairs would not give separation in the new tree. So the two outputs (xa,(1−y)d) and ((1−x)a,yd) are the right ones.

**Initial potential (reasoned).** A balanced edge of T1 has a ∈ [n/3,n/2]. On this range:

- ad = a(n−a) is increasing, so ad ≥ (n/3)(2n/3) = 2n²/9.
- 2a² ≥ 2n²/9.
- 2d² ≥ n²/2.

So Ψ ≥ 2n²/9.

**Iteration and integrality (reasoned).**

- After k−1 steps, Ψ ≥ (2n²/9)c^(k−1).
- This exceeds 2 exactly when n > 3c^(−(k−1)/2) = 3β^(k−1). At equality it is only ≥ 2, which is not enough.
- Strict Ψ > 2 forces both integer sizes to exceed 1, because Ψ ≤ 2a² and Ψ ≤ 2d². So both sizes are at least 2, and the quartet x1x2|y1y2 is displayed in every tree.
- Since c < 1, every intermediate potential is at least the final one, so every call has d ≥ 2 and leaf weight at most 1/2.
- No extra factor of 2 on n is needed. The size heuristic gives final size just above 1 at n just above 3β^(k−1), and strictness plus integrality lifts it to 2.
- The least integer n > z is ⌊z⌋+1 even when z is an integer. For k ≥ 2, 3β^(k−1) is irrational, because β² = β+3 makes β^m = u_m·β + 3u_{m−1} with positive integer u_m. So the equality case never arises there.
- The bound extends to all larger n, since restricting trees to a subset of leaves preserves a common quartet.

**k = 1.** There are no steps and the formula gives 4. That is correct: n > 3 means n ≥ 4, and any tree on 4 leaves has a quartet. In the literature h(k) is defined for k ≥ 2 as M_k(4) [[3]](https://arxiv.org/abs/2607.12778), so k=1 is a degenerate sanity case.

## 4. Implication for the common-quartet threshold

Since β = 1/t = (1+√13)/2 ≈ 2.302776, which is below 4/√3 ≈ 2.309401 [[1]], the exact constant strictly improves the base. Integer thresholds ⌊3β^(k−1)⌋+1 versus the 4/√3 version [[1]]:

| k | exact c, β ≈ 2.3028 | 4/√3 (c = 3/16) |
|---|---|---|
| 1 | 4 | 4 |
| 2 | 7 | 7 |
| 3 | 16 | 17 |
| 4 | 37 | 37 |
| 5 | 85 | 86 |
| 6 | 195 | 198 |
| 7 | 448 | 456 |
| 8 | 1031 | 1052 |

The integer gain appears at k=3 and k=5..8, but not at k=1,2,4.

Compared with published values:

- Snir–Yuster give 10 ≤ h(3) ≤ 14, and h(2) = 6 [[3]](https://arxiv.org/abs/2607.12778). The potential bounds of 16 and 7 are weaker, so the sharp constant does not displace the existing small-k results.
- The published bounds are 8^{1/4}·3^{k/4} ≤ h(k) ≤ tw₃(6(k−1)2^k + O(log k)) for k ≥ 3 [[3]](https://arxiv.org/abs/2607.12778). The new bound lies between these and is not contradicted by them.
- A single-exponential upper bound would be a large improvement on the tower-type bound in that paper. I re-derived each step and found no gap. I did not find a published single-exponential bound, but that does not establish that none exists. The result should not be presented as independently corroborated by the literature.

A second consistency check is reasoned, not executed. Since Ψ ≤ 2a² for the smaller side a, the potential method guarantees a smaller-side size of at least (n/3)·c^((k−1)/2).

- For k=2 this is about 0.145n, below the published n/6 ≈ 0.167n for g(2,n) [[3]](https://arxiv.org/abs/2607.12778).
- For k=3 it is about 0.063n, below the published 2n/27 ≈ 0.074n for g(3,n) [[3]](https://arxiv.org/abs/2607.12778).
- Those published bounds are described as asymptotically best possible [[3]](https://arxiv.org/abs/2607.12778).

So the lemma does not overstate what is achievable. The potential method is weaker than the published g(2,n) and g(3,n) bounds. Its value is a uniform recursion in k.

## 5. What remains unestablished

- **Formal verification.** There is no Lean or other formal proof of the sharp lemma. The statement that the existing Lean file proves only the rational 3/16 inequality is a repository claim I could not check. The sharper result should not be called Lean-verified until the formal proof is extended.
- **Integer infimum.** I have not proved that the integer-domain infimum equals c.
- **Tree simulation.** There is no completed end-to-end simulation for k≥3. The check was not completed because the analysis tool failed on re-runs. The k≥3 separation and iteration claims rest on reasoning.
- **Independent hand check.** A delegated hand check re-derived the lemma and found no counterexample. It ran no code and its notes were truncated, so it is a second reasoning pass, not an execution.
- **Scope.** The result is an upper bound from one potential and one strategy. It does not show that this strategy, or h(k), has an optimal exponential base.

## 6. Synthesis

The sharp constant c = (7−√13)/18 is supported by a complete case proof, by exact symbolic identities, and by numerical and integer searches that find nothing below c. The sharpness example is correct once (1−y)d is read as 4/3. For the integration:

- State that the weights are the normalised indicator of the larger set, and that Y is the larger set at every step.
- Describe the optimum as sharp over the reals only.
- Describe the improvement as relative to the 4/√3 version, not to the existing small-k values (14 at k=3, 6 at k=2).
- Add the formal and k≥3 simulation checks before adding "verified" language to videos or readiness notes.

## Sources

[1] Analysis: Exact/numeric audit of Psi lemma, sharpness, and threshold
[2] Testing Full Quartet Consistency: Adaptive Reconstruction, Random Verification, and Constant-Query Testability - https://arxiv.org/abs/2608.00987
[3] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/abs/2607.12778
