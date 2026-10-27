# Final production QA

Completed 2026-10-26. Final video: **548.566667 seconds (9:08.57)**, **1920x1080**, **30 fps**, **H.264 / yuv420p**, **AAC at 48 kHz**. Every individual scene was rendered at 1080p30; the preview was not upscaled. The full render took 384 seconds at nice 10. No additional dependencies were installed.

## Scientific and display checks

- Read the final paper, README, readiness, video brief, runtime and relevant certificate/checker code. The recorded 17-stage research replay passed; this worker did not rerun all 17 stages or perform the coordinator's separate final audit.
- Replayed the exact J3 edge-partition, admissible-axis and nontriviality certificate. The rendered motion is the accepted formula `s1 + R(t)s2`, with frozen coordinates in `geometry.json`.
- Checked 161 display angles from -8 to +8 degrees: maximum edge and face-plane error `3.33e-16`, minimum convex margin `0.64549`. At five degrees, the six hexagon angles alternate 115 and 125 degrees. These floating checks validate the illustration; the exact certificate supplies the mathematical justification.
- The classification grid is generated from the accepted classification file: 41 first-order rigid, 45 flexible, 6 first-order flexible but second-order rigid. The video explicitly distinguishes local from global rigidity and tangent directions from actual motion families.
- The pyramid argument is prior known work. The two-bar example is explicitly a teaching example with a rejected, length-changing attempt. It is not passed off as a literal certificate for a Johnson solid. J60/J82 are the two prestress-stable exceptions; the other four are correctly distinguished.
- Novelty is restricted to the full table and certificates, with the recorded search and general-criterion limits spoken in the ending. The antiprism theorem and large algebraic eliminations were omitted for pacing.

## Media checks

- `qa/ffprobe.json`: native final streams and measured duration.
- `qa/full-decode.log`: complete audio/video decode exits 0; 16,457 video frames decoded.
- All 36 narration clips were measured independently with ffprobe; longest **19.752 seconds**, all below the 25-second limit. Total speech 531.72 seconds.
- Manifest hashes match the exact current text, Cedar voice and generation instructions. Every script clip appears exactly once, in order, in the final scene timeline and fits its scene. Final source, audio and media SHA-256 records are in `qa/media-check.json`.
- Audio is non-silent: mean level -26.1 dBFS, peak -5.7 dBFS. This is a signal-level test, not a listening test.
- **No auditory listening or playback review was performed.** Pronunciation, pacing and complete spoken-word fidelity have not been independently assessed by ear or transcription. Script provenance is checked, not a claim that a listener verified each generated word.
- Subtitles use exact clip start times; subdivisions within clips are proportional to caption text length rather than word-level alignment. SRT and browser VTT are provided.

## Visual inspection

Inspected the preview contact sheet and retained samples; corrected two text overlaps before the full render. Inspected the final 30-frame contact sheet, the 30 start/middle/end frames covering all ten scenes via `qa/boundary-contact.png`, plus full-resolution Pyramid, Census and final-card stills. Individually checked the corrected velocity caption and zero-direction label at 1080p. The busiest census grid is legible and within the frame. The final end card, path and synthetic-voice disclosure are visible. Transition samples showing partially drawn objects are expected animation states.

Scene order: Rules; Cupola; Addition; Flatness; Pyramid; FirstOrder; SecondOrder; Census; Evidence; Ending. The retained `qa/frame-index.json` gives exact sample times. Preview evidence, final logs and sources remain available for coordinator review.

Confidence: high in technical media conformance and consistency with the read research package; audio perceptual quality remains unreviewed. This QA is not external peer review, a new full theorem audit, or proof of priority.
