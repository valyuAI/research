# Evidence and scope

Read locally on 26 October 2026. `source-snapshot.json` records accepted scientific input hashes. This video uses existing primary-source receipts, manuscript and exact verification records; no new web research was necessary.

| Beats | Claim / example | Evidence |
|---|---|---|
| t01-t04 | Maker-Breaker rules; the actual 5x5 twelve-pair defence | `../paper.tex`, sections1-2; `../video-brief.md` section3; all lines and pair disjointness rechecked in `check_examples.py` |
| t05-t10 | Cube lines 193; 343 cells; pairs as slot matching; Hall condition | `../paper.tex` sections1-2; direct line generator in `scenes.py`; production arithmetic checks |
| t11-t15 | Minimum over every nonempty group; deletion robustness; replication test | `../paper.tex`, Lemma `lem:surplus`; `formal/ValyuResearch/CubicTicTacToe.lean` at repository root; classical Hall and Lovasz-Plummer references |
| t16-t21 | Central greedy rule, 27 lines, 10627 leaves /14 sets; complete1296 histogram | `../verification/independent_check.md`; `../verification/independent/claim1_2.out`; `../verification/results/surplus_c_centre.txt` |
| t22-t24 | 12 partners; 48960 legal noncentral configurations all exact surplus3; two24480 shards;1158 classes | `../paper.tex`, Proposition `prop:noncentre`; `../verification/independent_check.md`, raw and class outputs |
| t25-t28 | Known2025 theorem; opposite octant omission;2916 unordered/5832 ordered pairs; exact game example | `../paper.tex` section `sec:gap`; `../verification/independent/claim5.out`; original arXiv:2509.21494v1 section4.3 as recorded by coordinator |
| t29-t34 | Six-cube counting obstruction; surplus cap4; precise Lean scope; open cases | `../paper.tex` sections `sec:six` and reproduction; `../verification/results/obstruction6.json`; `../verification/independent_check.md` |

The central histogram is `(lines met, surplus, count)`: `(27,>=4,576)`, `(26,>=4,288)`, `(25,2,384)`, `(22,no pairing,48)`. The first two are capped lower bounds, never exact-four assertions. The independent raw noncentral runs each checked 24,480 configurations and returned exact3 (cap4); total48,960. The additional class run has1,158 classes. The10,627-leaf tree leads to14 distinct sets. A class or configuration requires multiple matching computations, so the video does not call1,224 the number of individual matching tests.

The contribution is a new short computer-assisted proof/correction of the known7x7x7 result of Cain-Raymond-Kallersjo (2025). It does not solve5x5x5 or6x6x6. Opposite-octant criticism concerns the published text; unseen noncentral code is not assessed. The root hardened failure propagation in runners without changing matching algorithms. No expensive research matching run was duplicated during production.

Lean proves abstract Hall replication, surplus, deletion matching and the counting obstruction. It does not formalize the actual board enumeration, opening pattern tree or whole game. The paper connects the exact computations to the game. The5x5 pairing, all cube lines, displayed greedy central example, noncentral partner count, and counterexample coordinates are independently checked as production assets.

Teaching simplifications: the small matching graphs are labelled illustrations. The displayed central path chooses legal moves with no later Maker diagonal obstruction; the separate accepted pattern-tree certificate supplies universality. The projected cube is a two-dimensional drawing of exact3D coordinates. Wording remains Maker-Breaker throughout; the ordinary-game draw needs the standard additional strategy-stealing argument, which is omitted rather than conflated.

Correctness confidence is high for the accepted certificate; originality confidence for this surplus application is moderate and bounded by sources inspected. Private production: Cedar synthetic voice; no listening review, upload, contact or public action occurred.

## Canonical reference metadata

- John W. Cain, Ioannis M. Raymond and Nora C. Källersjö, *Cubic tic-tac-toe: A matching-based approach* (2025), [arXiv2509.21494](https://arxiv.org/abs/2509.21494), accepted package version1. Known seven-cube result, pairing example and the noncentral written case analysis.
- John W. Cain, [central-opening code archive](https://people.math.harvard.edu/~jcain2/tic-tac-toe-code.tar.gz) (2025), as cited in the accepted bibliography. It does not supply the unseen noncentral implementation discussed in the correction.
- Philip Hall, *On representatives of subsets*, Journal of the London Mathematical Society10 (1935),26-30. Matching criterion.
- László Lovász and Michael D. Plummer, *Matching Theory*, North-Holland (1986), Theorem1.3.6. Classical surplus characterization by replication.
- Alfred W. Hales and Robert I. Jewett, *Regularity and positional games*, Transactions of the American Mathematical Society106 (1963),222-229. Pairing background.
- Jos Uiterwijk, *Set Matching: An Enhancement of the Hales-Jewett Pairing Strategy* (2017), [arXiv1703.10678](https://arxiv.org/abs/1703.10678). Related strategy context, not a claimed six-cube resolution.

These are citation metadata from the accepted package, not newly retrieved texts. No raw responses, full third-party text or signed URLs are shipped.
