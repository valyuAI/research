"""Write measured rebuild docs and a local player after successful technical QA."""
import ast
import hashlib
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO=next(p for p in ROOT.parents if (p / 'tools/video/render.py').exists())
names={
  'mu-q-2-2':('Nine multiplications, and not one fewer','Karatsuba, binary polynomial arithmetic, rank-one grids, exhaustive lower bounds, the finite-field table and binary length-six convolution. The prior symmetric binary result and prior search methods are credited; novelty remains bounded. No Lean formalization is claimed.'),
  'latin-tableaux-staircase-count':('Four new ways, every time','Latin squares and staircase tableaux, one exact six-to-seven-column extension, forced entries, two independent swaps, invariant preservation and induction. This is an independent verification note; the earlier 22 October 2026 proof has priority.'),
  'cubic-tic-tac-toe-surplus':('Spare cells beat unknown moves','A concrete pairing defence, cube lines, Hall matching, surplus and deletion robustness, central and noncentral openings, the opposite-octant correction, and the six-cube obstruction. This is a new short proof of the known seven-cube theorem. Six-cube and five-cube remain open; Lean covers the abstract lemmas, not the actual board enumeration or whole game.'),
}
name,scope=names[ROOT.parent.name]
probe=json.loads((ROOT/'qa/ffprobe.json').read_text())
duration=float(probe['format']['duration'])
minutes=int(duration//60);seconds=duration-minutes*60
runtime=f'{minutes}:{seconds:06.3f}'
durations=json.loads((ROOT/'audio/durations.json').read_text())
alignment=json.loads((ROOT/'qa/audio-alignment.json').read_text())
assert 300<=duration<=600 and max(durations.values())<=25
snapshot=json.loads((ROOT/'source-snapshot.json').read_text())
for path,digest in snapshot['sources'].items():
  assert hashlib.sha256((REPO/path).read_bytes()).hexdigest()==digest, ('Scientific input changed',path)
tree=ast.parse((ROOT/'scenes.py').read_text())
scenes=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='SCENES' for t in n.targets))
srt=(ROOT/'subtitles.srt').read_text()
vtt='WEBVTT\n\n'+'\n'.join(line.replace(',','.') if '-->' in line else line for line in srt.splitlines())+'\n'
(ROOT/'subtitles.vtt').write_text(vtt)
readme=f'''# {name}

Completed local narrated video: **{runtime}** ({duration:.3f} seconds), native **1920x1080 at 30 fps**, H.264 video and AAC audio. {scope}

The editable package has {len(scenes)} Manim scenes and {len(durations)} Cedar clips. Every narration clip is measured below 25 seconds; the longest is {max(durations.values()):.3f} seconds. `QA.md` records full decode, frame inspection and timing evidence. Waveform matching finds every source clip at its scheduled position (minimum correlation {alignment['minimum_correlation']:.6f}, largest absolute offset {alignment['maximum_absolute_offset_seconds']:.4f} seconds). This verifies audio correspondence, not pronunciation. **No listening review or full real-time playback is claimed.**

- Play `video.mp4`, or open `preview.html` for a local player. External subtitles are `subtitles.srt` and `subtitles.vtt`.
- Edit `write_story.py` for the spoken script and storyboard, then regenerate `narration.json` and `storyboard.md`.
- Edit `scenes.py` for animation. Scene order: {', '.join(scenes)}.
- `audio/` contains source clips, measured durations and narration digests. `sources.md` and `source-snapshot.json` record scientific provenance and scope.
- `poster.png`, `contact.png`, `qa/beats.png` and `qa/boundaries.png` support visual review. `preview.mp4` is the development preview, not the final.
- `check_examples.py` independently verifies displayed examples and writes only `example-checks.json`. It does not repeat the expensive research enumerations.

Rebuild from this folder using the existing environment, one heavy stage at a time:

```sh
V=${VIDEO_PYTHON:-python3}
"$V" -B write_story.py
"$V" -B check_examples.py
"$V" -B run_stage.py preview
# Inspect the preview before proceeding.
"$V" -B run_stage.py dry-audio
"$V" -B run_stage.py audio
"$V" -B run_stage.py final
"$V" -B run_stage.py qa
"$V" -B run_stage.py alignment
"$V" -B finish_package.py
```

`run_stage.py` uses nice10, single-thread BLAS settings, 15-second progress and local stage logs. Final renders acquire the campaign advisory `final-render.lock` for their full subprocess lifetime, with 15-second wait heartbeats and a legacy PID96759 check. The lock is never unlinked. The shared `tools/video/` runtime remains read-only. Audio generation uses the existing private environment credential and regenerates only changed clips. A clean rebuild's first preview is silent and uses estimated timings; after audio exists, preview timings follow measured clips. Reinspect frames after edits; automated QA does not perform visual or listening review. No new dependencies, commit, push, upload or external contact were made.

Narration uses a synthetic voice. This artifact is local and private.
'''
(ROOT/'README.md').write_text(readme)
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(name)}</title><style>body{{margin:40px auto;padding:0 20px;max-width:1080px;background:#0d0f12;color:#eee;font:17px/1.6 system-ui}}h1{{font-size:28px;font-weight:600}}video{{width:100%;height:auto}}a{{color:#64c3ba}}p{{max-width:80ch}}small{{color:#bbb}}</style><h1>{html.escape(name)}</h1><video controls preload="metadata" poster="poster.png"><source src="video.mp4" type="video/mp4"><track kind="subtitles" src="subtitles.vtt" srclang="en" label="English"></video><p>{html.escape(scope)}</p><p>{runtime} · 1080p30 · <a href="README.md">Rebuild</a> · <a href="storyboard.md">Storyboard</a> · <a href="sources.md">Sources</a> · <a href="QA.md">QA</a></p><small>Narration uses a synthetic voice. No listening review is claimed.</small></html>'''
(ROOT/'preview.html').write_text(page)
summary={'title':name,'duration_seconds':duration,'native_resolution':[1920,1080],'fps':30,'video_codec':'h264','audio_codec':'aac','clips':len(durations),'max_clip_seconds':max(durations.values()),'scenes':scenes,'source_hashes_unchanged':True,'audio_alignment':{k:v for k,v in alignment.items() if k!='clips'},'listening_review':False,'scope':scope}
(ROOT/'delivery.json').write_text(json.dumps(summary,indent=2)+'\n')
hash_path=ROOT/'qa/artifact-sha256.json'
hashes=json.loads(hash_path.read_text())
for p in [*ROOT.glob('*.py'),*ROOT.glob('*.md'),*ROOT.glob('*.json'),ROOT/'subtitles.vtt',ROOT/'preview.html']:
  hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
hash_path.write_text(json.dumps(hashes,indent=2)+'\n')
print(f'Package complete: {name}, {runtime}, {len(durations)} clips.',flush=True)
