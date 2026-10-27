# Video brief: Why twenty-five knots need four bridges

Audience: a bright 16-year-old who has finished GCSE maths or physics. Target: a five-minute narrated visual explanation. Use clean strand drawings and eight numbered dots. Introduce each algebraic idea with a physical action on the dots before showing notation.

## The question in plain words

A bridge is a hump of a knot above a horizontal plane. The bridge number is the fewest humps possible after reshaping the knot without cutting it. A knot diagram may show four humps, but it does not rule out another drawing with three. A current table marked 293 thirteen-crossing knots as either three-bridge or four-bridge. We now have exact four-bridge certificates for twenty-five of those entries. Two other certificates check trefoil cables whose answers were already known.

Why it matters: bridge number is a basic measure of how hard a knot is to untangle geometrically. The proof also establishes, for these twenty-five knots, that four little loops around strands are needed to generate the knot's group. That is one instance of the meridional-rank conjecture, not a solution of it.

## Prerequisite ideas, in order

1. A knot is one closed strand in 3D. A flat diagram marks which strand passes over at each crossing.
2. Counting humps in one drawing gives an upper bound. A lower bound must work for every possible drawing.
3. A meridian is a tiny loop around a strand. At a crossing, the loop labels before and after the underpass are related by conjugation. For this video, show conjugation as relabeling numbered dots.
4. A permutation is an action on eight dots. A double transposition `(01)(23)` swaps dots 0 and 1 and, at the same time, swaps dots 2 and 3. The other four dots do not move.
5. Put one value from `F2 = {0,1}` on each dot. A vector fixed by `(01)(23)` must have equal values on 0 and 1, and on 2 and 3. This is two independent equality requirements. If all eight dots are connected by the actions, a vector fixed by every action has the same value on every dot, imposing seven independent requirements.

## Smallest worked example with exact numbers

Use `13n_1005` as the main knot. At its first PD crossing `[3,1,4,26]`, the incoming underarc carries `(01)(23)`, the overarc carries `(01)(34)`, and the outgoing underarc carries `(01)(24)`. Animate the overarc permutation relabeling the underarc permutation:

`(01)(34) (01)(23) (01)(34) = (01)(24)`.

Show this with two swapping pairs of dots, then return to the knot crossing. It is one of thirteen checked crossing relations for this knot. A saved checker verifies all thirteen.

Its four seed arcs are `0, 3, 7, 4`, with permutations `(01)(23)`, `(01)(24)`, `(03)(56)`, `(07)(15)`. Draw eight dots and connect each swapped pair with a line. All eight dots belong to one connected network. The four seed permutations generate a group of 20,160 even permutations, all of `A8`; this group-order fact is checked but the bridge proof needs only connectedness.

## Key insight in five visual steps

1. **The apparent gap.** Put `[3,4]` next to `13n_1005`. Show a four-hump drawing. The animation says: we can make four humps, but can we ever make three?
2. **The eight-dot witness.** Highlight `(01)(23)` as two independent constraints on eight dot-values. Show the other three seed actions connecting the network.
3. **The lower bound.** If three meridians generated the knot group, their actions could force at most `3 x 2 = 6` independent equalities. The eight-dot action needs seven. Display `6 < 7`, then `μ ≥ ceil(7/2) = 4`. The values on the dots are bookkeeping for an algebraic representation, not physical dots on the knot.
4. **The upper bound.** Start with the four seed arcs on the actual `13n_1005` diagram. At a crossing, a colored overarc and one colored underarc let the other underarc become colored. Animate the exact `(crossing, new arc)` sequence: `(3,2), (1,1), (2,5), (4,6), (6,11), (7,9), (8,8), (10,10), (11,12)`. All thirteen arcs become colored. A published theorem converts this four-seed coloring into a four-bridge drawing, so `b ≤ 4`.
5. **The census.** Combine `4 ≤ μ ≤ b ≤ 4`. Then zoom out to a compact list of twenty-four knots certified by double transpositions plus `13n_4645`, certified by 3-cycles. Display `25 removed from the pinned 293-name list; 268 entries remain on that list`.

## Exact figures and formulas on screen

- One thirteen-crossing diagram for `13n_1005`, with PD crossing `[3,1,4,26]` enlarged.
- Eight dots numbered `0` through `7`, the four seed permutations above, and the first-crossing conjugation equation.
- Four seed arcs `0,3,7,4` and the nine coloring moves in the stated order.
- `rank(P-I)=2` for either a double transposition or a 3-cycle; `codim(fixed space)=7` when the eight-point action is transitive.
- `3 x 2 = 6 < 7`, `μ ≥ 4`, `b ≤ 4`, and finally `b=μ=4`.
- A small final note that `13n_4587` and `13n_4639` are trefoil cables with prior known values, so the new count is twenty-five, not twenty-seven.

## What is proved, computed, and still open

The rank inequality and the implication from a four-seed coloring to a bridge upper bound are mathematical theorems. The permutations, all crossing relations, coloring moves, exact ranks, and group orders are finite computations with saved certificates checked in two independent ways. A separate finite screen found no overlap with the earlier rank-four `A4`, `D4` and `H4` reflection certificates. The result gives exact values for twenty-five named knots relative to the pinned release and KnotInfo snapshot. It does not classify all bridge-four thirteen-crossing knots or exclude every broader family theorem. The residual list is a ledger, not a proof that every remaining value is genuinely unknown.

Avoid these misconceptions: a four-hump picture by itself does not rule out three humps; the eight dots are algebraic test objects; a 3-cycle is not two swaps; the two cable knots are confirmations, not new discoveries. KnotInfo leaves its Conway, Montesinos and pretzel notation fields blank for all 9,988 thirteen-crossing entries, so those blanks do not classify the knots.
