# Source provenance after the 26 October 2026 input-validation fixes

`completion-manifest-20261026.json`, `results.json`, certificates and all pre-existing logs remain historical records. Their source hashes are deliberately unchanged. In particular, the twelve-case replay in `logs/replay-20261026T134435172402Z/` ran the earlier source versions below. Those logs must not be described as runs of the patched sources.

| Source | Historical SHA-256 | Patched SHA-256 |
|---|---|---|
| `rankfq.c` | `af830d7f8226e9d514ebd7ec27565aa9db48e5cf010b2c41cefbc365668438f5` | `02443304367f309555bc504b406235f30056bd11e28418065a5704a3926c291b` |
| `subsp.c` | `1a9ff45d83bd3c452cb98605ae6603fc0b85776f070bce9d53846d9fe1b60b7b` | `03f3fd557a4003c1d4748f59908264c23ad7a464466152bf727e2de997f5cebe` |
| `run_searches.py` | `80514a36f6224842e8a8794888153aec86aad7cabbbd9544785346898adc7350` | `b4255760daec0da3f88ef4126d15b127821d0e5365223833db04806298e99d10` |

The changes reject overflowing or malformed integer input and unsupported dimensions, guard the 64-entry representative array and allocation failures, enlarge the q=7 hash table to hold the maximum 160,000 rank-one forms, and require the complete deterministic RESULT line in the runner. The mathematical enumeration loops, field arithmetic and all twelve expected completed result lines are preserved. The existing rank workspace limit of 8,192 rows remains explicitly guarded; exhausting that or the representative capacity exits 2 without a RESULT.

Fresh verification compiled the current sources: 40 sanitizer rejection cases; 86 small binary subspace searches; 56 binary comparisons with the generic search; a q=7 degree-four hash-capacity control; and the five generic-search campaign cases listed below. The 142 small valid result lines were also compared with freshly executed original binaries and were identical. Allocation-failure and rank-workspace controls used a test translation unit including the actual source.

| Fresh case | Seconds | Exact result |
|---|---:|---|
| `fresh-rankfq_q2_rank8` | 3.425 | `RESULT q=2 f=1,0,1,0,1 rank<=8: NO (prefixes 74377, candidate buckets 464776)` |
| `fresh-rankfq_T4_rank8` | 1.657 | `RESULT q=2 f=0,0,0,0,1 rank<=8: YES (prefixes 24898, candidate buckets 400307)` |
| `fresh-rankfq_q3_rank7` | 1.750 | `RESULT q=3 f=1,0,2,0,1 rank<=7: NO (prefixes 4794, candidate buckets 205980)` |
| `fresh-rankfq_q4_rank7` | 36.875 | `RESULT q=4 f=3,0,1,0,1 rank<=7: NO (prefixes 21668, candidate buckets 1930239)` |
| `fresh-rankfq_q5_rank7` | 313.868 | `RESULT q=5 f=4,0,4,0,1 rank<=7: NO (prefixes 73000, candidate buckets 17417506)` |

The first four campaign rows used address/undefined-behavior sanitizers. The q=5 row used the optimized C binary. Twelve historical completed logs were passed to the patched runner as fixtures, and thirteen corrupted fixtures were rejected. Fixture acceptance is not a fresh search. The 103,406,616-subset `subsp 21 4` enumeration, the bucket searches and the C++ q=5 search were not repeated in this fix pass.

Reproduce the durable scoped regression with a new output directory:

```sh
python3 -B test_review_regressions.py --output /tmp/algebra-review-controls --q5
```

The script uses nice 10, single-thread BLAS settings and ten-second heartbeats for real searches. Omitting `--q5` skips only the larger optimized C replay. Detailed raw controls, original source copies, before/after hashes and the closure report are in `<unpublished-record-18b8689d4964>`. No video files were edited. All 8 entries in `video/source-snapshot.json` still match: that snapshot does not include the three changed source files. The old completion manifest records their original hashes, not the new ones.
