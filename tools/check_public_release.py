"""Check publication hygiene without printing matched sensitive values."""

import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "personal filesystem path": re.compile(rb"/(?:Users|home)/[A-Za-z0-9_.-]+/"),
    "signed download URL": re.compile(rb"[?&]X-Amz-(?:Signature|Credential)="),
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub credential": re.compile(
        rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"
    ),
}


def main():
    failures = []
    scanned = 0
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=False
    )
    paths = (
        [ROOT / name.decode() for name in tracked.stdout.split(b"\0") if name]
        if tracked.returncode == 0 and tracked.stdout
        else sorted(ROOT.rglob("*"))
    )
    for path in paths:
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts:
            continue
        if any(
            part.is_symlink() for part in (path, *path.parents) if ROOT in part.parents
        ):
            failures.append((str(relative), "symlink"))
            continue
        if not path.is_file():
            continue
        scanned += 1
        # Binary media metadata was audited at release. Scan all text and PDFs;
        # do not decode hundreds of megabytes of audio/video on every CI run.
        if path.suffix.lower() in {
            ".mp4",
            ".mp3",
            ".wav",
            ".png",
            ".jpg",
            ".jpeg",
            ".gz",
        }:
            continue
        data = path.read_bytes()
        for name, pattern in PATTERNS.items():
            if pattern.search(data):
                failures.append((str(relative), name))

    omissions = json.loads(
        (ROOT / "public-release/export-exclusions.json").read_text()
    )["omit"]
    for relative in omissions:
        path = ROOT / relative
        if path.exists() or path.is_symlink():
            failures.append((relative, "excluded file present"))

    for relative, reason in failures:
        print(f"FAIL {relative}: {reason}")
    print(
        f"Publication hygiene: {scanned} files, {len(omissions)} omissions, {len(failures)} failures"
    )
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
