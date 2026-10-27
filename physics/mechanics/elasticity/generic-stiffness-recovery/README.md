# Recovering three-dimensional stiffness from wave speeds

A computer-assisted proof of generic uniqueness for density-normalized elasticity. The result resolves Conjecture E in de Hoop, Ilmavirta, Lassas and Várilly-Alvarado, [arXiv:2307.03312v2](https://arxiv.org/abs/2307.03312).

For a generic tensor, **22 scalar invariants determine all 21 stiffness parameters**, even against exceptional complex competitors. Unordered phase spectra in **eleven generic directions suffice; at least eight directions are necessary**. A separate interpolation corollary supplies fifteen explicit sufficient directions. Whether eight, nine or ten generic directions suffice remains open in this work; no count is claimed optimal.

- [Paper](../../../../public-release/papers/generic-stiffness-recovery.pdf) · [LaTeX](paper.tex)
- [Exact certificates and reproduction](verification/README.md)
- [Eleven-direction certificate and incidence proof](verification/finite-directions/README.md)
- [Prior-source check](SOURCE_FACTCHECK.md) · [Internal proof review](INTERNAL_REVIEW.md)
- [Readiness and author walkthrough](READINESS.md)
- [Formal verification coverage](../../../../docs/formal-coverage.md)

```bash
./build.sh
python3 verification/verify_all.py
```

The default verifier uses Python and SymPy 1.14.0, with exact arithmetic and no network calls. It includes both the original rank-stratum checks and the new finite-direction source and identity checks. The minor identities and the compact finite-direction certificate have separate standard-library checkers. Gröbner calculations are optional corroboration.

**Status:** internally reviewed research draft, revised 18 October 2026. High confidence in the checked argument; publication priority remains provisional. This is a generic identifiability theorem, not a reconstruction algorithm, stability guarantee, or claim that density and stiffness can be separated. Known ambiguities on exceptional symmetry classes remain. The full geometric argument is not formalized in Lean.

The eleven-direction extension has independent internal arithmetic replay and geometric review. A completed DeepResearch review of the full draft found no mathematical error and independently checked the dimension argument, but did not replay all saved certificates. Its findings were checked against the current proof, sources and verification records. All eleven determinant identities for the second normal quotient have separately compiled in Lean and passed their axiom audit. The distinct eleven pure-power identities for the finite-direction cubic slice have exact Python verification and are not formalized in Lean. See the formal-coverage record. No external peer review is claimed.
