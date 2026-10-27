# Why whole-number weights cannot recognise perfect symmetry

A narrated GCSE-level explanation of the 13-versus-13 collision, the asymmetric join with score zero, and the exact multinomial/pigeonhole proof for nonnegative common-unit weights at degrees 2, 3 and 4. The eight scenes are Trees, Weights, FalseZero, Recipes, Counting, Boxes, Crossing and Scope. Cedar narration is synthetic. Runtime and completed checks are recorded in QA.md after final verification; the research theorem and bounded originality assessment are distinguished on screen.

Open `video.mp4` for the final 1080p30 H.264/AAC film. `subtitles.srt` is a sidecar. Editable source is `scenes.py`, with `narration.json`, `storyboard.md` and `sources.md`. `audio/` holds the exact generated clips, measured durations and text digests. The silent `preview.mp4` and `preview-evidence/` are retained as development evidence, not final deliverables.

Rebuild from this folder using the existing environment:

```sh
V=${VIDEO_PYTHON:-python3}
"$V" run_stage.py audio
"$V" run_stage.py final
nice -n 10 "$V" verify_media.py
```

`run_stage.py` calls the shared Manim toolkit with nice 10, reports progress every 15 seconds and updates the assigned lab status file. No dependencies were installed. Only run one render at a time. Changing narration requires rerunning audio and final before QA; changing scenes requires final and QA. `qa/artifact-sha256.json` binds the completed media to its actual source and audio.

The scene explanation simplifies notation and omits the secondary example catalogue. It does not turn the exact recipe count into 27^m, impose an integer condition on f(0), claim a rank-two result, or present example checks as the universal proof. Subjective listening is not claimed; see QA.md for the precise audit scope.
