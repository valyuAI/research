# Python verification guards, 26 October 2026

The ACR independent checker and common-quartet iteration checker now refuse Python optimization mode, including an inherited `PYTHONOPTIMIZE=1`. Both use assertions for substantive verification. This is a validation fix; their normal-mode mathematics is unchanged.

Before the fix, two deliberately invalid probes failed normally but exited successfully under `-O`:

- ACR: `exact_stability(Poly(x**3+x**2+x+2, x))` returned the positive-real-root classification after its rejection assertion was removed. Its positive coefficients rule out a positive real root.
- Quartets: replacing `keeps_sharp_factor` with a function returning `False` allowed a weighted iteration to print success after its assertions were removed.

After the fix, both negative probes fail in normal and optimized modes. Direct execution with `PYTHONOPTIMIZE=1` also fails explicitly. A fresh normal ACR run passes both complete positive steady-state lists, exact stability classifications, the decoupled control and all 922 qualifying reactant sets. A fresh quartet check passes eight exact thresholds, the two factor controls and 18 seeded families across k=1..6. It does not repeat the earlier 613-family replay or finite h(3) enumeration.

The [before](before.json) and [after](after.json) records contain source hashes, exit codes and log hashes. The earlier completion manifests remain historical snapshots. The guard adds three lines to each checker and does not change any manuscript, Lean source, narration, scene or media file. The new evidence does not replace the earlier full mathematical reviews.

Reproduction: invoke the two checker modules with `python3 -B -O` or `PYTHONOPTIMIZE=1 python3 -B`; each must exit nonzero with `verification requires Python assertions enabled`. Run ACR normally for its full independent check. The targeted quartet families use `run_weighted(k, 3, 800+k)` for k=1..6. Python 3.13 and SymPy 1.14.0 were used.
