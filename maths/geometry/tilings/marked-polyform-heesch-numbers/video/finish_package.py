"""Close the package only after machine QA and explicit image inspection records."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil

from PIL import Image, ImageDraw

from run_stage import update_status

ROOT=Path(__file__).resolve().parent
QA=ROOT/'qa'
SUMMARY=json.loads((QA/'summary.json').read_text())
ALIGN=json.loads((QA/'audio-alignment.json').read_text())
VISUAL=json.loads((QA/'visual-inspection.json').read_text())
assert VISUAL['passed'] and VISUAL['inspected_files']
assert ALIGN['minimum_correlation']>.95 and ALIGN['maximum_absolute_offset_seconds']<.3
INPUTS=json.loads((ROOT/'render-input-sha256.json').read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest for p,digest in INPUTS.items())

name=ROOT.parent.name
POSTERS={'acr-multistability-bounds':'a13','hex-short-wins':'h11','min-modulus-six-odd-part-45':'c24','marked-polyform-heesch-numbers':'t14'}
shutil.copy2(QA/f'{POSTERS[name]}.png',ROOT/'poster.png')
if (ROOT/'contact.png').exists() and not (QA/'contact-automatic.png').exists():
  shutil.copy2(ROOT/'contact.png',QA/'contact-automatic.png')
frames=[f for f in json.loads((QA/'frames.json').read_text()) if f['kind']=='beat']
chosen=[frames[round(i*(len(frames)-1)/29)] for i in range(30)]
# Keep the mating seam and the complete published patch in the delivery sheet.
replacements={'t07':'t05','t29':'t30'}
chosen=[next(f for f in frames if f['label']==replacements[c['label']]) if c['label'] in replacements else c for c in chosen]
chosen.sort(key=lambda f:f['time'])
canvas=Image.new('RGB',(2400,6*294),'#20242a');draw=ImageDraw.Draw(canvas)
for i,frame in enumerate(chosen):
  x=(i%5)*480;y=(i//5)*294
  canvas.paste(Image.open(QA/frame['file']).convert('RGB').resize((480,270)),(x,y))
  draw.text((x+8,y+275),f'{frame["label"]} | {frame["time"]:.2f}s',fill='white')
canvas.save(ROOT/'contact.png')
(QA/'contact-selection.json').write_text(json.dumps(chosen,indent=2)+'\n')
duration=SUMMARY['duration'];runtime=f'{int(duration//60)}:{round(duration%60):02d}'
scenes=json.loads((QA/'scenes.json').read_text())
subtitles=json.loads((QA/'subtitle-check.json').read_text())
notes='\n'.join(f'- {note}' for note in VISUAL['notes'])
qa=f'''# Final media QA

Final native Manim render: **{runtime}** ({duration:.3f} seconds), 1920x1080, 30fps, H.264 / AAC 48kHz. Native 1080p scene outputs were checked individually. This is not an enlarged preview.

- {SUMMARY['clip_count']} Cedar clips. Maximum measured duration {SUMMARY['max_clip_seconds']:.3f}s; all are strictly under 25s. Source voice/model/text digests match final narration.
- Every narration clip appears exactly once in scene order, within measured scene boundaries. Full video and audio decode passed with zero error output.
- Final signal mean {SUMMARY['mean_db']}dB, peak {SUMMARY['peak_db']}dB. No digital clipping detected by peak measurement.
- Every source clip matches its expected final-media position. Minimum central-waveform correlation {ALIGN['minimum_correlation']:.6f}; largest absolute offset {ALIGN['maximum_absolute_offset_seconds']:.6f}s. This checks correspondence, not pronunciation.
- {subtitles['cues']} chronological nonoverlapping caption cues; concatenated words match narration exactly; at most 2 lines per cue. English captions are embedded as mov_text, with SRT and VTT supplied. Timing is proportional phrase timing inside measured clips, not forced word alignment.
- Scientific inputs match the preserved original snapshot plus any explicitly validated checker updates in `scientific-input-supplement.json`. Historical hashes remain intact. Final render inputs and source/audio/media hashes are retained in JSON records.

## Visual inspection

Inspected final-media narration-beat and scene-boundary sheets, plus the full-resolution frames listed in `qa/visual-inspection.json`. Extraction alone was not counted as inspection. Findings:

{notes}

Poster and selected contact sheet derive from these inspected settled frames. The automatic evenly spaced contact sheet is retained separately. Illustrations and simplified proof cases are identified in the storyboard and source ledger.

## Listening limitation

**No listening was performed.** No full real-time playback, subjective pronunciation check or audience comprehension test is claimed. Audio was checked by measured duration, manifest correspondence, complete decode, level measurement and waveform alignment. The local HTML preview offers captions and playback for a human listening pass.

## Records

`qa/ffprobe.json`, `qa/decode.log`, `qa/audio-levels.log`, `qa/clips.json`, `qa/timeline.json`, `qa/scenes.json`, `qa/subtitle-check.json`, `qa/audio-alignment.json`, `qa/scientific-input-check.json`, `qa/visual-inspection.json`, `qa/artifact-sha256.json`; stage logs are at the video root. Scientific inputs were read-only throughout.
'''
(ROOT/'QA.md').write_text(qa)
readme=f'''# {name.replace('-',' ').capitalize()}

Accessible narrated mathematical explainer, **{runtime}**, built from GCSE foundations with concrete examples and animated proof mechanics. Native 1920x1080 at 30fps, H.264/AAC, {SUMMARY['clip_count']} built-in Cedar clips, all under 25s. See [video](video.mp4), [captioned local player](preview.html), [storyboard](storyboard.md), [sources](sources.md) and [QA](QA.md). No listening was performed; machine audio validation and explicit visual inspection are documented.

## Editable files

`scenes.py` defines {len(scenes)} ordered Manim scenes: {', '.join(s['scene'] for s in scenes)}. `narration.json` is the exact speech script. `audio/` contains the final MP3 clips, measured durations and model/voice/text digests. `subtitles.srt` and `subtitles.vtt` supply English captions. `poster.png` and `contact.png` use inspected settled frames. Scientific-input hashes are frozen before production.

## Rebuild

Use the existing environment and toolkit; do not migrate the project or edit scientific inputs:

```sh
V=${VIDEO_PYTHON:-python3}
"$V" -B run_stage.py preview
"$V" -B run_stage.py dry-audio
"$V" -B run_stage.py audio
"$V" -B run_stage.py final
"$V" -B run_stage.py qa
"$V" -B run_stage.py alignment
```

Run from this video folder. The wrapper applies nice 10, single-thread BLAS variables and flushed 15-second heartbeats. Every final render holds the shared advisory flock at `$VIDEO_RENDER_LOCK` (default `/tmp/valyu-research-final-render.lock`), acquired nonblocking with wait heartbeats; the lock file is never removed or replaced. It also checks the legacy un-locked process PID 96759. The lock spans the entire final-render subprocess, including concatenation.

The audio stage calls the existing secure `tools/video/make_audio.py` wrapper, reading credentials only through the process environment or private env file. No credential belongs in this folder. It regenerates only changed clips. Measure them before final rendering; `verify_media.py` rejects any clip >=25s.

If this folder has `prepare_witness.py` or `prepare_geometry.py`, run it with the same interpreter to regenerate exact visual input data from the locked local witnesses. ACR's `trajectory-data.json` contains labelled illustrative numerical paths, not a stability proof. Re-rendering requires a fresh visual inspection record before running `finish_package.py`. The existing `qa/visual-inspection.json` applies only to the shipped final artifact hashes. After a rebuild, inspect the final beat and boundary sheets plus full-resolution critical frames, replace that inspection record, then run `"$V" -B finish_package.py` to refresh the poster, contact sheet, QA document and completion record. If you edited scenes, narration or visual input data, refresh `render-input-sha256.json` before rendering.

No publication, contact, commit or push is part of this rebuild procedure.
'''
(ROOT/'README.md').write_text(readme)
SUMMARY['visual_inspection']='passed; see visual-inspection.json'
SUMMARY['completedUtc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(ROOT/'completion.json').write_text(json.dumps(SUMMARY,indent=2)+'\n')
update_status({'stage':'complete','status':'complete','activePids':[],'updatedUtc':SUMMARY['completedUtc'],
               'log':str(ROOT/'alignment.log'),'note':f'{runtime}, native 1080p30 H.264/AAC; {SUMMARY["clip_count"]} Cedar clips all under 25s. Full decode, timing, caption and waveform checks pass; representative/boundary frames inspected. No listening performed. Final: {ROOT / "video.mp4"}'})
print(f'COMPLETE {ROOT / "video.mp4"}: {runtime}',flush=True)
