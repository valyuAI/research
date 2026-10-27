"""Scenes whose timing follows real narration clips.

Usage inside a scene:

    with self.say('s1_intro') as d:      # starts audio clip s1_intro, d = its length (s)
      self.play(Create(square), run_time=0.4 * d)
      self.play(Write(label), run_time=0.3 * d)
    # on exit the scene waits until the clip (plus a short pause) has finished

Clip lengths come from audio/durations.json (written by make_audio.py). If the audio has
not been generated yet, lengths are estimated from word counts and no sound is added, so
silent previews can be rendered first. Each scene logs when each clip starts to
media/timings/<Scene>.json; render.py turns that into subtitles.
"""

import json
import os
from contextlib import contextmanager
from pathlib import Path

from manim import Scene, ThreeDScene, MovingCameraScene

WORDS_PER_SECOND = 2.5


def _project_dir():
  return Path(os.environ.get('VR_VIDEO_DIR', Path.cwd())).resolve()


class _NarrationMixin:
  pause_after = 0.4

  def _load_narration(self):
    root = _project_dir()
    self._root = root
    spec = json.loads((root / 'narration.json').read_text())
    self._texts = {c['id']: c['text'] for c in spec['clips']}
    dur_path = root / 'audio' / 'durations.json'
    self._durations = json.loads(dur_path.read_text()) if dur_path.exists() else {}
    self._timings = []

  def clip_duration(self, key):
    if key in self._durations:
      return float(self._durations[key])
    return max(1.5, len(self._texts[key].split()) / WORDS_PER_SECOND)

  @contextmanager
  def say(self, key, pause=None):
    if not hasattr(self, '_texts'):
      self._load_narration()
    if key not in self._texts:
      raise KeyError(f'narration clip {key!r} is not in narration.json')
    duration = self.clip_duration(key)
    audio = self._root / 'audio' / f'{key}.mp3'
    start = self.renderer.time
    if audio.exists() and key in self._durations:
      self.add_sound(str(audio))
    self._timings.append({'id': key, 'start': start, 'duration': duration})
    yield duration
    spent = self.renderer.time - start
    rest = duration + (self.pause_after if pause is None else pause) - spent
    if rest > 1 / 60:
      self.wait(rest)

  def tear_down(self):
    super().tear_down()
    if getattr(self, '_timings', None):
      out = self._root / 'media' / 'timings'
      out.mkdir(parents=True, exist_ok=True)
      (out / f'{type(self).__name__}.json').write_text(json.dumps(
        {'scene': type(self).__name__, 'total': self.renderer.time, 'clips': self._timings}, indent=2))


class NarratedScene(_NarrationMixin, Scene):
  pass


class NarratedThreeDScene(_NarrationMixin, ThreeDScene):
  pass


class NarratedMovingCameraScene(_NarrationMixin, MovingCameraScene):
  pass
