# Which Johnson solids can wobble?

A narrated GCSE-level explanation of the fixed-edge-length, planar-face model: a shearing cube, the actual certified J3 cupola flex, coordinate addition, a square-pyramid obstruction, first-order versus second-order rigidity, and the complete 41 + 6 versus 45 classification. About nine minutes, Cedar synthetic narration, native 1920x1080 at 30 fps with H.264 video and AAC audio. The companion source ledger states the local-rigidity and novelty limits. See `QA.md` for the final measured runtime and verification, including the explicit absence of a listening review.

- Play `video.mp4`; `subtitles.srt` supplies external subtitles.
- Edit `scenes.py` for animation and `write_story.py` for narration/storyboard, then regenerate the JSON and Markdown with that script. `narration.json` contains the exact spoken script.
- `audio/` contains all 36 clips, measured durations and provenance manifests.
- `geometry.json` freezes display data derived from the accepted J3 certificate. `prepare_assets.py` replays that certificate and verifies the animation sample range without writing to research/checker folders.
- `poster.png`, `contact.png` and `qa/boundary-contact.png` are inspectable stills. `preview.mp4` and `qa/preview-*` preserve the earlier preview and its corrected defects.

Rebuild from this existing worktree, one render at a time:

```sh
V=${VIDEO_PYTHON:-python3}
T="$(git rev-parse --show-toplevel)/tools/video"
D="$(git rev-parse --show-toplevel)/maths/geometry/rigidity/johnson-solids/video"
$V -B "$D/prepare_assets.py"
$V -B "$D/write_story.py"
$V "$T/make_audio.py" "$D"
nice -n 10 "$V" -B "$D/build.py" --quality h
nice -n 10 "$V" -B "$D/qa_media.py"
```

No new dependencies were installed. The existing shared runtime is read-only. The independent coordinator audit of the research package remains separate from this production QA.
