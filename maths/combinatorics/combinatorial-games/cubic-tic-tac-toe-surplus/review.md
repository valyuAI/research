# Reviews and responses

## DeepResearch priority audit

Task `DR-046` (heavy, 26 Oct 2026). Findings:

- No resolution of 5^3 or 6^3 was found in any source: arXiv since Sep 2025, citing papers, Zenodo, GitHub, MathOverflow or MSE.
- arXiv:2509.21494 has only v1.
- No independent verification or criticism of the 7^3 proof was found.
- The audit independently noticed the same opposite-octant problem in Sec. 4.3.
- Beck (2008) calls 5^3 "a hopeless open problem (it is conjectured to be a draw game)".
- Uiterwijk's set matching (arXiv:1703.10678) is the closest related technique.

## DeepResearch adversarial review

Task `DR-018` (max, 26 Oct 2026). It found no fatal error. By hand, it re-derived:

- Lemma 2.1 and Corollary 2.2;
- the 12-partner count and the counts 25/168/339;
- the Table 1 set counts (576/288/384/48);
- the 10,627-leaf count;
- Remark 3.3, Proposition 5.1 and the symmetry characterization.

It confirmed the gap claim against the v1 text. Responses to its objections:

| Objection | Response |
|---|---|
| Lemma 2.1(2) is Lovasz-Plummer Thm 1.3.6; the Hall pairing criterion is Hales-Jewett 1963 / Beck's bigamy corollary. | Accepted. Both are now cited. The novelty claim is limited to using surplus to absorb unknown Maker moves, worded as "we are not aware of an earlier use". |
| "Erdos-Selfridge applies at n = 8" is misattributed (the classical sum criterion fails at 8^3). | Accepted. The clause is reworded to point to the potential-function discussion in CRK. |
| Seven versus eight Maker moves for 6^3. | Accepted. The text now says the first eight moves (seven after symmetry reduction of the first). |
| The count 49,104 is unexplained (hand count 48,960). | Accepted. The draft figure was a placeholder. The C run reports 48,960 configurations, all with sigma = 3. |
| The abstract's 24,359,523 mixes two enumerations. | Accepted. The abstract now gives the two figures separately and states where the greedy rule applies. |
| The repair should be Proposition 3.2, with the greedy run as a cross-check. | Accepted, and reworded. |
| "Opening lengths are optimal" is too strong. | Accepted. Renamed "Earliest possible pairing", with a caveat that it is a counting bound only. |
| The gap is larger: m1 = (3,3,3), m2 = (5,5,5) already blocks the second move. | Accepted. Added, with the counts: 5,832 ordered pairs, or 1,977,048 positions unreduced. |
| Say "assumes", not "wrongly claims"; check the "on request" statement. | Accepted. The tarball README says code for the other case "will be provided if requested". This is cited. |
| Unfair comparison with 3.5e7 raw positions; give wall-clock times. | Accepted. Section 6 now notes that CRK did not use symmetry, gives run times, and says the gain is structural. |
| Strong-game draw needs strategy stealing. | Accepted. Cited. |
| Empty slot set edge case. | Accepted. The text now assumes at least one alive line. |
| Provenance of the author block. | Not changed. It follows the collection's house convention. |
| The computations are trusted, not formalized. | Agreed; this is stated in the paper. Three separately written programs agree, and the independent from-scratch check is below. |

## Independent from-scratch check

A separate reconstruction completed the central checks, the pattern tree and both raw non-central shards. The review session ended before a narrative verdict was written. The recovered source, complete output files, method inspection and exact scope are recorded in `verification/independent_check.md`; the original scripts are preserved in `verification/independent/`.

## Build failure handling

Integration found that the Python check's output pipeline could hide a nonzero exit, while both C programs returned success even after reporting failed conditions. The build now waits for each check directly, propagates its status and prints progress every 15 seconds. The surplus checker validates its exact claimed histograms and configuration count; the published-strategy replay returns failure when any position fails. These changes affect acceptance and reporting, not the matching algorithms.
