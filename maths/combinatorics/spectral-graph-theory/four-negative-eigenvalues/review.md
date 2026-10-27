# Final review response and mathematical audit

These are internal adversarial reviews, not external peer review. The original campaign reports remain in the lab task directories.

## Reports reused

- Priority audit `graphs-priority-a4`, heavy, `DR-091`.
- First review `graphs-review-a4`, max, `DR-087`.
- Final review `graphs-review-final`, max, `DR-063`.

## Review responses

| Objection or finding | Final response |
|---|---|
| A4=11 and its two examples are already implied by prior work | Accepted. CFJK (2013) proved NPO(5)=16 and supplied W5 and X. Together with the identity of Elphick et al. (2026), this gives A4=11. The retained increment is uniqueness and independent verification. |
| Four maximum rank-8 graphs and their doubling constructions already appear in ACK (2004) | Accepted. ACK's convention permits one isolated vertex, so their order 31 is order 30 here. Neither the four classes nor their constructions are claimed as new. |
| The maximum-order algorithm is already ACK's | Accepted. Section 6 explicitly credits the nonsingular basis plus compatibility-clique method. |
| The closure lemma resembles known principal-rank results and Basso's termination criterion | Accepted. The paper credits the "no 001" theorem, Basso, Jacobi and the known nonsingular-basis lemma. The written extension argument specifies the inertia changes needed by the enumeration. |
| What remains new after these corrections? | The bound n(4)=30 across all possible ranks, in particular exclusion of ranks 9..15 from order 30, and uniqueness of W5/X after removing twins and isolated vertices. Priority confidence remains moderate. |
| Independent verification was needed | Two complete enumerations and two complete per-rank maximum computations agree. The final reviewer independently reproduced the census through order 9 and maxima for ranks 5..9 and 15. We freshly rechecked every census graph and all four order-30 certificates. |

## Mathematical and computational audit

The symmetric nonsingular-basis reduction preserves both nonzero inertia indices. Jacobi's complementary-minor identity gives a deletion of one vertex or an isotropic deletion of two vertices. In the latter case the nonzero off-diagonal Schur complement has one positive and one negative eigenvalue. This proves the extension recursion and that two consecutive empty levels terminate all later ones. The determinant sign is essential when interpreting the adjugate quadratic form and is now explicit in the video brief.

The complete recorded enumerations contain empty levels 16 and 17. The compressed census has 45,242 distinct graphs; its uncompressed SHA-256 is `a4dd169dfccc2c4b64f5e6f7fe88fb0d867da5e7fc51e2d9cb29d2e625c9e211`. A fresh exact LDL-congruence and graph-isomorphism replay found zero inertia or duplicate failures and identified the two order-15 graphs as W5 and X. Both maximum-order runs yield `5,10,18,30,26,22,20,17,15,15,15` for ranks 5..15. The recovered complete doubling check ends `ALL OK` for k=1..4.

Integer form evaluations are bounded before conversion to fixed-width arithmetic. The historical retained computations are also covered by the bound `15^2 * 14^7 < 2^62`. The independent enumerator uses rounded eigenvalues only for isomorphism buckets; actual merging requires exact isomorphism. This cannot delete a distinct class, and any duplicate split is detected by the final duplicate/count check. The auxiliary brute-force census uses a numerical filter with an exact fallback; it is supporting evidence rather than the sole proof.

The final pass audits the previously completed full generations and maxima; it does not mislabel them as freshly regenerated. The fresh checks cover every census graph, the explicit extremal graphs and the evidence structure. Original logs remain unchanged. Bash `pipefail` prevents failed producers from being masked. Negative tests confirm that incomplete termination logs and partial generated output are rejected. A clean package works without the gitignored generated directory; a full replay requires and compares it.

Correctness confidence is high. Originality confidence is moderate: Torgasev's 1987 full text and Mohammadian's 2022 full text were unavailable, and bounded searches do not exclude unpublished work. Nothing is proved for k>=5. Failed one-vertex extensions of six known examples and beam-search failures do not exhaust that case.

All seven final PDF pages were rendered and visually inspected. The final build has no overfull boxes, clipped equations, overlap or unresolved citations. `readiness.md` records the exact retained scope, final hashes and commands.
