#!/bin/sh
# Replay the verification and build the paper.
#   sh build.sh          quick replay (octagon parameters <= 8, a few minutes) and build
#   sh build.sh --full   full replay (parameters <= 14 for both octagon programs, implementation
#                        comparison <= 10, Hexhouses <= 11, asymmetric exploration; several hours)
# Every check writes its full output to a log in $LOGDIR and the build stops if any check exits
# with a nonzero status or prints a RESULT FAIL line.
set -eu
cd "$(dirname "$0")"
N=8
FAMILIES=0
case "${1:-}" in
  "") ;;
  --full) N=14; FAMILIES=1 ;;
  *) printf 'Usage: sh build.sh [--full]\n' >&2; exit 2 ;;
esac
LOGDIR="${TMPDIR:-/tmp}/special-octagon-build.$$"
mkdir -p "$LOGDIR"

# run NAME LINES CMD...: run CMD, keep its output in $LOGDIR/NAME.log, fail on nonzero exit or
# on a FAIL line, then show the last LINES lines.
run() {
  name=$1; lines=$2; shift 2
  status=0
  "$@" > "$LOGDIR/$name.log" 2>&1 || status=$?
  if [ "$status" -ne 0 ] || grep -q 'FAIL' "$LOGDIR/$name.log"; then
    tail -20 "$LOGDIR/$name.log" >&2
    printf 'build.sh: check %s failed (exit status %s); log: %s/%s.log\n' "$name" "$status" "$LOGDIR" "$name" >&2
    exit 1
  fi
  tail -"$lines" "$LOGDIR/$name.log"
}

cd verification
run S_count 1 python3 -B check_S_count.py
run independent 1 python3 -B independent_octagon_check.py "$N"
if [ "$N" = 14 ]; then
  run octagons 2 python3 -B check_octagons.py 14 octagon_results.json
else
  run octagons 2 python3 -B check_octagons.py "$N" "$LOGDIR/octagon_results_quick.json"
fi
run filled_set 5 python3 -B filled_set.py
run asymmetric 1 python3 -B asymmetric_octagon_check.py
if [ "$N" = 14 ]; then
  run hexhouses 2 python3 -B check_symmetric_hexhouses.py 11
  run compare 1 python3 -B compare_implementations.py 10
else
  run hexhouses 2 python3 -B check_symmetric_hexhouses.py 6
  run compare 1 python3 -B compare_implementations.py 6
fi
if [ "$FAMILIES" = 1 ]; then
  run families 1 python3 -B check_other_families.py 11
  run asymmetric_cap 4 python3 -B asymmetric_cap_check.py
fi
cd ..
run figure 0 python3 -B plot_figure.py
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'All checks passed; logs in %s. Built paper.pdf\n' "$LOGDIR"
