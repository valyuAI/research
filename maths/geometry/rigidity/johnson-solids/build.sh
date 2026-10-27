#!/bin/sh
# Stream every check, preserve logs, and stop on the first failure.
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
exec nice -n 10 python3 -B -u verification/run_build.py "$@"
