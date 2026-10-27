#!/bin/sh
# Replays the certificates and builds paper.pdf.
#   sh build.sh        shipped 5x5 certificates, mutation tests, figures, PDF (minutes)
#   sh build.sh full   also regenerates and replays the 6x6 and strict certificates (hours)
set -eu
cd "$(dirname "$0")"
case "${1:-}" in
  "") mode=quick ;;
  full) mode=full ;;
  *) printf 'Usage: sh build.sh [full]\n' >&2; exit 2 ;;
esac
bash verification/run_checks.sh "$mode"
python3 -B verification/negative_checks.py
python3 -B verification/strict_controls.py
python3 -B verification/check_records.py
if [ "$mode" = full ]; then bash verification/table5.sh; fi
python3 -B verification/py/make_figures.py .
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
