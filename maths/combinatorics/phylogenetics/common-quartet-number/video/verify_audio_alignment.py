"""Compare rendered speech waveforms with each source clip; this is not listening."""
import json
from pathlib import Path
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parent
RATE = 8000


def pcm(path):
  data = subprocess.check_output([
    'ffmpeg', '-nostdin', '-v', 'error', '-i', str(path), '-vn',
    '-ac', '1', '-ar', str(RATE), '-f', 'f32le', 'pipe:1',
  ])
  return np.frombuffer(data, dtype='<f4').astype(np.float64)


movie = pcm(ROOT / 'video.mp4')
timeline = json.loads((ROOT / 'qa/timeline.json').read_text())
records = []
for i, clip in enumerate(timeline, 1):
  source = pcm(ROOT / 'audio' / f'{clip["id"]}.mp3')
  # Use a central six-second speech interval, leaving room for encoding delay.
  length = min(6 * RATE, len(source) // 2)
  begin = (len(source) - length) // 2
  reference = source[begin:begin + length]
  reference = reference - reference.mean()
  expected = round(clip['start'] * RATE) + begin
  radius = round(.4 * RATE)
  lower = max(0, expected - radius)
  search = movie[lower:expected + radius + length]
  size = 1 << (len(search) + length - 2).bit_length()
  convolution = np.fft.irfft(
    np.fft.rfft(search, size) * np.fft.rfft(reference[::-1], size), size,
  )[length - 1:len(search)]
  sums = np.concatenate(([0.], np.cumsum(search)))
  squares = np.concatenate(([0.], np.cumsum(search * search)))
  energy = squares[length:] - squares[:-length]
  energy -= (sums[length:] - sums[:-length]) ** 2 / length
  correlations = convolution / np.sqrt(np.maximum(energy, 1e-30) * np.dot(reference, reference))
  peak = int(np.argmax(correlations))
  correlation = float(correlations[peak])
  offset = (lower + peak - expected) / RATE
  records.append({'id': clip['id'], 'correlation': correlation, 'offset_seconds': offset})
  print(f'{i}/{len(timeline)} {clip["id"]}: correlation {correlation:.6f}, offset {offset:+.4f}s', flush=True)
  assert correlation > .95, records[-1]
  assert abs(offset) < .3, records[-1]

(ROOT / 'qa/audio-alignment.json').write_text(json.dumps({
  'method': 'Central waveform correlation after mono 8kHz decoding; encoding delay allowed. Not listening.',
  'minimum_correlation': min(r['correlation'] for r in records),
  'maximum_absolute_offset_seconds': max(abs(r['offset_seconds']) for r in records),
  'clips': records,
}, indent=2) + '\n')
print('PASS: each source narration clip is present at its scheduled final-media position.', flush=True)
