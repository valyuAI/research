"""Freeze a finished delivery after manual inspection and objective QA."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
inputs = json.loads((ROOT/'research-input-sha256.json').read_text())
for name, digest in inputs.items():
  assert sha(ROOT.parent/name) == digest, f'Research input changed: {name}'
audio = json.loads((ROOT/'audio/durations.json').read_text())
alignment = json.loads((ROOT/'qa/audio-alignment.json').read_text())
browser = json.loads((ROOT/'qa/browser-playback.json').read_text())
assert len(alignment['clips']) == len(audio)
assert all(d < 25 for d in audio.values())
assert (ROOT/'qa/decode.log').read_text() == ''
assert 'Manual visual inspection' in (ROOT/'QA.md').read_text()
metadata = browser['metadata']
assert (metadata['width'], metadata['height']) == (1920, 1080)
assert 300 <= metadata['duration'] <= 600
delivery = {
  'video':'video.mp4', 'duration_seconds':metadata['duration'],
  'width':1920, 'height':1080, 'fps':30, 'video_codec':'H.264',
  'audio_codec':'AAC', 'voice':'cedar', 'clips':len(audio),
  'longest_clip_seconds':max(audio.values()),
  'smallest_waveform_correlation':min(x['correlation'] for x in alignment['clips']),
  'largest_alignment_offset_seconds':max(abs(x['lag_seconds']) for x in alignment['clips']),
  'research_inputs_reverified':len(inputs),
  'full_decode':'pass', 'clip_hashes_and_order':'pass',
  'browser_playback_and_captions':'pass',
  'manual_visual_inspection':'see QA.md',
  'listening_performed':False,
  'limitations':['Subjective pronunciation and listening comfort are not assessed.',
                 'Captions are phrase-timed using measured clips, not word-aligned.'],
}
(ROOT/'delivery.json').write_text(json.dumps(delivery, indent=2)+'\n')
files = [p for p in ROOT.rglob('*') if p.is_file()
  and not any(part in {'media','__pycache__'} for part in p.relative_to(ROOT).parts)
  and p.suffix != '.log'
  and p.name not in {'active-job.json','paused-pids.json','artifact-sha256.json'}]
hashes = {}
for i,p in enumerate(sorted(files), 1):
  hashes[str(p.relative_to(ROOT))] = sha(p)
  if i%50 == 0:
    print(f'Hashed {i}/{len(files)} delivery artifacts', flush=True)
(ROOT/'qa/artifact-sha256.json').write_text(json.dumps(hashes, indent=2)+'\n')
print(json.dumps(delivery, indent=2), flush=True)
print(f'Frozen {len(hashes)} artifact hashes.', flush=True)
