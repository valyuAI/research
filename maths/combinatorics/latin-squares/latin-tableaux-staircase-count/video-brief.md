# Video brief: "Four new ways, every time"

Audience: a bright 16-year-old who has just finished GCSE maths. Target length 5-7 minutes.

## 1. The question in plain words

A Latin square is a grid where every row and every column contains each symbol once (Sudoku without boxes). A Latin tableau does the same thing on a staircase-like shape: rows have different lengths, row i holds the numbers 1 to (its length) once each, and no number may repeat inside a column. Some shapes can be filled and some cannot, and a big open problem (the "wide partition conjecture") predicts exactly which.

For the shapes with rows k, k-1, ..., 5, 4, 3, 3 (for example 6, 5, 4, 3, 3), the source paper conjectured the pattern 9 x 4^(k-3). This video explains an independently reconstructed proof for every k. An earlier public proof dated 22 October 2026 already gives the same formula and four-extension mechanism; introduce this as a verification note, not a new discovery.

## 2. Why anyone cares

- Latin tableaux are a stepping stone towards Rota's basis conjecture (1989), a famous unsolved problem about arranging bases of a vector space.
- The conjecture "Latin exactly when wide" connects a rule about row lengths to whether a filling exists. Earlier finite checks already cover this family's cases through k = 10. The induction explains all k, with an exact count rather than existence alone.

## 3. Smallest concrete example

Shape (5, 4, 3, 3): rows of lengths 5, 4, 3, 3. One filling (top row first):

```
4 5 2 1 3
3 1 4 2
2 3 1
1 2 3
```

Check the rules on screen: row 1 uses 1-5, row 2 uses 1-4, rows 3-4 use 1-3; column 1 reads 4, 3, 2, 1 (no repeats), column 2 reads 5, 1, 3, 2, and so on. There are 144 such fillings.

Then show k = 6 with a new top row of length 6 placed above it, for example:

```
5 4 6 3 1 2
4 5 2 1 3
3 1 4 2
2 3 1
1 2 3
```

## 4. Prerequisites to build, in order

1. Latin squares (a 3 x 3 example).
2. Young diagrams: left-aligned rows that get shorter going down.
3. The filling rule for a Latin tableau (rows contain 1..length; columns have no repeats).
4. Counting by "build it row by row": the number of fillings equals the sum over fillings of the lower rows of the number of ways to add the top row.

## 5. Key insight in visual steps

1. **Peel off the top row.** Removing the top row of a k-shape leaves exactly the (k-1)-shape. So if every filling of the smaller shape can be extended in exactly 4 ways, the count multiplies by 4 each time: 576, 2304, 9216, ...
2. **The big numbers are squeezed left.** Columns 1-3 already contain every number up to k-3 (shown as full columns). So the new row must put its three largest numbers k-2, k-1, k into the first three cells. Animate the column contents as coloured sets.
3. **The middle is forced like dominoes.** Column 4 already contains 1..k-4, so it needs k-3; then column 5 needs k-4; and so on down to 4. Show these cells snapping into place one after another.
4. **The small numbers are squeezed right.** What is left, 1, 2, 3, goes into the last three cells. The third-last cell is forced (two of the three are already in that column).
5. **Exactly two binary choices.** In the first block, k-2 is forced, and k-1 and k can swap: 2 ways. In the last block, after the forced cell, the other two can swap: 2 ways. Total 2 x 2 = 4.
6. **Why it never breaks.** Five simple facts about the top two rows ("invariants") guarantee both swaps are always legal, and every new filling again has the same five facts. Check them once by computer for all 576 fillings of the k = 6 shape; then they hold forever by induction.

## 6. Objects to show on screen

- The (5, 4, 3, 3) filling above and the k = 6 extension.
- A tall shape (k = 10) with its top row: 9 8 10 7 6 5 4 3 1 2, colour-coding the three blocks (big values, forced middle diagonal, small values).
- The counter 144 -> 576 -> 2304 -> 9216 -> 36864 -> 147456 with "x 4" arrows.
- The formula 9 x 4^(k-3).

## 7. Proved, computed, open

- Proved: the formula for all k >= 5, by induction from a finite base case.
- Priority: the same formula and mechanism appear in the earlier public proof linked in the README. No first-resolution claim.
- Computed: the base case (all 576 fillings for k = 6 satisfy the five facts), and brute-force counts up to k = 10 as a cross-check.
- Open: the general wide partition conjecture, Rota's basis conjecture, and the other shapes and monotonicity conjectures listed in the source paper.

## 8. Misconceptions to avoid

- This is not about ordinary Latin squares; the shape is a staircase with two rows of length 3 at the bottom.
- The computer does not "check all k": it checks one finite case, and the argument covers every larger k.
- "Each filling extends in exactly 4 ways" is stronger than "the total is multiplied by 4"; the proof shows the stronger statement.
- Do not claim that no small examples were known before this work, or that the six supplied example tableaux are new existence results.
