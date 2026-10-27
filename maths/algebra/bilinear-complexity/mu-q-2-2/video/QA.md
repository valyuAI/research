# Media QA

- Final video: 504.233 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 32 Cedar clips; maximum measured length 20.304 seconds. All are <=25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Visual inspection, 26 October 2026

Inspected the full final contact sheet, every narration-beat sample in qa/beats.png, and the before/after scene boundary sheet in qa/boundaries.png. Native individual frames a10, a24 and end were inspected for labels, coefficients, field-size scope and end-card readability. The frame samples contain intentional Create/Write/Transform transitions; settled states are legible and remain in frame. The corrected Karatsuba rectangle removes areas8 and15 in the right proportions. The four exact target grids, q5 counts, final field table, binary ring cancellation and attribution/Lean limits match the accepted scientific inputs. Near-black scene-start frames are the initial frames of deliberate fades, not missing media. No clipping or unresolved layout defect found.

The final audio waveform audit passes for all32 clips; see qa/audio-alignment.json. No subjective listening or full real-time playback was performed.

Muted browser playback succeeded at beginning, middle and end: time advanced after seeks to5,252.117 and498.233 seconds, videoWidth1920/videoHeight1080, readyState4 and no media error. See qa/browser-playback.json. Seeking uses an in-memory Blob because the temporary simple HTTP server does not implement byte ranges. No listening or full real-time playback is claimed.

Caption completeness check passed: all narration words appear in order across 115 nonoverlapping cues, ending at 503.834 seconds within the final runtime. See qa/subtitles-check.json. Cue timing remains phrase-based.
