# Research readiness: ACR with multistability

Status: complete research package, ready for narrated video production and campaign integration. The full build passed, both example checkers now certify stability exactly, and all eight final PDF pages were visually inspected.

## Retained claims

For at-most-bimolecular mass-action systems with absolute concentration robustness (ACR) and multistability, the minimum stoichiometric dimension is **3**, the minimum number of complexes is **6**, and the minimum number of species is **3**. The two coupled examples attain these bounds where stated.

The main theorem is the dimension-two obstruction: if a class contains two distinct nondegenerate positive steady states, these are its only positive steady states and at least one has a positive real eigenvalue. The six-complex lower bound combines this with Feinberg's deficiency one theorem. The minimum number of reactant complexes is still between 4 and 6; with three species it is between 5 and 6. Four reactant complexes would need at least five species. The minimum number of reactions remains open.

The three-species counterexample to the corresponding part of the KNS conjecture is already available by a trivial decoupled construction. This is disclosed in the abstract, table and discussion. The substantive new-result candidates are the dimension-two obstruction, exact dimension/complex minima and explicit coupled examples. Correctness confidence: high. Originality confidence: moderate to moderate-high for the structural results, moderate for the examples; the priority search is bounded.

## Review response

Original reports are preserved in `verification/reviews/`.

- `chem-acr-priority`, `DR-033`: no earlier resolution found in retrieved sources. Citation-graph coverage is incomplete.
- `chem-acr-review`, `DR-035`: reviewed the complete dimension-two case analysis and found no failing step. Its notation, density argument, stronger instability conclusion and prior-attribution requests are addressed.
- `chem-acr-final-review`, `DR-049`: checked the complex bound, four-reactant proposition, examples and decoupled remark. It could not recheck the main case analysis because that part was omitted from its prompt; the full proof is present in the paper and was covered by the earlier review. This is a limitation of that review's coverage, not a new proof certificate. The three-species table row now explicitly restricts to dimension three, the trivial species construction is prominent, and the four-reactant argument has a complete hand proof.

The reviewers' calculations are recorded as reasoning unless they explicitly report execution. No external peer review or publication-priority guarantee is claimed.

## Replay and exact evidence

`PATH=$HOME/.elan/bin:$PATH nice -n 10 sh build.sh` completed with exit 0 on 26 October 2026, with SymPy and Lean available. The root wrapper checked both dependencies before running the build and emitted progress. Logs are preserved in `verification/results/resume-build-20261026.log` and the individual verification logs.

- Standard-library checker reconstructs both coupled networks and the decoupled example, their exact steady states, characteristic polynomials and stability. Every example has two stable states and one state with a positive real eigenvalue.
- Independent SymPy checker reconstructs the fields from text reaction lists and saturates the steady-state ideal away from the coordinate hyperplanes. It now checks positivity symbolically, the exact claimed state lists, all network counts, and stability using exact cubic Routh-Hurwitz inequalities. Negative constant coefficients certify the unstable states without numerical eigenvalue signs.
- The four-reactant enumeration examines all 1,365 complex sets: 195 have rank below three; 248 rank-three cases have no zero kernel coordinate; 688 have a zero coordinate and two distinct kernel values; 234 have a zero coordinate and three values. The separate nullspace implementation reproduces the 922 qualifying cases and maximum three values.
- Four controls reject a zero rate, a trimolecular complex, a nonhyperbolic cubic and an unstable positive-coefficient cubic that lacks the claimed certificate. Positive controls accept the expected stable and positive-real-root cases. Results: `verification/results/negative-controls-20261026.json`.
- Final LaTeX passes have no warnings, overfull boxes or undefined references. All eight pages were rendered at 110 dpi and inspected, including the repaired table and the complete dimension-two proof.

## Formal and biological scope

`formal/ValyuResearch/AcrMultistability.lean` compiles. It establishes the reaction-list vector fields, exact positive steady-state lists and ACR for the two coupled examples. It does not formalise their stability, the dimension-two theorem, the complex bound or the reactant-count argument.

ACR is a property of positive steady states. It does not guarantee convergence from every initial condition. Stability here is relative to the stoichiometric class; zero eigenvalues caused by conservation laws are not counted as strict contraction. Both reactant and product complexes have at most two molecules. These are mathematical networks, not experimentally demonstrated chemical devices.

## Optional searches

The two five-reactant random searches and the Tang-Zhang screening jobs are no longer running. The recovered Tang-Zhang logs end in DONE: the limited linear-identity screen reports 166 networks with a certificate among 375 parsed entries, and sampled rates produce no bistable ACR example. The paper reports 373 networks, so these parsed-entry counts are not treated as an audited classification count. Neither the restricted certificate screen nor random rate sampling proves absence or settles priority. The raw logs remain in the campaign lab; no theorem depends on them.

## Deliverables

[Paper](../../../../public-release/papers/acr-multistability-bounds.pdf), [source](paper.tex), [verification guide](verification/README.md), [video brief](video-brief.md). Earlier source, archival PDF and inspection hashes are in `verification/results/completion-manifest-20261026.json`; current public PDF hashes are in the [public manifest](../../../../public-release/papers/manifest.json). Video production and pre-commit simplification review remain separate campaign tasks.
