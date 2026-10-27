"""Download third-party inputs for the transfer analysis and verify their SHA-256 hashes.

The two promoter-annotation tables are published by the authors of the source study
(github.com/yj-tan/ExP-MPRA, no license file at the pinned commit). They are fetched
from a pinned commit rather than redistributed. Pass --counts to also fetch the
approximately 30 MB processed GEO count file.
"""
import argparse
import hashlib
from pathlib import Path
import sys
import urllib.request

HERE = Path(__file__).resolve().parent
COMMIT = "d73ad23ce29395d7b338d592b736804267554f2c"
RAW = f"https://raw.githubusercontent.com/yj-tan/ExP-MPRA/{COMMIT}/annotations"
GEO = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE334nnn/GSE334082/suppl"
ANNOTATIONS = {
  "500P_annotations.txt": (
    196550,
    "3e24ea1856ec0e957e3096ed799bbe99c769dc27b920a60c401c99836037b117",
  ),
  "78P_annotations.txt": (
    31808,
    "56fea65b72d557afc2fcd5e1d641f3691941f382d4d82ebf2fbf6ac94a09aa47",
  ),
}
COUNTS = {
  "GSE334082_21Ex500P_upstream_integrated_BC_counts.txt.gz": (
    30141417,
    "9e311cb5560905beca4478973ed84dfdaf0227a33f633896f891b8d14ef65dff",
  ),
}


def sha256(path):
  digest = hashlib.sha256()
  with path.open("rb") as stream:
    for block in iter(lambda: stream.read(1 << 20), b""):
      digest.update(block)
  return digest.hexdigest()


def fetch(name, url, size, expected):
  target = HERE / name
  if target.exists() and sha256(target) == expected:
    print(f"{name}: present, hash verified", flush=True)
    return
  partial = target.with_name(target.name + ".part")
  print(f"{name}: downloading {url}", flush=True)
  try:
    with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as out:
      received = 0
      for block in iter(lambda: response.read(1 << 20), b""):
        out.write(block)
        received += len(block)
        print(f"  {received:,} of {size:,} bytes", flush=True)
  except OSError as error:
    partial.unlink(missing_ok=True)
    sys.exit(f"{name}: download failed ({error}); if certificate verification fails, "
             "install your Python's CA certificates or download the URL manually")
  actual = sha256(partial)
  if actual != expected or partial.stat().st_size != size:
    partial.unlink()
    sys.exit(f"{name}: hash mismatch (got {actual}); file not written")
  partial.replace(target)
  print(f"{name}: written, hash verified", flush=True)


def main():
  parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
  parser.add_argument("--counts", action="store_true", help="also fetch the GEO count file")
  args = parser.parse_args()
  for name, (size, expected) in ANNOTATIONS.items():
    fetch(name, f"{RAW}/{name}", size, expected)
  if args.counts:
    for name, (size, expected) in COUNTS.items():
      fetch(name, f"{GEO}/{name}", size, expected)


if __name__ == "__main__":
  main()
