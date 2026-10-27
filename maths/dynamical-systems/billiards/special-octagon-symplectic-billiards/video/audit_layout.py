"""Render one still per narration beat without encoding a movie."""
import importlib.util
import json
import os
import sys
from contextlib import contextmanager
from pathlib import Path

from manim import MathTex, Tex, config, tempconfig
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
REPO = next(p for p in ROOT.parents if (p / "tools/video/vrvideo").exists())
sys.path.insert(0, str(REPO / "tools/video"))
os.environ["VR_VIDEO_DIR"] = str(ROOT)
from vrvideo import NarratedScene

OUT = ROOT / "audit/layout"
OUT.mkdir(parents=True, exist_ok=True)
originalSay = NarratedScene.say
records = []


@contextmanager
def inspectSay(self, key, pause=None):
  with originalSay(self, key, pause=pause) as duration:
    yield duration
  self.renderer.update_frame(self)
  Image.fromarray(self.renderer.get_frame()).save(OUT / f"{key}.png")
  overflow = []
  seen = set()
  for top in self.mobjects:
    for mob in top.get_family():
      if isinstance(mob, (Tex, MathTex)) and id(mob) not in seen:
        seen.add(id(mob))
        if mob.width and (mob.get_left()[0] < -7.05 or mob.get_right()[0] > 7.05
                         or mob.get_top()[1] > 3.95 or mob.get_bottom()[1] < -3.95):
          overflow.append(getattr(mob, "tex_string", repr(mob)))
  records.append({"clip": key, "overflow": overflow})
  print(f"  {key}: {len(overflow)} possible text overflows", flush=True)


NarratedScene.say = inspectSay
os.chdir(ROOT)
with tempconfig({"dry_run": True, "skip_animations": True, "write_to_movie": False,
                 "save_last_frame": False, "pixel_width": 1920, "pixel_height": 1080,
                 "frame_rate": 30, "progress_bar": "none", "verbosity": "ERROR"}):
  spec = importlib.util.spec_from_file_location("video_scenes", ROOT / "scenes.py")
  scenes = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(scenes)
  selected = sys.argv[1:] or scenes.SCENES
  for i, name in enumerate(selected, 1):
    print(f"[{i}/{len(selected)}] layout: {name}", flush=True)
    getattr(scenes, name)().render()
(OUT / "report.json").write_text(json.dumps(records, indent=2))
thumbW, thumbH = 480, 295
sheet = Image.new("RGB", (thumbW * 4, thumbH * ((len(records) + 3) // 4)), "#0d0f12")
draw = ImageDraw.Draw(sheet)
for i, record in enumerate(records):
  x, y = (i % 4) * thumbW, (i // 4) * thumbH
  with Image.open(OUT / f'{record["clip"]}.png') as frame:
    frame.thumbnail((480, 270))
    sheet.paste(frame, (x, y))
  draw.text((x + 8, y + 273), record["clip"], fill="white")
sheet.save(OUT / "contact.png")
print(f"Saved {len(records)} beat stills to {OUT}", flush=True)

