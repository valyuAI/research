# Media QA

- Final video: 553.167 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 36 Cedar clips; maximum measured length 18.120 seconds. All are strictly shorter than 25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Manual visual inspection and final alignment

All 90 preview concept/transition frames and all 90 corrected final frames were visually inspected across six sheets per render. Native frames for the rank bounds, four order-30 graphs, W5/X uniqueness and proof structure were also inspected individually. The reduced-graph teaching example was clarified after final inspection: equal rows are explicitly labelled as not reduced, then the matrix transforms into the two-vertex reduced example. The corrected native movie was rendered again under the shared campaign lock, followed by fresh decode, timing, alignment and visual QA. Both sides of the corrected reduction were inspected at native resolution. No visible clipping or unintended overlap remains in the inspected frames.

The film animates neighbour sums, signed eigenvectors, duplicate cancellation, induced cores, the one/two-vertex extension rule, empty-level stopping, compatible reconstruction and both doubling variants. Exact W5/X adjacency and inertia, the four order-30 classes and edge counts, and all rank maxima come from the finalized research inputs. ACK's prior four rank-eight classes and CFJK's prior numerical bound are credited explicitly. Higher-rank exclusion and uniqueness are distinguished from these prior results. The film does not claim a proof-assistant formalisation or a theorem for five negative eigenvalues.

All 36 source MP3 clips match their expected final AAC positions. Minimum normalized two-second waveform correlation: 0.99937370; maximum timing offset: 0.02133333 seconds. Full hashes and alignment records are in `qa/audio-alignment.json`.

Muted Chrome playback verifies native dimensions, seeking and advancement near the beginning, middle and end, 121 caption cues and 36 transcript sections. Browser captions wrap at 60 characters and occupy the upper margin to preserve the source footers. The final screenshot was visually inspected. Canonical references and claim-specific notes are shipped; raw article responses and signed URLs are not retained.

Confidence is high for the checked scope, exact examples, native format, ordering and media integrity. No actual listening was performed: subjective pronunciation and listening comfort remain unassessed. Captions use measured clip durations and phrase timing rather than word alignment.
