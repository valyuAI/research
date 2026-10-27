# Four leaves that agree

Completed local video: **9:25.267** (565.267 seconds), native **1920x1080 at 30 fps**, **H.264/AAC**, using the accepted sharp potential bound. The narrated explainer starts with four leaves, follows the actual 13-leaf counterexample, explains why every triple on 14 leaves succeeds, and uses the integer 16/32 example to teach the shrinking-budget argument for many trees. The final script has 36 Cedar clips and seven editable Manim scenes. All 36 Cedar clips are measured at or below 18.504 seconds. The full media decode, source/audio correspondence, subtitles and visual checks pass; see `QA.md`. Subjective listening and full real-time playback were not performed.

## Rebuild

From this folder, using the existing environment:

```bash
V=${VIDEO_PYTHON:-python3}
PYTHONDONTWRITEBYTECODE=1 "$V" run_stage.py audio
PYTHONDONTWRITEBYTECODE=1 "$V" run_stage.py final
PYTHONDONTWRITEBYTECODE=1 nice -n 10 "$V" verify_media.py
PYTHONDONTWRITEBYTECODE=1 nice -n 10 "$V" verify_audio_alignment.py
```

The stage runner uses `nice -n 10`, streams heartbeats, and appends durable progress to the assigned lab status file. Audio generation reuses clips whose narration, voice and instructions match. Final rendering uses the existing shared Manim toolkit at native 1920x1080 and 30 fps. Run one render at a time. Re-run visual inspection after rebuilding; the technical audit alone does not inspect frames or listen to audio.

## Final artifacts

`video.mp4`, `subtitles.srt`, `poster.png` and `contact.png` are the final media and companion images. `QA.md` records the exact checks and their limits. `qa/` retains ffprobe output, full decode log, frame samples, audio alignment and signal statistics. The locked scientific manifest is copied to `scientific-completion-manifest.json`; all listed scientific hashes were verified against the final package.

## Editable inputs and evidence

- `scenes.py`: FourLeaves, Witness, Separating, GridArgument, Budget, ManyTrees, Evidence.
- `storyboard.md`, `narration.json`, `audio/`: teaching plan, exact narration, Cedar clips, measured durations and text/voice/instruction digests.
- `witness-data.json`: actual 13-leaf topology, drawing coordinates and checked selected quartet splits.
- `sources.md`: scientific claims, attribution and verification scope; `sharp-production-check.json`: production arithmetic cross-check.
- `draft-before-sharp-update/`: preserved old 3/16 source, audio and preview. `preview.mp4`, `witness-restriction-preview.mp4`, and `sharp-preview.mp4` are development previews, never final media.

## Scientific scope

The accepted factor is c=(7-sqrt(13))/18, with t=(sqrt(13)-1)/6 and beta=1/t=(1+sqrt(13))/2. The general upper bound is floor(3 beta^(k-1))+1. Its thresholds are guarantees, not exact values: h(3)=14 and 23<=h(4)<=28 remain the central small-case results. Relabel the smaller retained set X and the larger Y at every step.

Optimality applies only to the stated real-variable potential inequality. The irrational equality example is not presented as an exact finite tree. Lean checks the sharp inequality and its equality example; it does not formalise the tree model, iteration, DP/SAT, or h(3)=14. The two-case animation explains the crossing while leaving the checks of all three minimum terms to the written proof. The lower bound 2^k+2 is credited to Snir and Yuster. The unresolved 23-leaf searches provide no additional bound.

Narration uses a synthetic voice. No listening review is claimed.
