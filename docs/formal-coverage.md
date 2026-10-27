# Formal verification coverage

The expanded default library was rebuilt on **26 October 2026**. Its axiom audit passed for **153 project declarations (96 named theorems and 57 generated helpers)** across seven mathematical modules. The retained [build, audit and source hashes](verification/formal-library-20261026/manifest.json) record that local run. The independent six-checker replay of all **153** audited declarations then passed in hosted Linux CI on 26 October (runs `40373907951` and `40373880188`, commit `07467db`); the [retained replay record](verification/formal-library-20261026/ci-replay.json) gives the checker results and export hash. The earlier 17 October replay covered the 121-declaration library. The separate determinant package passed on 18 October. All use Lean **v4.35.0** and mathlib **v4.35.0**, commit `56a005855ea17e0b0958f73ec801ae140b0a1679`. The committed Lake manifest fixes all dependency revisions.

## What is proved

| Paper | Checked Lean scope | Outside the formalization |
|---|---|---|
| Hales-Jewett | **Complete prime-successor theorem**, on actual finite cubes: explicit coloring, general lower bound, universal upper bound, least forced dimension, HJ(8,2)=8 and HJ(12,2)=12 | Publication priority; the cited geometric number G(8,2) |
| Lotka-Volterra | Exact algebraic obstruction along a three-vertex path | Support connectivity, complete Darboux support classification, dependent triples, tree reconstruction and the full generic equivalence theorem |
| Restart | Finite real symmetric-kernel gap identity and global minimum; exact rational three-state counterexample | Brownian Green representation and measure-theoretic uniqueness; Markov semigroup interpretation; the cyclicity converse |
| Elasticity | Seven matrix lemmas, including the characteristic-coefficient collision reduction; eleven original minor determinant identities in a separate package | Tensor assembly, normal quotients, finite-field slice arguments, initial-ideal dimension bounds and the full generic recovery theorem |
| Chemical robustness and multistability | Two reaction lists, their vector fields, complete positive steady-state lists and ACR | Stability, the dimension-two obstruction and minimum dimension/complex/species counts |
| Cubic tic-tac-toe | Abstract replication-to-surplus, matching after deletions and the necessary cell-count inequality | Enumeration of actual boards, verification of replication hypotheses and game conclusions |
| Common quartets | Sharp real-variable potential inequality and an equality witness | Trees, separating edges, iteration, finite certificates and the values or bounds for h(k) |
| Truncated dodecahedron | None | Exact certificate replay is performed in Python; the local algebra, specialization and complete rigidity theorem are written proofs |

Other findings in the [collection index](collection.md) have no Lean formalization in this repository. Their exact checkers and written proofs are separate evidence.

### Hales-Jewett

Source: [`HalesJewett.lean`](../formal/ValyuResearch/HalesJewett.lean), namespace `ValyuResearch.HalesJewett`.

- `prime_coloring_avoids_of_le`: for every prime p<k and every n≤p, the stated coordinate-sum coloring avoids both forbidden configurations on `(Fin k)^n`.
- `prime_lower_bound`: p+1≤HJ(k) whenever p is prime and p<k.
- `forces_self` and `HJ_le_self`: every coloring in dimension k has a forbidden configuration, hence HJ(k)≤k for k≥2. The upper bound is proved locally, not assumed.
- `HJ_prime_successor`: HJ(p+1)=p+1 for every prime p.
- `HJ_eight` and `HJ_twelve`: the exact instances 8 and 12, with primality checked by kernel-reduced `decide`.

`Word k n` means `Fin n → Fin k`. A full line replaces a nonempty coordinate set by one common letter. The blue obstruction uses adjacent natural letter values, with no wraparound. `HJ` is the least forced dimension, using `Nat.find` and the proved upper bound; its convenience value for k<2 is outside the paper's domain. An [independent semantic review](hales-jewett-formal-review.md) checked that these definitions match the paper.

### Lotka-Volterra

Source: [`LotkaVolterra.lean`](../formal/ValyuResearch/LotkaVolterra.lean), namespace `ValyuResearch.LotkaVolterra`.

The four named lemmas are `path_cancellation`, `path_forces_middle_sum`, `no_path_coefficients`, and `positive_off_diagonal_no_path_coefficients`. They establish the polynomial cancellation and contradiction used to exclude a three-vertex path from a larger Darboux support under the stated nonvanishing conditions. The surrounding graph and dynamical arguments remain written proofs.

### Restart

Source: [`Resetting.lean`](../formal/ValyuResearch/Resetting.lean), namespace `ValyuResearch.Resetting`.

`kernel_gap_identity`, `kernel_gap_nonnegative`, `kernel_self_cost`, and `kernel_global_minimum` prove the finite symmetric-kernel optimization argument for positive real vectors and an entrywise nonnegative symmetric kernel. These are finite sums, not a formalization of the paper's infinite integrals.

The rational certificate checks the Green inverse, both resolvent equations, success identities, normalized squared-success weights and exact costs. `example_strict_improvement` gives the exact negative difference; `example_competitor_better` proves strict improvement. The translation from resolvent equations to exponential renewal laws is explained in the paper, not formalized as probability semantics.

### Elasticity

Source: [`Elasticity.lean`](../formal/ValyuResearch/Elasticity.lean), namespace `ValyuResearch.ExploratoryElasticity`.

The seven named results prove the second-coefficient difference, determinant difference, characteristic expansion, trace collision, quadratic collision, cubic collision and the full coefficient-collision equivalence. They hold for arbitrary 3 by 3 matrices over characteristic-zero fields, so they apply pointwise to Christoffel matrices. The generic-injectivity theorem remains a written geometric proof supported by exact arithmetic certificates. It is not described as fully Lean-verified.

### Chemical robustness and multistability

Source: [`AcrMultistability.lean`](../formal/ValyuResearch/AcrMultistability.lean), namespace `ValyuResearch.AcrMultistability`.

`ex1_field` and `ex2_field` derive the polynomial vector fields from the encoded reaction lists. `ex1_steady_states` and `ex2_steady_states` characterize all positive steady states, and `ex1_acr` and `ex2_acr` show that the first species has concentration one at every positive steady state. These statements do not assert stability or convergence. The Routh-Hurwitz checks and general lower-bound proofs remain outside Lean.

### Cubic tic-tac-toe

Source: [`CubicTicTacToe.lean`](../formal/ValyuResearch/CubicTicTacToe.lean), namespace `CubicTicTacToe`.

`surplus_of_replication` derives a Hall-type surplus from an abstract replication hypothesis. `matching_avoiding` and `pairing_of_replication` produce a matching after a bounded set of cells is deleted. `pairing_needs_cells` gives the necessary inequality that twice the number of lines cannot exceed the available cells. No concrete cubic board or finite search is encoded here. In particular, these lemmas neither settle the six-cube game nor independently certify the seven-cube enumeration.

### Common quartets

Source: [`CommonQuartetPotential.lean`](../formal/ValyuResearch/CommonQuartetPotential.lean), namespace `ValyuResearch.CommonQuartet`.

For the potential `psi(a,d) = min(ad, 2a², 2d²)`, `potential_step_sharp` proves the factor `(7 - sqrt(13))/18` under the stated split and ordering hypotheses. `potential_step_sharp_witness` proves equality for the explicit real inputs. The sharpness claim concerns this real-variable inequality; it is not a claim that the resulting tree strategy or exponential base is optimal. The earlier factor `3/16` remains available as `potential_step`. Translating the inequality into the bound for h(k), and the separate proof of h(3)=14, require arguments and certificates outside this formalization.

## Verification boundary

Completed locally on macOS:

```bash
cd formal
lake build
lake env lean Audit.lean
```

The 26 October build passed for all **seven mathematical modules**. Lean emitted only module-system migration notices. The automated audit enumerated all **153 project declarations (96 named theorems and 57 generated helpers)**, including generated helpers, and checked their transitive axiom dependencies. Selection uses the declaration's owning module as well as its namespace, so private project declarations are included. Every dependency belongs to the allowlist `propext`, `Classical.choice`, `Quot.sound`. No admitted proof, custom axiom, or compiler-trusted decision axiom occurs. See the complete [axiom audit](verification/formal-library-20261026/axiom-audit.log) and [build log](verification/formal-library-20261026/build.log).

`Audit.lean` fails on unexpected axioms and refuses an empty theorem collection. This is an axiom audit and an ordinary Lean build. It is separate from the stronger export-and-replay check on Linux:

```bash
bash replay-proofs.sh /absolute/path/to/diagnostics
```

The script exports every audited theorem and its full transitive proof dependencies with the official `leanexport` tool, then runs all six bundled checkers using `lake check --from-export ... --paranoid`. Both export and replay are sandboxed. It checks the exported root list against the completed audit count, rejects duplicates, and retains the names and export hash. This excludes unrelated imported theorems from the export without omitting any project proof dependency. The broader `lake check --paranoid` command remains available but exports every declaration in scope, including unrelated imported mathematics.

The complete six-checker replay **passed** in Linux CI on 17 October 2026, in run `39072477795` for commit `368f61c6e4dc3fa23f304cfd65578423231bf200`. All 121 project theorem roots in that version and their proof dependencies were exported. Lean paranoid, lean4lean, nanoda, con-leche, con-ron and Lean default each reported acceptance. The export and all checkers ran with `bubblewrap`; this Linux-only sandbox is not bypassed on macOS.

The expanded library's six-checker replay **passed** in Linux CI on 26 October 2026, in runs `40373907951` (pull request) and `40373880188` (push) for commit `07467db1a6fd9ac583831bb4a430a9f481e74832`. Both exported all 153 audited declarations and their proof dependencies to byte-identical exports, SHA-256 `6497252b58050ff8873e62a2a46408405fb95df04f121e7bdfd564b073cd506b`. Lean paranoid, lean4lean, nanoda, con-leche, con-ron and Lean default each reported acceptance. The CI axiom audit is byte-identical to the retained local audit. The [replay record](verification/formal-library-20261026/ci-replay.json) and the [retained checker log and theorem list](verification/formal-library-20261026/ci-replay-40373907951/) preserve this evidence beyond the expiry of the Actions artifacts. The local [build manifest](verification/formal-library-20261026/manifest.json) predates these runs and is unchanged. This replay covers the shared formal library only; it does not formalize the papers' other claims.

Formal checking establishes the encoded mathematical propositions relative to the toolchain and foundational axioms. It does not certify the bibliography, publication priority, or claims outside the scopes above.

## Additional determinant certificates

A separate [package](../physics/mechanics/elasticity/generic-stiffness-recovery/verification/lean-certificate-checks/) formalizes eleven exact minor identities used in the elasticity dimension bounds. Its source translation independently matches all 91 matrix entries, eleven target polynomials and 237 minor definitions in the rational certificate.

The successful 18 October CI run `39114539272`, on commit `351b43b71bb22f3e36cfc7f585729a522891f9a4`, compiled all 24 modules, including the final quintic certificate, and completed the axiom audit. All eleven named certificate theorems and all 4,224 owned theorem declarations, including generated auxiliaries, depend only on `propext`, `Classical.choice`, and `Quot.sound`. Compilation and audit took about 26 minutes 31 seconds. The six independent proof checkers were not run on this additional package.

The previous run, `39112686026`, compiled ten identities, then hit the 6 GB memory guard on the quintic batch without a reported Lean proof error. Dividing the two pending batches into smaller modules preserved all 88 declaration and proof texts and retained the same resource limits. The successful run establishes the determinant identities and their audited axioms, not the full initial-ideal dimension argument or geometric elasticity theorem. This package remains outside the default formal library and outside the completed 121-theorem independent-checker replay.

## Linux CI execution record

The runs in this section and the 18 October determinant run were executed in the project's earlier CI before this collection was published. Their hosted pages are not public, and their logs are not retained in this repository; the run numbers and commits are recorded for traceability only. The retained public receipt for the shared formal library is the 26 October [replay record](verification/formal-library-20261026/ci-replay.json) with its [checker log and theorem list](verification/formal-library-20261026/ci-replay-40373907951/). The determinant package can be rerun with its [local runner](../physics/mechanics/elasticity/generic-stiffness-recovery/verification/lean-certificate-checks/) or the manual `lean-certificates.yml` workflow.

The successful run, `39072477795`, passed the build, 121-theorem axiom audit and all six replay checkers. Its logs record 11,684 checked declarations in the dependency export. The workflow retained the theorem inventory, export hash, checker logs and resource diagnostics as artifact `proof-replay-diagnostics` (ID `12115489132`). The earlier attempts below explain the sandbox and resource changes that preceded this pass.

The initial run, `39065926821`, on source commit `420a5733ce42b516f8065964913fcbe12774a6eb`, passed the Linux Lean build and the all-project axiom audit. The independent replay stopped before proof checking with `bwrap: setting up uid map: Permission denied` on Ubuntu 24.04. This is a sandbox initialization failure, not a proof rejection. The retry changed the runner environment and retained the sandbox.

The Ubuntu 22.04 run, `39066462522`, on commit `b8288e833f1ba2ff8d1f80bb7d4f737b0d21ff85`, again passed the build and the **111-declaration axiom audit**. Its replay step failed and the run later finalized as cancelled. Its detailed logs remained unavailable. The mathematical sources were unchanged between these two runs.

The diagnostic run, `39070100688`, on commit `9c6b85c1c58a919ea2e49f25c1eeff872b27fe7c`, exported 243,971 declarations. **Lean paranoid and lean4lean accepted the export.** During nanoda, recorded resident memory reached about 7.2 GB on an 8 GB runner, with about 1.6 GB of swap used; the job then terminated with exit code 143. This documents severe memory pressure and termination, not a reported mathematical rejection. The complete six-checker replay did not finish. The current workflow narrows the export to every project theorem and its dependencies to address that resource problem.
