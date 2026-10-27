# Checked proofs

Lean sources for the research collection, pinned to Lean and mathlib 4.35.0.

- `HalesJewett.lean`: the complete prime-successor theorem on finite cubes.
- `Elasticity.lean`: the matrix identities behind the collision reduction.
- `LotkaVolterra.lean`: the three-vertex path obstruction.
- `Resetting.lean`: finite-kernel optimality and an exact counterexample.
- `AcrMultistability.lean`: two chemical reaction lists, their exact positive steady states and absolute concentration robustness; stability and the dimension theorem remain outside Lean.
- `CubicTicTacToe.lean`: abstract matching surplus and deletion lemmas; the board enumeration and game theorem remain outside Lean.
- `CommonQuartetPotential.lean`: the sharp real-variable potential inequality and its equality example; trees, iteration and the exact quartet threshold remain outside Lean.

The files are in [`ValyuResearch/`](ValyuResearch/). See the [coverage ledger](../docs/formal-coverage.md) for exactly which paper claims are formalized.

```bash
lake exe cache get
lake build
lake env lean Audit.lean
```

On Linux with `bubblewrap`, replay every project theorem and its proof dependencies with all bundled checkers:

```bash
bash replay-proofs.sh /absolute/path/to/diagnostics
```

The replay records the complete theorem inventory and export hash. Passing the ordinary Lean build and axiom audit is recorded separately from completing all independent checkers.
