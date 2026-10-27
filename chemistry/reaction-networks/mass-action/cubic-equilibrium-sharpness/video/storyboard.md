# Storyboard: How many ways can a chemical soup come to rest?

Finding: for every `n >= 2` there is an `n`-species, `n`-reaction mass action network of rank `n - 1`
with exactly `n` positive nondegenerate equilibria on one stoichiometric class, using sources of at most
three molecules; three is minimal by Banaji and Feliu's quadratic obstruction (`paper.tex`, Theorem 1).
Running example: the `n = 2` network `2X+Y -> X` (rate 1/9), `2Y -> X+3Y` (rate 1), slice `X - Y = 2`,
resting states `(3,1)` and `(6,4)`. Scaled example: the `n = 3` network with curve `(60t^3, 85t^2, 11t^4)`,
slice `-X+Y+Z = 36` and resting states at `t = 1, 2, 3`; then the `n = 4` polynomial. Every number is
taken from `../verification/cubic-sharpness-certificate.json` and reproduced by `check_numbers.py`.

Words used on screen and in narration: "resting state" = positive equilibrium; "slice" = stoichiometric
class; "clean crossing" = nondegenerate; "pair collision" = source molecularity at most two;
"three-body collision" = source molecularity three; "balance curve" = the set where the reaction rates
balance (for `n = 3`, the full positive equilibrium curve).

Colour meaning (fixed for the whole video): X molecules and the X axis blue (`PRIMARY`), Y gold (`WARM`),
Z pink (`EXTRA`); balance curves white; slices grey and dashed; the mixture point, and whatever is being
changed or pointed at, yellow (`SECONDARY`); resting states and successes teal (`ACCENT`); failures,
touches and "only one crossing" red (`WARN`). Water in the tank is dark blue (`SOFT`).

| Scene | Narration summary | Visual | What the viewer now understands |
|---|---|---|---|
| 1 Hook | Mixtures often settle into one state; some can settle into different states depending on the start, like a switch. How many resting states can a small network have, and how complicated must the reactions be? | A flask of drifting blue and gold molecules; two arrows to two smaller flasks, one mostly blue and one mostly gold, with a two-position switch icon; the question in two short lines | The question, in pictures |
| 2 Mass action | Molecules meet and react. Three X and two Y give 3 x 2 = 6 possible meetings, double X gives 12: twice as fast. Rate = rate constant x X x Y (law of mass action). Two X and a Y at once: rate proportional to X squared Y, a three-body collision; at most two molecules in is a pair collision | Box of drifting molecules with one X-Y meeting flashed; then 3 blue and 2 gold discs joined by 6 lines, then 6 blue discs and 12 lines; formula `rate = k X Y`; three discs converging, formula `k X^2 Y`; two labels "pair collision", "three-body collision" | Mass action as counting meetings; what "three-body" means |
| 3 Tank | Tap fills a tank at a steady rate; drain faster when fuller. Level rises until outflow = inflow: an equilibrium (resting state). Plot both flows against level: flat line and rising curve cross at the resting level. Counting resting states = counting crossings; wiggly curves could cross more than once | Tank with tap and drain, in/out arrows whose lengths are the flows, level rising and settling; axes "level" and "flow", dashed flat line, white rising curve, live dots, teal crossing; the curve morphs into a wiggly one crossing three times | Equilibrium = balance of flows, not stillness; equilibria are crossings |
| 4 Two chemicals | The paper's two-species network. First: 2X+Y -> X, so one X and one Y vanish. Second: 2Y -> X+3Y, one X and one Y appear. Rates (1/9) X^2 Y and Y^2. Counter demo 5,3 -> 4,2 -> 5,3: X minus Y never changes, a conservation law | Two rows of molecule discs with arrows and net changes; rate formulas under each row; two counters for X and Y that tick, and a third showing X - Y = 2 that never changes | The running example and what a conservation law is |
| 5 Plane | Mixture = point (X across, Y up). Since X - Y = 2, the mixture slides along a line: the slice. Rest needs equal rates: (1/9) X^2 Y = Y^2 gives Y = X^2/9, the balance curve. Both together: X^2/9 = X - 2, factorises as (X-3)(X-6): resting states (3,1) and (6,4). Both are clean crossings (nondegenerate); a touch vanishes under a nudge, a clean crossing slides | Axes 0..8 by 0..6; yellow mixture point sliding on the dashed slice; equations transform term by term on the right; white parabola drawn; teal dots and labels at (3,1) and (6,4); inset with a clean crossing and a red tangent touch while the slice is nudged | Resting states are curve crossings; the meaning of nondegenerate |
| 6 Question | Banaji and Feliu: n chemicals, n reactions, one conservation law means at most n clean resting states on a slice. Ours reaches 2. Their questions: reached for every n? how many molecules per collision? New result: yes for every n >= 2 with at most three molecules, and three is the least. Two chemicals was already known | Statement card; a row of n = 2..6 with "max n" and a teal tick at 2 and yellow question marks; two questions; the marks turn to ticks; "least: 3"; small "n = 2 known before" | The open problem and the claim, with the prior case credited |
| 7 Pair collisions fail | Puzzle (pause). The reaction removing an X and a Y must have both in its input; with two molecules that is X + Y. Balanced against any other pair collision, the balance curve is a line from the corner, a falling curve, or a flat or upright line; each meets the rising slice once. With 2X+Y the X squared bends it into a parabola: two crossings. A falling slice meets only non-falling balance curves: one crossing. Banaji and Feliu: pair collisions give at most two for bigger networks | The plane again; candidate curves `Y = cX`, `XY = c`, `Y = c`, `X = c` replace each other, one yellow crossing each and a red "1 crossing" tag; then the parabola with two teal dots; a small panel with a falling slice and a rising curve | Why three molecules are needed for two species, and what is cited for larger n |
| 8 Three chemicals | Reactions 2X+Y -> X (1/306000), 2Y+Z -> Y+2Z (1/79475), 2Z -> X+2Y+Z (1/121). X: used by first, made by third; Z: made by second, used by third; so all three rates equal. One free dial t: X = 60t^3, Y = 85t^2, Z = 11t^4. Check: 60^2 x 85 = 306000, so the first rate is t^8; the others too | Three molecule rows with rate constants; X and Z discs highlighted in yellow as their reactions are matched; the curve formula; TransformMatchingTex from `X^2Y/306000` through `60^2 85 t^8/306000` to `t^8`, then the two other rates | Why all resting states lie on one curve, and that the rates are tuned so the numbers cancel |
| 9 Slice for three | Every reaction leaves Y + Z - X unchanged; slice Y + Z - X = 36. Along the curve the quantity is 11t^4 - 60t^3 + 85t^2, a polynomial. It equals 36 at t = 1, 2, 3: three resting states, (60,85,11), (480,340,176), (1620,765,891) | Small table of each reaction's change in X, Y, Z with a zero in the last column; axes t from 0 to 3.3 and value 0 to 90; white curve, dashed line at 36, teal dots at t = 1, 2, 3; table of the three resting states | The same crossing picture, now with a polynomial |
| 10 Descartes | Could a fourth hide? `11t^4 - 60t^3 + 85t^2 - 36 = 0`, signs + - + -, three flips. Descartes (1637): no more positive solutions than sign flips; a touch counts twice, so all three are clean. Factorisation `(t-1)(t-2)(t-3)(11t+6)` on screen. Crossings are robust: shift the slice or rates and they survive | Polynomial large; sign terms coloured, three yellow arcs numbered 1, 2, 3; "at most 3"; factorisation fades in below; then the plot again with the dashed line moving between 30 and 42 and the three teal dots sliding | Why there are exactly three, and that the count is not a fluke |
| 11 Recipe | Inputs 2X1 + X2, ..., 2X(n-1) + Xn, 2Xn: never more than three. Resting states lie on one curve with each concentration a different power of t; the conservation law gives a polynomial with n + 1 terms: at most n flips, so at most n crossings. Backwards: choose the polynomial zero at 1, ..., n; its numbers fix the outputs and rates; the paper proves they are valid. n = 4 polynomial with four flips, zero at 1, 2, 3, 4 | Column of inputs; powers table n = 2: 1, 2; n = 3: 3, 2, 4; n = 4: 5, 6, 4, 8; braces "n + 1 terms" and "at most n flips"; arrow chain "choose zeros -> polynomial -> outputs and rates"; the n = 4 polynomial with four arcs and its zeros | How the construction works for every n |
| 12 Honest | Resting is not stable: in the n = 2 example the flow along the slice runs away from (3,1) and into (6,4) (hilltop and valley). The theorem counts resting states, not stable ones. The conserved quantity has a minus sign, so the slice is unbounded; Banaji and Feliu: bounded slices allow at most two, so this is unavoidable beyond two. Three-molecule limit is on inputs: one output has four. Mathematics, not a lab mixture | The plane with flow arrows along the slice, small hilltop and valley icons; X + Y = const as a bounded segment beside the unbounded slice with an arrow; the n = 3 third reaction with a brace "4 out" | What is and is not claimed |
| 13 Evidence | Written proof for every n, internally reviewed; two independent programs checked the 35 resting states for n = 2..8 exactly. Checks catch formula errors but cannot prove every n. Not yet externally reviewed; bounded literature search | Two cards "proof (every n)" and "computer checks (n = 2 to 8, 35 resting states, exact fractions)"; below, two yellow items "outside review: not yet" and "earlier work: none found, search is bounded" | Proof versus computation, and the status |
| 14 Ending | Recap in three points; open: how many can be stable at once, and whether outputs can be kept small; end card | Three numbered lines; two open questions with yellow marks; end card with the title, "Valyu Research, 2026", folder path, "Narration uses a synthetic voice." | Status of the problem |

## First-time viewer review (GCSE level)

Each clip was read against only what earlier clips had shown.

- "Resting state" appears in the hook as everyday language alongside two settled flasks, and is defined
  properly in scene 3 (flows balance, nothing frozen) before it carries any argument.
- "Concentration" is GCSE chemistry; "rate constant" is named the moment it appears; mass action is
  pictured as counting possible meetings (3 x 2 = 6, then 12) before the formula is shown.
- "Three-body collision" and "pair collision" are defined by the number of molecules going in, so that
  inputs like a single Y count as pair collisions, which is what the minimality statement needs.
- "Conservation law" is shown with a counter that never changes before it is named; "slice" is named only
  after the viewer has seen the mixture point sliding on the line.
- "Balance curve" is named in scene 5 (added during this review: scene 7 used the phrase before it had
  been given a name).
- "Nondegenerate" is introduced as a name for the clean crossing, with the fragile touch shown beside it.
  Scene 10's "a touch would count twice" relies on this and on repeated roots of quadratics.
- `n` is introduced as "n chemicals" with a row of examples n = 2..6, so the general statement is never
  abstract for long.
- "Polynomial" is defined at first use in scene 9 ("a sum of powers"). "Sign flips" is shown before it is
  counted. Descartes' rule is stated, not proved; the narration says it is a rule from 1637.
- "Recipe" is used for the first time in scene 11, where it is shown. In scene 8 the narration only says
  "three reactions" so the word is not used before it means something.
- The hilltop and valley picture for stability is introduced in scene 12 with arrows on the slice, so
  "stable" is never used without a picture.
- Changes made during this review: removed the word "recipe" from scene 8; added "Call it the balance
  curve"; replaced "positive total" with "total mass in a sealed flask"; replaced "factorises" in scene 5
  by an on-screen intermediate step `X^2 - 9X + 18 = 0` so the tidy-up is visible.

## Claims simplified, and choices made

- "Positive nondegenerate equilibria on one stoichiometric class" becomes "clean resting states on a
  slice"; "rank n - 1" becomes "one conservation law"; "maximum source molecularity three" becomes
  "collisions of at most three molecules going in".
- The `n = 2` explanation of why pair collisions fail (scene 7) is an elementary argument written for this
  video, not text from the paper; the paper cites Banaji and Feliu's Corollary 5.16 (and the source states
  the two-species exclusion). `check_numbers.py` corroborates it with a randomised search over every
  two-species pair-collision network with small reaction vectors; the case analysis is: the consuming
  reaction's input must be `X + Y`, so the balance curve is `XY = c`, `Y = c`, `X = c` or `Y = cX`, and
  each meets a rising line at most once; for a falling slice every admissible balance curve is non-falling.
- The hilltop/valley statement for the `n = 2` example (scene 12) is not a claim of the paper. On the slice
  `dX/dt = -(X-2)(X-3)(X-6)/9`; its slope is `+1/3` at `X = 3` and `-4/3` at `X = 6`, which equal the
  certificate's restricted Jacobian determinants; `check_numbers.py` also integrates the flow. The video
  says plainly that the theorem makes no stability claim.
- The persistence statement (scene 10) shows only a shift of the slice level (any level between about
  22.7 and 44.4 keeps three crossings) and says in words that small changes of the rate constants also
  preserve the count, as the paper proves.
- Omitted: the explicit formula for the powers `p_i`, the sign vector and product formula, the restricted
  Jacobian argument (replaced by the clean-crossing picture), the product molecularity bound `2n`, and the
  anonymous full-rank quadratic manuscript.
- "A literature search found no earlier recipe for every n" summarises the bounded priority checks in
  `readiness.md` (originality confidence moderate).
