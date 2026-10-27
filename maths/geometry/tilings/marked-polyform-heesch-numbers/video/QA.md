# Final media QA

Final native Manim render: **9:32** (572.433 seconds), 1920x1080, 30fps, H.264 / AAC 48kHz. Native 1080p scene outputs were checked individually. This is not an enlarged preview.

- 34 Cedar clips. Maximum measured duration 19.920s; all are strictly under 25s. Source voice/model/text digests match final narration.
- Every narration clip appears exactly once in scene order, within measured scene boundaries. Full video and audio decode passed with zero error output.
- Final signal mean -26.4dB, peak -5.6dB. No digital clipping detected by peak measurement.
- Every source clip matches its expected final-media position. Minimum central-waveform correlation 0.976592; largest absolute offset 0.021375s. This checks correspondence, not pronunciation.
- 146 chronological nonoverlapping caption cues; concatenated words match narration exactly; at most 2 lines per cue. English captions are embedded as mov_text, with SRT and VTT supplied. Timing is proportional phrase timing inside measured clips, not forced word alignment.
- Scientific inputs match the preserved original snapshot plus any explicitly validated checker updates in `scientific-input-supplement.json`. Historical hashes remain intact. Final render inputs and source/audio/media hashes are retained in JSON records.

## Visual inspection

Inspected final-media narration-beat and scene-boundary sheets, plus the full-resolution frames listed in `qa/visual-inspection.json`. Extraction alone was not counted as inspection. Findings:

- Inspected all34 final beat frames and all16 scene-boundary frames. Initial boundary samples show intentional FadeIn/Write starts.
- Full-resolution retained bump-nick pair has the intended curved shared seam. Base thumbnail layouts and maximum labels are separated.
- The actual131-piece five-ring row witness and169-piece published six-ring patch are fully visible with legible counts. Their outlines and placements come from the retained exact geometry.
- The hypothetical unmarked fourth-ring diagram is labelled impossible; schematic growth and window illustrations are labelled. No decorative patch is substituted for a witness.
- Prior Mann/Atlas results, possible Mann-Thomas overlap, strict lattice scope, no off-grid upper bound and retained-proof limitations remain explicit. No clipping observed in inspected settled frames.
- Checker/control provenance updates are validated and do not alter the inspected media. No fresh DRAT replay or new170-mutation audit claimed.
- No listening or real-time playback performed.

Poster and selected contact sheet derive from these inspected settled frames. The automatic evenly spaced contact sheet is retained separately. Illustrations and simplified proof cases are identified in the storyboard and source ledger.

## Listening limitation

**No listening was performed.** No full real-time playback, subjective pronunciation check or audience comprehension test is claimed. Audio was checked by measured duration, manifest correspondence, complete decode, level measurement and waveform alignment. The local HTML preview offers captions and playback for a human listening pass.

## Records

`qa/ffprobe.json`, `qa/decode.log`, `qa/audio-levels.log`, `qa/clips.json`, `qa/timeline.json`, `qa/scenes.json`, `qa/subtitle-check.json`, `qa/audio-alignment.json`, `qa/scientific-input-check.json`, `qa/visual-inspection.json`, `qa/artifact-sha256.json`; stage logs are at the video root. Video production did not edit scientific inputs; validated checker changes by their owners are recorded separately.

Final delivery integrity and text audit: `qa/delivery-audit.json`; complete deliverable hashes: `delivery-sha256.json`.
