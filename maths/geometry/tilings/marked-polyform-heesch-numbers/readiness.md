# Research readiness

**Narrowed computational result; the author has not yet completed a line-by-line review.** No pending DRAT process blocks the retained tables. Originality remains bounded and qualified.

## Exact scope

Maximum strict lattice Heesch number over **all unbalanced, single-centred-slot markings**, with grid-aligned rotations/reflections/translations: every polyhex of size <=4 (12 bases), every polyomino of size <=5 (21 bases), and the straight five-hexagon row. Maximum 5 for the polyhex family, attained by the straight four-row; the straight five-row also has maximum 5. Polyomino maximum 3, attained by the straight four- and five-rows.

This is not a new planar Heesch record. It does not exclude off-grid coronas of the realized curved tiles, balanced non-tilers, extra mark slots, oriented rules or richer alphabets. The Bašić patch check confirms an existing result.

## Evidence closure

- **34** witnesses freshly checked, with one centred slot per edge enforced by the ledger. **170** witness mutations and **6** corrupt ledgers rejected.
- **34** original DRAT success records retained in `verification/logs/drat/`, with CNF/proof hashes, formula dimensions, UNSAT and VERIFIED markers. The default build checks these records; it does not replay the large DRAT proofs.
- Straight four-row: 947,735 variables, 6,895,353 clauses, 257,547,287 proof bytes; original DRAT replay **3,445.971 seconds**, completed 12:56:12 UTC.
- Straight five-row: 1,562,333 variables, 12,387,835 clauses, 743,985,765 proof bytes; original DRAT replay **4,378.861 seconds**, completed 14:30:44 UTC. This record relies on the completed search and replay, which were not repeated.
- Second encoder: **64** retained SAT/UNSAT agreements, covering both bounds for 32 bases. The straight four- and five-row are excluded from this cross-check. Unmarked control: **41** saved Hc values agree with Kaplan's `heesch-sat`.
- Bašić: **169** copies, layers 1,6,10,13,32,52,55; all original strict-disk/interior checks pass. An additional boundary-cycle algorithm confirms one simple cycle at every U0..U6, with boundary edge counts 75,227,343,490,718,842,965. It rejects pinch, hole and disconnected examples. It shares the original exact geometric representation, not the topology test.

Large proof files were removed by the original workflow after verification; regeneration commands and hashes are supplied. Only one small formula was tested for bit-identical proof regeneration. No blanket bit-identity guarantee is made.

## Review and confidence

Correctness: **high** within the stated lattice model, conditional on the written encoding argument, exact witness programs and recorded DRAT checks. DRAT certifies the CNF, not the correctness of the encoding. No Lean formalization or formally verified DRAT checker.

Originality: **moderate** for the all-markings row exclusions, **low to moderate** for the small tables. Mann already supplied Heesch-5 hexapillars; the Atlas already reports exact 5 for a particular marking of both rows; Kaplan proposed extending SAT to marked polyforms. Mann-Thomas 2016 fulltext was unavailable, so table overlap remains unknown. No first-discovery claim is justified by a negative search alone.

Review DR-031 recommended major revision. Scope, geometric counting and prior-art issues are addressed in `review.md` and `verification/review.md`. Priority: DR-072. Scout: DR-012.

Root owns independent final review, integration and video. `video-brief.md` builds from tilings and rings, explains the two certificate types, and explicitly restricts the result. No video files were edited.

## Final artifact inspection

Built `paper.pdf`: **9 pages**, all visually inspected after the final source edit. No overfull boxes or undefined references. SHA-256 `52783ae8e8d2f8e1a7f47c56fb893f26460b369d4b02df9f0cddff1a47f126c6`. `verification/pdf-inspection.json` records the inspected revision. Both one-page figure PDFs were also visually inspected. 
