# Storyboard: why loops of states respond in a predictable way

Running example: the driven triangle. States 0, 1, 2 in a ring; clockwise hops rate 2, anticlockwise
hops rate 1. Knob: the rate of the hop 0 to 1. Every number on screen is recomputed by
`check_numbers.py` (which also writes `numbers.json`, read by `scenes.py`) or quoted from
`../verification/*.json` through that script.

Colour meaning: states are blue discs; the root of a tree has a teal ring; tree arrows white; the
nudged arrow 0 to 1 and anything currently changing is yellow; red is failure, look-alikes and
contradictions; teal/green is success (uniquely constructable families, ticks). From scene 9 on, the
three edges of the ring carry fixed token colours (edge {0,1} orange, edge {1,2} lilac, edge {2,0}
maroon), and a tree family is drawn as three chips coloured by the edge each root cuts.

| Scene | Narration summary | Visual | What the viewer now understands |
|---|---|---|---|
| 1 Hook | Molecular machines flip between states; the simplest is a ring of three; turn a knob, how do the time fractions shift, how far can they? Fancher and Horowitz guessed an answer; we prove it for a family of networks and find where the method breaks | triangle of states with a hopping dot; a dial next to the arrow 0 to 1 turns; question in one line | The question |
| 2 Hopping | Arrows are hops with rates (2 clockwise, 1 back); a simulated dot; stopwatch fractions settle at 1/3 each: the steady state pi; one net clockwise hop per second summed across all three edges (one third per edge) | rates on arrows; dot hops along the seeded trajectory; three bars of time fractions converging to a dashed 1/3 line; "net current" arrow | Markov jump network, rates, steady state, not equilibrium |
| 3 Trees | Trees pointing at a root; on a ring, cut one edge and point the rest at the root; weights 4, 2, 1 for root 0 | build one tree arrow by arrow; then the three root-0 trees side by side with products 2 x 2 = 4, 1 x 2 = 2, 1 x 1 = 1 | Rooted spanning tree, weight |
| 4 TreeTheorem | pi_j proportional to total tree weight; 7, 7, 7 gives 1/3; each root's lottery 4/7, 2/7, 1/7 | formula pi_j = W_j / (W_0+W_1+W_2); three totals; probabilities appear under the trees | Markov chain tree theorem; tree lottery P_j |
| 5 Knob | 1 percent faster 0 to 1: trees using it get 1 percent heavier; totals 7, 7.06, 7.04; pi changes -0.47%, +0.38%, +0.1%; rule: share using the arrow (0, 6/7, 4/7) minus average 10/21 gives (-10, 8, 2)/21 | 3 x 3 grid of trees, arrow 0 to 1 yellow, weights tick up; totals; equation transforms term by term | Response = per-root share minus average |
| 6 Families | Pick a tree per root: 27 families; score of a family; example (cut 0, 1, 2) scores (-2/3, 1/3, 1/3); independent average = response; plot: 27 families land on 4 points, response inside | one family row of three trees with 0/1 marks; plot with axes "relative response of pi_0", "relative response of pi_1"; dots; hull; response dot | Eq. (5): response is a weighted average of building blocks; convex hull |
| 7 Conjecture | Bags of arrows; two families with the same bag; 18 bags, 11 UC; the guess; on the triangle it removes the corner (-1/3, -1/3), which only look-alikes reach; FH proved 3 states | two family rows pour arrows into bags; bags equal; counters 27, 18, 11; hull shrinks to the UC triangle, removed corner red | Uniquely constructable; the Fancher-Horowitz conjecture |
| 8 Reframe | Independent lotteries pick a look-alike 44% of the time (152/343); the score at root 1 depends only on root 1's tree; goal: a shared lottery with right odds at every root, only on UC families; pause | red 44%; the three score parts each linked only to their own root; goal written as two short lines | Why a coupling of the root lotteries suffices (Lemma 2.2) |
| 9 Staircase | A ring tree = the cut edge; sliding the cut flips one arrow, weight halves, for every root; staircase 1, 1/2, 1/4, 1/8, 1/16; windows of 3 for roots 0, 1, 2; once round drops by 8 | ring with the cut moving and one arrow flipping; bar chart on a doubling scale coloured by edge; three window brackets | Cycle identity w_r(k) = c_r lambda_k |
| 10 Tokens | Gumbel-max trick on root 0 with tally 4/7, 2/7, 1/7; one token per edge on all bars of that edge; each window sees each token once; seeded draws; 7 families at 1/7 each; balance of 1, 2, 4 families equals the response | bars with bonus blocks; tally bars converging; tokens copied onto matching bars; winners per window; family chips; tally of 7 families converging to 1/7; three plot points with 1, 2, 4 coins and a balance point | The edge-Gumbel coupling and that it reproduces the response |
| 11 WhyUC | A doubling-scale bonus is a positive multiplier a, b or c; divide both rates on each edge by its multiplier; a tree cutting a has weight w/(bc) = wa/(abc), so the common denominator cancels and each chosen tree is strictly heaviest; same bag means same weight; a look-alike must use a lighter tree, contradiction | one coloured triangle and the cancellation w/(bc) = wa/(abc), then three chosen trees with crowns; a look-alike with one lighter tree; scales tipping; red cross | Dominant families are UC (FH Lemma 4) |
| 12 Cactus | Any ring size; cactus = rings sharing single states plus branches; trees split per ring; independent tokens per ring, glue | 6-ring with cut; cactus (triangle + square at one state + a branch); pieces separate and rejoin | Main theorem for cacti |
| 13 K4 | K4: 16 trees per root, 65,536 families, 346 UC; +/-1 labels on 64 pairs; UC families score 0, 2 or 4; root-lottery average -0.0566; contradiction; spreads to connected bidirected networks with a K4 minor for some positive rates; not a refutation, 150 searches | K4; 4 x 16 grid of + and - cells; one UC family's four cells; row averages summing to -0.0566; subdivided K4 shrinking; network containing K4 | The obstruction and its scope |
| 14 Status | Proved for cacti; K4 exact certificate; minor extension written; not refereed, not Lean; open beyond cacti | list with ticks and open circles | How much to trust it |
| 15 Ending | Recap in three points; open: general guess, the diamond (edge tokens fail, error 0.06, but shared lotteries seem to exist); end card | three lines; diamond picture; end card | The whole story |

## First-time viewer review (GCSE level)

- "Rate" is introduced as how often a hop tends to happen while occupying its starting state, before any formula. No
  exponentials or calculus are used; the response is introduced as the limiting "relative percent change per percent of
  nudge" through a concrete 1 percent nudge, and the exact numbers -10/21, 8/21, 2/21 are then
  shown to follow a simple rule (share minus average). The finite-difference values -0.474%,
  +0.379%, +0.095% approach the infinitesimal rule as the nudge shrinks (checked in `check_numbers.py`).
- "Tree" is shown (one arrow out of each non-root state, all paths reach the root) before it is
  named; on the ring it is "cut one edge", which is all the viewer needs later.
- The tree theorem is stated, not proved (it is classical), and checked against the simulation.
- "Building block" and "weighted average lands inside the shape" are shown on a 2D plot with the
  real points before the conjecture is stated, so "weighted average of UC building blocks" uses
  only words already introduced. The plot uses the relative responses of pi_0 and pi_1; the narration says why
  two numbers suffice here (they add to zero because pi is uniform).
- "Uniquely constructable" is defined through the bag picture, with a real look-alike pair
  (cuts (0,1,1) and (1,1,0)).
- Log scale is avoided by name: bars "count doublings" of the weight. The Gumbel distribution is
  named and shown as a lopsided curve; its key property (winner chance proportional to weight) is
  stated and demonstrated by the seeded tally, not proved.
- The K4 argument reuses the scene 8 principle (an average of per-root parts only depends on each
  root's own lottery), so the contradiction needs no new idea.

## Simplifications

- The paper works with any perturbation of the log-rates (sensitivities d_a); the video uses one
  knob (the rate 0 to 1). The weights 1/7 do not depend on the knob, which is said only implicitly.
- "Strongly connected networks with missing arcs and parallel arcs" (Lemma 3.3) are not mentioned;
  the cactus scene shows bidirected cacti.
- The minor extension explicitly requires a connected network with hops allowed both ways on
  every link. It asserts bad rates exist, not that all rate choices fail.
- The hierarchy (i)-(iv) of Section 5 is compressed to "the guess asks for much less than a shared
  lottery".
- The convex-hull picture is drawn for this knob only; the conjecture quantifies over all knobs.

## Finalization audit, 26 October 2026

- A finite 1% change is an illustration. The exact response vector is the infinitesimal relative
  change, and the plot labels and narration now say so. The unweighted average is valid in the
  symmetric example because the unperturbed stationary probabilities are each 1/3.
- The new rates use the same multiplier on both directions of each edge. The explicit
  w/(bc) = wa/(abc) calculation fills the missing causal step in WhyUC. The displayed Gumbel
  bonuses are scaled by 1/log(2), consistently with bars counting doublings.
- “Steady state = tree count” is corrected to weighted tree totals. Arbitrary rates do not give
  uniformly weighted trees. Cactus gluing explains the root orientation and product weights.
- Numerical searches and Monte Carlo tallies are evidence for sampled instances only. The
  seven-family probabilities and K4 negative expectation are exact calculations, replayed by
  check_numbers.py. The minor extension is a written proof, not a full enumeration of graphs.
- Correctness confidence is high after the recorded internal reviews; originality is less
  certain. No earlier result found is not a proof of novelty. No external peer review or Lean
  verification is claimed. See sources.md for the evidence ledger.
- The construction and proof are illustrated on bidirected simple graphs. Missing arcs,
  parallel arcs and the compactness limit are handled in the paper, not animated here.

- Final encoded-frame review found two labels crossing the Families hull. The horizontal-axis label now sits below the plot and the response label below the star; the repaired scene was re-rendered and checked in the full final encode.
