# Verification

Everything uses exact arithmetic over GF(q) and runs on the Python 3 standard library.

| File | Role |
|---|---|
| `construct.py` | Generator: finite fields, the Gabidulin family, balanced blocks (Lemma 4.2), absorption (Lemma 4.3), the inductive recipe (Theorem 4.4) and the base-case search. |
| `generate_certificates.py` | Writes `certificates/` with deterministic seeds: `base/` (245 base cases, q = 3, 4, 5, r = 4, 5), `table/` (the four new ququart codes), `maximal/` ([[q^3+1, q^3−4, 3]]_q for q = 3, 4, 5, 7, 8, 9). `generation_log.json` records the method used for each. |
| `check_codes.py` | **Independent checker.** It shares no code with the generator and uses no assertions. It rebuilds GF(q) from the stored modulus and checks irreducibility. It then checks that the symplectic Gram matrix is zero and that all n(q²−1) single-qudit syndromes are distinct and nonzero, which is equivalent to purity to distance three. It also computes the rank and checks base-case coverage; the default run exits with status 1 if any certificate is invalid or any required base case is missing (explicit-file mode fails only on invalid certificates). Output: `check_codes_results.json` with SHA-256 hashes. |
| `missing_certificate_check.py` | Negative test for coverage: in a temporary copy it deletes `certificates/base/q3_r4_n5.json` and confirms that `check_codes.py` then exits nonzero, while explicit-file mode on one certificate still passes. Output: `missing_certificate_check.log` via `build.sh`. |
| `negative_checks.py` | Seven corrupted inputs (flipped entry, duplicated line, zero column, reducible modulus, out-of-range entry, rescaled column, appended duplicate qudit), all rejected. Output: `negative_checks_results.json`. |
| `check_bounds.py` | Bound arithmetic. It covers μ_q, Lemma 3.3 for q ≤ 32 and r ≤ 40, the reduction bounds of Theorem 3.4 and Corollary 5.2 against `codetables_snapshot_2026-10-25.json`, and Proposition 5.3 for additive ququart codes. Output: `check_bounds_results.json`. |
| `replay_recipe.py` | Replays the induction for small (q, r) with no search over line configurations (some line-block weights come from seeded random coefficient trials, as in Lemma 4.2(5)) and checks every configuration with `check_codes.check_dict`. Output: `replay_recipe_results.json` and `replay_recipe.log`. |
| `codetables_snapshot_2026-10-25.json` | The twelve open qudit entries compared in the paper, with their lower and upper bounds as listed on Markus Grassl's codetables.de on 25 October 2026. Each was re-read live. The full extraction of all 20,278 open entries (q = 3, 4, 5, 7, 8; n ≤ 100; k ≥ 1) is not redistributed; its SHA-256 is recorded in the file. |

## Commands

```sh
python3 -B -O verification/check_codes.py        # 255 certificates, about 3 s
python3 -B -O verification/negative_checks.py
python3 -B -O verification/missing_certificate_check.py
python3 -B -O verification/check_bounds.py
python3 -B -O verification/replay_recipe.py      # about 20 minutes
python3 -B verification/generate_certificates.py # regenerates certificates/
```

## Recorded results

- `check_codes`: 255/255 valid, base cases complete for q = 3, 4, 5 (r = 4: n = 5..μ_q(4); r = 5: n = 6..μ_q(5)).
- `negative_checks`: 7/7 rejected.
- `missing_certificate_check`: with one required base certificate removed, `check_codes.py` exits 1 and reports `q3_r4: [5]` missing.
- `check_bounds`: no violation of Lemma 3.3; max over t of 2t + μ_q(r−t) equals μ_q(r) for every checked q ≥ 3 and r ≥ 4. Twelve table entries improve and eleven become exact. The public snapshot reproduces the recorded `check_bounds_results.json` and log byte for byte. That no other open entry improves was established on 25 October 2026 by running the same checker on the full extraction; replaying that completeness scan requires extracting the tables from codetables.de again. The additive ququart bounds are 65 < 66 and 66 < 67.
- `replay_recipe`: all OK. The runs cover q = 3, r ≤ 8; q = 4, r ≤ 7; q = 5, 7, 8, r ≤ 6; q = 9, 11, r ≤ 5; q = 13, r = 4. Every r+1 ≤ n ≤ μ_q(r) is included, with lengths capped at 700 for (7,6) and (8,6) and at 400 for (11,5).

## What is and is not certified

The certificates prove existence for the stored parameters. The general theorem rests on the written proofs in the paper: Lemmas 2.1–4.3, Theorem 4.4 and Corollary 5.2. Thas's generalized-arc bound and the Năstase–Sissokho value a(10) = 65 are cited, not re-proved. Nothing is formalized in Lean.
