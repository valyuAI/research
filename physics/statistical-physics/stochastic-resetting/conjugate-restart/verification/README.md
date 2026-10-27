# Restart: exact certificates and numerical checks

```bash
python3 verify_resetting.py
```

Tested with Python 3.13.7, NumPy 2.3.3, SciPy 1.16.3 and SymPy 1.14.0. The script prints progress and writes `resetting_verification.json` beside itself.

The finite-chain calculations use exact SymPy rationals. They verify the symmetric-kernel gap and the nonreversible three-state counterexample, including the strict cost change

```text
J(9/10) - J(1) = -761111595 / 7705213313411 < 0.
```

The Brownian checks compare independent time and spatial integrals at nine points, then evaluate 40 exponential-mixture restart laws for an exponential target-distance density. The random seed is fixed. All reported quadratures must be finite; the output includes estimated integration errors. These numerical examples do not establish the infinite-dimensional optimum. That statement rests on the written analytic proof, and is not part of the current Lean formalization.
