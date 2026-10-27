# Video brief: how many rings can a broken jigsaw piece grow?

Audience: a bright 16-year-old who has just finished GCSE maths or physics. Target length 5-8 minutes.

## 1. The question in plain words

Take a jigsaw-like piece. Lay copies of it around the original so that the original is completely enclosed, with no gaps and no overlaps: that is one ring, or "corona". Now enclose that whole cluster with a second ring, then a third, and keep going. If the piece can tile the whole plane, you can go on forever. If it cannot, you get stuck after some number of rings. That number is the piece's **Heesch number**.

Nobody knows how large a Heesch number can be in the plane. The record is 6 (Bojan Bašić, 2021). This package does not break the record. It answers a smaller question exactly:

> For the simplest pieces made of 1 to 4 hexagons or 1 to 5 squares, with edges that may carry a bump or a matching dent, what is the most rings any unbalanced choice of bumps and dents can achieve, keeping copies on the prescribed grid and using one centred mark per edge?

## 2. Why anyone cares

- Heesch's problem (1968) is one of the classic open problems of tiling theory: is there any limit to the number of rings?
- Bumps and dents ("nicks") are the oldest trick for building pieces with many rings. Casey Mann used them in 2001-2004 to build rows of hexagons with 5 rings, the previous planar record.
- Computers now search millions of such pieces. Most searches give a lower bound ("at least 5 rings") but cannot say "and no better marking exists". This package gives exact answers with certificates that anyone can re-check.

## 3. The rules, shown on screen

- Grid of regular hexagons (and later a grid of squares).
- A piece = a few cells glued edge to edge, for example a straight row of 4 hexagons (18 outer edges).
- Each outer edge is labelled B (bump: a small semicircle sticking out), N (nick: a semicircle cut in) or F (flat).
- Two copies may touch along an edge only if a bump meets a nick or a flat meets a flat. Copies may be rotated and flipped, and stay on the grid.
- Rings must be solid: no holes, and each ring must completely wrap the previous cluster.

## 4. The smallest concrete example

**A single hexagon with marks B N N F B B** (going round the six edges). It has 3 bumps and 2 nicks, so bumps outnumber nicks by one. Show that it can be surrounded 3 times (37 hexagons in total: 1 + 6 + 12 + 18), and that no unbalanced marking of a hexagon can reach 4 rings under these rules. This matches Epstein's classical counting proof, which is worth animating: a fourth ring would contain 61 hexagons, each bringing one surplus bump, but the cluster has only 54 outer edges on which unmatched bumps can sit, and 61 > 54. For longer pieces this simple count is no longer strong enough, and that is where the computer is needed.

Then the star: **the straight row of 4 hexagons**. It has 18 outer edges. Going once round the boundary, the best marking found is

b b b b b b b b b  f  n n n n n n n n

a block of 9 bumps, one flat edge, then a block of 8 nicks (bumps beat nicks by one). Every best marking found for the straight rows has this shape: for 1, 2, 3, 4, 5 hexagons it is BBB F NN, B⁵ F N⁴, B⁷ F N⁶, B⁹ F N⁸, B¹¹ F N¹⁰. Show its 5 rings: 131 pieces, the cluster sizes in hexagons are 4, 24, 68, 160, 316, 524 (figure `patch-bar4.pdf` in this folder: the red piece in the middle, rings in alternating blues).

## 5. Prerequisite ideas to build from scratch, in order

1. Tiling the plane with copies of one shape (squares, hexagons, a brick).
2. A corona: one complete ring around a shape. Then rings around rings.
3. Why a shape that tiles the plane has infinitely many rings, and why a shape that does not tile has only finitely many (just the idea: if you could build arbitrarily many rings you could build a whole tiling).
4. Counting argument: in any big patch, every bump must sit in exactly one nick. If each piece has one more bump than nick, then N pieces bring N more bumps than nicks. Only the pieces near the edge of the patch can hide the extra bumps, and there are only about the perimeter's worth of them. Area grows like R², perimeter like R, so for a big patch the counts cannot match. So the shape can never tile the plane.
5. Yes/no puzzles for computers (SAT): describe the puzzle as many true/false switches plus rules; a SAT solver either finds a setting of all switches that obeys the rules or proves that none exists.

## 6. The key insight in visual steps

**Step 1. The marking is part of the puzzle.** Do not try the 3^18 (about 387 million) markings of the 4-row one at a time. Put one switch per edge label into the puzzle and let the solver choose the marking and the rings together. Show 18 edges each with a dial B/N/F spinning, all while ring placements light up.

**Step 2. One rule replaces the hardest test.** Earlier searches stalled because they could not tell which markings tile the plane. Add one rule: "bumps minus nicks is at least 1". By the counting argument, every marking that obeys it automatically cannot tile. (Swapping all bumps and nicks shows we lose nothing by insisting on more bumps than nicks.)

**Step 3. A finite search window suffices.** Every piece in ring j lies within a fixed distance of the centre, growing by at most (piece width + 1) per ring. So the solver only needs pieces inside a circle of radius 32 for the 4-row at 6 rings. Animate rings growing inside a dashed circle.

**Step 4. Yes answers come with pictures.** When the solver says yes, it hands over the actual rings. A short independent program re-checks them from scratch: no overlaps, bumps in nicks, no holes, each ring wraps the last.

**Step 5. No answers come with proofs.** When the solver says no (for example "no unbalanced marking of the 4-row gives 6 lattice rings"), it writes a step-by-step proof of millions of lines (a DRAT proof), and a separate checker program replays every step. Show a scrolling wall of tiny clauses ending in "s VERIFIED".

**Step 6. The scoreboard.** Show the table: single hexagon 3, two hexagons 4, rows of 3, 4, 5 hexagons give 4, 5, 5; all other small hexagon shapes at most 3. For squares, the rows of 4 and 5 give 3, and most other shapes only 1.

## 7. Exact figures and objects to show

- The hexagon row of 4 with its 18 edge labels (above).
- `patch-bar4.pdf`: the 131-piece, 5-ring patch.
- `table-tiles.pdf`: every small shape with its value h.
- Numbers: 3^18 ≈ 3.9 × 10^8 markings of the 4-row; the 6-ring question for the 4-row is a yes/no puzzle with about 0.95 million switches and 6.9 million rules (the 5-row: 1.6 million and 12.4 million).
- Bašić's record piece (6 hexagons plus 11.5 triangles, 169 pieces in 6 rings). We re-checked his published picture exactly: every one of the 169 pieces snaps onto the grid, and the rings are solid with no holes or pinch points.

## 8. What is proved, what is computed, what is open

- Proved by hand: the counting argument (unbalanced bumps and nicks mean no tiling), and that rings found on the grid give rings of the real curved shape.
- Computed and certified: every value in the table, for pieces kept on the grid with one mark per edge.
- Not covered: pieces that slide off the grid, several marks per edge, colours or arrows on edges. The real curved shape could, in principle, have more rings if copies slide off the grid; the table is about grid-aligned rings.
- Still open: whether any shape in the plane has Heesch number 7 or more.

## 9. Misconceptions to avoid

- This is not a new record. Mann reached 5 in 2001 and Bašić reached 6 in 2021. The proposed contribution is the maximum over all unbalanced markings in this lattice model, plus certificates. The Atlas already reports Heesch number 5 for one marking of each straight 4- and 5-row; Mann-Thomas may overlap with the smaller tables.
- "Cannot tile" does not mean "few rings": the hexagon rows cannot tile but still reach 5.
- A computer "no" is not hand-waving here: the DRAT proof is checked line by line by a separate program, and the yes-answers are checked by a third, very short program.
- More bumps is not better: the straight-row witnesses have one surplus bump. Six other optimal witnesses have imbalance 2 or 3; do not generalize the straight-row pattern.

## Narration and accessibility handoff

Build each unfamiliar term from the concrete example before showing the formula. Read the key inequality or count aloud and leave it on screen long enough to follow. Use captions matching the spoken narration, and use labels/patterns as well as colour. Keep the proved/computed/open distinction visible in the final scene. Credit the named prior work where its result first appears. Root produces the narrated MP4 and editable video source; this brief does not claim that a video has been produced.
