# Verification

All claims reduce to two kinds of check.

1. **Explicit algorithms (upper bounds).** A list of terms (a_t, b_t, c_t) is a bilinear algorithm for A = F_q[x]/(f) iff for every pair of monomials x^i, x^j the identity x^i x^j = sum_t a_t[i] b_t[j] (sum_k c_t[k] x^k) holds in A. This is 16 (or 36 for C_6) polynomial identities over F_q.
2. **Exhaustive search (lower bounds).** Rank <= n + m iff some (n+m)-dimensional space W of n x n bilinear forms containing the n slices S of the tensor is spanned by rank-one forms (paper, Lemmas 2.1-2.3). Writing W = S + <F_1, ..., F_m>, F_1 is fixed to one of three orbit representatives under the unit group and transposition, F_2 < ... < F_{m-1} range over all rank-one forms, and F_m is handled by bucketing all rank-one forms by the projective class of their image modulo the prefix span.

## Files

| File | Role |
|---|---|
| `verify.py` | Standard-library replay of everything below the C layer: checks every algorithm in `certificates/`, 96 corrupted variants of the F_3 certificate (all rejected), the exhaustive proof R_{F_2}(A_2) > 8 and two controls. `--full` adds the exhaustive proof R_{F_3}(F_3[x]/((x^2+1)^2)) > 7. No assertions; non-zero exit on failure; writes `results.json`. |
| `certificates/upper_bounds.json` | 9-term algorithm for F_2[x]/((x^2+x+1)^2); 3-term for F_2[x]/((x+1)^2); 12-term for F_2[x]/(x^6+1) (CRT lift); 8-term for F_5[x]/((x^2+2)^2). |
| `certificates/q3_rank8.json` | The symmetric 8-term algorithm for F_3[x]/((x^2+1)^2) (paper, Table 1). `q3_W.txt` lists the 8 rank-one forms spanning the subspace W found by the search. |
| `construct.py` | Generates `upper_bounds.json` from the constructions in the paper (p-adic Karatsuba, CRT lift, interpolation over F_5). |
| `extract.py` | Turns a subspace W found by the search into an explicit algorithm (`q3_W.txt` -> `q3_rank8.json`). |
| `subsp.c` | C, F_2 only, no symmetry: enumerates every set {F_1, ..., F_4} of rank-one forms with independent images (103,406,616 sets for A_2). |
| `bucket.c` | C, prime fields, the bucket search with orbit reduction (m = 4). |
| `rankfq.c` | C, field tables (q = 2, 3, 4, 5, 7), the bucket search for m = 1..4. |
| `check_local_rank7.cpp` | Separate prime-field checker in the basis 1,t,u,tu, with t²=-d and u²=0; sorts full-matrix residuals and computes modular row ranks. Checks q=3,5. `--split` replaces u²=0 by u²=u and must find a rank-at-most-seven space. |
| `check_q2.py`, `rankq.py` | Earlier standalone Python versions (F_2 bit-vector version; generic prime-field version) used during discovery; same results. |
| `satenc.py` | DIMACS encoder for "rank <= r over F_2". The rank-eight formula is UNSAT and its DRAT proof passed `drat-trim`; see `sat-replay.md`, the hash manifest and the retained checker log. The large proof itself is archived outside this package. |
| `run_searches.sh`, `run_searches.py` | Compile and replay C/C++ searches. Require the expected result and enumeration counts, preserve timestamped logs, emit 20-second heartbeats and exit nonzero on failure. No new successful manifest is written after a failed case. |
| `logs/` | Recorded outputs of the C runs (see table). |

## Recorded results

| Program | Algebra | Question | Result |
|---|---|---|---|
| subsp.c | F_2[x]/(x^4+x^2+1) | rank <= 8 | NO (103,406,616 independent 4-sets) |
| bucket.c | F_2[x]/(x^4+x^2+1) | rank <= 8 | NO (74,377 prefixes) |
| rankfq.c | F_2[x]/(x^4+x^2+1) | rank <= 8 | NO (74,377 prefixes) |
| check_q2.py | F_2[x]/(x^4+x^2+1) | rank <= 8 | NO (74,377 prefixes) |
| verify.py | F_2[x]/(x^4+x^2+1) | rank <= 8 | NO (74,377 prefixes) |
| subsp.c / bucket.c / rankfq.c / verify.py | F_16 = F_2[x]/(x^4+x+1) (control) | rank <= 8 | NO (known rank 9) |
| subsp.c / bucket.c / rankfq.c / verify.py | F_2[x]/(x^4) and F_2[x]/(x^4+1) (controls) | rank <= 8 | YES (known rank 8) |
| rankfq.c, rankq.py, verify.py --full | F_3[x]/((x^2+1)^2) | rank <= 7 | NO (4,794 prefixes) |
| bucket.c, rankfq.c | F_3[x]/((x^2+1)^2) | rank <= 8 | YES (certificate) |
| rankfq.c | F_4[x]/((x^2+x+w)^2), w^2 = w+1 | rank <= 7 | NO (21,668 prefixes) |
| rankfq.c, check_local_rank7.cpp | F_5[x]/((x^2+2)^2) | rank <= 7 | NO (73,000 prefixes, 17,417,506 candidate buckets in each program) |
| check_local_rank7.cpp | F_3[x]/((x^2+1)^2) | rank <= 7 | NO (4,794 prefixes, 205,980 candidate buckets) |
| check_local_rank7.cpp --split | F_(q²) × F_(q²), q=3,5 (controls) | rank <= 7 | YES in both cases |

## Commands

```sh
python3 -B -O verify.py          # minutes; standard library only
python3 -B -O verify.py --full   # adds the q = 3 lower bound
sh run_searches.sh               # needs C and C++17 compilers
```

The independent prime-field checker uses coordinate functionals on 1,t,u,tu. In the local algebra, multiplication by units has two orbits on projective functionals: those vanishing on the ideal (u), and those not vanishing there. This follows from the Frobenius duality argument in the paper. Representatives extracting the coefficients of 1 and u therefore give the three unordered pairs of functional types. Unlike `rankfq.c`, this checker does not recompute unit orbits or quotient coordinates; it reduces full 16-entry matrices and sorts their normalized residuals. The two implementations share the mathematical completeness argument, not their coordinate construction or field-arithmetic code.

The split controls only test for a positive witness and do not assert exhaustive orbit coverage for the split algebra. Every reported positive space is explicitly tested for rank seven, and its rank-one forms lie over the slice span by construction.
