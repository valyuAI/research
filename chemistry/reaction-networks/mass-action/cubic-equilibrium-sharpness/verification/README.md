# Exact finite checks

Run from the parent directory:

```sh
python3 -B -O verification/independent_cubic_check.py
```

This standard-library checker reads `cubic-sharpness-certificate.json`. It derives the stoichiometric matrix from the reaction complexes, computes the actual mass action vector field and its derivative using rational arithmetic, and checks each prescribed equilibrium. The nonzero determinant formed from the first `n - 1` field rows plus the conservation row certifies the constrained equilibrium is nondegenerate; a separately checked stoichiometric minor justifies this choice of field coordinates. Three corrupted inputs must be rejected. `-O` leaves the checks active because failures raise exceptions explicitly.

To reconstruct the certificate, run:

```sh
python3 -B -O verification/verify_cubic_sharpness.py
```

This generator uses SymPy, tested with version 1.14.0. It builds the cubic source matrix, solves the rational interpolation system, constructs admissible products and rates, and computes restricted Jacobians for `n = 2,...,8`. It records its source hash and the finite case inventory in the certificate. Regeneration updates execution timing and may change the certificate byte hash without changing its mathematical data.

Both implementations cover 35 specified positive nondegenerate equilibria. The finite data do not prove the universal statement, exclude every other root by themselves, or establish a minimum degree. Those conclusions follow from the manuscript's all-`n` argument, Descartes' rule and the explicitly cited published quadratic obstruction. No proof-assistant verification is claimed.
