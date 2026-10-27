"""Editable narration and storyboard source; run to regenerate the two manifests."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORY = [
  ('Rules', 'A square shears, then a unit-edge cube tilts with its vertical bars keeping length.', 'Fixed bars and flat faces allow changing angles.', [
    ('r1', 'Can you change this square without stretching any of its four sides? Push one corner sideways, and you get a diamond shape. The sides stay the same length. The angles change.'),
    ('r2', 'Now try the same idea with a solid. These bars keep their lengths, and every face must stay perfectly flat. But a flat face can change shape. It is not a rigid plate.'),
    ('r3', 'Watch the top of this cube move sideways and slightly down. The upright bars tilt instead of stretching. Every face remains flat, so this is an allowed change of shape, called a flex.'),
    ('r4', 'Which solids can do this, and which are locked? We will explore a family of ninety two shapes called Johnson solids. The answer is forty seven locally rigid and forty five flexible. Here is why that is subtle.'),
  ]),
  ('Cupola', 'Verified J3 geometry, face highlights, genuine certificate flex and changing diagonal.', 'Triangles do not suffice when other faces can deform.', [
    ('c1', 'Meet our running example, the triangular cupola, also called J three. It has a triangle on top, a hexagon underneath, and a ring of three squares and three triangles. All fifteen edges have length one.'),
    ('c2', 'Those triangles look like braces. Before we move anything, pause and predict: will this shape lock, or wobble? Remember that the hexagon and squares must stay flat, but their angles are allowed to change.'),
    ('c3', 'It wobbles. This animation uses the actual construction checked in the research. Every bar keeps its length. The squares become rhombuses, and the hexagon changes its angles while staying in a single plane.'),
    ('c4', 'The yellow line joins two corners that are not connected by an edge. Its length changes. That proves we are changing the shape itself, rather than just turning the entire object in space.'),
  ]),
  ('Addition', 'Two component shapes and vector addition at one actual vertex; then rotate only tetrahedron.', 'A vertex is a sum of two component positions.', [
    ('a1', 'The trick is to build each corner by adding two positions. Start at the origin, follow one blue arrow, then one yellow arrow. The endpoint is their sum. This is ordinary coordinate addition, drawn as a journey.'),
    ('a2', 'For this cupola, the blue positions form a triangle. The yellow positions form a tetrahedron, a solid with four triangular faces. The outer corners of their sum make our cupola. The colours track which component supplies each edge.'),
    ('a3', 'Keep the blue triangle fixed. Turn the yellow tetrahedron a little around this vertical axis. Then add the positions again. We have a recipe for every corner, at every small angle, rather than a collection of guessed frames.'),
    ('a4', 'A blue edge comes entirely from the unchanged triangle. A yellow edge comes entirely from the rotating tetrahedron. Turning a rigid object does not change its edge lengths. That explains why every bar survives the motion.'),
  ]),
  ('Flatness', 'Top-down hexagon, alternate edge families and measured 115/125 degree angles; planar parallelogram.', 'Edge preservation and face planarity are distinct requirements.', [
    ('f1', 'But unchanged edges are only half the rules. Look straight down at the hexagon. Its sides alternate blue and yellow. Each colour supplies a closed triangle of edge directions, so turning one colour still leaves a closed six-sided path.'),
    ('f2', 'The turn happens inside this plane, so the hexagon stays flat. At a five degree turn, its angles alternate between one hundred and fifteen and one hundred and twenty five degrees. Its six sides still have length one.'),
    ('f3', 'Each square combines one direction from each component. Two directions span a plane, so its four corners remain a flat parallelogram. The triangular faces stay triangles. The certificate checks these requirements and confirms the motion is nontrivial.'),
  ]),
  ('Pyramid', 'Square pyramid; base rhombus with unequal half-diagonals and incompatible equal apex distances.', 'A simple rigid example can be explained by Pythagoras.', [
    ('p1', 'Compare a square pyramid, J one. It has four unit bars around the base and four unit bars rising to the tip. Could its base do the same square-to-rhombus trick? Let us try the necessary geometry first.'),
    ('p2', 'The tip must be equally far from all four base corners. Its shadow on the base must therefore be equally far from them too. For a rhombus, that would put the shadow at the crossing of the diagonals.'),
    ('p3', 'Call the half-diagonal lengths a and b, and the height h. Pythagoras gives a squared plus h squared equals one, and b squared plus h squared equals one. Subtract: a squared must equal b squared.'),
    ('p4', 'So the two diagonals must have equal length. A rhombus with equal diagonals is a square. The attempted squash fails. This is a small example of rigidity, already covered by earlier work, rather than a new discovery here.'),
  ]),
  ('FirstOrder', 'A rod, transverse velocity arrow and length expansion; many constraints funnel to remaining directions.', 'First-order tests concern instantaneous directions, with whole-object movement excluded.', [
    ('v1', 'For complicated solids, we start with a simpler question. Give every corner a tiny velocity arrow. Which arrows avoid changing any edge length or face flatness at the very first instant? This is the first-order test.'),
    ('v2', 'For one horizontal bar, pulling an end along the bar immediately changes its length. Moving that end straight sideways has zero initial rate of length change. The test notices the linear part of a change, before squared terms matter.'),
    ('v3', 'All these first-instant rules become simultaneous linear equations. Sliding or turning the whole solid always works. In three dimensions, three slides and three turns give six ordinary motions. We remove those because they do not change the shape.'),
    ('v4', 'For forty one Johnson solids, no other velocity survives. That proves local rigidity. But an extra velocity arrow does not yet prove a real wobble. An apparent escape can disappear when you look at the next order.'),
  ]),
  ('SecondOrder', 'Two unit rods between fixed endpoints: middle point moves transversely only as a rejected attempt; h squared obstruction.', 'A first-order candidate need not extend to an actual flex.', [
    ('s1', 'Here is a simpler model of that trap. Two unit bars lie in a straight line between fixed endpoints, two units apart. The middle joint seems free to move upwards at the first instant. Try to give it a height h.'),
    ('s2', 'By Pythagoras, each bar would then have squared length one plus h squared. Keeping its length one requires h squared to equal zero. So the joint cannot actually rise. The red drawing is a rejected attempt, not an allowed flex.'),
    ('s3', 'The six exceptional Johnson solids have this kind of first-order false hope, although their equations are more complicated. Exact second-order certificates rule out every nonzero candidate direction. The only real solution left is no change of shape.'),
    ('s4', 'Those six are J fifty eight, fifty nine, sixty, eighty one, eighty two and eighty three. For J sixty and J eighty two, one suitable stress pattern blocks all candidate directions. The other four are rigid without that stronger property.'),
  ]),
  ('Census', '92 individually indexed cells, categories reveal in order; arithmetic 41+6=47 and 45.', 'The complete table combines different kinds of proof.', [
    ('n1', 'Now put all ninety two solids on one board. They begin with regular polygon faces and are convex, with no inward dents. The Johnson family excludes the familiar Platonic and Archimedean solids, and the prisms and antiprisms.'),
    ('n2', 'Forty one are rigid by the first-order test. Forty five have actual continuous flexes. Thirty eight use a certified rotation of a component; seven use an augmented prism construction. The remaining six are locked by second-order obstructions.'),
    ('n3', 'So forty one plus six gives forty seven locally rigid solids, alongside forty five flexible ones. Notice the distinction: fifty one have extra first-order directions, but only forty five really flex. A tangent direction is not a motion family.'),
  ]),
  ('Evidence', 'Exact arithmetic identities; two checked formulations; certificate-to-verdict flow.', 'Exact checks support the theorem, but do not prove priority or replace written deductions.', [
    ('e1', 'This is not a computer shaking shapes until something happens. Coordinates and certificates use exact algebraic numbers, including square roots. The first-order results are checked in two different formulations, using modular arithmetic and rigorously bounded intervals.'),
    ('e2', 'For the flexible shapes, the evidence is a formula for an actual motion, together with checks of lengths, flatness and a changing distance. For the six locked shapes, exact algebra rules out the candidate directions. Written arguments connect those checks to rigidity.'),
    ('e3', 'The research package reports a successful seventeen-stage replay. That is strong computational evidence with explicit assumptions, not a proof assistant formalisation or external peer review. This video checks its displayed cupola motion against the stored certificate; a separate coordinator audit remains separate.'),
  ]),
  ('Ending', 'Three-part recap, nearby versus distant configurations, end card with paper and disclosure.', 'Local rigidity and novelty have precise limits.', [
    ('z1', 'Keep three ideas. Flat does not mean rigid. A recipe preserving every constraint proves a genuine flex. And a first-instant permission can still be blocked at second order. Together, those ideas explain the three colours in the table.'),
    ('z2', 'Locally rigid means no small wobble from the starting shape. We are not claiming there can never be a distant different shape with the same edge lengths. Nor do these constructions classify every possible motion of the flexible solids.'),
    ('z3', 'The contribution is the complete Johnson table and its certificates, rather than a new general rigidity rule. The documented searches found no earlier full classification, but cannot prove priority. The paper and editable evidence accompany this video. Narration uses a synthetic voice.'),
  ]),
]

clips = [{'id': key, 'text': text} for _, _, _, rows in STORY for key, text in rows]
(ROOT / 'narration.json').write_text(json.dumps({'voice': 'cedar', 'clips': clips}, indent=2))
lines = ['# Storyboard: which Johnson solids can wobble?', '', 'Audience: GCSE graduate. Fixed-edge-length, planar-face model. Actual J3 data and certificate; all other mechanisms identified as elementary teaching examples.', '', '| Scene | Narration beats | Visual | New understanding |', '| --- | --- | --- | --- |']
for name, visual, understanding, rows in STORY:
  lines.append(f'| {name} | ' + '; '.join(k + ': ' + t for k, t in rows) + f' | {visual} | {understanding} |')
lines += ['', 'Comprehension review: coordinate addition is introduced with arrows before the component construction; Pythagoras precedes the second-order obstruction; instantaneous directions precede the census. No matrix rank, stress or novelty claim is used as an unexplained substitute for the motion mechanism. Stress is an optional final distinction, described as one pattern blocking all candidates. No audience study was performed.', '', 'Scope decisions: omit the antiprism theorem, J80/J81 visual comparison, and detailed elimination polynomials to give the real J3 mechanism time. The second-order toy equation is not represented as a literal J58/J59 certificate.']
(ROOT / 'storyboard.md').write_text('\n'.join(lines) + '\n')
print(f'{len(clips)} clips, {sum(len(c["text"].split()) for c in clips)} words', flush=True)
