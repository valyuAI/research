# Final adversarial review: Lemma B and the 4/√3 bound, the 2^k+1 caterpillar family, and the 22-leaf four-tree family

Task DR-007 | mode max | completed 2026-10-26T12:25:40.119Z | cost 16.125

# Final adversarial review: Lemma B and the 4/√3 bound, the 2^k+1 caterpillar family, and the 22-leaf four-tree family

## Executive summary

I found no mathematical errors in any of the three new items. The proofs hold line by line, and the computations support them.

- **Item 1 (base 4/√3 bound).** Lemma B is correct, and WLOG x+y≤1 is compatible with the case split. An exact-rational branch-and-bound over (x, y, r), which does not use x+y≤1, also certifies it [[1]]. The constant 3/16 is nearly tight: the worst ratio found is about 1.006 [[2]]. The Theorem is correct, and its small-k values are 4, 7, 17, 37, 86, 198 [[2]]. For k = 2, 3, 4, 5 it is weaker than the truth or the dynamic-programming bounds. It matters only asymptotically.
- **Item 2 (caterpillars).** The case analysis is complete and correct, including k = 2. The family has no common quartet for k = 1..6, with every 4-set checked, and for k = 7 on 129 leaves [[2]][[3]]. So h(k) ≥ 2^k+2.
- **Item 3 (22 leaves).** The four trees are unrooted binary trees on leaves 1..22 with 0 common quartets over all 7315 4-sets, by two independent methods [[4]][[5]]. They equal T, sT, s²T, s³T for s = (1 2 3 4)(5 6 7 8)(9 10 11 12)(13 14 15 16)(17 18 19 20)(21 22), of cycle type 4^5 2 [[5]]. So h(4) ≥ 23. With the previously confirmed h(4) ≤ 28, this gives 23 ≤ h(4) ≤ 28.
- **Prior art.** I found none for any of the three items among indexed sources up to 26 October 2026. Absence is not proven; see the limits in the prior-art section.

Together, Items 1 and 2 bracket the growth rate: 2^k+2 ≤ h(k) ≤ ⌊3(4/√3)^(k−1)⌋+1, so the exponential base lies between 2 and about 2.309. Currie et al. give only a lower bound of 8^{1/4}·3^{k/4} and a tower-type upper bound [[6]](https://arxiv.org/pdf/2607.12778v2).

## Item 1: the base-4/√3 upper bound

### Lemma B, every inequality

**Reduction (x,y) → (1−x,1−y).** O1(x,y) = Ψ(xa,(1−y)d) equals O2(1−x,1−y), since O2(x′,y′) = Ψ((1−x′)a, y′d). The map keeps y in [1/3, 2/3]. Either x+y ≤ 1 or (1−x)+(1−y) ≤ 1, so WLOG x+y ≤ 1.

**Homogeneity and the r ≤ 2 step.** Ψ is homogeneous of degree 2, so set a = 1 and d = r ≥ 1.
- For 1 ≤ r ≤ 2, Ψ(1,r) = min(r, 2, 2r²) = r. The target is therefore 3r/16.
- For r ≥ 2, Ψ(1,r) = 2.
- Ψ is nondecreasing in each argument, so O1 and O2 only decrease as r drops to 2. It suffices to prove max ≥ 3/8 at r = 2, which is the r = 2 instance of the target.
- Hypothesis a ≤ d survives the reduction.

**Case x ≥ 7/16.** This case uses both x+y ≤ 1 and r ≥ 1.
- From y ≤ 1−x we get 1−y ≥ x, and r ≥ 1 gives (1−y)r ≥ x. So the third term 2(1−y)²r² is at least 2x², and O1 = min(x(1−y)r, 2x²).
- x(1−y) ≥ x² ≥ 49/256 > 3/16, so the first term exceeds 3r/16.
- 2x² ≥ 98/256 ≈ 0.383 > 0.375 ≥ 3r/16 for r ≤ 2.

**Case x < 7/16.** This case does not use x+y ≤ 1, so the WLOG is compatible with it. All three terms of O2 = Ψ(1−x, yr) are checked.
- (1−x)·y·r > (9/16)(1/3)r = 3r/16.
- 2(1−x)² > 162/256 ≈ 0.633 > 0.375.
- 2y²r² ≥ 2r²/9 ≥ 3r/16, which holds iff r ≥ 27/32, true since r ≥ 1.

So Lemma B holds, with strict inequalities.

**Computational checks.** None found a violation.
- Grid and random-sample searches (5,000,000 random samples). The minimum of max(O1,O2)/((3/16)Ψ) is 1.0062 on the grid and 1.0119 in the random sample [[2]]. The worst grid point is r = 2, y = 1/3, x ≈ 0.434 [[2]].
- Exact-rational branch-and-bound over (x, y, r) ∈ [0,1] × [1/3,2/3] × [[2]][[7]](https://pith.science/paper/2607.12778). It certified max(O1,O2) ≥ 3r/16 on all boxes (551 boxes, no failure) [[1]].
  - The monotone box bounds used are valid, because Ψ is monotone in each argument and O1 and O2 are monotone in x, y and r.
  - This check does not use the x+y ≤ 1 reduction.
  - The case r > 2 follows from monotonicity together with the r = 2 box.

The slack is only about 0.6%, so the constants 7/16 and 3/16 cannot be shaved without a new argument.

### The Theorem

**Base step.** Lemma A with weights 1/n gives sides a ≤ n/2 ≤ d with a ≥ n/3. Then:
- ad ≥ (n/3)(2n/3) = 2n²/9, because a(n−a) increases for a ≤ n/2;
- 2a² ≥ 2n²/9;
- 2d² ≥ n²/2.

So Ψ ≥ 2n²/9.

**Inductive step.**
- Lemma A needs every leaf weight at most 1/2, that is d ≥ 2. This holds because Ψ ≤ 2·min(a,d)² and Ψ > 2 force min ≥ 2 for integers. The theorem states the final claim (both sets of size ≥ 2) but should say explicitly that d ≥ 2 holds at every stage; it does.
- The restriction T′|(X∪Y) has at least 2 leaves.
- The new pairs have sizes (xa, (1−y)d) and ((1−x)a, yd), exactly the arguments of O1 and O2.
- Ψ is symmetric. After each step the smaller set must be relabelled as X, to match the hypothesis a ≤ d of Lemma B.
- Lemma B allows x = 0 or x = 1.

**Final bound.** After k trees, Ψ ≥ (2n²/9)(3/16)^(k−1) > 2 iff n² > 9(16/3)^(k−1), that is n > 3(4/√3)^(k−1). The lower bounds on Ψ decrease along the chain, so Ψ > 2 holds at every stage.

**Integrality.** The smallest integer n is ⌊3(4/√3)^(k−1)⌋+1. The floating-point value at k = 3 is 16.000000000000004, but the exact value is 16, so n = 16 fails the strict inequality and the bound is 17 [[2]].

| k | 3(4/√3)^(k−1) (float) | smallest n (exact) |
|---|---|---|
| 1 | 3.0 | 4 |
| 2 | 6.93 | 7 |
| 3 | 16.0 | 17 |
| 4 | 36.95 | 37 |
| 5 | 85.33 | 86 |
| 6 | 197.07 | 198 |
| 7 | 455.11 | 456 |
| 8 | 1051.03 | 1052 |

Source for the table: [[2]]. The task's list for k = 1..6 is confirmed.

**Small k.** k = 1 gives 4, which is tight. k = 2 gives 7, against h(2) = 6, which Snir and Yuster state [[8]](https://arxiv.org/pdf/2602.23096). For k = 3, 4, 5 the theorem gives 17, 37, 86, against h(3) = 14 and the dynamic-programming bounds 28 and 61 (confirmed earlier, not redone here).

**Consistency with Snir–Yuster's tight constants.** The method yields min(a,d) ≥ √(Ψ/2). That is about 0.144n at k = 2 and n/16 at k = 3. These are below the tight constants n/6 and 2n/27 [[8]](https://arxiv.org/pdf/2602.23096), so there is no contradiction.

**End-to-end simulation.** The theorem's procedure was run on random binary trees (n = 30 to 120, k = 3 to 6, 1070 steps). A balanced edge always existed, and the better diagonal pair always had Ψ_new ≥ (3/16)Ψ_old; the minimum observed ratio was 0.2 [[1]]. This is only a sanity check. A separate exact-fraction test of Lemma A (2664 random trees with 2 to 14 leaves, including weights of exactly 1/2) found no failure [[3]].

## Item 2: the caterpillar family

### Proof, every case

The structure used is as follows.
- C_0 is the identity order. C_{k−1} differs from C_0 only in layers j > L/2, because bit k−2 of j−1 is 1 exactly for j > L/2. Hence C_{k−1} is C_0 with the middle block (positions L/2+1 … m−L/2, centre fixed) reversed.
- Outer layers j ≤ L/2 never leave their blocks in any C_t, and they keep their left/right sides in C_0 and C_{k−1}. In C_t they swap sides according to bits 0..k−3 of j−1.
- Restricting to inner layers + centre, or to outer layers + centre, C_0..C_{k−2} become the (k−1)-family. For inner layers, j−1 = L/2+(i−1), so the extra bit sits at position k−2 and the lower bits are those of i−1.

Case analysis by the number o of outer elements in the 4-set Q, with "middle" meaning inner layers plus centre:

- **o = 0 or o = 4.** Induction on the restricted families.
- **o = 3 plus a middle element x.** Replacing x by the centre changes no split, since both lie in the middle block in every C_t. The set then falls under "outer + centre", handled by induction.
- **o = 1, middle elements p<q<r in C_0 order.**
  - Outer element on the left: C_0 gives op|qr and C_{k−1} gives or|qp.
  - Outer element on the right: C_0 gives pq|ro and C_{k−1} gives rq|po.
  - Both pairs differ.
- **o = 2, middle p<q.**
  - Outer elements on opposite sides in C_0: C_0 gives o₁p|qo₂ and C_{k−1} gives o₁q|po₂, which differ.
  - Same side in C_0: C_0 and C_{k−1} both give o₁o₂|pq. Here o₁ and o₂ lie in different layers j₁ ≠ j₂, because a layer's two elements are on opposite sides in C_0. They have the same smaller/larger status, so in C_t they are on opposite sides iff β_t(j₁) ≠ β_t(j₂). Since j₁,j₂ ≤ L/2, the numbers j₁−1 and j₂−1 have only bits 0..k−3 and differ in one of them. That gives some t ∈ [1, k−2] where they are on opposite sides, and then the split cannot be o₁o₂|pq.

**k = 1 and k = 2.** For k = 1 there are 3 leaves and no 4-set. For k = 2 there is a single outer layer, so any two outer elements are the same layer on opposite sides, and the "same side" subcase is vacuous. The inner-plus-centre set has 3 elements, so the o = 0 case is vacuous. The k = 2 orders are 12345 and 14325 [[2]].

**Completeness.** All o ∈ {0,…,4} are covered, and the centre counts as middle throughout. I found no gap.

### Computation

- For k = 1..6 (m = 3, 5, 9, 17, 33, 65), every C_t is a permutation of [m] and all C(m,4) 4-sets (677,040 for k = 6) were enumerated. There are 0 common quartets in every case [[2]].
- For k = 7 (129 leaves, C(129,4) = 11,009,376 4-sets), a different, vectorised encoding also found 0 common quartets [[3]].
- The k = 3 orders are 123456789, 183654729, 127654389 [[2]].

### Relation to Snir–Yuster

Snir and Yuster state h*(k) = 2^k+2. They say the upper-bound family on 2^k+1 leaves "can be done recursively; we omit the details", and give only k = 3 [[8]](https://arxiv.org/pdf/2602.23096). Their lower-bound argument is that any k permutations of order 2^k+2 separate two disjoint 2-sets [[8]](https://arxiv.org/pdf/2602.23096).

Their printed example "12345679, 127654389, 183654729" has a first order missing the digit 8. The construction gives 123456789 [[8]](https://arxiv.org/pdf/2602.23096)[[2]]. The extracted text prints "2k", which I read as 2^k with the superscript lost; this agrees with their h*(3) = 10 [[8]](https://arxiv.org/pdf/2602.23096).

Since a restriction of a no-common-quartet family has none either, the family gives h(k) ≥ 2^k+2. This is 18 at k = 4, below the 22-leaf bound.

## Item 3: the 22-leaf family

- **Structure.** All four Newick strings parse as connected unrooted binary trees on exactly the leaves 1..22, with 20 internal vertices of degree 3 each [[4]].
- **Common quartets.** Over all 7315 4-sets there are 0 common quartets, by edge-split enumeration [[4]] and independently by the four-point condition on path lengths [[5]].
- **Agreement profile.** Pairwise common quartets are 1882 for the pairs (1,2), (2,3), (1,4), (3,4) and 1769 for (1,3), (2,4). Every triple of trees shares exactly 287 quartets [[4]]. So the zero count is not a near-agreement artefact.
- **Permutation structure.** Each consecutive pair has 256 label-preserving isomorphisms, and exactly one leaf permutation s satisfies s(T₁)=T₂, s(T₂)=T₃, s(T₃)=T₄, s(T₄)=T₁ [[4]].
  - Its cycles are (1 2 3 4)(5 6 7 8)(9 10 11 12)(13 14 15 16)(17 18 19 20)(21 22), so the type is 4^5 2 and s⁴ = id [[5]].
  - Direct relabelling of the quartet tables confirmed s(T_i) = T_{i+1} for all four i, indices mod 4 [[5]].

The four trees are therefore T, sT, s²T, s³T, and h(4) ≥ 23.

## Item 4: prior art up to 26 October 2026

**What was found.**
- Snir–Yuster arXiv:2602.23096 has only v1 (26 Feb 2026) [[9]](https://arxiv.org/abs/2602.23096). It contains h(2) = h*(2) = 6, h(3) > h*(3) = 10 via a Figure 4 on 10 leaves, and the omitted-details statement for h*(k) = 2^k+2 [[8]](https://arxiv.org/pdf/2602.23096).
- Currie et al. arXiv:2607.12778 has v1 (14 Jul 2026) and v2 (17 Jul 2026), and no later version appears on the abstract page [[10]](https://arxiv.org/abs/2607.12778v2). Theorem 5 states 8^{1/4}3^{k/4} ≤ h(k) ≤ tw₃(6(k−1)2^k + O(log k)) for k ≥ 3, with 10 ≤ h(3) ≤ 14 quoted from Snir–Yuster [[6]](https://arxiv.org/pdf/2607.12778v2). Their lower bound is about 5.05 at k = 4. They contain no caterpillar construction, no exponential upper bound with base below 3, and no lower bound on h(4) beyond that.
- Other 2026 postings retrieved concern different problems: maximum quartet distance [[11]](https://arxiv.org/html/2608.03542), quartet CSP refutation [[12]](https://arxiv.org/abs/2607.13817), and 2-weakly compatible split systems [[13]](https://pith.science/paper/2608.23275). None addresses h(k).

**Not found.** In the sources searched, I found no bound h(k) ≤ C·c^k with c < 3, no h(4) ≥ 23 or four 22-leaf trees, and no explicit k-caterpillar family.

**Limits on that conclusion.**
- The journal version of Snir–Yuster could not be read: the publisher page returned a bot wall [[14]](https://www.sciencedirect.com/science/article/pii/S0166218X26001228). Whether it expands the omitted construction is unverified, though the arXiv abstract and the Haifa record's abstract are identical [[15]](https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/).
- The search covered indexed sources only. Unindexed blogs, theses and private repositories cannot be excluded.

**Citation detail.**
- The DAM volume is 387: pages 160–171, published 15 July 2026, DOI 10.1016/j.dam.2026.02.042 [[15]](https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/), with ScienceDirect [[16]](https://www.sciencedirect.com/author/7004689495/raphael-yuster) and ACM DL [[17]](https://dl.acm.org/doi/book/10.5555/984029) agreeing. The task's citation is correct.
- Currie et al.'s abstract says 347 [[10]](https://arxiv.org/abs/2607.12778v2)[[6]](https://arxiv.org/pdf/2607.12778v2), but their own reference list says 387 [[6]](https://arxiv.org/pdf/2607.12778v2). The 347 is their typo.
- A machine review (Pith) flagged a constant slip in Currie et al.'s Theorem 2 [[7]](https://pith.science/paper/2607.12778). The paper itself states Theorem 2 with 2^k(k−1)n [[6]](https://arxiv.org/pdf/2607.12778v2), consistent with its 6(k−1)2^k bound for h(k). The flag appears to come from lost superscripts. It does not affect h(k).

## Precise error list

- **No mathematical errors found** in Lemma B, the Theorem, the caterpillar proof, or the 22-leaf family.
- **Presentation points for the note:**
  1. State that d ≥ 2 is guaranteed at every stage by Ψ > 2 (Lemma A needs weights ≤ 1/2).
  2. State that the smaller set is relabelled X after each step.
  3. In Lemma B's case x ≥ 7/16, note the use of both x+y ≤ 1 and r ≤ 2.
  4. Compute the threshold exactly: the float value at k = 3 is 16.000000000000004 but the exact value is 16, so the bound is 17.
  5. Say that for k = 2, 3, 4, 5 the theorem is weaker than the known values or bounds (7 vs 6, 17 vs 14, 37 vs 28, 86 vs 61).
  6. In the caterpillar proof, say the o = 2 same-side subcase is vacuous at k = 2.
  7. The Snir–Yuster k = 3 example has a missing 8 in its first order.

## Synthesis

Together the three items give 18 ≤ h(4) and, from Item 3, 23 ≤ h(4) ≤ 28. For general k, they give 2^k+2 ≤ h(k) ≤ ⌊3(4/√3)^(k−1)⌋+1. The growth base of h(k) lies between 2 and about 2.309, sharply narrowing the gap left by the published exponential lower bound and tower-type upper bound. Item 1 is a genuine asymptotic gain but gives no small-k improvement. Items 2 and 3 are explicit, machine-checked lower-bound constructions. The 22-leaf family beats the caterpillar bound at k = 4 and has a clean cyclic symmetry, which may suggest a route to more such families, though this is not established here. Priority claims rest on an indexed-source search only and should be worded accordingly.

## Sources

[1] Analysis: Rigorous exact-rational box verification of Lemma B + simulation of theorem procedure
[2] Analysis: Lemma B numeric search, Theorem values, caterpillar check k<=6
[3] Analysis: Lemma A stress test and caterpillar k=7 check
[4] Analysis: Verify 22-leaf four-tree family
[5] Analysis: Independent 4-point check of 22-leaf family and s-cycle
[6] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/pdf/2607.12778v2
[7] On Agreement Subtrees in Multiple Phylogenetic Trees · Pith Review - https://pith.science/paper/2607.12778
[8] 2602.23096 - https://arxiv.org/pdf/2602.23096
[9] [2602.23096] Simultaneous separation in bounded degree trees - https://arxiv.org/abs/2602.23096
[10] [2607.12778v2] On Agreement Subtrees in Multiple Phylogenetic Trees - https://arxiv.org/abs/2607.12778v2
[11] The maximum quartet distance between phylogenetic trees - https://arxiv.org/html/2608.03542
[12] Strong Refutation of Ordering, Phylogenetic, and Ordinary CSPs, and New Satisfiability and Refutation Thresholds for Triplet and Quartet Reconstruction - https://arxiv.org/abs/2607.13817
[13] On the maximum size of 2-weakly compatible split systems · Pith Review - https://pith.science/paper/2608.23275
[14] ScienceDirect - https://www.sciencedirect.com/science/article/pii/S0166218X26001228
[15] Simultaneous separation in bounded degree trees - University of Haifa - https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/
[16] Raphael Yuster | ScienceDirect - https://www.sciencedirect.com/author/7004689495/raphael-yuster
[17] Algorithmic Graph Theory and Perfect Graphs (Annals of Discrete Mathematics, Vol 57): | Guide books | ACM Digital Library - https://dl.acm.org/doi/book/10.5555/984029
