#!/usr/bin/env python3
"""Render every scene of one video, join them, and write subtitles and a poster.

  python render.py <video-dir> [--quality l|m|h|k] [--fps 30] [--scenes A B ...] [--contact]

<video-dir>/scenes.py must define SCENES = ['SceneOne', 'SceneTwo', ...] in playing order.
Outputs: <video-dir>/video.mp4 (H.264 + AAC), subtitles.srt, poster.png, and with
--contact a contact sheet of frames every few seconds (contact.png) for visual review.
"""

import argparse
import ast
import json
import os
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
RES = {'l': '480p15', 'm': '720p30', 'h': '1080p30', 'k': '2160p30'}


def scene_list(root):
  tree = ast.parse((root / 'scenes.py').read_text())
  for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == 'SCENES' for t in node.targets):
      return [ast.literal_eval(e) for e in node.value.elts]
  sys.exit('scenes.py must define SCENES = [...]')


def probe(path):
  out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type:format=duration', '-of', 'json',
                        str(path)], capture_output=True, text=True, check=True).stdout
  d = json.loads(out)
  return float(d['format']['duration']), any(s['codec_type'] == 'audio' for s in d['streams'])


def srt_time(t):
  ms = int(round(t * 1000))
  h, ms = divmod(ms, 3600000)
  m, ms = divmod(ms, 60000)
  s, ms = divmod(ms, 1000)
  return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def split_caption(text, limit=84):
  """Break narration into subtitle-sized chunks at sentence or clause boundaries."""
  words, chunks, cur = text.split(), [], []
  for w in words:
    cur.append(w)
    if len(' '.join(cur)) >= limit or (w.endswith(('.', '?', '!')) and len(' '.join(cur)) > limit * 0.45):
      chunks.append(' '.join(cur))
      cur = []
  if cur:
    chunks.append(' '.join(cur))
  return chunks


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument('video_dir')
  ap.add_argument('--quality', default='h', choices=RES)
  ap.add_argument('--fps', type=int, default=None)
  ap.add_argument('--scenes', nargs='*')
  ap.add_argument('--contact', action='store_true', help='also write contact.png (30 frames spanning the video)')
  ap.add_argument('--output', default='video.mp4')
  ns = ap.parse_args()

  root = Path(ns.video_dir).resolve()
  scenes = ns.scenes or scene_list(root)
  fps = ns.fps or int(RES[ns.quality].split('p')[1])
  res_dir = RES[ns.quality].split('p')[0] + f'p{fps}'
  env = dict(os.environ, VR_VIDEO_DIR=str(root), PYTHONPATH=f'{TOOLS}{os.pathsep}' + os.environ.get('PYTHONPATH', ''))

  parts = []
  t0 = time.time()
  for i, name in enumerate(scenes, 1):
    print(f'[{i}/{len(scenes)}] rendering {name} ({res_dir}), elapsed {int(time.time() - t0)}s', flush=True)
    cmd = [sys.executable, '-m', 'manim', 'render', f'-q{ns.quality}', '--fps', str(fps), '--disable_caching',
           'scenes.py', name]
    log = root / 'media' / 'logs'
    log.mkdir(parents=True, exist_ok=True)
    with open(log / f'{name}.log', 'w') as fh:
      rc = subprocess.run(cmd, cwd=root, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
    if rc != 0:
      sys.exit(f'{name} failed; see {log / (name + ".log")}')
    mp4 = root / 'media' / 'videos' / 'scenes' / res_dir / f'{name}.mp4'
    if not mp4.exists():
      sys.exit(f'expected output {mp4} not found')
    parts.append(mp4)

  # Give every part an audio track so the concat filter has matching streams.
  fixed = []
  for mp4 in parts:
    dur, has_audio = probe(mp4)
    if has_audio:
      fixed.append(mp4)
      continue
    silent = mp4.with_name(mp4.stem + '.silent.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(mp4), '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-shortest', '-c:v', 'copy', '-c:a', 'aac', str(silent)], check=True)
    fixed.append(silent)

  out = root / ns.output
  inputs = sum((['-i', str(p)] for p in fixed), [])
  streams = ''.join(f'[{i}:v:0][{i}:a:0]' for i in range(len(fixed)))
  filt = f'{streams}concat=n={len(fixed)}:v=1:a=1[v][a]'
  print(f'joining {len(fixed)} part(s) -> {out}', flush=True)
  subprocess.run(['ffmpeg', '-y', '-v', 'error', '-stats', *inputs, '-filter_complex', filt, '-map', '[v]', '-map', '[a]',
                  '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                  '-b:a', '160k', '-ar', '48000', '-movflags', '+faststart', str(out)], check=True)

  # Subtitles from the per-scene clip timings.
  texts = {c['id']: c['text'] for c in json.loads((root / 'narration.json').read_text())['clips']}
  offset, n, lines = 0.0, 1, []
  for name, mp4 in zip(scenes, fixed):
    dur, _ = probe(mp4)
    tpath = root / 'media' / 'timings' / f'{name}.json'
    if tpath.exists():
      for clip in json.loads(tpath.read_text())['clips']:
        chunks = split_caption(texts[clip['id']])
        total_chars = sum(len(c) for c in chunks) or 1
        t = offset + clip['start']
        for chunk in chunks:
          span = clip['duration'] * len(chunk) / total_chars
          lines.append(f'{n}\n{srt_time(t)} --> {srt_time(t + span)}\n{chunk}\n')
          n += 1
          t += span
    offset += dur
  (root / 'subtitles.srt').write_text('\n'.join(lines))

  total, _ = probe(out)
  subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(min(12.0, total / 3)), '-i', str(out), '-frames:v', '1',
                  str(root / 'poster.png')], check=True)
  if ns.contact:
    step = max(1.0, total / 30)  # 30 evenly spaced frames across the whole video
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(out), '-vf', f'fps=1/{step:.3f},scale=480:-1,tile=5x6',
                    '-frames:v', '1', str(root / 'contact.png')], check=True)
  print(f'done: {out} ({total / 60:.1f} min) in {int(time.time() - t0)}s', flush=True)


if __name__ == '__main__':
  main()
