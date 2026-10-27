# Storyboard: Tic-tac-toe where nobody wins

Finding: `HJ(p+1, 2; 2) = p+1` for every prime `p` (paper.tex, Theorem 1 and Corollary 2), formalised in
`formal/ValyuResearch/HalesJewett.lean`. Running example: the 3 by 3 board, which is the `p = 2` case of
the construction. Scaled example: `p = 7` (eight digits, seven dimensions), the smallest new case, with
numbers from `verification/hj8_independent_verification.json`. Every number is reproduced by
`check_numbers.py` in this folder.

Colour meaning (fixed for the whole video): blue cells = blue (`BLUE_D` fill), red cells = muted red fill,
yellow = the line, star or value currently being looked at, bright red outline or cross = a win for
someone (a failure of the draw), green tick or teal = success. Stars in patterns are always yellow.

| Scene | Narration summary | Visual | What the viewer now understands |
|---|---|---|---|
| 1 Hook | Tic-tac-toe; new game: colour all cells red or blue; red wins with a whole red line, blue with two blue neighbours on a line; can nobody win? Bigger boards, more dimensions? | 3 by 3 board, quick X/O game won along the bottom row; cells fill red/blue; a red row and a blue pair outlined in bright red; small 4 by 4 board and cube appear beside the question | The lopsided game and the question "can a colouring avoid both wins?" |
| 2 Lines | Cells named by column then row (00 ... 22). A line is a pattern with a star: `*1` gives 01, 11, 21. `1*` a column, `**` the diagonal. The other diagonal is not a line (digits move in opposite directions), so 7 lines. Neighbours: stars filled with consecutive digits; the ends are not neighbours | Board with axis numbers and cell names; pattern written on the right, star in yellow, filled words appear as cells light up; yellow bands for each line; anti-diagonal dashed and crossed out; all 7 bands; arcs on row `*1`: 01-11 and 11-21 green, 01-21 red | Exactly which triples count as lines and which pairs count as neighbours |
| 3 Puzzle | The puzzle stated. Idea: digit sums; one step along a row or column changes the sum by one; colour odd sums blue (chessboard); rows and columns fine; diagonal sums 0, 2, 4 all red: red wins | Goals card on the right; names turn into sums (2+1 becomes 3); odd cells blue; green ticks beside rows and columns; diagonal band turns into a bright red failure | The natural idea and exactly where it fails: the all-star line |
| 3 Repair | Pause. Make 00 blue: diagonal saved, but 00 now neighbours 10 and 01: blue wins. Turn those red. Check all 7 lines: a draw. 12 and 21 share no line. The middle row was rescued by its last cell, 21 | 00 flashes yellow and turns blue; two bright red pair outlines; 10 and 01 turn red; seven bands checked one by one with ticks; "A draw" in teal; dotted link 12-21 labelled "no common line"; gold ring on 21 | A concrete draw: blue = {00, 12, 21}; the repair = add zero, remove sum-one cells |
| 4 Dimensions | Add a dimension: 3 by 3 by 3 cube, 37 lines. No draw possible there (exhaustive search). General board: n digits from 0 to k-1, n dimensions; smallest n with no draw is HJ(k, 2; 2); for tic-tac-toe it is 3 | Oblique cube of 27 dots with two example lines (`*12`, `***`); three random colourings, each with its win outlined; digit boxes with braces; `HJ(k,2;2)` with three labelled parts, then `HJ(3,2;2) = 3` | What the number means, with a case where we know the answer and why |
| 5 Known | Hales and Jewett 1963 (classic version: enough dimensions, no draw). Conlon, Farnsworth and Robertson 2026: answer at most k (upper bound); exactly k for prime k; conjectured always k; computers settled up to 7; 8 left as "7 or 8". New result: for every prime p, `HJ(p+1,2;2) = p+1`. 7 gives 8, 11 gives 12. The work is a draw in dimension p; p = 2 is the board we coloured | Names and years; `HJ(k,2;2) <= k` labelled "upper bound"; table k = 2..8 filled primes first, then 4 and 6, then "7 or 8?" in yellow; the 8 entry becomes 8 in teal; boxed theorem; TransformMatchingTex `p+1 -> 7+1 -> 8`; small draw board labelled p = 2 | Why the result matters and what has to be built |
| 6 Rule | Rule for prime p: blue if the digit sum is one more than a multiple of p; then add the zero cell and remove the sum-one cells. p = 2: sums 0 and 3, our board. p = 3: 4 by 4 by 4 cube, sums 0, 4, 7 (19 of 64 cells) | Number line 0..22 for p = 7: 1, 8, 15, 22 marked as 0+1, 7+1, 14+1, 21+1; 0 added, 1 crossed; 3 by 3 board with sums; four 4 by 4 layers with 19 blue cells | The colouring is the repair story made general |
| 7 Hops | Sums along a line go up in equal steps: middle row 1, 2, 3; diagonal 0, 2, 4. In general sum = S + d a. Example from p = 7: pattern `3*02**0`, d = 3, S = 5, sums 5, 8, ..., 26 (8 is blue). Two jobs. Job 2: blue sums above one are a multiple of p apart, neighbours are d apart (d < p); zero's neighbour has sum d (removed if d = 1, wrong remainder otherwise); all-star line: 0, p, 2p, ..., only 0 blue | Small board with sums copied onto a short number line as hops; pattern with braces "d = 3 stars", "fixed digits add to S = 5"; TransformMatchingTex `S + d a -> 5 + 3 a`; number line 0..49 with the seven blue sums; hops land; camera zooms near zero for the zero-cell case, then out for hops of 7 | Every line is a sequence of equal hops; why no line has two blue neighbours |
| 8 Clock | Job 1: remainders on a p-hour clock; hops of d; 7-hour clock with hops of 3 from 5 visits every hour (hits 1 at the second cell, sum 8). Any hop 1..6 works because 7 is prime; 6-hour clock, hops of 2 from 0 visit 0, 2, 4 only. Snag: sum exactly 1. Case 1: first cell with S = 1, jump to the last cell (all stars = p), sum 1 + d p is blue: why the extra digit p is needed (callback to 21). Case 2: S = 0, line starts at the zero cell. So dimension p has a draw; smaller dimensions by padding with zeros; with the upper bound, `HJ(p+1,2;2) = p+1` | Two clocks side by side with lit visited hours; number line 0..16 with hops 1..8 for S = 1, d = 1; `S + d a -> 1 + d p`; mini middle row 01, 11, 21 with sums 1, 2, 3; inequality `p+1 <= HJ <= p+1` becomes an equality | The single place primality is used and the single place the extra digit is used |
| 9 Eight | p = 7, k = 8: 8^7 = 2,097,152 cells (32,768 boards of 8 by 8). Histogram of digit sums 0..49, blue sums 0, 8, 15, 22, 29, 36, 43 with counts 1, 2,996, 42,252, 124,824, 104,692, 23,898, 924: 299,587 blue. Separate program: 2,685,817 lines, 0 red lines, 0 blue neighbours. This checks one board; the proof covers all primes. `HJ(8,2;2) = 8` | 8 by 8 board with "x 32,768"; bar chart with blue bars and their counts; counters rolling up to the verified totals; boxed `HJ(8,2;2) = 8` | The new case concretely, and the difference between a finite check and a proof |
| 10 Lean | Lean checks every step against the rules of logic. It proves the colouring for every prime, the upper bound, `HJ(p+1) = p+1`, with 8 and 12; no step assumed (no `sorry`, standard axioms only). It cannot check that the definitions match the intended question (a separate review did), nor novelty (bounded literature search), and the paper is not yet peer reviewed | Card with the real theorem statements `HJ_prime_successor` and `HJ_eight`; ticks appear one by one; then two gold question marks with short labels | What "formalised in Lean" does and does not mean |
| 11 Ending | Recap in three points. Still open: k = 9 (8 or 9) and k = 10 (8 to 10); conjecture says k. End card | Three numbered lines; small table for 9 and 10 with yellow question marks; end card with title, "Valyu Research, 2026", folder path, "Narration uses a synthetic voice." | The status of the problem |

## First-time viewer review (GCSE level)

Checked each clip against only what earlier clips have shown.

- "Line" is never used in the technical sense before scene 2 defines it with patterns. Scene 1 says "line"
  in the everyday tic-tac-toe sense, which matches rows, columns and the main diagonal; scene 2 then removes
  the anti-diagonal explicitly so nobody carries the wrong picture forward.
- "Neighbours on a line" is defined with a picture (arcs on one row) before the puzzle uses it. The ends of
  a line are shown not to be neighbours, because the proof depends on there being no wraparound.
- "Digit sum", "odd", "remainder", "multiple of p" and "prime" are GCSE words. "Remainder" is pictured as a
  clock before it carries any argument.
- "Dimension" is tied to "number of digits per cell" (2 digits: board, 3 digits: cube, n digits: n dimensions).
- `HJ(k, 2; 2)` is named only after its meaning is shown, and each part is labelled.
- `S`, `d` and `a` are introduced on one concrete pattern (`3*02**0`) at the same moment as the formula, and
  the formula is transformed into numbers on screen.
- Changes made during this review: "upper bound" was used before it was defined, so scene 5 now says "That is
  an upper bound"; "conjectured" became "guessed"; "n digits" now says "That is n dimensions"; "squares" became
  "cells" throughout so the word still works for cubes; the sum-exactly-one snag is stated before the two cases
  rather than folded into them; one sentence on padding with zeros was kept, because the number is the
  smallest dimension that forces a winner, so draws are needed in every dimension up to p.

## Claims simplified

- The theorem holds for all `k >= p+1` (`HJ(k,2;2) >= p+1`); the video states only the `k = p+1` case and the
  consequences for 9 and 10 that follow from the general bound.
- The geometric comparison (`G(8,2) = 7`, Question D) is omitted: it depends on a computation the Lean proof does
  not cover, and it needs a second kind of line.
- The upper bound proof (`HJ(k,2;2) <= k`) is stated as prior work and as re-proved in Lean, not animated.
- "A search of published work found nothing earlier" summarises the bounded literature review in `readiness.md`
  (originality confidence moderate).
