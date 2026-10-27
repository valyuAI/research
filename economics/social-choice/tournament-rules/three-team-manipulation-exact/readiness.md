# Final readiness: social choice

**Status: COMPLETE at the finite scope below.** Final completion on 26 October 2026. No required research job remains running.

## Exact retained claim

Among Condorcet-consistent tournament rules with coalitions of every size at most three, the optimal manipulability is 1/3 at n=3,4 and 2/5 at n=5,6,7,8. These values are attained by monotone, top-cycle-consistent rules as well. For n=7 and coalitions of size at most four, the optimum is 3/7. The known lower bounds supply optimality; this package supplies finite exact rational upper-bound certificates. The 14 certificates include a compact five-team example.

For the plain CC rules at n=5..8, the only constraints attaining 2/5 are the known regular-five-team-core lower-bound configurations. This is a property of these finite certificates, not an all-n structural theorem.

## Verification and review response

- Fresh independent replay of both n8 certificates: 6,880 classes and 2,889,600 manipulations each, exact maximum 2/5, 20 tight manipulations. The MT certificate also passes 192,640 monotonicity checks and all top-cycle support checks.
- Every remaining certificate freshly passes the canonical-form checker. The n7/k4 certificate checks 1,126,776 manipulations and has exact maximum 3/7.
- The independent labelled checker passes every certificate with n<=6, including the compact n5 MT rule. It checks all labelled tournaments without canonical forms; the n6 check covers all 32,768 labelled tournaments.
- Corrupted certificates are rejected. Real two-shard results merge successfully; missing shards, wrong certificate hashes, failed shards and changed coalition definitions fail. `check_results.py` binds all 14 results to exact counts, hashes, properties and le-mode definitions.
- Original successful n8 MT exactification logs are preserved in `verification/recovery/`; export and independent replay establish the final result. The formerly incomplete n8 claim is now supported. `review.md` answers both internal reports and records direct primary-source checks.

**Correctness confidence: high. Originality confidence: moderate.** The finite computations may have unpublished predecessors; bounded searches do not prove priority. DeepResearch reports reused: `DR-080` and `DR-040`.

## Not proved or claimed

No all-n result for n>=9, no k4 result beyond n=7, no universal formula for an optimal rule, and no resolution of the already-refuted general SSW question. The weak-strategyproofness observation is preempted by Brandt-Lederer Remark 3 and is excluded. Monotonicity and top-cycle consistency are separate certificate checks, not consequences inferred from the optimum.

## Reproduce

From this package run `sh build.sh` for every exact certificate, the labelled checks, negative tests and the PDF. `sh build.sh --quick` is only a reduced replay, not the full result. Default `JOBS=1` keeps a single heavy worker; use `nice -n 10 sh build.sh`. Replay needs standard-library Python and LaTeX; discovery additionally needs nauty, numpy/scipy/highspy/python-flint. `python3 verification/test_shard_merge.py` replays the shard failure tests.

| Evidence | SHA-256 |
|---|---|
| `paper.pdf` | `0efa36a1b5a9504caf67fe76fb312ab9eaec0e90b43bb1c0770bd4cf2ebc80fc` |
| `verification/certificates/rule_n8_k3.json` | `f695b1a28f570d764ae3c01cef9c84a75bde61682ce5cddecf97183056538b45` |
| `verification/certificates/rule_n8_k3_mt.json` | `25294d408524fba577126c7e8d3bd250637af78f64e144fadcf761092fc9ba60` |
| `verification/certificates/rule_n7_k4.json` | `05004298598c4e6ba4f5ab3074a7fbc21197ba2d882183a16808046593f21ef4` |
| `verification/results/rule_n8_k3_mt.result.json` | `a81f6934a81ea57efc62fbd6abaab6e1386c4224ee9cca77ccb7b3c479414970` |
| `verification/results/final_remaining.log` | `819e7f60ee433b110f2aa91bf4bad8b533f683645d58d31bbdff2bf7a9113c9f` |
| `verification/results/shard_failure_tests.json` | `f8a6d6d8ec71f6bb1cdba8b4afdcf16707b5fdad6e9a157304a294047d6320e6` |

## Artifact integrity and paths

- Package: `economics/social-choice/tournament-rules/three-team-manipulation-exact`.
- Final paper: `paper.pdf` (6 pages); editable source: `paper.tex` and `references.bib`.
- Complete evidence manifest: `verification/evidence.sha256`, SHA-256 `fca80352089d441e820267c470962b676962a1c3eea05985d12b5d9c5815a6e7`. It covers sources, certificates, recorded results, original logs and final PDF/inspection files. It excludes this readiness file itself, generated caches/binaries and the regenerable graph output directory.
- Verify from this package with `shasum -a 256 -c verification/evidence.sha256`.
- Every final page was rendered at 100 dpi and individually inspected. `verification/pdf-inspection/inspection.json` binds the inspected PNGs to the final PDF hash. No clipping, overlap or unresolved reference remains.
- Final scope is locked in `video-brief.md`; research is ready for the separate video pass. No video folder was edited. This is internal research completion, not external peer review or a public-release approval.
