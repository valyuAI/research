# Public release records

This collection is published from a clean source snapshot. Earlier working
history is not part of the public repository.

- `papers/` contains the publication PDFs and their reproducible build manifest.
  The editable manuscript sources remain in each research package.
- `release-changes.json` records exact current hashes for files that differ
  from the earlier artifact inventory in `docs/artifact-hashes.json`.
- `export-exclusions.json` records the earlier hashes of omitted files:
  restricted third-party tables, superseded presentations, intermediate media
  and administrative records.
- `path-redactions.json` records changes to local execution paths and research
  service identifiers in log and review copies. Original records are preserved
  separately. These substitutions do not change mathematical certificates,
  inputs, proof statements or recorded numerical results.
- [Review identifiers](../docs/review-identifiers.json) commit the original job
  identifiers by hash while using stable labels in the public documentation.
- [Third-party material](THIRD_PARTY.md) lists attribution and license exceptions.

Historical evidence records describe the executions and sources they originally
checked. Their embedded hashes are not silently rewritten to claim that a
redacted copy was the original execution input. The change and redaction records
explain the differences; `python3 tools/catalog.py check` checks the public files
against their declared hashes.

The papers distinguish internal review, exact computational checking and the
scope of formal verification. Publication of this snapshot does not constitute
external peer review or establish priority over unexamined literature.
