# Video brief: every symplectic billiard path in a special octagon repeats

Audience: a bright 16-year-old who has just finished GCSE maths or physics. Target length 6-9 minutes.

## 1. The question in plain words

Take an octagon drawn on squared paper. Put two points on its edge. Draw the line between them: that is a "shot". The next point of the shot is found by a strange rule (below) that uses only parallel lines. Repeat forever. Does the sequence of points always come back to where it started, exactly, after some number of steps?

In 2019 five mathematicians (Albers, Banhatti, Sadlo, Schwartz, Tabachnikov) ran computer experiments and conjectured: for a certain family of octagons, "special octagons", every such sequence comes back. They wrote that they could "only give computer evidence". This package proves it.

## 2. Why anyone cares

- Billiards are a model of motion: a ball bouncing in a box. Mathematicians use them to study when motion is regular (repeats) and when it is chaotic.
- For ordinary billiards in a polygon it is a famous open problem whether every triangle even has one repeating path. Symplectic billiards are a newer, cousin game where the same kind of question is open: nobody knows whether every polygon has a repeating path.
- "Every path repeats" is the most orderly behaviour possible. Only a few shapes were known to do this (trapezoids, affine images of regular polygons). Special octagons are a new infinite family where it is now proved.

## 3. The rule (symplectic billiards in a polygon)

Points x0, x1, x2, ... lie on the boundary of the polygon. Given x0 and x1:

> x2 is the other end of the chord through x0 that is parallel to the side containing x1.

Then x3 is the other end of the chord through x1 parallel to the side containing x2, and so on. Every step uses only "draw a line through a point, parallel to an edge, until it hits the boundary".

Animate this once slowly: highlight the side containing x1 in colour, slide a ruler parallel to it until it passes through x0, follow it across the octagon to x2.

## 4. The smallest concrete example

The octagon O(5,6,1,2): start with the rectangle 0 <= x <= 5, 0 <= y <= 6. Cut the two bottom corners with 45-degree cuts of size 2 and the two top corners with 45-degree cuts of size 1. Vertices:

(2,0), (3,0), (5,2), (5,5), (4,6), (1,6), (0,5), (0,2).

It is mirror symmetric about the vertical line x = 2.5. Its eight sides lie on the lines

y = 0, x - y = 3, x = 5, x + y = 10, y = 6, y - x = 5, x = 0, x + y = 2.

Every number on the right is a whole number. This is the whole secret.

The figure `octagon-figure.pdf` in this folder shows this octagon, with a trajectory that starts at the corner (2,0), with x1 on the lower-right diagonal side, and ends at the corner (3,0) after 46 steps. Its even-numbered points include (7/2, 1/2) and (7/2, 6). If you start at a random point instead, the orbit repeats with one of the periods 4, 16, 32, 44, 68, 92 (these are exactly the periods the 2019 paper reported for its Figure 23).

## 5. Prerequisite ideas to build from scratch, in order

1. Coordinates and lines: horizontal (y = K), vertical (x = K), diagonal (x + y = K or x - y = K).
2. Moving along a direction keeps a quantity fixed: horizontal keeps y, vertical keeps x, direction (1,1) keeps x - y, direction (1,-1) keeps x + y.
3. Half-integers: numbers like 1/2, 3/2, 5/2. The "half-grid" is all points whose coordinates are whole or half-whole.
4. Reflection in a vertical mirror line x = W/2 sends (x, y) to (W - x, y).
5. Periodic means: after n steps you are back exactly where you started.
6. Area preservation (only the idea): the rule moves small patches of starting pairs around without shrinking or stretching their total area. If a patch keeps moving inside a box of finite area, it must eventually overlap itself.

## 6. The key insight in visual steps

**Step 1. The dangerous points are corners.** A path breaks only if it hits a corner exactly. Collect all points that can be reached from a corner by the rule in an even number of steps. Call them the critical points C. Show them as red dots on the boundary.

**Step 2. Finitely many critical points means everything repeats.** If C is a finite set of red dots, they chop the boundary into finitely many pieces. Pairs of pieces form finitely many rectangles of starting pairs (draw a grid on a square "phase space" picture). Each rectangle moves as one block, the blocks keep their area, there is only finite area to go round, so each block must return to itself, and then every point in it repeats. (This criterion is due to Albers, Lander and Westermann; the paper reproves it.)

**Step 3. Track the even points on the half-grid.** Show the octagon on squared paper with a lighter half-grid. Claim: every even point x0, x2, x4, ... of a path that starts at a corner lands on one of three kinds of dots:
- green: whole-number grid points on the boundary;
- blue: half-grid points (both coordinates end in .5) on a diagonal side;
- orange: points on the top or bottom side whose x-coordinate ends in .5.

**Step 4. Why the dots stay on the dots.** Animate each move type from a green dot:
- vertical move keeps x a whole number, and every side line has a whole-number constant, so the landing point is green;
- a diagonal move keeps x - y (or x + y) whole; meeting another diagonal line x + y = K gives x = (K + k)/2, which is whole or half: green or blue;
- a horizontal move is just the mirror reflection (x, y) -> (W - x, y), because the octagon is symmetric. Whole numbers stay whole.

**Step 5. The one dangerous case, and how symmetry rescues it.** An orange dot (x ends in .5, on the top or bottom) is risky. In O(5,6,1,2), a slope -1 chord from the orange dot (7/2, 6) would land at (5, 9/2), a half-height on a vertical side; a slope 1 chord from there would land at the quarter-point (5/4, 3/4) on the lower-left diagonal, and the pattern would break. Show this hypothetical in grey with a red cross. But: we only reach an orange dot by a vertical move, so the odd point just before it was on a vertical side. The next odd point is found by a horizontal chord from that vertical side, which (mirror!) lands on the other vertical side. So the move out of an orange dot is always vertical again, and a vertical move keeps x ending in .5. The danger never happens.

**Step 6. Count and conclude.** The dots form a finite set of 4W + 2H - 2(c1 + c2) points (for O(5,6,1,2): 20 + 12 - 6 = 26 points). So C is finite (for O(5,6,1,2) it actually has 20 points), and Step 2 says every orbit is periodic.

## 7. What must appear on screen

- The octagon O(5,6,1,2) on squared paper, its eight side equations listed, the vertical mirror line dashed.
- The rule animation (ruler slid parallel to a side).
- Red critical dots; then the green, blue and orange dot sets; count 26.
- The grey near miss (7/2, 6) -> (5, 9/2) -> (5/4, 3/4) in Step 5 crossed out, then the mirror argument as two arrows: vertical side -> horizontal chord -> other vertical side.
- A phase-space square divided into a grid of rectangles that shuffle and return (Step 2).
- The asymmetric octagon Q with vertices (1,0), (3,0), (4,1), (4,4), (3,5), (2,5), (0,3), (0,1) and its six-point loop

  (4, 11/3) -> (5/3, 0) -> (2/3, 11/3) -> (4, 7/3) -> (2/3, 1/3) -> (5/3, 14/3) -> back.

  Show that nudging the start point by e along its side comes back as -2e (stretched), while nudging the second point comes back as -e/2 (squeezed). A point that is squeezed toward the loop forever never repeats exactly, so Q is NOT fully periodic. Coordinates with thirds are a hint that this loop never meets the half-grid at all.

## 8. Proved versus computed versus open

- Proved (written proof): every orbit in every special octagon is periodic, with period at most 4(N^2 - N), N = 4W + 2H - 2(c1 + c2). The bound is crude; actual periods are much smaller (largest 92 for O(5,6,1,2)).
- Proved: the symmetry cannot be dropped: Q above has a non-repeating orbit.
- Proved (same argument): every mirror-symmetric "Hexhouse" (a square with a symmetric trapezoid roof, for example the square [0,3]^2 with roof corners (1,4) and (2,4)) is fully periodic. Squashing it by (x, y) -> (hx, py) turns the roof slopes into +-1, so it becomes a cut-corner hexagon of the same kind. Lopsided Hexhouses are still open.
- Computed (checks, not proofs): two independent exact programs confirm the dot rule for all 1484 special octagons with parameters up to 14. Instance checks of the related "Hexhouse" and "Penthouse" conjectures.
- Open: the Hexhouse conjecture and the Penthouse period conjecture in general; octagons of this shape whose side lengths are not in whole-number ratios; whether every convex polygon has at least one repeating symplectic billiard path.

## 9. Misconceptions to avoid

- This is not the usual "angle in = angle out" billiard. The rule uses parallel lines only, no angles.
- "Every orbit is periodic" does not mean every orbit has the same period: O(5,6,1,2) has periods 4, 16, 32, 44, 68, 92.
- The proof does not run the computer forever. The computer checks were used to discover the dot rule and to double-check it; the proof is the short case analysis.
- The half-grid is not obvious: the set of points reachable from corners using all four directions freely keeps growing in the computer search (20000 points, denominators like 2^14), with no sign of closing; we have not proved whether it is finite, and the proof does not need it. The trick is that only the even points of real trajectories matter, and the mirror symmetry forces the right move at the one dangerous moment.
- Both hypotheses matter: whole-number corners (lattice) and the mirror axis.
- The general periodicity criterion (Step 2) is not new: it is due to Albers, Lander and Westermann (2024-2026). What is new is the dot rule for special octagons.
