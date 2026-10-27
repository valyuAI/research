# All symplectic billiard orbits in special octagons (and symmetric Hexhouses) are periodic

**Status: theorem (written proof) with exact computational checks. Research draft, not externally refereed.**

A *special octagon* is a lattice octagon whose opposite sides are parallel, with slopes 0, ±1 and ∞, and which has an axis of symmetry parallel to a pair of sides. Albers, Banhatti, Sadlo, Schwartz and Tabachnikov conjectured from computer experiments that every orbit of the symplectic billiard map in a special octagon is periodic ([Polygonal symplectic billiards](https://arxiv.org/abs/1912.09404), Conjecture 6.2; published in J. Exp. Math. 1 (2025) 1-22, DOI 10.56994/JXM.001.001.001). They wrote that for this family they "can only give computer evidence".

**Theorem.** Conjecture 6.2 is true. After an affine normalization to O(W,H,c1,c2) (the rectangle [0,W]x[0,H] with the lower corners cut by 45-degree segments of leg c2 and the upper corners by legs c1), every orbit has period at most 4(N^2 - N), where N = 4W + 2H - 2(c1 + c2).

**Corollary (mirror-symmetric Hexhouses).** The same lemma holds for the hexagons O(W,H,c1,0). The linear map (x,y) -> (hx, py) sends the Hexhouse X(s,h,p,q) (square [0,s]^2 with roof vertices (p,s+h), (q,s+h)) with p + q = s onto O(hs, p(s+h), hp, 0). Hence every mirror-symmetric Hexhouse is fully periodic: the symmetric case of ABS Conjecture 6.1. Hexhouses with p + q != s have a non-harmonic cross-ratio of side directions, are not affine images of these hexagons, and remain open.

[Paper](../../../../public-release/papers/special-octagon-symplectic-billiards.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md)

## The idea

1. **Criterion (not new).** Let C be the set of even points x_0, x_2, x_4, ... of trajectories that start at a vertex. If C is finite, every orbit is periodic. This is Albers-Lander-Westermann ([arXiv:2402.12244v2](https://arxiv.org/abs/2402.12244), Theorem 1.1 = Theorem 3.4(III)); the paper includes a short self-contained proof for convex tables (a cell-counting argument).
2. **Half-lattice lemma (new).** In O(W,H,c1,c2), every even point of a trajectory from a vertex lies in S = (lattice points of the boundary) ∪ (points with both coordinates in Z+1/2 on a diagonal side) ∪ (points on a horizontal side with x in Z+1/2), and whenever an even point lies in the last class, the next odd point lies on a vertical side. All side lines have integer constants, so vertical and diagonal chords keep the points on the half-lattice; horizontal chords from non-horizontal sides are the mirror reflection x -> W - x, which supplies the coupling clause. The coupling blocks the only bad case (a diagonal chord from a half-integer point on a horizontal side). Hence C ⊂ S, which is finite with abs(S) = N.
3. **Symmetric Hexhouses.** Corollary 3.4, via the map above.
4. **Symmetry is needed.** The asymmetric lattice octagon Q with vertices (1,0),(3,0),(4,1),(4,4),(3,5),(2,5),(0,3),(0,1) (same side slopes, no axis) has a hyperbolic 6-periodic orbit (4,11/3), (5/3,0), (2/3,11/3), (4,7/3), (2/3,1/3), (5/3,14/3) with return multipliers -2 and -1/2, so it is not fully periodic (Proposition 3.6).

## Evidence and confidence

| Layer | What | Confidence |
| --- | --- | --- |
| Written proof | Lemma 3.2 (half-lattice), Lemma 3.1 (normalization), Theorem 2.4 (criterion), Corollary 3.4 (symmetric Hexhouses), Proposition 3.6 | High (about 90%) that the theorem is correct as stated; the proof is short and elementary, re-checked line by line, plus an independent adversarial agent review and a max-mode DeepResearch review (see below) |
| Exact computation | Symmetric Hexhouses with parameters <= 11: C finite and inside S after the map (`verification/check_symmetric_hexhouses.py`). Two independent exact programs: all 1484 admissible parameter tuples with W,H,c1,c2 <= 14 (mirror and rescaled copies counted separately) have finite C ⊂ S, clause (b) holds at every state; identical C and state counts for parameters <= 10; abs(S) formula for parameters <= 12 | Certain for the instances checked |
| Asymmetric octagon Q | Exact check of the orbit, multipliers and perturbation | Certain (also checked by hand) |
| Originality | Priority search on 26 Oct 2026: arXiv API (symplectic billiard listings to 4 Oct 2026, author listings since 2025-06), Zenodo, GitHub, Valyu paper/web search, author pages, and DeepResearch audit DR-019: no proof of Conjecture 6.2 found. ALW Corollary 3.3 covers lattice polygons with at most three side directions; special octagons have four. ALW's filled-set criterion (Theorem 3.1) does not currently supply a proof for the family: for O(5,6,1,2) and others the exploration of the filled set has not closed after 20000 points (`verification/filled_set.py`; this does not prove the set infinite) | Moderate-high (about 80%) that the result is new |

## Closest prior work

- Albers-Tabachnikov, *Introducing symplectic billiards*, Adv. Math. 333 (2018) ([arXiv:1708.07395](https://arxiv.org/abs/1708.07395)): trapezoids and affine-regular polygons are fully periodic.
- Albers-Banhatti-Sadlo-Schwartz-Tabachnikov (arXiv:1912.09404v1; JEM 2025): the conjectures (4.1 Penthouses, 6.1 Hexhouses, 6.2 special octagons, Question 7.1).
- Albers-Lander-Westermann, *Symplectic billiards for pairs of polygons* (arXiv:2402.12244v2, 15 July 2026): the critical-set criterion used here and full periodicity for lattice polygons with at most three side directions (Corollary 3.3). Their Figure 21 shows one special octagon (apparently O(3,3,1,1)) in BP via a finite filled set F; they do not state or address Conjecture 6.2, and for several special octagons the exploration of F has not closed after 20000 points (`verification/filled_set.py`).

**What is new:** the half-lattice lemma with its coupling clause, hence a proof of Conjecture 6.2, an explicit period bound, and the asymmetric example showing the mirror symmetry cannot be dropped.

## What is not claimed

- The Hexhouse Conjecture 6.1 for Hexhouses without mirror symmetry (p + q != s) and the Penthouse Conjecture 4.1 remain open. `verification/check_other_families.py` gives finitely many instance checks only (Hexhouses with integer parameters <= 11, 60 rational Penthouses).
- Octagons of the same shape with rationally incommensurable real parameters are not covered (exploratory runs with generic rational legs suggest they are also fully periodic).
- The period bound is crude; exact period sets are not determined. Observed generic periods of O(5,6,1,2) are 4, 16, 32, 44, 68, 92.
- No Lean formalization.

## Reproduce

```sh
sh build.sh          # quick replay (octagon parameters <= 8, a few minutes) and PDF build
sh build.sh --full   # full replay (parameters <= 14, Hexhouses <= 11; several hours)
```

Python 3 standard library for all checks; `plot_figure.py` needs matplotlib; `pdflatex` and `bibtex` for the paper.

## DeepResearch tasks

- `dynamics-symp-priority` (heavy), id DR-019: priority audit for ABS Conjectures 4.1, 6.1, 6.2 and Question 7.1. Found no resolution.
- `dynamics-octagon-review` (max), id DR-085: adversarial review of the final statement and proof. Outcome: see the section below.

- `dynamics-hexhouse-review` (heavy), id DR-058: review of the symmetric-Hexhouse corollary and priority check for Conjectures 6.1 and 6.2.

## Review outcome

Internal reviews (two DeepResearch reviews and an agent review, not included in this package) found no fatal or serious error; their minor points are fixed in the paper. An independent referee report on this package found no gap in the three claims, with high confidence in the theorem and moderate confidence in novelty. These are not external peer review. What a reader can verify directly is the written proof and the programs in `verification/`.
