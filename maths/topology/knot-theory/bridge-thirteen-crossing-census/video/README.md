# Why these knots need four bridges

A narrated GCSE-level explanation of bridge number, meridian journeys, a concrete crossing relation for `13n_1005`, two-swap actions on eight dots, the seven-versus-six equality obstruction, and an exact four-seed colouring. The ending states the 25/27/268 accounting and unresolved broader priority. About nine minutes, Cedar synthetic narration, native 1080p30 H.264/AAC. The final measured runtime and verification limits are in `QA.md`; no listening review is claimed.

- Play `video.mp4`, with optional `subtitles.srt` or the local `preview.html` player.
- Edit `scenes.py` for animation. Edit `write_story.py` and run it to regenerate `storyboard.md` and `narration.json`.
- `audio/` holds the 34 measured clips, durations and generation-provenance manifest.
- `example.json` freezes the actual knot certificate, checked planar drawing, seed actions and colouring moves. Regenerate with `prepare_assets.py`, which reads the research package without modifying it.
- `sources.md` maps each claim to its evidence. `qa/` preserves checker logs, input hashes, frame samples, full decode and stream checks. `poster.png` and `contact.png` accompany the final media.

Rebuild using the existing environment, one render at a time:

```sh
V=${VIDEO_PYTHON:-python3}
T="$(git rev-parse --show-toplevel)/tools/video"
D="$(git rev-parse --show-toplevel)/maths/topology/knot-theory/bridge-thirteen-crossing-census/video"
nice -n 10 "$V" -B "$D/prepare_assets.py"
$V -B "$D/write_story.py"
$V "$T/make_audio.py" "$D"
nice -n 10 "$V" -B "$D/build.py" --quality h
nice -n 10 "$V" -B "$D/qa_media.py"
```

No new dependencies were installed. No research papers, checkers, shared runtime or other workers' folders were changed. Artifact production and internal QA do not replace the coordinator's separate research audit.
