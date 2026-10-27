# Three phylogenetic trees on fourteen leaves always share a quartet

Snir and Yuster (arXiv:2602.23096, Discrete Applied Mathematics 387 (2026) 160-171, Section 5) asked for h(k): the least n such that any k unrooted binary phylogenetic trees on the same n leaves resolve some 4-set identically (a common quartet). Known before: h(2) = 6 (Bandelt and Dress 1986); 11 <= h(3) <= 14 (Snir-Yuster Figure 4 and Theorem 1.3, the upper bound as observed by Currie, Czabarka, Fischer, Simmons, Szekely and Wicke, arXiv:2607.12778v2, and resting on an error-free small-n form that Snir and Yuster only sketch); for general k an upper bound that is a four-fold iterated exponential (Currie et al., Theorem 5). Snir and Yuster also state h*(k) = 2^k + 2 for caterpillars (construction omitted), which gives h(k) >= 2^k + 2; Currie et al. state only 8^(1/4) 3^(k/4) <= h(k).

## Claims

| Claim | Status | Evidence |
|---|---|---|
| h(3) >= 14: T, sigma T, sigma^2 T on 13 leaves have no common quartet, sigma = (1 2 3)(4 5 6)(7 8 9)(10 11 12) | theorem (finite check) | `verification/sym_triple.py`, `verification/check_family.py` (standard library); recomputed independently in the adversarial review `phylo-h3-review` |
| h(3) <= 14: a balanced edge X\|Y of the first tree (both sides >= 5), then Lemma 3.4 (for every such split of [14] and every tree, some edge leaves separated sets of sizes >= 3 and >= 4), then a balanced edge of the third tree | computer-assisted theorem (exhaustive enumeration, standard library, about a minute) | `verification/bipartition_check.py`: 0 failures over 135 shapes x all 5-, 6-, 7-subsets (1,138,995 cases); sharp: 891 failures on 13 leaves with \|X\| = 5 |
| Lemma 3.3: any two trees on [14] have separated leaf sets of sizes 3 and 4 (implied by Lemma 3.4; independent second proof of h(3) <= 14) | computer-assisted theorem | 135 SAT instances, all UNSAT; CaDiCaL 3.0.1 DRAT proofs all verified by DRAT-trim; CNF SHA-256 hashes recorded; a second encoding sharing no code, solved by Kissat 4.0.4: all 135 UNSAT (`verification/results/indep_twotree_n14_kissat.json`, no proofs); positive control at 13 leaves is SAT |
| h(3) = 14 | theorem | rows above |
| h(k) <= floor(3 beta^(k-1)) + 1 for all k >= 1, beta=(1+sqrt(13))/2 (4, 7, 16, 37, 85, 195 for k=1..6) | theorem: cut balanced on the larger set Y, keep the better diagonal and track min(\|X\|\|Y\|, 2\|X\|^2, 2\|Y\|^2); every step retains at least c=(7-sqrt(13))/18 | Theorem 2.7; exact sharp two-case proof in Lemma 2.6, Lean theorems `potential_step_sharp` and `potential_step_sharp_witness`, fresh max review `phylo-sharp-potential-review`; `verification/iterate_check.py` checks exact thresholds, the sharp inequality and separation at every step on random families |
| h(4) <= 28, h(5) <= 61, h(6) <= 125 (and again h(3) <= 14) | computer-assisted theorem: the one-pair strategy optimised exactly by dynamic programming over colour counts of subtrees (Lemma 2.8, Theorem 2.9) | `verification/game/`: numpy generator and a separately written standard-library checker that re-derives every claim used (31 evaluations for k <= 6); the recursion agrees with brute-force enumeration of all trees on <= 8 leaves on 1075 random instances, and with Lemma 3.4 at level two |
| h(k) >= 2^k + 2: explicit k caterpillars on 2^k + 1 leaves without a common quartet (Snir and Yuster state this and list the k = 3 case; we give the construction and proof) | theorem (hand proof by induction) | Proposition 4.1; `verification/caterpillar_family.py` checks k <= 6 |
| h(4) >= 23: four trees on 22 leaves without a common quartet (T, sigma T, sigma^2 T, sigma^3 T with sigma of cycle type 4^5 2) | explicit construction | `verification/families/quad22_k4.nwk`, checked by `check_family.py` |

So 2^k + 2 <= h(k) <= floor(3 ((1+sqrt(13))/2)^(k-1)) + 1, 23 <= h(4) <= 28, 34 <= h(5) <= 61, 66 <= h(6) <= 125.

What is new, as far as the searches show: the 13-leaf triple (closing 11 <= h(3) <= 14 at 14); an elementary exhaustive proof of the 14-leaf upper bound (plus a DRAT-certified SAT confirmation), replacing the sketched error-free step of Snir and Yuster; the first single-exponential upper bound for h(k), with base (1+sqrt(13))/2, approximately 2.3028 against the lower base 2; the exact one-pair bounds for k = 4, 5, 6; and the 22-leaf four-tree family. The ingredients of the upper bounds (balanced edge, pigeonhole on a 2x2 grid, restricting to X u Y and keeping the better diagonal) are Snir and Yuster's; the cut balanced on the larger set, the potential and the dynamic programme are new. The caterpillar lower bound is Snir and Yuster's statement with our proof. The exact best factor for this real-variable potential inequality is c=(7-sqrt(13))/18, proved by a two-case argument and an equality example. This does not prove that the base is optimal for all tree strategies or potentials. Equal weights on X and Y give 4/25 (base 5/2); the suggested value 3/sqrt(2), about 2.12, for a broader one-pair game remains numerical and unproved.

Superseded and removed during review: a lower bound h(k) >= (3/4 - o(1))(2 * 3^k)^(1/3) by alteration and a Latin-square product N(a+b+c) >= min N^2 (both correct but weaker than the caterpillar bound 2^k + 2 for every k), a five-tree family on 27 leaves (weaker than 33), and the upper bounds 2 * 3^(k-1) + 1 (kept as Proposition 2.3 for comparison) and (3^k + 1)/2 (conditional on the error-free Snir-Yuster theorem). The retired files are kept outside this folder.

## Confidence

- Correctness: very high for h(3) = 14 (explicit lower-bound family recomputed by a reviewer; the upper bound by a one-minute exhaustive enumeration and, independently, by DRAT-certified SAT plus a second encoding). High for Theorem 2.7 (exact two-case hand proof and max review `phylo-sharp-potential-review`, which found no gap in the sharp lemma or its iteration; an earlier equal-weight version with factor 4/25 was checked by the max-mode review `phylo-hk52-review`, which found no error; the 3/16 version was checked on a rational grid and by executing the proof with exact rationals on random families; the final max review `phylo-final-review` checked the new 3/16 argument and the 22-leaf witness without finding a mathematical error). High for Theorem 2.9 (two separately written implementations of a short recursion, validated against brute force; the max-mode review `phylo-game-review` re-implemented the recursion and the 14-leaf enumeration independently and reproduced every threshold and bound, finding no logical error). High for Proposition 4.1 (short induction, checked by computer for k <= 6).
- Originality: moderate-high. DeepResearch audits (tasks below) found no determination of h(3), no 11-13 leaf construction, no exponential upper bound for h(k) and no bound on h(4) below towers. Searches are not exhaustive.

## Closest prior work

- S. Snir and R. Yuster, Simultaneous separation in bounded degree trees, arXiv:2602.23096v1; DAM 387 (2026) 160-171, doi:10.1016/j.dam.2026.02.042. Defines h(k), states h*(k) = 2^k + 2, shows h(3) > 10, proves g(3,n) >= 2n/27.
- B. Currie, E. Czabarka, M. Fischer, H. Simmons, L. Szekely, K. Wicke, On agreement subtrees in multiple phylogenetic trees, arXiv:2607.12778v2 (17 July 2026). States 10 <= h(3) <= 14 and the tower bounds.
- H.-J. Bandelt and A. Dress, Adv. Appl. Math. 7 (1986) 309-343: h(2) = 6.

## Reproduce

```sh
sh build.sh                 # standard-library checks (Lemma 3.4, Theorem 2.9 checker, Proposition 4.1, families, proof runs) and the PDF; about 5 minutes
sh build.sh --game          # recomputes the Theorem 2.9 table (numpy) and checks the recursion against brute force
sh build.sh --sat-hashes    # regenerates the 135 CNFs of Lemma 3.3 and compares hashes
CADICAL=... DRAT_TRIM=... python3 verification/sat/run_twotree_certificates.py --workers 1   # full DRAT replay
```

## Provenance

Valyu Search, Contents and DeepResearch were used for the literature search, priority audits and reviews. DeepResearch tasks: `scout-phylogenetics` (domain scouting), `phylo-h3-prior` DR-055 (priority audit), `phylo-h3-review` DR-059 (max-mode adversarial review with code execution), `phylo-hk-bounds` DR-043 (review and priority check of the general bounds), `phylo-hk52-review` DR-020 (max-mode review of the equal-weight base-5/2 version; it pointed out the caterpillar lower bound), `phylo-game-review` DR-041 (max-mode review of Lemma 3.4 and Theorem 2.9), `phylo-final-review` DR-007 (max-mode review of the factor-3/16 lemma, the caterpillar proof and the 22-leaf family). The 13-leaf tree was found by a symmetric SAT search (`verification/sat/symsat.py`).

## Files

- `paper.tex`, `references.bib`, [public PDF](../../../../public-release/papers/common-quartet-number.pdf): the note.
- `triple13.pdf`, `plot_triple.py`: Figure 1.
- `video-brief.md`: brief for an explainer video.
- `verification/`: checkers, generators, solver logs and hashes (see its README).

## Priority checks performed (25-26 October 2026)

- DeepResearch audits `phylo-h3-prior`, `phylo-h3-review`, `phylo-hk-bounds`, `phylo-hk52-review` (citers of Snir-Yuster and of Currie et al., MAST literature, quartet literature, simultaneous separation, Zenodo and GitHub): no determination of h(3), no construction on 11-13 leaves, no single-exponential upper bound, no bound of the form C c^k with c <= 3. The caterpillar lower bound 2^k + 2 is Snir and Yuster's (stated without the construction).
- arXiv: Snir-Yuster has only v1 (26 Feb 2026); Currie et al. latest is v2 (17 Jul 2026), no v3; arXiv full-text search for "common quartet" returns only Currie et al.; searches for agreement subtrees and quartets from 2026-08-01 onward found only unrelated papers (quartet distance arXiv:2608.03542, quartet testing arXiv:2608.00987, quartet weights arXiv:2609.00614, uniform attachment trees arXiv:2609.30098).
- Zenodo API: exact-phrase queries "common quartet" and "Colless-like" return 0 records; "agreement subtree" and quartet + Snir return only unrelated datasets.
- GitHub API: issues and repositories for "common quartet", "no common quartet", Snir Yuster, agreement subtree: nothing relevant (the only Lean phylogenetics repository found, vltanh/lean4-phylogenetics, treats coalescent models and concordance factors).
- Author pages: K. Wicke's publication list (lists Currie et al. as submitted, nothing later on h(k)); M. Fischer's Greifswald page (nothing relevant). Pages of Snir, Yuster and Szekely could not be retrieved.
- erdosproblems.com is not relevant to this problem.
These searches are not exhaustive; absence of a match does not prove novelty.

## Final review and formal scope

The completed final max review (`DR-007`, 2026-10-26 12:25:40 UTC) found no mathematical error in the 3/16 lemma, caterpillar proof or 22-leaf family. It independently checked the latter by two quartet algorithms. Its presentation requests are addressed: relabel the smaller retained set X, preserve d >= 2 throughout, use exact threshold arithmetic, distinguish weaker general small-k bounds, and state the empty k=2 subcase. The caterpillar lower bound remains credited to Snir and Yuster.

Lean verifies the sharp real-variable inequality (`potential_step_sharp`) and its equality example (`potential_step_sharp_witness`). The earlier `potential_step` theorem retains the weaker 3/16 version. Neither h(3)=14 nor the tree lemmas, iteration, dynamic programme, SAT reduction or caterpillar construction is formalised in that file. The dynamic-programming checker verifies the safe pairs supporting the stated bounds; it does not certify global optimality of the strategy or every table entry's minimality.

The 23-leaf symmetric searches remain **unresolved**. No witness or UNSAT result was recovered. Their exact PIDs were paused in the lab to obey the one-heavy-worker limit; they are not part of this package's proof. The retained bound is 23 <= h(4) <= 28.

The journal text of Snir-Yuster was not directly accessible to the final reviewer; its arXiv v1 was read. Whether the journal version expands the omitted caterpillar construction remains unverified. This limits any originality claim for the exposition of that construction, not attribution of the already published lower bound.

Final commands, review responses and artifact links: [readiness.md](readiness.md). Original review reports are preserved in `verification/reviews/`.

The sharper update is reviewed in `verification/reviews/phylo-sharp-potential-review.md` (max task `DR-017`). The updated exact-arithmetic proof execution passes on 613 families for k=1..6 at n=4,7,16,37,85,195. It checks the retained potential, separation in every processed tree and the final common quartet. These simulations corroborate the bookkeeping; they do not replace the written proof. The threshold calculation uses integer square roots and is checked through k=8.
