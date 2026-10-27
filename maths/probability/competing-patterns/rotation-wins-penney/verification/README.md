# Exact verification

The written paper proves the probabilistic identities, cancellation recurrence, clump tail, half-binomial bound and the infinite range `k >= 8`. The files here verify the finite integer counts and exact arithmetic. They do not encode the full proof in a formal theorem prover.

## Commands

`../build.sh` reconstructs all counts with C++, checks the saved certificate, runs controls, and builds the PDF. Run it from the finding directory as `./build.sh`.

```sh
python3 verification/verify.py
nice -n 10 python3 verification/replay_python.py
nice -n 10 python3 verification/controls.py
nice -n 10 python3 verification/check_length_three.py
```

The first checks saved counts, coverage, rational minima and the uniform arithmetic. The second reconstructs every coefficient independently in standard-library Python. The third directly enumerates all permutations through length nine for `2341` versus `1234` and tests the pointwise recurrence on all start subsets through span 13 for lengths 3 through 8. The fourth reconstructs the length-three finite-horizon certificate by two independent integer recurrences. These finite controls support implementation and sign conventions; the recurrence and tail are proved for all spans in the paper.

## Certificate format

`certificates.json` has schema version 1 and one list for each of `k=4,5,6,7`. Each row contains:

- `pattern`: the first player's permutation, using ranks `1,...,k`.
- `cutoff`: the maximum difference between first and last marked start positions.
- `coefficients`: two integer arrays. Entry `s` is the signed count of all clusters rooted at start 0 and ending at start `s`, with final type respectively the given pattern or its right rotation. A cluster with `m` marked occurrences contributes sign `(-1)^m`, multiplied by its number of compatible total orders.

Only the lexicographically smaller of a permutation and its value-complement is stored. Complementation commutes with rotation and preserves all probabilities. The checker constructs the complete expected representative sets rather than trusting the recorded counts of representatives.

If the arrays are `cA,cB`, the exact partial difference is

\[
D_S=\sum_{s=0}^{S}\frac{cA_s-cB_s}{(k+s)!}.
\]

Put `r=2(k-1)/k!` and `q=floor((S-k+1)/(2k-2))`. The complete omitted tail has absolute value at most

\[
T(k,S)=\frac4{k!}\frac{r^{q+1}}{1-r}.
\]

Every row passes `D_S > T(k,S)` using rational arithmetic. The checker also verifies the simpler lower bounds printed in the paper and the exact minima recorded in `results.json`.

## Two reconstructions

`enumerate_python.py` stores transitive predecessor masks. It adds order relations incrementally and counts extensions recursively by choosing a currently minimal element.

`enumerate_independent.cpp` stores successor masks, adds all comparisons of each occurrence, computes full transitive closure, and counts extensions recursively by deleting a currently maximal element. It independently tests overlap compatibility using pairwise comparisons. Its output is newline-delimited JSON with the same rows, one file per length. The build passes those files to `verify.py --generated <directory>` for coefficient-by-coefficient comparison.

Both enumerate every connected sequence of marked occurrence starts and types, reject cyclic orders, and add signed multiplicities when resulting orders coincide. They use different relation orientation, closure procedures, overlap tests and extension recursions.

The largest order has 19 elements, so each extension count is at most `19!`, which fits in unsigned 64-bit integers. The C++ signed accumulated counts use 128-bit integers. At span `s >= 1` there are at most `4*3^(s-1)` possible marked paths: two endpoint labels each, and absent/a/b at every internal start. Since every cutoff is at most 15, the absolute accumulation is bounded by `4*3^14*19! = 2327298977029323128832000 < 2^81`, well below the signed 128-bit range. Python uses unbounded integers. The certificate inequalities use `fractions.Fraction`; floating point is not used.

## Length-three horizon certificate

`length-three.json` stores exact counts at horizon 18 for the three complement representatives `123`, `132`, `213`. Its fields `winsA`, `winsB`, `unresolved` partition all `18!` permutations according to whether the first player's pattern wins by the horizon, the rotation wins, or neither has occurred. Even if every unresolved case eventually favors the first player, that player's probability is at most `(winsA + unresolved)/18!`, which is below `47/100` in every case.

`check_length_three.py` reconstructs these counts twice. One recurrence appends each possible new global rank to a permutation prefix that still avoids both patterns, retaining the global ranks of its last two positions. The second deletes the first position from permutations whose first hit is at their final window, retaining their first two global ranks and classifying the newly exposed first triple. It aggregates each length-n first-hit count using exactly `18!/n!` extensions. The two methods agree at every length, not only on the final totals. These are ranks among all observations seen, not just ranks inside the latest window.

This supplies an additional exact verification of the known length-three case. No discovery claim is attached to that case.

## Archived independent output

`independent/k4.jsonl` through `independent/k7.jsonl` are the actual C++ reconstruction outputs from a completed build. Their SHA-256 digests are in `independent/sha256.json`. Compare them with the certificate using:

```sh
python3 verification/verify.py --generated verification/independent
```

This compares archived output. The build performs a fresh C++ reconstruction instead.

`length_three_oracle.cpp` directly enumerates every permutation at horizons 8, 9 and 10 for all six ordered length-three races, without using a rank-state recurrence. `compare_length_three_oracle.py` compares its winner, unresolved and first-hit-time counts with both recurrences. The build runs this oracle, and its actual output is archived as `independent/length-three-oracle.jsonl`. The saved execution transcript is `execution-log.txt`.

## Checked environment

The recorded campaign runs used Python 3.13, Apple Clang with C++17, and pdfTeX/BibTeX. No new packages were installed. Every heavy reconstruction used `nice -n 10`, with at most two simultaneous workers. The build script itself runs sequentially and writes intermediate files to its printed temporary directory.
