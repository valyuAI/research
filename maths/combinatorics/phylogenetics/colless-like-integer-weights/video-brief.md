# Video brief: why whole-number weights cannot measure perfect symmetry

## The question in plain words

Biologists measure how lopsided an evolutionary tree is. For trees where a branch point can split into many branches, one family of measures ("Colless-like indices") works like this: give every vertex, including leaves, a weight that depends only on how many children it has, add up weights to get the "size" of each subtree, and at every branch point measure how unequal the sizes of its child subtrees are. Add all those inequalities. A perfectly symmetric tree (at every branch point, all child subtrees look the same) scores zero. The measure is called "sound" if only perfectly symmetric trees score zero.

In 2018 the inventors conjectured that if all the weights are whole numbers, the measure can never be sound. We prove it.

## Why anyone cares

A balance index that gives zero to a lopsided tree is misleading. The inventors found weights that work (e to the power of the outdegree, or a logarithm), but these are awkward irrational numbers. Whole-number weights would be simpler; the theorem says they always fail.

## Smallest concrete example

Use weight f(n) = n + 1 for a vertex with n children (so a leaf weighs 1, a vertex with 2 children weighs 3, with 6 children weighs 7).

- Tree A: a root with 2 children, each with 2 leaf children. Size = 3 (root) + 3 + 3 (two middle vertices) + 4 x 1 (leaves) = 13.
- Tree B: a root with 6 leaf children. Size = 7 + 6 x 1 = 13.

Both are perfectly symmetric, but they are different trees with the same size. Now join them under a new root. The new root sees two child subtrees of equal size, so it scores zero; everything inside A and B also scores zero. The whole tree scores zero, but it is clearly not symmetric (one side has 4 leaves at depth 2, the other 6 leaves at depth 1).

## Prerequisite ideas in order

1. Rooted trees, outdegree (number of children), leaves have outdegree 0.
2. Perfectly symmetric trees are described by a list of outdegrees, one per level: (2,2) means 2 children, then each has 2 children.
3. The size formula for a symmetric tree with list (k1, k2, ..., kh): f(k1) + k1 f(k2) + k1 k2 f(k3) + ... + (k1 k2 ... kh) f(0).
4. The pigeonhole principle: more pigeons than holes forces two pigeons into one hole.
5. Multinomial coefficients: the number of ways to arrange m 2s, m 3s and m 4s in a row is (3m)!/(m! m! m!).

## The key insight in visual steps

1. Lists made of m 2s, m 3s and m 4s all describe trees with exactly 2^m 3^m 4^m = 24^m leaves. Show a few lists for m = 1: (2,3,4), (2,4,3), (3,2,4), ... six of them, all with 24 leaves.
2. Count the lists: about 27^m of them (the six for m = 1, ninety for m = 2, and so on). Show the count growing.
3. All these trees have the same number of leaves, so the leaf weights add the same amount to each. What is left (the internal part) is a whole number between 0 and (largest weight) x 24^m. Show a number line of "holes" of length growing like 24^m.
4. 27 beats 24: the pigeons grow like 27^m and the holes like 24^m. Animate the two exponential curves; eventually the pigeons outnumber the holes.
5. So two different symmetric trees share a size, and joining them under a root gives a lopsided tree with score zero.

## Exact formulas and objects on screen

- Size of symmetric tree: sum over levels of (number of vertices on the level) x f(outdegree), plus (number of leaves) x f(0).
- Example collisions: f(n) = n+1: (2,2) and (6) both 13; f(n) = 2^n: (2,3) and (3,2) both 26; f(n) = n! + 1: (4,3) and (2,2,2,2) both 77.
- Count: (3m)!/(m!)^3, at least 27^m divided by a polynomial; holes: at most M 24^m + 1.

## Proved versus computed versus open

- Proved: no weight function whose values at outdegrees 2, 3 and 4 are whole numbers (or fractions) gives a sound index; the leaf weight f(0) does not matter.
- Computed: the small examples above, checked by a script that builds the trees.
- Not settled here: whether some choice of weights in a rank-two group, such as integers plus integer multiples of the square root of 2, is sound. Some particular choices already have known collisions.

## Misconceptions to avoid

- The theorem does not say Colless-like indices are useless; the inventors' recommended weight ln(n + e) is sound.
- The collision guaranteed by the counting argument can involve huge trees, while the displayed weight choices already have small collisions. This is not a universal bound on the smallest counterexample.
- "Sound" is about which trees get the minimum score zero, not about ranking all other trees correctly.

## Final production handoff

The theorem is a hand proof, not a Lean formalisation. `verification/check_colless.py` checks illustrative collisions by both the level formula and explicit trees. The leaf contribution cancels in the equal-leaf counting family even when f(0) is irrational, so animate the internal sums as the pigeonholes. For the strongest statement, f is nonnegative and f(2), f(3), f(4) are integer multiples of one positive real unit; all other values are arbitrary within the domain.

Use `(2,2)` and `(6)` with total sizes 13, then the new root, as the opening animation. Use the exact count `(3m)!/(m!)^3` for the curve; `27^m` is its exponential growth rate, not the exact count. Correctness confidence is high; originality confidence is moderate after the documented search. The original theorem is an explicit 2018 conjecture, not a new definition of tree balance. See `readiness.md` for final review evidence. No video is produced in this research task.
