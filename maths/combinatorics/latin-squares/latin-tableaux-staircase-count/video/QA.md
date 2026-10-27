# Media QA

- Final video: 486.733 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 32 Cedar clips; maximum measured length 19.848 seconds. All are <=25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Visual inspection, 26 October 2026

Inspected every final narration-beat sample, both sides of all seven scene boundaries, and native frames l17, l22 and end. Preview inspection caught and corrected a column-clash example that had changed the row's permitted numbers, an invariant highlight that moved without its digit, and digit occlusion during a swap. The final tableau preserves valid row permutations in the clash demonstration; both large digits remain visible after the swap. The four explicitly displayed extension rows agree with check_examples.py. Forced middle entries, two independent swaps, restored safeguards, the576 base count and9*4^(k-3) formula are legible. Priority and the independent-verification scope remain explicit. No unresolved clipping or layout defect found. Near-empty scene-start frames are the opening of intentional Create/Write animations, not missing media.

Muted browser playback of the actual final MP4 passed at beginning, middle and end: time advanced after seeks to5,243.367 and480.733 seconds, native1920x1080, readyState4, no media error. See qa/browser-playback.json. An in-memory Blob supplies seeking because the temporary simple HTTP server lacks byte ranges. No listening or full real-time playback is claimed.

Caption completeness check passed: all narration words appear in order across 112 nonoverlapping cues, ending at 486.341 seconds within the final runtime. See qa/subtitles-check.json. Cue timing remains phrase-based.

All32 final narration waveforms match their scheduled source clips. Minimum normalized correlation 0.983415; maximum absolute timing offset 0.021375 seconds. See qa/audio-alignment.json. The final contact sheet and native clash-l05 frame were also inspected. This is a signal comparison, not listening.
