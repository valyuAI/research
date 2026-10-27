# How much can three teams gain by fixing their matches?

Exact optimum 1/3 for n=3,4 and 2/5 for n=5..8, for coalitions of at most three; monotone/top-cycle certificates attain the same optima. Separate n=7, k=4 optimum 3/7. No arbitrary-team-count result.

Play `video.mp4` directly. For the captioned browser player and full transcript, run `python3 serve.py` from this directory and open `http://127.0.0.1:8000/preview.html`. The local server supports MP4 byte ranges for seeking. The final deliverable is native 1920x1080, 30 fps, H.264/AAC, with Cedar narration. See `QA.md` for measured runtime and verification. `subtitles.srt` and `subtitles.vtt` are phrase captions timed from measured audio; they are not word-aligned. The exact script is in `narration.json` and `transcript.md`.

Edit `scenes.py` for motion and `write_story.py` for narration and storyboard. `sources.md` maps every beat to evidence. `audio/` holds generated clips, measured durations and text/voice digests. The original preview and all concept/boundary frames are retained under `preview-evidence/`; final checks are in `qa/` and `final-evidence/`. The existing `tools/video` runtime remains unchanged.

Rebuild inside this video directory with the existing environment, one render at a time:

```sh
V=${VIDEO_PYTHON:-python3}
"$V" -B write_story.py
# For the CTLN and graph films, also run: "$V" -B prepare_assets.py
"$V" -B run_stage.py dry-audio
"$V" -B run_stage.py audio
"$V" -B run_stage.py final
"$V" -B run_stage.py qa
"$V" -B audit_audio.py
"$V" -B inspect_frames.py
"$V" -B package.py
```

The local stage runner sets nice 10 and single-thread BLAS, writes the active PID/log and reports every 15 seconds. Final renders hold the campaign shared advisory lock for the entire subprocess. No dependency installation is required. Source/audio edits require a fresh final render and QA. No audio listening is claimed; objective duration, waveform, order and decode checks cannot establish subjective pronunciation. No upload, publication or contact is authorised by these artifacts.

The linear-program feasible region and slack bars are explicitly schematic. The averaging proof is animated in full for five teams; the complete canonical-form and rational replay algorithms remain in the paper. Fourteen pass results are from the finalized research handoff, not fresh full replays by this video worker.
