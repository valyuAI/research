# A Hall-surplus certificate for 7x7x7 tic-tac-toe

**Status:** a new computer-assisted proof of a known theorem, plus a correction to the published case analysis. The target open problem, 6x6x6, is **not** settled.

## The question

In Maker-Breaker tic-tac-toe on the n x n x n cube, Maker moves first and wins by claiming all n cells of a line. The lines are the 3n^2 rows, the 6n plane diagonals and the 4 space diagonals. Maker wins for n <= 4 (Patashnik 1980 for n = 4). Breaker wins for n >= 8 (pairing; Golomb-Hales 2002). Cain, Raymond and Kallersjo, [arXiv:2509.21494v1](https://arxiv.org/abs/2509.21494) (25 Sep 2025), proved that Breaker wins for n = 7 by checking about 3.5 x 10^7 positions for a pairing strategy. They state (Sec. 6.2) that n = 5 and n = 6 are the only unresolved cases.

## What this package shows

1. **Surplus lemma (theorem, Lean-checked; textbook ingredients).** Take the bipartite graph from surviving lines (two slots each) to free cells. If its Hall surplus is at least d, a pairing survives any d further Maker cells. The surplus characterization is Lovasz-Plummer, Matching Theory, Thm 1.3.6. The pairing-as-matching criterion is Hales-Jewett 1963 (Beck's "bigamy corollary"). What is new is using surplus to absorb unknown Maker moves; we are not aware of an earlier use. The surplus is computed with one matching test per line. So Maker's later opening moves need not be enumerated. Lean: `formal/ValyuResearch/CubicTicTacToe.lean` (`pairing_of_replication`, standard axioms only).
2. **New proof that Breaker wins 7^3 (computer-assisted).**
   - *Maker opens at the centre.* Breaker takes (5,5,5), then one cell on each other space diagonal. Any such 4-set meeting at least 26 lines has surplus >= 4 (all 864 such sets). A greedy rule always reaches 27 lines against every Maker play (10,627-leaf pattern tree). Three unknown Maker moves remain, and 3 <= 4.
   - *Maker opens elsewhere.* Breaker takes the centre, then any space-diagonal cell a, then any cell b on another space diagonal sharing no line with a. There are 144 such pairs and 12 partners per cell, so one is always free. Every such position has surplus 3, for every Maker first move. Two unknown Maker moves remain.
   - Total: 66 + 1,158 symmetry classes of positions, each checked with at most 170 matchings, instead of about 3.5 x 10^7 positions.
3. **Positions not covered by the published case analysis (checked).** In the non-central case the text assumes, by symmetry, that both of Maker's first two moves have x <= 4. This fails when the two moves lie in strictly opposite octants about the centre. Example: Maker plays (1,7,1) then (6,2,6), Breaker plays (4,4,4) then (5,5,5), Maker plays (7,1,7). Then both of Breaker's prescribed third moves are taken. With m1 = (3,3,3) and m2 = (5,5,5), even the prescribed second move is taken. This affects 5,832 ordered (m1, m2) pairs. Proposition 3.2 covers all of these positions. The authors' public code covers only the central opening. As a cross-check we re-ran the published central enumeration: 22,163,142 positions, all with a pairing. We also ran the published non-central rule, with a greedy completion on the uncovered positions: 2,196,381 positions with m1 reduced by symmetry, 91,530 of them uncovered, all with a pairing. The theorem stands.
4. **Why 6^3 resists (theorem + evidence).** No pairing can exist before Breaker's 8th move: 7 cells meet at most 46 lines, and 47 are needed. Any 6^3 position has surplus at most 4. So a 6^3 proof must enumerate at least 3 of Maker's moves after the first and react to threats. Heuristic play reached a pairing only after 9-11 rounds.

## Confidence

- Correctness of the 7^3 certificate: **high**. Two independent implementations agree: Python (standard library, symmetry classes) and C (no symmetry). An independent from-scratch check and a third program replaying the published strategy also agree. The surplus lemma is proved in Lean. The game-theoretic step (pairing implies Breaker win) and the pattern-tree argument are short and on paper, not in Lean.
- Uncovered-positions claim (about the text): **high**. Confirmed by both DR reviews. The text of arXiv:2509.21494v1 Sec. 4.3 and its count 195 x 194 x 339 restrict both moves to x <= 4. The authors' unpublished code for this case might handle it differently; we could not check.
- Originality: **moderate** (adversarial review `2f5a6d77-...` found no fatal error and no earlier surplus-based Maker-Breaker proof). A DeepResearch priority audit (task `DR-046`) found no verification, criticism or repair of the 7^3 proof, and no resolution of 5^3 or 6^3. Robust or deficiency versions of Hall's theorem are classical (Lovasz-Plummer). We found no prior use of them as "pairings that tolerate d unknown moves" in Maker-Breaker proofs, but did not search exhaustively. Uiterwijk's set matching (arXiv:1703.10678) is related.
- Significance: **modest**. This is a shorter and more robust proof of a 2025 result, and a correction. It does not settle 5^3 or 6^3.

## Reproduce

```sh
sh build.sh          # surplus certificate (Python + C), counting facts, paper.pdf  (~10-30 min)
sh build.sh --full   # also replays the published strategy on 24,359,523 positions
```

See `verification/README.md`. Reviews: DeepResearch priority audit `DR-046`; DeepResearch adversarial review `DR-018` (see `review.md`).

## Files

- `paper.tex`, [public PDF](../../../../public-release/papers/cubic-tic-tac-toe-surplus.pdf), `references.bib`: the note.
- `verification/`: checkers and results.
- `video-brief.md`: brief for the explainer video.
- `review.md`: adversarial review and responses.
