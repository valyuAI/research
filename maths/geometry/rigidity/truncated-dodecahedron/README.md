# Rigidity of the truncated dodecahedron

The classical truncated dodecahedron is locally rigid when its original edge lengths remain fixed and every original face remains planar. Faces may change shape; their diagonals are not fixed. Every sufficiently nearby allowed realization is congruent to the original solid.

Adrian-Himmelmann, Winter and Zhang leave this example unresolved in [*Deformations and second-order rigidity of polytopes*](https://arxiv.org/abs/2607.09252), Section 8.2. The present proof uses exact finite-field certificates and a specialization argument. Priority review is pending; this is a research draft, not an externally refereed publication.

[Paper](../../../../public-release/papers/truncated-dodecahedron.pdf) · [LaTeX](paper.tex) · [Written proof](proof.md) · [Mathematical review](review.md) · [Source and priority review](source-review.md)

[Readiness](readiness.md) · [Author proof walkthrough](author-walkthrough.md)

## Reproduce

From this directory, using Python 3 and its standard library:

```sh
python3 -B -O verification/independent_verification.py
python3 -B -O verification/negative_verification_checks.py
```

The first command independently reconstructs the exact geometry, verifies the transverse Euclidean gauges and modular rank, reconstructs the four cubic obstructions, and checks four explicit identities placing each variable's ninth power in their ideal. The second rejects seven deliberately corrupted inputs. Neither command runs a computer algebra system or relies on Python assertions.

The replay writes [its result and input hashes](verification/independent_verification.json); [the source audit](source-audit.md) explains what is checked. The supplied `.sing` file records the cubic forms and is parsed as data only. The discovery generator is unnecessary for verification.

Run `sh build.sh` to rebuild both PDFs with `pdflatex` and BibTeX, using the supplied diagram. The optional `--redraw-figure` flag also needs matplotlib. The illustration uses floating-point projection; the mathematical checks use exact arithmetic. The linked public PDF uses the human-author presentation and the current contribution statement. To rebuild it, run `python3 tools/public_papers.py build --only truncated-dodecahedron` from the repository root; `build.sh` reproduces the earlier manuscript presentations locally.

## Verification scope

The exact arithmetic certificate and written mathematical deductions are separate layers. Formal elimination and Nakayama's lemma give local isolation in characteristic 1009; openness of the quasi-finite locus transfers isolation along the actual zero-section to characteristic zero. The six transverse gauges then give rigidity modulo Euclidean motions.

This proof has **no Lean formalization**. Lean coverage elsewhere in this collection does not apply to it. The theorem concerns this specific solid with flat-face constraints; it does not assert global uniqueness or rigidity of its edge-only bar framework.
