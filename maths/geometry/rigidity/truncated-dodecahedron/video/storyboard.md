# Storyboard: the truncated dodecahedron is rigid

Audience: a bright 16-year-old after GCSE maths and physics. Running example: the truncated
dodecahedron itself, with the hinged square, the box and two sticks in a line as the small
cases that teach each idea first. Colour meaning, used throughout: sticks white, decagon faces
blue, triangle faces gold, arrows and the thing currently changing yellow, failures and
stretching red, rigid or "passes" green, clock arithmetic teal.

| Scene | Narration summary | Visual | What the viewer now understands |
|---|---|---|---|
| 1 Hook | Four hinged sticks wobble into a rhombus; three sticks keep their shape; "rigid" means no wobble except sliding or turning. | 2D: a square of sticks pushed into a rhombus, a triangle that will not move, then slides and turns as a whole. | What a wobble is, and what rigid means. |
| 2 Solid | In 3D, sticks keep lengths and faces stay flat but may change shape. The box still leans into flat rhombi. Meet the truncated dodecahedron (60 corners, 90 sticks, 20 triangles, 12 decagons). A decagon alone can flex in its plane. Could the whole solid wobble? 31 solids tested in 2026; this one undecided. | 3D: a slowly rotating box shears into a rhombohedron; the truncated dodecahedron rotates; one decagon glows; inset of an equilateral decagon flexing in its plane; "?" | The exact question, and why it is not obvious. |
| 3 Counting | Count numbers minus rules minus whole-body moves: square 8-4-3 = 1, triangle 6-3-3 = 0, solid 276-270-6 = 0, box 42-36-6 = 0 but it wobbles. Euler's formula makes the count zero for every such solid. | 2D: icons with their equations built term by term; box count turns red; V - E + F = 2. | Counting cannot decide; rules can repeat each other. |
| 4 Arrows | A wobble starting gives each corner an arrow. A stick does not change length at first if its end arrows have equal shadows along it. Square passes. This is an infinitesimal flex; the first-order test. | 2D: arrows on the square's corners, one stick with perpendicular "shadow" drops, matching (green) and mismatched (red) cases, check marks. | First-order motion as arrows that keep lengths unchanged at first. |
| 5 Fake | Two sticks in a line, pinned at both ends: sideways arrow passes the first-order test but the joint is stuck. Pythagoras: length sqrt(1 + t^2), too long by about t^2/2 (t = 0.1 gives 1.005). Nudging along the line cannot satisfy both sticks: a second-order obstruction. Tests come in layers t, t^2, t^3. | 2D: pinned sticks, right-angle marks, right triangle with legs 1 and t, numeric check, two conflicting yellow nudges turning red, a ladder of layers. | Why passing the first-order test is not enough; what an obstruction is. |
| 6 SolidFlex | The solid has four independent infinitesimal flexes (mod slides and turns); one is shown. Any mix v0, v1, v2, v3 works. Moving straight along the arrows stretches sticks by about t^2. | 3D: rotating solid with yellow arrows of a real first-order flex (computed from the exact geometry); then the solid moves along the arrows and its edges redden. | The solid passes the first-order test in four ways. |
| 7 Layers | Bending the path cancels every t^2 error (all 40 second-order numbers are zero); this is where the 2026 paper stopped. The remaining errors grow like t^3; four cubic leftovers remain. | 2D: plot of worst stick error against t for the straight path (grows like t^2) and the bent path (grows like t^3), from the real solid, then the same axes zoomed 33 times so the t^3 growth is visible; "all 40 are zero"; four cubic boxes. | Second order is inconclusive; the question is now four cubics. |
| 8 Obstruction | A wobble needs all four leftovers zero at a point that is not all zeros. Toy: x^2 - y^2 and xy. Their zero sets (diagonals, axes) meet only at the origin; x(x^2 - y^2) + y(xy) = x^3. The certificate does the same with four cubics and ninth powers. | 2D: axes with the two zero sets drawn and meeting only at the origin; the algebra transforming term by term with the cancelling terms highlighted; the identity for v0^9. | The key idea of the proof: combine the leftovers into a pure power. |
| 9 Clock | Exact arithmetic is needed: coordinates use the golden ratio (square = itself + 1); rounding can fake a wobble (the 2026 numerical search snapped back). Use a 1009-hour clock: 1000 + 20 = 11; 627^2 = 393129 lands on 628 = 627 + 1; 1009 is prime so division works. | 2D: a solid icon (labelled "illustration") wobbling then snapping back; a clock dial with a hand wrapping round; the 627 computation. | Clock arithmetic and why it is exact and small. |
| 10 Cancel | The first real leftover in clock numbers (649 v0^3 + 692 v0^2 v1 + ... 20 terms). Grid of the 220 terms whose powers add to nine. Adding the four products leaves 201, 182, 161, then 1 lit square: v0^9 with coefficient 1. Same for v1, v2, v3. Higher terms cannot rescue a wobble (Nakayama's lemma). | 2D: the real coefficients; a 20 x 11 grid lighting and going dark with the real counts; three more small grids collapsing to a single square. | The actual certificate, watched cancelling. |
| 11 Transfer | Why a clock answer counts for real numbers: a zero number reads zero, so a nonzero reading proves nonzero. A real wobble would show on the clock too; none shows, so none exists. The reverse fails (1009 reads 0), so a clock can invent a wobble but not hide one; one clock is enough. | 2D: numbers and their clock readings; implication arrows from "real wobbles" to "clock wobbles", then the contrapositive in green; 1009 to 0 in red. | Why one prime is enough, and the one-way nature of the transfer. |
| 12 Status | Proved: local rigidity, no small wobble, nearby shapes are congruent. Says nothing about far-away shapes. Computer-assisted: an independent exact program rebuilds and checks every identity in under a second. The deductions are written and internally reviewed, not Lean-checked, not yet externally refereed. | 3D: the solid rotating with one or two short status lines at a time. | Exactly what is and is not established. |
| 13 Recap | Three points; what is still open; end card. | 2D: three recap lines, two open-question lines, end card with title, "Valyu Research, 2026", folder path, synthetic-voice line. | The whole story in three sentences. |

## First-time viewer review

Checked each clip against what has already been shown:

- "Rigid", "wobble", "rhombus", "decagon", "infinitesimal flex", "first-order test",
  "second-order obstruction", "leftover", "certificate" and "clock" are each pictured before or
  as they are named. "Certificate" is defined in the same sentence ("a list of numbers anyone
  can check").
- "Degree" was replaced by "terms whose powers add up to nine", with an on-screen example.
- "Each face's plane needs three numbers" is supported on screen by "tilt: 2, position: 1".
- "About half of t squared" gets a worked number (t = 0.1: the square root of 1.01 is 1.005).
- The four flex amounts v0 to v3 are named on screen when the mix is introduced, before the
  cubics use them.
- The 2026 paper's own numerical deformation is not reproduced; the "snaps back" picture uses
  the real flex and its second-order correction and is labelled as an illustration.
- Clock wobbling is simplified: on a finite clock a "wobble" means a family of nearby solutions
  rather than an isolated one. The narration keeps the word "wobble" and says the step is made
  precise in the paper.

## Sources for every number

All figures come from `../paper.tex`, `../proof.md`, `../verification/independent_verification.json`,
`../verification/modular-obstruction.json`, `../verification/pure-power-certificate.json` and
`../verification/cubic-obstruction.sing`, plus `data_prep.py`, which recomputes:

- 60 vertices, 90 edges, 32 faces; 276 variables, 270 equations plus 6 gauges; rank 272 over
  F_1009; 4 infinitesimal parameters; 40 zero quadratic coefficients; 80 cubic coefficients.
- The real first-order flex space modulo rigid motions has dimension 4 (numerical SVD; the four
  near-zero singular values are below 1e-11, the next is 0.042). The flex drawn in scene 6 is one
  element of it; the plot in scene 7 uses its real second-order correction (residual 4e-15).
- Running sums for the v0^9 identity: 201, 182, 161 and finally 1 nonzero coefficient out of
  220 (for v1: 200, 179, 161, 1; v2: 199, 181, 160, 1; v3: 200, 179, 160, 1).
- 627^2 = 393129 = 389 x 1009 + 628.
- The source paper, Adrian-Himmelmann, Winter and Zhang, arXiv:2607.09252 (retrieved
  25 October 2026): 31 Platonic, Archimedean and Catalan solids tested; only the truncated
  dodecahedron undecided; 4-dimensional first-order flexes; all quadratic forms identically
  zero; a numerically found deformation converged back to the symmetric solid under a more
  robust scheme.
