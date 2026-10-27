# Verification

Everything claimed as proved in the paper rests on strategy certificates replayed by the checkers in `py/`. The checkers use only the Python standard library and share no code with the search programs in `src/`.

## Commands

From the package directory:

```sh
sh build.sh             # quick: shipped 5x5 certificates + mutation tests + PDF
sh build.sh full        # also regenerates and replays the 6x6 and strict certificates, and the full 5x5 tables
```

or directly from this directory:

```sh
bash run_checks.sh          # 100 shipped 5x5 certificates, about 4 minutes
python3 negative_checks.py  # 10 corrupted certificates must be rejected
bash run_checks.sh full     # + regenerate and replay Hex_9(6), Hex_10(6), Hex(6,7), strict Hex*(5,6)
bash table5.sh              # certify every entry of the 5x5 opening tables (Figure 1)
```

Run times are for a loaded 14-core laptop, one process per check. `full` takes several hours, dominated by the Python replay of the 6x6 certificates.

## What each certificate proves

| Statement | Certificate(s) | Checker output |
|---|---|---|
| Red holds $\mathrm{Hex}(5,5)$ after every opening, so $\lambda(5)\ge6$ | `certs/n5L5_{0..24}_red.txt.gz` | 25 x VERIFIED, 52,666 positions |
| Blue wins $\mathrm{Hex}(5,6)$ from the centre, so $\lambda(5)\le6$ | `certs/n5L6_12.txt.gz` | 106,826 positions, at most 12 Blue stones |
| Blue's first connection contains a path of at most 6 cells (strict game), so $\lambda^*(5)\le6$ | regenerated: `gen/strict5_6_12.txt` | 875,938 keys, at most 13 Blue stones |
| Red holds $\mathrm{Hex}_6(5)$ after every opening, so $\delta(5)\ge7$ | `certs/n5D6_{0..24}_red.txt.gz` | 25 x VERIFIED, 4,060 positions |
| Blue wins $\mathrm{Hex}_7(5)$ from $(3,3)$, $(2,4)$, $(4,2)$, so $\delta(5)\le7$ | `certs/n5D7_{8,12,16}.txt.gz` | 12,651 positions for the centre |
| Red holds $\mathrm{Hex}_9(6)$ after every opening, so $\delta(6)\ge10$ | regenerated: `gen/n6D9_{0..35}_red.txt` | 36 x VERIFIED, 1,472,836 positions |
| Blue wins $\mathrm{Hex}_{10}(6)$ from $(3,4)$, so $\delta(6)\le10$ | regenerated: `gen/n6D10_15.txt` (5,222,871 lines, 122 MB) | 5,158,730 positions, at most 10 Blue stones |
| Red holds $\mathrm{Hex}(6,7)$ after every opening, so $\lambda(6)\ge8$ | regenerated: `gen/n6L7_{0..35}_red.txt` | 36 x VERIFIED, 22,780,097 positions |
| Every entry of the 5x5 tables | `table5.sh` (Blue certificate at the value, Red certificate one below; Red certificate for $\mathrm{Hex}_{13}(5)$, i.e. ordinary Hex, for losing openings) | 64/64 expected certificate replays (13 winning and 12 losing openings) |

Recorded outputs are in `logs/` (`quick_checks.log`, `table5.log`, `negative_checks.log`, and the 6x6 and strict replays copied from the original runs). `results.json` lists the claims, certificate hashes and checked counts.

The statement $\lambda(6)\le8$ (Blue wins $\mathrm{Hex}(6,8)$ from $(3,4)$) is a search result only: `src/hexmb3.c` found it (2.9e9 positions); no certificate has been replayed.

## Rules implemented by the checkers

Board: cell $(r,c)$, $1\le r,c\le n$, index $(r-1)n+(c-1)$ in the files. Neighbours of $(r,c)$: $(r,c\pm1)$, $(r-1,c)$, $(r-1,c+1)$, $(r+1,c-1)$, $(r+1,c)$. Blue moves first and joins row 1 to row $n$. The short diagonal is $r+c=n+1$.

- `check_cert.py`, mode `L` (Campbell's $\mathrm{Hex}(n,l)$): Blue wins as soon as its stones contain a top-bottom path of at most $l$ cells (BFS on the actual Blue stones); play continues after a longer connection; there is no move limit.
- `check_cert.py`, mode `D` (Campbell's $\mathrm{Hex}_d(n)$): Blue wins if its stones contain a top-bottom connection while it has placed at most $d$ stones.
- `check_strict.py` (strict game $\mathrm{Hex}^*(n,l)$): ordinary Hex, which ends at the first connection of either player; Blue succeeds only if it connects first and that connection contains a path of at most $l$ cells.

At every position reached, the checker reads the certified move, checks that it is legal (and, for mode L/D Blue certificates, that it lies on a live winning set, which only restricts Blue), and then tries **every** empty cell as the opponent's reply. Winning sets are recomputed from scratch by enumerating all simple top-bottom paths of at most $l$ cells and keeping the inclusion-minimal cell sets.

## Certificate format

Header `# n=<n> mode=<L|D> bound=<l or d> first=<index> [side=red]`, then one line per position: `m blue_rel rel move`, where `rel` (hex) is the union $R$ of the live winning sets, `blue_rel` (hex) the Blue cells in $R$, `m` the number of Blue stones left (ignored in mode L), and `move` the certified cell index. Strict certificates: header `# strict n=.. bound=.. first=..`, lines `blue re kp move` keyed by all Blue stones, the empty cells of $R$, and the number of other empty cells. The paper (Section 3) explains why these keys determine the rest of the game.

## Sources

- `src/hexmb4.c`: Maker-Breaker search with dead-cell normalisation, forced moves, double-threat pruning and Breaker domination; writes certificates when `CERT=<prefix>` is set. `src/hexmb3.c` is the earlier version used for the $\lambda(6)$ runs (same search, no certificate-size option).
- `src/hexstrict2.c`: strict-game search; writes strict certificates with `CERT=<prefix>`.
- `src/hexmb.c`, `src/hexmb2.c`: walk-based searches used as cross-checks (centre win in $\mathrm{Hex}(5,6)$; Red holds $\mathrm{Hex}_9(6)$ for all openings).
- `py/indep_solve.py`: slow plain minimax solver for small cases.
- `py/longest_line.py`: prints a game against a Blue certificate in which Red maximises Blue's stones (Figure 2 of the paper).
- `py/make_figures.py`, `py/tikz_board.py`: TikZ figures.

Compile with `cc -O3 -o build/hexmb4 src/hexmb4.c` (Apple clang 17 used). Example: `CERT=gen/n6D10 build/hexmb4 6 D 10 15` writes `gen/n6D10_15.txt` in about a minute.

## Mutation tests

`negative_checks.py` relabels certificates with a smaller bound or a different opening, deletes entries, replaces moves with occupied or off-board cells, and tries an empty certificate on a 1x1 board; the checker must reject all ten (`logs/negative_checks.log`).

## Finishing checks

`python3 verification/strict_controls.py` replays the small strict4 certificate and rejects six mutations. `python3 verification/check_records.py` checks completeness of the retained large-run and table records and hashes of the 100 shipped main certificates. These are included in `build.sh`. Retained original large replays are not a fresh full replay. See `readiness.md` and `review.md`.
