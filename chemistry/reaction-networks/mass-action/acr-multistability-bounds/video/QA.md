# Final media QA

Final native Manim render: **9:44** (583.567 seconds), 1920x1080, 30fps, H.264 / AAC 48kHz. Native 1080p scene outputs were checked individually. This is not an enlarged preview.

- 37 Cedar clips. Maximum measured duration 18.600s; all are strictly under 25s. Source voice/model/text digests match final narration.
- Every narration clip appears exactly once in scene order, within measured scene boundaries. Full video and audio decode passed with zero error output.
- Final signal mean -26.6dB, peak -4.3dB. No digital clipping detected by peak measurement.
- Every source clip matches its expected final-media position. Minimum central-waveform correlation 0.966495; largest absolute offset 0.021375s. This checks correspondence, not pronunciation.
- 148 chronological nonoverlapping caption cues; concatenated words match narration exactly; at most 2 lines per cue. English captions are embedded as mov_text, with SRT and VTT supplied. Timing is proportional phrase timing inside measured clips, not forced word alignment.
- Historical scientific-input hashes are preserved. The sole approved change is the validated assertion-mode guard in `verification/independent_check.py`; `scientific-input-supplement.json` binds its current hash and root's positive/negative validation evidence. All other frozen input hashes match. Final render inputs and source/audio/media hashes are retained in JSON records.

## Visual inspection

Inspected final-media narration-beat and scene-boundary sheets, plus the full-resolution frames listed in `qa/visual-inspection.json`. Extraction alone was not counted as inspection. Findings:

- All 37 final beat images and all 16 scene-boundary images inspected. Early boundary samples intentionally capture the beginning of Write or FadeIn animations.
- Full-resolution network frames show separated arrowheads, rate labels and complex names after the spacing repair; both reactant and product molecule limits remain visible.
- The exact equilibria, restricted nullcline, dimension-two hypotheses, decoupled species construction and formal-proof scope remain legible. The representative sign case is labelled as only one case.
- No clipped text or unintended overlays observed in inspected final frames. Colour distinctions also have labels or numerical values.
- No listening or real-time playback performed.

Poster and selected contact sheet derive from these inspected settled frames. The automatic evenly spaced contact sheet is retained separately. Illustrations and simplified proof cases are identified in the storyboard and source ledger.

## Listening limitation

**No listening was performed.** No full real-time playback, subjective pronunciation check or audience comprehension test is claimed. Audio was checked by measured duration, manifest correspondence, complete decode, level measurement and waveform alignment. The local HTML preview offers captions and playback for a human listening pass.

## Records

`qa/ffprobe.json`, `qa/decode.log`, `qa/audio-levels.log`, `qa/clips.json`, `qa/timeline.json`, `qa/scenes.json`, `qa/subtitle-check.json`, `qa/audio-alignment.json`, `qa/scientific-input-check.json`, `qa/visual-inspection.json`, `qa/artifact-sha256.json`; stage logs are at the video root. Video production did not edit scientific inputs; validated checker changes by their owners are recorded separately.

Final delivery integrity and text audit: `qa/delivery-audit.json`; complete deliverable hashes: `delivery-sha256.json`.
