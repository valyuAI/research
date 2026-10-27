#!/bin/sh
set -eu
cd "$(dirname "$0")"
case "${1:-}" in
  "") ;;
  --redraw-figure) python3 -B plot_counterexample.py ;;
  *) printf 'Usage: sh build.sh [--redraw-figure]\n' >&2; exit 2 ;;
esac
python3 -B -O verification/check_short_lag.py
for document in paper journal; do
  printf 'Building %s\n' "$document"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" > "$document.build.log"
  bibtex "$document" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  printf 'Built %s.pdf\n' "$document"
done
