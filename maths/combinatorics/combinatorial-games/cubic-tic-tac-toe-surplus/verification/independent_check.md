# Independent reconstruction of the 7x7x7 certificate

The separate reconstruction in `independent/` generates the 343 cells and 193
winning lines directly, then computes surplus using a line-capacitated augmenting
path algorithm. It does not import the package's slot-matching implementation.
The numerical runs completed on 26 October 2026. The review session ended before
its narrative report was written; this record is based on the recovered source
and complete output files, inspected during campaign integration.

## Completed results

- `claim1_2.out`: all 1,296 central configurations. The histogram is
  `(lines met, surplus, count) = (27, >=4, 576), (26, >=4, 288),
  (25, 2, 384), (22, no matching, 48)`. Surplus is capped at 4.
- The same run enumerates all 10,627 diagonal-relevant leaves of the greedy
  opening, giving 14 distinct final Breaker sets. Each meets 27 lines and has
  surplus at least 4 with only Maker's centre move removed.
- `claim3_raw0.out` and `claim3_raw1.out`: the two disjoint parity shards each
  contain 24,480 of the 48,960 legal non-central configurations. Every surplus
  is exactly 3, with zero failures. The cap is 4, so a returned 3 is exact.
- `claim3_classes.out`: an additional symmetry-reduced run agrees with the raw
  run, including the 1,158 classes and their total weight.
- `claim5.out`: 2,916 unordered pairs cannot simultaneously be moved into the
  stated half-cube. This is 5,832 ordered pairs. The specific pair
  `(1,7,1), (6,2,6)` fails the symmetry test.
- `crosscheck.out`: 24 selected inputs agree between the independent
  line-capacitated matcher and a further from-scratch slot matcher. These
  include controls outside the legal opening family;
  they are not an additional exhaustive enumeration.

The two raw-output SHA-256 hashes are
`ce0a631b7e2a15bbb441bff788414cec77a98b4bdaff4d3509955225279fdd26`
and `5490aed3908f4ec0bd92d070f68a03be9d76ad6bdbbda9e32cea9b21e7479ae8`.

## Why the surplus calculation is independent

Every alive line supplies two identical slots. A minimizing nonempty set of
slots can therefore be enlarged to include the other slot of every represented
line without increasing its neighborhood. It is enough to minimize
`|free cells in the selected lines| - 2 * |selected lines|` over nonempty sets
of lines. After saturating two units per line, the reconstruction augments
extra units from each line in turn. Taking the minimum number that can be
added computes this surplus, capped at 4. The matching and line construction
were inspected against this characterization.

## Replay

From `verification/independent/`, run without Python's `-O` option because the
original independent scripts use assertions for board sanity checks:

```sh
python3 -u claim1_2.py
python3 -u claim3.py classes
python3 -u claim3.py raw 0 2
python3 -u claim3.py raw 1 2
python3 -u claim5.py
```

The original scripts are preserved unchanged. Their final distributions must be
compared with the values above: the exploratory drivers print discrepancies and
do not themselves consistently turn them into a nonzero exit status. The main
package's production checkers and build do reject discrepancies.

These computations support the 7x7x7 proof. They neither settle 6x6x6 nor
establish novelty of the surplus method. The written game argument and the
scope of the Lean lemma remain separate from the finite computations.
