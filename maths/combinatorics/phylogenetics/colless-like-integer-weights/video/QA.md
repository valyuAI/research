# Media QA

- Final video: 460.400 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 31 Cedar clips; maximum measured length 18.120 seconds. All are <=25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Visual inspection completed

Viewed the final boundary sheet and all 31 beat thumbnails, plus full-resolution frames c05 (weighted trees), c14 (corrected 576-leaf caption), c23 (busy exact-ratio plot) and end. Start, middle, end and every scene boundary were inspected. No clipping, overlapping labels or off-frame objects found in these samples. Partly drawn formulas in boundary samples are intentional Write animations and settle in beat samples. The ratio plot uses a labelled logarithmic scale. The silent preview contact sheet was inspected before final rendering; its stale 24-leaf caption was corrected to 576 and verified in final media.

Final runtime: 460.400 seconds (7:40.4). No subjective listening or real audience test was performed.
