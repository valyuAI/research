# Rigidity of the 92 Johnson solids with fixed edge lengths and flat faces

[Up one level](../README.md)

**Status:** theorem (computer-assisted; two independent first-order checkers, plus exact flex and second-order checks).

## Claim

Model: Adrian-Himmelmann, Schulze, Winter (arXiv:2505.00874v3) and Adrian-Himmelmann, Winter, Zhang (arXiv:2607.09252v1). A convex polytope is a point-hyperplane framework: a deformation must keep every edge length and the planarity of every face, but face shapes (angles) may change. Johnson solids are taken with unit edges.

1. **Exactly 41 Johnson solids are first-order rigid:** J1, J2, J6, J10-J13, J17, J22-J25, J32-J34, J44-J48, J50, J51, J61-J66, J68-J71, J84-J92.
2. **The other 51 are first-order flexible.** The exact flex-space dimensions are in `verification/results/classification.json` and in the paper's table, e.g. J3 1, J38 7, J72 6, J81 4.
3. **45 are flexible** (explicit continuous flexes): J3-J5, J7-J9, J14-J16, J18-J21, J26-J31, J35-J43, J49, J52-J57, J67, J72-J80. Of these, 38 flex by rotating one summand of an edge partition $P = s_1 + s_2$ about an admissible axis (a Minkowski-type flex adapted to summands with parallel faces); the 7 augmented prisms flex through their prism.
4. **Six are first-order flexible but second-order rigid, hence rigid:** J58, J59, J60 (augmented dodecahedra) and J81, J82, J83 (diminished rhombicosidodecahedra). J60 and J82 are prestress stable (exact). J58, J59, J81 and J83 are exactly not prestress stable: stored positive definite matrices are exactly orthogonal to all their second-order stress forms. J83 also has an independent pencil determinant test.

So **47 Johnson solids are rigid and 45 are flexible.**

5. **Every antiprism is first-order rigid** (all n >= 3, any positive height): a Fourier decomposition of the stress space gives a 4 x 4 block with determinant 4R^4(c-1)^3(c+1)(z-1)(z^2 - 2cos(2 pi/n) z + 1)/z^3, plus explicit minors for the three low modes. Every prism is flexible (polygon + segment). Together with AHWZ, this determines the rigidity of every strictly convex polyhedron with regular faces except the truncated dodecahedron.

The regular dodecahedron and truncated icosahedron are also checked: each has five first-order flexes, a degree-six Macaulay matrix of rank 210/210, and a stored exact non-prestress certificate. Their rigidity verdicts are already in AHWZ; these are consistency checks and exact certification.

## What is new, and closest prior work

- AHWZ (arXiv:2607.09252v1) treat the 31 Platonic, Archimedean and Catalan solids, leaving the truncated dodecahedron open. Their software, DeformationPaths.jl, tests the same 31. We inspected both Zenodo deposits, 10.5281/zenodo.20595067 (supplement) and 10.5281/zenodo.19830468 (v1.1.0), plus GitHub main and all 15 branches (newest 2026-09-23). They contain no Johnson solid.
- Three earlier statements agree with our table: Kochetkov arXiv:2008.07285v1 (convex quadrangular pyramids are determined locally by their edge lengths, so J1 is rigid), arXiv:2302.14194v2 Fig. 16 (the square pyramid J1 is rigid as a polytope) and arXiv:2505.00874v3 Fig. 6 (a "cube with pyramid roof", combinatorially J8, is flexible).
- We searched arXiv listings after 2026-09-01 and the papers citing 2607.09252: 2610.17004, 2609.02818, 2607.14878, 2609.14645, 2610.31212, 2610.09990, 2602.08016v2 and 2603.19827. None treats Johnson solids. The DeepResearch priority audit (task `geometry-johnson-priority`, DR-022) found no prior classification either.
- New: the full classification; exact flex dimensions; six natural rigid-but-not-first-order-rigid polytopes (before this, the natural examples were the dodecahedron and the truncated icosahedron); and the J80 (flexible) versus J81 (rigid) contrast.

## Confidence

- Correctness of the classification and of the antiprism theorem: **high**. Two independent checkers agree on all 92 rank values: modular rank over a number field, and interval-arithmetic rank of a different, vertex-only formulation. Flexes and second-order certificates are exact. The written lemmas (vertex-only equivalence, summand-rotation flex, prism flex, stress test usage) are short. An adversarial review is recorded below.
- Originality: **moderate-high**. Nothing found after a targeted search of the source papers, their software and data, recent arXiv listings and citing papers. A search cannot prove absence.
- Significance: a complete, natural classification that extends AHWZ's tables. It introduces no new general criterion.

## Reproduce

```sh
sh build.sh            # replays every checker (about 30-60 min on a loaded laptop) and builds paper.pdf
sh build.sh --quick    # partial replay only, using saved second-order results
```

See `verification/README.md` for the individual commands and what each one certifies.

## Reviews and how they were handled

- **DeepResearch max review** (`geometry-johnson-review`). No mathematical step fails. Its requests were handled as follows:
  - AHWZ's numbering is now used exactly (Cor. 3.2, Thm. 3.3, Prop. 3.6, Thm. 4.1, Thm. 4.2).
  - The paper states the equivalence between the HSW and AHWZ formulations and the invariance of the second-order forms modulo trivial motions.
  - The J-number labels are now checked (`check_labels.py`, plus an isomorphism check against the OSCAR "Exact Johnson Solids" dataset for the 91 solids it contains).
  - J83's prestress status is decided exactly.
  - The paper notes that the flex dimensions are first-order counts.
  - New prior art is cited: Kochetkov arXiv:2008.07285 (quadrangular pyramids are rigid with fixed edge lengths, consistent with J1). The review also mentions a 2024 Cornell thesis by Zhang on the rigidity of the dodecahedron; its body could not be read, and it is not cited.
  - The review's worry about J58/J59 (a residual real double point) is excluded by the stdlib Sturm count: the gcd has 0 real roots. A separate sympy Groebner elimination now checks both affine/projective charts and a negative quadratic discriminant. It shares the stress forms, but not the resultant, gcd or Sturm code.
- **DeepResearch heavy review of the antiprism theorem** (`geometry-antiprism-review`). No error found and no prior art located. It asks that "convex" be read as strictly convex (done) and that Zalgaller's 1967 original be noted.
- **Independent code-soundness review** (fresh agent; corrupted-input tests, fuzzing of the interval arithmetic, float re-derivation of all 92 ranks and of the second-order forms). It found no verdict-changing bug and recommended four fixes, all applied:
  - explicit raises instead of `assert`;
  - non-zero exit codes on failure;
  - stronger structure checks in `prismflex.py`;
  - label checks.

## DeepResearch tasks

- `geometry-johnson-priority` (DR-022, heavy): priority audit.
- `geometry-johnson-review` (DR-070, max): adversarial review of the statement and the proof.
- `geometry-antiprism-review` (DR-039, heavy): adversarial review and priority check of the antiprism theorem.

## Files

- `paper.tex`, [public PDF](../../../../public-release/papers/johnson-solids.pdf), `references.bib`: the paper.
- `verification/`: exact data, checkers, certificates and results.
- `video-brief.md`: brief for the explainer video.

Final replay, precise review responses and remaining limits: [readiness.md](readiness.md). Build runs are sequential at nice 10, emit heartbeats, preserve logs, and stop on any failed checker. Full mode requires sympy.
