# Final research readiness: Johnson solids

Status: research package complete; full replay passed and all ten PDF pages visually inspected. The author has not yet completed a line-by-line review of every proof.

## Exact claims and scope

- In the fixed-edge-length, planar-face model at the regular convex realisations, 41 of the 92 Johnson solids are first-order rigid, 45 admit explicit continuous flexes, and J58, J59, J60, J81, J82, J83 are first-order flexible but second-order rigid. Thus 47 are locally rigid and 45 flexible.
- J60 and J82 are prestress stable. J58, J59, J81 and J83 are not: each has a stored positive definite dual matrix orthogonal to every stress form. J81's old numerical search failed; the replacement certificate is exact and does not inherit that failed verdict.
- Every regular-cap n-antiprism with n >= 3, radius > 0 and height > 0 is first-order rigid. Every regular prism flexes by tilting its segment summand.
- Comparison only: the regular dodecahedron and truncated icosahedron each have five first-order flexes and a degree-six Macaulay matrix of rank 210/210. Saved dual matrices exactly certify their published non-prestress verdicts. Their rigidity is not claimed as new here.
- No global rigidity statement, no classification of all branches of the flexible realisation spaces, and no Lean formalisation are claimed. First-order dimensions are tangent counts, not dimensions of actual motion families.

## Review issues and resolutions

Original reviews are preserved in `verification/reviews/`.

| Issue | Resolution and evidence |
| --- | --- |
| AHWZ numbering and overbroad attribution | Correct theorem/proposition numbers; explicitly retain its truncated-dodecahedron exception. |
| HSW vs AHWZ formulations | Local change of normal coordinates stated. |
| Second-order forms modulo trivial motions | Invariance stated on the first-order kernel, not arbitrary vectors. |
| J-number identification | Exact geometry and automorphism checks; saved OSCAR incidence isomorphisms for its 91 available solids. J79 has no OSCAR comparison. |
| J58/J59 real double-point concern | Original exact resultant/gcd/Sturm check plus independent sympy Groebner elimination, negative discriminant and projective chart exclusion. The latter shares the stress forms; it is not an independent reconstruction of the whole model. |
| Deficient Macaulay rank | Now described as an inconclusive sufficient test. Complex-zero existence uses the proper chart ideal, not the rank deficiency alone. |
| Unverified J81 non-prestress claim | Historical failure preserved; a higher-precision numerical proposal produced a matrix accepted by exact Sylvester and orthogonality checks. No approximate eigenvalue is used in the proof. |
| Extra checks kept only booleans | Both exact matrices are now saved and replayable. |
| Build masked failures through pipes | Sequential runner propagates child exit codes, emits 25-second heartbeats, requires symbolic checks and records input hashes and logs. No result file is deleted to force replay. |
| Antiprism review did not check determinants | Symbolic checker enforces generic determinant and both low-mode minors; positive height is explicit. |
| Small manuscript inaccuracies | Field degrees corrected to 45 degree-two fields and five above degree eight. Video brief distinguishes exact tangent counts, local rigidity and actual motion. |

## Correctness and originality

Correctness confidence: high, supported by the full replay recorded below. Two separate formulations and arithmetic implementations cover all 92 first-order verdicts. Finite flex and second-order checks have narrower implementation independence, described above. Internal reviews are not external peer review. An earlier code-review summary was retained in working notes, but its standalone transcript was not recovered and is not counted as a new independent replay.

Originality confidence: moderate-high for the complete Johnson table and antiprism statement; no prior classification was found in the documented source/software/recent-paper searches. This is not proof of priority. The dodecahedron and truncated icosahedron verdicts are prior work. The elementary dual-certificate method is a standard separation argument, not a new general rigidity criterion.

DeepResearch: priority `DR-022`; Johnson review `DR-070`; antiprism review `DR-039`. These reviews completed before the recorded final replay.

## Deliverables and reproduction

- `sh build.sh`: all checkers, then LaTeX/BibTeX; sequential worker at nice 10.
- `sh build.sh --quick`: partial replay only.
- Paper: [public PDF](../../../../public-release/papers/johnson-solids.pdf), editable source [paper.tex](paper.tex).
- Narration and animation brief: [video-brief.md](video-brief.md).
- Detailed evidence map: [verification/README.md](verification/README.md).

## Final command results

`sh build.sh` exited **0**, start 2026-10-26 12:53:15 UTC, finish 2026-10-26T13:03:48.766192+00:00. All 17 stages exited 0; every recorded input hash still matches. Manifest and full per-stage logs: `verification/results/replay/20261026T125315Z/`.

- Labels: all 92 passed.
- Both first-order checkers: all 92 passed; exactly 41 R1.
- Finite flexes: 45/45 passed.
- Second order: all six passed; J81 rank 56/56, J82/J83 rank 4/4, J58/J59 zero real roots, J60 nonzero scalar form.
- Non-prestress certificates: J58/J59/J81/J83 all passed exact positive-definiteness and orthogonality checks.
- Comparison solids: both rank 210/210 and exact dual certificates passed.
- Independent J58/J59 elimination: both passed; proper complex chart ideals, negative quadratic discriminants, no projective point at infinity.
- Exact dimensions: all 51 first-order flexible solids recomputed, matching the modular and interval bounds.
- Irreducibility and antiprism symbolic determinant/minors: passed.
- Summary: 41 R1 / 45 F / 6 R2.
- LaTeX/BibTeX: clean final pass, no overfull boxes or undefined references. Rendered and inspected pages 1-10.

Paper SHA-256: `6d7687d4835efb62d6b367a5e22ad02d1a07bc4ea775b686caf4ee396849f111`.
No mathematical computation required by the stated claims remains pending. No external peer review or additional independent final review was performed during the recorded replay.
