# Exact Heesch numbers of small edge-marked polyforms

An edge-marked polyform has a bump, a nick or a flat side on every boundary edge, and copies may meet only bump-to-nick or flat-to-flat. If bumps and nicks are unequal in number, the shape cannot tile the plane, so its Heesch number (how many complete rings of copies can surround it) is finite. Mann's hexapillars, rows of hexagons with one particular marking, reach 5 (2001-2004). We ask, for small base shapes, what the best possible marking achieves, and answer exactly with certificates.

`h(P)` is the largest number of strict coronas (each ring a closed disk wrapping the previous one) achievable by grid-aligned copies of `P` under some marking with one centred mark per edge and #bumps != #nicks. We call this the lattice Heesch number; all results below are about it.

| Base shapes | Result |
|---|---|
| straight rows of 4 and of 5 hexagons | **h = 5**: no unbalanced marking reaches 6 lattice coronas, so in this model Mann's hexapillar value cannot be beaten on these base shapes |
| all 12 polyhexes with at most 4 cells | single hexagon 3; two hexagons 4; straight rows of 3 and 4: 4 and 5; bent tromino 3, triangle tromino 2; the six other tetrahexes 3, 2, 2, 2, 1, 1. **Max 5, only for the straight 4-row** |
| all 21 polyominoes with at most 5 cells | **max h = 3**, attained only by the straight 4- and 5-rows; L-tetromino, domino and straight tromino give 2; the other 16 give 1 |
| Bašić's 2021 record figure (Heesch number 6) | independent, replayable exact check that his published 169-tile patch is a valid strict 6-corona patch (no holes or pinch points); confirms, does not extend, his result |

[Paper](../../../../public-release/papers/marked-polyform-heesch-numbers.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md)

## Status

- **Computer-assisted theorems** (within the stated model: grid-aligned copies, one mark from {bump, nick, flat} per edge, strict coronas).
  1. `h(straight 4-row) = h(straight 5-row) = 5`.
  2. The values of `h` for every polyhex with at most 4 cells (table in the paper and `verification/results.json`).
  3. The values of `h` for every polyomino with at most 5 cells; none exceeds 3.
  4. Bašić's published patch satisfies the strict corona definition.
- Every lower bound is an explicit patch checked by a standard-library program. Every upper bound is the unsatisfiability of a CNF formula that does not even forbid holes, with a DRAT proof checked by drat-trim. A second, independently written encoder agrees on every value it was run on.
- **Hand proof** (paper, Proposition 3.1): with small semicircular bumps and nicks, an unbalanced marking gives a closed disk that cannot tile the plane under any isometries, and grid-aligned coronas are coronas of that disk. So each `h(P)` is realized by a plane figure with finite Heesch number at least `h(P)`.

## Closest prior work and what is new

- C. Mann, *Heesch's tiling problem*, Amer. Math. Monthly 111(6) (2004) 509-517 (thesis, Univ. of Arkansas 2001). Hexapillars, rows of n hexagons with one specific marking, have Heesch number 4 for n = 2, 3 and 5 for n >= 4; W. R. Marshall independently found 4 for n = 2. Polypillars give 2, 2, 3 for n = 2, 3, >= 4. Epstein's counting proof shows that unbalanced marked hexagons have Heesch number at most 3; Mann notes that the hexagon markings can simply be enumerated. Our values reproduce all of these.
- C. Mann and B. C. Thomas, Exp. Math. 25(3) (2016) 281-294. Per Kaplan's account, they enumerated **all** bump/nick assignments for a small family of low-order polyominoes, polyhexes and polyiamonds. They found values up to 5, but cut the search off at five coronas and left most cases inconclusive. We could not read the full text. Some of our lower bounds, and possibly some of our small exact values, may already be in it. Its cut-off means it could not show that 6 is impossible for the hexagon rows.
- C. S. Kaplan, Contrib. Discrete Math. 17(2) (2022), arXiv:2105.09438. SAT encoding of coronas for unmarked polyforms. Its Conclusions say the technique "could easily be extended to handle marked polyforms" and that non-tiling would then have to be checked, "whether based on combinatorial imbalance or a more complex computation". We follow that suggestion.
- Heesch Number Atlas (heesch-atlas.netlify.app, associated with Anton Bakker, 2026, not peer reviewed). Automated marking sweeps on eight lattices. Its inventory lists the straight 4- and 5-hexagon rows, as polyiamonds on the triangular lattice, with one marking each: a block of bumps, a block of nicks one longer or shorter, and one flat edge. It gives both Heesch number exactly 5. These are the same markings as our optimal witnesses, up to swapping bumps and nicks. The Atlas also re-verified Bašić's record, and notes that its own stored witness has a pinch point.
- B. Bašić, Math. Intelligencer 43(3) (2021) 50-53, the planar record 6, with a computer check that 6 is the maximum for his figure. D. Smith (hedraweb, 2019) and A. Džuklevski (arXiv:2610.02579) describe the family behind it.
- **New here:** (1) The marking is a SAT variable, and one cardinality constraint certifies non-tiling for all unbalanced markings at once. (2) We give exact maxima over **all** unbalanced markings for every base shape listed above, including a certified exclusion of 6 coronas for every unbalanced marking of the straight 4- or 5-row; the closest known Atlas entries give the value for one specific marking per row. (3) Every upper bound has a DRAT certificate. (4) An exact, replayable strict check of Bašić's published patch.
- **This is incremental.** The marked-polyform direction is heavily explored (Mann, Mann-Thomas, Smith, Bašić, the Atlas, and the Layr-Labs and Epoch AI Heesch challenges). We set no record and say nothing about Heesch number 7.

## Confidence

- Correctness of the computed values: **high**. Lower bounds are replayed by a standard-library checker that shares no code with the encoders, and 170 mutation tests confirm it rejects corrupted witnesses. Upper bounds are DRAT-checked with drat-trim. One small formula produced bit-identical proofs on a repeat run with CaDiCaL 3.0.1. All 34 original verification logs are retained; the default build checks their completeness and consistency, rather than replaying the large proofs.
- Encoding checks: a second encoder agrees on every value at k = h and k = h + 1, except the two k = 6 row formulas. The encoder reproduces Mann's and Epstein's values. In unmarked mode it reproduces Kaplan's `heesch-sat` values of Hc for unmarked polyhexes (see the paper). The residual risk is a shared misreading of the corona definition. This is mitigated by the written soundness argument (paper, Section 4) and by the agreement with `heesch-sat`, which was written independently by Kaplan.
- Proposition 3.1 (realization, non-tiling): **high**. It is a short geometric argument, a version of Epstein's and Mann's classical counting.
- Scope: the results concern grid-aligned copies, one centred mark per edge, strict coronas and unbalanced markings. For the realized curved figures, `h(P)` is only a lower bound on the true Heesch number: copies that slide along flat edges or sit on the finer triangular lattice are not excluded. Day's convention, which allows nick-to-flat voids (under it Ammann's hexagon reaches 4), would give larger numbers.
- Originality: **moderate to low** for the small tables, which Mann-Thomas may contain; **moderate** for the all-markings upper bound 6 on the 4- and 5-rows. We searched arXiv to 26 October 2026, the Valyu search index, GitHub, the Atlas pages, Mann (2004), Eppstein's Geometry Junkyard and secondary accounts of Mann-Thomas 2016 (full text paywalled), and ran three DeepResearch audits (below).

## Reproduce

```sh
sh build.sh             # witnesses, mutation tests, Bašić's patch, ledger completeness, PDF (about a minute)
sh build.sh --cnf       # also regenerate every CNF and compare hashes (needs python-sat)
sh build.sh --drat      # also re-solve the small CNFs and re-check their DRAT proofs (needs cadical, drat-trim)
sh build.sh --figures   # redraw figures (needs matplotlib)
```

The two largest formulas (straight 4-row and 5-row at k = 6: 6,895,353 and 12,387,835 clauses; proof replays 3,445.971 and 4,378.861 seconds) are regenerated by `--cnf` but re-solving them is left to the reader.

## Provenance

Valyu DeepResearch tasks: `tilings-scout` (heavy, DR-012; domain scouting), `tilings-priority-marked` (heavy, DR-072; prior-art audit for marked polyforms), `tilings-review-marked` (max, DR-031; adversarial review, see [review notes](verification/review.md)). Valyu Search and Contents were used to read Mann (2004), Džuklevski (arXiv:2610.02579), Bašić (arXiv:2610.24281), Smith's 2019 post and the Wikimedia Commons file page of Bašić's figure.

## Limitations and open questions

- Only one centred mark per edge and grid-aligned copies. With two marks per edge, the solver found no five-corona patch for the hexagon domino; there is no DRAT proof and we make no claim. Colours, oriented edges and other richer rules are untouched; an unpublished Heesch number of 11 is reported for oriented rules.
- Balanced markings that fail to tile are not covered.
- Pentahexes other than the straight row were not classified (the screen was stopped for time).
- The DRAT proofs are not shipped (the two largest are hundreds of MB). Commands to regenerate and replay them, and their original hashes, are in `verification/results.json`. No formally verified checker (cake_lpr) was used.
- Heesch number 7 in the plane remains open.
