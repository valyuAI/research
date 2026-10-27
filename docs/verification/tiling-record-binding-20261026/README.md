# Tiling record binding, 26 October 2026

Final integration review found that the ledger checker accepted a genuine retained proof log for the wrong tile. Substituting the dihex upper-bound record into the straight-trihex entry, then restoring only the trihex `cells`, reproduced the defect. Both entries have the same bound, so the old count and hash-string checks did not detect it.

The checker now requires exactly one complete formula-scope line, validates the integer coordinate pairs, and binds its grid, canonical tile shape, corona bound, imbalance and formula dimensions to the ledger. It also rejects a malformed additional scope line. The original hash and completion-marker checks remain.

The implementation review and replay accepted all 34 actual entries, rejected 34 corruptions, accepted eight translated/rotated/reflected/reordered geometry controls, and reconciled the retained 64 marked and 41 unmarked crosschecks. Root independently reread both changed files and repeated the full ledger and control commands; the [root replay record](root-replay.json) binds the current code to its logs. From the package's `verification/` directory, reproduce with:

```sh
python3 -B check_ledger.py
python3 -B negative_ledger.py
python3 -B check_crosschecks.py
```

Only `check_ledger.py` and `negative_ledger.py` changed among 97 verification files. The other 95, including the ledger, witnesses, encoders and retained proof logs, remain byte-identical. The [source hashes](source-hashes.json) preserve both versions; [scope preservation](scope-preservation.json) records the comparison.

This closes a retained-record consistency defect. It is not a fresh DRAT replay or formula regeneration and cannot authenticate a deliberately forged log. Encoder options omitted from the original log header remain governed by the documented commands and regeneration procedure. No mathematical value, paper, narration or animation changed. Confidence in this scoped fix is high.
