# Adversarial review of h(k) ≤ ⌊3(5/2)^(k−1)⌋ + 1 for common quartets of k phylogenetic trees

Task DR-020 | mode max | completed 2026-10-26T11:31:03.346Z | cost 16.225

# Adversarial review of h(k) ≤ ⌊3(5/2)^(k−1)⌋ + 1 for common quartets of k phylogenetic trees

## Executive summary

- **No error found.** Lemma A, Lemma B and the Theorem hold as stated. This covers the case analysis, the symmetry reductions, the restriction/edge correspondence, integrality and k = 1, 2. Only a one-word slip in Lemma A's proof needs fixing (see §1.1).
- **Independent computation agrees.** Grid and random-plus-local-minimisation searches over (r, x, y) find the minimum of max(O1,O2)/Ψ(a,d) at 0.16, attained at the stated equality case or its complement [[1]]. A simulation of the full strategy on random, caterpillar, balanced and "blob" trees at n = ⌊3(5/2)^(k−1)⌋ + 1 for k ≤ 6 violated nothing [[2]]. These runs are a sanity check, not a worst-case search.
- **Prior art.** No single-exponential bound, and no bound of the form C·c^k with c ≤ 3, was found for h(k) up to 2026-10-26. The best posted upper bound is a four-fold iterated exponential [[3]](https://arxiv.org/abs/2607.12778)[[4]](https://pith.science/paper/2607.12778). This negative result comes from a non-exhaustive search; absence from citation indexes, GitHub and Zenodo is unestablished.
- **Correction to the context.** Snir–Yuster's caterpillar value is h\*(k) = 2^k + 2, not a linear function of k [[5]](https://ar5iv.org/abs/2602.23096). The lower bound 8^(1/4)·3^(k/4) of Currie et al. [[3]](https://arxiv.org/abs/2607.12778) is therefore far from the best available. The honest sandwich is 2^k + 2 ≤ h(k) ≤ ⌊3(5/2)^(k−1)⌋ + 1, so the base lies in [2, 5/2].
- **Small cases improve nothing.** h(2) = 6 and h(3) ≤ 14 are already known [[3]](https://arxiv.org/abs/2607.12778), while the claim gives 8 and 19. The contribution is asymptotic.
- **Base 5/2.** The reported adaptive constant is plausible but not reproduced in general. A one-pair method cannot beat base 3/√2 ≈ 2.12 without contradicting Snir–Yuster's bounded-degree constructions (§4). A cheap constant improvement is available by starting from Snir–Yuster's two-tree lemma (§4).

## 1. Verification

### 1.1 Lemma A

The out-degree argument is correct. Orient each edge toward its side of weight > 1/2; a vertex with two out-edges would need two disjoint sides each of weight > 1/2. A tree has fewer edges than vertices, so some vertex has out-degree 0, and the heaviest of its three components lies in [1/3, 1/2].

One wording slip: "else the leaf weighs > 1/2" should read ≥ 1/2. A leaf of weight exactly 1/2 gives an edge with both sides 1/2, which is the excluded first case, so the conclusion is unaffected. The hypotheses needed are at least 2 leaves and weights ≤ 1/2. The weights 1/(2a) and 1/(2d) are ≤ 1/2 because a, d ≥ 1.

The unweighted (1/3, 2/3) form is the "well known" property that Snir–Yuster use for phylogenetic trees [[5]](https://ar5iv.org/abs/2602.23096).

### 1.2 Lemma B

The symmetries and reductions are all valid.

- Swapping (x,a)↔(y,d) swaps O1 and O2. So does (x,y)→(1−x,1−y). Both preserve 2/3 ≤ x+y ≤ 4/3.
- For r > 2, Ψ(1,r) = 2 and the O_i are nondecreasing in d, so lowering r to 2 only weakens the target.
- With x ≤ 1−y ≤ (1−y)r, the dropped term 2(1−y)²r² in O1 is never the minimum.

Each case holds.

- **x ≥ 2/5.** x(1−y) ≥ x² ≥ 4/25 and 2x² ≥ 8/25 ≥ 4r/25.
- **x < 2/5, y ≥ 2/(5w).** The map x ↦ (1−x)(2/3−x) is decreasing, with value 4/25 at x = 2/5. Also 2(1−x)² > 18/25 ≥ 4r/25, and 2y²r² ≥ 8r²/(25·2r) = 4r/25.
- **x < 2/5, y < 2/(5w).** The inequality 2/3 − 2/(5w) ≥ w/5 is equivalent to 3w² − 10w + 6 ≤ 0. The roots are (5±√7)/3 ≈ 0.785 and 2.549, which bracket [√2, 2] [[1]]. Then 2x² > 4r/25, and x(1−y) > (5√2−2)/25 ≈ 0.2028 > 0.16 [[1]].

Hand evaluations at boundary points:

| Point (r = d/a, x, y) | O1 | O2 | max vs 4r/25 |
|---|---|---|---|
| r=2, x=2/5, y=4/15 (equality) | 8/25 | 8/25 | 0.32 = 0.32 |
| r=2, x=y=1/3 | 2/9 | 4/9 | 0.444 > 0.32 |
| r=2, x=0, y=2/3 | 0 | 4/3 | 1.333 > 0.32 |
| r=2, x=2/3, y=0 | 8/9 | 0 | 0.889 > 0.32 |
| r=1, x=y=1/3 | 2/9 | 2/9 | 0.222 > 0.16 |

Numerical search [[1]]:

- The grid used r log-spaced on [1/30, 30] plus [1, 2.5], with a 1201² grid in (x,y) restricted to 2/3 ≤ x+y ≤ 4/3. Its minimum ratio is 0.16 at r = 2, (x,y) = (0.6, 0.7333), the complement of the stated equality point.
- Random starts with local refinement gave 0.160006 at r ≈ 2.000.
- The explicit forms of O1 and O2 matched the true Ψ values on 55,582 random points.
- The case implications showed 0 violations in 300,000 samples.

So the constant 4/25 is tight for this potential and step.

### 1.3 Theorem

- **Initial potential.** With a ∈ [n/3, n/2] and d = n−a, ad ≥ 2n²/9, 2a² ≥ 2n²/9 and 2d² ≥ n²/2, so Ψ ≥ 2n²/9.
- **Step.** The Z-weight (x+y)/2 ∈ [1/3, 2/3] gives exactly the hypothesis of Lemma B. Both diagonal pairs are separated in T1..T_{j+1}. An edge of T|S corresponds to a path of T, and every edge of that path induces the same split of S. Subsets of separated sets stay separated.
- **End.** Ψ > 2 implies both sets are nonempty throughout. Ψ ≤ 2·min² then gives min² > 1, so min ≥ 2 by integrality.
- **Threshold.** The condition (2n²/9)(4/25)^(k−1) > 2 is equivalent to n² > 9(25/4)^(k−1), i.e. n > 3(5/2)^(k−1).
- **Values.** The thresholds are 4, 8, 19, 47, 118, 293 for k = 1..6. Since the Theorem holds for every n above the bound, h(k) ≤ ⌊3(5/2)^(k−1)⌋ + 1.

### 1.4 Strategy simulation

The strategy was run at n = ⌊3(5/2)^(k−1)⌋ + 1. Tree families were random, caterpillars, balanced trees, "blob" trees (pendant caterpillars on a random skeleton) and mixed sets, with independently shuffled labels. Each set was run with both the best and the worst admissible balanced edge. The program asserted, on every run:

- a Lemma A edge exists in each restricted tree;
- every step ratio is ≥ 0.16;
- the final Ψ > 2 and min(|X|,|Y|) ≥ 2;
- X and Y are explicitly separated in all k trees [[2]].

| k | n | runs | min observed step ratio |
|---|---|---|---|
| 1 | 4 | 360 | no step |
| 2 | 8 | 360 | 0.25 |
| 3 | 19 | 360 | 0.2143 |
| 4 | 47 | 360 | 0.18 |
| 5 | 118 | 360 | 0.1641 |
| 6 | 293 | 96 | 0.1675 |

All assertions passed, and the final min(|X|,|Y|) reached exactly 2 for every k [[2]]. The step ratio comes within 0.004 of the proven floor of 0.16 at k = 5, consistent with tightness. Earlier failures in the process were generator bugs in the test harness (a "blob" skeleton whose root was a leaf), not failures of the claim [[6]]. These trees are not adversarially optimised.

## 2. Consistency with known results

| Quantity | Known | Claim |
|---|---|---|
| h(2) | = 6 [[3]](https://arxiv.org/abs/2607.12778)[[5]](https://ar5iv.org/abs/2602.23096) | ≤ 8 |
| h(3) | h(3) > h\*(3) = 10 [[5]](https://ar5iv.org/abs/2602.23096); upper bound 14 from the 2n/27 bound at n = 14 [[3]](https://arxiv.org/abs/2607.12778) | ≤ 19 |
| Caterpillar value | h\*(k) = 2^k + 2 [[5]](https://ar5iv.org/abs/2602.23096) | h(6): 66 ≤ h(6) ≤ 293 |
| Currie et al. lower bound | 8^(1/4)·3^(k/4) ≈ 1.316^k [[3]](https://arxiv.org/abs/2607.12778) | far below the claim |
| Currie et al. upper bound | tw₃(6(k−1)2^k + O(log k)) [[3]](https://arxiv.org/abs/2607.12778) | the claim is far smaller |

Notes on the table:

- Currie et al. quote "10 ≤ h(3) ≤ 14" [[3]](https://arxiv.org/abs/2607.12778), one lower than Snir–Yuster's own "h(3) > 10".
- The caterpillar value is visible only where superscripts survive. The ar5iv rendering shows h\*(k) = 2^k + 2 and "2^k + 1 leaves" [[5]](https://ar5iv.org/abs/2602.23096), while plain-text extraction shows the garbled "2k+2" [[7]](https://arxiv.org/html/2602.23096v1). The k = 3 example uses 9 leaves, consistent with 2^3 + 1. Snir–Yuster omit the proof details of h\*(k) = 2^k + 2 [[5]](https://ar5iv.org/abs/2602.23096).
- Currie et al. do not mention the caterpillar bound [[3]](https://arxiv.org/abs/2607.12778).

**Consistency with the implied g(k,n).** The proof gives min(|X|,|Y|) ≳ (n/3)(2/5)^(k−1). Snir–Yuster's random-label constructions give f ≤ n·2^((k−1)/2)/3^k for odd k [[7]](https://arxiv.org/html/2602.23096v1). Since 0.4 < √2/3 ≈ 0.471, there is no contradiction:

- k = 3: 0.0533 against 2/27 = 0.0741, and 2/27 is exact for phylogenetic trees [[5]](https://ar5iv.org/abs/2602.23096).
- k = 5: 0.00853 against 4/243 = 0.0165.

Those general-k constructions are stated for bounded-degree trees where labelled path vertices may have degree 2. For phylogenetic trees they are adapted explicitly only for k = 2 and 3 [[5]](https://ar5iv.org/abs/2602.23096).

## 3. Prior art and credit

### 3.1 Search result

- **Published or posted bounds.** The only upper bounds located for h(k) are Currie–Czabarka–Fischer–Simmons–Székely–Wicke, *On Agreement Subtrees in Multiple Phylogenetic Trees*, arXiv:2607.12778. Theorem 5 gives 8^(1/4)·3^(k/4) ≤ h(k) ≤ tw₃(6(k−1)2^k + O(log k)), via Ramsey R^4_{2^(k−1)}(6) and Erdős–Rado [[3]](https://arxiv.org/abs/2607.12778). A Pith review confirms h(k) is "sandwiched between an exponential and a four-times iterated exponential" [[4]](https://pith.science/paper/2607.12778). Snir–Yuster, arXiv:2602.23096, pose h(k) as open beyond k = 2 and give h(3) > 10 [[5]](https://ar5iv.org/abs/2602.23096).
- **Versions.** arXiv:2607.12778 has v1 (14 Jul 2026) and v2 (17 Jul 2026, latest) [[8]](https://arxiv.org/abs/2607.12778v2)[[9]](https://arxiv.org/abs/2607.12778v1). The Currie abstract cites Snir–Yuster as "Discrete Appl. Math. 347", but their reference list and the journal record give volume 387, 160–171, doi:10.1016/j.dam.2026.02.042 [[10]](https://arxiv.org/html/2607.12778v2)[[11]](https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/). The question's volume is correct.
- **Citing works.** Beyond Currie et al. citing Snir–Yuster, no citing work was found in the indexed record. Related work on k = 2 (Markin, Discrete Appl. Math. 285 (2020) 612–620, mast₂(n) = Θ(log n) [[12]](https://arxiv.org/pdf/1812.06951)[[13]](https://markin-alex.github.io/documents/papers/amarkin-extremal-MAST-published.pdf); Martin–Thatte, arXiv:1201.5168 [[14]](https://arxiv.org/pdf/1201.5168)) does not bound h(k). Whether anything exists in citation indexes, GitHub, Zenodo or theses is unestablished.

### 3.2 Who should be credited for which ingredient

| Ingredient | Source |
|---|---|
| Balanced vertex in a tree | Jordan, cited by Snir–Yuster for the vertex form and the ⌈(n−1)/r⌉ edge form; separator tradition: Halin, Robertson–Seymour, Lipton–Tarjan; they note these extend to vertex weights "under appropriate assumptions" [[15]](https://arxiv.org/abs/2602.23096) |
| (1/3, 2/3) edge for phylogenetic trees | Snir–Yuster cite Lemma 3.1 of Snir & Yuster, SIAM J. Comput. 41(6) (2012) [[5]](https://ar5iv.org/abs/2602.23096). Currie et al. trace it to Erdős–Faudree–Rousseau–Schelp (1988), *The Book-Tree Ramsey Numbers*, Scientia A 1, 111–117, as the earliest reference they know [[3]](https://arxiv.org/abs/2607.12778)[[10]](https://arxiv.org/html/2607.12778v2). The weighted form with weights ≤ 1/2 (Lemma A) appears in neither |
| Two-bipartition lemma (the k = 2 step, n/6) | Spencer (2004), Contemp. Math. 342, 269–271, in the formulation of Asplund et al., arXiv:1709.08136 [[3]](https://arxiv.org/abs/2607.12778)[[16]](https://arxiv.org/abs/1709.08136). Currie et al. note measure versions [[3]](https://arxiv.org/abs/2607.12778) |
| Iterated halving of separated pairs (paths/permutations) | Alon–Maass, FOCS 1986, Lemma 2.1: with each element appearing k times and N = N₁∪N₂, there exist S ⊆ N₁, T ⊆ N₂ of sizes ≥ |N_i|/2^(2k−1) with all order-type vectors identical [[17]](https://www.tau.ac.il/~nogaa/PDFS/Publications/Meanders,%20Ramsey%20Theory%20and%20lower%20bounds%20for%20branching%20programs.pdf). Journal version: J. Comput. System Sci. 37 (1988) 118–129 [[18]](https://www.tau.ac.il/~nogaa/PDFS/Publications2/Meanders%20and%20their%20applications%20in%20lower%20bounds%20arguments.pdf). Snir–Yuster's proof of f(2,k) = 1/2^k is "quite similar to" this lemma [[7]](https://arxiv.org/html/2602.23096v1) |
| Restrict to X∪Y, balance the next tree, keep the better diagonal pair | Already in Snir–Yuster's proof of Theorem 2.5: for T3 they apply the balanced-edge lemma to X∪Y, form the four cells A, B, C, D, and take the better separated pair. They state g(k,n) ≥ f(3,k,n) [[7]](https://arxiv.org/html/2602.23096v1) |
| **New as far as found** | (i) leaf weights 1/(2a) and 1/(2d), which let one balanced edge control both x and y; (ii) the potential Ψ = min(ad, 2a², 2d²) with per-step factor 4/25 valid for every k; (iii) the resulting single-exponential h(k) bound. No source read applies such a potential across k trees |

So the weighted-centroid-plus-halving idea is classical in spirit, and its two-tree and three-tree instances are in Snir–Yuster. Attribution of the general-k single-exponential bound rests on the potential.

## 4. Is base 5/2 improvable?

**Reported adaptive constant (≈ 17/90, base ≈ 2.30).** A hand check at r = 2 puts all leaf weight on Y, which is allowed when d ≥ 2. The constraint is then y ∈ [1/3, 2/3] with x free. At y = 1/3, O1 = 2x² and O2 = (2/3)(1−x). They meet at 3x² + x − 1 = 0, so x = (√13−1)/6 ≈ 0.4343. The value is (7−√13)/9 ≈ 0.3772, a factor (7−√13)/18 ≈ 0.18858 against Ψ(1,2) = 2, and 1/√0.18858 ≈ 2.303.

- This is within 0.2% of 17/90 = 0.18889 but not equal to it.
- It is a single weighting at r = 2 (plus spot checks at r = 1), not the minimax over all r and all weightings. So 17/90 is plausible but unproven here.
- A rigorous improvement would also need the integrality and final threshold redone.

**Barrier for any one-pair method.** A method guaranteeing min(|X|,|Y|) ≥ c·ρ^k·n for all k needs a per-step potential factor ρ². Snir–Yuster's constructions give f ≤ n·2^((k−1)/2)/3^k for odd k [[7]](https://arxiv.org/html/2602.23096v1). That forces ρ ≤ √2/3, a per-step factor of at least 2/9 and base at most 3/√2 ≈ 2.12. This matches the stated "game value ≈ 3/√2". Two caveats:

- The constructions are rigorous for bounded-degree trees. For phylogenetic trees they are adapted only for k = 2, 3 [[5]](https://ar5iv.org/abs/2602.23096), so the barrier at general k is an extrapolation.
- It concerns the linear regime in n. It does not bound the integer threshold h(k), whose only rigorous floor is 2^k + 2 [[5]](https://ar5iv.org/abs/2602.23096).

**Better arguments.**

- **Unbalanced edges.** Snir–Yuster's f(3,3) = 2/27 and f(3,2) = 1/6 beat this method's 0.0533 and 2/15, which is evidence that unbalanced edges and case analysis help [[7]](https://arxiv.org/html/2602.23096v1)[[5]](https://ar5iv.org/abs/2602.23096).
- **Track more.** Track both diagonal pairs, or the whole 2×2 cell structure, rather than a single pair.
- **Use integrality at small k.** Currie et al. obtain h(3) ≤ 14 from ⌈2n/27⌉ at n = 14 [[3]](https://arxiv.org/abs/2607.12778).
- **Cheap constant gain from a better start (my arithmetic, not tested).**
  - Snir–Yuster's error-free two-tree lemma for phylogenetic trees gives X, Y separated in T1, T2 with |X|, |Y| ≥ 4n/27 and |X∪Y| ≥ 4n/9 [[5]](https://ar5iv.org/abs/2602.23096).
  - This yields Ψ ≥ 32n²/729 ≈ 0.0439n², attained at a = 4n/27 and d = 8n/27. The proof's start (2/9)(4/25)n² gives only 0.0356n².
  - Iterating Lemma B for T3..Tk then gives n > (27/4)(5/2)^(k−2) = 2.7·(5/2)^(k−1). This is a constant improvement (3 → 2.7) at the same base, for example n ≥ 17 at k = 3.

## 5. Conclusions

1. The proof stands. The only fix is "> 1/2" → "≥ 1/2" in Lemma A's proof. Lemma B's constant 4/25 is attained, and the full strategy never violated its guarantees in simulation.
2. As far as the available record shows, h(k) ≤ ⌊3(5/2)^(k−1)⌋ + 1 is the first posted single-exponential upper bound. Present it against the corrected lower bound 2^k + 2, not 8^(1/4)·3^(k/4).
3. Credit the ingredients as in §3.2: Jordan and Erdős–Faudree–Rousseau–Schelp for the balanced edge, Spencer for the two-bipartition lemma, Alon–Maass for iterated halving, and Snir–Yuster for restricting to X∪Y and taking the better diagonal pair. The weighting and the potential Ψ are the new part.
4. Within the one-pair framework the base can plausibly drop to about 2.3 and cannot go below about 2.12 (rigorous for bounded-degree trees, extrapolated for phylogenetic trees). Closing the gap to 2, or proving the true base, needs an argument that uses more than one separated pair.

## Sources

[1] Analysis: Lemma B numerical search (grid + random + local refinement)
[2] Analysis: Simulate the potential strategy on random/adversarial trees at n=floor(3(5/2)^(k-1))+1, k<=6
[3] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/abs/2607.12778
[4] On Agreement Subtrees in Multiple Phylogenetic Trees · Pith Review - https://pith.science/paper/2607.12778
[5] [2602.23096] Simultaneous separation in bounded degree trees - https://ar5iv.org/abs/2602.23096
[6] Analysis: Find which tree kind triggers Lemma A check failure at n=19
[7] 2602.23096 - https://arxiv.org/html/2602.23096v1
[8] [2607.12778v2] On Agreement Subtrees in Multiple Phylogenetic Trees - https://arxiv.org/abs/2607.12778v2
[9] [2607.12778v1] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/abs/2607.12778v1
[10] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/html/2607.12778v2
[11] Simultaneous separation in bounded degree trees - University of Haifa - https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/
[12] On the Extremal Maximum Agreement Subtree Problem - https://arxiv.org/pdf/1812.06951
[13] On the extremal maximum agreement subtree problem - https://markin-alex.github.io/documents/papers/amarkin-extremal-MAST-published.pdf
[14] The maximum agreement subtree problem - https://arxiv.org/pdf/1201.5168
[15] [2602.23096] Simultaneous separation in bounded degree trees - https://arxiv.org/abs/2602.23096
[16] The k-planar crossing number of random graphs and random regular graphs - https://arxiv.org/abs/1709.08136
[17] 1 <s <log n, any input oblivious sequen- tfal-camputation that solves SE(n,m) using 2m/s space, takes n(n· s) time. This result is sharp for all admissible values of n,m,s and is the first known nontrivial time space tradeoff lower bound (… - https://www.tau.ac.il/~nogaa/PDFS/Publications/Meanders,%20Ramsey%20Theory%20and%20lower%20bounds%20for%20branching%20programs.pdf
[18] PII: 0022-0000(88)90002-5 - https://www.tau.ac.il/~nogaa/PDFS/Publications2/Meanders%20and%20their%20applications%20in%20lower%20bounds%20arguments.pdf
