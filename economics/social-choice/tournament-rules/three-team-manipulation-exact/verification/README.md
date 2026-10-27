# Verification

Everything needed to check the theorem is in this directory. The checker uses only the Python 3 standard library.

## Certificates

`certificates/rule_n<n>_k<k>.json` is one neutral tournament rule:

```json
{"n": 5, "k": 3, "mode": "le", "alpha": "2/5",
 "classes": [{"T": "0011001000", "r": ["1/5", "1/5", "1/5", "1/5", "1/5"]}, ...]}
```

- `T` lists the results of the matches `(0,1), (0,2), ..., (n-2,n-1)` in lexicographic order; `1` means the lower-numbered team wins.
- `r[i]` is the exact winning probability of team `i` in `T`.
- `mode: "le"` means coalitions of every size from 2 to `k` (the standard definition of `k`-SNM).

| File | n | k | alpha | properties | rounding D | largest denominator |
|---|---|---|---|---|---|---|
| `rule_n3_k3.json` | 3 | 3 | 1/3 | CC | by hand | 3 |
| `rule_n4_k3.json` | 4 | 3 | 1/3 | CC | 3 | 3 |
| `rule_n5_k3.json` | 5 | 3 | 2/5 | CC | 1000 | 1001 |
| `rule_n6_k3.json` | 6 | 3 | 2/5 | CC | 1000 | 1002 |
| `rule_n7_k3.json` | 7 | 3 | 2/5 | CC | 1000 | 1002 |
| `rule_n8_k3.json` | 8 | 3 | 2/5 | CC | 10^6 | 1000003 |
| `rule_n7_k4.json` | 7 | 4 | 3/7 | CC | 70 | 72 |
| `rule_n3_k3_mt.json` | 3 | 3 | 1/3 | CC, monotone, top-cycle consistent | by hand | 3 |
| `rule_n4_k3_mt.json` | 4 | 3 | 1/3 | CC, monotone, TCC | 300 | 3 |
| `rule_n5_k3_mt.json` | 5 | 3 | 2/5 | CC, monotone, TCC | 1000 | 1002 |
| `rule_n5_k3_mt_small.json` | 5 | 3 | 2/5 | CC, monotone, TCC (Table 2 of the paper) | 20 | 21 |
| `rule_n6_k3_mt.json` | 6 | 3 | 2/5 | CC, monotone, TCC | 1000 | 1002 |
| `rule_n7_k3_mt.json` | 7 | 3 | 2/5 | CC, monotone, TCC | 1000 | 1002 |
| `rule_n8_k3_mt.json` | 8 | 3 | 2/5 | CC, monotone, TCC | 10^6 | 1000003 |

Certificates with `"monotone": true` and `"top_cycle": true` ask the checker to verify those properties as well.

## Checker

```sh
python3 -B -O verify_rule.py certificates/rule_n7_k3.json results/rule_n7_k3.result.json
```

`verify_rule.py` does not import anything from the discovery code. It:

1. computes its own canonical form of every listed tournament (colour refinement by out- and in-neighbour colours, then exhaustive search inside colour classes) and checks that the list has exactly one tournament from each of the A000568(n) isomorphism classes (2, 4, 12, 56, 456, 6880 for n = 3..8);
2. checks that every vector is a probability vector, is constant on the automorphism orbits of its tournament (all canonical labellings must give the same values), and gives probability 1 to a Condorcet winner;
3. for every listed `T`, every coalition `S` with `2 <= |S| <= k` and every re-orientation `T'` of the matches inside `S`, finds the representative of `T'`, transports its vector along the isomorphism, and checks `r_S(T') - r_S(T) <= alpha` in exact rational arithmetic;
4. if the certificate says so, checks monotonicity (for every representative and every match a team lost, reversing it does not lower that team's probability) and top-cycle consistency (zero probability outside the set of teams that reach every team by beat-paths);
5. reports the largest gain and every manipulation whose gain equals `alpha` (the "tight" set).

`--shard=i/m` restricts step 3 to every m-th class (the other steps always run in full); `combine_shards.py out.json shard0.json ... ` checks that all m shards are present and merges them. `build.sh` uses this with `JOBS=m`.

`verify_labelled.py` is a second, independent checker for n <= 6. It uses no canonical forms and no neutrality argument: it expands the certificate to all 2^(n(n-1)/2) labelled tournaments by trying every permutation, rejects the certificate if two isomorphisms disagree, and checks lotteries, Condorcet consistency and every coalition on every labelled tournament. It also checks monotonicity and top-cycle consistency when those flags are present.

It exits with status 1 and prints `FAIL: ...` on the first failed check. Neutrality is what makes one representative per class enough: the rule on labelled tournaments is defined by relabelling, step 2 makes that well defined, and the set of constraints is invariant under relabelling.

`negative_tests.py <certificate>` corrupts a certificate in seven ways (lower alpha by 10^-6, delete a class, duplicate a class, move probability inside a class, give a Condorcet winner 1/2, give two teams in one automorphism orbit different probabilities, scale a vector by 9/10) and confirms that each corrupted file is rejected.

## Results

`results/*.result.json` hold the replayed outcomes (counts, largest gain, tight set). Summary:

| certificate | manipulations checked | largest gain | tight manipulations | tight classes (score vector) |
|---|---|---|---|---|
| n3_k3, n3_k3_mt | 20 | 1/3 | 3 | 3-cycle |
| n4_k3, n4_k3_mt | 136 | 1/3 | 22 | (2,2,2,0), (2,2,1,1) |
| n5_k3 | 960 | 2/5 | 10 | (2,2,2,2,2) |
| n5_k3_mt | 960 | 2/5 | 12 | (2,2,2,2,2), (3,3,2,2,0) |
| n5_k3_mt_small | 960 | 2/5 | 17 | (2,2,2,2,2), (3,2,2,2,1), (3,3,2,2,0) |
| n6_k3, n6_k3_mt | 8,680 | 2/5 | 10 | (3,3,3,3,3,0) |
| n7_k3, n7_k3_mt | 121,296 | 2/5 | 10 | (4,4,4,4,4,1,0) |
| n8_k3 | 2,889,600 | 2/5 | 20 | (5,5,5,5,5,1,1,1), (5,5,5,5,5,2,1,0) |
| n8_k3_mt | 2,889,600 | 2/5 | 20 | (5,5,5,5,5,1,1,1), (5,5,5,5,5,2,1,0) |
| n7_k4 | 1,126,776 | 3/7 | 168 | the three regular 7-team tournaments |

For the plain CC certificates with n = 5..8 and k = 3 the tight set is exactly the lower-bound configuration of Schneider, Schvartzman and Weinberg: the regular 5-team tournament plus losers, with the five coalitions "a team and the two teams that beat it", each with two orientations of the match between the two helpers (5 x 2 = 10 per class).

Running times of `verify_rule.py` on the shared, heavily loaded development laptop (load average above 70): under 5 s for n <= 6, about 90 s wall (11 s CPU) for n = 7 (k = 3), 24 min wall (100 s CPU) for n = 7 (k = 4) and 41 min wall (242 s CPU) for n = 8. `verify_labelled.py` takes about 35 s CPU for n = 6.

## Discovery code (not needed for checking)

`discovery/` holds the code that found the rules. It needs nauty's `gentourng`, a C compiler and Python with numpy, scipy, highspy and python-flint.

```sh
cc -O2 -o gen_snm discovery/gen_snm.c
gentourng -q 8 | ./gen_snm 8 3 le lp_n8_k3_le        # symmetry-reduced LP: .vars, .ub, .meta
python3 discovery/facial.py lp_n8_k3_le 2 5            # interior-point solve at alpha = 2/5, no crossover
python3 discovery/exactify.py lp_n8_k3_le 2 5 1000000  # round, exact correction, exact check of all LP rows
PKL=lp_n8_k3_le_frrule.pkl python3 discovery/export_rule.py lp_n8_k3_le 8 3 le rule_n8_k3.json
python3 discovery/tight_rows.py lp_n8_k3_le 0.4 8      # list near-tight rows at the interior point
```

`gen_snm.c` writes one row per (representative, coalition, re-orientation), drops rows that are identically zero and is followed by duplicate removal, giving 2,667,216 distinct rows for n = 8, k = 3. `exactify.py` checks every one of these rows exactly before the rule is exported, which is a second check independent of `verify_rule.py`. The rounding parameters D are listed in the certificate table above. `solve_lp.py` solves the minimisation LP with `alpha` free; for n <= 7 its optimum agreed with the lower bound in every case (for n = 8 we solved only the feasibility problem at `alpha = 2/5`, which is all the theorem needs).

## Final recovery and stronger certificate

The saved n = 8 monotone/TCC exactification completed successfully; its original logs are preserved in `recovery/`. The independently replayed certificate has 6,880 classes, 2,889,600 manipulation checks, 192,640 monotonicity checks, maximum gain exactly 2/5, and 20 tight manipulations in the same two lower-bound classes as the CC certificate.

To regenerate the monotone/TCC rule, add `mono` to the generator command, use `facial.py <prefix> 2 5 mono tcc`, then `exactify.py <prefix> 2 5 1000000 1e-9 1e-9 mono tcc`. Export with `FLAGS=monotone,top_cycle PKL=<prefix>_mono_tcc_frrule.pkl`. Discovery requires numpy/scipy/highspy/python-flint; replay does not. Solver output can vary between versions; the committed certificates are the stable proof objects. The solve and exactification exit nonzero on failure.

The build checks every worker's exit status and uses a fresh directory for each set of shards. `check_results.py` then requires the exact certificate SHA-256, the expected complete manipulation count, le mode, exact optimum, and both extra properties for each MT certificate. No stale shard or changed certificate can supply a successful build.
