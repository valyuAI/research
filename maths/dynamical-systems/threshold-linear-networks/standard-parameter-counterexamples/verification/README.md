# Verification

The example certificates and stability decisions use exact integer or rational arithmetic. Floating point appears in `simulate.py` and `region.py`, which are illustrations, and in a prefilter of `fixedscan.c` that is rigorous under the IEEE arithmetic model documented below: it rejects a graph only when a residual-based error bound proves non-permission.

## Files

| file | role |
|---|---|
| `examples/G11.json` | the 11-vertex counterexample: arc list `edges` ([j, i] means j -> i) and `deleted_arcs` |
| `examples/G11_certificate.json` | (I+3N)^{-1}1, K^{-1}1, the fixed point at theta = 1, coefficients of det(zI+K), Hurwitz determinants |
| `examples/W4.json` | W_4 (23 vertices), rebuilt from the family W_k of github.com/hturcotte1/CLTN (Theorem Q2; arcs [i, j] mean i -> j) |
| `examples/G27.json`, `examples/G100.json` | our independent 27- and 100-vertex examples (G100 carries its 7-class quotient data) |
| `check_ctln.py` (+ `mm.py`) | standard-library checker. It checks legality, the nonclique property, the exact fixed point and its positivity, and the characteristic polynomial by 2-3 agreeing methods: multimodular Hessenberg with CRT under a Hadamard bound, Berkowitz, rational Hessenberg, and for G100 the class quotient. It then applies the Routh array and the Lienard-Chipart criterion, and checks K = I (mod 3) for nondegeneracy, plus brute-force nondegeneracy over all subsets for n <= 12 |
| `check_flint.py` | independent checker on FLINT (`python-flint`). It computes the exact solve, the exact characteristic polynomial and all n Hurwitz determinants; it shares no code with `check_ctln.py` |
| `fixedscan.c`, `recheck.py`, `scan.sh` | exhaustive scan at beta = t = 3. nauty enumerates digraphs, read as nonedge matrices. The C program does an exact int128 fraction-free solve for permission and exact Berkowitz coefficients, and emits every coefficient-positive candidate. `recheck.py` decides each candidate exactly with Routh and Lienard-Chipart over Q |
| `scan_results/` | recorded scan summaries for n = 2..7 and the positive control |
| `check_ctln_results.txt`, `check_flint_results.txt` | recorded outputs |
| `simulate.py`, `region.py` | floating-point dynamics and parameter-region illustrations |

## Commands

```sh
python3 -B check_ctln.py examples/G11.json examples/W4.json examples/G27.json examples/G100.json   # ~30 s
python3 -B check_flint.py examples/G11.json examples/W4.json examples/G27.json examples/G100.json   # needs python-flint
sh scan.sh 6                                     # n = 2..6 plus the positive control (~1-2 min)
sh scan.sh 7                                     # adds all 882,033,440 digraphs on 7 vertices (hours)
python3 simulate.py examples/G11.json 1500 0.3   # perturbation returns to the fixed point
```

## Exhaustive scan logic

A graph G has a stable fixed point with nonclique full support at (eps, delta) = (1/4, 1/2) iff N != 0, (I+3N)^{-1}1 > 0, and K = I + 3N + 3J is positive stable. The second condition is equivalent to K^{-1}1 > 0 by the rank-one identity. det(I+3N) = 1 (mod 3) is never zero. Positive stability requires all coefficients of det(zI+K) to be positive, and then is decided exactly by the Hurwitz criterion. Every graph is either rejected by an exact test (permission, or a nonpositive coefficient), rejected by the rigorous float prefilter, or written out and decided exactly by `recheck.py`. Relabelling preserves all conditions, and complementation is a bijection of digraphs, so enumerating digraphs up to isomorphism and reading each as N covers every case. The enumeration counts 3, 16, 218, 9,608, 1,540,944 and 882,033,440 match OEIS A000273.

## Final recovered seven-vertex run

The three complete shard totals are 139,411,110; 193,878,344; and 548,743,986, summing to 882,033,440. All original `.err` and candidate `.txt` files are retained byte-for-byte under `recovery/`, together with the original scanner source and its hash. The 35,842 distinct coefficient-positive candidates (3,979 + 18,713 + 13,150) were freshly rechecked: exact permission, exact Berkowitz coefficients, Routh and Lienard-Chipart all agree, with **zero stable candidates**. `scan_results/n7_recovered.recheck.json` binds the result to all three input hashes. `check_scan_results.py` fails on an incomplete shard, wrong count, changed input or wrong exact result.

The original n7 scan uses a residual-bound permission filter, not a floating eigenvalue test. For C=I+3N and n<=7, each row has Euclidean norm at most sqrt(1+9(n-1)), |det C|>=1, and Hadamard bounds the inverse infinity norm by n(1+9(n-1))^((n-1)/2). The filter's actual double constant is over 1.001 times this exact bound; `prefilter_constants.c` and `scan_results/prefilter_constants.json` check that inequality using exact squared rational comparisons. For IEEE binary64 unit roundoff 2^-53, the residual's at most 14 multiply/subtract operations have error below gamma_14(1+3n max|yhat|), with gamma_14 < 1.6e-15. The code allows 1e-13 times that magnitude, plus the inverse-bound margin, covering rounding of the residual, final product and comparison. Nonfinite intermediates cannot satisfy the rejection inequality. This explains why those rejections are rigorous under the documented IEEE arithmetic model; we do not treat an unchecked floating sign as proof.

For the 128-bit integer stages, fraction-free intermediate minors are bounded by Hadamard; even using the control's largest C-entry 21 and n=7, twice the squared minor bound is at most 2(7*21^2+1)^7 < 2^83. Berkowitz intermediate sums have the conservative bound n*2^n*(n*M)^n with M<=521, below 2^93 for n<=7. Both are below 2^127. Fresh scans additionally enable signed-overflow sanitization. The scan runner rejects unsupported parameters/orders instead of extending these bounds silently.

Fresh n=2..6 standard scans disable the prefilter entirely. Their totals are 3, 16, 218, 9,608 and 1,540,944. All coefficient-positive candidates (0, 0, 2, 15, 372) are exactly rejected. The six-vertex positive control checks all 1,540,944 digraphs and all 2,322 candidates, finding exactly two stable graphs. These rescans corroborate the filter on small orders, but do not constitute a fresh all-rational rerun of 882 million n7 graphs.

`check_induced.py` verifies 2,035 proper subsets of G11 of sizes 2..10: 90 cliques, 1,778 not permitted, 167 permitted but unstable, zero stable nonclique subsets. Cliques are deliberately excluded from the counterexample claim.

The runner checks each pipeline stage separately and checks counts, candidates and exact outcomes. It does not skip missing nauty/FLINT dependencies. The full-scan option regenerates n7; the default additionally replays the saved n7 candidates and validates their hashes.
