# Verification

All checkers use only the Python 3 standard library (`fractions`, `json`, `math`), except `check_irreducible.py`, `check_antiprisms.py` and `check_real_zeros_independent.py` (sympy) and `check_labels_oscar.py` (networkx). Every checker raises or exits non-zero on failure, and no check relies on `assert`, so `python3 -O` is safe. Run them from this directory. Timings were measured on a heavily loaded laptop.

| command | certifies | output |
| --- | --- | --- |
| `python3 -B check_labels.py` | Each data file is the Johnson solid it is labelled as. The combinatorial automorphism group order equals the known symmetry order for all 92; by Cauchy, every combinatorial automorphism of a regular-faced convex polyhedron is a symmetry. Ortho and gyro members of the bicupola pairs are told apart, and no two data sets share these invariants. | `results/labels.log` |
| `python3 check_labels_oscar.py DIR` | Optional, needs networkx: the vertex-facet incidence graphs are isomorphic to those of the independent OSCAR dataset "Exact Johnson Solids" (Zenodo 10729583) for all 91 solids it contains (it lacks J79). | `results/labels_oscar.log` |
| `python3 -B check1_rank.py` | Exact validation of all 92 data sets: Sturm-isolated real embedding; unit edges, planar faces, regular faces, strict convexity, Euler characteristic, each edge in two faces. Rank of the point-hyperplane rigidity matrix modulo a prime, a lower bound for the real rank. 41 solids have rank = cols - 6, so they are first-order rigid. (about 5 min) | `results/check1_rank.json` |
| `python3 -B check2_independent.py` | An independent re-implementation sharing no code with the other checkers. Vertex-only formulation with determinant coplanarity rows; formal ring arithmetic for equalities; 640-bit fixed-point interval arithmetic for inequalities and for an interval Gaussian-elimination rank lower bound. 41 solids have rank 3V - 6. For the other 51 it verifies an explicit exact first-order flex (`certificates/flex_vectors.json`) formally, with non-triviality certified by an interval. (about 5 min) | `results/check2.json` |
| `python3 -B check2_independent.py --rank-only` | Negative control: the interval rank lower bound equals 3V - 6 - d for every solid. | `results/check2_rank_only.json` |
| `python3 -B check_flex_finite.py` | Continuous flexes for 45 solids. 38 come from rotating one summand of an edge partition (`minkflex.py`, partitions in `certificates/minkowski_partitions.json`); 7 are augmented prisms (`prismflex.py`). | `results/flex_finite.json` |
| `python3 -B check_second_order.py` | J58, J59, J60, J81, J82, J83, over Q(sqrt 5). Exact flex and stress bases, second-order forms, and a no-common-real-zero certificate for each: a single nonzero form (J60), full-rank Macaulay matrix (J81, J82, J83), or resultants, gcd and Sturm (J58, J59). Also exact prestress stability for J60 and J82 and an exact pencil test for k = 2. (about 15 min) | `results/second_order.json` |
| `python3 -B exact_flex_dims.py` | Exact rank over the coordinate field for the 51 first-order flexible solids, which gives the exact flex dimensions. (about 30 min) | `results/exact_flex_dims.json` |
| `python3 -B check_antiprisms.py` | Antiprisms (needs sympy): the symbolic Fourier-block determinant and the low-mode minors behind first-order rigidity of every antiprism. | stdout |
| `python3 -B check_antiprisms_numeric.py 25 [height]` | Floating-point cross-check (numpy): corank 6 for 3 <= n <= 24. | stdout |
| `python3 -B check_irreducible.py` | All minimal polynomials are irreducible over Q (needs sympy; required only by checker 1). | stdout |
| `python3 -B summarize.py` | Cross-checks all of the above and writes the classification and the paper table. | `results/classification.json`, `results/table.tex` |

`gen_flex_vectors.py` regenerates `certificates/flex_vectors.json`. It is a generator, not a checker: its output is trusted only because `check2_independent.py` verifies it.

## Data

`data/JNN.json` holds the solid's name, a monic integer minimal polynomial (low degree first), a rational isolating interval, an optional `tower` `[w]` meaning the field K(sqrt w), vertex coordinates, and faces as cyclic vertex lists.

The data come from D. McCooey's exact coordinates (https://dmccooey.com/polyhedra/), converted to a primitive element by PSLQ/LLL; J23, J28, J37 and J84 were constructed directly, and J87 is J86 plus a square pyramid. That conversion is untrusted; the exact validation in both checkers certifies the data. By Cauchy's rigidity theorem, a validated convex realization with regular faces and the given combinatorics is the Johnson solid.

## Soundness notes

- Checker 1: a modular rank is a lower bound for the real rank only when the coordinate ring is a field. `check_irreducible.py` covers the base fields. `tower.py` certifies that each radicand is a non-square, by its norm or by a quadratic non-residue at a prime where the minimal polynomial is squarefree.
- Checker 2 needs no irreducibility. A formal identity in Q[x]/(m) holds at every root, and all inequalities and ranks are certified at one root located by bisection on a certified sign change.
- The second-order forms are invariant under adding trivial motions, because the constraints are invariant under the Euclidean group. So testing them on a complement of the trivial motions is the stress test of arXiv:2607.09252, Theorem 4.2.

## Resume additions and replay contract

- `check_prestress.py`: recomputes exact flex/stress bases for J58, J59, J81 and J83, then checks the stored matrices in `certificates/prestress.json`: dimensions, symmetry, exact trace orthogonality and positive definiteness. No numerical optimizer is run in the build. The original failed J81 search remains in `results/prestress.json` and `.log` as historical evidence; current verdicts are in `results/prestress_replay.json`.
- `check_extra.py`: recomputes the dodecahedron and truncated icosahedron forms; certifies flex/stress dimension 5, Macaulay rank 210/210 in degree 6 and exact dual certificates. Writes `results/extra_replay.json`. Avoids the old unsuccessful integer search for a positive stress and the unnecessary duplicate form computation.
- `check_real_zeros_independent.py`: sympy Groebner elimination for J58/J59. It shares the exact stress forms but independently checks the real-zero exclusion using negative discriminants and the projective chart at infinity. Writes `results/real_zeros_independent.json`.
- `run_build.py`: full build stops on the first nonzero exit, requires all symbolic checks, writes each stage log plus exit codes, durations and input SHA-256 hashes to `results/replay/<UTC>/`, and emits a heartbeat every 25 seconds. Old logs are preserved. `--quick` is explicitly a partial replay, not certification of the full theorem.
- `check_antiprisms.py` now enforces equality of both low-mode minors as well as the generic determinant; it previously only printed the minors. Remaining optimization-sensitive assertions in the field constructor and symbolic determinant check were replaced by explicit errors.

The optional old numerical proposal code is not part of the verification trust base. Certificates were found numerically and rounded, then accepted only by exact checks. J81 required accurate evaluation of the algebraic coefficients for the proposal; this does not change the exact checker.
