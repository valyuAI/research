#!/usr/bin/env bash
# Rebuild the explainer video for this finding.
#   ./build.sh          numbers, narration (changed clips only), final 1080p render
#   ./build.sh preview  quick 480p15 layout check (writes preview_l.mp4)
# Set V to a Python 3.12 with manim 0.22, numpy and openai (the collection's video env).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOLS="$(cd "$HERE/../../../../../tools/video" && pwd)"
V="${V:-python3}"

"$V" "$HERE/data_prep.py"
if [[ "${1:-}" == "preview" ]]; then
  nice -n 10 "$V" "$TOOLS/render.py" "$HERE" --quality l --contact --output preview_l.mp4
  exit 0
fi
"$V" "$TOOLS/make_audio.py" "$HERE"
nice -n 10 "$V" "$TOOLS/render.py" "$HERE" --quality h --contact
