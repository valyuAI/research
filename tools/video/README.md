# Explainer video toolkit

Each finding can carry a narrated explainer in `<finding>/video/`, written with
[Manim Community](https://www.manim.community/) and narrated from a script. Scene timing
follows the measured length of each narration clip, so pictures and speech stay in step.

## Layout of a video folder

```text
video/
  storyboard.md    scene-by-scene plan: narration, visual, what the viewer learns
  narration.json   {"voice": "cedar", "clips": [{"id": "s01_hook", "text": "..."}]}
  scenes.py        SCENES = [...] in playing order; scenes subclass NarratedScene
  audio/           one mp3 per clip, durations.json, manifest.json
  video.mp4        final 1080p30 H.264/AAC render
  subtitles.srt    generated from clip timings
  poster.png       still frame
```

## Build

Requirements: Python 3.12 with `manim==0.22.0` and `openai`, ffmpeg, a TeX installation
with `standalone`, `preview`, `doublestroke`, `relsize`, `setspace`, `rsfs` and `dvisvgm`,
and Node 22.18 or newer for the narration wrapper. `OPENAI_API_KEY` is read from a private
env file (default `~/.env.local`); it is never passed on the command line.

```bash
python tools/video/render.py path/to/video --quality l --contact   # silent preview
python tools/video/make_audio.py path/to/video                     # narration clips
python tools/video/render.py path/to/video --quality h --contact   # final render
```

`make_audio.py` only regenerates clips whose text changed. Without audio, scenes use
word-count estimates so the layout can be previewed before narration exists.

## Minimal scene

```python
from manim import *
from vrvideo import *

SCENES = ['Hook']


class Hook(NarratedScene):
  def construct(self):
    square = Square(2, color=PRIMARY)
    with self.say('s01_hook') as d:  # d is the clip length in seconds
      self.play(Create(square), run_time=0.4 * d)
      self.play(square.animate.stretch(1.5, 0), run_time=0.4 * d)
```

The narration voice is synthetic; every video says so on its end card.
