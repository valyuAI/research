# The bilinear complexity of F_{q^2}[u]/(u^2), and length-6 cyclic convolution over F_2

**Status:** theorem with exact computer-assisted lower bounds and explicit algorithms. Research draft; not externally refereed.

[Paper](../../../../public-release/papers/mu-q-2-2.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md)

## Claim

Let mu_q(2,2) be the bilinear complexity (tensor rank) over F_q of multiplication in F_{q^2}[u]/(u^2), equivalently in F_q[x]/(p(x)^2) for an irreducible quadratic p. Then

| q | 2 | 3 | 4 | 5 | >= 7 |
|---|---|---|---|---|---|
| mu_q(2,2) = mu_q^sym(2,2) | **9** | **8** | 8 | 8 | 7 |

The proposed new contributions are the unrestricted binary lower bound and the ternary eight-product algorithm. The symmetric binary value 9 was already tabulated by Rambaud in WAIFI 2014 and retained in his corrected thesis. Corollary: cyclic convolution of length 6 over F_2 (multiplication in F_2[x]/(x^6 - 1)) has bilinear complexity exactly **12**.

## Why it was open

- Randriambololona, *Bilinear complexity of algebras and the Chudnovsky-Chudnovsky interpolation method*, J. Complexity 28 (2012), arXiv:1107.0336v5. Question 4.1 asks for the actual values of mu_q(m, l) for small parameters; Example 4.4 says: "Unfortunately it seems difficult to improve the bound mu_q(2,2) <= 9 for q = 2 or 3, at least with this generic method. Whether this is the exact value is yet unsettled." The 2020 survey arXiv:1906.07456v2 (Section 8.2) still uses mu_q^sym(2,2) <= 9 and records mu_4(2,2) <= 8.
- Chengu Wang, *Automated Lower Bounds for Bilinear Complexity over Finite Fields*, arXiv:2603.07280v11 (29 Aug 2026), Table 5: R_{F_2}(C_6) in [11, 12]; his framework also proves only 11.

The answer differs between these two fields: for q = 2 the generic bound 9 is sharp even when asymmetric algorithms are allowed; for q = 3 it is not. The 2012 statement must be read alongside Rambaud's later result for symmetric binary algorithms.

## What is new and how it is proved

- **mu_2(2,2) >= 9** (computer-assisted). Rank <= 8 holds iff some 8-dimensional space W of 4x4 bilinear forms containing the 4 slices of the tensor is spanned by rank-one forms; W can be written as S + <F1, F2, F3, F4>. Using the unit group to fix F1 (3 orbit representatives) and bucketing the last form, 74,377 prefixes are examined and none works. A second program without any symmetry checks all 103,406,616 four-element sets and agrees. Five implementations in total (three C, two standard-library Python) give the same answer, and controls reproduce the known ranks 8 for F_2[x]/(x^4) and 9 for F_16.
- **mu_3(2,2) <= 8**: an explicit symmetric 8-product algorithm for F_3[x]/((x^2+1)^2) (paper, Table 1), found by the same search and checked on all monomial pairs.
- **Lower bound 8 for q = 3, 4, 5** is established by exact searches over 4,794, 21,668 and 73,000 prefixes respectively. A separate C++ checker uses the basis 1,t,u,tu and sorted full-matrix residuals to reproduce the q = 3 and q = 5 exclusions. Its positive controls find algorithms in products of two quadratic fields. The proof does not rely on the draft's unverified attribution of a field-size threshold to Blaser's classification. Upper bounds 9 (p-adic Karatsuba, all q), 8 (q >= 4) and 7 (q >= 7) are elementary constructions; the latter bounds are prior results of Randriambololona.
- **R_{F_2}(C_6) = 12**: x^6 - 1 = (x+1)^2 (x^2+x+1)^2, so C_6 = F_2[x]/((x+1)^2) x F_2[x]/((x^2+x+1)^2); the first factor is a 2x2x2 tensor of rank 3, and the Ja'Ja'-Takche theorem (SIAM J. Comput. 1986: additivity over any field when one format dimension is 2) gives 3 + 9.

## Confidence

- Correctness of mu_2(2,2) = 9 and R_{F_2}(C_6) = 12: high. The reduction lemmas are short and proved in the paper; the exhaustive computation is replicated by independent programs with positive and negative controls. Ja'Ja'-Takche is a published theorem stated for any field.
- Correctness of the complete table: high. The q = 3 algorithm is directly checked; exact finite searches supply the small-field lower bounds, while Alder-Strassen and interpolation settle q >= 7. No Lean formalization is claimed.
- Originality: moderate. The max adversarial review and direct primary-source reads identified substantial prior work: the subspace method is BDEZ/Covanov/Rambaud, symmetric mu_2(2,2)=9 is Rambaud's, and mu_4(2,2)=8 was already claimed in the survey. Searches found no earlier exact unrestricted mu_2(2,2), mu_3(2,2), or binary C_6 rank12 in the sources checked. This is bounded evidence, not proof of priority. The q = 5 computation is a reproducible lower bound, not a claim to a new classical theorem.
- Significance: modest. It answers a concrete question from a 2012 paper and closes one entry of a 2026 table; it does not change asymptotic bounds.

## Reproduce

```sh
sh build.sh                       # replays verification/verify.py and builds paper.pdf
sh build.sh --full                # Python replay plus all compiled searches and controls
sh build.sh --compiled-only       # compiled searches, including independent q = 5 replay
```

`verify.py` uses only the Python standard library and no assertions; see [verification/README.md](verification/README.md) for the C programs and their recorded outputs.

## Not covered

No Lean formalization. The q = 4 lower bound is replayed by the field-table C checker; its upper bound is the elementary construction in the paper. The q = 5 algorithm is included and checked. The optional DRAT proof is archived outside this package, with its successful verification log and hashes included. Quadratic (non-bilinear) multiplicative complexity is not addressed.

## DeepResearch tasks

- `scout-algebra` DR-054 (domain scouting)
- `algebra-c6-priority` DR-079 (priority audit)
- `algebra-mu22-review` DR-086 (adversarial review)
- `algebra-q5-primary-followup` DR-025 (completed primary-source follow-up; could not verify the classical field-size attribution and executed no code. The retained lower bound uses the local exact searches.)
