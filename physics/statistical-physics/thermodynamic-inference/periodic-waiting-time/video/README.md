# Explainer video: a machine that wastes nothing, but looks like it does

`video.mp4` (about 9 min 40 s, 1080p30, narrated) explains this finding for a GCSE-level
viewer. It starts from a ball bouncing backwards (the arrow of time) and builds a three-square
board game: hopping rates, probabilities, traffic, detailed balance, entropy production, and the
waiting-time test that compares a pair of visible jumps with its reverse. It then drives the
paper's network (door a has rate `1 + epsilon cos t`, door b has rate `1 + epsilon sin t`, and the
hidden line has rate 1), shows that its entropy production is exactly zero, and animates the exact
identity `(f - g)'(0) = epsilon^2`. At `epsilon = 1/2` the starting slopes are -2.125 and -2.375.
The pairwise score `(f - g) log(f/g)` is never negative, so the forward-protocol estimate is positive
and the conjectured bound fails. The video is explicit about scope: the reversed-protocol theorem
still stands, earlier false-positive work is credited, the cost of the device that drives the rates
is not claimed, and there is no formal proof or external review. Rebuild it from the repository root
with `python tools/video/render.py <this folder> --quality l --contact` for a silent preview,
`python tools/video/make_audio.py <this folder>` for narration (only changed clips are regenerated),
and `python tools/video/render.py <this folder> --quality h --contact` for the final render. Use the
toolkit's Python environment (manim 0.22). `storyboard.md` holds the scene plan and the number ledger.
The narration uses a synthetic voice.
