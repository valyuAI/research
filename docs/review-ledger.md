# Review ledger

The full arguments are in the papers. This ledger records the limits of the review process and consequential changes.

## 25-26 October campaign

The [collection index](collection.md) links nineteen additional packages and their individual review records. Consequential review changes include:

Final integration review found and reproduced five validation defects and one case-sensitive link error. The fixes bind tiling proof logs to their exact formula scope, reject unsafe algebra inputs and exhausted resources, enforce complete result counts, and prevent Python optimization from disabling substantive checks. A related q=7 hash-capacity hang was also repaired. A [fresh closure review](verification/final-fix-closure-20261026/report.md) found all six findings and the q=7 defect closed with no actionable regression in that scope. Its precise fresh-versus-retained evidence is recorded; it is not a new reproof of every package or a certification of novelty.

| Package | Finding or correction accepted | Evidence boundary |
|---|---|---|
| Common quartets | Relabel the larger retained set at every cut; exact threshold arithmetic; sharpen the potential factor to `(7-sqrt(13))/18` | Fresh max review, Lean inequality/equality audit and 613 executable tree-family checks. Neither the tree theorem nor global strategy optimality is formalized. |
| Chemical robustness | Replace numerical stability decisions in the second checker with exact Routh-Hurwitz tests; expose the elementary nature of the three-species construction | The main dimension-two proof was covered by an earlier full review. The final review's shorter prompt omitted that case analysis and cannot be counted as a second full audit of it. |
| Finite-field multiplication | Credit Rambaud's symmetric binary value and earlier subspace methods; replace an unsupported completed-run claim with two actual q=5 exhaustive replays | The two q=5 programs agree on 73,000 prefixes and 17,417,506 candidate buckets. The focused literature report executed no code. |
| Latin tableaux | Withdraw the first-resolution claim after reading the earlier public proof | Same formula and four-extension mechanism. Retained only as an independent verification note. |
| CTLN | Credit standard-parameter counterexamples implied by a prior family | The eleven-vertex example is minimal under deletion. Global minimality remains between eight and eleven. |
| Spectral graphs | Credit the known A4=11 bound and the four rank-eight extremal graphs | The proposed new contributions are higher-rank exclusion, the maximum reduced order 30 and uniqueness in the stated second classification. |
| Hex | Recover all 36 L7 replays, enforce scoped checker outputs and preserve both rule readings | 22,780,097 positions establish the L7 exclusion. The L8 upper result remains search-only. |
| Covering systems | Fix a broken absolute-path invocation and require successful exits, exact counts and completed result summaries | Three primary implementations complete with zero survivors. The optional odd-part-135 extension lacks a clean independent static replay and is excluded. |
| Marked tilings | Require strict disk topology, check pinch points, correct the imbalance-one overstatement and recover both large DRAT completions | Upper bounds are only for the lattice marking model. Logs and regeneration hashes are retained; the large proof files were removed after their original checks. The default build does not replay them. |
| Knots | Keep the 25-entry increment tied to the pinned census | Two exact checkers replay the certificates. Overlap with broad family theorems remains unresolved. |
| Qudit codes | Credit earlier near-endpoint constructions, support-removal methods and strengthened Hamming bounds | Full classification is for F_q-linear stabilizer codes; merely additive non-prime-field cases are separately scoped. |
| Cactus response | Separate the K4-minor obstruction to coherent coupling from the response conjecture itself | The cactus theorem proves a restricted case. Failure of the stronger coupling method is not a counterexample to the general conjecture. |

The remaining package records cover Johnson-solid certificates, Cartesian-tree words, special-octagon billiards, permutation races, integer tree weights, tournament rules and the shortened seven-cube proof. Internal adversarial reviews and exact replays support high correctness confidence within their stated models. Originality assessments remain bounded and are not publication-priority certificates.

The combined default Lean library passed its 26 October build and **153-declaration axiom audit**. All 153 audited declarations then passed the independent six-checker replay in hosted CI on 26 October ([replay record](verification/formal-library-20261026/ci-replay.json)). See [formal coverage](formal-coverage.md) for source hashes and theorem boundaries. One unfinished draft is not a reviewed result or a release item.

## Three-dimensional elasticity

The proposed proof resolves the generic-injectivity statement of Conjecture E in de Hoop, Ilmavirta, Lassas and Várilly-Alvarado, arXiv:2307.03312v2. An independent geometric audit checked the Borel fixed-point reduction, both normal-space bounds, the projective-slice argument, proper specialization and the final collision-incidence dimension estimate. No fatal gap was found. A separate arithmetic reconstruction agrees with the source construction.

The final proof uses **upper bounds** for two determinantal dimensions. Eleven explicit identities in the original minors certify those bounds; a standard-library rational checker verifies every coefficient. Complete Gröbner computations in two orders remain optional corroboration. The default verifier also confirms that the saved minor matrix equals the matrix reconstructed from the elasticity tensor. This avoids treating a correct calculation on an unrelated matrix as evidence for the theorem.

The stronger conclusion uses 22 scalar invariants and gives fifteen explicit measurement directions. Neither number is claimed optimal. The theorem concerns density-normalized stiffness, generic uniqueness and ideal phase wave kinematics. It does not identify density separately, remove known ambiguities on exceptional symmetry subfamilies, or supply numerical stability. The full geometric theorem is not formalized in Lean.

A bounded current-source search found no earlier resolution; priority remains provisional. The completed full-manuscript DeepResearch review found no fatal geometric gap conditional on the certificates. It independently reconstructed several ranks but did not replay the saved minor and slice identities. Its input was the seven-page draft, so this review does not cover the later eleven-direction extension. The separate minimal-direction report did not prove eight-direction global uniqueness; its suggestion that all-direction spectra contain more information than the slowness polynomial was rejected, since the homogeneous pieces recover the same characteristic coefficients. See the finding's [source audit](../physics/mechanics/elasticity/generic-stiffness-recovery/SOURCE_FACTCHECK.md) and [internal proof review](../physics/mechanics/elasticity/generic-stiffness-recovery/INTERNAL_REVIEW.md).

The subsequent review of the full eleven-direction draft completed on 18 October. It independently checked the incidence counts and geometric deductions and found no new proof defect. It did not replay the complete saved certificates, which remain supported by the local exact checks and separately scoped Lean runs. Additional prior art concerns full acoustic tensors, restricted symmetry classes or a different inverse problem; the Aristégui-Baste full-text comparison remains open.

## Truncated-dodecahedron rigidity

The source paper, Adrian-Himmelmann, Winter and Zhang, [arXiv:2607.09252](https://arxiv.org/abs/2607.09252), explicitly leaves this classical solid unresolved under its fixed-edge and flat-face model. Independent exact geometry checks identify the saved realization as the uniform truncation of a regular dodecahedron, reconstruct all supporting facets, and verify that the six gauges are transverse to Euclidean motions.

The modular checker reconstructs the original quadratic equations and verifies a rank-272 Jacobian, four infinitesimal parameters, the vanishing quadratic obstruction, four cubic obstructions and four direct identities expressing each parameter's ninth power in their ideal. It uses only the Python standard library and no generator code or computer-algebra engine. Seven mutations independently test the source-normal, kernel, rank-dual, left-nullspace, quadratic-correction, cubic and final-identity checks. Both the original replay and the negative checks pass with Python assertions disabled.

Independent theoretical reviews checked formal elimination, the degree-33 Nakayama argument, and the open quasi-finite locus along the actual integral zero section. The latter tracks the specified solid into characteristic zero without assuming flatness, properness or constant Jacobian rank. The two geometric implementations use opposite rotation conventions, giving gauge determinants +4 and -4; both certify the same nonzero transversality condition.

The result is local rigidity with original edges fixed and faces planar. It does not fix face shapes, assert rigidity of the bare bar graph, or prove global uniqueness among remote realizations. Exact arithmetic is independently replayed; the complete theorem is not formalized in Lean. The completed focused DeepResearch audit supports the proof and source-model interpretation. It independently constructed modular obstructions, but did not replay the saved certificates. Its bounded search found no earlier resolution; that is not a proof of priority. See the finding's source and theory audits for the checked argument.

## Hales-Jewett

Independent algebraic review and exhaustive finite verification agree with the prime-successor construction. The focused DeepResearch review found no proof error or exact collision within the inspected sources. The modular seed and the known prime-alphabet result are attributed to prior work. No claim is made that failed searching establishes priority.

The geometric-number consequence uses the source's reported G(8,2)=7. The collection does not independently certify that geometric computation. The off-diagonal definition uses consecutive alphabet values; it must not be confused with diagonal Hales-Jewett numbers or arbitrary pairs along a line.

## Lotka-Volterra

The result concerns generic members of the tree families, not all exceptional parameter specializations. Its recovered tree describes supports of Darboux polynomials, not an observed ecological interaction network. The June 2026 follow-up paper inspected during the review does not provide this reconstruction proof.

The focused review then found a material priority collision: Zijian Zeng, [*WITHDRAWN: Generic Lotka-Volterra Tree Systems Determine Their Trees*](https://doi.org/10.2139/ssrn.7379198), written 27 August and posted 2 September 2026. The primary SSRN record was independently retrieved. Its current abstract is a withdrawal notice, and the page reports no downloadable manuscript. The title and keywords overlap substantially, but precise theorem hypotheses and proof methods cannot be compared without the missing text. The collection makes no priority claim for the LV result and presents a self-contained reconstruction and verification note. The earlier announcement is cited prominently; its withdrawal is not treated as permission to disregard it.

## Restart

The generic positive-kernel inequality is established machinery, with a directly matching ratio-gap expression in Dávila and Topp, JFA 284 (2023), 109885, Lemma 4.3. The paper cites this explicitly. Evans and Ray already introduced the conjugate prescription and the exponential pair. The proposed additions are the global and unique renewal-law conclusion and the finite-state converse under cyclicity.

Several generated-review suggestions were rejected after independent checking:

- Exponential damping of the weighted reciprocal-time measure is valid and supplies a finite measure for Laplace uniqueness without an extra moment assumption.
- The general Green-representation defect is the eventual escape probability, not survival to a finite restart time. A one-state killed chain disproves the report's alternative formula.
- The large-rate success-vector resolvent expansion has no constant term.
- The Donsker-Varadhan occupation functional is relevant to the kernel algebra; it is not restricted to the eigenvalue characterization discussed in the report.

The current theorem is confined to one-dimensional Brownian search and stable finite killed chains. No claim of waiting-law uniqueness is made for finite state spaces. No adaptive or costly restart optimum is claimed.

## Periodic waiting-time entropy inference

The counterexample uses event-conditioned phases, not uniform phases: after an observed 12 event the phase density is a(t)/(2*pi), and after 32 it is b(t)/(2*pi). Independent exact Fourier arithmetic confirms the derivative difference epsilon squared. Equal event rates normalize the full estimator as 4/3 times a KL divergence; the written audit checks reverse-closed support, exponential tails and finite integrability.

The completed focused report supports the literal conjecture counterexample. Its ancillary claim that phase-resolved conditional densities agree pointwise under protocol reversal was rejected: the initial and final event-rate factors differ. Event-weighted joint densities obey the relevant relation. That incorrect auxiliary statement is not used in the paper. Its numerical extensions were not accepted without validation.

Primary-source checks distinguish the forward-only conjecture from the source theorem and Harunari et al.'s reversed-protocol estimator. Existing equilibrium waiting-time false positives are credited to Hartich and Godec. The specific counterexample is analytically checked, not Lean-formalized; priority remains provisional.

## Cubic-source equilibrium counts

Independent written reviews confirm the all-n construction: the source matrix is invertible; the interpolation polynomial has exactly n simple positive roots; all reaction products are nonnegative integral complexes; the complete equilibrium curve meets the chosen class transversely. The published quadratic obstruction covers n ≥ 3 and separately excludes two equilibria for n = 2.

The two exact checkers validate 35 equilibria for n = 2 through 8. The independent checker reconstructs the reaction vector field and differentiated Jacobian using rational arithmetic, and rejects modified products, rates and equilibrium points. This finite replay corroborates the formulas; it is not the all-n proof. Persistence uses Descartes' rule to exclude additional roots, including degenerate ones, rather than incorrectly applying an upper bound only on nondegenerate equilibria.

The classes are unbounded, product molecularity is not restricted to three, and stability is unproved. Local correctness reviews pass. The dedicated DeepResearch review has completed and its recommendations were independently assessed. Prior attainment at n = 2 is now credited explicitly. Its two incorrect suggestions about the published quadratic exclusion and the identity of that example were rejected after comparison with the primary source. No exact earlier all-n construction was found in the bounded search; external specialist review and final priority assessment remain open.

## External review

Independent agents, generated adversarial reports, exact computation, and Lean are complementary checks. None is described here as external specialist or journal peer review. Formal correctness also does not establish novelty, scientific importance, or publication priority.
