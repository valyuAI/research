# Storyboard: every symplectic billiard path in a special octagon repeats

Audience: a bright 16-year-old after GCSE maths and physics. Running example: the special
octagon O(5,6,1,2) (the rectangle 5 x 6 with bottom corners cut 2 squares in and top corners
1 square in), with the rectangle 4 x 3 used once to teach the rule and the lopsided octagon Q
for the counterexample. The worked coordinates, counts and periods are recomputed by
`check_numbers.py` from the paper's own exact library (`../verification/symplectic_billiard.py`).
The 20,000-point filled-set exploration and 1484-tuple campaign count are reported from
the stored verification results, with their limits recorded in `sources.md`.

Colour meaning, used throughout: table edges white; path chords blue; even points gold; odd
points lavender; the side or quantity currently in use yellow; critical (corner-born) points
and failures red; success and whole-number dots green; half-grid dots blue (slanted sides) and
orange (top and bottom); the mirror line dashed grey.

| Scene | Narration summary | Visual | What the viewer now understands |
|---|---|---|---|
| 1 Hook | A point hops around an octagon on squared paper by one rule; after 92 hops it is back. Luck, or does every path return? | O(5,6,1,2) on a grid; the real period-92 orbit from (7/3, 0), (11/3, 2/3) drawn chord by chord with a moving dot; the start flashes on return; question on the right. | The question, as a picture. |
| 2 Billiards | Ordinary billiards: angle in = angle out. From (1/2, 0) at 45 degrees the ball returns after 14 bounces; with slope root 2 it never repeats; switch from equal angles to the parallel-line rule. | 4 x 3 table; equal-angle marks at the first bounce; the closed 14-bounce path; then a root-2 path filling the table; a short caption introduces the new rule. | What "repeating path" means; that it is a real question. |
| 3 Rule | Symplectic billiards (Albers and Tabachnikov, 2018): x2 is the other end of the chord through x0 parallel to the side containing x1. In the 4 x 3 rectangle: (1,0), (4,2), (1,3), (0,2), back to (1,0). Periodic = returns exactly. Even and odd points form two chains, each steering the other. | The side of x1 glows yellow, a copy slides parallel until it passes through x0 and extends to x2; repeated twice; the inscribed rectangle; even dots gold, odd lavender. | The exact rule (the paper's definition), periodicity, and the even/odd chains. |
| 4 Octagon | Build O(5,6,1,2) by cutting corners; its 8 side lines all have whole-number constants; mirror x = 5/2; definition of special octagon; the 2019 experiments and conjecture (only computer evidence). | Rectangle morphs into the octagon; 8 equations with constants in yellow; dashed mirror; gallery of six real orbits with periods 4, 16, 32, 44, 68, 92; conjecture card. | What a special octagon is and what was conjectured. |
| 5 Corners | A corner sits on two sides, so the rule breaks there; corners split nearby paths; critical points = even points of paths starting at a corner; the 46-step path from (2,0) to (3,0); in total 20 red dots. | Corner with two yellow sides and "?"; two vertical chords from points beside (4,1) landing on different sides; the real corner path with red dots dropped at even points; all 20 red dots and a counter. | Why corners matter, and the critical set C (here 20 points). |
| 6 Boxes | Unroll the boundary; a moment of a path is a pair (where it is, where it goes next) = a dot in a square; red lines cut it into fewer than 400 boxes that each travel as one piece; the period-16 box visits 16 boxes and returns; group by the entire side sequence, with at least one box in each region; finitely many regions and reversibility force a return; two return laps separate the coordinates and four undo the flips. Criterion due to Albers, Lander and Westermann. | Octagon sides fly into a straight line with red dots; the line becomes both axes of a square with 20 x 20 red grid lines; a yellow box hops through 16 real boxes and returns; regions explained beside the example grid; a small box flips but does not stretch; two/four return-lap captions. | Finitely many red dots implies every path is periodic (the pigeonhole idea). |
| 7 Naive | Sliding from corners in all four directions catches every red dot, but after 20,000 points it has still not stopped and fractions keep getting finer (denominators up to 16384); the filled set has not closed after 20,000 sampled points; this does not prove infinity. | Dots appearing in batches on the octagon edge with a counter of points and the finest fraction; red "after 20,000 points: not finished". | Why a different idea is needed. |
| 8 Dots | The half grid; three kinds of dots: green (whole), blue (half/half on slanted sides), orange (half x on top and bottom): 16 + 6 + 4 = 26. Key lemma: even points of paths from corners land on these dots; all 20 red dots do. | Faint half-grid; green, blue, orange dots appear with counts; red rings on the 20 critical points. | The statement of the new lemma. |
| 9 Why | Each slide keeps one number fixed. Slope hop (2,0) to (5,3) keeps x - y = 2. Sideways hop = mirror x -> 5 - x. From (0,4): x + y = 4 meets x - y = 3, add and halve: (7/2, 1/2), blue; never quarters. Upright hop to (7/2, 6), orange. Danger: a slanted hop would give (5, 9/2) then (5/4, 3/4). Rescue: x13 = (5, 112/25) on the right side, x15 = (0, 112/25) its mirror, so the next even hop is upright again, to (7/2, 1/2). | Four direction arrows with "keeps x", "keeps y", "keeps x - y", "keeps x + y"; the real red path step by step; equations transforming term by term with the spoken term highlighted; grey dashed hypothetical crossed in red; lavender odd points mirrored. | The key step of the proof, including why the mirror is needed. |
| 10 Conclude | 26 dots, so finitely many red dots, so every path is periodic; same for every special octagon; bound 2600 hops versus 92 observed. | Three-step chain of implications; N = 4W + 2H - 2(c1 + c2) = 26; 4(N^2 - N) = 2600 next to 92. | The theorem and its explicit bound. |
| 11 Lopsided | Q = (1,0),(3,0),(4,1),(4,4),(3,5),(2,5),(0,3),(0,1); the 6-loop (4,11/3), (5/3,0), (2/3,11/3), (4,7/3), (2/3,1/3), (5/3,14/3); nudging x0 doubles and flips (1/24, -1/12, 1/6, -1/3, thrown off); nudging x1 halves and flips (1/4, -1/8, 1/16, -1/32); that path creeps toward the loop forever, so not every path is periodic. | Q on a grid with the loop; yellow nudged copies lap by lap with the offsets as fractions; the odd point converging. | The mirror hypothesis cannot be dropped. |
| 12 Status | Written proof, internally reviewed, not externally refereed; high correctness confidence, originality less certain and search does not establish priority; two independent exact programs checked 1484 parameter tuples, including rescaled copies (sizes up to 14), a check not the proof; symmetric Hexhouse corollary (X(3,2,1,2) stretched by 2 becomes O(6,5,2,0)); open problems. | Status list with ticks and open circles; Hexhouse stretching into the cut-corner hexagon; open list. | What is proved, what was computed, what is open. |
| 13 Ending | Three-point recap; what we still don't know; end card. | Three recap lines; open questions; end card with title, Valyu Research, 2026, folder path, synthetic voice line. | The whole story in their own words. |

## First-time viewer review (GCSE level)

- "Periodic" is shown (rectangle path closing) before it is named; "even" and "odd" points are
  shown as two coloured chains before they are used.
- The rule is the paper's definition, read as: "x two is where the line through x zero, parallel to
  the side of x one, meets the edge again". It is demonstrated on the 4 x 3 rectangle with real
  coordinates before the octagon appears.
- "Critical point" is introduced as a red dot left by a path that starts at a corner, after the
  viewer has seen why corners break the rule. The name "critical" is used once only.
- The box argument (scene 6) first shows the exactly checked period-16 box. It then explicitly
  distinguishes the general side-sequence regions, each containing a box. Two return laps
  separate the even/odd coordinates; boundedness in both time directions forbids non-unit
  stretch, and four return laps undo flips. The video illustrates the criterion rather than
  reproducing its boundary-point and connectedness arguments; those remain in paper.tex.
- "Half grid", "slide keeps a number fixed" and "mirror image" are each shown with a picture and
  real coordinates before they are used in the argument. The quarter-point danger is shown as a
  grey hypothetical with a red cross, then the real odd points show why it cannot happen.
- Fix applied after review: the counting formula N = 4W + 2H - 2(c1 + c2) is shown on screen but
  only described in words ("a simple formula"), so no new letters need to be read aloud.
- Fix applied after review: the lopsided octagon is described as "not every path is periodic",
  which is exactly what the counterexample shows; the narration does not claim anything about
  other lopsided shapes.

## Finalization audit, 26 October 2026

- “Every path” is explicitly restricted to paths defined for all time, forwards and backwards.
- The example has 26 allowed half-grid points, of which 20 are critical. Other octagons have
  different finite counts. The general proof uses the formula displayed in Conclude.
- 92 is a reported sampled period, not a proven upper bound on every observed type; 2600 is
  the proved bound for this example. The filled-set computation proves no infinity statement.
- Removed the stale ordinary-billiard triangle-open-problem assertion. The remaining general
  question explicitly says symplectic billiards and convex polygons.
- The asymmetric example illustrates the local forward contraction. The paper separately
  proves backward existence outside a countable exceptional set; the video does not claim its
  displayed rational nudge supplies that entire backward-existence proof.
- Each factual layer and retained limitation is mapped in sources.md. No audience test or
  listening review is claimed. Source and 480p preview at intake remain in audit/intake/.
