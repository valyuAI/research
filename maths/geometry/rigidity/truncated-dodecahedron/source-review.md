# Source and priority review

Checked 17 October 2026 using Valyu Search and Contents. This record separates the source question from the new certificate and from the unresolved priority review.

## The original question

Matthias Adrian-Himmelmann, Martin Winter and Zhen Zhang, [*Deformations and second-order rigidity of polytopes*, arXiv:2607.09252](https://arxiv.org/abs/2607.09252), supplies the precise model and target. The retrieved arXiv record identifies version 1; its full text is available through [the primary HTML page](https://arxiv.org/html/2607.09252v1).

- Sections 2.2 and 2.3 describe normalized point-hyperplane realizations, fixed original edge lengths, and preserved facet coplanarity. They quotient by Euclidean isometries. This permits the shape of a polygonal face to change.
- Section 8.2 identifies the truncated dodecahedron as neither first-order nor second-order rigid and leaves actual rigidity undecided. It reports four first-order flex dimensions and vanishing of all the quadratic stress forms for this example.
- Appendix C.3 points to the authors' symbolic second-order computation. It is not a higher-order rigidity proof.

Cauchy's rigidity theorem for congruent rigid faces addresses a different constraint system. The certificate here keeps the decagons planar without adding diagonal bars or fixed face shapes. The [exact geometric audit](source-audit.md) identifies the supplied coordinates with the classical uniform truncation of a regular dodecahedron.

## What the present work adds

The new candidate contribution is a finite, exactly replayable certificate for local rigidity of this particular configuration in that model. The local computation uses characteristic 1009 and four cubic obstructions; four explicit degree-nine identities prove isolation. A zero-section specialization argument then establishes isolation at the actual characteristic-zero configuration. The finite-field identities are not claimed to lift coefficient by coefficient.

The underlying algebraic tools are standard. Relevant primary references are the Stacks Project: [formal parameter changes, 07NM](https://stacks.math.columbia.edu/tag/07NM), [completion, 00MA](https://stacks.math.columbia.edu/tag/00MA), [Nakayama's lemma, 00DV](https://stacks.math.columbia.edu/tag/00DV), [dimension under completion, 07NV](https://stacks.math.columbia.edu/tag/07NV), [isolated fiber points, 01TH](https://stacks.math.columbia.edu/tag/01TH), [openness of the quasi-finite locus, 01TI](https://stacks.math.columbia.edu/tag/01TI), and [base change, 01TM](https://stacks.math.columbia.edu/tag/01TM).

Valyu DeepResearch identified the published target and suggested a cubic-obstruction direction with numerical evidence. The present exact coordinates, certificates and verification were developed and checked locally. A research report is neither the mathematical proof nor evidence of priority.

## Priority remains pending

The primary arXiv record and [Martin Winter's publications page](https://martinwintermath.github.io/publications.html) were checked on the review date. The source still presents the target as unresolved. This is bounded evidence, not a proof that no later paper, thesis, preprint or unpublished argument resolves it. No claim of first discovery is made here. No author contact, public announcement or submission has occurred.

The written proof has received internal adversarial review and its exact arithmetic has independent implementations. Neither establishes publication priority or constitutes external peer review. There is no Lean proof of this result.
