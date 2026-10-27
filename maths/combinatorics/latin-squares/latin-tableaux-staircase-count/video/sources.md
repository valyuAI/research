# Evidence and scope

Read locally on 26 October 2026. `source-snapshot.json` hashes the accepted manuscript, README, brief and recorded checks. No new web research was required: the coordinator had already retrieved and inspected the priority sources.

| Beats | Claim / example | Evidence |
|---|---|---|
| l01-l05 | Row and column rules; actual (5,4,3,3) filling | `../paper.tex`, definition in section 1; `../video-brief.md` section 3; `check_examples.py` |
| l06 | Novelty withdrawn | `../README.md`, prior-proof section; root resumption record |
| l07-l18 | Exact extension of [5,4,6,3,1,2] to four seven-cell top rows | `../paper.tex`, Lemma `lem:step`; all four displayed rows rechecked in `check_examples.py` |
| l19-l24 | Five invariants and preservation, including both top-two-row safeguards | `../paper.tex`, I1-I5 and proof of `lem:step`; the animation uses actual entries from the same example |
| l25-l29 | Base576; counts144/576/2304 by two methods; unique parent; recurrence and exact formula | `../verification/results.json`, `../verification/check_latin.py`, `../paper.tex` lemmas `lem:base`, `lem:step` and main theorem |
| l30-l32 | Wideness for this family; broader conjectures untouched; ordinary proof scope | `../paper.tex` corollary and scope paragraph; `../README.md` |

The same formula and four-extension mechanism were already publicly proved on 22 October 2026: [issue 20269](https://github.com/the-omega-institute/trureturing/issues/20269) and [merged PR20329](https://github.com/the-omega-institute/trureturing/pull/20329). These were directly retrieved with Valyu Contents by the coordinator on 26 October 2026. This video does not claim a new discovery, first resolution, or a replay of the external formal implementation.

The source conjecture is Daugherty et al., *Counting and constructing Latin tableaux*, arXiv:2610.29291v1, section6. Earlier finite Latinness checks of Chow-Fan-Goemans-Vondrak (2003) already cover this family's small cases through k10, and the six additional 32-cell examples. The video neither claims those examples as new nor attempts to teach the unrelated basis conjecture without prerequisites.

The current accepted recorded build establishes 144,576,2304 by two methods; 576 base invariant cases; all four extensions for the checked next steps; and wideness controls. The video reads these records rather than rerunning the 504-second k7 research enumeration. The production checks only its displayed examples and algebra of the count formula.

Teaching simplifications: the 576-tile collection and branch tree are schematic, labelled as such. Wideness is described only informally; its dominance definition is in the paper. The base is k6, with k5 checked separately. The k10 visual shows only its top three rows and says so. Correctness confidence is high; priority overlap is established. The general wide partition conjecture and Rota's basis conjecture remain untouched.

Production provenance: Cedar synthetic narration, generated with the existing pipeline. No listening review occurred.

## Canonical reference metadata

- Spencer Daugherty, Michaela Fahnestock, Shawn Huxtable, Michael Larson, Nourah Al Munayes and Storey Peacock, *Counting and constructing Latin tableaux* (2026), [arXiv2610.29291](https://arxiv.org/abs/2610.29291). Conjecture6.3 states the count being explained.
- Timothy Y. Chow, C. Kenneth Fan, Michel X. Goemans and Jan Vondrák, *Wide partitions, Latin tableaux, and Rota's basis conjecture* (2003), [arXivmath/0205288](https://arxiv.org/abs/math/0205288), [DOI](https://doi.org/10.1016/S0196-8858(03)00015-0). Wideness context and prior finite Latinness verification.
- The Omega Institute contributors, *Ordinary proof of Latin tableaux count Conjecture6.3* and *Prove Daugherty's full Latin tableaux Conjecture6.3* (22October2026): canonical issue and merged-PR links appear above. Those sources have priority over this independent reconstruction.

Metadata transcribes the accepted bibliography. No raw retrieval response, full third-party text or signed URL is retained here.
