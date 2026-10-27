# Adversarial review of three claims on common quartets of three phylogenetic trees: h(3) = 14 and a Latin-square product bound

Task DR-059 | mode max | completed 2026-10-26T00:07:50.558Z | cost 16.425

# Adversarial review of three claims on common quartets of three phylogenetic trees: h(3) = 14 and a Latin-square product bound

## Executive summary

- **Claim 1 (h(3) ≥ 14) holds.** I recomputed all quartet splits of both triples. The 13-leaf triple has 0 common quartets out of 715, and the 12-leaf triple has 0 out of 495 [[1]]. Both σ-relations hold [[1]]. Independent annealing runs also found other quartet-free triples at n = 11, 12 and 13 [[2]].
- **Claim 2 is logically sound, but it is not an independent proof.** The Theorem is the Snir–Yuster proof of their Theorem 2.5 with exact integer counts [[3]](https://arxiv.org/html/2602.23096). Lemma C is a finite check of the one step they justify only asymptotically. Lemma C itself is only partly reproduced, for 4 of the 135 shapes. The SAT/DRAT run was not reproduced.
- **Claim 3 (product theorem) holds.** I found no gap in the case analysis. A direct check on 6 trees over 25 leaves and on 9 trees over 169 leaves found 0 common quartets [[4]].
- **Prior art.** No source I located determines h(3), exhibits a quartet-free triple on 11–13 leaves, or proves a product or Latin-square inequality for this problem. This is an absence of retrieved sources, not proof of absence.
- **Lower-bound baseline.** Snir–Yuster's Figure 4 already gives h(3) > 10, so h(3) ≥ 11 [[3]](https://arxiv.org/html/2602.23096). Currie et al. state only 10 ≤ h(3) [[5]](https://arxiv.org/html/2607.12778v2). Claim 1 improves the lower bound from 11, not from 10.

## 1. Citations

| Item | Details |
|---|---|
| Snir–Yuster, arXiv | arXiv:2602.23096, version v1 only, submitted 26 Feb 2026 [[6]](https://arxiv.org/abs/2602.23096v1) |
| Snir–Yuster, journal | Discrete Applied Mathematics 387, pp. 160–171, 15 Jul 2026, DOI 10.1016/j.dam.2026.02.042 [[7]](https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/) |
| Currie–Czabarka–Fischer–Simmons–Székely–Wicke | arXiv:2607.12778, v1 14 Jul 2026, v2 17 Jul 2026 (last revised) [[8]](https://arxiv.org/abs/2607.12778v2) |
| Volume-number typo | The Currie et al. abstract writes "Discrete Appl. Math. 347" [[8]](https://arxiv.org/abs/2607.12778v2). Their reference list and the publisher record give 387 [[5]](https://arxiv.org/html/2607.12778v2)[[7]](https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/). |
| Bandelt–Dress | Adv. Appl. Math. 7(3):309–343, 1986 [[3]](https://arxiv.org/html/2602.23096) |
| Alon–Maass | FOCS 1986, pp. 410–417, cited for the permutation analogue [[3]](https://arxiv.org/html/2602.23096) |
| Markin | DAM 285:612–620 (2020), DOI 10.1016/j.dam.2020.07.007 [[9]](https://markin-alex.github.io/documents/papers/amarkin-extremal-MAST-published.pdf); arXiv:1812.06951 [[10]](https://arxiv.org/pdf/1812.06951) |
| Steel–Székely | Appl. Math. Lett. 22(11):1778–1780 (2009), DOI 10.1016/j.aml.2009.06.019 [[11]](https://pmc.ncbi.nlm.nih.gov/articles/PMC2758697/) |
| Martin–Thatte | arXiv:1201.5168 [[12]](https://arxiv.org/pdf/1201.5168); DAM 161(13–14):1805–1817 (2013), DOI 10.1016/j.dam.2013.02.037 [[13]](https://www.sciencedirect.com/science/article/pii/S0166218X13001327) |

**Snir–Yuster text caveat.** The arXiv HTML renders Snir–Yuster's h\*(k) = 2^k + 2 as "2k + 2" [[3]](https://arxiv.org/html/2602.23096). It also drops digits from the example permutations [[3]](https://arxiv.org/html/2602.23096). The stated value h\*(3) = 10 matches 2^k + 2 [[3]](https://arxiv.org/html/2602.23096).

I read only arXiv v1 of Snir–Yuster. The published DAM text could not be compared with it.

**Lower-bound attribution.** Snir–Yuster state h(3) > h\*(3) = 10, shown by three unrooted trees on [[7]](https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/) with no common quartet [[3]](https://arxiv.org/html/2602.23096). That gives h(3) ≥ 11. Currie et al. write "10 ≤ h(3) ≤ 14" and attribute both bounds to Snir–Yuster [[5]](https://arxiv.org/html/2607.12778v2)[[14]](https://arxiv.org/abs/2607.12778). They derive the upper bound from g(3,n) ≥ 2n/27 via ⌈2·14/27⌉ = 2 [[5]](https://arxiv.org/html/2607.12778v2).

## 2. Claim 1: three trees on [[15]](https://www.researchgate.net/profile/Sagi-Snir) with no common quartet

I parsed each Newick string and checked that every internal vertex has degree 3 and that the leaves are exactly 1..13. I computed all quartet splits by the four-point condition with unit edge lengths [[1]].

| Check | Result |
|---|---|
| 13-leaf triple, quartets / common | 715 / 0 [[1]] |
| 12-leaf triple, quartets / common | 495 / 0 [[1]] |
| T2 = σ(T1) and T3 = σ²(T1) as labelled trees | both true [[1]] |
| Common quartets within each pair of the 13-leaf trees | 137 of 715 for each of the three pairs [[1]] |

Each pair shares quartets, as it must since h(2) = 6. The three-way intersection is empty.

Simulated annealing with leaf prune-and-regraft moves, run without the σ-symmetric structure, found other quartet-free triples. It found them at n = 11, 12 and, for two seeds, 13. I re-verified each in Python and found 0 common quartets [[2]]. At n = 14 the triple search never got below 2 common quartets in two seeds [[2]]. Annealing finds no 14-leaf triple, but it was not calibrated at n = 14, so this is weak evidence.

**Consequence.** By restriction, a quartet-free triple on 13 leaves gives h(3) > 13, so h(3) ≥ 14. The Claim 1 conclusion is rigorous for the explicit trees.

## 3. Claim 2: upper bound h(3) ≤ 14

### 3.1 Lemmas A and B

**Lemma A (centroid)** is correct. It is the classical (1/3, 2/3) property. Currie et al. cite Erdős–Faudree–Rousseau–Schelp (1988) as the earliest reference they know [[5]](https://arxiv.org/html/2607.12778v2). Snir–Yuster cite their own earlier Lemma 3.1 [[3]](https://arxiv.org/html/2602.23096). For 7 leaves it gives sides of at least ⌈7/3⌉ = 3.

**Lemma B** is correct as stated. I found no counterexample. A quartet xx'|yy' means some edge separates {x,x'} from {y,y'} [[3]](https://arxiv.org/html/2602.23096).

- (⇒) An edge separating X from Y separates every such pair of pairs.
- (⇐) In a binary tree, xx'|yy' holds exactly when the x–x' path and the y–y' path are vertex-disjoint. Span(X) is the union of the pairwise paths in X, and likewise for Y. So when |X|, |Y| ≥ 2, all those paths are pairwise disjoint and Span(X) and Span(Y) are disjoint subtrees. Any path from Span(X) to Span(Y) crosses the unique connecting path. Any edge of that path separates X from Y.
- The hypothesis |X|, |Y| ≥ 2 is needed. It makes each span a union of paths.
- A pair of trees can separate X from Y in the restriction to X∪Y while the edge it uses in the full tree still separates them, so passing to restrictions is safe.

### 3.2 The Theorem's case analysis

Take X, Y from Lemma C with |X|, |Y| ∈ {3,4} (passing to subsets keeps them separated). Take W, Z from Lemma A applied to T3 restricted to the 7 leaves of X∪Y. Define A = X∩Z, B = X∩W, C = Y∩Z, D = Y∩W.

The four sums |A|+|B|, |A|+|C|, |D|+|B|, |D|+|C| equal |X|, |Z|, |W|, |Y|, each at least 3. If min(|A|,|D|) ≤ 1 and min(|B|,|C|) ≤ 1, one of those sums is at most 2. That is a contradiction. So either A and D, or B and C, each have at least 2 elements. They are separated by all three trees, and Lemma B gives a common quartet.

**Relation to Snir–Yuster.** Their proof of Theorem 2.5 is the same argument. They take X, Y from their Lemma 2.6 and apply the 1/3–2/3 lemma to T3 on X∪Y. They define A, B, C, D as above and conclude by the same four-sums contradiction [[3]](https://arxiv.org/html/2602.23096). Your Theorem is therefore a finite-n version of their proof, not a new route.

### 3.3 Lemma C and the SAT relaxation

**Direction of the relaxation.** The direction is correct. Every real T2 satisfies the necessary constraints: one-hot quartet variables plus 5-point consistency. So if the relaxed formula is unsatisfiable, no real T2 exists with a (3,4)-separated pair against T1. Relabelling T1 to a representative shape is without loss of generality because T2 ranges over all labelled trees.

**What I could reproduce.** The SAT part could not be reproduced. No SAT solver or drat-trim was available [[16]]. Instead I ran an exhaustive search over labelled T2, built by leaf insertion. A partial tree is pruned as soon as a good pair appears. That pruning is valid because the cell counts only grow as leaves are added.

- The enumeration produced 135 shapes on 14 leaves [[17]].
- The search completed with zero survivors for 4 of the 135 shapes, indices 0 and 67 in one run [[18]] and 0, 1 and 10 in another [[19]].
- A parallel run over all shapes finished none within its limit [[4]].
- **Lemma C is therefore independently confirmed for only 4 of 135 shapes.** The other 131 rest on the SAT/DRAT run and on the analytic Snir–Yuster lemma.
- As a positive control, with T1 taken from the 13-leaf triple the search reached level 13 with 242,554 surviving partial trees. So the code does find trees with no good pair when they exist [[19]].
- Annealing on pairs reached 0 good edge pairs at n = 12 and 13. At n = 14 it stalled at a minimum of 1 in all four seeds [[2]]. That is a near-miss, not a counterexample.

**Consistency at n = 13.** None of the three pairs from the 13-leaf triple has a (3,4)-separated pair. Each pair does have a (2,2)-separated pair, which is a common quartet [[4]]. This matches your check and shows Lemma C fails at 13.

### 3.4 Question 5: is g(3,n) ≥ 2n/27 used correctly at n = 14?

**Arithmetic.** The use is arithmetically correct. g is integer-valued [[5]](https://arxiv.org/html/2607.12778v2). With n = 14, 2n/27 = 28/27 > 1, so g(3,14) ≥ 2. By Snir–Yuster's reading, g(3,n) ≥ 2 means a common quartet [[3]](https://arxiv.org/html/2602.23096). Snir–Yuster use the same rounding for two trees: "Theorem 1.3 only gives h(2) ≤ 7" [[3]](https://arxiv.org/html/2602.23096). At n = 13, 26/27 < 1 gives nothing, which is consistent with Claim 1.

**Rigour of the underlying bound.** The error-free claim is only sketched.

- Their Lemma 2.6 is proved with weights w(S) = |S|/n, and "all stated equalities and inequalities hold up to o_n(1)" [[4]][[3]](https://arxiv.org/html/2602.23096).
- The case analysis uses fixed real slack constants: +1/54 and −1/54 in the case splits [[3]](https://arxiv.org/html/2602.23096), and z = 1/108 with an ad hoc threshold 0.7 [[3]](https://arxiv.org/html/2602.23096).
- Section 4 then lists three sources of error and says that analogues without error terms exist. It states the integer version of Lemma 2.6 as: |X|, |Y| ≥ 4n/27 and |X∪Y| ≥ 4n/9 [[3]](https://arxiv.org/html/2602.23096). It does not redo the cases with integer counts.
- At n = 14 the quantities 14/54 ≈ 0.26 and 14/108 ≈ 0.13 are not negligible against integer counts.
- At n = 14, the error-free Lemma 2.6 asserts |X|, |Y| ≥ 3 and |X∪Y| ≥ 7. This is exactly Lemma C.

**Conclusion on Question 5.** The bound is used correctly given its statement. Its proof at n = 14 is not established in the paper. Currie et al. give no further argument for the h(3) ≤ 14 step [[5]](https://arxiv.org/html/2607.12778v2). So Lemma C, or an equivalent exact check, is the only finite justification for h(3) ≤ 14 I found. It is also the one component that is only partly reproduced.

## 4. Claim 3: product theorem

**Case analysis.** The partitions of a 4-set Q by the lines of each class are handled as follows.

- **1+1+1+1 in some class.** That class's family disagrees on those four lines. Quartet-freeness of the family guarantees a disagreeing tree.
- **4 in one class.** Then every other class has the four points on four distinct lines, because two points share at most one line overall.
- **3+1 in class c (p1,p2,p3 collinear, p4 off the line).**
  - In each other class the p_t lie on distinct lines.
  - Either p4 shares a line with exactly one p_t, which forces the split {p_t,p4}|rest, or the class is 1+1+1+1.
  - Two other classes cannot pair p4 with the same p_t, since that would put p_t and p4 on two common lines. So the splits differ.
- **Otherwise.** Each class has a collinear pair R_c. R_c is a block of the common split, because a pendant subtree is a cluster. The three R_c are distinct pairs, but a split has only two blocks.

I found no gap. Restricting quartet-free families to a common size n preserves quartet-freeness, so N(a+b+c) ≥ min(N(a),N(b),N(c))² follows.

**Computational check.** The check used a cyclic Latin square of order n and a chain-shaped pendant tree on each line [[4]].

- Six trees on 25 points: 0 common quartets out of 12,650. A control with identical families gave 555, so the checker detects failures [[4]].
- Nine trees on 169 points, built from the 13-leaf triple: 0 common quartets out of 32,795,126 [[4]].
- Your stated 121-leaf instance (from an 11-leaf triple) was not the one tested. The 169-leaf instance is stronger and implies h(9) ≥ 170.
- The 6-tree consequence h(6) ≥ 26 depends only on N(2) = 5, which is the 5-leaf case of Bandelt–Dress h(2) = 6.
- The step N(1) = 3 ⇒ N(3) ≥ 9 was not computed. It is superseded by Claim 1 in any case.

**Strength relative to the existing bound.** The existing exponential lower bound is h(k) ≥ 8^{1/4}·3^{k/4} [[5]](https://arxiv.org/html/2607.12778v2). Claim 3's bound N(3^j) ≥ 13^{2^{j−1}} is much better for small k and worse for large k.

| k | Claim 3: N(k) ≥ | Existing: h(k) ≥ (approx.) |
|---|---|---|
| 9 | 169 | 19.9 |
| 27 | 28,561 | about 2.8×10³ |
| 81 | about 8.2×10⁸ | about 7.7×10⁹ |

The crossover lies between k = 27 and k = 81. For non-powers of 3, monotonicity in k carries the bound across. Claim 3 matters for small k, not asymptotically.

**An untested observation.** The case analysis appears to need only at least 3 parallel classes. An affine plane of prime-power order q ≤ N(a) would give N((q+1)a) ≥ q², for example N(12) ≥ 25 from N(2) = 5. That would be weaker than the monotone consequence N(12) ≥ N(9) ≥ 169, so I did not pursue it.

## 5. Prior art (Questions 3 and 4)

**Current state of knowledge.**

- Currie et al. give 10 ≤ h(3) ≤ 14 and 8^{1/4}·3^{k/4} ≤ h(k) ≤ tw₃(…) [[5]](https://arxiv.org/html/2607.12778v2).
- h(2) = 6 is credited to Bandelt–Dress [[3]](https://arxiv.org/html/2602.23096)[[5]](https://arxiv.org/html/2607.12778v2).
- Currie et al. note h(k) = M_k(4), the size-4 case of their k-tree agreement-subtree function [[5]](https://arxiv.org/html/2607.12778v2).
- They remark that hypergraph Ramsey lower bounds "do not automatically carry over" to agreement subtrees [[5]](https://arxiv.org/html/2607.12778v2).
- Their paper has no product or Latin-square construction in the sections I read.

**Searches.**

- I located no source that determines h(3), exhibits quartet-free triples on 11–13 leaves, or proves a product, blow-up or Latin-square inequality for common quartets.
- I found no v3 of Currie et al. (the latest I saw is v2) and no later arXiv version of Snir–Yuster (only v1 [[6]](https://arxiv.org/abs/2602.23096v1)).
- I found no erratum to Section 4 of Snir–Yuster.
- The closest constructions are Snir–Yuster's path and caterpillar blow-ups of a single tree. They serve the upper-bound constructions for f(r,k) and g(k,n) and are neither products of families nor Latin-square based [[3]](https://arxiv.org/html/2602.23096).
- Pachter's arXiv:2608.03542 (4 Aug 2026) and Alon–Naves–Sudakov (SIAM J. Discrete Math. 30(2):718–735, arXiv:1505.04344) concern the quartet distance between two trees, not common quartets of several trees [[20]](https://arxiv.org/abs/2608.03542)[[21]](https://experts.umn.edu/en/publications/on-the-maximum-quartet-distance-between-phylogenetic-trees-2/)[[22]](https://arxiv.org/abs/1505.04344).
- Markin, Steel–Székely and Martin–Thatte concern two-tree extremal MAST bounds: Θ(log n) [[9]](https://markin-alex.github.io/documents/papers/amarkin-extremal-MAST-published.pdf), c·log log n via Ramsey [[11]](https://pmc.ncbi.nlm.nih.gov/articles/PMC2758697/), and Ω(√log n) with balanced trees and caterpillars [[12]](https://arxiv.org/pdf/1201.5168). Their abstracts show no Latin-square or product construction. I could not confirm the contents of every section of these papers.

The prior-art search was not exhaustive. These are searches that found nothing, not a proof that nothing exists.

## 6. Synthesis and recommendations

| Result | Status |
|---|---|
| h(3) ≥ 14 | Proven for the explicit 13-leaf triple; recomputation confirms 0 common quartets of 715 [[1]] |
| h(3) ≤ 14 | Supported. Exact finite proof depends on Lemma C, verified for 4 of 135 shapes by exhaustive search; the rest rests on the unreproduced SAT/DRAT run |
| h(3) = 14 | Well supported, but Lemma C should not be called independently verified |
| N(a+b+c) ≥ min N² | Proof checked; instances at 25 and 169 leaves confirmed [[4]] |
| h(6) ≥ 26, h(9) ≥ 170 | Confirmed computationally [[4]] |
| h(k) for k ≥ 4, exact | Not settled by anything found |

**Recommended steps.**

1. **Lemma C.** Publish the CNF files and DRAT proofs so a third party can run drat-trim on all 135 shapes. Add a positive control: the same encoding at n = 13 with T1 from the 13-leaf triple should be satisfiable. That would confirm the relaxation encoding is faithful.
2. **Framing of Claim 2.** Present it as a computer-assisted, integer version of Snir–Yuster's Theorem 2.5, with Lemma C replacing their asymptotic Lemma 2.6 at n = 14. Do not call it independent of them.
3. **Baselines.** State the improvement over h(3) ≥ 11, which is what Snir–Yuster's Figure 4 gives. Note that Currie et al. state 10.
4. **Published text.** Check Sections 4 and 5 against the DAM version, which was not available here for comparison.

## Sources

[1] Analysis: Verify claim 1: no common quartet in 13- and 12-leaf triples
[2] Analysis: Simulated-annealing search for counterexamples to Lemma C (pairs) and to h(3)<=14 (triples), calibrated at n=12,13
[3] 2602.23096 - https://arxiv.org/html/2602.23096
[4] Analysis: Lemma C exhaustive check (135 shapes, parallel) and Claim 3 blow-up verification, 13-leaf pair check
[5] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/html/2607.12778v2
[6] [2602.23096v1] Simultaneous separation in bounded degree trees - https://arxiv.org/abs/2602.23096v1
[7] Simultaneous separation in bounded degree trees - University of Haifa - https://cris.haifa.ac.il/en/publications/simultaneous-separation-in-bounded-degree-trees/
[8] [2607.12778v2] On Agreement Subtrees in Multiple Phylogenetic Trees - https://arxiv.org/abs/2607.12778v2
[9] On the extremal maximum agreement subtree problem - https://markin-alex.github.io/documents/papers/amarkin-extremal-MAST-published.pdf
[10] On the Extremal Maximum Agreement Subtree Problem - https://arxiv.org/pdf/1812.06951
[11] An improved bound on the Maximum Agreement Subtree problem - PMC - https://pmc.ncbi.nlm.nih.gov/articles/PMC2758697/
[12] The maximum agreement subtree problem - https://arxiv.org/pdf/1201.5168
[13] The maximum agreement subtree problem - ScienceDirect - https://www.sciencedirect.com/science/article/pii/S0166218X13001327
[14] On Agreement Subtrees in Multiple Pylogenetic Trees - https://arxiv.org/abs/2607.12778
[15] Sagi SNIR - https://www.researchgate.net/profile/Sagi-Snir
[16] Analysis: Check available SAT tools and (3,4)-separation for the 13-leaf pairs
[17] Analysis: Enumerate 14-leaf unrooted binary shapes; write C search for Lemma C; test feasibility
[18] Analysis: Exhaustive search for Lemma C counterexample with monotone pruning (feasibility test)
[19] Analysis: Lemma C search on as many of 135 shapes as budget allows (job queue) + N=13 sanity that the search finds survivors
[20] The maximum quartet distance between phylogenetic trees - https://arxiv.org/abs/2608.03542
[21] On the maximum quartet distance between phylogenetic trees - Experts@Minnesota - https://experts.umn.edu/en/publications/on-the-maximum-quartet-distance-between-phylogenetic-trees-2/
[22] [1505.04344] On the maximum quartet distance between phylogenetic trees - https://arxiv.org/abs/1505.04344
