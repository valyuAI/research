# Physics and mechanics campaign

Started 17 October 2026. **Active research, not a list of discoveries.**

The objective is significant, defensible findings. Scientific importance is assessed separately from how easily a result can be explained or demonstrated.

## Research briefs

Nineteen DeepResearch tasks were run with computation enabled. The first twelve explore fields in parallel; seven follow concrete mathematical questions and review drafts. They seek explicit unresolved claims, precise equations and assumptions, strong prior-art checks, and a calculation that can actually be attempted. No candidate qualifies merely because a generated report calls it novel.

| Field | Task |
|---|---|
| Inverse elasticity | `DR-016` |
| Rigidity prestress | `DR-038` |
| Origami multistability | `DR-045` |
| Dissipative wave physics | `DR-078` |
| Stochastic thermodynamics | `DR-001` |
| Topological mechanics | `DR-068` |
| Contact friction | `DR-050` |
| Active odd mechanics | `DR-021` |
| Hydrodynamics mixing | `DR-083` |
| Soft matter instability | `DR-051` |
| Passive wave bounds | `DR-034` |
| Thermal transport | `DR-069` |
| Minimal directions for elastic reconstruction | `DR-048` |
| Exact origami branch counts | `DR-084` |
| Optimal thermal series designs | `DR-077` |
| Full elasticity manuscript review | `DR-011` |
| Nonlinear contact-law exponent | `DR-060` |
| Truncated-dodecahedron proof review | `DR-093` |
| Periodic waiting-time counterexample | `DR-071` |

All nineteen tasks are terminal: sixteen completed and three failed. Topological mechanics, active odd mechanics and hydrodynamics did not complete; they are not counted as completed research or as scientific rejections. All seven focused follow-ups completed; their conclusions were checked against the actual mathematics.

## Findings and live questions

The [elasticity proof](../../physics/mechanics/elasticity/generic-stiffness-recovery/) has passed independent internal mathematical and exact-arithmetic checks. The primary paper and current related work were read directly; coding agents running locally produced the proof. The completed initial DeepResearch report reviewed literature and an early proof summary, but did not replay the exact certificates. A separate completed review supports the seven-page manuscript conditional on its exact certificates. It did not replay those certificates or review the later eleven-direction extension.

The finite-direction question is sharper: a dimension count rules out generic recovery from seven directions, while exact certificates and an incidence argument now give eleven generic directions. The earlier fifteen explicit directions remain a separate constructive result. Whether eight, nine or ten generic directions suffice is unresolved. A full-rank numerical Jacobian would establish only local identifiability and will not be presented as a global uniqueness proof.

The [truncated-dodecahedron proof](../../maths/geometry/rigidity/truncated-dodecahedron/) settles the specific classical solid left open by the cited July second-order analysis. Exact polynomial identities over a finite field prove isolation, and an integral zero-section argument transfers it to the real solid. A separate checker reconstructs the geometry and every identity without importing the generator. The result has passed independent arithmetic and theoretical review; the completed focused review found no earlier resolution within its bounded search. Priority remains provisional.

A separate two-mode damping draft has a checked mathematical argument, but unresolved overlap with classical optimization literature. It remains exploratory.

Two further drafts have concrete mathematical content:

- **Thermal series design.** An exact comparison argument selects the optimal sequence from a finite library of materials with piecewise-constant conductivity. A three-material example needs four layers in the order A, B, A, C. The proof and 47 reconstructed designs have been independently checked; overlap with the original 2019 graded-material optimization paper is not yet cleared.
- **Nonlinear contact laws.** In an explicitly defined reduced three-cylinder spring model, the static floor-slip branch has critical stiffness exponent `1/(p+1)` when normal and tangential forces have common homogeneity `p`. The derivation, linear-law limit and 48 high-precision primitive-equation checks pass. This is not yet a result about dynamic failure or a full Hertz-Mindlin model; the completed review supports that model-level calculation but does not establish originality.

A further [periodic waiting-time counterexample](../../physics/statistical-physics/thermodynamic-inference/periodic-waiting-time/) disproves a specific conjectured entropy upper bound with three states and smooth symmetric rates. Its analytic proof, exact derivative identities and source interpretation passed independent local review. Earlier waiting-time false positives are explicitly credited; this is a targeted correction, not a general new thermodynamic principle.

Negative checks also matter. Exact origami computations with two, four and five interior vertices agreed with the existing branch-count conjecture; six-vertex computations timed out. A proposed broad curvature obstruction from a report was disproved by an explicit embedded tube patch, but that does not contradict the source paper's narrower prescribed-metric problem. Neither exercise is represented as a new discovery.

## Promotion standard

A candidate must survive independent reading of the primary source, an explicit prior-art search, and direct mathematical or computational testing. Physical models must satisfy their stated stability, passivity, boundary and dimensional assumptions. Finite numerical evidence does not establish a general theorem. A contradiction must target what the source actually claims.

The leading candidates are investigated locally alongside the reports. Their status and disposition will be recorded before they appear among the repository's findings. A correction based on a known mechanism may be worth retaining, but is not promoted as a major new physical discovery.

No outreach, public announcement or submission was part of this campaign.
