# Verification

Run from the package directory (`sh build.sh` runs all of these and rebuilds the PDF).

| command | needs | checks | output |
|---|---|---|---|
| `python3 -B verification/verify_examples.py` | standard library | Examples 5.1, 5.2 and Remark 5.3 with exact rationals: mass-action field built from the reaction list, the factor forcing ACR, at-most-bimolecularity and counts (reactions, complexes, reactant complexes, dimension), reduction of all positive steady states to an explicit univariate polynomial with the listed roots, exact Jacobians, characteristic polynomials and Routh-Hurwitz tests | `examples-certificate.json`, `verify_examples.log` |
| `python3 -B verification/four_reactant_exponents.py` | standard library | Proposition 4.4: for all 1365 sets of four at-most-bimolecular complexes in four species, the kernel vector `b` of `M = [y1-y4; y2-y4; y3-y4]` (when rank 3) has at most 3 distinct coordinates whenever one coordinate is zero (922 such sets) | `four_reactant_exponents.log` |
| `python3 -B verification/independent_check.py` | SymPy | second implementation: parses a text reaction list, computes all steady states off the coordinate hyperplanes by a saturated lexicographic Groebner basis, keeps the positive ones, checks ACR and the stability pattern by exact cubic Routh-Hurwitz inequalities and positive-real-root certificates from negative constant coefficients; redoes the Remark 5.3 example and the Proposition 4.4 enumeration with SymPy nullspaces | `independent_check.log` |
| `cd ../../../../formal && lake env lean ValyuResearch/AcrMultistability.lean` | Lean 4 + Mathlib (repo `formal/`) | for both examples: the mass-action field computed from the reaction list, ACR in A, and the exact set of positive steady states | `lean_check.log` (empty on success) |

Expected final lines: `ALL CHECKS PASSED`, `FOUR-REACTANT CHECK PASSED`, `INDEPENDENT CHECK PASSED`.

What is computed versus proved: the examples are fully certified by finite exact computation. Theorem 3.1, Corollaries 4.1-4.2 and Theorem 4.3 are hand proofs with no computational input. Proposition 4.4 is a hand argument; its combinatorial step (at most three distinct kernel values) is proved by hand in the paper and independently confirmed by the enumeration above.

The independent checker also enforces the exact published steady-state lists, reaction/complex counts, dimension and the 922/3 enumeration result. Positive-state filtering uses exact symbolic sign decisions and refuses an undecided sign.
