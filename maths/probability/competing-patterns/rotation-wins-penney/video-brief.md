# The reply that wins by moving one number

## Question in plain words

Two people write different order patterns. A machine draws unrelated random numbers, one at a time. Keep looking at the last four numbers, or the last k numbers in the general game. Whoever first sees their chosen order wins. Can the second player always get better than a 50 percent chance simply by moving the first player's last symbol to the front?

The result proves that this reply wins for every pattern length k at least 3. It need not be the best possible reply. The pattern labels describe relative order, not particular numerical values.

## Why care

Each pattern has the same probability in a single window, yet one can be more likely to appear first. Overlapping windows share observations, so a fair snapshot does not make a fair race. This is a clean example of dependence changing a probability question. It also settles a precise conjecture published by Elizalde and Lin in 2026.

## Smallest useful concrete example

Use four symbols because the key count fits on screen. Player A chooses 2341. Explain this as: second smallest, third smallest, largest, smallest. The numbers 0.2, 0.4, 0.6, 0.1 have that order. Player B moves the last symbol to the front and gets 1234, an increasing run.

Show the stream 0.10, 0.20, 0.40, 0.60, 0.15. Its first window is increasing, so B wins. Its next window has order 2341, so A arrives one draw too late.

Now replace the actual numbers with five movable points x0,...,x4. To see B followed immediately by A requires x0<x1<x2<x3 and x4<x1<x2<x3. The only freedom is which of x0 and x4 is smaller. There are exactly two possible total orders. To see B followed immediately by B requires x0<x1<x2<x3<x4, exactly one order. A followed immediately by B is impossible, as is A followed immediately by A. There are 5!=120 equally likely total orders. The signed difference from this overlap is therefore (2-1)/120=1/120.

This local count motivates the proof. It is not, by itself, the complete winning probability. Do not call 1/120 the final winning advantage.

## Prerequisites to build in order

1. Relative order: turn four actual heights into a permutation of 1,2,3,4.
2. Equally likely orders: four distinct independent observations have 24 possible orders; five have 120.
3. A moving window: adjacent windows share all but one observation.
4. Dependence: sharing numbers changes which event can follow which.
5. Inclusion-exclusion: count events, subtract overlaps, add triple overlaps. Start with two overlapping circles and actual small integers.
6. A chain of overlapping occurrences, called a clump. Separated windows use fresh independent observations.
7. A geometric tail: if each extra step has chance at most r, the total remaining contribution is bounded by r+r^2+...=r/(1-r).

## Proof in six visual steps

1. **Equal snapshots, unequal races.** Display 24 four-point order cards with equal area 1/24. Highlight A=2341 and B=1234. Slide a window over the example stream. Show that equal frequency is not the same statement as equal chance to arrive first.
2. **The first overlap favors the rotation.** Animate the two five-point total orders for B then A, next to the one order for B then B. Cross out the two impossible arrows from A. Display 2-1=1 and 1/120. In general the corresponding advantage is at least 1/(k+1)!.
3. **Control short overlaps with interleavings.** Draw shared points as a black chain and private points as red and blue chains. An ordering is a red-blue interleaving. When the missing ranks differ, swapping all red and blue sends every allowed interleaving to a disjoint set. Therefore at most half of the balanced interleavings can be allowed. Build binomial(2s,s) as choosing the s red positions, then explain the factor 1/2.
4. **Cancel a jungle of marks.** Draw occurrence starts on a time line. Show that many inclusion-exclusion markings cancel. The surviving pointwise coefficient is only -1, 0 or +1. Its cumulative sum stays at -1 or 0. Nonzero signs alternate. Equal signs cannot be less than k starts apart. In any group of k starts, at most two nonzero contributions survive.
5. **Bound everything beyond the horizon.** Group actual occurrences into a connected clump. Add an anchor after skipping k starts. For it to remain in the same clump there must be a new occurrence among k-1 fresh possible windows. Its probability is at most r=2(k-1)/k!. Explain that the candidate windows overlap each other, so the proof uses a union bound, not an independence assertion between those windows. The observations after an anchor's ending time are fresh. Multiply successive necessary-event bounds to obtain a geometric tail.
6. **Close the infinite and finite parts.** Show a number line of lengths: 3 is credited to the original paper; 4,5,6,7 receive exact certificates; every length at least 8 follows from one uniform inequality. At length 8 the general bound leaves at least 218738049/2305503200, approximately 0.094876489, after scaling by (k+1)!. The exact finite comparisons have wide positive gaps. Finally connect the positive signed difference D to B winning more than half the races.

## Exact screen objects and formulas

- Right rotation: 2341 -> 1234; general a1...ak -> ak a1...a(k-1).
- Actual five-number stream: 0.10,0.20,0.40,0.60,0.15.
- Two B-then-A orders: x0<x4<x1<x2<x3 and x4<x0<x1<x2<x3.
- One B-then-B order: x0<x1<x2<x3<x4.
- One-step signed contribution: 1/5!=1/120.
- General one-step lower bound: 1/(k+1)!.
- Two-chain count: product over gaps of binomial(xj+yj,xj).
- Pointwise recurrence: u0=-1; uj= minus the sum of earlier ui whose start is less than k positions back.
- Partial sums of uj: only 0 and -1.
- Root-clump anchor probability bound: r=2(k-1)/k!.
- Finite-cutoff tail: T=(4/k!)r^(q+1)/(1-r), where q is a nonnegative integer and S>=q(2k-2)+k-1.
- Table of scaled partial sums and scaled tails: k=4, >3/4 versus 5/12; k=5, >9/10 versus 4/35; k=6, >49/50 versus 28/71; k=7, >99/100 versus 32/419.
- All-length conclusion: probability that the rotation appears first is strictly greater than 1/2.

## What is proved, computed and still open

Proved: the reply wins for every k>=3 in the independent continuous model. The k>=8 part is a written uniform proof with exact rational bounds. Lengths 4 through 7 use finite exact enumeration with a proved infinite-tail bound. Both implementations reconstruct all integer coefficients for 2952 complement representatives. Length 3 was already treated by exact recurrences in the source and must be credited. A supplementary horizon-18 check independently verifies its strict winning comparisons using two integer recurrences and counts every unresolved case against the rotation.

Still open here: identify the best reply for an arbitrary pattern; find practical closed formulas for all winning probabilities. This work does not settle those questions and does not claim that the rotation is always the best reply.

## Misconceptions to avoid

- The pattern 1234 does not mean the next observations must literally be 1,2,3,4.
- The permutation of the latest window is not enough to justify replacing the independent-observation process by a uniform-rank Markov chain.
- Equal window probabilities do not imply equal first-arrival probabilities.
- The local count 1/120 is a signed cluster contribution, not the final advantage in the race.
- Numerical sampling and a finite list of examples do not prove the infinite statement.
- The tail argument counts only anchors in the root clump. The global sequence of anchors is infinite.
- A winning reply can be worse than another winning reply. The result proves a strict advantage, not optimality.
