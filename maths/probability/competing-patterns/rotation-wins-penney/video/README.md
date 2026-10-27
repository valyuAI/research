# The reply that wins by moving one number

A narrated GCSE-level explanation of relative-order races, the 2341-to-1234 right rotation, the two-versus-one overlap count, inclusion-exclusion cancellation, interleavings and the clump-tail bound. The eight scenes are RankAndRace, LocalOverlap, CancelMarks, Interleavings, Tail, UniformRange, Certificates and Conclusion. The final film uses Cedar synthetic narration; exact runtime and verification results are recorded in QA.md.

`video.mp4` is the native 1080p30 H.264/AAC final film; `subtitles.srt` is its sidecar. Edit `scenes.py` and `narration.json`; the storyboard and evidence ledger are in `storyboard.md` and `sources.md`. Generated clips, measured durations and text digests are in `audio/`. The silent preview and preview-evidence are retained for comparison, not substituted for final media.

Rebuild from this directory with the existing environment:

```sh
V=${VIDEO_PYTHON:-python3}
"$V" mechanism_check.py
"$V" run_stage.py audio
"$V" run_stage.py final
nice -n 10 "$V" verify_media.py
```

The local runner uses the existing shared Manim pipeline, nice 10 and a 15-second heartbeat. Run only one render at a time. No new dependencies were installed. Changes to source or narration require a fresh final render and QA. Final source, audio and media hashes are recorded under `qa/`.

Simplifications: the complete cluster generating-function proof and tail derivation remain in the paper. On screen, a positive factor K abbreviates the exact conversion from signed comparison D to winning probability. Neither 1/120 nor the approximately .095 scaled margin is called the final winning advantage. Length three and the cluster method are credited to prior work. The finite checks cover all 2,952 representatives at lengths four through seven; the infinite range is a written proof, not finite exhaustion. Novelty remains bounded and moderate. Subjective listening is not claimed.
