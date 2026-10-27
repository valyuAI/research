# Bounded priority audit

The audit date is 26 October 2026. All online searches and content retrieval used the Valyu CLI. This record separates successful checks from failures and does not treat an empty search as proof of novelty.

## Source and closest prior work

- [arXiv:2404.06585](https://arxiv.org/abs/2404.06585) metadata: v4 is dated 6 July 2026. Earlier versions are dated 9 April 2024, 6 August 2025 and 27 April 2026.
- Read the full text retrieved for [v4](https://arxiv.org/html/2404.06585v4), particularly Section 6, Conjecture 6.1, the first-occurrence formulas and the length-three results. Contents returned the same mathematical text through the HTML and versioned PDF URLs. The conjecture wording and reported numerical short cases agree with the journal-linked record.
- [DMTCS article page](https://dmtcs.episciences.org/en/articles/18715): published 8 July 2026; last modified 7 September 2026; DOI 10.46298/dmtcs.16361; links arXiv v4. Direct extraction of the journal download URL failed to return text locally. The focused literature review retrieved the journal PDF and corroborated Conjecture 6.1 there.
- [Elizalde's research page](https://math.dartmouth.edu/~sergi/research.html) lists the 2026 DMTCS paper. No relevant follow-up was identified in the retrieved list. This is a bounded page inspection.
- Read the cluster-method and linear-extension sections of [Elizalde and Noy, arXiv:1210.6061v1](https://arxiv.org/abs/1210.6061v1). Verified journal, pages and DOI against its arXiv metadata. The cluster machinery is prior work and is credited.

## Search queries

Initial and focused searches included:

```text
Penney game open problems conjectures 2025 2026
"Penney" "permutations" conjecture solution cyclic rotation
"Penney" "permutations"  [publication start date 2026-09-01]
"Penney" "permutations" "conjecture" [GitHub and Zenodo sources]
"2404.06585" solution conjecture [GitHub, Zenodo and Erdos Problems sources]
```

The domain-restricted searches often returned unrelated results. They are weak negative evidence and missed the exact GitHub target below.

## Direct public API checks through Contents

- GitHub issue search, `q="2404.06585"`: total 1, `incomplete_results=false`. The result is [V3R1T4S proposal 688](https://github.com/elder-plinius/V3R1T4S/pull/688), created 24 October and closed 25 October without merging. Read the pull record and its discussion. The maintainer's 25 October 19:30 UTC comment still calls the conjecture open, notes only truncated evidence for lengths four and five, and explains that closure followed addition to the bank. It provides no proof or counterexample.
- Retrieved the main branch's `bank/targets.json` and read the exact `penney-permutations-rotation-conjecture` record. Its `status_checked` field is 25 October 2026 and its `disclosure` is `open`. It requests exact finite verifications or a formal proof; this is a problem statement, not a solution.
- GitHub issue search, `q="Penney" "rotation" in:title`, `per_page=25`: total 2, `incomplete_results=false`. One result is proposal 688; the other concerns a word-game proposal and is outside the permutation model. No resolution appeared in these results.
- GitHub repository search, `q="2404.06585" in:readme`, `per_page=25`: total 0, `incomplete_results=false`.
- GitHub code search for the exact arXiv ID returned HTTP 401, requiring authentication. Code-search coverage is therefore absent. A broader issue query returned a large truncated response and is not used as complete evidence.
- Zenodo records API, `q="2404.06585"`, `size=25`: total 0.
- Zenodo records API, `q="Penney" AND "permutations"`, `size=25`: total 0.
- Earlier Zenodo requests with `size=50` failed with HTTP 400 because unauthenticated page size is limited to 25. The corrected queries above succeeded.
- arXiv API, `all:Penney AND submittedDate:[202609010000 TO 202610262359]`, maximum 50: 7 returned records, all unrelated to the permutation race. Repeated with `lastUpdatedDate` over the same interval: again 7 unrelated records. The returned records concern Kronig-Penney models, quantum walks, vertex algebras and band extrema. These are metadata-keyword checks, not searches of all citing full texts.

## Research-review checks

- `probability-fresh-scout`, heavy, `DR-056`: recommended the conjecture and found no resolution within its bounded search.
- `probability-penney-priority`, heavy, `DR-042`: checked source versions, the journal paper, author material and related literature. It found no proof, counterexample or partial resolution. It explicitly lacked direct Zenodo/forum checks and complete citation-database access. The direct API checks above supplement it.
- `probability-penney-final-review`, `DR-044`: completed 26 October at 11:47 UTC. It found no fatal error or prior proof, independently reconstructed all finite inequalities, and re-derived the uniform argument. It requested clearer exposition, actual C++ execution records and a rigorous length-three comparison. These are supplied in the revised package, including a new independent horizon-18 certificate. The focused follow-up found no material gap in the added base case; its operational reproduction request was closed by local independent executions and exhaustive controls.
- Semantic Scholar's public graph API listed two citing records. Read the relevant passages in arXiv:2601.16580v2 (independent streams of words) and arXiv:2511.13287 (avoiding increasing subwords, citing Lin's thesis). Neither addresses Conjecture 6.1. The citation list is not assumed complete.
- An Erdos Problems domain search returned a number-theory tag page and forum thread 473 on prime sums of adjacent permutation entries, both unrelated. Direct `/search?query=Penney` returned 404. No matching Erdos problem entry was identified.

## Limits

No assertion is made about private, unpublished, unindexed or differently titled work. GitHub code search was unavailable. Empty Zenodo and repository searches do not prove absence. The problem-bank record is strong contemporary evidence that its maintainers still regarded the question as open on 25 October; it is not a novelty certificate. Originality confidence remains moderate.

## Final repeat before curation

Repeated on 26 October 2026 around 12:10 UTC: Zenodo exact-ID search sorted by newest still returned zero. GitHub title search sorted by update still returned two records, with only the target proposal relevant; its latest update was 25 October 19:30 UTC, and its sole discussion comment was unchanged. A direct arXiv ID-list API request timed out or was refused. The fallback abstract URL with `context=math.CO` succeeded and still listed v4, revised 6 July 2026, as latest. No resolution was identified. Originality confidence remains moderate, with all earlier coverage limits retained.

Follow-up review `DR-014` completed at 12:21 UTC. Its scope was the new length-three certificate, rather than a fresh complete literature search.
