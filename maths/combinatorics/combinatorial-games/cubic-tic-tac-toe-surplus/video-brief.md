# Video brief: why 7x7x7 noughts and crosses is a draw, in about a thousand checks

Audience: a bright 16-year-old who has just finished GCSE maths. Target length: 6-8 minutes.

## 1. The question in plain words

Play noughts and crosses in a 7 x 7 x 7 cube of cells. You win by filling a whole straight line of 7 cells: along a row, along a diagonal of a flat slice, or along one of the 4 corner-to-corner diagonals of the cube. We play the "Maker-Breaker" version. Maker (X) moves first and wants a full line. Breaker (O) only wants to stop every line. Question: can Breaker always stop Maker?

Known answers: Maker wins on cubes up to 4 x 4 x 4. Breaker wins on 8 x 8 x 8 and bigger. 7 x 7 x 7 was settled in 2025 by Cain, Raymond and Kallersjo: Breaker wins, so the ordinary game is a draw. 5 x 5 x 5 and 6 x 6 x 6 are still unknown. That includes 6 x 6 x 6, which this project set out to crack and did not.

## 2. Why anyone cares

- These are the simplest unsolved cases of a 50-year-old family of problems, connected to the Hales-Jewett theorem.
- The 2025 proof checked about 35 million positions by computer. A proof that needs about a thousand checks is easier to trust and to re-run.
- Checking proofs matters: the published argument skipped a family of cases (section 6 below).

## 3. Smallest example: the pairing trick on a 5 x 5 board

Show a 5 x 5 board (12 lines: 5 rows, 5 columns, 2 diagonals). Label 24 of the 25 cells with numbers 1 to 12, each number used twice, so that every line contains both cells of some number. The centre stays blank. Use Figure "5x5 pairing" from arXiv:2509.21494 as a model:

```
 2  6  8  5  8
11 10  3  1 10
11  4  .  4 12
 9  1  9  5 12
 7  6  3  7  2
```

Rule for Breaker: whenever Maker takes a numbered cell, take the other cell with the same number. Each line holds a matched pair, and Breaker gets one cell of every pair. So Maker can never fill a line. Counting shows why this needs room: 12 lines x 2 cells = 24 cells, and the 5 x 5 board has 25.

On the 7 x 7 x 7 cube: 193 lines would need 386 cells, but the cube has only 343. So Breaker cannot pair from the start. Breaker must first spend a few moves "killing" lines (placing an O on them).

## 4. Prerequisites to build, in order

1. Lines in a cube. Count them: (9^3 - 7^3)/2 = 193 for the 7-cube. Show the centre cell (4,4,4) sitting on 13 lines.
2. A pairing = every line gets two private cells.
3. Matching. Draw lines on the left and cells on the right, with each line drawn twice ("two slots"). Join each slot to the free cells of its line. A pairing is a way to give every slot its own cell.
4. Hall's condition. A pairing exists exactly when every group of slots touches at least as many cells as there are slots in the group. Show a small failing example: 3 slots that together touch only 2 cells.

## 5. The key insight in 5 visual steps

1. **Breaker's opening.** If Maker starts in the centre, Breaker puts O's on the four space diagonals, starting at (5,5,5). Animate 27 lines turning grey (killed). 166 lines survive.
2. **The worry.** Meanwhile Maker has made 3 more moves somewhere. The 2025 proof tried every possibility: about 340 x 340 x 340 / 2, or 22 million, cases.
3. **Spare room ("surplus").** Instead, measure how much spare room the matching has. Surplus = the smallest value of (cells touched - slots) over all groups of slots. Show a bar for one group: 340 cells touched, 332 slots, spare 8. The real minimum, over all groups, is 4.
4. **Why spare room beats enumeration.** If every group of slots has at least 4 spare cells, Maker can delete ANY 3 cells and every group still has at least one cell per slot. Animate 3 X's landing anywhere: the matching re-routes along a chain of swaps and still works. So we never need to know where Maker's 3 moves went.
5. **Count of checks.** Computing the surplus takes one matching test per surviving line, about 170 tests per position. Up to symmetries of the cube there are 66 opening patterns for the centre case and 1,158 for the other case. That is about 1,200 checks instead of 35 million positions.

## 6. The skipped cases (short segment)

The 2025 paper says: "by rotating the cube, assume both of Maker's first two moves are in the half of the cube with x at most 4." Show two cells in opposite corners' octants, (1,7,1) and (6,2,6). Spin the cube through all 48 rotations and reflections. The two cells are never both in the left half. So those games were not checked. Show the concrete game: Maker (1,7,1), Breaker (4,4,4), Maker (6,2,6), Breaker (5,5,5), Maker (7,1,7). Now both of Breaker's planned third moves are taken. Our computation covers these cases. The theorem is still true.

## 7. Why 6 x 6 x 6 is harder (closing segment)

- 6-cube: 216 cells, 148 lines. A pairing needs 2 x (surviving lines) <= free cells.
- Each Breaker cell kills at most 7 lines, and only 4 lines are space diagonals, so k cells kill at most 6k + 4 lines. After 7 rounds that is at most 46 lines, but 47 are needed. So a pairing is impossible until round 8.
- Spare room is capped too. A surviving line has only 6 cells, and needs 2 of them, so its spare room is at most 4. So the "ignore Maker's moves" trick can absorb at most 4 of Maker's moves, while Maker makes 7 or more before a pairing is possible.
- Animate a simulation: a pairing first appears around move 9-11.

## 8. Proved vs computed vs open

- Proved on paper and in Lean: the spare-room lemma (surplus d means any d deleted cells still allow a pairing).
- Proved on paper: pairing means Breaker wins. The opening rules are always possible.
- Computed (three independent programs agree): the surplus values and the pattern tree. The published strategy also works on all 24,359,523 positions it reaches.
- Open: 5 x 5 x 5 and 6 x 6 x 6.

## 9. Misconceptions to avoid

- Do not say we solved 6 x 6 x 6 or 5 x 5 x 5. We did not.
- Do not say the 2025 result was wrong. The theorem is true; its write-up skipped some cases, which we checked.
- "Draw" refers to the ordinary game. In Maker-Breaker terms, Breaker wins.
- Surplus is not "free cells minus slots" for the whole board. It is the minimum over every group of slots, which is why a computer is needed.
- The symmetry count (48) includes reflections, not just rotations.

## On-screen objects and formulas

- Number of lines: ((n+2)^3 - n^3)/2. Examples: 193 for n = 7, 148 for n = 6.
- Hall: |N(S)| >= |S|. Surplus: sigma = min over S of (|N(S)| - |S|).
- Centre-case table: lines killed 27 -> sigma 4; 26 -> 4; 25 -> 2; 22 -> no pairing.
- 6-cube bound: need E >= 40 + k; have E <= 6k + min(k, 4); 46 < 47 at k = 7.
