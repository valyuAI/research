#!/bin/sh
set -eu
cd "$(dirname "$0")"
run_python_checks() {
  mkdir -p verification/logs
  replay_log="verification/logs/verify_$(date -u +%Y%m%dT%H%M%SZ).txt"
  python3 -B -O verification/verify.py "$@" > "$replay_log" 2>&1 &
  replay_pid=$!
  printf 'Python verification started, log: %s\n' "$replay_log"
  while kill -0 "$replay_pid" 2>/dev/null; do
    sleep 20
    if kill -0 "$replay_pid" 2>/dev/null; then
      printf 'Python verification still running\n'
      tail -n 2 "$replay_log"
    fi
  done
  if wait "$replay_pid"; then
    cat "$replay_log"
  else
    replay_status=$?
    cat "$replay_log" >&2
    return "$replay_status"
  fi
}
case "${1:-}" in
  "") run_python_checks ;;
  --full) run_python_checks --full; sh verification/run_searches.sh ;;
  --compiled-only) sh verification/run_searches.sh ;;
  --pdf-only) ;;
  *) printf 'Usage: sh build.sh [--full | --compiled-only | --pdf-only]\n' >&2; exit 2 ;;
esac
printf 'Building paper\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
