#!/bin/sh
set -eu
cd "$(dirname "$0")"
case "${1:-}" in
  "") ;;
  --redraw-figure) python3 -B plot_polytope.py ;;
  *) printf 'Usage: sh build.sh [--redraw-figure]\n' >&2; exit 2 ;;
esac
python3 -B -O verification/independent_verification.py
python3 -B -O verification/negative_verification_checks.py
for document in paper journal; do
  printf 'Building %s\n' "$document"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" > "$document.build.log"
  bibtex "$document" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  printf 'Built %s.pdf\n' "$document"
done
