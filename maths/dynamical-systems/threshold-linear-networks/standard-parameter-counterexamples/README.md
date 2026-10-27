# Target-free clique counterexamples at the standard CTLN parameters

**Claim.** Curto, Geneson and Morrison conjectured that the stable fixed points of a combinatorial threshold-linear network (CTLN) are supported exactly on target-free cliques ([AAM 2024, Conjecture 1.2](https://arxiv.org/abs/1909.02947); Open Question 10 in [Curto-Morrison, Notices AMS 2023](https://arxiv.org/abs/2301.12638)). The conjecture is already known to be false in general. This note shows that it also fails at the parameters used throughout the CTLN literature, eps = 1/4, delta = 1/2, theta = 1:

1. **Theorem.** Every CTLN at these parameters is nondegenerate, because (I - W)/eps is congruent to I modulo 3.
2. **Counterexample (exact certificate).** The 11-vertex graph G11, which is the complete digraph with 21 arcs deleted, has a linearly stable fixed point with full, nonclique support.
3. **Vertex-minimality (exact).** No proper induced subgraph of G11 has a stable nonclique full support.
4. **Exact exhaustive computation.** No digraph on at most 7 vertices has such a support at these parameters.

So the smallest counterexample support at the standard parameters has between 8 and 11 neurons.

[Paper](../../../../public-release/papers/standard-parameter-counterexamples.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md) · [Reviews](review.md) · [Final readiness](readiness.md)

## Status and confidence

| Item | Type | Correctness confidence | Originality confidence |
|---|---|---|---|
| Mod-3 nondegeneracy | theorem (two-line proof) | high | moderate. It is an obvious analogue of Geneson's mod-2 argument, and we found no statement of it. |
| G11 counterexample | exact computation, two independent checkers | high | moderate. See prior art below. |
| No proper induced subgraph of G11 works | exact computation (2035 subsets) | high | - |
| No example with n <= 7 | exact exhaustive computation (nauty enumeration, exact integer and rational tests) | high, given the enumeration | low to moderate. It also follows from the unrefereed n = 7 map in the repository below, which we did not replay. |
| Minimum is 8, 9, 10 or 11 | open | - | - |

## Closest prior work, and what is new

- **Geneson, [arXiv:2607.21396v1](https://arxiv.org/abs/2607.21396)** (23 Jul 2026). Six-vertex counterexample at delta = 29 eps/25, eps -> 0, q -> 29/25. It is not stable at the standard parameters.
- **Anonymous, "Six Is Minimal", [Zenodo 23089682](https://zenodo.org/records/23089682)** (1 Oct 2026, unrefereed). Shows supports of size at most 5 are impossible at all legal parameters, and gives a family with q -> 1.
- **[github.com/hturcotte1/CLTN](https://github.com/hturcotte1/CLTN)**, branch `claude/compassionate-maxwell-mtoyeb` (unrefereed; accessed 26 Oct 2026 at head `f061cd5`). It reports exact parameter maps for n = 6 and n = 7, with no counterexample on 7 or fewer vertices once q is at least the plastic number, about 1.3247. It also gives several infinite families. Its "Theorem Q2" family W_k (commit `9a4ab7f`, 15 Oct 2026) is a 7-vertex core plus two bidirected classes of sizes k and 3k, so n = 7 + 4k. Files under `notes/theorem_A_fixed/` (commit `3744200`, 15 Oct 2026) add two things. A table gives the exact stable t-intervals at beta = 3: k = 4 is stable for t > 2.0932. An unrefereed "Theorem B" says W_k with k >= 6 (n >= 31) is stable at every legal point with beta <= 3. **Together these imply counterexamples at the standard point (beta = t = 3), with nondegeneracy supplied by our Lemma 1, although the repository never names this point.** We confirmed exactly that W_4 (23 vertices) works there ([`verification/examples/W4.json`](verification/examples/W4.json)) and W_3 does not. G11 was obtained by deleting vertices from W_4 and repairing stability by local search.
- **Our independent route.** Before finding the repository, we built counterexamples at the standard parameters by continuation from Geneson's graph: a 100-vertex graph with 7 classes of identical rows, whose stability reduces to a 7 x 7 matrix, and a 27-vertex graph. Both are in `verification/examples/`.

**What is new, honestly scoped.** Counterexamples at the standard parameters are implied, though not stated, by the repository above. Our increment has four parts: an explicit 11-vertex example at that point, minimal under vertex deletion (the implied ones have 23 or more vertices); the mod-3 nondegeneracy lemma; an independent exact exclusion of 7 or fewer vertices; and hence the bracket 8 <= minimum <= 11. The two DeepResearch audits found no prior statement of any of these. Their coverage of author pages, OpenReview and repository commits between 15 and 26 Oct was incomplete. Eleven-vertex counterexamples at other parameters already exist; for example the r = 1 member of the Zenodo family, at eps = 1/123, is not isomorphic to G11.

## Caveats

- Stability is linear (local) and slow: the slowest decay rate of the Jacobian -K/4 is about 0.0094, with oscillation period about 37. For G11, sampled random perturbations of up to 30% relative size return to the fixed point. Trajectories from 40 random initial conditions in [0, 0.5]^11 all went elsewhere, which suggests other attractors but does not prove their classification. For the 27-vertex example the basin is tiny: sampled perturbations of norm 3e-3 escape. These are numerical observations, not uniform basin bounds.
- G11 remains a counterexample on a band of parameters around (1/4, 1/2), roughly 0.02 < eps < 0.44 along delta of about 1.8 eps ([figure](region.pdf), floating-point scan, illustration only).
- No Lean formalization.

## Reproduce

```sh
sh build.sh             # both exact example checkers, n <= 6 scan, saved n7 replay, positive control, PDF
sh build.sh --full-scan # additionally rescans all 882,033,440 digraphs on 7 vertices (hours; needs nauty + cc)
```

Both builds require a C compiler, nauty, LaTeX and Python with `python-flint`; set `PYTHON=/path/to/python` when using a virtual environment. The default build reruns every example through the standard-library checker and the independent FLINT checker, checks all proper induced subgraphs of G11, rechecks all saved n7 candidates and validates their original scan totals. The full option additionally regenerates the seven-vertex scan.

## DeepResearch tasks

- `modelling-ctln-prior` (DR-024): priority audit, which found the Zenodo preprint.
- `modelling-ctln-review1` (DR-029): adversarial review of the 100-vertex example. It raised nondegeneracy, which Lemma 1 now resolves.
- `modelling-ctln-review2` (DR-074): max-mode adversarial and priority review of the final claims.
