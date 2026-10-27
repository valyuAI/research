# Spare cells beat unknown moves

Completed local narrated video: **9:02.433** (542.433 seconds), native **1920x1080 at 30 fps**, H.264 video and AAC audio. A concrete pairing defence, cube lines, Hall matching, surplus and deletion robustness, central and noncentral openings, the opposite-octant correction, and the six-cube obstruction. This is a new short proof of the known seven-cube theorem. Six-cube and five-cube remain open; Lean covers the abstract lemmas, not the actual board enumeration or whole game.

The editable package has 9 Manim scenes and 34 Cedar clips. Every narration clip is measured below 25 seconds; the longest is 20.904 seconds. `QA.md` records full decode, frame inspection and timing evidence. Waveform matching finds every source clip at its scheduled position (minimum correlation 0.981456, largest absolute offset 0.0214 seconds). This verifies audio correspondence, not pronunciation. **No listening review or full real-time playback is claimed.**

- Play `video.mp4`, or open `preview.html` for a local player. External subtitles are `subtitles.srt` and `subtitles.vtt`.
- Edit `write_story.py` for the spoken script and storyboard, then regenerate `narration.json` and `storyboard.md`.
- Edit `scenes.py` for animation. Scene order: Pairing, Cube, Matching, Surplus, Central, Noncentral, Correction, SixCube, Scope.
- `audio/` contains source clips, measured durations and narration digests. `sources.md` and `source-snapshot.json` record scientific provenance and scope.
- `poster.png`, `contact.png`, `qa/beats.png` and `qa/boundaries.png` support visual review. `preview.mp4` is the development preview, not the final.
- `check_examples.py` independently verifies displayed examples and writes only `example-checks.json`. It does not repeat the expensive research enumerations.

Rebuild from this folder using the existing environment, one heavy stage at a time:

```sh
V=${VIDEO_PYTHON:-python3}
"$V" -B write_story.py
"$V" -B check_examples.py
"$V" -B run_stage.py preview
# Inspect the preview before proceeding.
"$V" -B run_stage.py dry-audio
"$V" -B run_stage.py audio
"$V" -B run_stage.py final
"$V" -B run_stage.py qa
"$V" -B run_stage.py alignment
"$V" -B finish_package.py
```

`run_stage.py` uses nice10, single-thread BLAS settings, 15-second progress and local stage logs. Final renders acquire a shared advisory `final-render.lock` for their full subprocess lifetime, with 15-second wait heartbeats. The lock is never unlinked. The shared `tools/video/` runtime remains read-only. Audio generation reads API credentials from the process environment and regenerates only changed clips. A clean rebuild's first preview is silent and uses estimated timings; after audio exists, preview timings follow measured clips. Reinspect frames after edits; automated QA does not perform visual or listening review.

Narration uses a synthetic voice.
