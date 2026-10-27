"""Package narration, local player and source ledger; verify frozen research inputs."""
import ast
import hashlib
import html
import json
from pathlib import Path
import re
import textwrap

ROOT=Path(__file__).resolve().parent
FINDING=ROOT.parent
name=FINDING.name
info={
  'three-team-manipulation-exact':{
    'title':'How much can three teams gain by fixing their matches?',
    'scope':'Exact optimum 1/3 for n=3,4 and 2/5 for n=5..8, for coalitions of at most three; monotone/top-cycle certificates attain the same optima. Separate n=7, k=4 optimum 3/7. No arbitrary-team-count result.',
    'evidence':['verification/certificates/rule_n5_k3_mt_small.json','verification/results/rule_n8_k3.result.json','verification/results/rule_n8_k3_mt.result.json','verification/results/rule_n7_k4.result.json'],
    'credit':'The five-team lower-bound argument is Schneider, Schvartzman and Weinberg (2017), Theorem 3.2. The broad conjecture was refuted for some large coalitions by Schvartzman, Weinberg, Zlatin and Zuo (2020). The finite fraction tables are the contribution illustrated here.',
    'links':['https://arxiv.org/html/1605.09733','https://arxiv.org/html/1906.03324v2','https://arxiv.org/html/2407.17569v1'],
    'simplifications':'The linear-program feasible region and slack bars are explicitly schematic. The averaging proof is animated in full for five teams; the complete canonical-form and rational replay algorithms remain in the paper. Fourteen pass results are from the finalized research handoff, not fresh full replays by this video worker.'},
  'standard-parameter-counterexamples':{
    'title':'A stable pattern outside the clique prediction',
    'scope':'G11 at epsilon=1/4, delta=1/2, theta=1 has stable nonclique full support and is vertex-minimal. Every CTLN at this epsilon/delta pair is nondegenerate. Complete exclusion through seven gives an 8..11 minimum support-size bracket. No global minimum-11 or first-standard-counterexample assertion.',
    'evidence':['verification/examples/G11.json','verification/examples/G11_certificate.json','verification/scan_results/n7_recovered.recheck.json','verification/scan_results/final_summary.json'],
    'credit':'Curto, Geneson and Morrison proposed the target-free clique conjecture. Geneson (2026) disproved it at other parameters. hturcotte1/CLTN commit 3744200 (15 October 2026) already implied standard-point counterexamples, including W4 on 23 vertices, and the n<=7 exclusion. G11 was found by shrinking and modifying that example.',
    'links':['https://github.com/hturcotte1/CLTN/commit/3744200','https://arxiv.org/abs/2301.12638'],
    'simplifications':'The Hurwitz criterion is introduced through the quadratic case and its actual first three determinants, with all eleven positive checks displayed; its general theorem is not derived. Matrix entries and rates are actual certificate data. prepare_assets.py verifies every fixed-point row exactly. The G11 plot is one numerical 0.1% sinusoidal relative perturbation and is not a basin theorem. The two-neuron return uses an exact decaying mode. The n7 scan uses certified residual rejections under the documented IEEE model and exact saved-candidate replay, not 882 million exact eigenvalue calculations.'},
  'four-negative-eigenvalues':{
    'title':'Why four negative eigenvalues permit at most thirty essential dots',
    'scope':'n(4)=30 for reduced graphs. Four order-30 classes all have inertia (4,22,4), rank 8. W5 and X are the only reduced graphs attaining eleven positive and four negative eigenvalues. No theorem for five or more negatives.',
    'evidence':['verification/order30_graphs.g6','verification/final_order30_check.json','verification/extremal_result.json','verification/census_counts.json','verification/final_census_result.json','verification/max_reduced_order.log','verification/max_reduced_order_check.log'],
    'credit':'ACK (Akbari, Cameron and Khosrovshahi, 2004) already supplied the four rank-8 classes, both doubling constructions and the compatibility method. Kotlov and Lovasz (1996) supplied the ordinary doubling. CFJK (Charles, Farber, Johnson and Kennedy-Shaffer, 2013) supplied W5/X and the numerical bound; the identity of Elphick and colleagues (2026) makes its implication explicit. Retained increments: exclusion of other ranks, especially 9..15, and uniqueness. Jacobi, the known core lemma, Basso and principal-rank precedents are credited in the paper.',
    'links':['https://webspace.maths.qmul.ac.uk/p.j.cameron/preprints/ranksign.pdf','https://arxiv.org/abs/1108.4810','https://arxiv.org/abs/2609.06319','https://doi.org/10.1016/j.laa.2022.01.011'],
    'simplifications':'The K2 eigenpairs, duplicate cancellation and K2-to-triangle Schur complement are exact worked calculations. The general Jacobi, inertia-additivity and reconstruction arguments are mechanism sketches, with full derivations in the paper. All displayed extremal graphs are built and checked from exact definitions. The complete census and maximum-order computations are finalized recorded research evidence, not regenerated for this animation. Torgasev 1987 and Mohammadian 2022 full texts were unavailable in the priority audit; no first-ever assertion is made.'},
}[name]

hashes={}
for line in (FINDING/'verification/evidence.sha256').read_text().splitlines():
  if not line.strip():continue
  digest,relative=line.split(maxsplit=1);relative=relative.lstrip('* ')
  path=FINDING/relative
  actual=hashlib.sha256(path.read_bytes()).hexdigest()
  assert actual==digest,(relative,digest,actual)
  hashes[relative]=actual
for relative in ['paper.tex','readiness.md','review.md','video-brief.md','verification/README.md']:
  hashes[relative]=hashlib.sha256((FINDING/relative).read_bytes()).hexdigest()
(ROOT/'research-input-sha256.json').write_text(json.dumps(hashes,indent=2))
print(f'{name}: {len(hashes)} research input hashes verified/frozen',flush=True)

tree=ast.parse((ROOT/'write_story.py').read_text())
beats=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='BEATS' for t in n.targets))
ledger=['# Sources and scope\n',info['scope'],'\n## Scientific provenance\n',info['credit'],'\n## Local authoritative inputs\n']
for relative in ['paper.tex','readiness.md','review.md','video-brief.md','verification/README.md',*info['evidence']]:
  path=FINDING/relative
  assert path.exists(),path
  ledger.append(f'- [{relative}](../{relative}), SHA-256 `{hashlib.sha256(path.read_bytes()).hexdigest()}`.')
ledger+=['\nAll research evidence manifest entries were verified during packaging. The full snapshot is in `research-input-sha256.json`. The final research handoff reports correctness confidence high and originality confidence moderate, with the CTLN arithmetic and priority limitations stated in its readiness file.\n','## Beat-level evidence\n','| Clip | Source supporting the spoken claim |','|---|---|']
ledger += [f'| {i} | {e} |' for _,i,_,_,e in beats]
ledger += ['\n## Primary references\n','The research review and its source retrievals are reused from 26 October 2026; no new priority search or claim of fresh online retrieval is made by the video pass. See the finding references.bib for complete citations.']
ledger += [f'- [{u}]({u})' for u in info['links']]
ledger += ['\n## Explanatory simplifications\n',info['simplifications'],'\n## Media provenance\n','Local unpublished production. Cedar synthetic narration, gpt-4o-mini-tts-2025-12-15, generated through the installed speech SDK wrapper with credentials from the existing private environment. No credentials are stored here. Audio manifests bind text, voice and instructions; QA also hashes the files. The end card discloses the synthetic voice. No subjective listening review is claimed.']
(ROOT/'sources.md').write_text('\n'.join(ledger)+'\n')

spec=json.loads((ROOT/'narration.json').read_text())
transcript='\n\n'.join(f'## {s} / {i}\n\n{t}' for s,i,t,_,_ in beats)
(ROOT/'transcript.md').write_text(f'# {info["title"]}\n\n{transcript}\n')
if (ROOT/'subtitles.srt').exists():
  srt=(ROOT/'subtitles.srt').read_text()
  vtt=re.sub(r'(\d\d:\d\d:\d\d),(\d{3})',r'\1.\2',srt)
  vtt=re.sub(r'(\d\d:\d\d:\d\d\.\d{3} --> \d\d:\d\d:\d\d\.\d{3})',r'\1 line:2% position:50% size:94% align:center',vtt)
  blocks=[]
  for block in vtt.strip().split('\n\n'):
    lines=block.splitlines()
    blocks.append('\n'.join(lines[:2])+ '\n'+textwrap.fill(' '.join(lines[2:]),width=60,break_long_words=False,break_on_hyphens=False))
  vtt='\n\n'.join(blocks)+'\n'
  (ROOT/'subtitles.vtt').write_text('WEBVTT\n\n'+vtt)
body=''.join(f'<h2>{html.escape(s)} / {i}</h2><p>{html.escape(t)}</p>' for s,i,t,_,_ in beats)
(ROOT/'preview.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(info['title'])}</title><style>body{{margin:32px auto;padding:0 24px;max-width:1000px;background:#0d0f12;color:#f4f4f4;font:18px/1.6 system-ui}}video{{width:100%;height:auto}}a{{color:#70c9bd}}h1{{font-size:28px}}h2{{font-size:20px;margin-top:32px}}p{{max-width:75ch}}details{{margin-top:28px}}summary{{cursor:pointer}}</style><h1>{html.escape(info['title'])}</h1><video controls preload="metadata" poster="poster.png"><source src="video.mp4" type="video/mp4"><track kind="captions" src="subtitles.vtt" srclang="en" label="English" default>Your browser cannot play this video. <a href="video.mp4">Download the MP4</a>.</video><p><a href="video.mp4">MP4</a> · <a href="subtitles.srt">Subtitles</a> · <a href="sources.md">Sources</a> · <a href="scenes.py">Editable animation</a></p><details><summary>Full narration transcript</summary>{body}</details></html>''')
(ROOT/'README.md').write_text(f'''# {info['title']}

{info['scope']}

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

{info['simplifications']}
''')
print('Sources, transcript, rebuild instructions and local accessible player written.',flush=True)
