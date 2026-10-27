# Video brief: why loops of chemical states respond in a predictable way

Audience: a bright 16-year-old who has finished GCSE maths or physics. Target length 6-9 minutes.

## 1. The question in plain words

A small machine (a molecule, a motor protein, a receptor) hops at random between a few states. Each possible hop has a rate: how many times per second it tends to happen. After a while the machine settles into a steady pattern: it spends a fixed fraction of its time in each state. Call these fractions pi_0, pi_1, pi_2, ...

Now turn a knob: change one of the rates a little. The fractions shift. **How much can they shift, and in which directions?**

Fancher and Horowitz (University of Michigan, July 2026) guessed a clean answer: every possible shift is a *weighted average* of a short list of "building block" shifts, and that list depends only on the shape of the network (which states connect to which), not on the actual rates. They checked it for 3 states and asked for a proof. We prove it for every network whose loops never share an edge (a "cactus"), including every single loop of any size. We also show that our method provably cannot work for the network where 4 states all connect to each other, or for any network that contains it as a minor, even though the guess still looks true there.

## 2. Why anyone cares

- Cells sense signals (hormones, sugar, light) with networks like this. "How sharply can a network respond?" is a central question in biophysics.
- If the guess is true, the most extreme responses are achieved by a finite list of simple "optimal designs" readable from a picture of the network. That turns an infinite search over rates into a finite check.
- Their Eq. (8) then gives a hard speed limit on any measurable quantity's sensitivity.

## 3. Smallest concrete example (use these exact numbers)

**The driven triangle.** States 0, 1, 2 in a ring. Clockwise hops (0 to 1, 1 to 2, 2 to 0) have rate 2. Anticlockwise hops have rate 1. The ring is pushed clockwise, like a tiny motor.

- Steady state: by symmetry pi = (1/3, 1/3, 1/3).

**Trees pointing at a root.** A spanning tree pointing at root 0 is a set of arrows, one out of every other state, so that following arrows from anywhere leads to 0. On a ring, such a tree is "delete one edge, point everything else towards the root". The weight of a tree is the product of its arrow rates.

| Root 0: deleted edge | arrows | weight | probability |
|---|---|---|---|
| {0,1} | 1 to 2, 2 to 0 | 2 x 2 = 4 | 4/7 |
| {1,2} | 1 to 0, 2 to 0 | 1 x 2 = 2 | 2/7 |
| {2,0} | 1 to 0, 2 to 1 | 1 x 1 = 1 | 1/7 |

Every root looks the same here by symmetry: the edge just after the root (clockwise) is deleted with probability 4/7, the next with 2/7, the last with 1/7.

**Markov chain tree theorem** (on screen): pi_j is proportional to the total weight of trees pointing at j. Here each root has total 4 + 2 + 1 = 7, so pi = (7, 7, 7)/21 = (1/3, 1/3, 1/3).

**Turning the knob.** Multiply the single rate "0 to 1" by (1 + epsilon). The exact response is

  d ln pi / d epsilon = (-10/21, +8/21, +2/21)  for states (0, 1, 2).

Speeding up 0-to-1 drains state 0 and fills state 1, as you would expect.

**Tree families.** A tree family picks one tree for each root: 3 x 3 x 3 = 27 families. Pool all arrows of a family into a bag (a multiset). The 27 families give only 18 different bags. A family is *uniquely constructable* (UC) if no other family produces the same bag: 11 of the 27 are UC.

**The punchline on this example.** Our construction picks out exactly 7 UC families, each with probability exactly 1/7 (forced by the tree probabilities above; a simulation of 400,000 draws gives 0.142-0.144 each). Averaging their building-block responses reproduces (-10/21, 8/21, 2/21) exactly. Label families by the deleted edge at roots (0, 1, 2), writing edge {k, k+1} as k:

  (0,0,0), (1,1,1), (2,2,2), (0,1,0), (1,1,2), (0,2,2), (0,1,2), each with probability 1/7.

## 4. Prerequisite ideas, built from scratch in this order

1. **Random hopping with rates.** A dot on a graph of states; arrows labelled with rates. Show a long simulated trajectory and the fraction of time in each state converging.
2. **Steady state.** The long-run fractions pi_j. Flow in = flow out (but here with a net clockwise current, so it is not equilibrium).
3. **Spanning trees pointing at a root.** One outgoing arrow from every non-root state, no cycles, everything drains to the root. Weight = product of rates.
4. **Markov chain tree theorem.** pi_j is proportional to the sum of weights of trees rooted at j. Verify on the triangle (7, 7, 7).
5. **Each root's tree lottery.** Dividing by the total turns tree weights into probabilities P_j(T): "pick a random tree rooted at j, heavier trees more likely".
6. **Response as an average.** Taking the log-derivative of the tree theorem gives: response = average over a random tree family (one independent tree lottery per root) of a simple score G (sum of knob sensitivities along the tree's arrows, recentred). This is Fancher and Horowitz's Eq. (5). Each family gives a "vertex"; the response is inside their convex hull (a weighted average).
7. **Convex hull.** Show 2D points and the shape stretched around them; a weighted average with nonnegative weights summing to 1 always lands inside.
8. **The Gumbel-max trick.** To pick option k with probability proportional to weight w_k: add an independent random "Gumbel" number g_k to each ln w_k and take the largest. Show a histogram confirming 4/7, 2/7, 1/7.

## 5. The key insight in 6 visual steps

1. **Only some families matter.** Two different families with the same bag of arrows always have equal weight, so neither can ever dominate. Fancher and Horowitz guessed that the UC families alone suffice: the response is a weighted average of UC vertices only.
2. **Reframe: one shared lottery.** The response depends only on each root's own tree lottery, not on how the lotteries are correlated. So if we can draw a whole family at once, correlated across roots, with each root's tree still having the right law, and the family is always UC, then the guess holds with weights theta = probability of each family.
3. **Trees on a ring are deleted edges.** Draw a ring of n states. A tree rooted at r is fixed by which edge is deleted. Moving the deleted edge one step changes only one arrow, so the weight changes by a factor a_k/b_k that does not depend on the root. All roots therefore read their tree weights off ONE long sequence lambda_k (bar chart), each root through its own window of n consecutive bars. The sequence is not periodic when the ring is driven: going once round multiplies it by the product of anticlockwise over clockwise rates (1/8 on the triangle).
4. **One coin per edge.** Attach one Gumbel number to each edge of the ring (show n coloured tokens). Every window contains every edge exactly once, so in every window the bars receive n independent Gumbel bumps. The tallest bumped bar in each window is a correct sample of that root's tree, for all roots simultaneously, with the same tokens.
5. **Why the family is UC.** The tokens are equivalent to changing the rates; under those new rates each chosen tree is strictly the heaviest at its root. A family of heaviest trees cannot share its bag with another family (that family would weigh strictly less, yet same bag means same weight). So the family is UC.
6. **Cacti by gluing.** Rings that share single states (a cactus) split every tree into independent pieces, one per ring. Use independent tokens for each ring and glue.

## 6. Figures, formulas and objects to show

- Ring diagram with arrows labelled 2 (clockwise) and 1 (anticlockwise); a dot hopping.
- The three trees rooted at 0 with weights 4, 2, 1 and probabilities 4/7, 2/7, 1/7.
- Tree theorem: pi_j = w(trees at j) / sum_k w(trees at k).
- Response formula (FH Eq. 5): d ln pi_j = sum over families sigma of [w(sigma)/Z] (G_j^sigma - <G^sigma>).
- Conjecture (FH Eq. 6): same, but summing only over UC families alpha with weights theta^alpha >= 0 that sum to 1.
- Cycle formula: w_r(k) = (product of a_v for v = r+1..k) x (product of b_v for v = k+1..r+n-1), and w_r(k)/w_r(k-1) = a_k/b_k.
- Bar chart of lambda_k = 1, 1/2, 1/4, 1/8, 1/16, ... with sliding windows of width 3 for roots 0, 1, 2.
- Gumbel tokens: one per edge, same colours re-appearing in every window.
- The 7 families with probability 1/7 each; the 27 families, 18 bags, 11 UC.
- A cactus: e.g. a triangle and a square sharing one state, plus a dangling edge.
- K4 (four mutually connected states) with a red "no shared lottery" stamp, and a note that the guess is still believed true there.

## 7. Proved vs computed vs open

- **Proved (written proof):** the Fancher-Horowitz conjecture for every network whose underlying graph is a cactus, with explicit weights theta (the Gumbel family law), and the resulting sensitivity bound. Includes all single-loop networks of any size and gives a new proof of their 3-state case.
- **Checked by exact computation:** the ring weight identity for rings up to 8 states, block splitting on five cacti, UC-ness of sampled families; and for K4 with specific integer rates, an exact certificate (a +1/-1 labelling of the 64 root-tree pairs) proving that no shared lottery on UC families exists.
- **Proved (written proof plus one exact replay):** the K4 obstruction spreads to every network containing a K4 "minor" (a K4 you can get by deleting edges and shortening paths). The trick: shrinking a path or pruning a dangling state turns any shared lottery on the big network into one on the small network, so a lottery on the big one would give one on K4.
- **Numerical evidence only:** the conjecture itself survived searches on K4 and 5-state graphs; shared lotteries seem to exist on every network with no K4 minor (for example the diamond), but outside cacti this is unproved.
- **Open:** the general conjecture (e.g. for K4, binding cubes, proofreading ladders).

## 8. Misconceptions to avoid

- The Gumbel noise is a mathematical device for building weights theta, not physical noise in the system.
- The K4 result does NOT disprove the conjecture. It only shows that this particular method (a lottery matching every root's full tree law) cannot be used there. The conjecture needs much less.
- "Uniquely constructable" is about the bag of arrows of the whole family, not about single trees.
- The weights theta depend on the rates but not on which rate you nudge; the building blocks depend only on the network's shape.
- A cactus is not "any graph with cycles": its loops may touch at single states but never share an edge. Two triangles glued along an edge (the "diamond") is not a cactus, and the simple per-edge noise trick fails there (error about 0.06).
- Steady state here is not equilibrium: the triangle carries a net clockwise current.
