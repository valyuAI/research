# Media QA

- Final video: 542.433 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 34 Cedar clips; maximum measured length 20.904 seconds. All are <=25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Visual inspection, 26 October 2026

Inspected the final contact sheet, all 34 narration-beat samples and both sides of all nine scene boundaries, plus native settled frames t20, t27, t30 and t31. The repaired Hall shortage expands its reachable-cell outline from two to three cells. The deletion illustration reroutes assignments to four surviving cells and updates the surplus caption to zero. The central histogram preserves the >=4 lower bounds; the noncentral total is48,960 with exact surplus3. The axis transformations preserve opposite signs, and the six-cube count shows46<47 without claiming that the open game is solved. Native labels, symbols, end card and Lean scope are legible and in frame. No unresolved clipping or layout defect found. Initial Create/Write frames and fading transitions are intentionally incomplete; the settled mechanism states were also inspected.

No subjective listening or full real-time playback was performed.

Muted browser playback of the actual final MP4 passed at beginning, middle and end: time advanced after seeks to5,271.217 and536.433 seconds, native1920x1080, readyState4, no media error. See qa/browser-playback.json. An in-memory Blob supplies seeking because the temporary simple HTTP server lacks byte ranges. No listening or full real-time playback is claimed.

All34 final narration waveforms match their scheduled source clips. Minimum normalized correlation 0.981456; maximum absolute timing offset 0.021375 seconds. See qa/audio-alignment.json. This is a signal comparison, not listening.

Caption completeness check passed: all narration words appear in order across 124 nonoverlapping cues, ending at 542.060 seconds within the final runtime. See qa/subtitles-check.json. Cue timing remains phrase-based.
