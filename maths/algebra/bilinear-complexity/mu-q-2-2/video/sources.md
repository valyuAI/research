# Evidence and scope

Read locally on 26 October 2026. The accepted research package is the factual authority for this production; no new web search or research claims were needed. `source-snapshot.json` records the exact scientific input hashes used. Narration is in `narration.json`; animation is in `scenes.py`.

| Beats | Claim / example | Local evidence |
|---|---|---|
| a01-a04 | Karatsuba: 8, 15, 45; middle 22; coefficient products are counted | `../paper.tex`, Proposition `prop:nine`; `../video-brief.md` section 3; directly recomputed in `check_examples.py` |
| a05-a14 | Binary reduction x^4=x^2+1; four slices; 225 rank-one forms | `../paper.tex` section 2 and Theorem `thm:q2`; four actual slice matrices checked independently in `check_examples.py` |
| a15-a19 | Span equivalence, 103,406,616 eligible independent four-sets, 74,377 prefixes, no rank-eight algorithm | Lemmas `lem:slices`, `lem:normal`, `lem:sym`; `../readiness.md`; `../verification/logs/replay-20261026T134435172402Z/results.json` |
| a20-a24 | Complete finite-field table; symmetric ternary recipe; 16 monomial identities; two q=5 exclusions | `../paper.tex` Table 1, upper/lower bounds; `../verification/certificates/q3_rank8.json`; `../readiness.md` |
| a25-a28 | Binary C6 has rank12; special two-dimensional summand additivity | `../paper.tex` section `sec:c6`; `../verification/certificates/upper_bounds.json`; ring example checked locally |
| a29-a32 | Prior symmetric binary9, prior methods and q4 survey claim, bounded novelty, no Lean | `../README.md`, `../readiness.md`, `../verification/sat-replay.md`; accepted root resumption record |

Primary references and provenance are retained in `../references.bib`. The root read Rambaud's WAIFI 2014 paper and corrected thesis, and corrected the earlier novelty claim. The subspace method belongs to Barbulescu-Detrey-Estibals-Zimmermann, Covanov and Rambaud. Randriambololona's 2012 constructions supply the larger-field upper bounds. Ja'Ja'-Takche (1986) supplies the special direct-sum theorem. The general direct-sum claim is explicitly not made.

The q=5 lower bound is computational: each exact checker reports 73,000 prefixes and 17,417,506 residual buckets with no rank7 witness, plus successful split-product controls. No unsupported Blaser field-size threshold is used. The compiled research run has 12 passing cases. This video production reads those completed logs; it does not rerun the expensive exhaustive research searches.

The approximately 628 MB DRAT certificate is archived in the lab, outside the repository. Only the manifest and successful replay logs are bundled with the research package. No Lean formalization exists for this algebra package. Correctness confidence is high; priority confidence is moderate and bounded.

Teaching simplifications: the span container is explicitly schematic. Candidate boxes do not stand for individual sampled scientific failures. Product-reuse arrows explain the representation criterion, not an unverified eight-term decomposition. The video presents one actual ternary form, while all eight terms and output weights remain in the paper. A finite field of four elements is distinguished from integers modulo four. The full interpolation and additivity proofs are outside this short explanation.

Production provenance: Cedar synthetic narration from the existing speech pipeline. No listening review is claimed.

## Canonical reference metadata

- Hugues Randriambololona, *Bilinear complexity of algebras and the Chudnovsky-Chudnovsky interpolation method* (2012), [arXiv1107.0336](https://arxiv.org/abs/1107.0336). Question4.1 and Example4.4 supply the small-algebra question and interpolation bounds.
- Matthieu Rambaud, *Finding optimal Chudnovsky-Chudnovsky multiplication algorithms* (WAIFI2014), [author manuscript](https://perso.telecom-paristech.fr/rambaud/articles/waifi.pdf), and [corrected thesis](https://perso.telecom-paristech.fr/rambaud/articles/thesis_final.pdf). Prior symmetric binary value9; thesis TableI.2.1 and sectionII.3.1.
- Stéphane Ballet, Jean Chaumine, Julia Pieltant, Matthieu Rambaud, Hugues Randriambololona and Robert Rolland, *On the tensor rank of multiplication in finite extensions of finite fields and related issues in algebraic geometry* (2020), [arXiv1906.07456](https://arxiv.org/abs/1906.07456). Section8.2 records the prior q4 claim.
- Razvan Barbulescu, Jérémie Detrey, Nicolas Estibals and Paul Zimmermann, *Finding optimal formulae for bilinear maps* (2012), [DOI](https://doi.org/10.1007/978-3-642-31662-3_12); Svyatoslav Covanov, *Improved method for finding optimal formulae for bilinear maps in a finite field* (2019), [arXiv1705.07728](https://arxiv.org/abs/1705.07728). Method credit for the finite subspace search.
- Joseph Ja'Ja' and Jean Takche, *On the validity of the direct sum conjecture* (1986), [DOI](https://doi.org/10.1137/0215071). Special additivity theorem used for the C6 consequence.
- Chengu Wang, *Automated Lower Bounds for Bilinear Complexity over Finite Fields* (2026), [arXiv2603.07280](https://arxiv.org/abs/2603.07280), accepted package version11. The earlier C6 interval is11-12.

These entries transcribe the accepted bibliography; no full third-party text, raw retrieval response, credential or signed URL is included.
