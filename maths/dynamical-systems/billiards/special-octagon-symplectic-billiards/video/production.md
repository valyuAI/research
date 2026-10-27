# Special-octagon symplectic billiards: narrated explainer

[Watch video.mp4](video.mp4): **10:34.267**, native **1920 × 1080, 30 fps, H.264 video and AAC stereo narration**. The synthetic cedar voice is disclosed on the end card. This is an accessible proof outline for a viewer with GCSE maths, using the final research paper and the campaign's exact computations.

The running example is O(5,6,1,2). The film first teaches the parallel-line billiard rule on a rectangle, then explains why corner-born paths matter, how finitely many critical points force periodicity, and why the mirror prevents finer and finer fractions. It ends with the asymmetric counterexample, evidence and remaining questions.

## Claims and limits

- Every path means a path defined for all time, forwards and backwards. The lattice, direction and mirror assumptions are stated.
- In the example, 20 critical points lie among 26 allowed points. The proved bound is 2600; 92 is the largest reported sampled period, not an optimal universal bound.
- The filled set **has not closed after 20,000 sampled points**. This does not prove it infinite. The animation draws a prefix and reports the saved 20,000-point computation.
- The general argument uses side-sequence regions containing boxes; two return laps separate coordinates and four undo flips. The illustrated moving box is one exact example.
- The asymmetric animation illustrates forward contraction. The paper also proves that a suitable nudge has a backward-defined orbit; the displayed rational nudge alone does not certify that argument.
- The 1484 checks are parameter tuples, including rescaled copies. Correctness confidence is high after internal review; originality is less certain. There is no external peer review or proof-software formalization.

## Editable package

- [scenes.py](scenes.py): Manim animation source.
- [narration.json](narration.json): all 53 spoken clips; [audio/](audio/) contains their measured audio and cache manifest.
- [storyboard.md](storyboard.md): scene plan, prerequisites and comprehension audit.
- [sources.md](sources.md): scene-level evidence, citations and limitations.
- [subtitles.srt](subtitles.srt): synchronized captions; [poster.png](poster.png) and [contact.png](contact.png): final render previews.
- [check_numbers.py](check_numbers.py): exact on-screen calculations, using the package's verification library.
- [paper.tex](../paper.tex): complete mathematical arguments.

## Chapters

| Start | Scene |
|---|---|
| 00:00 | Hook |
| 00:17 | Billiards |
| 00:44 | Rule |
| 01:52 | Octagon |
| 02:55 | Corners |
| 03:41 | Boxes |
| 05:05 | Naive |
| 05:29 | Dots |
| 06:03 | Why |
| 07:42 | Conclude |
| 08:08 | Lopsided |
| 08:58 | Status |
| 10:00 | Ending |

## Rebuild locally

Run from the repository root, reusing the campaign environment. Existing audio is retained unless its text or voice instructions change. Audio generation requires the existing private credentials; never put them in source or command arguments.

    VIDEO_DIR=maths/dynamical-systems/billiards/special-octagon-symplectic-billiards/video
    VIDEO_PY=${VIDEO_PYTHON:-python3}
    nice -n 10 "$VIDEO_PY" -u "$VIDEO_DIR/check_numbers.py"
    "$VIDEO_PY" tools/video/make_audio.py "$VIDEO_DIR" --dry-run
    "$VIDEO_PY" tools/video/make_audio.py "$VIDEO_DIR"
    nice -n 10 "$VIDEO_PY" -u "$VIDEO_DIR/audit_layout.py"
    nice -n 10 "$VIDEO_PY" -u "$VIDEO_DIR/render_final.py"
    nice -n 10 "$VIDEO_PY" -u "$VIDEO_DIR/inspect_final.py"

Render sequentially with other campaign videos. The wrapper uses the existing shared tools/video/render.py at quality h and explicitly 30 fps, with UTC heartbeats. It writes video-1080p-candidate.mp4, leaving the delivered video.mp4 intact until the candidate has been inspected. Review the candidate's contact sheet, frames and validation before replacing the delivery file. The shared pipeline requires Manim 0.22.0, ffmpeg and the installed TeX packages.

## Validation and provenance

The actual encoded output was checked with ffprobe; 53 clip hashes match the current narration, measured durations match, every clip appears once, and speech timing has no overlap or truncation. The exact numerical checker passed. The final contact sheet and ten individual frames were visually inspected, including start, middle, end, the four-lap argument, filled-set caveat, half-grid proof, asymmetric offsets and originality statement. This samples the animation; it is not a frame-by-frame review.

Receipts: [validation.json](audit/validation.json), [ffprobe.json](audit/ffprobe.json), [scene-index.json](audit/scene-index.json), [render log](audit/render-1080p.log), [number checks](audit/numbers-validation.log), [inspected frames](audit/frames/). No listening review or audience test was performed. Stream and timing checks do not establish pronunciation quality.

The incoming 480p preview and original editable files remain in ignored audit/intake/. Superseded audio remains in audio/.stale/. Unchanged narration reused 39 original clips; 14 clips were changed or added. Primary-source extracts remain local in ignored audit/private-cache/. No paper, prior review or shared toolkit was edited. No publication was performed.

Full video and audio decoding also passed with ffmpeg -xerror -err_detect explode; [decode receipt](audit/decode-validation.json) and [streaming decode log](audit/decode-validation.log) are retained. Caption text was checked against every narration clip. The checked candidate was promoted to video.mp4 only after confirming that the preserved 480p intake copy matched the previous delivery. SHA-256 and actual final-file ffprobe checks confirm the delivery is the reviewed encode.
