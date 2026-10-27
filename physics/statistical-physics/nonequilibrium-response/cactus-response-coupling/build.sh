#!/bin/sh
set -eu
cd "$(dirname "$0")"
case "${1:-}" in
  "") ;;
  --numerics) python3 -B verification/numerical_evidence.py ;;
  *) printf 'Usage: sh build.sh [--numerics]\n' >&2; exit 2 ;;
esac
python3 -B verification/check_cactus_lemmas.py
python3 -B verification/check_k4_obstruction.py
python3 -B verification/check_k4_subdivision.py
printf 'Building paper\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
