# Storyboard: different trees, different population systems

Audience: a bright 16-year-old after GCSE maths and physics. Running example: the
four-species chain 1-2-3-4, with the four-species star (centre 1) as its rival. Both tables
are the verifier's explicit generic parameters (`check_numbers.py` rebuilds them with
`generic_matrix` from `../verification/verify_lv_tree.py` and checks every number shown).
The two-species plane is the chain with species 3 and 4 absent.

Colour meaning, used throughout: species and single-species invariants blue; foxes maroon
(hook only); pair mixtures and linked triangles gold; tree branches teal / maroon / brown
(tree-rule scene only); the thing currently changing yellow; contradictions and failures
red; success green; secondary text grey.

| Scene | Narration summary | Visual | What the viewer now understands |
|---|---|---|---|
| 1 Hook | Rabbits and foxes rise and fall in cycles. With many species organised by a tree, could two different-looking trees give the same behaviour? Status up front: a previously announced result, independently checked, not a first discovery. | Two population curves over time (blue rabbits, maroon foxes); then the chain and the star side by side with a "?"; a quiet card "an independent check of a result announced earlier". | The question, and that this video verifies rather than discovers. |
| 2 Growth | Rabbits alone grow by about ten percent a month: 100, about 110, about 122. Rate of change (the gradient) equals 0.1 times r. | Exponential curve with dots at months 0, 1, 2; a yellow tangent line; the equation. | What a rate of change is; growth proportional to population. |
| 3 PredatorPrey | Foxes lower the rabbits' growth rate: rate of r = r(2 - f). Foxes need rabbits: rate of f = f(r - 3). The population plane: every point a state, arrows show where it heads. Following arrows goes round a loop. Lotka and Volterra, a century ago. | Equations; a plane (rabbits across, foxes up) filled with arrows; a dot circling a closed orbit, leaving a trail. Illustrative numbers. | Predator-prey as a simple rule; equations as arrows on a plane. |
| 4 ManySpecies | Many species: each population times a weighted sum of all populations. The paper's systems drop constant birth/death numbers. The weights fit a table; row 1 is -25, 1, 1, 1. Negative diagonal: each species crowds itself. | The species-1 equation with its coefficients lighting up the matching table row; the 4 by 4 chain table; diagonal highlighted. | The kind of system studied, and its table. |
| 5 Trees | Dots and lines; no loops and connected is a tree; four dots give two trees (chain, star). The tree is not a food web: it is a rule about equal effects. Remove species 2: branches {1} and {3, 4}; column 2 is 1, then 2, 2. Ten free numbers instead of sixteen. The star has its own pattern. | Graph drawing; a loop crossed out; species 2 fades, branches tint; matching column cells tint the same; the star's column 1 with three branches 1, 2, 3. | Interaction networks as graphs, trees, and the tree family rule. |
| 6 Mixing | With species 3 and 4 absent they stay absent, so watch species 1 and 2 on a plane. New variables: keep x1, replace x2 by 27 x2 - 26 x1. The grid shears and arrows go with it. Surprise: the rules have the same shape again, with a new table (1/27)(-649, 1; -1351, -26). Same system in disguise: equivalent. The question: can a chain system be disguised as a star system? Van der Kamp's 2025 conjecture, checked up to eight species. | Arrow field on the positive quadrant; the whole picture shears; the two tables side by side; the two trees with a "?". | What "equivalent" means, and the exact question. |
| 7 Invariants | Why did that mixture work? An absent species stays absent: its rate is itself times something. The mixture 27 x2 - 26 x1 has the same property: its rate factorises as itself times (-25 x1 - 26 x2). So the line where it is zero is never left: ratio 27 to 26 stays fixed. Name: Darboux polynomials; zeros are conserved, and combinations give conserved quantities. The mixing turned the hidden line into an axis. A tree system has one per species and one per tree line: seven for the chain, seven for the star. | The factorisation with matching terms highlighted; a dot gliding straight along the ray while others curve in; the shear re-run, the ray landing on the axis; the list of seven invariants for the chain. | Darboux polynomials as hidden invariants, concretely. |
| 8 Fingerprint | Mixing rewrites invariants as invariants, so equivalent systems have matching sets. But formulas get scrambled (x3 - x4 becomes y1). What survives: three invariants (x1, x2, 27 x2 - 26 x1) where one is built from the other two, a linked triple. Each tree line gives one; draw them as triangles. Mixing moves things but triangles stay triangles. Count: chain has two invariants in two triangles each; star has one in three. So no disguise is possible. | The chain drawn with gold mixture dots near each line's middle and slim triangles; labels morph to the mixed formulas, then fade; dots scatter with triangles attached; yellow counts; star alongside. | The invariant that survives mixing, and why path and star differ. |
| 9 Complete | Hole: maybe there are more invariants. Skipping a species fails: species 2 affects 1 with strength 1 and 3 with strength 2. Three in a row: pair equations 27p1 + 26p2 = 0, p2 + p3 = 0, 28p1 + 26p3 = 0. First, minus 26 times the second, plus the third: p2 and p3 cancel, 55 p1 = 0. But p1 is not zero: contradiction. So only singles and tree pairs. 55 = (1 + 26) + (2 + 26), built from column 2; "generic" excludes the rare coincidence where such a sum is zero. Lean checks this cancellation. | Table column 2 with 1 and 2 in red; the three equations in aligned columns; yellow cancellations; red "55 p1 = 0" and "p1 is not 0"; the 55 = (1 + 26) + (2 + 26) split with column 2 lit; "checked in Lean" tag. | The key step of the proof, watched happening. |
| 10 Rebuild | Rule: invariants in two or more triangles are species with several neighbours; a triangle joining two of those is a tree line; a triangle with one adds an end species. A seven-species tree rebuilt from triangles alone. So different trees give different triangle patterns. | Scattered triangles; shared dots light yellow; the tree is redrawn from them, edge by edge. | How the tree is rebuilt for any size. |
| 11 Status | History: 2023 families introduced; 2025 conjecture; September 2026 Zeng's preprint announced the result, now withdrawn and unavailable; withdrawal does not cancel the announcement. This work: independent self-contained proof, verification note, no priority. Written proof for all sizes; exact checks for 986 trees up to 12 species and 200 trees up to 10 species (consistency checks, not proof); Lean only for the three-in-a-row step; not externally refereed. Limits: unlucky special tables (equal rows) excluded; tree is a rule, not a food web from data. | A timeline built point by point; short status rows with tick marks; an equal-rows table turning red. | Exactly what is proved, checked, credited and excluded. |
| 12 Recap | Three points; still open (special tables, networks beyond trees); end card. | Three recap lines; two open-question lines; end card with title, "Valyu Research, 2026", folder path and synthetic-voice line. | The whole story in three sentences. |

## First-time viewer review

Checked each clip against what has already been shown:

- "Rate of change" is introduced with a gradient on a graph before any equation uses it.
- "Population plane", "state" and "arrow" are pictured before the loop is named a cycle.
- "Table", "row", "column" and "diagonal" are shown with the species-1 equation lighting up
  its row before the tree rule refers to columns.
- "Tree", "branch" and "family" are pictured before use; the warning that the tree is not a
  food web comes before the rule, so the viewer does not build the wrong picture.
- "Mixture" and "new variables" are shown as a shear of the plane before "equivalent" is
  named. The surprising mixture is shown first and explained in the next scene, so the
  viewer meets the question before the answer.
- "Hidden invariant" is built from "an absent species stays absent", which the viewer saw
  in scene 6; the name "Darboux polynomial" comes after the picture.
- "Linked triple" is defined in the sentence that names it, with the concrete triple
  x1, x2, 27 x2 - 26 x1 on screen.
- "p1, p2, p3" are introduced as the amounts of each species in the mixture before the
  equations use them.
- "Generic" is explained as excluding rare coincidences, with the equal-rows example given
  later in the status scene.
- "Lean" is described as a program that checks proofs line by line.

## Simplifications

- The classic fox-rabbit equations (with constant terms 2 and -3) are an illustration; the
  paper's systems have no constant terms (a shared constant is also allowed, not mentioned).
- The pair equations are stated as what "writing out the condition" gives; the general
  derivation (matching coefficients) is shown only for the two-species factorisation.
- Equation 2, 28 p2 + 28 p3 = 0, is shown divided by 28; the combination is the paper's
  beta, -alpha, C combination divided by 28.
- The precise genericity conditions (three inequalities per column) are summarised as
  "rare unlucky coincidences"; the skip and three-in-a-row steps show two of them at work.
- The mixed table is shown only on the two-species plane; the shear picture uses the
  vertical axis 27 x2 - 26 x1 drawn at a scale of one twenty-seventh (a change of units).
- Linked triples are drawn as triangles; positions after "mixing" are schematic, while the
  formulas shown are the exact rewrites under an integer mixing of determinant 1.
- The pair invariant for the line 1-2 is shown as 27 x2 - 26 x1, the paper's P12 = 26 x1 - 27 x2 with
  the sign flipped (the same invariant), so that it matches the mixing variable.
