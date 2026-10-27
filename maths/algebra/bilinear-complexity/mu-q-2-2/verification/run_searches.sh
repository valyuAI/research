#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec python3 -B run_searches.py
