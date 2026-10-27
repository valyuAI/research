# Check of the claimed proof of the Mir–Rotger–Rosselló conjecture, with prior-art status

Task DR-082 | mode heavy | completed 2026-10-26T09:32:07.523Z | cost 3.125

# Check of the claimed proof of the Mir–Rotger–Rosselló conjecture, with prior-art status

## Executive summary

**The argument is correct for the class of f it covers.** It shows that if f(2), f(3), f(4) lie in a common group γ·Z (in particular if they are rational or natural numbers), then δ_f is not injective on fully symmetric trees. By Lemma 10 this makes C_{D,f} unsound, so the conjecture holds for f taking values in the natural numbers.

- **Formula, Lemma 10 and counting.** The f-size formula you use is Example 3 of the original paper [[1]](https://arxiv.org/pdf/1805.01329). The direction of Lemma 10 you invoke is the paper's own "only if" proof [[1]](https://arxiv.org/pdf/1805.01329). The counting step goes through, and the range bound 2M·24^m is valid.
- **Leaf term.** f(0) can be dropped from the hypotheses entirely, because every word yields a tree with the same number of leaves (see §1.3).
- **Open status.** In the sources I could read, the conjecture is still listed as open: the Fischer–Herbst–Kersting–Kühn–Wicke survey (arXiv:2109.12281v2, revised 9 Nov 2023) calls finding further sound f an "open problem" and restates the conjecture [[2]](https://arxiv.org/abs/2109.12281). I found no later paper, thesis, website page or package document that proves, disproves or discusses it.
- **Priority.** The reasoning itself does not appear in any source I could read. That does not establish that it is new.
- **Rank-2 weights.** Nothing in the sources addresses injectivity of f-sizes for values in a rank-2 group such as Z + Z√2. Your counting argument does not extend to that case (§3). The paper does give a collision for the weight (√2)^n, whose values lie in such a group.

## 1. Is the argument correct?

### 1.1 The f-size formula and the tree encoding

The paper's Example 3 states δ_f(FS_{n1,…,nk}) = n1⋯nk·f(0) + n1⋯n_{k−1}·f(nk) + ⋯ + n1·f(n2) + f(n1) [[1]](https://arxiv.org/pdf/1805.01329). With w = (k_1,…,k_h) this is your formula Σ_{i}(k_1⋯k_{i−1})f(k_i) + (k_1⋯k_h)f(0). The leaf term is real: the paper's own example of the leaf-count size takes f(0)=1 and f(n)=0 for n>0 [[1]](https://arxiv.org/pdf/1805.01329).

Fully symmetric trees correspond to ordered factorizations with all factors ≥ 2. The paper states that every FS_{n1,…,nk} is fully symmetric, every fully symmetric tree is isomorphic to one of them, and the number with n leaves is the number of ordered factorizations of n [[1]](https://arxiv.org/pdf/1805.01329). So distinct level sequences give non-isomorphic trees, as the argument needs.

### 1.2 Use of Lemma 10

Lemma 10 says C_{D,f} is sound iff δ_f(T1) ≠ δ_f(T2) for every pair of different fully symmetric trees [[1]](https://arxiv.org/pdf/1805.01329). Its "only if" proof is the step you need. If two non-isomorphic fully symmetric trees have equal f-size, then T = T1⋆T2 is not fully symmetric, yet C_{D,f}(T) = C_{D,f}(T1) + C_{D,f}(T2) + D(δ_f(T1), δ_f(T2)) = 0 [[1]](https://arxiv.org/pdf/1805.01329). The first two terms vanish because fully symmetric trees have index 0 [[1]](https://arxiv.org/pdf/1805.01329). The third vanishes because a dissimilarity is zero on equal arguments [[1]](https://arxiv.org/pdf/1805.01329). Soundness is a property of f alone and holds for every D [[1]](https://arxiv.org/pdf/1805.01329), so one collision refutes it for all D simultaneously. Use of the lemma is correct.

### 1.3 The counting step

- **Words.** Words with m letters each of 2, 3, 4 number (3m)!/(m!)^3 and all have product 2^m·3^m·4^m = 24^m. Each word gives a tree with exactly 24^m leaves.
- **Range.** With a_k = f(k)/γ and M the maximum of these values, the internal part of δ_f/γ is at most M·(1 + p_1 + … + p_{3m−1}), where p_j are the prefix products. The paper's Lemma 15 states 1 + n1 + n1n2 + ⋯ + n1⋯n_{k−1} < n1⋯nk when all n_i ≥ 2 [[1]](https://arxiv.org/pdf/1805.01329), so this sum is below 24^m. Adding the leaf term at most M·24^m gives a total in [0, 2M·24^m]. So your bound is valid as stated, and the prefix-product inequality p_i ≥ 2p_{i−1} is not even needed beyond Lemma 15.
- **Lower bound on the count.** The multinomial coefficient is maximal when the three parts are equal [[3]](https://djalil.chafai.net/blog/2015/08/29/about-the-central-multinomial-coefficient/). The 27^m words of length 3m over a 3-letter alphabet are split among at most (3m+1)(3m+2)/2 ≤ (3m+1)^2 type-classes. The central class therefore has at least 27^m/(3m+1)^2 words, matching your inequality (this uses the standard identity that the coefficients sum to 3^{3m}).
- **Pigeonhole.** (27/24)^m = 1.125^m beats the polynomial factor (3m+1)^2 times the constant 2M+1, so the count exceeds 2M·24^m + 1 for large m. Two distinct words then give equal δ_f. The bound is crude and only guarantees existence for large m; actual collisions appear much earlier (§1.5).

**Refinement: f(0) is not needed.** All words give trees with the same leaf count 24^m, so the term 24^m·f(0) is identical across words. Two words collide iff their internal sums Σ(k_1⋯k_{i−1})f(k_i) coincide. The hypothesis can therefore be weakened to "f(2), f(3), f(4) lie in a common γ·Z", with f(0) any real. The argument also does not depend on the sign of the values, since |a| ≤ M gives a symmetric finite range.

### 1.4 The domain of f

The sources are inconsistent about the domain of f, and this affects how the theorem should be stated:

- The arXiv version writes f: N → R_{>0} [[1]](https://arxiv.org/pdf/1805.01329); the PLoS abstract and the bioRxiv text write f: N → R_{≥0} [[4]](https://pmc.ncbi.nlm.nih.gov/articles/PMC6155497/)[[5]](https://www.biorxiv.org/content/10.1101/313908).
- The same arXiv text uses f(0) and f(n)=0 for n>0 in its examples [[1]](https://arxiv.org/pdf/1805.01329), so its N must include 0, and "R_{>0}" is not meant literally there.
- The survey and the treebalance fact sheet state f: N_{≥0} → R_{≥0} [[2]](https://arxiv.org/abs/2109.12281)[[6]](https://treebalance.wordpress.com/colless-like-indices/).
- The conjecture itself is stated as "no function f: N → N taking values in the set of natural numbers" in the PLoS conclusions as indexed by PubMed Central [[7]](https://pubmed.ncbi.nlm.nih.gov/PMC6155497), in the bioRxiv preprint ("no function f: ℕ → ℕ") [[8]](https://www.biorxiv.org/content/10.1101/313908v1.full), and in the survey [[2]](https://arxiv.org/abs/2109.12281).

Since the formula needs f(0) [[1]](https://arxiv.org/pdf/1805.01329), the natural reading is f: N_{≥0} → N. Your proof covers that reading and, by §1.3, much more. It is not a full resolution of "all f", since sound f exist (e^n, ln(n+e)), but those take irrational values that do not lie in one γ·Z.

### 1.5 The small collisions

I recomputed each from the Example 3 formula [[1]](https://arxiv.org/pdf/1805.01329):

| f | Tree 1 | Tree 2 | δ_f |
|---|---|---|---|
| n+1 (f(0)=1, f(2)=3, f(6)=7) | FS_{2,2}: 4·1 + 2·3 + 3 | FS_6: 6·1 + 7 | 13 = 13 |
| 2^n (f(0)=1, f(2)=4, f(3)=8) | FS_{2,3}: 6·1 + 2·8 + 4 | FS_{3,2}: 6·1 + 3·4 + 8 | 26 = 26 |
| n!+1 (f(0)=2, f(2)=3, f(3)=7, f(4)=25) | FS_{2,2,2,2}: 16·2 + 8·3 + 4·3 + 2·3 + 3 | FS_{4,3}: 12·2 + 4·7 + 25 | 77 = 77 |

The 2^n collision, δ_{2^n}(FS_{2,3}) = δ_{2^n}(FS_{3,2}) = 26, appears in the original paper [[1]](https://arxiv.org/pdf/1805.01329). The paper's own non-soundness examples (quadratic f, f = n^d, and logarithms) are also collisions of this type [[1]](https://arxiv.org/pdf/1805.01329).

### 1.6 Consistency with the known sound functions

For f(n) = e^n, the values f(2) = e², f(3) = e³, f(4) = e⁴ have ratio e, which is irrational, so they do not lie in a common γ·Z. The proof is therefore consistent with Proposition 16, which proves soundness via the transcendence of e [[1]](https://arxiv.org/pdf/1805.01329).

## 2. Prior art and later work (2018–2026)

**Bottom line:** I found no source that proves, disproves or discusses the conjecture after its publication. The sources I could read are limited to passages and abstracts, so this is not an exhaustive negative.

| Source | What it says | Bearing on the conjecture |
|---|---|---|
| Mir, Rotger, Rosselló, PLoS ONE 13(9):e0203401, DOI 10.1371/journal.pone.0203401 [[9]](https://www.researchgate.net/publication/327874459_Sound_Colless-like_balance_indices_for_multifurcating_trees); arXiv:1805.01329 [[1]](https://arxiv.org/pdf/1805.01329) | "Our conjecture is that there is no function f: N → N taking values in the set of natural numbers that satisfies this property." [[7]](https://pubmed.ncbi.nlm.nih.gov/PMC6155497) | Origin of the conjecture |
| bioRxiv 10.1101/313908 (preprint, 2018-05-04) | "Our conjecture is that no function f: ℕ → ℕ satisfies this property." [[8]](https://www.biorxiv.org/content/10.1101/313908v1.full) | Same conjecture, earlier wording |
| Fischer, Herbst, Kersting, Kühn, Wicke, arXiv:2109.12281, v1 submitted 25 Sep 2021, v2 last revised 9 Nov 2023, "superseded by the SpringerNature book" ISBN 978-3-031-39799-8 [[2]](https://arxiv.org/abs/2109.12281) | "it remains an open problem to find further functions f such that C_{D,f} is sound. An interesting conjecture posed by Mir et al. [[10]](https://pith.science/paper/2506.08614) states that there is no function f: N → N taking values in the set of natural numbers that yields a sound Colless-like index." (§9.7) [[2]](https://arxiv.org/abs/2109.12281) | Lists it as open |
| Springer book, DOI 10.1007/978-3-031-39800-1, 404 pp., published 31 Oct 2023 [[11]](https://researchwith.njit.edu/en/publications/tree-balance-indices-a-comprehensive-survey/) | Only metadata and abstract seen | Section 9.7 of the book itself was not readable; the "open" status rests on the arXiv v2 text |
| treebalance.wordpress.com, Colless-like fact sheet | States the problem: "A problem posed in (Mir et al., 2018, Definition 9) is to find functions f: ℕ≥0 → ℝ≥0 such that C_{D,f} is sound (for all dissimilarities D)." It lists e^n and ln(n+e) as the two known choices [[6]](https://treebalance.wordpress.com/colless-like-indices/) | The natural-number conjecture is not mentioned anywhere on the page [[6]](https://treebalance.wordpress.com/colless-like-indices/) |
| R package `treebalance` v1.2.2 (CRAN, published 2026-10-01), DOI 10.32614/CRAN.package.treebalance | Accompanies the 2023 book; offers the Colless-like family and a `collesslikeI` function [[12]](https://cran.r-project.org/package=treebalance)[[13]](https://cran.r-project.org/web/packages/treebalance/treebalance.pdf) | The package description does not mention the conjecture; the `collesslikeI` help page text was not available |
| R package `CollessLike` (Rotger) | Offers f.size options "ln" (ln(n+e)) and "exp" (e^n) [[14]](https://rdrr.io/cran/CollessLike/man/colless.like.index.html) | No conjecture discussed |
| Rotger, PhD thesis, UIB, "New balance indices and metrics for phylogenetic trees" (TDX handle 10803/671417, 282 pp.) [[15]](https://www.tdx.cat/handle/10803/671417) | Abstract calls the Colless-like indices "the first sound extension to multifurcating trees of the Colless index" [[15]](https://www.tdx.cat/handle/10803/671417). Chapter 4 has §4.3 "Sound Colless-like indices" [[16]](https://www.tdx.cat/bitstream/handle/10803/671417/tlrg1de1.pdf?sequence=1&isAllowed=y). The thesis states that the Chapter 4 results are included in the PLoS ONE paper [[16]](https://www.tdx.cat/bitstream/handle/10803/671417/tlrg1de1.pdf?sequence=1&isAllowed=y) | The only "conjecture" found in the retrievable text concerns the order of the variance of the total cophenetic index [[16]](https://www.tdx.cat/bitstream/handle/10803/671417/tlrg1de1.pdf?sequence=1&isAllowed=y). The text of §4.3 itself was not retrievable (the stored text stops before Chapter 4) |
| Coronado, Fischer, Herbst, Rosselló, Wicke, J. Math. Biol. 80(7):1993–2054, DOI 10.1007/s00285-020-01488-9; arXiv:1907.05064 [[17]](https://www.semanticscholar.org/paper/On-the-minimum-value-of-the-Colless-index-and-the-Coronado-Fischer/eb162769c667e73b13d9556bbb20f3ad7b538bda)[[18]](https://arxiv.org/pdf/1907.05064) | Minimum Colless index for bifurcating trees | Different topic |
| Kersting, Wicke, Fischer, "Tree balance in phylogenetic models", arXiv:2406.05185 [[19]](https://arxiv.org/html/2406.05185v2); Phil. Trans. R. Soc. B 380(1919), DOI 10.1098/rstb.2023.0303 [[20]](https://pith.science/paper/2509.04995) | Uses the Colless-like index for multifurcating trees [[21]](https://www.researchgate.net/figure/Each-node-in-this-asymmetric-tree-has-all-its-children-with-the-same-number-of-descendant_fig1_327874459) | The retrieved passages do not address soundness or the conjecture |
| Other works citing or using Colless-like indices or related metaconcepts: Lemant et al., Syst. Biol. 71(5):1210, DOI 10.1093/sysbio/syac027 [[22]](https://academic.oup.com/sysbio/article/71/5/1210/6567363); Fischer et al., arXiv:2506.08614 [[23]](https://arxiv.org/abs/2506.08614); arXiv:2601.15219 [[24]](https://arxiv.org/abs/2601.15219); arXiv:2509.04995 [[25]](https://arxiv.org/abs/2509.04995) | The retrieved passages concern other indices or the Colless-like definition | No retrieved passage mentions the conjecture |

Notes on this table:

- **Thesis dates.** TDX gives a defence date of 2019-07-31 [[15]](https://www.tdx.cat/handle/10803/671417), while a University of La Rioja record lists 13 July 2020 [[26]](https://investigacion.unirioja.es/documentos/6087618b84b60544a15d3ac3). This is a metadata discrepancy and does not affect the mathematics.
- **Open-status caveat.** The "2023 Springer survey lists it as open" statement is verified only through the arXiv v2 text of the same survey [[2]](https://arxiv.org/abs/2109.12281), not through a directly read passage of the book.
- **Limits of the negative result.** I found no source (arXiv, journal, thesis, website or package) stating your argument. The retrieved snippets of later papers do not rule out a passing mention elsewhere in their full text.

## 3. Known results on which f give injective f-sizes

**Published sound examples.** All come from the original paper and rely on transcendence:

- f(n) = e^n (Proposition 16) and f(n) = ln(n+e) (Proposition 17) [[1]](https://arxiv.org/pdf/1805.01329).
- Every f(n) = r^n with r transcendental, and every f(n) = log_r(n+r) with r > 1 transcendental [[1]](https://arxiv.org/pdf/1805.01329).
- The proofs convert an equality of f-sizes into an identity of polynomials in Z[x] using transcendence, then compare the leading coefficients via Lemmas 14 and 15 [[1]](https://arxiv.org/pdf/1805.01329).

**Published non-sound examples.**

- Quadratic f, with δ_f(FS_{2,2,2,7}) = δ_f(FS_{14,4}) = 420a + 70b + 71c [[1]](https://arxiv.org/pdf/1805.01329).
- f(n) = n^d for every d > 0 [[1]](https://arxiv.org/pdf/1805.01329).
- f(n) = log_a(n) with f(0)=0 and f(n) = log_a(n+1) [[1]](https://arxiv.org/pdf/1805.01329).
- Non-transcendental bases: "if r is not transcendental, then C_{D,r^n} need not be sound", with δ_{2^n}(FS_{2,3}) = δ_{2^n}(FS_{3,2}) = 26 and δ_{(√2)^n}(FS_{8,10}) = δ_{(√2)^n}(FS_{12,8}) = 352 [[1]](https://arxiv.org/pdf/1805.01329). For log_2(n+2): δ(FS_{9,6}) = δ(FS_{20,2}) = 81 + log_2(11) [[1]](https://arxiv.org/pdf/1805.01329).

**Rank-2 and general groups.** No source gives a characterization of injective weight functions, nor any result for weights with values in Z + Z√2.

- The weight (√2)^n takes the values 1, √2, 2, 2√2, … in Z + Z√2, and it has a collision at 352 [[1]](https://arxiv.org/pdf/1805.01329). So rank-2 values can collide, but this is one example, not a theorem.
- Your counting argument does not extend to rank 2. If δ_f lies in Zγ₁ + Zγ₂ with coefficients bounded by C·24^m, the number of candidate values is about (C·24^m)² ≈ C²·576^m, which exceeds the 27^m words used. This is my estimate, not a published result.
- So for rank-2 groups, and for weights with Q-linearly independent values, injectivity is **unestablished** here. The conjecture's natural-number case being settled by rank-1 counting does not say anything about the rank-2 case.

## Synthesis and recommended actions

1. **State the theorem precisely.** For any f with f(2), f(3), f(4) in one group γ·Z (γ real, in particular all rational), δ_f is not injective on fully symmetric trees. Hence C_{D,f} is unsound for every dissimilarity D. This includes every f: N_{≥0} → N, which is the conjecture. Mention that f(0) is irrelevant (§1.3).
2. **Fix the presentation, not the logic.** Cite Lemma 15 for the bound 2M·24^m, cite the maximality of the central multinomial coefficient for the 27^m/(3m+1)^2 bound, and state the domain convention explicitly (§1.4).
3. **Position it as open-but-resolved.** The most recent source I could read treats the conjecture as open [[2]](https://arxiv.org/abs/2109.12281), so a short note or arXiv submission would be the first source I could find to settle it. The sources do not let me assert that it has never been proved elsewhere.
4. **Flag the rank-2 problem as open.** Whether any f with Q-rank ≥ 2 values beyond e^n and ln(n+e) (for example transcendental-base weights with other structure) gives injectivity is not covered by this argument or by any source I found.

## Sources

[1] Sound Colless-like balance indices for multifurcating trees - https://arxiv.org/pdf/1805.01329
[2] Tree balance indices: a comprehensive survey - https://arxiv.org/abs/2109.12281
[3] About the central multinomial coefficient – Libres pensées d'un mathématicien ordinaire - https://djalil.chafai.net/blog/2015/08/29/about-the-central-multinomial-coefficient/
[4] Sound Colless-like balance indices for multifurcating trees Sound Colless-like balance indices for multifurcating trees - https://pmc.ncbi.nlm.nih.gov/articles/PMC6155497/
[5] Sound colless-like balance indices for multifurcating trees - https://www.biorxiv.org/content/10.1101/313908
[6] Colless-like indices – TREE BALANCE - https://treebalance.wordpress.com/colless-like-indices/
[7] Sound Colless-like balance indices for multifurcating trees Sound Colless-like balance indices for multifurcating trees - https://pubmed.ncbi.nlm.nih.gov/PMC6155497
[8] Sound colless-like balance indices for multifurcating trees | bioRxiv - https://www.biorxiv.org/content/10.1101/313908v1.full
[9] (PDF) Sound Colless-like balance indices for multifurcating trees - https://www.researchgate.net/publication/327874459_Sound_Colless-like_balance_indices_for_multifurcating_trees
[10] Metaconcepts of rooted tree balance · Pith Review - https://pith.science/paper/2506.08614
[11] Tree balance indices: A comprehensive survey - New Jersey Institute of Technology - https://researchwith.njit.edu/en/publications/tree-balance-indices-a-comprehensive-survey/
[12] CRAN: Package treebalance - https://cran.r-project.org/package=treebalance
[13] treebalance: Computation of Tree (Im)Balance Indices - https://cran.r-project.org/web/packages/treebalance/treebalance.pdf
[14] colless.like.index: Computes the Colless-like balance index of a phylogenetic... in CollessLike: Distribution and Percentile of Sackin, Cophenetic and Colless-Like Balance Indices of Phylogenetic Trees - https://rdrr.io/cran/CollessLike/man/colless.like.index.html
[15] New balance indices and metrics for phylogenetic trees - TDX (Tesis Doctorals en Xarxa) - https://www.tdx.cat/handle/10803/671417
[16] DOCTORAL THESIS - https://www.tdx.cat/bitstream/handle/10803/671417/tlrg1de1.pdf?sequence=1&isAllowed=y
[17] [PDF] On the minimum value of the Colless index and the bifurcating trees that achieve it - https://www.semanticscholar.org/paper/On-the-minimum-value-of-the-Colless-index-and-the-Coronado-Fischer/eb162769c667e73b13d9556bbb20f3ad7b538bda
[18] On the minimum value of the Colless index and the bifurcating trees that achieve it - https://arxiv.org/pdf/1907.05064
[19] Tree balance in phylogenetic models - https://arxiv.org/html/2406.05185v2
[20] Revealing the building blocks of tree balance: fundamental units of the Sackin and Colless Indices · Pith - https://pith.science/paper/2509.04995
[21] Each node in this asymmetric tree has all its children with the same... - https://www.researchgate.net/figure/Each-node-in-this-asymmetric-tree-has-all-its-children-with-the-same-number-of-descendant_fig1_327874459
[22] Robust, Universal Tree Balance Indices - https://academic.oup.com/sysbio/article/71/5/1210/6567363
[23] Metaconcepts of rooted tree balance - https://arxiv.org/abs/2506.08614
[24] A height-based metaconcept for rooted tree balance and its implications for the $B_1$ index - https://arxiv.org/abs/2601.15219
[25] Revealing the building blocks of tree balance: fundamental units of the Sackin and Colless Indices - https://arxiv.org/abs/2509.04995
[26] New balance indices and metrics for phylogenetic trees | Documents - Universidad de La Rioja - https://investigacion.unirioja.es/documentos/6087618b84b60544a15d3ac3
