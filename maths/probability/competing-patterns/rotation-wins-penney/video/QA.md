# Media QA

- Final video: 590.367 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 35 Cedar clips; maximum measured length 19.752 seconds. All are <=25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Visual and claim inspection completed

Viewed final boundary sheet and all 35 beat thumbnails. Inspected individual frames p08 (both compatible orders), p14, p21 (overlapping fresh candidate windows), p29 (exact certificate table), p31 and the end card. Because the first p14 and p31 samples fell within transitions, extracted and viewed settled frames for p14, p26 and p31 as well. The cancellation reaches +1-1=0, the adverse-overlap bar leaves the stated positive scaled margin, and the horizon18 bound is complete and readable. No clipping, label collisions or off-frame objects found in inspected settled frames. Start, middle, end and both sides of each scene were inspected. Preview rotation endpoint was separately checked before final rendering.

The silent preview was inspected, then the cancellation endpoint and opaque subtraction colours were improved before the native final render. Every source/audio hash was generated after final encode. Scientific claims match the final paper and recorded verification: exact short cases, analytical k>=8, known length3, bounded moderate novelty, no optimality or Lean claim. The finite illustrations additionally pass mechanism_check.py; archived certificate arithmetic/coverage comparison passes. No fresh full C++ reconstruction is claimed by this video worker.

Final runtime: 590.367 seconds (9:50.367). No subjective listening or audience test was performed.
