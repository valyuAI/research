#!/bin/sh
# Replays the fast verification steps and builds the PDF.
# Optional heavy steps:
#   sh build.sh --sat-hashes   regenerates the 135 CNF files of Lemma 3.3 and compares SHA-256 hashes
#   sh build.sh --game         recomputes the safe-pair tables of Theorem 2.9 (numpy) and checks the recursion
#                              against brute force on small trees
# The full certificate replay (CaDiCaL + DRAT-trim, a few CPU hours) is
#   CADICAL=/path/cadical DRAT_TRIM=/path/drat-trim python3 verification/sat/run_twotree_certificates.py
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
printf 'Replay started: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
HASHES=0; GAME=0
for arg in "$@"; do
  case "$arg" in
    --sat-hashes) HASHES=1 ;;
    --game) GAME=1 ;;
    *) printf 'Usage: sh build.sh [--sat-hashes] [--game]\n' >&2; exit 2 ;;
  esac
done
cd verification
python3 -E -B -u check_family.py --expect-common 0 families/triple13.nwk families/triple12.nwk families/triple11.nwk \
  families/quad22_k4.nwk
python3 -E -B -u check_family_edges.py families/triple13.nwk families/quad22_k4.nwk
python3 -E -B -u sym_triple.py
python3 -E -B -u sep_check.py families/triple13.nwk 3 4
python3 -E -B -u iterate_check.py
for u in 5 6 7; do python3 -E -B -u bipartition_check.py 14 $u --expect-shapes 135 --expect-bad 0; done   # Lemma 3.4 (about a minute)
python3 -E -B -u bipartition_check.py 13 5 --expect-shapes 66 --expect-bad 891
python3 -E -B -u bipartition_check.py 13 6 --expect-shapes 66 --expect-bad 0     # sharpness: 891 failures for |X| = 5, none for 6
python3 -E -B -u game/verify_exact_game.py game/thresholds_K6_N150.json 6  # Theorem 2.9 (standard library)
python3 -E -B -u caterpillar_family.py 6                                    # Proposition 4.1
if [ "$GAME" = 1 ]; then
  V="$(pwd)"; T="$V/results/game-replay-$(date -u +%Y%m%dT%H%M%SZ)"
  mkdir -p "$T"
  (cd "$T" && python3 -E -B -u "$V/game/exact_game.py" 5 70 6 && cmp thresholds_K5_N70.json "$V/game/thresholds_K5_N70.json" && printf 'recomputed table matches\n')
  printf 'Preserved generator output: %s\n' "$T"
  (cd game && python3 -E -B -u brute_dp_check.py)
fi
if [ "$HASHES" = 1 ]; then python3 -E -B -u sat/run_twotree_certificates.py --hash-only --workers 1; fi
cd ..
printf 'Building paper\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf at %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
