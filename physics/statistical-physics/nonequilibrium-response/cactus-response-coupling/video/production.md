# Cactus response: production and verification

The film starts from GCSE-level probability on a driven three-state ring: clockwise hopping rate 2, anticlockwise rate 1. It explains stationary time fractions, rooted trees and their weights, the classical tree theorem, a concrete 1% rate nudge, response blocks, and uniquely constructable families. Its proof outline builds the shared edge-token lottery, explicitly cancels w/(bc)=wa/(abc), glues rings into a cactus, then shows why an exact K4 certificate blocks this stronger method without refuting the response conjecture.

## Claims and limits

- Rates are conditional on occupying the hop's starting state. The example's stationary distribution is uniform even though it carries a circulating current.
- The 1% change illustrates a finite perturbation. The exact vector (-10/21,8/21,2/21) is the infinitesimal relative response per relative nudge; the simple unweighted average uses the uniform starting distribution.
- Root-0 tree weights are 4,2,1, with probabilities 4/7,2/7,1/7. There are 27 families, 18 bags of arrows and 11 uniquely constructable families. Independent lotteries choose a look-alike with probability 152/343.
- The seven cycle families each have exact probability 1/7. The 400,000-draw tally is an illustration, separate from the exact calculation. Shared positive multipliers on both directions of an edge give the same modified rates for all roots, which is the missing causal step repaired in this finalization.
- The K4 calculation is exact: 346 uniquely constructable families score 0,2 or 4, yet the prescribed root marginals give expectation -74467043099669441/1314877998480476367. This excludes a full tree-law coupling, not the weaker response conjecture.
- The minor extension applies to connected bidirected networks containing a K4 minor and asserts that some positive rates fail. It does not say every rate choice fails. The 150 searches finding no response violation are not a proof. The diamond's roughly 0.061 discrepancy is a sampled edge-token error, not an exact impossibility certificate for all couplings.
- The film shows simple bidirected graphs. Missing arcs, parallel arcs, compactness and graph-minor lifting are handled in the paper. The classical tree theorem and Gumbel-max identity are stated and demonstrated, not proved here.
- Correctness confidence is high after the recorded internal reviews; originality remains less certain. Search does not prove priority. No external peer review or proof-software formalization is claimed.

## Editable package

- [scenes.py](scenes.py): Manim animation source.
- [narration.json](narration.json): all 52 spoken clips; [audio/](audio/) retains their measured audio and cache manifest.
- [storyboard.md](storyboard.md): scene plan, prerequisites and comprehension audit.
- [sources.md](sources.md): evidence, citations and limitations by scene.
- [subtitles.srt](subtitles.srt), [poster.png](poster.png) and [contact.png](contact.png): captions and final render previews.
- [check_numbers.py](check_numbers.py) and [numbers.json](numbers.json): reproducible on-screen calculations and the scene data.
- [paper.tex](../paper.tex): full mathematical arguments.

## Rebuild locally

Run from the repository root, using the existing campaign environment and installed Manim 0.22.0, ffmpeg and TeX dependencies. Existing audio is retained unless its text or voice instructions change. Audio generation uses the existing private credentials; never place them in source or command arguments.

    VIDEO_DIR=physics/statistical-physics/nonequilibrium-response/cactus-response-coupling/video
    VIDEO_PY=${VIDEO_PYTHON:-python3}
    nice -n 10 "$VIDEO_PY" -u "$VIDEO_DIR/check_numbers.py"
    "$VIDEO_PY" tools/video/make_audio.py "$VIDEO_DIR" --dry-run
    "$VIDEO_PY" tools/video/make_audio.py "$VIDEO_DIR"
    nice -n 10 "$VIDEO_PY" -u "$VIDEO_DIR/audit_layout.py"
    nice -n 10 "$VIDEO_PY" -u "$VIDEO_DIR/render_final.py"
    nice -n 10 "$VIDEO_PY" -u "$VIDEO_DIR/inspect_final.py"

Render sequentially with other campaign videos. The wrapper calls the established tools/video/render.py at quality h and explicitly 30 fps, emitting UTC heartbeats. It writes video-1080p-candidate.mp4, leaving the delivered video.mp4 intact until review. Inspect the new contact sheet, extracted frames and validation report before replacing the delivery file.

## Preservation

The incoming 480p preview and original editable files remain in ignored audit/intake/. Superseded audio remains in audio/.stale/. The final narration reuses 41 original clips; 11 clips were changed or added. Primary-source extracts stay in ignored audit/private-cache/. The final paper, prior reviews and shared toolkit were not edited. No publication was performed.

## Runtime and chapters

Native 1920 × 1080 at 30 fps, H.264/AAC stereo, 10:41.300. There are 52 narration clips across 15 scenes. The end card discloses the synthetic voice.

| Start | Scene |
|---|---|
| 00:00 | Hook |
| 00:36 | Hopping |
| 01:19 | Trees |
| 01:56 | TreeTheorem |
| 02:29 | Knob |
| 03:14 | Families |
| 04:04 | Conjecture |
| 04:51 | Reframe |
| 05:24 | Staircase |
| 06:00 | Tokens |
| 07:03 | WhyUC |
| 07:53 | Cactus |
| 08:20 | K4 |
| 09:28 | Status |
| 09:59 | Ending |

## Validation

The actual encoded output passed ffprobe: native 1920 × 1080, 30 fps, H.264 video and non-empty AAC stereo narration. All 52 clip hashes match the current script, measured durations match, every clip appears once, and no speech overlaps or is truncated at a scene boundary. The numerical checker passed, including the seven exact 1/7 cycle-family probabilities and the exact negative K4 expectation.

Inspected the contact sheet and eleven individual start/middle/end and dense proof frames. Two labels crossed the convex-hull boundary; those were repaired in Families and that scene alone was re-rendered before rejoining all fifteen scenes. The final contact sheet, corrected hull, cancellation, K4 certificate and start/middle/end were inspected again. Unchanged scene renders and all audio were reused for this repair. This is sampled visual inspection, not a review of every frame.

Receipts: [validation.json](audit/validation.json), [ffprobe.json](audit/ffprobe.json), [scene-index.json](audit/scene-index.json), [render log](audit/render-1080p.log), [repair log](audit/repair-families-render.log), [number checks](audit/numbers-validation.log), [inspected frames](audit/frames/). No listening review or audience test was performed. Stream and timing checks do not establish pronunciation quality.

Full video and audio decoding also passed with ffmpeg -xerror -err_detect explode; [decode receipt](audit/decode-validation.json) and [streaming decode log](audit/decode-validation.log) are retained. Caption text was checked against every narration clip. The checked candidate was promoted to video.mp4 only after confirming that the preserved 480p intake copy matched the previous delivery. SHA-256 and actual final-file ffprobe checks confirm the delivery is the reviewed encode.
