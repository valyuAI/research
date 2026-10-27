"""Serve this video folder locally with byte-range support for MP4 seeking."""
import argparse
import http.server
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class RangeHandler(http.server.SimpleHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=str(ROOT), **kwargs)

  def send_head(self):
    self.remaining = None
    path = Path(self.translate_path(self.path))
    header = self.headers.get('Range')
    if not header or path.suffix != '.mp4':
      return super().send_head()
    bounds = header.removeprefix('bytes=').split('-', 1)
    total = path.stat().st_size
    start = int(bounds[0] or 0)
    end = min(int(bounds[1]) if bounds[1] else total-1, total-1)
    self.send_response(206)
    self.send_header('Content-Type', 'video/mp4')
    self.send_header('Accept-Ranges', 'bytes')
    self.send_header('Content-Range', f'bytes {start}-{end}/{total}')
    self.send_header('Content-Length', str(end-start+1))
    self.end_headers()
    self.remaining = end-start+1
    f = path.open('rb')
    f.seek(start)
    return f

  def copyfile(self, source, outputfile):
    try:
      if self.remaining is None:
        return super().copyfile(source, outputfile)
      while self.remaining:
        chunk = source.read(min(65536, self.remaining))
        if not chunk:
          break
        outputfile.write(chunk)
        self.remaining -= len(chunk)
    except (BrokenPipeError, ConnectionResetError):
      pass  # Browsers cancel byte ranges when seeking.

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, default=8000)
  args = parser.parse_args()
  server = http.server.ThreadingHTTPServer(('127.0.0.1', args.port), RangeHandler)
  print(f'Open http://127.0.0.1:{server.server_port}/preview.html', flush=True)
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    server.server_close()
