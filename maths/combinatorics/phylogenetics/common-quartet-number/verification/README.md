# Verification

All Python files run with Python 3.10 or later. Files marked (stdlib) use only the standard library.

## Lower bounds: explicit families

| File | Content |
|---|---|
| `families/triple13.nwk` | T, sigma T, sigma^2 T on 13 leaves (Proposition 3.1) |
| `families/triple12.nwk` | three trees on 12 leaves, not all of the same shape |
| `families/triple11.nwk` | three trees on 11 leaves, the first a caterpillar |
| `families/triple10.nwk` | three trees on 10 leaves |
| `families/quad22_k4.nwk` | four trees on 22 leaves (sigma of type 4^5 2): h(4) >= 23 |

- `check_family.py FILE...` (stdlib): parses Newick, checks that each tree is binary on leaves 1..n, computes every quartet split by the four-point condition and counts 4-sets resolved identically by all trees. Expected output: `common quartets: 0` for every file.
- `sym_triple.py` (stdlib): rebuilds sigma T and sigma^2 T from T and checks them.
- `sep_check.py FILE 3 4` (stdlib): brute force over all pairs of edges; for `triple13.nwk` it prints `None` for every pair, i.e. no two of the trees have separated sets of sizes 3 and 4. This shows Lemma 3.3 fails at 13 leaves, as the proof of Theorem 1.1 predicts.

## Upper bound for three trees: Lemma 3.4 (exhaustive) and Lemma 3.3 (SAT)

- `bipartition_check.py N U` (stdlib) checks Lemma 3.4: for every unrooted shape on N leaves (enumerated by leaf insertion, the same enumeration as `sat/indep/indep_cnf.py`, counts matching OEIS A000672) and every choice of U leaves as X, some edge splits the leaves into Z, W with (X n Z, Y n W) or (X n W, Y n Z) of sizes at least 3 and 4 in some order. `14 5`, `14 6`, `14 7`: 0 failures out of 135 x 2002, 135 x 3003, 135 x 3432 cases. Sharpness: `13 5` gives 891 failures, `13 6` gives 0. About a minute per run. With a balanced edge of the first tree (both sides at least 5 on 14 leaves) this proves h(3) <= 14 without SAT.

## Lemma 3.3 on 14 leaves (SAT, independent confirmation)

- `sat/twotree.py` (stdlib) writes, for a shape index s in 0..134, the CNF whose models are trees T2 such that the pair (representative of shape s, T2) has no separated sets of sizes 3 and 4. Shape representatives come from `sat/shapes.py` (rooted shapes on 13 leaves plus a leaf at the root, deduplicated by a centre-based canonical form; counts match OEIS A000672). Quartet variables and 5-point constraints come from `sat/qlib.py`.
- `results/twotree_n14_cadical_drat.json`: per shape, status (all 135 `UNSAT`), DRAT-trim result (all 135 `VERIFIED`), solve and check times, proof size, CNF variable and clause counts, and the SHA-256 of the CNF. `results/twotree_n14_cadical_drat.log` is the run log (25-26 October 2026, CaDiCaL 3.0.1 and DRAT-trim from github.com/marijnheule/drat-trim, on a heavily shared 14-core laptop).
- `sat/run_twotree_certificates.py --hash-only` regenerates all CNFs and compares hashes (about a minute per 10 shapes). Without `--hash-only` it also re-solves with CaDiCaL (path in `CADICAL`) and checks each DRAT proof with DRAT-trim (path in `DRAT_TRIM`); proofs total about 3.2 GB and are deleted after checking.
- Independent second implementation: `sat/indep/indep_twotree.py` (stdlib) shares no code with the files above. It derives the allowed 5-leaf patterns by generating all 15 labelled 5-leaf trees, enumerates shapes by leaf insertion, forbids the 228 non-tree patterns by direct clauses and writes its own separation clauses. `sat/indep/run_indep_twotree.py` solves all 135 with Kissat 4.0.4 (path in `KISSAT`). Results: `results/indep_twotree_n14_kissat.json` (all 135 `UNSAT`, with the SHA-256 of each CNF; regenerating a CNF with `python3 sat/indep/indep_twotree.py 14 3 4 OUT SHAPE` reproduces the hash). The run used two runners (ascending and descending shape order, logs `results/indep_twotree_n14_kissat_forward.log` and `_reverse.log`), merged once together they covered all shapes; the three shapes solved by both agree. Kissat was run without proof output, so this is an independent cross-check of the encoding, not a second certificate.
- Positive control: `python3 sat/twotree.py 13 3 4 50 pos.cnf` (shape 50 is the shape of T) is satisfiable; `sat/decode_twotree.py 13 3 4 50 MODEL` rebuilds the second tree and confirms by brute force that the pair has no separated (3,4) sets. With shape 0 (caterpillar) the 13-leaf formula is unsatisfiable. Recorded in `results/positive_control_n13.txt`.

Soundness of the reduction: relabelling leaves preserves separation, so the first tree may be a shape representative. Every tree satisfies the one-hot and 5-point constraints, so unsatisfiability excludes all second trees; by Lemma 3.2 of the paper, the separation clauses say exactly that no (3,4) pair is separated in the second tree.

## Lean

- `lean/CommonQuartetPotential.lean` (copy of `formal/ValyuResearch/CommonQuartetPotential.lean` in the repository's Lean project): the sharp inequality `potential_step_sharp` and its equality example `potential_step_sharp_witness`, plus the earlier weaker 3/16 form `potential_step`, for real `0 < a <= d`, `x` in [0, 1], `y` in [1/3, 2/3]. Build: `cd formal && lake env lean ValyuResearch/CommonQuartetPotential.lean` (Lean v4.35.0, Mathlib); `#print axioms` gives only propext, Classical.choice, Quot.sound.

## Small k by exact bookkeeping (Theorem 2.9): `game/`

- `game/exact_game.py K N VCAP` (numpy) computes, for m = 1..K-1, the least v such that (u, v) is m-safe (u <= N; only v < VCAP*u + 10 is tried, which can only weaken the bounds), by dynamic programming over colour counts of rooted subtrees, and the resulting bounds on h(k). Outputs `game/thresholds_K5_N70.json` (bounds h(2) <= 7, h(3) <= 14, h(4) <= 28, h(5) <= 61; deterministic, recomputed by `sh build.sh --game` in under a minute) and `game/thresholds_K6_N150.json` (`exact_game.py 6 150 6`, about 10 minutes; adds h(6) <= 125 and agrees with the first table on its range).
- `game/verify_exact_game.py FILE K` (stdlib, written separately): re-derives every claim used by the stated bounds with its own implementation of the recursion (13 dynamic-programming evaluations for k <= 5, 31 for k <= 6; a few seconds) and checks the first-tree condition. Negative controls: claiming h(4) <= 27, or lowering the level-2 or level-3 table by one, is rejected.
- `game/brute_dp_check.py` (numpy): compares the recursion with brute-force enumeration of all labelled trees on 5 to 8 leaves for 1075 random complement-symmetric sets of bad colour counts; all agree.

## General upper bound

- `iterate_check.py` (stdlib) runs the plain bound on random families for k=2..5, then tests the sharp potential inequality on an exact rational grid with 1/60 spacing. The grid minimum is 17/90 at r=2, x=13/30, y=1/3, above c=(7-sqrt(13))/18. The sharp iteration is run on 613 families for k=1..6 at n=4,7,16,37,85,195. Every retained pair is checked for separation in all processed trees and for retaining at least c of the potential; the final quartet is checked by tree distances. Radical comparisons use integer/rational squares with sign checks, not floating point. Thresholds use the integer recurrence for powers of 1+sqrt(13) and integer square roots; k=1..8 must give 4,7,16,37,85,195,448,1031. These finite checks test the bookkeeping, not the universal theorem. The completed run is `results/sharp-potential-iteration-20261026.log`.

## Caterpillar lower bound (Proposition 4.1)

- `caterpillar_family.py [KMAX]` (stdlib) builds the k caterpillars C_0..C_{k-1} on 2^k + 1 leaves and counts common quartets over all 4-sets for k <= KMAX (default 6, 677,040 four-sets at k = 6): 0 for every k. For k = 3 it prints the three orders listed by Snir and Yuster.

## Search tools (not needed to check the claims)

`sat/symsat.py` (symmetric search T, sigma T, ..., needs python-sat), `sat/h3sat.py` and `sat/write_cnf.py` (k trees with T1 fixed), `sat/catsat.py` (caterpillar-only sanity check reproducing h*(2) = 6 and h*(3) = 10), `sat/recon.py` (rebuild a tree from a quartet system by leaf insertion), `sat/export_sym.py`. `results/three_tree_n12_partial.log` records the 12-leaf three-tree run: shapes 0-4 (including the caterpillar) UNSAT with verified DRAT proofs, shapes 8-10 SAT.

## Final replay additions

- `check_family.py --expect-common 0 FILE...` now fails on a nonzero common-quartet count. The build uses this expectation for every retained family.
- `check_family_edges.py FILE...` independently computes quartet topologies from edge bipartitions, sharing only the Newick parser with the distance checker. It rechecks binary degrees, reciprocal adjacency, connectivity, tree edge counts and unique quartet splits. The build checks the 13-leaf triple and 22-leaf four-tree family with both algorithms.
- `bipartition_check.py N U --expect-shapes S --expect-bad B` now enforces the stated counts and emits progress. The build requires 135 shapes and zero failures at (14,5), (14,6), (14,7); 66 shapes and respectively 891/0 failures at (13,5)/(13,6).
- `build.sh --game` preserves fresh generator outputs under `results/game-replay-<UTC>/` and compares the K=5 table byte for byte. It does not delete a temporary directory. SAT hash mode uses one worker. Run builds with `nice -n 10` in the shared campaign.
- Historical DRAT proofs were verified during the earlier campaign run and then removed by that run. The current package preserves the logs, CNF hashes and replay scripts; a fresh DRAT replay was not substituted for the independent finite enumeration performed in this resume.
- The supplied Lean file proves only the numerical potential inequality. It contains no formal phylogenetic-tree model and is not a formal proof of the whole paper.
