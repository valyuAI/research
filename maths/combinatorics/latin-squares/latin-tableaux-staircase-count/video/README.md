# Four new ways, every time

Completed local narrated video: **8:06.733** (486.733 seconds), native **1920x1080 at 30 fps**, H.264 video and AAC audio. Latin squares and staircase tableaux, one exact six-to-seven-column extension, forced entries, two independent swaps, invariant preservation and induction. This is an independent verification note; the earlier 22 October 2026 proof has priority.

The editable package has 7 Manim scenes and 32 Cedar clips. Every narration clip is measured below 25 seconds; the longest is 19.848 seconds. `QA.md` records full decode, frame inspection and timing evidence. Waveform matching finds every source clip at its scheduled position (minimum correlation 0.983415, largest absolute offset 0.0214 seconds). This verifies audio correspondence, not pronunciation. **No listening review or full real-time playback is claimed.**

- Play `video.mp4`, or open `preview.html` for a local player. External subtitles are `subtitles.srt` and `subtitles.vtt`.
- Edit `write_story.py` for the spoken script and storyboard, then regenerate `narration.json` and `storyboard.md`.
- Edit `scenes.py` for animation. Scene order: Rules, Grow, ForcedMiddle, FourWays, Invariants, Induction, Scope.
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
