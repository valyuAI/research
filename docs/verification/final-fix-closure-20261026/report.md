# Round 2: focused closure review of F1-F6 and q7 capacity

Date: 26 October 2026. Historical verification review; reviewed source hashes are recorded in [source-hash-snapshot.json](source-hash-snapshot.json).

**Conclusion: F1-F6 and the additional q7 hash-capacity defect are closed in the reviewed snapshot. No actionable regression or unresolved objection was found within this scope. Confidence: high.** This conclusion rests on source inspection, independent small probes, and reconciliation of the implementation/root replay evidence. It is not a fresh reproof of the 26 research packages, an unrestricted-input completeness claim, or a novelty certification.

This was a read-only review of the retained artifacts. No new literature search, formal build, DRAT replay or media QA was performed.

## Closure decisions

### F1: retained tiling log bound to the wrong tile

**Closed.** `maths/geometry/tilings/marked-polyform-heesch-numbers/verification/check_ledger.py:88-114` now counts every line containing `cells=` before parsing and requires exactly one complete header. The parsed cell list must be nonempty, with integer coordinate pairs; booleans, floats and extra coordinates are rejected. Grid and canonical shape, k, imbalance 1, and all three formula dimensions must agree with the ledger. Existing hash and completion checks remain.

The canonicalizer at lines 40-48 retains multiplicity, so duplicate cells cannot silently disappear. Its translation, rotation and reflection equivalences are appropriate to the existing hexagonal/square scope. The added negative controls check specific failure messages rather than accepting arbitrary failures as successful rejection.

Fresh probes in this round invoked the current checker without writing fixtures to the repository:

- The genuine dihex proof record substituted into the straight-trihex entry is rejected with `formula log is for another tile`.
- A valid header followed by a malformed second `cells=` header is rejected with `missing or ambiguous formula scope`.
- `cells=[[0, 0, 999]]` is rejected with `invalid formula cells`.

The implementation's 34 actual entries, 34 negative controls, eight equivalent-geometry controls and 64/41 retained crosschecks were inspected as prior executed evidence, not re-executed in this round. Both root replay source/log hash pairs match. All 97 current verification-file hashes match the implementation's after snapshot; comparing its before/after maps confirms exactly the two intended changes and 95 unchanged files.

This closes record consistency, not proof authenticity. The original header does not encode every encoder option; the fix correctly avoids claiming that it does. A deliberately forged log, regeneration of the formula, and a fresh DRAT check remain separate questions. These documented limits do not leave F1 open.

### F2: algebra representative-array overrun

**Closed.** `maths/algebra/bilinear-complexity/mu-q-2-2/verification/rankfq.c:252-261` checks capacity before every `reps[nreps++]` write. Exhaustion returns 2 before the final RESULT output. The accepted-input parsing and allocations were also inspected at lines 20-27, 155-179, 199-214 and 233-247.

The original reproducer `rankfq 5 3 0 4 1 4 1` is covered by both implementation and root sanitizer suites and rejects without a RESULT. The current source hash matches both suites. I did not recompile or rerun this C case in round 2.

The 64-representative cap remains a supported refusal boundary. Rejection of a mathematically admissible polynomial is not reported as a negative rank decision. Increasing the cap or replacing the orbit enumeration is unnecessary for closure.

### F3: unsafe binary-search inputs and dimensions

**Closed.** `maths/algebra/bilinear-complexity/mu-q-2-2/verification/subsp.c:20-27,48-62,97-99` rejects failed/overflowing/trailing-input conversions before narrowing, requires `2 <= f <= 31`, `0 <= m <= 8`, and `m <= n*n-n`, and checks allocation success. The zero-bitmask, degree-five and increment-nine reproducers now reject in both recorded sanitizer suites.

I checked the dimensional argument against the actual loops: n is 1..4; multiplication by 1 makes the n output slices independent; the quotient dimension is at most 12; there are at most 225 binary rank-one forms; and the subset span has at most 256 elements. These bounds fit the fixed arrays and shifts. The m=0 loop terminates safely through the short-circuited `k >= 0` condition. The largest permitted subset count fits signed 64-bit counters. No enumeration loop was changed by the fix.

The implementation/root records contain 40 invalid cases and 142 small valid searches. The separate implementation differential record compares all 142 complete result lines with the original binaries. These are reconciled prior runs, not fresh executions by this reviewer.

### F4: optimized Python silently removes verification

**Closed.** The guards are module-level in `chemistry/reaction-networks/mass-action/acr-multistability-bounds/verification/independent_check.py:17-18` and `maths/combinatorics/phylogenetics/common-quartet-number/verification/iterate_check.py:16-17`. They protect imports as well as direct entry-point execution.

This round freshly tested imports of each module under `-O`, `-OO`, `PYTHONOPTIMIZE=1` and `PYTHONOPTIMIZE=2`: all eight exit 1 with `verification requires Python assertions enabled`. Normal-mode ACR probes correctly classify a strict Hurwitz polynomial and a negative-constant polynomial, and reject the original undecided polynomial `x^3+x^2+x+2`. For quartets, all eight exact thresholds and both factor controls pass; one seeded k=3 family passes, and the identical family rejects after an in-memory forced-false factor predicate.

Removing only the three-line guard from each current source restores its exact recorded before SHA-256. The normal-mode algorithms are therefore byte-identical to the prior versions. All four before-log and eight after-log hashes match their records. Root's full ACR and 18-family quartet runs are inspected evidence; the 613-family replay and the complete dimension-two chemistry proof were not repeated.

### F5: incomplete result/count validation

**Closed.** `maths/algebra/bilinear-complexity/mu-q-2-2/verification/run_searches.py:22-26,41-54` now requires `results == [expected]` and a zero process exit. All twelve expectations are complete deterministic RESULT lines. The q=5 C and C++ expectations both require 17,417,506 candidates and 73,000 prefixes.

I independently extracted all twelve cases from the current source and compared each expected line with the singleton RESULT in its raw retained log, the recorded result, and the recorded command arguments: all agree. The implementation/root fixtures and thirteen rejected mutants exercise wrong counts/scope/answer/rank, malformed or extra result text, missing/duplicate results and nonzero exit. Those fixture executions were not repeated in this round.

The C++ RESULT format has no q/polynomial fields; its entire printed line is pinned and associated with the fixed command arguments. The fix does not claim to validate fields the executable never prints.

### F6: case-sensitive readiness link

**Closed.** The lab generator `integrate_collection.py:75-78` selects readiness names from actual directory-entry spellings. It no longer relies on a case-insensitive path-existence check. `docs/collection.md` uses `generic-stiffness-recovery/READINESS.md` and contains no lowercase variant for that target.

I executed only the generator's two read-only selection assignments, extracted from its syntax tree, against all 26 current entries. All 18 emitted review-state links have the exact selected filename spelling. The generator itself was not run and no navigation file was regenerated. Root's broader 48-document/332-link audit is supplied evidence, not a second full navigation audit by this reviewer.

### Additional q7 hash-capacity fix

**Closed.** `rankfq.c:100-107` uses `HB = 1 << 18`, with the corresponding 18-bit hash index (`h >> 46`). Given the validated field and degree limits, the number of projective functionals is at most `(7^4-1)/(7-1) = 400`, and rank-one forms number at most 160,000. Every occupied bucket originates from a form, so occupancy cannot reach 262,144. Lookup occurs during positive-count bucket construction, before processed-slot marking, and touched slots are reset between prefixes. Changing the hash placement does not change form IDs or their candidate traversal order.

I independently recomputed the maximum over every supported q and n, the conservative signed-64-bit counter bound, and the q7 stress polynomial's irreducibility by trial division against all 56 monic degree-one/two polynomials. All checks pass. The retained instrumented original run demonstrates saturation at 131,072 slots; both implementation and root post-fix sanitizer runs complete the same 160,000-form instance with:

```text
RESULT q=7 f=1,0,0,1,1 rank<=5: NO (prefixes 1, candidate buckets 0)
```

No q7 executable replay was needed in this review. The existing 8,192-row guard remains an explicit failure boundary, distinct from a scientific RESULT.

## Evidence reconciliation and provenance

The supplied original brief, prior report/proposed patch, algebra report/changes/closure summary, tiling report/implemented patch/hash maps, and repository closure records were read. Current source hashes agree with the implementation and root records.

Fresh reconciliation in this round checked:

- Five algebra source/provenance hashes and all 299 entries in the algebra implementation evidence manifest, with no mismatch.
- Both guard sources, the exact guard-only before/after change, and all twelve guard evidence logs.
- All 97 tiling verification hashes and both root source/log pairs.
- The new root algebra results: 189 process records, comprising two compilations, 40 invalid cases, 142 small valid cases, one q7 case, and four fresh q2/q3/q4 campaign cases. All recorded statuses are consistent with their case categories.
- The implementation algebra results: 191 records, adding the optimized compilation and q5 replay. The four repository copies of implementation results, closure summary, resource controls and differential controls are byte-identical to their lab originals.
- The historical algebra completion manifest still records the original hashes for `rankfq.c`, `subsp.c` and `run_searches.py`; each matches the saved original source and differs from the patched source, as the supplemental provenance explains.

The root replay did not include q5. The implementation's post-fix q5 C run is fresh evidence from that earlier fix pass, with 73,000 prefixes and 17,417,506 buckets; I inspected its raw final output and reconciled its recorded evidence hash. The 103,406,616-subset binary enumeration, bucket searches and independent C++ q5 search remain retained historical evidence. Historical runs have not been relabelled as executions of patched code.

## Simplification assessment

The exact singleton RESULT comparison is a useful simplification and is correctly retained. The small parsing helpers, pre-write capacity check, module guards and exact filename selection are proportionate to the defects. Keeping each C source independently compilable is preferable to adding a shared abstraction solely to remove two tiny parsing helpers. Tiling's separate scope/schema/geometry/dimension checks and positive controls cover different failure modes and should remain.

No further simplification is worth changing tested code in this closure pass. In particular, no mathematical enumeration, field arithmetic, canonicalizer, exact quartet comparison or witness checker needs rewriting to close these findings.

## Fresh checks, retained checks and limits

Fresh executions by this reviewer were limited to the small in-memory/read-only Python probes, twelve retained-line/command comparisons, the bounded q7 arithmetic/divisibility check, exact readiness-name selection, and hash/evidence reconciliation described above. Probes used nice 10, single-thread numerical-library settings and disabled bytecode writing. The combined Python execution probes took about six seconds and printed incremental per-case results. No temporary binary, fixture or log was left behind.

No complete C regression suite, q4/q5 campaign search, full ACR rerun, full quartet replay, full tiling negative suite, new manuscript proof audit, formal build, removed DRAT proof recreation or media check was performed here. Root's updated 26-video completion, ffprobe and 1,707-artifact-hash results are outside this review and are not independently certified by it. Final inventory/counts, secret scan, release integration and commit/PR remain root-owned.

There are **no unresolved objections to the scoped F1-F6/q7 closure**. Confidence is high for these concrete verification-contract and capacity fixes. This report makes no new assessment of broader mathematical completeness, publication priority, human listening review or release readiness.
