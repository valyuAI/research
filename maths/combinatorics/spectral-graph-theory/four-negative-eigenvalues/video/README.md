# Why four negative eigenvalues permit at most thirty essential dots

n(4)=30 for reduced graphs. Four order-30 classes all have inertia (4,22,4), rank 8. W5 and X are the only reduced graphs attaining eleven positive and four negative eigenvalues. No theorem for five or more negatives.

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

The K2 eigenpairs, duplicate cancellation and K2-to-triangle Schur complement are exact worked calculations. The general Jacobi, inertia-additivity and reconstruction arguments are mechanism sketches, with full derivations in the paper. All displayed extremal graphs are built and checked from exact definitions. The complete census and maximum-order computations are finalized recorded research evidence, not regenerated for this animation. Torgasev 1987 and Mohammadian 2022 full texts were unavailable in the priority audit; no first-ever assertion is made.
