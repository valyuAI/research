"""Check the local accessible player in a fresh, muted headless browser."""
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
from serve import RangeHandler

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), RangeHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
checks = []
try:
  with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1100})
    page.goto(f'http://127.0.0.1:{server.server_port}/preview.html')
    page.wait_for_function('document.querySelector("video").readyState >= 1')
    metadata = page.evaluate('''() => {
      const v = document.querySelector('video');
      v.muted = true;
      v.textTracks[0].mode = 'showing';
      return {width:v.videoWidth, height:v.videoHeight, duration:v.duration,
        controls:v.controls, captionLanguage:v.textTracks[0].language,
        transcriptSections:document.querySelectorAll('details h2').length};
    }''')
    assert (metadata['width'], metadata['height']) == (1920, 1080), metadata
    assert metadata['controls'] and metadata['transcriptSections'] >= 32
    for at in [3, metadata['duration']/2, metadata['duration']-6]:
      print(f'Playback sample at {at:.2f}s', flush=True)
      page.evaluate('(t) => { document.querySelector("video").currentTime=t; }', at)
      page.wait_for_function('!document.querySelector("video").seeking')
      start = page.evaluate('document.querySelector("video").currentTime')
      assert abs(start-at) < 0.2, (start, at)
      page.evaluate('document.querySelector("video").play()')
      page.wait_for_timeout(1500)
      sample = page.evaluate('''() => {
        const v=document.querySelector('video'); v.pause();
        return {time:v.currentTime, error:v.error, readyState:v.readyState,
          cueCount:v.textTracks[0].cues.length,
          activeCaptions:Array.from(v.textTracks[0].activeCues).map(c=>c.text),
          droppedFrames:v.getVideoPlaybackQuality().droppedVideoFrames};
      }''')
      sample['requestedTime'] = at
      sample['advancedSeconds'] = sample['time']-start
      assert sample['error'] is None and sample['advancedSeconds'] > 0.8, sample
      assert sample['cueCount'] > 0, sample
      checks.append(sample)
    page.screenshot(path=str(ROOT/'qa/browser-player.png'), full_page=False)
    browser.close()
finally:
  server.shutdown()
(ROOT/'qa/browser-playback.json').write_text(json.dumps({
  'metadata':metadata, 'samples':checks,
  'mode':'Installed Chrome, fresh context, muted headless playback. No listening.',
}, indent=2)+'\n')
print('Native player, seeking, advancing playback and caption loading passed.', flush=True)
