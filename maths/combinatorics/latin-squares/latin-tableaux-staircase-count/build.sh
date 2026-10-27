#!/bin/sh
set -eu
cd "$(dirname "$0")"
case "${1:-}" in
  "") python3 -B -O verification/check_latin.py 7 7 ;;
  --full) python3 -B -O verification/check_latin.py 9 8 ;;
  --pdf-only) ;;
  *) printf 'Usage: sh build.sh [--full | --pdf-only]\n' >&2; exit 2 ;;
esac
printf 'Building paper\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
