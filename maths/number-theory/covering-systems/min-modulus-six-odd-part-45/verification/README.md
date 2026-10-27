# Verification

Everything here checks **Proposition 3.1** of the paper. Every system that uses each modulus in
M2 = {6, 9, 10, 12, 15, 18, 20, 30, 36, 45, 60, 90, 180} at most once, with any residues, has
Q_2(ρ) = Σ_{x mod 4} φ_ρ(S_x) ≥ R(ρ) = Σ_d ρ_d for at least one ρ in [`prices.txt`](prices.txt).
The theorem then follows from the doubling lemma (paper, Lemma 2.2 and Corollary 2.3), which is proved by hand.

Column order in `prices.txt`: ρ_1 ρ_3 ρ_5 ρ_9 ρ_15 ρ_45.

## Files

| File | Role |
|---|---|
| `prices.txt` | The 11 integer price vectors (the certificate data) |
| `prices_first10.txt` | The first 10 vectors, for the negative control |
| `c/phi.h` | Exact min-cost cover φ_ρ(S) via the product structure Z/45 = Z/9 × Z/5 |
| `c/wsc_brute.h`, `c/test_phi.c` | Brute-force branching cover, and a self-test comparing it with `phi.h` on 20,000 random instances |
| `c/dfs2.c` | Main search: 14 level-0 orbits under (S3 wr S3) × S5, tree symmetry, multi-price pruning |
| `c/gen.c`, `prices_gen_order.txt` | Generic C search for odd part 3^B·5. Cover by dynamic programming over the 3-adic tree; symmetry by swapping identical sibling subtrees, identical rows and identical 2-adic halves; level-0 moduli may be skipped. Prices are in type order 1,5,3,15,9,45 |
| `c/dfsg.c` | Third C search: translations only, no tree symmetry. Too slow on this machine; stopped after 17.8M nodes with 0 survivors |
| `check_p2.py` | Independent standard-library Python search: residues mod 45, 135 translation-normalised roots, its own cover routine (self-tested against exhaustive branching at start-up) |
| `control_m4.py`, `control_m4_L360_covering.json` | Control: a real covering (minimum modulus 4, moduli dividing 360) has Q_2 < R for every vector, and the level-2 part of the source paper's infinite covering has Q_2 = R for vectors 3, 9 and 10 |
| `calib.py` | Generic version (any odd part D, minimum modulus m) that grows its own price family from empty; calibration on cases with known answers |
| `logs/` | Run logs of all three searches, the negative controls and the calibration |

## Commands

```sh
cc -O3 -o test_phi c/test_phi.c && ./test_phi                       # mismatches 0
cc -O3 -o dfs2 c/dfs2.c && ./dfs2 prices.txt 1 -1 surv.txt          # TOTAL nodes 498464 survivors 0
./dfs2 prices_first10.txt 100000 -1 surv10.txt                      # TOTAL nodes 708955 survivors 1704
cc -O3 -o gen c/gen.c && ./gen 2 6 2 prices_gen_order.txt 1 sg.txt  # TOTAL nodes 66821 survivors 0
python3 -B check_p2.py prices.txt 0 135                             # 4,684,432 nodes, 0 survivors (about 1 h per 45 roots here)
python3 -B check_p2.py prices_first10.txt 21 22                     # root 21 = orbit 3: 200024 nodes, 1560 survivors
python3 -B control_m4.py                                            # control 1: PASS
python3 calib.py 9 4 1; python3 calib.py 15 5 2                     # NO SURVIVORS (known negative cases)
python3 calib.py 9 3 1; python3 calib.py 27 4 1                     # ALIVE survivor (coverings exist)
```

`dfs2 FAMILY MAXSURV ORBIT OUT`: ORBIT = -1 runs all 14 orbits. `check_p2.py FAMILY LO HI` runs roots LO..HI-1. Root number 45j + r (j = 0, 1, 2; 0 ≤ r < 45) fixes the level-0 classes 0 mod 9, 5j mod 15 and r mod 45.

## What each reduction relies on

* **Level-0 moduli present.** If a covering omits 9, 15 or 45, adding any class with that modulus keeps it a covering.
* **Translations** b ↦ b + t map coverings to coverings with the same moduli. Choosing t ≡ -r9 (mod 9) and t ≡ -r15 (mod 5) puts the classes mod 9 and mod 15 at 0 mod 9 and 0 mod 5 (135 roots).
* **(S3 wr S3) × S5** (only in `dfs2.c`). Permutations of Z/9 that preserve the three classes mod 3, combined with any permutation of Z/5, map every residue class mod d | 45 to a class mod d. Applied to the y-coordinate, they preserve moduli and coverage. The orbits of (class mod 9, class mod 15, class mod 45) number 14. The Python checker does not use this reduction, so it independently covers it.
* **Tree symmetry.** If the two halves b ≡ 0 and b ≡ 1 (mod 2) carry the same pair of columns, only one half is branched on. Likewise, columns x and x+2 (mod 4) are interchangeable when equal. `dfsg.c` does not use this reduction.
* **Pruning.** A level-i class meets 2^(2-i) columns, and φ drops by at most ρ_d per column (inequality (1) in the paper). A branch is closed when Q_2(partial) - Σ_{undecided} 2^(2-i) ρ_d ≥ R for some ρ.
* **Skip branch.** Every modulus may also stay unused. Residues whose class meets no uncovered point give the same state as skipping, so they are merged into the skip branch.

## Agreement between implementations

`check_p2.py` and `dfs2.c` process items in the same order with the same tree symmetry. On roots that coincide with orbit representatives they report identical node counts: root 0 = orbit 0, 22,270 nodes; root 6 = orbit 3, 68,004 nodes; root 45 = orbit 6, 25,752 nodes. With the first ten vectors, root 21 (= orbit 3) gives 200,024 nodes and 1,560 survivors in both implementations. The Python code shares no source with the C code: it indexes residues mod 45 directly and computes covers with its own routine.

## The first price vector is inert

For ρ = (1,1,1,1,1,1), φ ≤ 1 per column, so Q_2 ≤ 4 < R = 6 and this vector never closes a branch. It stays in `prices.txt` because every run used that file. `dfs2.c` with the other ten vectors gives the same 498,464 nodes and 0 survivors.

## Calibration (`calib.py`)

Starting from an empty price family, the generic tool alternates exhaustive search and the linear program. `calib.py` uses `scipy.optimize.linprog` only to propose prices; every price vector it returns is checked with exact integer covers.

| (odd part, min modulus) | Known answer | Method |
|---|---|---|
| (9, 4) | no covering (Krukenberg; Dalton-Trifonov Thm 2(v)) | NO SURVIVORS with 2 vectors |
| (15, 5) | no covering (HKLT Lemma 5.1) | NO SURVIVORS with 2 vectors |
| (9, 3) | covering with L = 2^4 3^2 | ALIVE state found (method silent) |
| (27, 4) | covering with L = 2^7 3^3 | ALIVE state found (method silent) |

## Fail-closed build

`run_checks.py` enforces successful process exits, exact final totals, survivor-file sizes and the ordering of the eleven prices across implementations. It rejects three synthetic incomplete or wrong completion records. Both covering controls are required to pass. The long Python logs are retained originals; the default build does not rerun that search. See `../readiness.md`.
