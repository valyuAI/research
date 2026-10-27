# Final media QA

Final native Manim render: **9:19** (559.167 seconds), 1920x1080, 30fps, H.264 / AAC 48kHz. Native 1080p scene outputs were checked individually. This is not an enlarged preview.

- 35 Cedar clips. Maximum measured duration 19.320s; all are strictly under 25s. Source voice/model/text digests match final narration.
- Every narration clip appears exactly once in scene order, within measured scene boundaries. Full video and audio decode passed with zero error output.
- Final signal mean -26.2dB, peak -5.3dB. No digital clipping detected by peak measurement.
- Every source clip matches its expected final-media position. Minimum central-waveform correlation 0.983259; largest absolute offset 0.021375s. This checks correspondence, not pronunciation.
- 141 chronological nonoverlapping caption cues; concatenated words match narration exactly; at most 2 lines per cue. English captions are embedded as mov_text, with SRT and VTT supplied. Timing is proportional phrase timing inside measured clips, not forced word alignment.
- All frozen scientific-input hashes remain unchanged. Final render inputs and source/audio/media hashes are retained in JSON records.

## Visual inspection

Inspected final-media narration-beat and scene-boundary sheets, plus the full-resolution frames listed in `qa/visual-inspection.json`. Extraction alone was not counted as inspection. Findings:

- Inspected all 35 final beat frames and all 14 scene-boundary frames. Early boundaries capture intentional drawing or fading animations.
- The exact23-move position and six-cell path are legible at full resolution. The counter changes from move number to path cells to Blue stones.
- Certified and search-only six-board path bounds remain visibly separated. The strict first-connection panel states only bounds8 through10.
- The 5-by-5 continued-play and first-connection values, stone budgets, prior work and absence of Lean remain legible. No clipping or unintended overlays observed in inspected settled frames.
- No listening or real-time playback performed.

Poster and selected contact sheet derive from these inspected settled frames. The automatic evenly spaced contact sheet is retained separately. Illustrations and simplified proof cases are identified in the storyboard and source ledger.

## Listening limitation

**No listening was performed.** No full real-time playback, subjective pronunciation check or audience comprehension test is claimed. Audio was checked by measured duration, manifest correspondence, complete decode, level measurement and waveform alignment. The local HTML preview offers captions and playback for a human listening pass.

## Records

`qa/ffprobe.json`, `qa/decode.log`, `qa/audio-levels.log`, `qa/clips.json`, `qa/timeline.json`, `qa/scenes.json`, `qa/subtitle-check.json`, `qa/audio-alignment.json`, `qa/scientific-input-check.json`, `qa/visual-inspection.json`, `qa/artifact-sha256.json`; stage logs are at the video root. Video production did not edit scientific inputs; validated checker changes by their owners are recorded separately.

Final delivery integrity and text audit: `qa/delivery-audit.json`; complete deliverable hashes: `delivery-sha256.json`.
