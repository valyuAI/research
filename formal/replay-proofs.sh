#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

diagnostics="${1:?Usage: ./replay-proofs.sh /absolute/diagnostics-directory}"
mkdir -p "$diagnostics"
diagnostics="$(cd "$diagnostics" && pwd)"

printf 'Audit all project theorems, including private declarations\n'
lake env lean Audit.lean | tee "$diagnostics/axiom-audit.log"
python3 - "$diagnostics" <<'PY'
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
audit = (root / "axiom-audit.log").read_text()
names = re.findall(r"^PASS ([^\s:]+):", audit, re.MULTILINE)
counts = re.findall(r"Audited (\d+) project theorems;", audit)
if len(counts) != 1 or not names or len(names) != int(counts[0]):
  raise SystemExit("Theorem inventory does not match the completed axiom audit")
if len(set(names)) != len(names):
  raise SystemExit("Duplicate theorem names in audit")
(root / "requested-theorems.txt").write_text("\n".join(names) + "\n")
print(f"Exporting all {len(names)} audited theorem roots and their proof dependencies", flush=True)
PY
mapfile -t theorem_names < "$diagnostics/requested-theorems.txt"

# The exporter runs with no network and a read-only host filesystem.
# Lake may refresh its already-built project cache within the sandbox.
bwrap --unshare-all --die-with-parent --new-session \
  --ro-bind / / --dev /dev --proc /proc \
  --tmpfs /tmp --tmpfs /run --tmpfs /var \
  --bind "$PWD/.lake" "$PWD/.lake" --chdir "$PWD" \
  --clearenv --setenv PATH "$PATH" --setenv HOME "$HOME" \
  --setenv LEAN_ABORT_ON_PANIC 1 \
  --setenv LEAN_NUM_THREADS "${LEAN_NUM_THREADS:-2}" \
  lake env leanexport ValyuResearch -- "${theorem_names[@]}" \
  > "$diagnostics/project-proofs.ndjson"

sha256sum "$diagnostics/project-proofs.ndjson" | tee "$diagnostics/export.sha256"
wc -lc "$diagnostics/project-proofs.ndjson" | tee "$diagnostics/export-size.txt"
printf 'Replay the complete project proof closure with every bundled checker\n'
lake check --from-export "$diagnostics/project-proofs.ndjson" --paranoid
