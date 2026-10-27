#!/bin/sh
# Replays the verification and builds paper.pdf.
#   sh build.sh            surplus certificate (Python + C) and counting facts, then the PDF
#   sh build.sh --full     additionally re-runs the published 7^3 strategy on all 24,359,523
#                          positions (about 10-60 CPU minutes)
#   sh build.sh --pdf      PDF only
set -eu
cd "$(dirname "$0")"
CC="${CC:-cc}"
mode="${1:-}"
case "$mode" in
  ""|--full|--pdf) ;;
  *) printf 'Usage: sh build.sh [--full|--pdf]\n' >&2; exit 2 ;;
esac
run_check() {
  checkLog="$1"
  shift
  printf 'Running %s\n' "$*"
  "$@" > "$checkLog" 2>&1 &
  checkPid=$!
  while kill -0 "$checkPid" 2>/dev/null; do
    printf 'Checking %s (%s)\n' "$checkLog" "$(date -u '+%H:%M:%S UTC')"
    tail -n 2 "$checkLog"
    sleep 15
  done
  if wait "$checkPid"; then
    tail -n 5 "$checkLog"
  else
    checkStatus=$?
    cat "$checkLog" >&2
    return "$checkStatus"
  fi
}
if [ "$mode" != "--pdf" ]; then
  cd verification
  mkdir -p results bin
  python3 -I obstruction6.py > results/obstruction6.log
  tail -n 1 results/obstruction6.log
  run_check results/surplus_python.log python3 -u -I surplus_certificate.py --workers "${WORKERS:-3}" --out results/surplus_python.json
  "$CC" -O2 -o bin/surplus7 surplus7.c
  run_check results/surplus_c_centre.txt ./bin/surplus7 1
  run_check results/surplus_c_noncentre.txt ./bin/surplus7 2
  if [ "$mode" = "--full" ]; then
    "$CC" -O2 -o bin/replicate_published replicate_published.c
    run_check results/replicate_noncentre.txt ./bin/replicate_published 2
    run_check results/replicate_centre.txt ./bin/replicate_published 1
  fi
  cd ..
fi
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
