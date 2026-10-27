# Readiness

Reviewed 18 October 2026. **The paper and replayable certificate are technically prepared for author and specialist review.** It has not been submitted to a journal.

## Precise result

The classical truncated dodecahedron is locally rigid when the original edge lengths and the coplanarity of every original face are preserved. The decagons can change shape; their diagonals are not fixed. The theorem is neither global uniqueness among distant realizations nor rigidity of the edge-only bar framework.

The proof has three distinct components:

1. Exact reconstruction verifies the intended geometry, a transverse Euclidean gauge, and polynomial identities over `F_1009`.
2. Formal elimination and Nakayama's lemma show that those identities isolate the special-fiber point, including against all higher-order terms.
3. The actual realization defines a section over `Z[phi,1/55]`. Openness of the quasi-finite locus along this section transfers isolation to characteristic zero; the transverse slice then gives Euclidean local rigidity.

The arithmetic has an independent standard-library checker. The mathematical implications have written internal review but **no Lean formalization**. Other papers' formal proofs do not cover this result. No proof gap was found in this review; outside scrutiny of the specialization and geometric encoding is still recommended.

## Source and bounded novelty review

The current metadata of [Adrian-Himmelmann, Winter and Zhang, arXiv:2607.09252](https://arxiv.org/abs/2607.09252) still identifies v1, submitted 10 July 2026; its manuscript is dated 13 July. These dates are now distinguished in the bibliography. The complete primary text explicitly leaves the truncated dodecahedron open in its introduction and Section 8.2, after finding four infinitesimal parameters and vanishing second-order obstructions. Its deformation model preserves exactly the edges and face planes used here.

The earlier [Himmelmann, Schulze and Winter paper, arXiv:2505.00874v3](https://arxiv.org/abs/2505.00874), gives generic three-dimensional rigidity in this model. Generic rigidity does not imply rigidity of this exceptional symmetric configuration. Neither Cauchy's face-congruence theorem nor bar-only framework results answer the current question.

Valyu searches on 18 October included `"truncated dodecahedron" "rigidity" "cubic"`, `"truncated dodecahedron" "rigid" "Winter"` with a July-onward date restriction, and the more useful `"truncated dodecahedron" "rigidity"` restricted to arxiv.org. No retrieved primary work resolved this exact example after the source. General solid-description pages and automated secondary reviews were not treated as evidence of priority. This is a bounded search; absence of a retrieved collision is not a guarantee of originality.

All seven foundational Stacks references were independently read again: [07NM](https://stacks.math.columbia.edu/tag/07NM), [00MA](https://stacks.math.columbia.edu/tag/00MA), [00DV](https://stacks.math.columbia.edu/tag/00DV), [07NV](https://stacks.math.columbia.edu/tag/07NV), [01TH](https://stacks.math.columbia.edu/tag/01TH), [01TI](https://stacks.math.columbia.edu/tag/01TI) and [01TM](https://stacks.math.columbia.edu/tag/01TM). They support respectively the formal parameter change, completion of finite quotients, Nakayama argument, dimension preservation, isolated-fiber characterization, open quasi-finite locus and base change. No flatness or properness assumption is needed in the section argument.

## Fresh verification

From this directory:

```sh
python3 -B -O verification/independent_verification.py
python3 -B -O verification/negative_verification_checks.py
sh build.sh
```

The exact replay passed in approximately 0.21 seconds. It reconstructed 60 vertices, 90 edges and 32 facets, checked all 1,740 strict supporting inequalities, the uniform-truncation identification, the six-gauge determinant of absolute value four, rank 272, all 40 zero quadratic coefficients, all 80 cubic coefficients and the four direct pure-power identities. All seven deliberate corruptions were rejected with assertions disabled. Neither the replay nor the proof needs Singular or a trusted numerical hull.

Both five-page author variants were rebuilt. Final LaTeX logs have no undefined citations, missing references or overfull/underfull boxes. All ten PDF pages were rendered and visually reviewed. The source now contains an early proof outline and a truthful account of the agents' roles in developing the certificate, argument, code and manuscript. No theorem or certificate input changed during the editorial pass.

## Remaining work

- Harvey Yorke has not yet completed a line-by-line review of the claim and its proof. The [author walkthrough](author-walkthrough.md) identifies the critical deductions. No human sign-off is asserted here.
- An algebraic geometer or rigidity specialist should scrutinize the complete argument and certificate interpretation. Internal agent reviews are not external peer review.
- Passing the arithmetic checks does not substitute for either review.

Correctness confidence: high for the arithmetic and stated written deductions. Originality confidence: moderate after the bounded source review. This is a specific geometry result, not a general new rigidity theorem or experimentally validated mechanics claim.
