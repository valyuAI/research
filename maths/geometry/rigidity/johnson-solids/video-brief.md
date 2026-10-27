# Video brief: which Johnson solids can wobble?

Audience: a bright 16-year-old who has just finished GCSE maths or physics. Target length 6-9 minutes.

## 1. The question in plain words

Build a solid out of stiff sticks (the edges) joined at hinges (the corners). Every face must stay perfectly flat, like an imaginary perfectly flat sheet that can shear: a square may become a rhombus. The sheet is a geometric constraint, not a rigid glass panel. Can the solid wobble into a different shape without bending a stick and without any face buckling? If it cannot, it is **rigid**; if it can, it is **flexible**.

We answer this for all 92 **Johnson solids**: the convex solids whose faces are all regular polygons (equilateral triangles, squares, regular pentagons and so on), leaving out the familiar Platonic and Archimedean solids and the prisms and antiprisms. The answer: **47 are rigid and 45 are flexible.** Six of the rigid ones are rigid only in a subtle "second-order" way.

## 2. Why anyone cares

- In 1813 Cauchy proved that a convex solid is rigid if each face is a rigid plate. Here the faces are not rigid plates: only their edges and their flatness are fixed. So the rule changes, and some solids become wobbly. The cube is the simplest example: it shears like a cardboard box with the lids removed, except that here every face stays flat.
- The question separates fixed-length bars from rigid panels. Real engineering structures may impose extra material constraints; the theorem concerns the geometric model shown here.
- In 2026 mathematicians (Adrian-Himmelmann, Winter, Zhang) studied the 31 Platonic, Archimedean and Catalan solids, leaving the truncated dodecahedron undecided. We extend the tables to the Johnson solids; the recorded searches found no prior full classification.

## 3. Smallest concrete examples (with numbers)

**A wobbly one: the triangular cupola (J3).** It has 9 corners and 15 edges, all of length 1. Its faces are a triangle on top, a regular hexagon underneath, three squares and three triangles around the side.
- Key fact to animate: J3 is a regular triangle "plus" a regular tetrahedron. Take every point of the triangle and every point of the tetrahedron and add their coordinates; you get the cupola. This is a Minkowski sum.
- Now spin the tetrahedron about the vertical axis by a small angle t, keep the triangle still, and add again. Every edge of the cupola is a copy of an edge of the triangle or of the tetrahedron, so every edge keeps length 1. The squares become rhombi. The hexagon stays flat because the spin axis is perpendicular to it.
- Numbers: the hexagon's six sides alternate between triangle sides and tetrahedron sides. Spinning the tetrahedron by t turns every other side of the hexagon by t, so the angles go from 120, 120, 120, 120, 120, 120 degrees to 120 + t, 120 - t, 120 + t, ... (at t = 5 degrees: 125, 115, 125, 115, 125, 115). The side squares become rhombi, so their diagonals change length: the shape really is different.

**A rigid one: the square pyramid (J1).** It has 5 corners and 8 edges. Squash the square base into a rhombus: to keep the four slanted edges of length 1 the apex must sit above the centre, at the same distance from all four base corners. But the corners of a non-square rhombus do not lie on a circle, so no such point exists. The base is forced to stay a square, and nothing can move.

## 4. Prerequisite ideas, built from scratch in order

1. **Coordinates and distance.** Points (x, y, z); distance from Pythagoras in 3D.
2. **Velocity of a motion.** If each corner moves with velocity v_i, an edge between corners i and j keeps its length to first order exactly when (p_i - p_j) . (v_i - v_j) = 0. Show this with a single rod: the ends may move sideways but not apart.
3. **Trivial motions.** Sliding or turning the whole solid always satisfies every constraint: 3 slides + 3 turns = 6 "free" motions. These do not count.
4. **First-order rigid.** Write one equation per edge and one per "corner lies in face plane". If the only solutions are the 6 trivial ones, the solid is first-order rigid, and that already guarantees it is rigid. Counting the solutions is linear algebra: the rank of a big matrix.
5. **First-order flexible but still rigid.** Sometimes there are extra velocity solutions that cannot be continued into an actual motion: the solid "wants" to move but jams at second order. Physical analogy: a rope pulled tight between two nails can be pushed sideways a little at first order, but it cannot actually move sideways without stretching.

## 5. The key insight in 5 visual steps

1. **Exact coordinates.** Each Johnson solid is placed with edge length exactly 1, using exact numbers such as (1 + sqrt 5)/2 instead of decimals. Some solids need nastier numbers: our coordinates for the sphenomegacorona J88 use a degree-16 root and an additional square root, giving a degree-32 field. Show one ugly polynomial scrolling past to make the point.
2. **The big matrix.** For each solid build the rigidity matrix: one row per edge and one per corner-face contact, one column per coordinate. For the parabiaugmented truncated dodecahedron J69 that is 360 rows by 366 columns. Rank 360 = 366 - 6 means only the 6 trivial motions remain, so the solid is rigid. This holds for 41 solids.
3. **Two independent checks.** The rank is computed twice by different methods: once with arithmetic modulo a large prime (like clock arithmetic with 1,000,039 hours), and once with guaranteed error-bounded decimals (interval arithmetic). Picture two different accountants who arrive at the same total.
4. **Wobbles from splitting into two pieces.** For 38 of the flexible solids the edges split into two groups and each vertex is the sum of two component positions. Spinning one piece about a well-chosen axis gives the wobble. Animate it for J3 (triangle + tetrahedron), J8 (cube with a pyramid roof: the cube shears, the roof rides along), and J72 (the gyrate rhombicosidodecahedron: its edges split into two families, each forming a smaller solid, and one of them is turned about a five-fold axis). The remaining 7 flexible solids are augmented prisms: the n-gon floor of the prism bends, like a hexagon turning into a squashed hexagon, while the walls stay square.
5. **Jammed at second order.** Six solids pass the "wants to move" test but still cannot move: the augmented dodecahedra J58, J59, J60 and the diminished rhombicosidodecahedra J81, J82, J83. For each, a short list of quadratic equations must have a common real solution for a motion to exist. We prove that it has none. For J58 and J59 the two candidate solutions turn out to be complex numbers, not real ones. Show the equation x^2 + 1 = 0 next to a 3D picture with "no real wobble direction".

## 6. Exact figures, formulas and objects to put on screen

- The edge constraint: (p_i - p_j) . (v_i - v_j) = 0. The face constraint: <p_i, a_s> = 1 (corner i lies on plane s).
- Counting: 6 trivial motions; for polyhedra the number of rows = number of columns - 6 (an Euler-formula fact: V - E + F = 2).
- J3 = triangle + tetrahedron, animated, with the hexagon angles changing.
- J80 vs J81 side by side: both are a rhombicosidodecahedron with two five-fold caps (pentagonal cupolae) sliced off, leaving two decagon faces. When the two decagons are opposite and parallel (J80, "para") the solid wobbles about the axis through both. When they are not opposite (J81, "meta") the simple rotation construction fails; the separate second-order certificate proves that it locks. The punchline: same faces, same counts, opposite answers.
- The dodecahedron family: dodecahedron (5 wobble directions at first order, yet rigid), then add pyramids: J58 (3), J59 (3), J60 (1), J61 (0, plainly rigid).
- A final 92-cell grid coloured three ways: plainly rigid (41), jammed at second order (6), flexible (45).
- Bonus infinite family: antiprisms (two regular n-gons, one twisted by 180/n degrees, joined by a zigzag band of 2n triangles) are rigid for every n, while prisms (joined by squares) always shear. Show a square antiprism and a cube side by side, then let n grow. The proof idea is to split any attempted "balanced set of tensions" into waves going round the band (like Fourier modes, z = e^{2 pi i j / n}). For each wave a 4 x 4 determinant must be non-zero. It equals a constant times (z - 1)(z^2 - 2 cos(2 pi/n) z + 1), which vanishes only for the three slowest waves, and those are handled separately.

## 7. Proved versus computed versus open

- **Proved (with computer-checked certificates):** the full classification, and rigidity of every antiprism (by a symbolic determinant valid for all n at once). Together with the 2026 paper, every strictly convex solid with regular faces is now decided, except the truncated dodecahedron. First-order rigidity of the 41 solids is a theorem resting on exact rank computations replayed by two independent programs. Flexibility of the 45 comes from explicit motions checked in exact arithmetic. Rigidity of the 6 comes from exact second-order certificates.
- **Also certified exactly:** the number of independent first-order wobble directions for each flexible solid (for example 7 for J38). These are tangent-space dimensions, not dimensions of actual families of motion.
- **Also proved:** J60 and J82 are "prestress stable" (a single internal tension pattern locks them), while J58, J59, J81 and J83 are not: they are rigid only through the subtler second-order effect. The proof is exact, not numerical.
- **Open:** whether the flexible solids have other kinds of motion beyond the ones we exhibit. Also open: a general rule predicting rigidity for solids with only triangles and squares, a question asked in the 2026 paper.

## 8. Common misconceptions to avoid

- "Flat faces means rigid faces." No: a flat square may turn into a flat rhombus. Only edge lengths and flatness are fixed.
- "Triangles make everything rigid." Not here: the triangular cupola is full of triangles and still wobbles, because its hexagon and squares can deform.
- "The computer just tried shaking it." No: the verdicts are exact. Decimals appear only inside guaranteed error bounds, never as evidence on their own.
- "First-order flexible means flexible." No: six solids are first-order flexible but rigid.
- "Rigid means it can never have another shape with the same edges." We prove local rigidity: no small wobble. Far-away different shapes are a separate question.

## 9. Production handoff

No video is produced in this research task. Use `verification/data/J03.json`, `J80.json`, `J81.json`, the exact partitions in `verification/certificates/minkowski_partitions.json`, and `verification/results/classification.json` as the animation source. The final replay and review limits are in `readiness.md`. Do not animate an approximate failed flex as an actual motion. The original failed J81 numerical search is historical; the current exact dual matrix is in `verification/certificates/prestress.json`.
