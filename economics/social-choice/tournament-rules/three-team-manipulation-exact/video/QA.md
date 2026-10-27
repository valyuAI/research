# Media QA

- Final video: 452.100 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 32 Cedar clips; maximum measured length 18.048 seconds. All are strictly shorter than 25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Manual visual inspection and final alignment

All 80 preview frames and all 80 final concept/transition frames were visually inspected across five sheets for each render. Native final frames s07, s16, s20 and s32 were also inspected individually. The final row of exact probabilities is legible; the two-fifths border fits its expression; the closing paper title fits the frame. Every scene transition and both sampled moments of every narration beat are represented. No visible clipping or unintended overlap was found. Source labels stay adjacent to the claims.

The final soundtrack was independently matched against all 32 source MP3 clips using normalized correlation of two-second waveform samples at their expected timeline positions. Minimum correlation was 0.99211 and maximum timing offset was 0.02134 seconds, consistent with AAC encoding delay. Full per-clip hashes and results are in `qa/audio-alignment.json`.

Muted playback in installed Chrome verified native dimensions, seeking and advancing playback near the start, middle and end. All 107 caption cues load; the full transcript has 32 sections. Results and a screenshot are in `qa/browser-playback.json` and `qa/browser-player.png`. Browser captions use the top margin so lower source labels remain visible. The first T3 browser attempt timed out twice; the fallback used a fresh headless Chrome context, without user profile or login access. The test server supports HTTP byte ranges so seeking is actually verified.

Confidence is high for the checked scientific scope, exact examples, native format, clip ordering and media integrity. Subjective pronunciation and listening comfort remain unassessed: no actual listening was performed. Captions follow measured clip durations but are phrase-timed, not word-aligned.

Browser caption follow-up: explicit line breaks at 60 characters prevent long cues from clipping horizontally. The local player was retested and its updated captioned screenshot inspected. Caption wording and measured timing are unchanged.
