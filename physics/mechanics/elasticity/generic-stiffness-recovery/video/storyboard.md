# Storyboard: recovering a material's stiffness from wave speeds

Audience: a bright 16-year-old after GCSE maths and physics. Running example: the paper's
synthetic test crystal (the reference tensor in
`../verification/numerical-illustration/`, no symmetry at all), with a box-symmetric twin
pair and the paper's isotropic witness as the two small side examples.

Colour meaning, used throughout: our crystal and anything belonging to it blue; a competing
or twin table gold; the half-gap D pink; the thing currently changing yellow; failure or
"not enough" red; success green; springs, balls and plain text white or grey.

| Scene | Narration summary | Visual | What the viewer now understands |
|---|---|---|---|
| 1 Hook | Tapping a crystal sends out a ripple; in many materials it is not a circle (wood grain, rocks in the Earth). Question: from speeds in every direction, can you work out what the material is? Pause. | A block with faint grain lines; a tap; an oval ripple spreading faster along the grain; then arrows of different lengths in many directions and a one-line question. | The question, as a picture. |
| 2 Springs | A spring pushes back when squashed; how hard per unit squash is stiffness. A solid is balls and springs; a squash passed along is a sound wave. Stiffer is faster, heavier is slower: speed squared = stiffness / density, so only the ratio is visible. | Two springs squashed equally with long and short push-back arrows; a chain of balls carrying a pulse; two chains racing; the formula. | Stiffness, waves, and why density cannot be separated. |
| 3 Waves | Three kinds of wave (push-pull, two sideways shakes), three speeds per direction. Stiff springs one way: a flat wave runs faster along them. Arrows of length = speed trace a curve; "anisotropy". | Three rows of balls moving in the three ways; a spring grid (thick horizontal, thin vertical); two flat wavefronts racing; arrows sweeping out a closed curve. | Direction-dependent speed and the curve of speeds. |
| 4 Surface | In 3D the tips trace a surface: the fastest wave's surface for our crystal, an imaginary no-symmetry crystal from the paper's test files; lumpy because stiffness varies with direction. | Rotating 3D surface of the fastest phase speed (computed from the 21 numbers; range 1.54 to 2.33). | What the data look like. |
| 5 Slice | Each kind of wave has its own nested surface; a slice through all three. One over speed is slowness, same information. | Three nested curves in one plane through the crystal. | Three nested surfaces = the measurement. |
| 6 TwentyOne | Six ways to deform a cube (three stretches, three skews); each can push back in all six ways: a 6 x 6 table, symmetric, so 6+5+4+3+2+1 = 21 unknowns. | Six small cubes deforming one at a time; the 6 x 6 table of our crystal filling in, the lower half greyed as a mirror, row counts 6,5,4,3,2,1 adding to 21. | Twenty-one unknowns, with a real table. |
| 7 Summaries | Straight up: speeds 1.12, 1.42, 1.69; squares 1.244, 2.015, 2.841; summaries sum 6.1, pairs about 11.8, product about 7.1. Summaries are equivalent to the numbers (toy: add to 5, multiply to 6 gives 2 and 3). The sum is a formula 7.1x^2 + 6.3y^2 + 6.1z^2 - 2.4xy - 1.1xz + 0.7yz fixed by six numbers; straight up gives 6.1. Pairs: 15 numbers; product: 28; 49 in all, all set by the 21. | An upward arrow; speeds, squares and summaries appearing in columns; the toy puzzle; the formula with its six coefficients highlighted, then x = 0, y = 0, z = 1 substituted; three triangles of 6, 15 and 28 dots. | What the measurements are as numbers, and how many there are. |
| 8 Twins | 49 vs 21 seems enough, but x^2 = 4 has two answers. Two box-symmetric tables that differ in two entries have identical speeds in every direction (illustration). De Hoop, Ilmavirta, Lassas and Varilly-Alvarado proved 2D; 3D is their Conjecture E. | "49 > 21" then x^2 = 4 with two answers in blue and gold; two tables side by side with the two differing entries yellow; their speed curves drawn exactly on top of each other; a short conjecture card. | Why counting is not enough, and the precise question. |
| 9 Result | The paper proves Conjecture E: a typical material has no twin, even among impossible tables. 22 numbers suffice: 6 + 15 + 1. Typical = outside a thinner set, like a curve on paper; a dart misses with probability one. | Blocks 6 + 15 + 1 = 22; a sheet with a red curve and darts landing off it. | The theorem and what "typical" means. |
| 10 Split | Two tables A, B with the same data; midpoint M and half-gap D; 21 + 21 dials. Test 1 leaves D 15 dials. Test 2: 15 straight-line equations for M; if all genuinely different, M keeps 6; 15 + 6 = 21. Test 3 (one product) cuts to 20 unless automatic. The paper's witness: M = 0, isotropic D; straight up D gives -1, -1, 2 and -D gives 1, 1, -2; sums 0 and 0, pairs -3 and -3, products 2 and -2. | Points A (blue) and B (gold) with midpoint M and pink arrows +D and -D; dial counters ticking 21 to 15 and 21 to 6; total 21 then 20; a small table of the witness numbers with green ticks and a red cross. | The proof's bookkeeping, with real numbers. |
| 11 Balance | Equations can repeat (x + y = 2 and 2x + 2y = 4). With only r genuine equations M keeps 21 - r dials. Key result: those half-gaps have at most r - 1 dials. (r - 1) + (21 - r) = 20. Bars for r = 15 down to 6 all stop at 20, below 21; nothing below 6 except zero. So all twin pairs fill at most 20 dials: a typical material has none. | The repeated pair of equations; 15 equation strips with some greyed; the cancellation done term by term; a stacked bar chart (pink D, blue M) under a dashed line at 21; for r = 15 the bar touches 21 and test three knocks off one; the sheet and curve return. | The key step of the proof, watched happening. |
| 12 Computer | A rotation-symmetry argument forces every family of bad half-gaps through one of two special tables (6 and 11 genuine equations; the third rotation-symmetric table, with 15, has no bad families through it, so the paper marks it "not needed"); the computer looks closely there and checks a few flat slices. Exact whole-number arithmetic, partly on a 32003-hour clock; certificates anyone can check. | Two marked points with curves running through them; a flat slice missing a small set; a clock face with 32000 + 10 landing on 7; a certificate tick. | What the computer did, and why it is checkable. |
| 13 Directions | Seven or fewer directions never work: 6 + 7 + 7 = 20 < 21. Eleven random directions work with probability one (43 dials vs at most 42). Fifteen specific directions (a triangle of grid points) also work. 8, 9, 10 open. | A row of direction counts 1 to 15 colouring red, grey and green; the two counts; the triangle of 15 points. | The practical version and where it stops. |
| 14 Status | Proved: a typical material has no twin; computer-assisted; Lean checked eleven key identities, not the whole argument; internal review only. Not claimed: stability (one simulated test: 0.1% noise, best 22-number fit 45% off), every material (symmetric twins), density. | Short status lines, two at a time; a small bar pair "noise 0.1%" vs "error 45%". | Exactly what is and is not established. |
| 15 Recap | Three recap points; what is still unknown; end card. | Three numbered lines; two open-question lines; end card with title, "Valyu Research, 2026", folder path, synthetic-voice line. | The whole story in three sentences. |

## First-time viewer review

Checked each clip against what has already been shown:

- "Stiffness", "sound wave", "density", "anisotropy", "surface of speeds", "slowness", "table",
  "summary", "twin", "typical", "dial", "midpoint", "half-gap", "genuine equation" and
  "certificate" are each pictured before or as they are named. "Dial" is introduced with the
  sheet-of-paper picture (a sheet has two dials, a curve one) before it is used for tables.
- "Sum of products in pairs" is shown on screen with the actual three squares before it is
  used, and the toy puzzle (add to 5, multiply to 6) says why the summaries carry the same
  information as the speeds.
- "Formula fixed by six numbers" is shown with the real six coefficients and checked by
  substituting straight up; the 15 and 28 are shown as triangles of dots, not formulas.
- "Straight-line simultaneous equations" is the GCSE name for a linear system; the repeated
  equation example (x + y = 2 and 2x + 2y = 4) defines "genuinely different" before r appears.
- r is introduced as "the number of genuinely different equations" on screen before any
  arithmetic with it.
- The rotation-symmetry step (Borel fixed points) and the slice step (projective
  intersection) are described in one sentence each; the narration does not claim more than
  that they reduce the check to a few places.
- Words avoided: tensor, eigenvalue, Christoffel, rank, kernel, generic, Zariski, projective,
  Borel, Bezout, characteristic. "Rank" becomes "genuine equations", "generic" becomes
  "typical", "dimension" becomes "dials".

## Simplifications (and how they stay true)

- "Typical" stands for "outside a proper algebraic subset". Such a set has zero volume, so a
  material chosen at random from any continuous spread misses it with probability one.
- "Stiffness" always means stiffness divided by density, as the video says; the paper's tensor
  is density-normalized and no density separation is claimed.
- The ripple in scene 1 is a picture of anisotropy; the measured data are speeds of flat waves
  (phase speeds), which is what scene 3 shows.
- "A family that big couldn't be missed" is the projective intersection theorem; "a miss on the
  clock is a miss for ordinary numbers" is the paper's properness argument over the integers.
- The twin pair in scene 8 is a teaching example, built in `data_prep.py` by a sign flip that is
  valid for box-symmetric ("orthorhombic") tables, the class where de Hoop et al. report
  four-to-one ambiguity. Both tables are physically valid (positive definite); their speeds
  agree to 1e-14 in 20,000 random directions; it is labelled as an illustration on screen.
- "Eleven random directions work" is the paper's nonempty Zariski-open set of eleven-direction
  configurations, which a random choice hits with probability one. "Fifteen specific
  directions work for any typical material" is Corollary 6.1.
- The noise example is one simulated tensor, one noise draw per level (README of the
  numerical illustration); the narration says "in one simulated test".

## Sources for every number

All figures come from `../paper.tex`, `../README.md`, `../READINESS.md`,
`../verification/verification_run.log` and `../verification/numerical-illustration/`, and are
recomputed and asserted by `data_prep.py` (which writes `data.json`):

- 21 = 6 + 5 + 4 + 3 + 2 + 1 free entries; 6, 15, 28 coefficients (degree 2, 4, 6 forms in
  three variables), 49 in all; trace kernel dimension 15 (`verification_run.log`).
- Our crystal: the reference Voigt matrix (seed 20261017). Straight-up speeds 1.1152,
  1.4195, 1.6856 (matching `reconstruction_results.json`); squares 1.2437, 2.0149, 2.8413;
  sum 6.1, pairs 11.765, product 7.1205; trace formula coefficients 7.1, 6.3, 6.1, -2.4,
  -1.1, 0.7 (fitted and checked to 1e-9). Fastest speed over all directions 1.54 to 2.33.
- Witness (paper, proof of Theorem 1.1): isotropic H0, Lame parameters 4 and -1, Gamma = 3pp^T - qI; straight
  up diag(-1, -1, 2); sums 0, 0; pairs -3, -3; products 2, -2; rank 15.
- Ranks 6, 11, 15 at the three fixed points (`verification_run.log`, check_minimum_rank_borel); the rank-15 point is "not needed" (paper, subsection "The first fixed points"), so the video shows only the 6 and 11 points.
- Bound dim R_r <= r - 1 for 6 <= r <= 14, R_5 = {0} (Proposition 2.1); totals 20.
- Prime 32003; 32000 + 10 = 7 on that clock.
- Directions: min(m, 6) + 2m <= 20 for m <= 7; 21 + 2 x 11 = 43 vs at most 42; fifteen
  directions (a, b, 1) with a + b <= 4; 8 to 10 open (Theorem 7.1, Corollary 6.1).
- Lean: eleven second-normal-quotient determinant identities compiled with axiom audit
  (`README.md`, `READINESS.md`); the full theorem is not Lean-verified.
- Noise: 0.1% relative speed noise, compressed 22-number fit with the smallest residual:
  45.2% relative error (`reconstruction_results.json`).
