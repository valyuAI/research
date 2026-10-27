# A stable pattern outside the clique prediction

G11 at epsilon=1/4, delta=1/2, theta=1 has stable nonclique full support and is vertex-minimal. Every CTLN at this epsilon/delta pair is nondegenerate. Complete exclusion through seven gives an 8..11 minimum support-size bracket. No global minimum-11 or first-standard-counterexample assertion.

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

The Hurwitz criterion is introduced through the quadratic case and its actual first three determinants, with all eleven positive checks displayed; its general theorem is not derived. Matrix entries and rates are actual certificate data. prepare_assets.py verifies every fixed-point row exactly. The G11 plot is one numerical 0.1% sinusoidal relative perturbation and is not a basin theorem. The two-neuron return uses an exact decaying mode. The n7 scan uses certified residual rejections under the documented IEEE model and exact saved-candidate replay, not 882 million exact eigenvalue calculations.
