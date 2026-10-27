#!/usr/bin/env python3
"""Generate narration clips for one video directory and record their lengths.

  python make_audio.py <video-dir> [--dry-run] [--env-file ~/.env.local]

Reads <video-dir>/narration.json:
  {"voice": "cedar", "instructions": "...", "clips": [{"id": "s1_intro", "text": "..."}]}
Writes <video-dir>/audio/<id>.mp3, audio/durations.json and audio/manifest.json.
Only clips that are missing or whose text changed are (re)generated, so reruns are cheap.
The API key is read by the narration wrapper from the env file; it never appears in
arguments or output.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WRAPPER = Path.home() / '.agents/skills/explainer-video/scripts/narrate.mjs'
MODEL = 'gpt-4o-mini-tts-2025-12-15'
DEFAULT_INSTRUCTIONS = (
  'Voice Affect: warm, curious and unhurried, like a teacher who loves the subject.\n'
  'Tone: friendly, clear and conversational; never salesy.\n'
  'Pacing: measured, with natural pauses between ideas; slow down slightly for numbers and formulas.\n'
  'Pronunciation: read mathematical symbols as words, as written in the text.'
)


def digest(text, voice, instructions):
  return hashlib.sha256(f'{MODEL}|{voice}|{instructions}|{text}'.encode()).hexdigest()[:16]


def duration(path):
  out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(path)],
                       capture_output=True, text=True, check=True).stdout
  return float(json.loads(out)['format']['duration'])


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument('video_dir')
  ap.add_argument('--dry-run', action='store_true')
  ap.add_argument('--env-file', default=str(Path.home() / '.env.local'))
  ns = ap.parse_args()

  root = Path(ns.video_dir).resolve()
  spec = json.loads((root / 'narration.json').read_text())
  voice = spec.get('voice', 'cedar')
  instructions = spec.get('instructions', DEFAULT_INSTRUCTIONS)
  audio = root / 'audio'
  audio.mkdir(exist_ok=True)
  manifest_path = audio / 'manifest.json'
  manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

  ids = [c['id'] for c in spec['clips']]
  if len(ids) != len(set(ids)):
    sys.exit('narration.json has duplicate clip ids')
  for c in spec['clips']:
    if len(c['text']) > 4000:
      sys.exit(f'clip {c["id"]} is longer than 4000 characters; split it')

  jobs = []
  for c in spec['clips']:
    h = digest(c['text'], voice, instructions)
    mp3 = audio / f'{c["id"]}.mp3'
    if mp3.exists() and manifest.get(c['id'], {}).get('hash') == h:
      continue
    if mp3.exists():
      stale = audio / '.stale'
      stale.mkdir(exist_ok=True)
      shutil.move(str(mp3), str(stale / mp3.name))
    jobs.append({'input': c['text'], 'out': mp3.name, 'voice': voice})
    manifest[c['id']] = {'hash': h, 'model': MODEL, 'voice': voice}

  print(f'{len(jobs)} clip(s) to generate, {len(ids) - len(jobs)} up to date', flush=True)
  if jobs:
    with tempfile.TemporaryDirectory() as tmp:
      jl = Path(tmp) / 'jobs.jsonl'
      jl.write_text(''.join(json.dumps(j) + '\n' for j in jobs))
      ins = Path(tmp) / 'instructions.txt'
      ins.write_text(instructions)
      cmd = ['node', str(WRAPPER), '--env-file', ns.env_file, '--python', sys.executable, '--',
             'speak-batch', '--input', str(jl), '--out-dir', str(audio), '--model', MODEL, '--voice', voice,
             '--instructions-file', str(ins), '--rpm', '30', '--attempts', '2']
      if ns.dry_run:
        cmd.append('--dry-run')
      rc = subprocess.run(cmd).returncode
      if rc != 0:
        sys.exit(f'narration failed with exit code {rc}; rerun to resume missing clips')
  if ns.dry_run:
    return

  durations = {}
  for i in ids:
    mp3 = audio / f'{i}.mp3'
    if not mp3.exists():
      sys.exit(f'missing clip {mp3}')
    durations[i] = round(duration(mp3), 3)
  (audio / 'durations.json').write_text(json.dumps(durations, indent=2))
  manifest_path.write_text(json.dumps({k: v for k, v in manifest.items() if k in durations}, indent=2))
  total = sum(durations.values())
  print(f'{len(durations)} clips, {total / 60:.1f} min of narration -> {audio / "durations.json"}', flush=True)


if __name__ == '__main__':
  main()
