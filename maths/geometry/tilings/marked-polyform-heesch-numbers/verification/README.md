# Verification

Everything here except the encoders uses only the Python 3 standard library.

| File | Role |
|---|---|
| `check_marked.py` | Independent checker for corona witnesses of marked polyhexes and polyominoes (strict coronas, exact integers). |
| `negative_tests.py` | Corrupts every witness five ways (relabel an edge, drop a copy, shift a copy, fake an extra corona, balance the marking); all corrupted witnesses must be rejected. |
| `check_ledger.py` | Enumerates all free polyhexes with at most 4 cells and polyominoes with at most 5 cells from scratch. Checks that `results.json` lists each exactly once, that every value `h` has a witness with exactly `h` coronas, and that every upper bound is a DRAT-verified unsatisfiable base formula at `k = h + 1` for the same tile. |
| `results.json` | The ledger: per tile, `h`, witness file, and the upper-bound record (encoder command, CNF size and SHA-256, CaDiCaL time, proof size and SHA-256, drat-trim outcome and time). |
| `witnesses/*.json` | Explicit corona patches: tile cells, boundary edges with labels, copies as integer matrix `M` and translation `t` with a level. |
| `regenerate_cnfs.py` | Regenerates every base CNF with `encoder/marked_syn.py` and compares SHA-256 hashes; optionally re-solves and re-checks DRAT proofs. |
| `encoder/marked_syn.py` | Encoder used for all CNFs and witnesses (needs `python-sat`). `--cnf-only` writes the base formula without hole-blocking clauses. |
| `encoder/marked_gen.py` | Second encoder, built from polygon vertices instead of axial offsets, used to cross-check every value (`runs` summarised below). |
| `basic/check_corona.py` | Exact checker on the trihexagonal grid refined into drafters, used for Bašić's patch. |
| `basic/basic_patch.json` | Bašić's published 169-tile patch recovered on the grid (checker format); `basic_patch_grid.json` the same in encoder format; `basic_tile.json` the tile. |
| `basic/svg_to_grid.py` (+ `thd.py`, `heesch_enc.py`, `export_witness.py`) | Provenance: how the patch was recovered from Bašić's Wikimedia Commons SVG (needs numpy and the SVG file, not shipped). |

## Commands

```sh
python3 check_marked.py witnesses/*.json      # every lower bound
python3 negative_tests.py                     # checker rejects corrupted witnesses
python3 check_ledger.py                       # completeness and consistency of the ledger
python3 basic/check_corona.py basic/basic_patch.json
PYTHON=/path/to/python-with-pysat python3 regenerate_cnfs.py                          # CNF hashes
PYTHON=... DRAT_TRIM=/path/to/drat-trim python3 regenerate_cnfs.py --drat-max-clauses 2000000
```

## What each certificate proves

- A witness proves `h(P) >= k` for its tile: it is an unbalanced marking with a strict `k`-corona patch of grid-aligned copies (Definition 2.1 of the paper).
- An upper-bound record proves `h(P) < k`: the base formula `F(P, k)` (unbalanced marking with imbalance at least 1, copies within the window of Lemma 4.1, contact and interior containment, label compatibility, no hole-blocking) is unsatisfiable. Exchanging bumps and nicks covers imbalance at most -1. The DRAT proofs were checked with drat-trim and then deleted because of their size; the CNF hash lets anyone regenerate the exact formula and repeat the check.

## Tools and versions used

- CaDiCaL 3.0.1 (Homebrew), binary DRAT output.
- drat-trim built from source (the copy vendored in the Layr-Labs/heesch repository; SHA-256 of the source tarball `d834b649...`, matching upstream commit `2e3b2dc`).
- python-sat 1.9.dev16 (CaDiCaL 1.9.5 inside, used for witness search), Python 3.13.

## Run times

Wall-clock times on a shared, heavily loaded 14-core laptop are in `results.json` (`cadical_seconds`, `drat_trim_seconds`).

## Finishing checks

`audit_basic_boundary.py` replays the original geometry checker and adds a simple-boundary-cycle test at every level; `boundary.py` also guards the marked witnesses. `negative_ledger.py` rejects six corrupted metadata records. `check_crosschecks.py` checks the 64 marked outcomes and 41 unmarked comparisons in retained logs. `check_ledger.py` requires the correct one-slot scope, hashes and all completion markers in the retained DRAT records. These all run in the default build.

A retained upper-bound record documents a completed proof check; it is not itself a DRAT proof. Fresh DRAT replay requires regenerating the CNF/proof. All 34 original logs are shipped; no proof assistant verified the encoder or checker. See `../readiness.md`.
