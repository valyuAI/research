# Lean determinant certificates

This package checks the eleven explicit minor identities used in the dimension
certificates. Each theorem states an identity over `ℂ` involving actual
`Matrix.det` expressions. It does not assume the desired identity.

**Status: all eleven determinant certificates compiled and passed the axiom
audit.** CI run `39114539272`
passed on 18 October 2026 at commit `351b43b`. The audit allows only
`propext`, `Classical.choice`, and `Quot.sound`. The earlier run reached the
6 GB memory guard; splitting compilation units preserved every proof text
and allowed the complete run to finish within the same limits. This package
is outside the default `formal/` library, and the collection's existing
six-independent-checker success does not cover it. Run `39114539272` was in the
project's earlier, non-public CI and its log is not retained here. The
[formal coverage ledger](../../../../../../docs/formal-coverage.md#additional-determinant-certificates)
records its scope; rerun the compilation below to reproduce it.

The manual **Check pending elasticity certificates** workflow compiles the core,
twenty-one batches, umbrella module, and axiom audit sequentially with two Lean
threads. It uses the repository's pinned Lean and Mathlib 4.35.0 environment,
retains logs even on failure, and records progress and resources every thirty
seconds. Compilation has a 45-minute budget inside a 60-minute job. A process
above 6 GB RSS or less than 1 GB free disk stops the run with a failure. Such a
resource failure does not establish that an identity is false. The
quintic chunks occupy smaller modules, with its final identity in a separate
module. This changes only compilation boundaries, preserving the proof text.

For a local source-only check, with no Lean compilation:

```sh
python3 -B -O run_checks.py --verify-sources-only
```

For compilation, choose a fresh output directory outside the source checkout:

```sh
python3 -B -u run_checks.py --project /path/to/research/formal \
  --output /path/to/fresh-temporary-output
```

`source-manifest.json` pins every proof input, retains original hashes, and records
the declaration-preserving repartition of the two previously pending batches.
The translation check independently compares all 91 matrix entries, eleven
target polynomials, and 237 minor index lists with the rational certificate
input. Lean then checks the determinant expansions and polynomial identities.
The final audit requires all eleven named certificates and every theorem owned
by the core and batch modules, allowing only `propext`, `Classical.choice`, and
`Quot.sound`. No `sorry`, `admit`, `native_decide`, or new axioms are permitted.

The successful run establishes compilation and that axiom audit. It does not yet
run the six independent proof checkers, formalize the initial-ideal dimension
argument, or formalize the full elasticity theorem. Generated `.olean` files
stay in the temporary output directory and are not committed or uploaded.
