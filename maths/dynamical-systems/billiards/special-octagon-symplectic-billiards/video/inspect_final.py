"""Validate actual encoded media and extract reproducible inspection frames."""
import argparse
import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
sys.dont_write_bytecode = True
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = next(p for p in ROOT.parents if (p / "tools/video/render.py").exists())
OUT = ROOT / "audit"
OUT.mkdir(exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument("--input", default="video-1080p-candidate.mp4")
args = parser.parse_args()
video = ROOT / args.input


def probe(path):
  return json.loads(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries",
    "stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels,duration,bit_rate,nb_frames:format=duration,size",
    "-of", "json", str(path)], text=True))


meta = probe(video)
streams = meta["streams"]
v = next(s for s in streams if s["codec_type"] == "video")
a = next(s for s in streams if s["codec_type"] == "audio")
assert (v["width"], v["height"], v["r_frame_rate"], v["codec_name"]) == (1920, 1080, "30/1", "h264")
assert a["codec_name"] == "aac" and float(a["duration"]) > 0 and int(a["bit_rate"]) > 0
total = float(meta["format"]["duration"])
tree = ast.parse((ROOT / "scenes.py").read_text())
scenes = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == "SCENES" for t in n.targets))
narration = json.loads((ROOT / "narration.json").read_text())
durations = json.loads((ROOT / "audio/durations.json").read_text())
manifest = json.loads((ROOT / "audio/manifest.json").read_text())
audioSpec = importlib.util.spec_from_file_location("shared_audio", REPO / "tools/video/make_audio.py")
audioTool = importlib.util.module_from_spec(audioSpec)
audioSpec.loader.exec_module(audioTool)
for clip in narration["clips"]:
  key = clip["id"]
  expected = audioTool.digest(clip["text"], narration.get("voice", "cedar"),
                              narration.get("instructions", audioTool.DEFAULT_INSTRUCTIONS))
  assert manifest[key]["hash"] == expected, f"Stale audio: {key}"
  actual = float(probe(ROOT / "audio" / f"{key}.mp3")["format"]["duration"])
  assert abs(actual - durations[key]) < 0.003, key

timeline, clipIndex, offset = [], {}, 0.0
for name in scenes:
  part = ROOT / "media/videos/scenes/1080p30" / f"{name}.mp4"
  duration = float(probe(part)["format"]["duration"])
  timings = json.loads((ROOT / "media/timings" / f"{name}.json").read_text())
  lastEnd = -1
  for clip in timings["clips"]:
    assert clip["start"] >= lastEnd - 1 / 30, f"Speech overlap: {name}/{clip['id']}"
    lastEnd = clip["start"] + clip["duration"]
    assert lastEnd <= duration + 0.05, f"Truncated speech: {clip['id']}"
    clipIndex[clip["id"]] = {"scene": name, "start": offset + clip["start"], "duration": clip["duration"]}
  timeline.append({"scene": name, "start": offset, "duration": duration})
  offset += duration
assert set(clipIndex) == {c["id"] for c in narration["clips"]}
assert abs(offset - total) < 0.15, (offset, total)
(OUT / "scene-index.json").write_text(json.dumps({"scenes": timeline, "clips": clipIndex}, indent=2) + "\n")
(OUT / "ffprobe.json").write_text(json.dumps(meta, indent=2) + "\n")

selected = {"start": 12.0, "middle": total / 2, "end": total - 3}
keyClips = (["s06_stretch", "s07_fail", "s09_halve", "s09_rescue", "s11_squeeze", "s11_never", "s12_priority"]
            if "s09_rescue" in clipIndex else
            ["s05_totals", "s06_hull", "s10_draw", "s10_balance", "s11_factors", "s11_cancel", "s13_contra", "s14_caveat"])
for key in keyClips:
  c = clipIndex[key]
  selected[key] = c["start"] + 0.92 * c["duration"]
frames = OUT / "frames"
frames.mkdir(exist_ok=True)
for i, (label, timestamp) in enumerate(selected.items(), 1):
  subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-ss", str(timestamp),
                  "-i", str(video), "-frames:v", "1", str(frames / f"{label}.png")], check=True)
  print(f"[{i}/{len(selected)}] frame {label} at {timestamp:.3f}s", flush=True)
report = {
  "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
  "input": video.name, "duration_seconds": total, "streams": streams,
  "sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
  "narration_clips": len(clipIndex), "source_audio_hashes_match": True,
  "measured_clip_durations_match": True, "no_narration_overlap_or_truncation": True,
  "scene_duration_sum_matches_output": True,
  "frames": selected, "listening_review_performed": False,
  "visual_review": "Pending manual inspection of extracted frames and contact sheet"
}
(OUT / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"video": str(video), "duration": total, "clips": len(clipIndex),
                  "dimensions": [v["width"], v["height"]], "fps": v["r_frame_rate"],
                  "codecs": [v["codec_name"], a["codec_name"]]}, indent=2), flush=True)

