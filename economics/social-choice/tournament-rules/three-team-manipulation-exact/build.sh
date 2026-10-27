#!/bin/sh
# Replays the exact certificate checks and builds paper.pdf.
#   sh build.sh          all certificates, including both n=8 rules
#   sh build.sh --quick  skip the large certificates (n=8, k=3 and n=7, k=4)
#   JOBS=3 sh build.sh   split each n=8 check into 3 parallel shards
set -eu
cd "$(dirname "$0")"
quick=0
case "${1:-}" in
  "") ;;
  --quick) quick=1 ;;
  *) printf 'Usage: sh build.sh [--quick]\n' >&2; exit 2 ;;
esac
mkdir -p verification/results
certs="n3_k3 n3_k3_mt n4_k3 n4_k3_mt n5_k3 n5_k3_mt n5_k3_mt_small n6_k3 n6_k3_mt n7_k3 n7_k3_mt"
if [ "$quick" -eq 0 ]; then certs="$certs n7_k4"; fi
for c in $certs; do
  python3 -B -O verification/verify_rule.py "verification/certificates/rule_$c.json" "verification/results/rule_$c.result.json"
done
if [ "$quick" -eq 0 ]; then
  jobs=${JOBS:-1}
  for c in n8_k3 n8_k3_mt; do
    if [ "$jobs" -le 1 ]; then
      python3 -B -O verification/verify_rule.py "verification/certificates/rule_$c.json" "verification/results/rule_$c.result.json"
    else
      run_dir=$(mktemp -d verification/results/shards.XXXXXX)
      i=0; parts=""; pids=""
      while [ "$i" -lt "$jobs" ]; do
        python3 -B -O verification/verify_rule.py "verification/certificates/rule_$c.json" "$run_dir/rule_$c.shard$i.json" "--shard=$i/$jobs" &
        pids="$pids $!"
        parts="$parts $run_dir/rule_$c.shard$i.json"; i=$((i + 1))
      done
      failed=0
      for pid in $pids; do
        if ! wait "$pid"; then failed=1; fi
      done
      if [ "$failed" -ne 0 ]; then printf 'FAIL: certificate worker failed\n' >&2; exit 1; fi
      python3 -B verification/combine_shards.py "verification/results/rule_$c.result.json" $parts
    fi
  done
fi
python3 -B verification/check_results.py $(if [ "$quick" -eq 1 ]; then printf -- '--quick'; fi)
labelled="n3_k3 n3_k3_mt n4_k3 n4_k3_mt n5_k3 n5_k3_mt n5_k3_mt_small"
if [ "$quick" -eq 0 ]; then labelled="$labelled n6_k3 n6_k3_mt"; fi
for c in $labelled; do
  python3 -B -O verification/verify_labelled.py "verification/certificates/rule_$c.json"
done
python3 -B -O verification/negative_tests.py verification/certificates/rule_n6_k3.json
python3 -B -O verification/negative_tests.py verification/certificates/rule_n6_k3_mt.json
printf 'Building paper\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
