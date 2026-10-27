# Video brief: an 11-neuron memory that should not exist

Audience: a bright 16-year-old who has finished GCSE maths or physics. Target length 6-8 minutes.

## 1. The question in plain words

Neuroscientists model a patch of brain as a network of neurons. Each neuron has a firing rate, a number x_i >= 0. An arrow j -> i marks weaker inhibition from neuron j to neuron i. Every off-diagonal interaction in this model is inhibitory; the arrow does not mean a positive excitatory weight.

A **memory** in this model is a pattern of firing rates that the network settles into and returns to after a small nudge: a *stable fixed point*. The set of neurons firing in that pattern is its *support*.

In 2019 Curto, Geneson and Morrison conjectured a beautiful rule. The only groups of neurons that can hold a memory are **target-free cliques**: groups where all pairs have arrows in both directions, and no outside neuron receives arrows from the whole group. Since then this has been the guiding picture.

**The rule fails at the standard parameter settings used in the cited CTLN simulations: eps = 1/4, delta = 1/2.** A public research repository's unrefereed results imply this for networks of 23 or more neurons, without saying so. We give an explicit 11-neuron network holding a stable memory in which all 11 neurons fire, although 21 arrows are missing. We also show that no network with 7 or fewer neurons can do this.

## 2. Why anyone cares

- If the rule were true, you could read every memory a network can store straight off its wiring diagram. That would be a perfect "structure determines function" theorem.
- Geneson disproved the general rule in July 2026. Earlier repository results also imply failure at the standard parameter pair. Our contribution is a smaller explicit example there, with an exact certificate.
- We also pin down how small such a rogue memory can be at these settings: between 8 and 11 neurons.

## 3. Smallest concrete example (use these exact numbers)

**The rule of the network (CTLN).** Each neuron obeys

  dx_i/dt = -x_i + [ sum_j W_ij x_j + 1 ]_+

where [u]_+ = max(u, 0) (a "ReLU"). The weights are:
- W_ij = -3/4 if j -> i (weak inhibition, because excitation partly cancels it),
- W_ij = -3/2 if there is no arrow j -> i (strong inhibition),
- W_ii = 0.

These are eps = 1/4 and delta = 1/2: -1 + 1/4 = -3/4 and -1 - 1/2 = -3/2.

**Warm-up 1: two neurons with arrows both ways (a clique).** Fixed point x1 = x2 = x with x = -3/4 x + 1, so x = 4/7. Nudge it and it returns. This is a memory, as the rule predicts.

**Warm-up 2: three neurons in a cycle 1 -> 2 -> 3 -> 1.** No clique; its positive fixed point is unstable. A numerical trajectory can illustrate activity passing around the cycle, labelled as a simulation.

**The counterexample G11.** Neurons 0 to 10. Start with every arrow present (121 - 11 = 110 arrows), then delete these 21:

| neuron | gets NO arrow from |
|---|---|
| 0 | 5, 8 |
| 1 | 5 |
| 2 | 3, 4, 9 |
| 3 | 5, 9 |
| 4 | 1 |
| 5 | 2, 4, 9 |
| 6 | 1 |
| 7 | 0, 8 |
| 8 | 4, 5, 9 |
| 9 | 1 |
| 10 | 0, 8 |

Notice the repeated rows: neurons 4, 6 and 9 all lack an arrow from neuron 1 only, so they have the same missing-in-arrow pattern. Neurons 7 and 10 both lack arrows from 0 and 8, and both also send to everyone, so they are full twins.

**The memory.** Every neuron fires, with rates (exact fractions)

  x* = (22, 52, 28, 31, 7, 37, 7, 67, 10, 7, 67) / 292

that is, about (0.075, 0.178, 0.096, 0.106, 0.024, 0.127, 0.024, 0.229, 0.034, 0.024, 0.229).

Check one neuron on screen, in units of 1/292. Neuron 0 receives strong inhibition (-3/2) from neurons 5 and 8 and weak inhibition (-3/4) from the other eight. The other ten rates add up to 313 and x_5 + x_8 = 37 + 10 = 47. So neuron 0's input is 1 - (3/4)(313) /292 - (3/4)(47)/292 = 1 - (3/4)(360/292) = 22/292, which is exactly x_0.

**It is stable.** The exact proof guarantees return for sufficiently small perturbations. Sampled numerical perturbations of relative size 30% also spiral back; this is not a guarantee for every perturbation of that size. The slowest return has time constant about 106 time units, and it wobbles with a period of about 37 time units, because the slowest eigenvalue pair is complex.

## 4. Prerequisite ideas, built from scratch in this order

1. **Firing rate and the ReLU.** A neuron's rate cannot go negative; show the [u]_+ ramp.
2. **Fixed point.** A state where every dx_i/dt = 0. Near a fixed point where all neurons fire, the ReLU is just the identity, so the system is linear: dx/dt = A (x - x*).
3. **Stability from eigenvalues.** In 1D, dx/dt = a x shrinks iff a < 0. In 2D a spiral shrinks iff the real part of the eigenvalue is negative. Show a spiral sink and a spiral source. Here A = -K/4, so we need every eigenvalue of K to have positive real part.
4. **Testing stability without finding eigenvalues.** For a polynomial, the Routh-Hurwitz test checks a list of determinants built from the coefficients. All positive means every root lies in the left half-plane. Show it for z^2 + b z + c: stable iff b > 0 and c > 0.
5. **Cliques and target-free cliques.** Draw a 3-clique with an outside neuron receiving from all three (a target), then remove one of those arrows so the clique becomes target-free.
6. **Working modulo 3.** 4 = 1, 3 = 0 and 6 = 0 (mod 3). This gives the "every network is nondegenerate" lemma in one line.

## 5. The key insight in 6 visual steps

1. **One matrix holds everything.** Multiply the equations by 4: K = 4 on the diagonal, 3 where there is an arrow, 6 where there is none. Animate the 11 x 11 grid of 3s and 6s, with the 21 sixes lighting up.
2. **The memory solves a linear system.** K y = (1, ..., 1) gives y, and x* = 4y. All 11 entries come out positive, so every neuron fires. Show the bar chart of x*.
3. **Stability is a polynomial question.** det(zI + K) = z^11 + 44 z^10 + 196 z^9 + 1110 z^8 + 3534 z^7 + 8391 z^6 + 16203 z^5 + 21300 z^4 + 18111 z^3 + 10963 z^2 + 4931 z + 1168. Its 11 Hurwitz determinants are all positive. Ticking them off one by one (44, 7514, 1867920, ...) is a satisfying animation.
4. **Eigenvalues in the plane.** Plot the 11 eigenvalues of K: one big real one (about 39.7), four exactly equal to 1 (three of them come from the neurons with identical inputs), and three complex pairs just right of the imaginary axis (real parts 0.038, 0.050, 0.055). All lie to the right of the axis, so x* is stable. Stress how thin the margin is.
5. **Why "nondegenerate" is automatic.** Reduce K mod 3: every 3 and 6 becomes 0 and every 4 becomes 1, so K becomes the identity. Every principal determinant is then 1 mod 3, never 0. Replacing one column by the ones vector also gives determinant 1 mod 3; show this separately for the Cramer condition. That is the whole proof of Lemma 1.
6. **How small can it be?** A computer checks all 882,033,440 networks of 7 neurons (and all smaller ones) exactly and finds none. So the answer lies between 8 and 11. Show a number line with 1 to 7 crossed out, 11 marked, and 8 to 10 marked "?".

## 6. Exact figures and objects for the screen

- The CTLN equation with eps = 1/4, delta = 1/2, theta = 1 and the weights -3/4 and -3/2.
- The G11 deleted-arc table above, drawn as a directed graph: the complete graph in light grey, with the 21 missing arrows drawn as dashed red "absent" arrows.
- x* = (22, 52, 28, 31, 7, 37, 7, 67, 10, 7, 67)/292.
- The degree-11 polynomial and its Hurwitz determinants: Delta_1 = 44, Delta_2 = 7514, Delta_3 = 1867920, ..., Delta_11 = Delta_10 x 1168.
- An eigenvalue plot of K.
- A simulation: rates from a 30% perturbation spiralling back to x*, and the 3-cycle chasing round for contrast.
- A parameter-plane picture: G11 works on a blue band around (1/4, 1/2), roughly 0.02 < eps < 0.44 with delta about 1.8 eps (`region.pdf`).

## 7. Proved, computed, open

- **Proved by hand:** every CTLN at eps = 1/4, delta = 1/2 is nondegenerate (the mod 3 argument).
- **Exact computer certificate:** G11 has a stable nonclique full-support fixed point, and none of its proper induced subgraphs has a stable nonclique full support. This uses exact fractions, two independent programs, and integer Hurwitz determinants. Stable nonclique full support is also exactly verified for the 23-neuron W_4 from the public repository and our own 27- and 100-neuron examples. We make no deletion-minimality claim for those larger graphs.
- **Exact exhaustive computation:** no network with 7 or fewer neurons has such a memory at these settings.
- **Open:** whether the true minimum is 8, 9, 10 or 11. Also open: whether the rule fails at every legal setting.

## 8. Misconceptions to avoid

- This is not the first counterexample to the conjecture; Geneson's 6-neuron network is. The retained contribution is the explicit 11-neuron example, its deletion-minimality, the 8..11 size bracket and the mod-3 lemma; standard-point failure was already implied by the credited repository.
- Stable means "returns after a small nudge". It does not mean "reached from anywhere". From random starting rates G11 usually ends up in a different behaviour. Those trajectories suggest other attractors; they do not prove a basin classification.
- The 11-neuron graph was not designed by hand. A computer search shrank a 23-neuron network from the family W_k of the public repository hturcotte1/CLTN. That repository's own tables and an unrefereed theorem already imply standard-parameter counterexamples with 23 or more neurons, but they never say so. Our own independent search had reached 27 and 100 neurons. Do not present the standard-parameter failure as entirely our discovery; our contribution is the small explicit example, the bound n >= 8 and the mod-3 lemma.
- "Nondegenerate" is a technical condition (no accidental zero determinants), not a statement about stability.
- The fixed-point rates are exact fractions. The pictures of trajectories are numerical illustrations; the proof is the exact algebra.

## Final scope lock

Ready for scripting at the retained scope. Exact final scan: 882,033,440 seven-vertex digraphs, 35,842 saved candidates, zero survivors of both rational stability tests. G11 deletion check: 2,035 subsets, of which 90 are cliques, 1,778 not permitted, 167 permitted but unstable. Do not say all proper subgraphs are unstable: clique supports can be stable. The original n7 permission filter uses a rigorous residual error bound; avoid animating it as 882 million exact eigenvalue calculations. Credit hturcotte1/CLTN commit 3744200 (15 October 2026). No video folders were edited in this research pass.
