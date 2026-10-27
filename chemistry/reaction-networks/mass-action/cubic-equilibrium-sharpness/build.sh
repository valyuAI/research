#!/bin/sh
set -eu
cd "$(dirname "$0")"
case "${1:-}" in
  "") ;;
  --regenerate-certificate) python3 -B -O verification/verify_cubic_sharpness.py ;;
  *) printf 'Usage: sh build.sh [--regenerate-certificate]\n' >&2; exit 2 ;;
esac
python3 -B -O verification/independent_cubic_check.py
for document in paper journal; do
  printf 'Building %s\n' "$document"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" > "$document.build.log"
  bibtex "$document" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  printf 'Built %s.pdf\n' "$document"
done
