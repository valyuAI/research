# Finish review

The original major-revision report and point-by-point response are in [verification/review.md](verification/review.md). This supplement records evidence closure and further corrections on 26 October 2026.

- Both large DRAT checks finished successfully. Recovered their original logs, hashes and elapsed times; refreshed every ledger entry. The check now binds each claim to its retained log and rejects incomplete/mismatched records. An execution log is not a self-contained proof; the actual large proof files are not shipped.
- Reconciled 64 second-encoder outcomes and 41 unmarked `heesch-sat` outcomes by canonical base shape. Replaced the paper's comparison placeholder with the exact scope and an example.
- Independently audited boundary topology: incidence-one edges must form a single degree-two cycle. Every marked witness and all seven levels of the Basic patch pass. Two positive shapes pass; point pinches, holes and disconnected unions are rejected. The Basic check shares the exact grid representation, so it is a second topology check rather than an independent geometric reconstruction.
- Corrected the assertion that all optimal witnesses have imbalance one: six non-row witnesses have imbalance two or three. Straight-row witnesses do have imbalance one.
- Corrected the geometric definition of a nick: intersect the base tile with the complement of the open disk, removing the middle edge segment too. Removing only an open inward half-disk would leave an extraneous line segment.
- Tightened the arbitrary-isometry non-tiling proof: swapping labels is a lattice compatibility symmetry, but should not be invoked as an unexplained geometric symmetry. In a complete tiling generic nick interiors also face bumps, and the full-arc lemma makes the matching bijective. Counting the more numerous arc kind handles both imbalance signs.
- Removed the unsupported blanket statement that every proof regenerates bit-for-bit; that experiment was performed for one small formula. Clarified that the default build replays witnesses and checks retained DRAT records, while a fresh DRAT replay is an explicit reproduction mode.
- Reduced priority wording: no claim of a first proof across inaccessible literature, no new Heesch-5 example and no Heesch-7 claim. Mann, Mann-Thomas, Kaplan, the Atlas and Bašić receive the relevant credit.

All original review gaps relevant to the retained scope have an explicit response. The unresolved limitation is bibliographic overlap with the inaccessible Mann-Thomas fulltext, not a pending computation. Root must perform the independent final review before integration.
