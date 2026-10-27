# Final production QA

Completed 2026-10-26. Final video: **526.900 seconds (8:46.90)**, **1920x1080**, **30 fps**, **H.264 / yuv420p**, **AAC at 48 kHz**. Every individual scene was rendered at 1080p30; no preview was upscaled. Final rendering and assembly took 263 seconds at nice 10. No new dependencies were installed.

## Scientific and illustration checks

- Read the complete final README, paper, brief, verification README, both checker implementations, final cell LOG handoff and final adversarial report. The final report's BKM overlap objection predates the completed A4/D4/H4 audit; the broader special-family priority limitation remains explicitly spoken.
- Replayed both complete standard-library checkers read-only, with logs saved here. All **27** certificates passed. Both cover the lower bound and four-seed upper bound. The first checks all 351 crossing relations, 243 colouring moves and image order 20,160; the independent matrix checker checks ranks two and seven and all colouring moves.
- Reconstructed the displayed `13n_1005` projection from the actual PD rotation system. Checked consistent counterclockwise order at all 13 crossings and absence of additional segment intersections. The displayed underpass gaps respect the saved crossing roles. This is a polygonal diagram, not a spatial four-bridge embedding.
- Checked the enlarged first crossing's exact labels: incoming `(01)(23)`, over `(01)(34)`, outgoing `(01)(24)`. The relabelling animation demonstrates the actual conjugation relation.
- The four displayed seed actions are taken directly from arcs 0, 3, 7, 4. The equality graph's component counts are 6, 5, 3, 1. Its seven distinct edges connect all eight dots, giving the displayed seven independent requirements.
- All nine colouring moves are derived from the certificate, including the known overarc, known underarc, newly reached arc and inherited seed colour. The local demonstration is actual crossing 3, with known underarc 3 and overarc 4 colouring new arc 2.
- The final scope is 24 double-transposition certificates plus `13n_4645` by a 3-cycle, giving 25 additions relative to the pinned 293-name list. There are 27 total certificates including two prior cable values, and 268 residual names including those two. No claim that all residual entries are unknown or that these are globally first discoveries.
- The height sketch is explicitly schematic. The colouring-to-bridge implication is credited as a published theorem. The video explains the lower-bound mechanism without pretending to animate a spatial four-bridge reconstruction, and does not equate crossing count with bridge count.
- Research input SHA-256 hashes remained unchanged from review through final rendering. See `qa/example-check.json` and `sources.md` for the evidence map and limitations.

## Media checks

- `qa/ffprobe.json` confirms native final stream specifications and duration.
- Full audio/video decode exits 0, with **15,807 frames** decoded; `qa/full-decode.log` is preserved.
- All 34 Cedar clips were individually measured with ffprobe. Total speech is **513.864 seconds**; longest clip is **20.016 seconds**, below the 25-second limit.
- Generation-manifest hashes match the current narration text, voice and instructions. Every clip appears exactly once, in script order, and fits within its final scene. The actual source, clip and media hashes are recorded in `qa/media-check.json`.
- Audio is non-silent: mean **-26.3 dBFS**, maximum **-4.7 dBFS**. These are signal checks.
- **No auditory listening or playback review was performed.** Pronunciation, pacing and exact generated spoken-word fidelity have not been independently checked by ear or transcription. Matching text/provenance hashes do not establish perceptual quality.
- Subtitles use measured clip starts. Within-clip caption subdivisions use proportional text length, not word-level alignment. Both SRT and browser VTT are supplied.

## Visual inspection and preserved failures

The first preview stopped at an unsupported Manim API call; the installed-version fix and original logs are preserved in `qa/preview-attempt1*`. The completed 480p15 preview was inspected through the full contact sheet and detailed Crossing, FixedValues, Connected, Colouring, Humps, Census and end-card frames. Equality connectors were shortened to avoid running through value glyphs before the final render.

Inspected all 30 final start/middle/end scene samples in `qa/boundary-contact.png`; individually viewed full-resolution opening, fixed-value scene, 27/25 accounting and ending. Also inspected full-resolution crossing, corrected equality links, actual seed network and fully coloured diagram. Extra samples extracted from the assembled final MP4 include its midpoint at **263.45s**, actual crossing at **162.979s**, connected seed graph at **287.016s** and the busiest coloured diagram at **405.983s**. Text and the synthetic-voice disclosure fit inside the frame. Early samples with incomplete paths are intentional drawing transitions.

Scene order: Humps; Loops; Permutations; Crossing; FixedValues; Connected; LowerBound; Colouring; Census; Ending. Exact scene and clip timings are in `qa/timeline.json`, and the systematic frame sample index is in `qa/frame-index.json`.

Confidence: high in technical media conformance and consistency with the checked finite certificates. Audio perceptual quality is unreviewed. Broader priority remains moderate/limited as explained in the research package, not resolved by this video QA. The coordinator's independent research audit and external peer review remain separate.
