# Contributing

Help us find something worth knowing, and leave enough evidence for someone else to check it.

Contributions made with any tools are welcome, including coding agents, literature-search services, computer algebra and proof assistants, or none of these. Record what you used and how it contributed. You are responsible for the claims, citations and submitted work.

## The workflow

1. **Find a precise question.** Explore a field, identify unresolved claims and find the closest existing results. Read the primary sources, including revisions and later work.
2. **Make a contribution.** Develop a proof, a counterexample, a reproducible scientific result or a useful extension. State the assumptions and explain exactly what changes relative to prior work. A search that finds no match does not establish novelty.
3. **Try to break it.** Have a separate reviewer, human or agent, check the argument. Check edge cases, competing explanations and numerical sensitivity. Use exact arithmetic, independent implementations or Lean where appropriate. Numerical patterns are evidence, not proofs; say precisely which statements are formally verified.
4. **Write a short paper.** Include the background, main result, complete proof or methods, properly checked citations, limitations and useful next questions. Supply editable LaTeX and a readable PDF. Distinguish a conjecture, a checked computation and a proved theorem.
5. **Make it reproducible.** Include the commands, dependency versions, seeds, data sources and certificates needed to repeat the work. Record how each tool contributed, including useful prompts and research task references. Keep credentials, private configuration and third-party full texts out of the repository.

This collection was produced with coding agents and Valyu DeepResearch, Search and Contents. Valyu AI develops those services. If you want to follow the same workflow, the [API docs](https://docs.valyu.ai/) describe them; for example, with the Valyu CLI:

```bash
valyu search paper "your precise research question" -n 10 --response-length max --json
valyu contents https://arxiv.org/abs/2307.03312 --length max --json
```

Replace the example paper with your own source. Nothing in this repository requires these services.

## What to submit

Use the existing subject hierarchy, adding a category only when it helps navigation:

```text
physics/mechanics/elasticity/your-finding/
  README.md          # Claim, status, significance and how to reproduce it
  paper.tex
  paper.pdf
  references.bib
  build.sh
  verification/      # Checks, certificates and reproduction instructions
  video/             # Optional narrated explainer; see tools/video/README.md
```

To list a finding in the [gallery](FINDINGS.md), add its entry to `docs/collection.json` and a plain-language summary to `catalog/findings.json`, then run:

```bash
python3 tools/catalog.py render
python3 tools/catalog.py check
```

Shared Lean proofs belong in `formal/`. Explain their scope in the [coverage ledger](docs/formal-coverage.md); accepted proofs must build without `sorry`, admitted results or unreviewed axioms. See the existing [reproduction instructions](docs/reproduce.md) and [taxonomy](docs/taxonomy.md).

## Licensing of contributions

Contributions are accepted under the same terms as the material they add to, as set out in [LICENSE](LICENSE): Apache-2.0 for software, Lean source, verification programs and build scripts; CC BY 4.0 for papers, documentation, original data, illustrations and media; and CC BY-SA 4.0 for adaptations of the Bašić-derived tiling coordinates and rendered visual assets covered by the stated exception. By opening a pull request you agree to license your contribution under the applicable terms. Include only material you are entitled to share. Other third-party data or code keeps its own terms; record its source and terms in the package and in [public-release/THIRD_PARTY.md](public-release/THIRD_PARTY.md).

Open a pull request with the claim, closest prior result, what is new, checks actually completed and any remaining uncertainty. Include the research provenance and an honest assessment of significance. Keep unsuccessful leads and exploratory notes separate from established findings. Independent replications and corrections are welcome when clearly labelled.

We review correctness, originality and presentation separately. An agent's endorsement is not peer review, and a polished paper is not evidence that its result is new.
