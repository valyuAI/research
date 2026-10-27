# Verification

All scripts are run from this directory. `verify_extremal.py` uses only the Python standard library. The rest need numpy, networkx, python-flint 0.9.0 and pynauty 2.8.8.1. `brute_census.py` also needs nauty's `geng` on the PATH.

| Script | What it does | Independent of | Expected result |
|---|---|---|---|
| `verify_extremal.py` | Builds W₅ and the AG(2,3) graph X from their definitions. Computes the characteristic polynomials (Faddeev–LeVerrier over ℚ) and the inertia by Descartes' rule and by LDLᵀ congruence. Checks that both graphs are reduced and connected. | everything else; standard library only | both graphs have inertia (11,0,4); `all_checks_passed: true` (see `extremal_result.json`) |
| `enumerate_nonsingular.py 4` | Main enumeration of all nonsingular graphs with n⁻ ≤ 4, by Theorem 3.3 of the paper. Uses FLINT for exact determinants, adjugates and charpolys, and nauty certificates for isomorphism. Writes `output/ns_k4/order{N}.txt`. | - | orders 16 and 17 are empty; `FINAL ... 4: (11, 15)` |
| `enumerate_check.py 4` | Second implementation of the same scheme. Uses Bareiss determinants, Fraction Gauss–Jordan inverses, LDLᵀ inertia, and invariant buckets with VF2 isomorphism. Uses neither FLINT nor nauty. | FLINT, nauty | identical per-order counts; `FINAL max n^+ by n^-: {1: 1, 2: 3, 3: 6, 4: 11}` |
| `check_census.py` | Re-verifies every graph in `census_nonsingular_nneg_le4.txt.gz`: exact inertia by LDLᵀ, pairwise non-isomorphism within each order (VF2), the recorded counts, and that the two order-15 graphs are W₅ and X. | FLINT, nauty | `inertia_or_duplicate_failures: 0`, `counts_match_json: true`, `order15_are_W5_and_X: true` |
| `brute_census.py 10` | Brute force over all graphs on ≤ 10 vertices from `geng`, connected or not. Counts nonsingular graphs with n⁻ ≤ 4. | the closure lemma and the extension code | matches Table 1 for N ≤ 10 |
| `max_reduced_order.py 4` | For every nonsingular basis with n⁻ = 4, computes the exact maximum clique of compatible isotropic 0/1 vectors. This gives the largest reduced graph of each rank. | - | per rank 5..15: 5, 10, 18, 30, 26, 22, 20, 17, 15, 15, 15; `OVERALL ... 30 (rank 8)` |
| `max_reduced_order_check.py 4` | Second implementation of the same computation. Reads the bases from the census certificate, inverts them over Python fractions, and uses its own bitset Bron–Kerbosch clique search; uses neither FLINT nor networkx. | FLINT, networkx, the enumerator output | the same per-rank maxima |
| `ack_check.py` | Enumerates all cliques (not only maximum ones) for every basis of rank ≤ 7, and counts the resulting reduced graphs by rank, number of negative eigenvalues and order. Compares the counts with Table 2 of Akbari–Cameron–Khosrovshahi (2004). | - | `ALL MATCH` (ranks 4–7, t = 2, 3, 4; see `ack_check.log`) |
| `classify_max_order.py 4 8 30` | Lists the isomorphism classes of reduced graphs of order 30 with n⁻ = 4 (all arise at rank 8). | - | see `classify_max_order.log` |
| `order30_check.py` | Reads the four order-30 graphs (`order30_graphs.g6`, copied from `classify_max_order.log`). Checks exactly (LDLᵀ over ℚ) that each has inertia (4,22,4) and is reduced and connected, and that they are pairwise non-isomorphic. Then builds the iterated doublings of K₂ (Kotlov–Lovász step and the variant in Section 6 of the paper) and matches them to the four graphs. | FLINT, nauty | `all_checks_passed: true` (see `order30_check.json`) |
| `extremal_doubling_check.py` | For k = 1..4, lists all reduced graphs with k negative eigenvalues and 2^{k+1} − 2 vertices (all maximum cliques over all bases of rank 2k) and matches them with the doubling words κ^{k−1−j}κ′^j(K₂). | - | k classes for each k, matched one-to-one; `ALL OK` (see `extremal_doubling_check.log`) |
| `k5_extension_check.py` | Evidence for k = 5 (not a proof): builds W₆, its three CFJK variants and the Clebsch + K₅ graphs, keeps those with exact inertia (16,0,5) (six isomorphism classes), and checks all 2²¹ neighbourhoods of a 22nd vertex for each. | - | `any_extension: false` (see `k5_extension_check.log`) |
| `enumerate_nonsingular.py k`, `max_reduced_order.py k` for k = 1,2,3 | Reproduce the published values A₁, A₂, A₃ = 1, 3, 6 and maximum orders 2, 6, 14. | - | as stated |
| `point_determining_bfs.py 3` then `torgasev_maximal_k3.py` | A different generator: all point-determining graphs with n⁻ ≤ 3, built with Sumner's deletion lemma and a pruned extension search. It then counts the maximal connected reduced graphs with three negative eigenvalues. | the Jacobi closure lemma | 32 maximal graphs of orders 9–14, as proved by Torgašev (1989) |

## Certificate

`census_nonsingular_nneg_le4.txt.gz` has one line per nonsingular graph with at most four negative eigenvalues: `graph6 N n⁺ n⁻`. There are 45,242 lines, and the SHA-256 of the uncompressed text is in `census_counts.json`. Soundness (every line is a nonsingular graph with the stated inertia) and distinctness (no two lines of the same order are isomorphic) are checked by `check_census.py` without FLINT or nauty.

Completeness rests on two things:

1. **Theorem 3.3 of the paper.** It is proved by hand from the Haynsworth inertia formula and Jacobi's complementary minor identity.
2. **The exhaustive application of that theorem.** It is carried out by two independent programs, which produce identical per-order counts.

A sound, duplicate-free list with the same per-order counts as a complete, duplicate-free enumeration is itself complete.

## Exactness

The main and second enumerators decide every sign exactly:

- the sign of bᵀ adj(H) b, an integer, together with the sign of det H, an integer;
- the integer bilinear forms used for double extensions;
- an exact characteristic polynomial, or an LDLᵀ over ℚ, for every stored graph.

`enumerate_check.py` uses rounded eigenvalues only to select isomorphism-test buckets; merging still requires an exact graph isomorphism. Rounding can split isomorphic candidates but cannot remove a distinct graph. The independent census soundness/count comparison detects any resulting duplicate count. `brute_census.py` uses floating-point eigenvalues to classify its auxiliary check. It accepts a sign pattern only when every eigenvalue has modulus above 10⁻⁶; for 0/1 matrices of order ≤ 10, the rounding error of the symmetric eigensolver is below 10⁻¹². Every other case goes to an exact FLINT characteristic polynomial.

## Final evidence audit and failure handling

`audit_recorded.py` verifies the census SHA-256, both complete census logs including empty orders 16 and 17, both per-rank maxima, and the explicit graph checks. When generated `output/ns_k4/` files exist, it also compares all 45,242 rows with them and rejects any incomplete output. Those reproducible files are gitignored; the compressed census and logs are the packaged evidence. `--require-generated` makes their presence mandatory, and is used after a full build. This is an audit of saved complete runs, not a fresh enumeration. `build.sh --full` reruns the generation and cross-checks. The default build states its limited scope, audits saved evidence, and freshly checks W5 and X. The build uses Bash with `pipefail`; a failed producer cannot be hidden by `tee` or `tail`. Explicit graph and doubling checks exit nonzero when their result is false.

The int64 form evaluations are bounded before use. For the retained ranks at most 15, Hadamard gives each adjugate entry at most 14^7, so the sum of at most 15^2 terms is below 2^62; the rational-inverse implementation also checks its actual scaled entries. This is separate from the exact-integer inertia and graph-isomorphism decisions.
