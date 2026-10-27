# Media QA

- Final video: 566.467 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 36 Cedar clips; maximum measured length 20.856 seconds. All are strictly shorter than 25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Manual visual inspection and final alignment

All 90 preview concept/transition frames were inspected. All 90 corrected final frames were inspected across six sheets, with the dense matrix, exact rate bars, eigenvalue zoom, determinant example, size bracket and prior-credit frames also viewed individually at native resolution. Final inspection found and fixed an eigenvalue tick label touching a point, a determinant caption that lagged its restored square, and an incorrectly typeset inequality in a credit footer. A fresh native render was then produced and the entire final QA rerun. Those three corrected frames were inspected again at native resolution; labels, points and footers are separated and readable.

The actual G11 rates and 11-by-11 matrix come from the finalized certificate. All eleven equilibrium equations and positive Hurwitz determinants are checked in `prepare_assets.py`. The numerical trajectory is explicitly a single small perturbation, not a basin theorem. The 8–11 bracket, vertex-minimal scope and prior hturcotte1/CLTN commit 3744200 credit are visible and narrated.

All 36 source MP3 clips match their expected positions in the final AAC soundtrack using normalized correlation of two-second waveform samples. Minimum correlation: 0.99935180; maximum timing offset: 0.02133333 seconds. Full results and clip SHA256 values are in `qa/audio-alignment.json`.

Muted Chrome playback passes start/middle/end seeking and advancement, native dimensions, 126 caption cues and all 36 transcript sections. Captions use the upper margin so source footers remain readable. `qa/browser-playback.json` and `qa/browser-player.png` record the test. Canonical source notes and research hashes are retained; no raw external article responses or signed URLs are shipped.

Confidence is high for checked scientific scope, exact examples, format, ordering and media integrity. No actual listening was performed, so subjective pronunciation and listening comfort remain unassessed. Captions are phrase-timed from measured clips, not word-aligned.

Browser caption follow-up: explicit line breaks at 60 characters prevent long cues from clipping horizontally. The local player was retested and its updated captioned screenshot inspected. Caption wording and measured timing are unchanged.
