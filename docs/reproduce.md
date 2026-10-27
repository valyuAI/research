# Reproducing the collection

## Formal proofs

Install the official [elan toolchain manager](https://github.com/leanprover/elan). The `formal/lean-toolchain` file selects Lean v4.35.0; `lake-manifest.json` pins every dependency revision.

```bash
cd formal
lake exe cache get
lake build
lake env lean Audit.lean
```

On Linux with `bubblewrap`, additionally run:

```bash
bash replay-proofs.sh /absolute/path/to/diagnostics
```

This audits every project theorem, exports their complete proof dependencies, and replays them with the toolchain's kernel and all bundled independent checkers. Export and replay are sandboxed; nonstandard axioms are rejected. A successful build alone is not described as completion of this separate replay check. See the [coverage ledger](formal-coverage.md) for completed commands and precise scope.

The selected release includes the fix for CVE-2026-72844: upstream commit `a39eab69e1eee9ad38f4efe507907b1026a77808` is an ancestor of v4.35.0. The dependency search and version selection were checked on 17 October 2026.

## Papers

The papers use AMS-LaTeX, BibTeX, Latin Modern, and microtype, available in a standard TeX Live or MacTeX installation. Each retained paper directory contains a build script. Some also produce an alternate sole-author presentation (`journal.pdf`) from the same mathematical source. The [collection index](collection.md) links every paper's verification instructions; requirements and the meaning of quick/full modes differ across packages.

## Computational evidence

The truncated-dodecahedron certificate has a Python standard-library checker. From its [paper directory](../maths/geometry/rigidity/truncated-dodecahedron/), run `python3 -B -O verification/independent_verification.py`. It reconstructs the exact solid and its equations, then checks the modular rank, quadratic correction, cubic obstructions and four polynomial identities proving isolation. Deliberately corrupted certificates are tested separately. The written local-algebra and specialization argument connects those identities to real rigidity; that argument is not Lean-formalized.

The elasticity verifier reconstructs the Christoffel map, its trace kernel, two normal quotients and the symmetry actions using exact arithmetic. It checks eleven explicit minor identities and complete finite-field slice certificates. It also reconstructs the eleven-direction cubic slice on full unisolvent grids and checks eleven direct ideal-membership identities proving that slice is empty in projective space. Run `python3 verification/verify_all.py` from the elasticity paper directory. Python and SymPy 1.14.0 are sufficient; Singular is optional. The [certificate instructions](../physics/mechanics/elasticity/generic-stiffness-recovery/verification/README.md) distinguish arithmetic verification from the written geometric proof.

The independent Hales-Jewett verifier enumerates the full cube and every nonempty wildcard word. It checks the compact coloring against the saved finite certificate and tests both forbidden configurations.

The Lotka-Volterra checker uses exact integer and rational arithmetic to test dependent triples, reconstruction, and complete linear supports at explicit generic parameters. Its finite enumeration is a consistency check, not the all-order proof.

The restart checker combines exact rational matrix arithmetic with an independent numerical quadrature check. The rational counterexample is exact; quadrature is reported with its numerical tolerances. Neither is used as a substitute for the analytic theorem.

The periodic waiting-time counterexample uses a standard-library rational Fourier-polynomial checker. From its paper directory, run `python3 -B -O verification/check_short_lag.py`. It checks six exact identities, including the positive derivative difference. The probability normalization, strict KL positivity and finiteness are written proofs, not claims made by the polynomial checker.

The cubic reaction-network family has two exact checkers. From its [paper directory](../chemistry/reaction-networks/mass-action/cubic-equilibrium-sharpness/), run `python3 -B verification/verify_cubic_sharpness.py` (SymPy 1.14.0) and `python3 -B -O verification/independent_cubic_check.py` (standard library only). The independent checker reconstructs the actual reaction equations and Jacobian from the retained complexes and rates, validates 35 equilibria, and rejects three corrupted inputs. The all-n interpolation and transversality proof remains a written argument.

Exact commands and requirements accompany each verification directory.

## The 25-26 October packages

Start with the [collection index](collection.md), then read the chosen package's README, verification instructions and `build.sh`. Do not substitute a quick check for a documented full replay. Some expensive enumerations and proof checks were completed earlier in the campaign and recovered from logs and source hashes instead of rerun during integration; the package records distinguish fresh execution from recovered evidence.

The new checkers use a mixture of standard-library Python, compiled C/C++, exact arithmetic libraries, SAT proof checking and Lean. There is no single dependency-free command that replays all packages. In particular, the algebra package keeps its large optional DRAT proof in the research archive but includes independent exhaustive checks; the quartet package supplies a fresh exhaustive proof that does not depend on the historical SAT proof files. Numerical illustrations are labelled separately from exact proof certificates.

## Narrated explainers

Each completed `video/` folder contains a playable MP4, editable scenes, narration, retained audio and subtitles. Follow its README and the shared [video toolkit](../tools/video/README.md) to rebuild. Regenerating narration uses the configured speech service; ordinary rendering can reuse the retained clips. Render intermediates are excluded from version control. A completed video has metadata, decode, timing and frame-inspection evidence; no listening review is claimed.

The per-package `run_stage.py`, `build.py` and packaging scripts locate the repository from their own path. Set `VIDEO_PYTHON` to an interpreter with the toolkit requirements (the README commands default to `python3`). Final renders serialize on an advisory lock at `$VIDEO_RENDER_LOCK`, by default `/tmp/valyu-research-final-render.lock`. Set `VIDEO_STATUS_FILE` to mirror progress to a Markdown file; otherwise progress is printed and kept in the folder's state file.

## Historical records and public copies

Historical run records and hash manifests describe the files used for the recorded checks. Public copies may replace machine-specific paths and research-task identifiers with stable labels. The [path-redaction record](../public-release/path-redactions.json) records each transformed file's original and public hashes; the [release-change record](../public-release/release-changes.json) describes other edits, and the [export exclusions](../public-release/export-exclusions.json) record omitted files. These changes do not represent new executions of the recorded checks.

Placeholders such as `<repo>/`, `<private-archive>/` and `<texmf-home>/` identify the original checkout, unpublished working archive and local TeX installation. They are provenance labels, not reproduction commands. Follow the repository-relative commands in each package instead. A historical hash continues to identify the original file, including an earlier PDF presentation, rather than a later public copy.
