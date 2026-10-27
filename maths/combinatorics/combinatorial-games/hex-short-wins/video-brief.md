# Video brief: how cheaply can you win at Hex?

Audience: a bright 16-year-old who has just finished GCSE maths. Style: calm, visual, one idea per scene.

## The question in plain words

Hex is a two-player board game on a diamond of hexagons. Blue tries to join the top edge to the bottom edge; Red tries to join the left edge to the right edge. Players take turns colouring one empty hexagon each. We use the ordinary alternating game without a swap rule. Someone always wins, and the first player can always force a win. So ask a sharper question: how *cheap* can the first player's win be made? Two ways to measure it:

- **lambda(n)**: the shortest winning path (number of hexagons in it) that Blue can force on an n by n board.
- **delta(n)**: the fewest Blue stones Blue needs to place to force a win.

In 2004 Garikai Campbell guessed lambda(5) = delta(5) = 7 and lambda(6) = delta(6) = 9. A July 2026 preprint said it had proved lambda(5) = 7. The retained results have different levels of verification:

- lambda(5) = **6**, not 7. Blue opens in the very centre and can always finish with a winning path of just 6 hexagons.
- delta(5) = 7 (Campbell was right here).
- delta(6) = **10**, not 9.
- lambda(6) = 8, not 9. That Red can stop every path of 7 or fewer cells is checked; that Blue can force 8 comes from the search and has not been replayed by the checker.

So the preprint's claimed proof of lambda(5) = 7 is wrong, and the two measures are genuinely different numbers.

## Why anyone cares

- Hex was invented by Piet Hein (1942) and independently by John Nash; it is the classic example of a game where we know who wins but not how.
- "How long must a winning strategy take?" is the game version of asking how efficient a proof can be.
- It is a clean example of a computer settling, and correcting, a pen-and-paper claim, with an independent checker so you do not have to trust the search.

## Smallest concrete example

Start with a 2 by 2 board. Blue opens at (1,2), touching the top edge. Both (2,1) and (2,2) are adjacent to it and touch the bottom edge. Red can occupy only one of those two cells; Blue takes the other and wins with two stones. This is the smallest concrete example of a strategy that changes with Red's reply. Then move to the 5 by 5 board, 25 hexagons. Any top-to-bottom path needs at least 5 hexagons (one per row). Campbell proved Red can always stop a 5-hexagon path. The question was 6 or 7.

The paper's Figure 2 shows the same game with move numbers. Show this final position from an actual game where Blue follows the certified strategy and Red defends as long as possible (rows top to bottom, each row shifted right by half a cell; B = Blue, R = Red, . = empty):

```
R R B R B
 R R . B R
  B R B B B
   B R R R B
    B R B B .
```

Blue's shortest top-bottom path here has 6 cells: (1,5), (2,4), (3,4), (3,5), (4,5), (5,4) (row, column; row 1 at the top). The other six Blue stones went into threats and defences along the way. Red delayed as long as possible; Blue needed 12 stones but the path is still only 6 long. The full game, 23 moves (B = Blue, R = Red, (row, column)): B(3,3) R(1,1) B(2,4) R(5,2) B(5,1) R(4,2) B(5,3) R(4,3) B(4,1) R(3,2) B(3,1) R(1,4) B(1,5) R(1,2) B(1,3) R(2,2) B(3,5) R(2,5) B(3,4) R(4,4) B(4,5) R(2,1) B(5,4). (The script `verification/py/longest_line.py` prints this game move by move.)

## Ideas to build first, in order

1. Hex rules and adjacency: each hexagon has up to 6 neighbours; show the six directions.
2. No draws: a full board always has exactly one winner (a red left-right chain blocks every blue top-bottom chain, and vice versa).
3. Strategy: a rule saying what to play in every situation. "Blue can force X" means there is a strategy that achieves X whatever Red does.
4. Game trees: Blue's choice is "there exists a good move"; Red's choice is "for all replies". Animate a tiny tree with OR nodes for Blue and AND nodes for Red.
5. Maker-Breaker view: list all the short top-bottom paths (on 5 by 5 there are 106 inclusion-minimal path cell sets of at most 6 cells). Blue wants to own one completely; Red wants to put a stone on every one. Red completing its own chain automatically blocks every Blue path.
6. Certificates: instead of trusting the search, write down Blue's move for every position the strategy can reach, and let a separate, simple program try every Red reply.

## Key insight in visual steps

1. Draw the empty 5 by 5 board; Blue stone in the centre.
2. Fade in the short paths through the centre (a few highlighted, the rest faint). Red's job: hit every one.
3. Show Red's reply and the paths it kills (they vanish). Blue's reply keeps at least two "threats" alive. The point: Blue chooses its path *after* seeing Red's moves.
4. Show why the published argument broke: it fixed one path in advance and let Red block it. An adaptive Blue simply switches to another 6-cell path.
5. Zoom out to the checker: a counter ticking through 106,826 positions, each one "Blue move given, every Red reply tried, still winning".
6. Scale up to 6 by 6: Red can stop any win that uses 9 or fewer Blue stones (36 openings, each with its own Red strategy table), but Blue wins with 10 by opening next to the centre.

## Objects that should appear on screen

- The 5 by 5 board with axial layout (rows shifted right). Blue edges top and bottom, red edges left and right.
- The two opening-value maps from the paper (Figure 1): each opening labelled with its value; centre labelled 6 for lambda and 7 for delta.
- The 6 by 6 board with the two winning 10-stone openings marked (the two cells touching the centre on the short diagonal).
- A small table: n = 2, 3, 4, 5, 6; lambda = 2, 3, 5, 6, 8; delta = 2, 3, 5, 7, 10. Old conjectures struck through: lambda(5)=7, lambda(6)=9, delta(6)=9.
- The relation "game length = 2 delta - 1": delta(6) = 10 means 19 moves in total, matching an earlier AI estimate (KataHex, 2024) that was never a proof.

## Proved, computed, open

- Proved by checked certificates: lambda(5) = 6 (with both rule readings below), delta(5) = 7, delta(6) = 10.
- Proved by checked certificates: lambda(6) >= 8 (Red stops every path of at most 7 cells on 6 by 6, whatever Blue opens with).
- Computed by the search but not replayed by the independent checker: lambda(6) <= 8, so lambda(6) = 8.
- Open: the strict-rule value for 6 by 6, lambda(7), delta(7) (the AI estimate suggests 13), and the infinite-strip question delta(5 by infinity).

Two readings of "shortest path": Campbell lets play continue if Blue first joins the edges by a long path; the 2026 paper ends the game at the first connection. lambda(5) = 6 holds under both, so the correction does not hinge on that detail.

## Misconceptions to avoid

- "The computer found one good game." No: the certificate covers every possible Red defence, not one line.
- "Shortest path = fewest stones." No: Blue may need extra stones to force the path; on 5 by 5 the path can be forced with 6 cells but forcing a win with 6 stones is impossible (that needs 7).
- "This solves Hex." No: who wins small Hex boards was already known; this is about how cheap a forced win can be.
- "The earlier paper's authors were careless with the definition." The disagreement is not about the definition; the value 6 holds under both readings. Their hand argument fixed the winning path too early.

## Narration and accessibility handoff

Build each unfamiliar term from the concrete example before showing the formula. Read the key inequality or count aloud and leave it on screen long enough to follow. Use captions matching the spoken narration, and use labels/patterns as well as colour. Keep the proved/computed/open distinction visible in the final scene. Credit the named prior work where its result first appears. Root produces the narrated MP4 and editable video source; this brief does not claim that a video has been produced.
