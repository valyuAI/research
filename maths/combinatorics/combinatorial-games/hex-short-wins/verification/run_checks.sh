#!/usr/bin/env bash
# Replays the Hex certificates with the independent Python checkers.
#
#   ./run_checks.sh          5x5 certificates shipped in certs/ (a few minutes)
#   ./run_checks.sh full     also regenerates and replays the 6x6 certificates
#                            and the strict 5x5 certificate (several hours)
#
# Certificates for 6x6 and for the strict game are too large to ship
# (up to 122 MB); the solver in src/ regenerates them deterministically and the
# checker, which shares no code with the solver, replays them.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
CC=${CC:-cc}
mode=${1:-quick}
fail=0

# check CHECKER FILE: replay FILE and require that the checker verified exactly
# the game, opening and side named by the file name.
check() {
  if ! "$PY" replay.py py/"$1" "$2"; then fail=1; fi
}

echo "== 5x5, Campbell's game Hex(5,l): Red holds Hex(5,5) after every opening"
for i in $(seq 0 24); do check check_cert.py certs/n5L5_${i}_red.txt.gz; done
echo "== 5x5: Blue wins Hex(5,6) opening in the centre; Red holds it after every other opening"
check check_cert.py certs/n5L6_12.txt.gz
for i in $(seq 0 24); do [ "$i" = 12 ] || check check_cert.py certs/n5L6_${i}_red.txt.gz; done
echo "== 5x5, Hex_d(5): Red holds Hex_6(5) after every opening"
for i in $(seq 0 24); do check check_cert.py certs/n5D6_${i}_red.txt.gz; done
echo "== 5x5: Blue wins Hex_7(5) from (3,3), (2,4), (4,2); Red holds it after the other openings"
for i in $(seq 0 24); do
  if [ -f certs/n5D7_${i}.txt.gz ]; then check check_cert.py certs/n5D7_${i}.txt.gz
  else check check_cert.py certs/n5D7_${i}_red.txt.gz; fi
done

if [ "$mode" = full ]; then
  mkdir -p build gen
  "$CC" -O3 -o build/hexmb4 src/hexmb4.c
  "$CC" -O3 -o build/hexstrict2 src/hexstrict2.c
  echo "== 6x6: regenerate Red certificates for Hex_9(6), all 36 openings"
  CERT=gen/n6D9 "$PY" progress.py build/hexmb4 6 D 9 $(seq 0 35)
  for i in $(seq 0 35); do check check_cert.py gen/n6D9_${i}_red.txt; done
  echo "== 6x6: regenerate the Blue certificate for Hex_10(6) from (3,4) (index 15)"
  CERT=gen/n6D10 "$PY" progress.py build/hexmb4 6 D 10 15
  check check_cert.py gen/n6D10_15.txt
  echo "== 6x6: regenerate Red certificates for Hex(6,7), all 36 openings"
  CERT=gen/n6L7 "$PY" progress.py build/hexmb4 6 L 7 $(seq 0 35)
  for i in $(seq 0 35); do check check_cert.py gen/n6L7_${i}_red.txt; done
  echo "== 5x5 strict game: regenerate the Blue certificate for the centre opening"
  CERT=gen/strict5_6 "$PY" progress.py build/hexstrict2 5 6 12
  check check_strict.py gen/strict5_6_12.txt
  echo "== compare regenerated certificates with the hashes of the original runs (informational)"
  "$PY" - <<'PYEOF'
import hashlib
for line in open("certs/SHA256SUMS-generated"):
    want, name = line.split()
    try:
        got = hashlib.sha256(open("gen/" + name, "rb").read()).hexdigest()
    except FileNotFoundError:
        print(f"{name}: not regenerated")
        continue
    print(f"{name}: {'same as original run' if got == want else 'differs from original run (replayed above)'}")
PYEOF
fi

if [ "$fail" = 0 ]; then echo "ALL CHECKS PASSED"; else echo "SOME CHECKS FAILED"; exit 1; fi
