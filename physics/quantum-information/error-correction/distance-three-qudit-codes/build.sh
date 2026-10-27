#!/bin/sh
# Replays the fast verification and builds both author variants of the paper.
# The full replay of the inductive construction (several minutes) is separate:
#   python3 -B -O verification/replay_recipe.py
set -eu
cd "$(dirname "$0")"
# Each step exits nonzero on failure; the build then stops before printing success.
check() {
  if ! python3 -B -O "verification/$1.py" > "verification/$1.log"; then
    printf 'Verification FAILED in %s (see verification/%s.log)\n' "$1" "$1" >&2
    exit 1
  fi
}
check check_codes                 # all certificates valid and base-case coverage complete
check negative_checks             # seven corrupted certificates rejected
check missing_certificate_check   # removing a required base certificate makes check_codes fail
check check_bounds
printf 'Verification passed (see verification/*.log)\n'
for document in paper journal; do
  printf 'Building %s\n' "$document"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" > "$document.build.log"
  bibtex "$document" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  printf 'Built %s.pdf\n' "$document"
done
