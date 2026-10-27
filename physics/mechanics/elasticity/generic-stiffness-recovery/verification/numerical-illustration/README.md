# A synthetic reconstruction example

This is a numerical illustration of the fifteen-direction corollary, separate from the proof. It uses one deterministic positive-definite tensor, dimensionless density-normalized stiffness, and simulated phase wave speeds. There are no experimental measurements here.

```bash
python3 reconstruct_from_directions.py
```

The script compares two objectives using the same fifteen measurement directions:

- The theorem's 22 scalar observables: six trace values, fifteen second-characteristic values and one determinant value.
- All 45 measured phase wave speeds, retaining data that the theorem does not need for noiseless identifiability.

Four fixed initial guesses are tried for each objective. Start 0 is a diagonal Voigt matrix scaled by the known reference matrix trace; it is an oracle-scale control, not an isotropic elastic tensor or a fully data-derived initialization. Starts 1-3 are independent seeded random positive-definite matrices. All three noisy fits selected for the figure use these independent random starts. A fifth full-data solve starts from the compressed-data fit with the smallest residual. That selection uses measured data only, not the known answer. Every attempt is retained in `reconstruction_results.json`, including inaccurate local minima and a previous iteration-limit case in `reconstruction_results_initial22.json`.

The exact-data compressed solve recovers the reference tensor to about 10^-12 relative Voigt-matrix Frobenius error from two starts. The other two starts reach inaccurate local minima. Direct full-data optimization also fails from all four initial guesses in this example. Initializing it with the compressed-data fit gives accurate recovery.

| Relative phase-speed noise standard deviation | Compressed fit selected by residual: tensor error | Full-data refinement: tensor error |
|---:|---:|---:|
| 0.001% | 5.45% | 0.00772% |
| 0.01% | 15.8% | 0.0989% |
| 0.1% | 45.2% | 0.577% |

These are three individual noise draws for one tensor, not average performance or a general stability bound. The finite-difference Jacobian condition numbers at the reference tensor are approximately 10,273 for the compressed objective and 38 for all speeds, using the stated upper-triangular Voigt coordinates and relative-residual scaling. Those numbers depend on the coordinates, weights and chosen tensor. Reported reconstruction error is the unweighted Frobenius error of the 6 by 6 Voigt matrix, not a coordinate-invariant fourth-order tensor norm.

The example shows why generic uniqueness should not be read as a guarantee that a naive optimizer will work or that discarding additional measurements is harmless. It suggests a useful initialization strategy, but does not establish that strategy's originality or reliability across materials. Such claims would require a broader benchmark and a separate literature review.

Requirements used: NumPy 2.3.3 and SciPy 1.16.3. No network access is needed. `plot_results.py` additionally uses Matplotlib 3.10.6 and produces a standalone figure.
