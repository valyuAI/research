# Research readiness, 26 October 2026

The retained theorem is `mu_q(2,2) = mu_q^sym(2,2)`: 9 for q=2, 8 for q=3,4,5, and 7 for prime powers q>=7. Binary cyclic convolution of length six consequently has unrestricted bilinear rank 12. Correctness confidence is high. Originality confidence is moderate and bounded by the primary sources inspected. The package has no Lean formalization and has not been externally refereed.

## What changed after adversarial review

- Credited Rambaud's WAIFI 2014 table and corrected thesis for the already-known **symmetric** binary value 9. The current lower bound also excludes asymmetric eight-product algorithms.
- Credited the subspace method and symmetry approach to BDEZ, Covanov and Rambaud. The q=4 equality was already claimed in the survey from an unpublished exhaustive search.
- Removed the unsupported attribution of a precise finite-field-size threshold to Blaser's classification. The original draft also claimed a completed q=5 run without a supporting log. Two actual exhaustive runs now establish that lower bound independently of the disputed citation.
- Restored the completed rank-eight SAT proof check: `drat-trim` reported `s VERIFIED`. The encoder regenerates the exact solved CNF. The successful log and input/proof hashes are bundled; the 628 MB proof is not included in this repository. The standard replay does not depend on that external file.
- Removed unfinished placeholders and the unsupported claim that the method decides every small four-dimensional algebra in minutes. The earlier full Python replay took about 26 minutes on a shared machine.

## Verification evidence

`verification/logs/replay-20261026T134435172402Z/results.json` records all 12 successful compiled checks, including:

| Check | Exact result |
|---|---|
| Binary rank<=8, no symmetry | 103,406,616 independent four-sets; no witness |
| Binary rank<=8, prime-field bucket / field-table bucket | 74,377 prefixes each; no witness |
| Binary controls | Rank-eight space found for F2[x]/x^4; none for F16 |
| q=3 rank<=7 | 4,794 prefixes; no witness |
| q=4 rank<=7 | 21,668 prefixes; no witness |
| q=5 rank<=7, field-table C | 73,000 prefixes, 17,417,506 candidate buckets; no witness |
| q=5 rank<=7, separate C++ | Same exact counts in basis 1,t,u,tu, with sorted full-matrix residuals; no witness |
| Separate C++ q=3 | 4,794 prefixes, 205,980 candidate buckets; no witness |
| Separate C++ positive controls | Finds rank-at-most-seven spaces for F9×F9 and F25×F25 |

The prior `verification/results.json` records the unchanged standard-library Python checker passing all explicit decompositions, 96 corrupt ternary certificates rejected, binary exhaustive checks and controls, and the full ternary lower-bound replay. The new C++ program does not share the field-table arithmetic or quotient-coordinate construction of the C program; it does share the mathematical subspace completeness argument.

The compiled runner now checks answers, enumeration counts and exit status, with timestamped logs and 20-second heartbeats. Negative controls reject a wrong answer, wrong count, count with an extra trailing digit, nonzero process exit and missing result. A valid control passes. The build wrapper propagates Python exit 37 and does not enter the PDF phase after failure. The guarded binary no-symmetry checker was recompiled without warnings and rerun after its final argument-validation change. All three edited compiled entry points reject missing arguments with exit 2. These controls and source hashes are recorded in the completion manifest.

## Literature review and limitations

- Adversarial task `DR-086` found no mathematical error in the supplied argument, but correctly flagged attribution and missing q=5 evidence.
- Focused task `DR-025` could not retrieve the necessary full classification theorems and executed no code. It therefore does not prove a classical lower bound or independently reproduce the new searches. Its limitation is addressed by the two local exact programs, not by promoting an abstract into a theorem.
- Direct primary-source reads recovered the corrected Rambaud thesis, unlike those review runs. Table I.2.1 and Section II.3.1 retain the symmetric binary value 9. This strengthens the priority correction.
- The unrestricted binary value, ternary eight-product algorithm and binary convolution rank 12 were not found as exact prior values in the sources checked. This does not establish global priority. The q=5 value is presented as a reproducible computation, without claiming a first classical theorem.
- Ja'Ja'-Takche additivity applies because one summand has format 2×2×2. Its arbitrary-field scope was checked against the primary abstract and the discussion in Buczynski-Postinghel-Rupniewski. General tensor-rank additivity is not asserted.

## Delivery state

The six-page PDF builds. All pages were visually inspected; a long inline equation and a stretched reference were repaired, and changed pages rechecked. The video brief matches the corrected claims. Harvey Yorke has not yet completed a line-by-line review of every proof.
