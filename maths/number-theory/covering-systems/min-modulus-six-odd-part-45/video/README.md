# Min modulus six odd part 45

Accessible narrated mathematical explainer, **8:55**, built from GCSE foundations with concrete examples and animated proof mechanics. Native 1920x1080 at 30fps, H.264/AAC, 33 built-in Cedar clips, all under 25s. See [video](video.mp4), [captioned local player](preview.html), [storyboard](storyboard.md), [sources](sources.md) and [QA](QA.md). No listening was performed; machine audio validation and explicit visual inspection are documented.

## Editable files

`scenes.py` defines 7 ordered Manim scenes: ClockCover, RemainderBoards, Doubling, Prices, TheTrap, ExactEnumeration, FiniteAndInfinite. `narration.json` is the exact speech script. `audio/` contains the final MP3 clips, measured durations and model/voice/text digests. `subtitles.srt` and `subtitles.vtt` supply English captions. `poster.png` and `contact.png` use inspected settled frames. Scientific-input hashes are frozen before production.

## Rebuild

Use the existing environment and toolkit; do not migrate the project or edit scientific inputs:

```sh
V=${VIDEO_PYTHON:-python3}
"$V" -B run_stage.py preview
"$V" -B run_stage.py dry-audio
"$V" -B run_stage.py audio
"$V" -B run_stage.py final
"$V" -B run_stage.py qa
"$V" -B run_stage.py alignment
```

Run from this video folder. The wrapper applies nice 10, single-thread BLAS variables and flushed 15-second heartbeats. Every final render holds the shared advisory flock at `$VIDEO_RENDER_LOCK` (default `/tmp/valyu-research-final-render.lock`), acquired nonblocking with wait heartbeats; the lock file is never removed or replaced. The lock spans the entire final-render subprocess, including concatenation.

The audio stage calls the existing secure `tools/video/make_audio.py` wrapper, reading credentials through the process environment or a local, untracked environment file. No credential belongs in this folder. It regenerates only changed clips. Measure them before final rendering; `verify_media.py` rejects any clip >=25s.

If this folder has `prepare_witness.py` or `prepare_geometry.py`, run it with the same interpreter to regenerate exact visual input data from the locked local witnesses. ACR's `trajectory-data.json` contains labelled illustrative numerical paths, not a stability proof. Re-rendering requires a fresh visual inspection record before running `finish_package.py`. The existing `qa/visual-inspection.json` applies only to the shipped final artifact hashes. After a rebuild, inspect the final beat and boundary sheets plus full-resolution critical frames, replace that inspection record, then run `"$V" -B finish_package.py` to refresh the poster, contact sheet, QA document and completion record. If you edited scenes, narration or visual input data, refresh `render-input-sha256.json` before rendering.

No publication, contact, commit or push is part of this rebuild procedure.
