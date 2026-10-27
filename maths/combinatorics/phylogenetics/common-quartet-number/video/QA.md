# Media QA

- Final video: 565.267 seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- 36 Cedar clips; maximum measured length 18.504 seconds. All are <=25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.

## Final visual inspection

Inspected both final-media sheets (`qa/boundaries.png`, `qa/beats.png`): start, middle, end, both sides of all seven scene boundaries, and all 36 narration beats. Also opened full-resolution frames for the actual witness paths and the three restricted quartets, failed-diagonal argument, 98/99 calculation, 96.553 guarantee, two-case crossing, Lean scope, beta formula, six-value table, 16-to-14 / 37-to-28 comparison, four-tree interval and end card. No clipped text, unintended overlap or illegible principal formulas found in those frames. The q08 automatic sample lands in a transition; `q08-paths.png` and `q08-pairings.png` show both settled states. Partially written formulas in automatic samples were checked again at settled times, retained in `qa/additional-frame-times.json` and `qa/q28-table.png`.

The graph shows the algebraic crossing of x squared and (1-x)/3; it is not a plot of every possible retained tree budget. The spoken explanation leaves the checks of all three minimum terms to the paper. The counter animation summarizes the saved exhaustive witness check rather than claiming a live replay. These are deliberate explanatory simplifications. No full real-time playback, listener evaluation or audience test was performed.

## Audio correspondence and subtitle checks

All 36 source clips were compared with their expected final-media positions using central six-second waveform intervals decoded to mono 8kHz. Minimum normalized correlation: 0.984226; maximum absolute timing offset: 0.021375 seconds. All passed the 0.95 correlation / 0.3-second limits. This confirms clip presence and alignment, not subjective pronunciation or listening quality. See `qa/audio-alignment.json` and its log. Measured final signal mean -26.2 dB, peak -5.5 dB; no clipping detected by peak measurement.

Subtitles contain 129 chronological, nonoverlapping cues whose concatenated text exactly matches final narration. They are phrase-timed from measured clips, not word aligned. The final cue ends at 564.885s.

## Scientific and source audit

At production completion, the locked completion manifest was compared with all 13 scientific input/output files: every SHA-256 matched. Its copy is `scientific-completion-manifest.json`; the production source hashes are `final-scientific-source-sha256.json`. These snapshots are preserved as historical evidence. The final documentation/layout fixes did not change any narrated mathematical claim.

The sharp inequality and real equality example are Lean checked with only propext, Classical.choice and Quot.sound. Trees, iteration, DP/SAT, caterpillar construction and h(3)=14 are not formalised. The 613-family executable replay is corroborating sampled evidence, not a proof by exhaustive enumeration. Written proof and accepted review establish the general claim. No research code was edited or rerun by this production continuation.

The exact h(3)=14 result, 23<=h(4)<=28, prior Snir-Yuster lower bound, bounded novelty, unresolved 23-leaf searches and real-variable-only optimality are retained accurately. Source, narration, witness data and every audio clip still match `render-input-sha256.json`.

Final `contact.png` selects 30 settled explanatory frames from the verified final movie, avoiding half-written equations in the automatic evenly spaced sheet. The automatic sheet is preserved as `qa/contact-automatic.png`; selected frame names are in `qa/contact-selection.json`. The final poster and selected contact sheet were visually inspected.

## Subsequent checker guard

After production, `verification/iterate_check.py` gained an explicit rejection of Python optimization mode, which would otherwise disable its substantive assertions. Root reproduced the defect and verified the guard, eight thresholds, two factor controls and 18 seeded families. The earlier 613-family run retains its original source hash. See `qa/checker-guard-provenance.json` and the collection's `docs/verification/checker-guards-20261026/` evidence. No manuscript, Lean source, narration, animation or media changed; no rerender was required.
