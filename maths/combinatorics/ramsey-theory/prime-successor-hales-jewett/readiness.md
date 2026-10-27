# Readiness

Reviewed 18 October 2026. **Technical preparation is complete; human line-by-line review remains open.** The paper has not been submitted to a journal.

## Claim and proof

The main theorem is `HJ(p+1,2;2)=p+1` for every prime `p`, with a red full combinatorial line and a blue **consecutive** two-point partial line as the forbidden alternatives. This is not the classical diagonal Hales-Jewett number usually written `HJ(k;2)`.

The elementary proof and the current Lean declarations agree. The semantic review checks the nonempty wildcard set, ordinary rather than reversed wildcards, absence of wraparound adjacency, availability of alphabet value `p`, all lower dimensions, and the least forcing dimension. `prime_lower_bound`, `HJ_le_self` and `HJ_prime_successor` establish the exact statement; `HJ_eight` and `HJ_twelve` instantiate it. The geometric comparison additionally uses the source's reported `G(8,2)=7`, which was not independently reproduced and is not included in the Lean proof.

The theorem's mathematical content and formal source were unchanged during this editorial pass. We made the lower-dimensional restriction explicit, added the concrete seven-coordinate coloring, credited the adjacent symmetric-coloring literature, and made the assistance disclosure accurately include the development of arguments, code, formalization and text.

## Closest prior work and bounded novelty check

- [Conlon, Farnsworth and Robertson, arXiv:2607.18111v1](https://arxiv.org/abs/2607.18111): current metadata still identifies v1, submitted 20 July 2026. The full text's Definitions 10 and 11 specify consecutive partial lines. Theorem 12 gives `HJ(k,2)<=k`; Theorem 15 gives the previous prime lower bound; Conjecture A asks for equality for every `k`; Table 3 and Question D contain the `k=8` geometric comparison. Our contribution is the repaired modular coloring and the infinite prime-successor family, not the upper bound or those definitions.
- [Mouhib, arXiv:2606.22155v2](https://arxiv.org/abs/2606.22155): current metadata identifies the 24 July 2026 consolidated version, superseding arXiv:2607.02226. Its symmetric and one-weight constructions concern classical diagonal numbers and other specified variants. Its `HJ(4,2)>=14` denotes four letters and two colors; it is not our off-diagonal `HJ(4,2;2)=4`. We cite the relevant method context without claiming symmetric colorings as a new technique.
- [Shelah, arXiv:2607.14732v3](https://arxiv.org/abs/2607.14732): the 15 October 2026 metadata concerns general upper bounds for the classical theorem. It does not announce this consecutive off-diagonal family.

The 18 October Valyu searches included `"Hales-Jewett" "prime" "successor" "Conlon"`, `"Hales-Jewett" "Farnsworth" "Robertson" "8"` with a July-onward date restriction, and `"off-diagonal" "Hales-Jewett"` restricted to arxiv.org. The first two returned substantial irrelevant material; the targeted search and primary-text reading carry more weight. No matching prior resolution was found in the retrieved sources. This is a bounded search, not proof of priority or a complete survey of unpublished work. Originality confidence remains moderate.

## Checks performed

From the paper's `verification` directory:

```sh
c++ -std=c++17 -O2 -Wall -Wextra verify_hj8.cpp -o /tmp/hj8-check
/tmp/hj8-check hj8_blue_histograms.csv
```

The fresh replay checked 490 blue histograms, all 2,685,817 ordered nonempty variable words and the rule on all 2,097,152 points. It found 299,587 blue points, zero red full lines, zero blue consecutive pairs and zero rule disagreements. The compiler emitted no warnings.

`sh build.sh` rebuilt both three-page PDFs, including their supplied `.bbl` files. Final LaTeX logs have no missing references, undefined citations, or overfull/underfull boxes. Every page of both variants was rendered and inspected. The complete Lean proof and the separate six-checker replay are documented in the repository's [formal coverage](../../../../docs/formal-coverage.md); the finite C++ check is supplementary, not the proof of the infinite family.

## Remaining work

1. Harvey Yorke has not yet completed a line-by-line review of the proof. The [author walkthrough](author-walkthrough.md) lists the steps that review must cover. No human sign-off is recorded here.
2. Editing by another coding agent does not substitute for that review. The [public paper](../../../../public-release/papers/prime-successor-hales-jewett.pdf) is a review draft, not a declaration that it has occurred.
3. The [public PDF](../../../../public-release/papers/prime-successor-hales-jewett.pdf) lists Harvey Yorke and Valyu DeepResearch as co-authors and records the contribution and review status. The earlier archival `paper.pdf` is omitted from the public export; its hash is retained in the release records.

Correctness confidence: high for the checked theorem. Originality confidence: moderate. Acceptance and significance remain editorial judgments.
