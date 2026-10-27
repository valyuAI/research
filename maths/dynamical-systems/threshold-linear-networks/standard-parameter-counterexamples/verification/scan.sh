#!/bin/sh
# Complete, count-checked scan; scan.py checks all pipeline exit statuses.
set -eu
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" -u -B scan.py "${1:-6}"
