# Research readiness

No pending computation blocks the retained certified claims. The author has not yet completed a line-by-line review.

## Retained result and scope

- Certified: lambda(5) = lambda*(5) = 6, delta(5) = 7, delta(6) = 10, lambda(6) >= 8. Ordinary alternating play, no swap rule. The strict value lambda* stops at the first connection; Campbell's lambda permits play after an overlong Blue connection.
- Search result only: lambda(6) <= 8, hence computed lambda(6) = 8. The Blue L8 certificate job was stopped; no replay is claimed and no restart is needed for the main result.
- The full 5x5 opening tables have 64/64 expected certificate records. The uniqueness of the two winning 6x6 openings at bounds D10/L8 is search evidence; the D10 winning strategy itself is certified.

## Evidence recovered and freshly checked

- 100 shipped main 5x5 certificates freshly replayed, with exact game/header tags; 10 corrupted variants rejected. A strict4 positive control replays 2,297 keys, and six strict corruptions are rejected.
- Original strict5 replay: 875,938 keys, at most 13 Blue stones. Original D9: 36/36 openings, 1,472,836 positions. Original D10: 5,158,730 positions, at most 10 Blue stones.
- Original L7: 36/36 openings, **22,780,097 positions**, recovered from five logs. `results.json` and the regeneration hash manifest now contain all 36 entries; the original certificate headers and hashes were checked during recovery.
- Original large replay logic is unchanged in the packaged checkers. The differences are gzip input, blank-line handling, header guards and scoped output tags. Large searches and large replays were not duplicated.
- `verification/check_records.py` fails on incomplete L7/D9/table records or changed shipped certificate hashes. `replay.py` requires both a successful process exit and the exact expected scoped conclusion. Long regeneration/replay commands emit 20-second heartbeats.
- `verification/logs/finish-build.log` records the fresh main replay. Strict control output and final source/PDF verification are recorded with the finish review.

## Confidence and credit

Correctness: **high** for the certified statements, conditional on the written game reduction and independent replay implementation. L8 upper bound: **moderate**, one search family, no independent replay. No Lean formalization or kernel-checked strategy theorem.

Originality: **moderate**. The completed bounded literature audits found no exact prior certificate result. Campbell and Stromquist supply the framework and classical bounds; the 2026 Casco-Pacifico-Sanhueza preprint supplies the contradicted claim. HZY/KataHex's 2024 estimate of 19 total moves already predicts delta(6) = 10 and is credited. Absence from the searches does not establish priority.

Reviews: `recreational-hex-priority` DR-065; `recreational-hex-review` DR-002. See `review.md` and `verification/review.md`.

## Handoff

Root owns the final independent review, integration and narrated video. `video-brief.md` specifies the rules, a 2x2 warm-up, a checked 23-move example, counts, credit and the certified/search-only distinction. No video files were edited. The optional L8 certificate remains out of scope.

## Final artifact inspection

Built `paper.pdf`: **6 pages**, all visually inspected after the final source edit. No overfull boxes or undefined references. SHA-256 `81ad7927b375d8ab2098801e2cfe3f6cca817013152ccc66a7c7b450e4dd0ac0`. `verification/pdf-inspection.json` records the inspected revision. 
