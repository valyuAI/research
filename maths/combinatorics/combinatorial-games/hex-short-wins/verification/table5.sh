#!/usr/bin/env bash
# Certifies every entry of the 5x5 opening tables (paper, Figure 1).
# For an opening with value v: a Blue certificate at bound v and a Red
# certificate at bound v-1.  For an opening that loses ordinary Hex: a Red
# certificate for Hex_13(5), which is ordinary 5x5 Hex (Blue never places more
# than 13 stones), so Blue cannot connect at all.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
mkdir -p build gen5
[ -x build/hexmb4 ] || ${CC:-cc} -O3 -o build/hexmb4 src/hexmb4.c
# rows 1..5, '-' = loses ordinary Hex
D5="- - - - 8  - 8 9 7 10  - 9 7 9 -  10 7 9 8 -  8 - - - -"
L5="- - - - 7  - 8 8 7 8  - 9 6 9 -  8 7 8 8 -  7 - - - -"
fail=0
run() {  # mode bound opening expected-side
  local f
  CERT=gen5/n5$1$2 "$PY" progress.py build/hexmb4 5 "$1" "$2" "$3"
  if [ "$4" = blue ]; then f=gen5/n5$1$2_$3.txt; else f=gen5/n5$1$2_$3_red.txt; fi
  if [ ! -f "$f" ]; then echo "MISSING $f"; fail=1; return; fi
  if ! "$PY" replay.py py/check_cert.py "$f"; then fail=1; fi
}
read -ra D <<< "$D5"
read -ra L <<< "$L5"
for i in $(seq 0 24); do
  if [ "${D[$i]}" = "-" ]; then
    run D 13 "$i" red
  else
    run D "${D[$i]}" "$i" blue; run D $((D[$i] - 1)) "$i" red
    run L "${L[$i]}" "$i" blue; run L $((L[$i] - 1)) "$i" red
  fi
done
if [ "$fail" = 0 ]; then echo "TABLE CERTIFIED"; else echo "TABLE CHECK FAILED"; exit 1; fi
