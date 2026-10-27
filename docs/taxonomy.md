# Research taxonomy

The repository is organized by **discipline → field → topic → finding**. Directories are the taxonomy; every populated category has a short README that links to its children.

| Level | Example |
|---|---|
| Discipline | `maths` |
| Field | `combinatorics` |
| Topic | `ramsey-theory` |
| Finding | `prime-successor-hales-jewett` |

A finding has one canonical location chosen by its central research question. Related categories link to it instead of copying files. Further topic levels can be added when a field becomes large enough to need them; empty categories are not pre-created.

The elasticity result sits under `physics/mechanics/elasticity`, where its inverse problem originates. The Lotka-Volterra result sits under mathematical dynamical systems because it classifies algebraic systems. It is not an empirical biological result. The restart result sits under statistical physics and is cross-linked from mathematics because its proofs also concern probability and Markov processes.

The truncated-dodecahedron result sits under `maths/geometry/rigidity`: its central question is whether fixed edge lengths and face coplanarity allow a polytope to deform.

The periodic waiting-time counterexample sits under `physics/statistical-physics/thermodynamic-inference`: its question is whether a particular observation-based estimator bounds entropy production.

The cubic equilibrium construction sits under `chemistry/reaction-networks/mass-action`: it concerns the number of positive equilibria allowed by reaction stoichiometry and kinetic degree, rather than an experimentally demonstrated chemical mechanism.

The 25-26 October additions include `economics/social-choice/tournament-rules`, mathematical phylogenetics, knot theory, covering systems and quantum error correction. Phylogenetic trees are placed under combinatorics because the results concern abstract tree agreement and balance, not empirical ancestry. The [curated inventory](collection.json) defines the retained findings and drives the [collection index](collection.md); unfinished drafts are excluded from those counts.

## Anatomy of a finding

```text
finding-name/
├── README.md
├── paper.tex
├── paper.pdf
├── references.bib
├── paper.bbl
├── journal.tex
├── journal.pdf
├── journal.bbl
├── build.sh
├── verification/
│   ├── README.md
│   ├── verifier source
│   └── retained certificates and results
└── video/
    ├── README.md
    ├── scenes.py
    ├── narration.json
    ├── audio/
    ├── subtitles.srt
    └── video.mp4
```

Formal Lean sources are linked from each finding's README and remain in the shared root `formal/` project. This avoids separate toolchains and dependency copies for every paper. The root `docs/` directory records cross-cutting provenance, review decisions and exact formal coverage.

Journal variants are optional in newer packages and are distinct from the canonical paper. Video production status is explicit in the inventory; a brief or partial render does not count as a finished explainer.

## Adding a finding

1. Choose the discipline, field and topic that best describe the actual contribution. Use lowercase hyphenated directory names.
2. Create a stable, descriptive finding folder and add its manuscript, references, reproducible evidence and a short README.
3. State whether it is a new-result candidate, an independent verification note, a conjecture or a negative result. Keep correctness, formal coverage and priority separate.
4. Link it from the parent category and the root collection index. Add cross-links for secondary subjects.
5. Update the formal-coverage ledger and artifact hashes when applicable. Keep raw exploratory data, credentials and full retrieved third-party texts outside the curated collection.

The taxonomy is for navigation; being included does not imply external peer review or established priority.
