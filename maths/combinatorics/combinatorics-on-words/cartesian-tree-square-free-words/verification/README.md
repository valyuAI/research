# Verification

| File | Purpose |
|---|---|
| `check_ct.py` | Independent standard-library verifier of properties (S), (D), (F) for `h2` (theorem `A`), `h3` (theorem `B`) and an alternative 6-uniform binary morphism (`A6`). No `assert` statements; exits with status 1 on any failure. Writes `results_check_ct.json`. |
| `controls.py` | Encoding agrees with the source authors' `psv_encoding` (their unit tests and 20,000 random words); exhaustive search reproduces the finite Cartesian-tree entries 1, 5, 29, 9 of Table 1 of arXiv:2607.00674; negative controls (half-length 3 for `h2`, corrupted morphisms) are rejected; images of a Dejean prefix are CT-square-free. |
| `ctproof.c` | Separate C implementation of the same three checks (`./ctproof s l q img_a img_b img_c`). Output in `results_ctproof.txt`. |
| `morphbt.c` | The exhaustive backtracking generator used to find the morphisms (discovery only; not needed for verification). It keeps only injective synchronizing triples, so its negative results concern that class. `./morphbt 2 4 4 8 1` and `./morphbt 3 3 5 8 1` report no candidates, `./morphbt 2 4 5 8 3` and `./morphbt 3 3 6 8 3` report candidates. |

Commands:

```sh
python3 -B -O controls.py
python3 -B -O check_ct.py A B A6
clang -O2 -o ctproof ctproof.c && ./ctproof 2 4 5 00101 00111 01100 && ./ctproof 3 3 6 000101 000221 022211
```

Recorded results (26 October 2026, Python 3.13): theorem A: q = 5, r = 3, M = 56, K = 24, 4,596 base words of length K (21,801 of lengths 1 to K), 23 encoding classes at radius 3, radius 2 ambiguous, no CT-square; theorem B: q = 6, r = 3, M = 64, K = 23, 3,654 base words of length K (17,205 of lengths 1 to K), 21 classes, radius 2 ambiguous, no CT-square. SHA-256 of the newline-joined base-word lists: length 24 `d4f833ee5321be30c05bbc988b1408654a6568cfecf12992c68a441c6fd2ff76`, length 23 `a317124a04c276733769b597d7780493b1665bce7ac55ddddef94f3e5fa6a09c`.

Trust boundary: the enumeration of 7/4+-free words (each program has its own), the parent-distance computation (quadratic definition for (D) and a monotone stack for (F) in Python; a nearest-smaller-or-equal table in C), and the comparison loops. The deduction from (S), (D), (F) to the theorem is the written Proposition 3.1 of the paper.
