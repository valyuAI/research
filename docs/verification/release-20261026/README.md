# Collection release checks, 26 October 2026

This release retains 26 research packages, with 19 added in the current campaign, and 26 narrated videos totalling 4 hours, 3 minutes, 37 seconds. The [collection](../../collection.md) is the entry point. Originality and proof scope are stated per package.

Completed integration evidence:

- The expanded Lean library builds and passes its 153-declaration local axiom audit. The initial integration record predates the expanded library's Linux replay; the earlier replay covered 121 declarations. The subsequent [26 October CI replay record](../formal-library-20261026/ci-replay.json) and retained logs establish six-checker replay of all 153 declarations. This covers the shared formal library only.
- Seven previously validated paper packages were rebuilt from their archives and matched the reviewed sole-author PDF text. Their formal archive includes all seven project imports. Unfinished drafts and videos are excluded from those submission archives.
- The [verification-fix closure review](../final-fix-closure-20261026/report.md) accepts all six reported issues plus the q=7 capacity correction, with no unresolved objection in that scope.
- The [media inventory](../media-completion-20261026/collection-media.json) records current MP4 hashes and native 1080p30 H.264/AAC metadata for all 26 videos, plus 1,707 matching retained artifact hashes. Production QA and listening limitations remain explicit.
- The [source scan](source-scan.json) records known credential/signed-URL pattern checks. The [navigation audit](navigation-check.json) checks exact local filename spelling independently of the case-insensitive filesystem.

The global `docs/artifact-hashes.json` inventories retained files except itself. One unfinished draft is deliberately excluded. Optional searches and removed large DRAT files are governed by each package's historical evidence and regeneration instructions. Neither this inventory nor the absence of a detected defect establishes publication priority or external peer review.

The staged whitespace check reports 137 trailing-space or extra-final-blank-line findings in 49 retained files. These are recorded in [retained whitespace](retained-whitespace.json). Certificate, execution-log and reviewed-source bytes were preserved for their existing hash records. No check, linter or hook was disabled, and the whitespace check is not reported as passing.
