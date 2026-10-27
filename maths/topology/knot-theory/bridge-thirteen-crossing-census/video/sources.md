# Evidence ledger

Reviewed 2026-10-26. Claims follow the final README, paper, verification data and cell handoff, including corrections made after the adversarial report. No paper or checker was edited during video production.

| Claim or visual | Source | What this worker checked |
| --- | --- | --- |
| 25 pinned-list additions, 27 total certificates, 268 residual | `../README.md`; `../paper.tex`, census and scope; `verification/open-list-v1.3.0.json`, `remaining-v1.3.0.json` | Both complete checkers replayed; preserved `qa/check.log` and `qa/check-matrices.log` |
| Actual `13n_1005` diagram | `verification/certificates.json`, matching source snapshot row | Reconstructed from the PD cyclic order; verified no extra segment intersections and correct counterclockwise port order at every crossing |
| First crossing `[3,1,4,26]`, incoming `(01)(23)`, over `(01)(34)`, outgoing `(01)(24)` | Paper finite certificates; same saved entry | Compared displayed labels to certificate; both checkers agree on arc reconstruction and all relations |
| Four seed arcs `0,3,7,4`; nine exact colouring moves | Same certificate | Every rendered move is derived from the source; checked known overarc, known underarc, new underarc and inherited seed colour |
| Four seed actions connect eight dots | Same certificate's seed permutations | Actual connected-component counts after each seed: 6, 5, 3, 1. The displayed tree has the seven distinct swap edges |
| Each meridian contributes rank difference two; full fixed-space codimension seven | Paper rank lemma and permutation-module argument | Both exact checkers replayed on all 27; displayed binary-equality model uses the full eight-dimensional module |
| `4 <= mu <= b <= 4` | Paper rank lemma plus cited BKVV theorem | Colouring theorem is attributed, not depicted as an unimplemented spatial reconstruction |
| 24 double-transposition entries plus `13n_4645` by a 3-cycle | Certificate status and type fields | Count and names derived from saved file; a 3-cycle is animated as a rotation of three tokens, not two swaps |
| Two prior cables excluded from 25 | Final README and paper, prior satellite bound | No claim to new cable values; residual ledger explicitly distinguished from mathematical openness |
| Coxeter overlap excluded only for A4/D4/H4 | `verification/coxeter-overlap-summary.json`; final README | Read completed audit and its scope; did not rerun this optional search |
| Broader family-theorem priority remains unresolved | Final README; final cell LOG; final adversarial review | Spoken explicitly; no globally-first or new-general-method claim |

Exact final review read: `<unpublished-record-51cb39cd55d9>`, task `DR-027`. Its inability to inspect 19 local certificates is a review-access limitation, addressed by the complete local checker replays. Its BKM overlap objection predates the subsequent completed A4/D4/H4 audit. Its special-family priority objection remains unresolved and is retained in the narration.

Background sources retrieved through `valyu contents` on 2026-10-26. Canonical citation metadata is saved in `qa/background-sources.json`; full retrieval responses are retained outside the repository:

- [Wirtinger systems of generators of knot groups](https://arxiv.org/abs/1705.03108v1), Blair, Kjuchukova, Velazquez and Villanueva. The package cites the colouring-to-bridge theorem.
- [Symmetric quotients of knot groups and a filtration of the Gordian graph](https://arxiv.org/abs/1711.08144), Baader and Kjuchukova. Prior permutation-quotient context; the method itself is not claimed as new.

Display validation is reproducible with `prepare_assets.py`. `example.json` freezes the displayed data; `qa/example-check.json` records input hashes, actual moves and layout checks. A preliminary nearest-angle unwrap test was unsuitable at boundary vertices with a gap larger than pi. It was replaced by a directed modular-gap cyclic-order check, which enforces the stated PD convention rather than weakening it.

Teaching limits: the height-profile and four-arch sketches are explicitly schematic, not embeddings of `13n_1005`. The complete diagram is a polygonal projection reconstructed from the accepted data. The full 20,160-element image group need not be explained to establish the lower bound; connectedness suffices. Finite checks are exact, but not proof-assistant formalisation, external peer review or proof of priority.
