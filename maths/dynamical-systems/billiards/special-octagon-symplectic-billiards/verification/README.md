# Verification

All programs use Python 3 with the standard library only and exact rational arithmetic (`fractions.Fraction`). Run them from this directory. The theorem rests on the written proof in `../paper.tex`; these programs test the half-lattice lemma, its implementation and the side claims.

| File | What it checks | Command | Time |
| --- | --- | --- | --- |
| `symplectic_billiard.py` | Library: exact symplectic billiard map, critical set C (exploration of states "even point, open interval of odd points"), generic periods, the polygon families | imported | - |
| `check_octagons.py` | For every admissible O(W,H,c1,c2) with parameters <= N: C is finite and C is contained in S. Writes `octagon_results.json` | `python3 -B check_octagons.py 14` | ~50 min |
| `independent_octagon_check.py` | Second implementation, written from the explicit side equations, sharing no code with the library. Checks clauses (a) and (b) of Lemma 3.2 at every explored state | `python3 -B independent_octagon_check.py 14` | ~50 min |
| `compare_implementations.py` | The two implementations give identical critical sets (as point sets) and identical state counts for every admissible octagon with parameters <= N. Output `compare_result.txt` | `python3 -B compare_implementations.py 10` | ~15 min |
| `check_S_count.py` | abs(S) = 4W + 2H - 2(c1 + c2) for all parameters <= 12 | `python3 -B check_S_count.py` | seconds |
| `filled_set.py` | The set generated from the vertices by chords in all four directions (hypothesis of ALW Theorem 3.1) consists of the 8 vertices for O(3,3,1,1) and O(4,4,1,1); for O(5,6,1,2), O(6,5,2,1), O(7,9,3,2) the exploration has not closed after 20000 points, with denominators up to 2^14 or 2^17. This does not prove the set infinite. Output `filled_set_results.txt` | `python3 -B filled_set.py` | ~1 min |
| `asymmetric_octagon_check.py` | Proposition 3.6: the 6-periodic trajectory in the asymmetric octagon Q, return multipliers -2 and -1/2, exact perturbation test. Output `asymmetric_octagon_result.txt` | `python3 -B asymmetric_octagon_check.py` | instant |
| `asymmetric_cap_check.py` | Exploratory: C exploration for three asymmetric lattice octagons (does not close within 40000 states) and one centrally symmetric octagon (finite C). Output `asymmetric_cap_result.txt` | `python3 -B asymmetric_cap_check.py` | minutes |
| `check_symmetric_hexhouses.py` | Corollary 3.4 on instances: every Hexhouse X(s,h,p,s-p) with parameters <= N has finite C, and its image under (x,y) -> (hx,py) lies in the half-lattice set S of O(hs, p(s+h), hp, 0). Output `symmetric_hexhouse_result.txt` | `python3 -B check_symmetric_hexhouses.py 11` | minutes |
| `check_other_families.py` | Instance checks of ABS Conjectures 6.1 (Hexhouses, integer parameters <= 11 up to scaling and mirror image) and 4.1 (60 rational Penthouses: finite C and generic periods 16m-4, 16m+4, 16m+12). Writes `other_families_results.json` | `python3 -B check_other_families.py 11` | ~1.8 h |

`sh ../build.sh` runs a quick replay (octagon parameters <= 8) and builds the paper; `sh ../build.sh --full` runs the full replay. Each check's output goes to a log under `$TMPDIR`; the build stops if any check exits nonzero or prints a FAIL line (the checkers exit nonzero on failure).

## Recorded results

- `octagon_results.json`: N = 14, 1484 octagons, `all_finite_and_in_S: true`, largest critical set 58 points; generic periods of O(5,6,1,2) are 4, 16, 32, 44, 68, 92. The per-octagon field `period_bound` records the sharper single-table bound 2(abs(C)^2 - abs(C)) of Albers-Lander-Westermann; the paper's self-contained Theorem 2.4 proves 4(abs(C)^2 - abs(C)).
- `independent_octagon_check.py 14`: PASS for all 1484 octagons (clauses (a) and (b) and finiteness). `compare_result.txt`: the two implementations give identical C and state counts for all 340 octagons with parameters <= 10.
- `asymmetric_octagon_result.txt`: PASS.
- `symmetric_hexhouse_result.txt`: PASS for all 252 symmetric Hexhouses with parameters <= 11 (largest critical set 123 points).
- `other_families_results.json`: 1007 Hexhouses (parameters <= 11, up to scaling and mirror image), all with finite C (largest 205); 60 Penthouses, all with finite C and generic periods exactly 16m-4, 16m+4, 16m+12.

## What the exploration means

A state is an even point p together with an open interval J of odd points on one side. For each state the program maps p by the parallel projection along J's side and splits J at the finitely many odd parameters that are sent to a vertex. If the set of states is finite the exploration closes and C, the set of even points that occur, is finite and computed exactly. If C were infinite the exploration would not close; the programs report a cap in that case.
