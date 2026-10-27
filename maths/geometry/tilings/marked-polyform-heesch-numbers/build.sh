#!/bin/sh
# Replays the standard-library checks and builds the PDF.
#   sh build.sh            check witnesses (incl. negative tests), Basic's patch, results ledger; build paper.pdf
#   sh build.sh --cnf      also regenerate every base CNF and compare SHA-256 with the ledger (needs python-sat)
#   sh build.sh --drat     also re-solve the small CNFs with cadical and check DRAT proofs with drat-trim
#   sh build.sh --figures  redraw the figures (needs matplotlib)
set -eu
cd "$(dirname "$0")"
MODE="${1:-}"
case "$MODE" in
  ""|--cnf|--drat|--figures) ;;
  *) printf 'Usage: sh build.sh [--cnf|--drat|--figures]\n' >&2; exit 2 ;;
esac
python3 -B verification/check_marked.py verification/witnesses/*.json
python3 -B verification/negative_tests.py
python3 -B verification/audit_basic_boundary.py
python3 -B verification/check_ledger.py
python3 -B verification/negative_ledger.py
python3 -B verification/check_crosschecks.py
case "$MODE" in
  --cnf) python3 -B verification/regenerate_cnfs.py ;;
  --drat) python3 -B verification/regenerate_cnfs.py --drat-max-clauses 2000000 ;;
  --figures) python3 -B plot_figures.py ;;
esac
python3 -B verification/make_tables.py
printf 'Building paper\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
