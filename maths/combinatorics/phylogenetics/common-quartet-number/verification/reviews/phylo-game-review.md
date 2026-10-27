# Adversarial review of the 14-leaf lemma (h(3) ≤ 14) and the dynamic-programming bounds h(4) ≤ 28, h(5) ≤ 61

Task DR-041 | mode max | completed 2026-10-26T12:02:46.081Z | cost 16.225

# Adversarial review of the 14-leaf lemma (h(3) ≤ 14) and the dynamic-programming bounds h(4) ≤ 28, h(5) ≤ 61

## Executive summary

**Claim 1 is reproduced.** Two independent re-implementations give 0 failures at n = 14 for |X| = 5, 6, 7. At n = 13 they give 0 failures for |X| = 6 and 891 (shape, X) pairs for |X| = 5. The deduction h(3) ≤ 14 is logically sound. It repeats a bound already in print (Currie et al.), but now rests on a finite check.

**Claim 2 is reproduced, with no logical error found.** An independent dynamic program recomputes the m-safe thresholds for m = 1..4. Every listed pair is m-safe, and each is minimal in its second coordinate. The first-tree check passes at n = 7, 14, 28, 61 for k = 2..5 and fails at n − 1 each time. The lemma was re-derived by hand (below), and the decision procedure was checked against brute force on small cases.

**Three corrections or flags:**
- The A000672 list is mislabelled (a bookkeeping slip).
- The method is not tight at k = 2: it gives 7, while h(2) = 6.
- h(5) ≥ 28 looks weaker than a published bound of 34. That bound rests on a construction the paper omits.

**Not verified here:**
- The 13-leaf triple, so h(3) ≥ 14 and hence h(3) = 14.
- h(4) ≥ 22.
- The level-3 and level-4 safe tables by independent enumeration. They rest on the validated DP and on your checker.

**Literature (to 26 Oct 2026):** no source found with an exhaustive h(3) ≤ 14, any numerical upper bound for h(4) or h(5), or a 13-leaf triple. This is a negative search result, not proof of absence.

## 1. Claim 1 (Lemma 3.4)

### 1.1 Independent recomputation

Two methods were run:
- **Enumeration.** Rooted shapes were built from Wedderburn–Etherington enumeration and converted to unrooted trees. Canonical form was the minimum over all edges, not your centre-based form. Leaf subsets X were enumerated as labelled subsets of one representative per shape.
- **Cluster DP.** This is the same realisable-cluster DP used for Claim 2, with the (3,4)-dominance predicate as "good". It involves no enumeration of shapes.

Unrooted shape counts for n = 4..14 came out as 1, 1, 2, 2, 4, 6, 11, 18, 37, 66, 135 [[1]]. A second run also gave 265 shapes at n = 15 [[2]], which matches the A000672 terms [[3]](https://oeis.org/A000672).

| n | \|X\| | (shape, X) pairs with no good edge | Shapes affected | DP: bad tree exists? |
|---|---|---|---|---|
| 13 | 5 | **891** | 6 | yes |
| 13 | 6 | 0 | 0 | no |
| 14 | 5 | 0 | 0 | no |
| 14 | 6 | 0 | 0 | no |
| 14 | 7 | 0 | 0 | no |
| 13 | 4 | 6449 | 60 | yes |
| 14 | 4 | 11514 | 105 | yes |

Sources: enumeration [[1]], DP [[4]].

The |X| = 4 rows show that the hypothesis |X|, |Y| ≥ 5 is needed. The enumeration and the DP agree on every row. Your 891 is therefore reproduced under the same convention, which counts X as a labelled subset of a fixed representative.

**Cross-check against Claim 2.** Your "good" predicate is exactly level-1 safety: (a,b) is safe iff min ≥ 3 and max ≥ 4. The level-1 thresholds are u = 3 → 4 and u ≥ 4 → 3 [[5]]. So Claim 1 is the statement that (5,9), (6,8), (7,7) are 2-safe at n = 14, while at n = 13 the pair (5,8) is not and (6,7) is. The level-2 thresholds are 5 → 9, 6 → 7, 7 → 6, 8 → 6 [[5]]. Brute force also gives (5,8) not 2-safe and (6,7) 2-safe [[2]]. All three computations agree.

### 1.2 Errata in the Claim 1 description and script

- **Mislabelled counts.** You list 13 numbers "for n = 3..14", which is 12 values. A000672 has offset 0 and is indexed by the number of degree-3 nodes. A tree with t = 2n + 2 vertices has n + 2 leaves [[3]](https://oeis.org/A000672). So the 13 entries are leaf counts 2..14, with 66 at n = 13 and 135 at n = 14.
- **Truncated listing.** The pasted `indep_cnf.py` listing is cut off: the body of `leaf_dists` is missing. As pasted it would not parse, but the function is unused by Claim 1.

### 1.3 The deduction h(3) ≤ 14

Each step was re-derived:

1. The balanced edge of T1 gives sides ≥ ⌈14/3⌉ = 5. Sizes 8 and 9 are symmetric to 6 and 5, so |X| ∈ {5, 6, 7} covers every case.
2. Claim 1 for T2 gives sets A, B of sizes 3 and 4, separated in T1 and T2.
3. T3 restricted to those 7 leaves has an edge splitting them into P, Q with |P|, |Q| ≥ 3. Let a = |A ∩ P| and b = |B ∩ P|, so a + b ∈ {3, 4}.
4. If a ≥ 2 and b ≤ 2, then (A ∩ P, B ∩ Q) has sizes ≥ 2 and ≥ 2. The case a ≥ 2, b ≥ 3 would give |P| ≥ 5, which is impossible.
5. If a ≤ 1, then b ≥ 2, and (A ∩ Q, B ∩ P) has sizes ≥ 2 and ≥ 2.
6. Two separated sets of size ≥ 2 in all three trees give a common quartet.

The deduction is sound.

**What the failures at n = 13 do not show.** The failures at n = 13 say only that this proof route stops at 14. They are not evidence that h(3) > 13. Currie et al. derive h(3) ≤ 14 as ⌈2·14/27⌉ = 2 from the Snir–Yuster bound g(3,n) ≥ 2n/27 [[6]](https://arxiv.org/abs/2607.12778). The error-free form of that bound is only sketched in Snir–Yuster [[7]](https://arxiv.org/html/2602.23096). Claim 1 is an independent, finite verification of the same bound, not an improvement.

## 2. Claim 2: logic of the method

### 2.1 Safe-pair lemma

The induction goes through.
- Shrinking X, Y to subsets X′, Y′ of sizes u′, v′ preserves separation. Swapping the roles of X and Y is harmless.
- A good edge of T′|(X′ ∪ Y′) with i red and j blue on one side gives cross pairs (i, v′ − j) and (u′ − i, j). These are separated in T1..Tj and T′ by the Step, and one dominates an (m−1)-safe pair.
- After m steps the pair is 0-safe (both sizes ≥ 2), which yields a common quartet.
- Taking the first tree's balanced edge as the (k−1)-safe split gives h(k) ≤ n.

Every m-safe pair has both coordinates ≥ 2. If u′ < 2 or v′ < 2, no edge can be good, since each candidate pair has a coordinate ≤ 1. So pendant edges are always bad.

### 2.2 Rooting and clusters

- Rooting at an internal degree-3 vertex gives three child subtrees, and each edge is the top edge of exactly one cluster.
- Goodness is complement-invariant, because (i, v − j) and (u − i, j) swap under i → u − i, j → v − j. So badness depends on the cluster alone.
- The root has no edge above it. A tree with all edges bad therefore exists iff (u, v) is a sum of three realisable clusters.

### 2.3 Realisability recursion and first-tree criterion

- The base cases (1,0) and (0,1) are always bad, as shown above.
- Any two realisable clusters can be siblings, since they come from disjoint leaf sets.
- The first-tree criterion is the same recursion with one colour: s is bad iff (s, n − s) is not (k−1)-safe. Safe sets are symmetric under swapping coordinates, so this is well defined.

### 2.4 Soundness of the checker

Your checker treats unclaimed pairs as unsafe, which only adds bad edges. A "no all-bad tree" verdict is therefore one-sided: it can certify a bound but cannot falsely certify one.

The minimality and monotonicity of thresholds are separate matters. The binary search for thresholds assumes monotonicity in v. That was confirmed numerically only at levels 1 and 2, where the direct tables are symmetric and upward-closed for 2 ≤ u, v ≤ 40 [[2]]. Levels 3 and 4 rely on it for the minimality claims, but not for the upper bounds.

## 3. Claim 2: recomputation

### 3.1 Validation of the decision procedure

- **Against labelled trees.** The cluster DP matched brute force over all labelled trees on 4..9 leaves, using random complement-symmetric "bad" predicates. There were 1980 tests, 839 positives and 0 mismatches [[4]].
- **Against shape × colouring enumeration.** The true level-1 and level-2 tables were compared over 41 pairs per level (u ≤ v, u + v ≤ 15), with 0 mismatches [[2]].
  - (3,4) is 1-safe and (3,3) is not.
  - (6,7) and (5,9) are 2-safe.
  - (6,6) and (5,8) are not.
- **Your checker.** Run on thresholds from the independent DP, it verified k = 2, 3, 4, 5 at n = 7, 14, 28, 61 [[8]]. It uses exact integer arithmetic. The independent DP used floating-point FFT sums thresholded at 0.5 [[5]], so FFT rounding is not a concern for the verified conclusions.

### 3.2 Least v such that (u, v) is m-safe

Each entry is the least v for a given u. The search used u ≤ 32 and v capped at 70. "None" means (u, 70) is not safe, not that no v works [[5]].

| Level | Thresholds (u → least v) |
|---|---|
| 1 | 2 none; 3 → 4; 4..32 → 3 [[5]] |
| 2 | ≤4 none; 5 → 9; 6 → 7; 7 → 6; 8 → 6; 9..32 → 5 [[5]] |
| 3 | ≤8 none; 9 → 22; 10 → 18; 11 → 16; 12 → 16; 13 → 14; 14 → 13; 15 → 13; 16 → 11; 17 → 11; 18..21 → 10; 22..32 → 9 [[5]] |
| 4 | ≤16 none; 17 → 53; 18 → 46; 19 → 43; 20 → 41; 21 → 38; 22 → 37; 23 → 35; 24 → 34; 25 → 31; 26 → 30; 27 → 28; 28 → 27; 29 → 27; 30 → 26; 31 → 25; 32 → 25 [[5]] |

The thresholds are symmetric, as they must be: 9 → 22 and 22 → 9, 13 → 14 and 14 → 13, 25 → 31 and 31 → 25, and so on.

### 3.3 Listed pairs

All listed pairs are safe at their level, and (a, b − 1) is not safe in each case [[5]]:
- (3,4);
- (5,9), (6,7);
- (10,18), (11,16), (13,14), (9,22);
- (20,41), (21,38), (22,37), (23,35), (24,34), (25,31).

### 3.4 Bounds

| k | n | First-tree check at n | at n − 1 |
|---|---|---|---|
| 2 | 7 | passes | fails (6) |
| 3 | 14 | passes | fails (13) |
| 4 | 28 | passes | fails (27) |
| 5 | 61 | passes | fails (60) |

Source: [[5]]. The first-tree check passes at n = 7, 8, 9, 10, 11 for k = 2, and likewise upward from the stated minimum for each k.

**Coverage of the balanced edge.** For k = 4 and n = 28, the balanced edge gives s ∈ 10..14. The pairs (10,18), (11,17), (12,16), (13,15), (14,14) each dominate a listed 3-safe pair, using the level-3 thresholds above. For k = 5 and n = 61, the balanced edge gives s ∈ 21..30. The pairs (21,40), (22,39), …, (30,31) each dominate a level-4 threshold pair. Every one of them also dominates (21,38) or (25,31), so the listed 4-safe pairs suffice. The pair (20,41) corresponds to s = 20, which the balanced-edge lemma does not require.

The DP's own first-tree check ranges over all trees, so it does not depend on the balanced-edge lemma. That lemma only shortlists which s values to examine.

### 3.5 The method is lossy at k = 2

The DP gives 7 for k = 2, but h(2) = 6 [[6]](https://arxiv.org/abs/2607.12778). Snir–Yuster likewise note that their Theorem 1.3 only gives h(2) ≤ 7 [[7]](https://arxiv.org/html/2602.23096). Exhaustive enumeration of labelled trees confirms the true value:
- n = 5: 30 ordered pairs of trees share no quartet.
- n = 6 and n = 7: no such pairs [[2]].

This is consistent with the fact that any two trees on n ≥ 6 leaves share a quartet split [[6]](https://arxiv.org/abs/2607.12778). The bounds 14, 28 and 61 are therefore upper bounds from a method known to lose at k = 2, not claimed optima.

## 4. Lower bounds

Snir–Yuster show h*(k) = 2^k + 2 for caterpillars [[9]](https://arxiv.org/abs/2602.23096). Caterpillars are a subfamily of all trees, so h(k) ≥ 2^k + 2. That gives h(4) ≥ 18 and h(5) ≥ 34. Three points follow:
- The paper omits the recursive construction on 2^k + 1 leaves. For k = 3 it prints permutations, one of which, 12345679, has a digit dropped [[9]](https://arxiv.org/abs/2602.23096).
- Your h(4) ≥ 22 would exceed 18.
- Your h(5) ≥ 28 is below 34, if the published claim is right.

For k = 3, Snir–Yuster give three trees on 10 leaves with no common quartet (Figure 4), so h(3) > 10 [[9]](https://arxiv.org/abs/2602.23096). Currie et al. state only 10 ≤ h(3) ≤ 14 [[6]](https://arxiv.org/abs/2607.12778). Your 13-leaf triple would give h(3) = 14 exactly. Neither it nor h(4) ≥ 22 appears in the sources, and neither was verified.

## 5. Literature and online (to 26 Oct 2026)

**Primary papers**
- Currie et al. state 10 ≤ h(3) ≤ 14. The upper bound is from (3.1) as ⌈2·14/27⌉ = 2. They also give the tower bound 8^{1/4}3^{k/4} ≤ h(k) ≤ tw_3(6(k−1)2^k + O(log k)) [[6]](https://arxiv.org/abs/2607.12778).
- The abstract of arXiv:2607.12778 cites "Discrete Appl. Math. 347" [[10]](https://arxiv.org/abs/2607.12778v2). The correct volume is 387, pp. 160–171, published 15 Jul 2026 [[11]](https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/).
- arXiv:2607.12778 has two versions only: v1 on 14 Jul 2026 and v2 on 17 Jul 2026 [[12]](https://arxiv.org/abs/2607.12778v1)[[10]](https://arxiv.org/abs/2607.12778v2).
- No sources give an exact h(3), numerical bounds for h(4) or h(5), or a 13-leaf triple.

**Searches**
- The arXiv API for "common quartet" returns one hit, Currie et al. [[13]](https://export.arxiv.org/api/query?search_query=all:%22common+quartet%22&max_results=20&sortBy=submittedDate&sortOrder=descending).
- "Simultaneous separation" AND trees returns only Snir–Yuster [[14]](https://export.arxiv.org/api/query?search_query=all:%22simultaneous+separation%22+AND+all:trees&max_results=20&sortBy=submittedDate&sortOrder=descending).
- A broader quartet/agreement-subtree query also returns only Currie et al. [[15]](https://export.arxiv.org/api/query?search_query=all:quartet+AND+all:%22phylogenetic+trees%22+AND+(all:%22agreement+subtree%22+OR+all:%22share+a+quartet%22+OR+all:%22common+quartets%22)&max_results=20&sortBy=submittedDate&sortOrder=descending).
- Semantic Scholar lists Currie et al. as the only citer of arXiv:2602.23096 [[16]](https://api.semanticscholar.org/graph/v1/paper/arXiv:2602.23096/citations?fields=title,year,externalIds&limit=50), and an empty citer list for arXiv:2607.12778 [[17]](https://api.semanticscholar.org/graph/v1/paper/arXiv:2607.12778/citations?fields=title,year,externalIds&limit=50).
- An OpenAlex query used a placeholder work ID, so it is uninformative [[18]](https://api.openalex.org/works?filter=cites:W7000000000&search=common%20quartet%20phylogenetic%20trees%20h(k)).
- The Pith machine reviews of Currie et al. mention only the tower and exponential bounds [[19]](https://pith.science/paper/2607.12778).
- Zenodo and GitHub hits were unrelated phylogenetics software [[20]](https://zenodo.org/records/22017696)[[21]](https://github.com/junkawahara/triquart)[[22]](https://github.com/molloy-lab/TREE-QMC). OEIS A000672 only counts trees [[3]](https://oeis.org/A000672).

**Limits.** No Google-Scholar-style citing list was accessible, and index lag is possible. The DAM full text was not read. Only the arXiv versions and the Haifa bibliographic record were seen [[11]](https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/).

## 6. Reasons the bounds could be wrong

No concrete error was found. The points checked:

- **Restriction coverage.** The DP ranges over every coloured tree with u′ red and v′ blue leaves, so it covers every possible T′|(X′ ∪ Y′). The brute-force comparisons enumerate all coloured trees up to 15 leaves, and agree [[2]].
- **Domination and shrinking.** Subsets preserve separation, and swapping the two sets is harmless, so safety is upward-closed. Levels 1 and 2 were confirmed upward-closed and symmetric numerically [[2]].
- **Floating point.** The FFT-based DP thresholds at 0.5. Your exact integer checker reproduces the same verdicts [[8]].
- **Soft spots:**
  - Levels 3 and 4 have no enumeration check. The smallest level-3 pair, (9,22), already has 31 leaves.
  - "None" entries are capped at v = 70.
  - Minimality at levels 3 and 4 relies on monotonicity in v, which was checked only at levels 1 and 2.

## 7. Synthesis

h(3) ≤ 14 now rests on an exhaustive finite check, consistent with the published analytic derivation. The same level-2 safety facts come out of two enumerations and the DP, which is a genuine three-way validation.

h(4) ≤ 28 and h(5) ≤ 61 are certified by an exact-integer checker over a procedure whose logic holds up. At the levels where brute force was feasible, that procedure matches enumeration.

The weakest links are the unverified lower bounds. Against your claimed h(3) = 14, the published lower bound is h(3) > 10 [[9]](https://arxiv.org/abs/2602.23096). The h(5) ≥ 28 claim should be reconciled with the published 2^k + 2 bound before any two-sided statement is made. The ranges that follow from the published lower bounds (h*(k) = 2^k + 2, plus h(3) > 10) and your upper bounds are:
- 11 ≤ h(3) ≤ 14.
- 18 ≤ h(4) ≤ 28. Your own h(4) ≥ 22 would tighten the lower end.
- 34 ≤ h(5) ≤ 61, if the published caterpillar construction holds.

The most useful independent check is the 13-leaf triple, since it alone supports h(3) = 14.

## Sources

[1] Analysis: Claim 1 re-implementation: shape enumeration (rooted->unrooted, min-over-edges canon) and DP over realisable clusters
[2] Analysis: Brute-force validation of level-1 and level-2 safe tables via shape x colouring enumeration (n<=15), and exhaustive h(2) sanity on labelled trees
[3] A000672 - OEIS - https://oeis.org/A000672
[4] Analysis: Validate cluster-DP (three-sum criterion) vs brute-force labelled trees; Claim 1 via DP
[5] Analysis: Recompute m-safe thresholds (levels 1-4), verify listed pairs and bounds h(k) for k=2..5
[6] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/abs/2607.12778
[7] 2602.23096 - https://arxiv.org/html/2602.23096
[8] Analysis: Run the user's pure-Python checker on independently computed thresholds (k=2..5, time-guarded) (computed from [5])
[9] 2602.23096 - https://arxiv.org/abs/2602.23096
[10] [2607.12778v2] On Agreement Subtrees in Multiple Phylogenetic Trees - https://arxiv.org/abs/2607.12778v2
[11] Simultaneous separation in bounded degree trees - University of Haifa - https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/
[12] [2607.12778v1] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/abs/2607.12778v1
[13] arXiv Query: search_query=all:"common quartet"&id_list=&start=0&max_results=20 - https://export.arxiv.org/api/query?search_query=all:%22common+quartet%22&max_results=20&sortBy=submittedDate&sortOrder=descending
[14] arXiv Query: search_query=all:"simultaneous separation" AND all:trees&id_list=&start=0&max_results=20 - https://export.arxiv.org/api/query?search_query=all:%22simultaneous+separation%22+AND+all:trees&max_results=20&sortBy=submittedDate&sortOrder=descending
[15] arXiv Query: search_query=all:quartet AND all:"phylogenetic trees" AND (all:"agreement subtree" OR all:"share a quartet" OR all:"common quartets")&id_list=&start=0&max_results=20 - https://export.arxiv.org/api/query?search_query=all:quartet+AND+all:%22phylogenetic+trees%22+AND+(all:%22agreement+subtree%22+OR+all:%22share+a+quartet%22+OR+all:%22common+quartets%22)&max_results=20&sortBy=submittedDate&sortOrder=descending
[16] JSON Data from api.semanticscholar.org - https://api.semanticscholar.org/graph/v1/paper/arXiv:2602.23096/citations?fields=title,year,externalIds&limit=50
[17] JSON Data from api.semanticscholar.org - https://api.semanticscholar.org/graph/v1/paper/arXiv:2607.12778/citations?fields=title,year,externalIds&limit=50
[18] JSON Data from api.openalex.org - https://api.openalex.org/works?filter=cites:W7000000000&search=common%20quartet%20phylogenetic%20trees%20h(k)
[19] On Agreement Subtrees in Multiple Phylogenetic Trees · Pith Review - https://pith.science/paper/2607.12778
[20] github.com/theiagen/public_health_bioinformatics/Snippy_Tree_PHB | Zenodo - https://zenodo.org/records/22017696
[21] GitHub - junkawahara/triquart · GitHub - https://github.com/junkawahara/triquart
[22] GitHub - molloy-lab/TREE-QMC: Quartet-based estimation of species trees, trees of blobs, and level-1 networks · GitHub - https://github.com/molloy-lab/TREE-QMC
