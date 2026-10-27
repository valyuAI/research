"""Build the shared-byline public PDFs from the recorded manuscript sources.

Each public PDF compiles a derived copy of a package's paper.tex in a temporary
directory: Harvey Yorke and Valyu DeepResearch share the byline, while the existing
\\journalversion body disclosures and the standard statement in
public-release/papers/contributions.tex are retained.
Package sources, the original paper.pdf files and docs/artifact-hashes.json are
never written. An export may omit an archival paper.pdf only if
public-release/export-exclusions.json declares it at its release hash. Every
public PDF must be free of local paths and pdfTeX file metadata, checked on the
raw bytes and in decoded Flate streams. Requires pdflatex, bibtex, pdfinfo
and pdftotext.

  python3 tools/public_papers.py build [--only SLUG ...]   write PDFs and manifest
  python3 tools/public_papers.py check [--only SLUG ...]   rebuild and compare
"""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import zlib

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public-release/papers"
STATEMENT = OUTPUT / "contributions.tex"
MANIFEST = OUTPUT / "manifest.json"
RELEASE_HASHES = ROOT / "docs/artifact-hashes.json"
EXCLUSIONS = ROOT / "public-release/export-exclusions.json"
EPOCH = int(datetime.datetime(2026, 10, 27, tzinfo=datetime.timezone.utc).timestamp())
AUTHORS = ("Harvey Yorke", "Valyu DeepResearch")

# Presentation-only wording for the public PDFs; the sources keep the original.
# Each pair must match the stated number of times or the build fails.
WORDING = {
    "acr-multistability-bounds": [
        ("has a hand proof", "has a direct written proof", 1),
        ("are proved by hand and", "have direct written proofs and", 1),
    ],
}
# Product names that must not appear in any public PDF's text.
PRODUCTS = ("Codex", "Claude", "OpenAI", "Anthropic")
# Byte patterns that must not appear in a public PDF, raw or in a decompressed
# stream. Failures name the label only, never the surrounding bytes.
LEAKS = {
    "pdfTeX file metadata": b"PTEX.",
    "macOS home path": b"/Users/",
    "Linux home path": b"/home/",
    "macOS temporary path": b"/var/folders/",
    "private path": b"/private/",
    "temporary path": b"/tmp/",
    "worktree path": b".t3/",
    "texmf home path": b"Library/texmf",
}
# Prepended to the derived source: drop PTEX.FileName, PTEX.PageNumber,
# PTEX.InfoDict and PTEX.Fullbanner, which record absolute figure paths.
PREAMBLE = "\\pdfsuppressptexinfo=-1\n\\def\\journalversion{1}\n"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def papers():
    # Tracked files plus untracked, non-ignored ones, so an uncommitted export works.
    names = subprocess.check_output(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "*/paper.tex",
        ],
        cwd=ROOT,
        text=True,
    ).split()
    found = {}
    for name in sorted(set(names)):
        source = ROOT / name
        slug = source.parent.name
        if slug in found:
            raise ValueError(f"Duplicate paper slug: {slug}")
        found[slug] = source
    return found


def derive(slug, source, statement):
    """Return the public manuscript text and the list of transforms applied."""
    text = source.read_text()
    transforms = ["suppress pdfTeX file metadata", "define \\journalversion"]
    for old, new, count in WORDING.get(slug, []):
        if text.count(old) != count:
            raise ValueError(f"{source}: expected {count} of {old!r}")
        text = text.replace(old, new)
        transforms.append(f"presentation wording: {old!r} -> {new!r} ({count}x)")
    body = text.index("\\begin{document}")
    # Select the shared author layout only in the preamble; keep journalversion
    # enabled in the body so its research-assistance disclosures remain visible.
    preamble = text[:body].replace("\\ifdefined\\journalversion", "\\iffalse")
    text = preamble + text[body:]
    transforms.append("retain Harvey Yorke and Valyu DeepResearch as co-authors")
    body = len(preamble)
    anchor = min(
        text.find(marker, body)
        for marker in ("\\bibliographystyle{", "\\bibliography{")
        if text.find(marker, body) >= 0
    )
    text = text[:anchor] + statement + "\n" + text[anchor:]
    transforms.append(
        "insert public-release/papers/contributions.tex before bibliography"
    )
    return PREAMBLE + text, transforms


def run(command, directory, env, log):
    with log.open("a") as stream:
        result = subprocess.run(
            command, cwd=directory, env=env, stdout=stream, stderr=stream
        )
    if result.returncode:
        tail = log.read_text(errors="replace").splitlines()[-25:]
        raise RuntimeError(f"{command[0]} failed:\n" + "\n".join(tail))


def compile_pdf(slug, source, statement, destination):
    folder = source.parent
    text, transforms = derive(slug, source, statement)
    env = {
        **os.environ,
        # The derived file has its own name, so it can never resolve to the package original.
        "TEXINPUTS": f".{os.pathsep}{folder}{os.pathsep}",
        "BIBINPUTS": f".{os.pathsep}{folder}{os.pathsep}",
        "BSTINPUTS": f".{os.pathsep}{folder}{os.pathsep}",
        "SOURCE_DATE_EPOCH": str(EPOCH),
        "FORCE_SOURCE_DATE": "1",
    }
    latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "public.tex"]
    with tempfile.TemporaryDirectory(prefix=f"public-{slug}-") as work:
        work = Path(work)
        (work / "public.tex").write_text(text)
        for step, command in enumerate([latex, ["bibtex", "public"], latex, latex], 1):
            print(f"  {slug}: step {step}/4 {command[0]}", flush=True)
            log = work / f"step{step}.log"
            run(command, work, env, log)
        # Only the final pass shows references that remain unresolved.
        warnings = re.findall(
            r"LaTeX Warning: (?:Citation|Reference) `[^']+' .*undefined",
            log.read_text(errors="replace"),
        )
        shutil.copyfile(work / "public.pdf", destination)
    return transforms, sorted(set(warnings))


def pdf_facts(path):
    info = subprocess.check_output(["pdfinfo", str(path)], text=True)
    fields = dict(line.split(":", 1) for line in info.splitlines() if ":" in line)
    first = subprocess.check_output(
        ["pdftotext", "-f", "1", "-l", "1", "-layout", str(path), "-"], text=True
    )
    full = subprocess.check_output(["pdftotext", str(path), "-"], text=True)
    return {
        "pages": int(fields["Pages"]),
        "author": fields.get("Author", "").strip(),
        "title": fields.get("Title", "").strip(),
        "titleBlock": first.split("Abstract")[0],
        "text": " ".join(full.split()),
    }


def leaks(path):
    """Scan raw bytes and Flate streams, including escaped and hex PDF strings."""
    data = path.read_bytes()
    chunks = [data]
    for match in re.finditer(rb"\bstream(?:\r\n|\n|\r)", data):
        try:
            # zlib stops at the end of its stream, even if compressed bytes
            # happen to contain the PDF endstream delimiter.
            chunks.append(zlib.decompress(data[match.end() :]))
        except zlib.error:
            pass
    decoded = []
    for chunk in chunks:
        for match in re.finditer(rb"(?<!<)<([\da-fA-F\s]+)>(?!>)", chunk):
            value = re.sub(rb"\s", b"", match.group(1))
            decoded.append(bytes.fromhex((value + b"0" * (len(value) % 2)).decode()))
        chunk = re.sub(rb"\\(?:\r\n|\r|\n)", b"", chunk)
        chunk = re.sub(
            rb"\\([0-7]{1,3})", lambda m: bytes([int(m.group(1), 8) % 256]), chunk
        )
        chunk = re.sub(rb"\\([\\()/])", rb"\1", chunk)
        decoded.append(
            re.sub(rb"#([\da-fA-F]{2})", lambda m: bytes.fromhex(m[1].decode()), chunk)
        )
    chunks += decoded
    return sorted(
        label
        for label, pattern in LEAKS.items()
        if any(
            encoded in chunk
            for encoded in (
                pattern,
                pattern.decode().encode("utf-16-be"),
                pattern.decode().encode("utf-16-le"),
            )
            for chunk in chunks
        )
    )


def contains_statement(text, paragraph, gap=60):
    """True if the paragraph occurs in the text, ignoring spacing and hyphens, with
    at most one inserted run of up to `gap` characters (a page break's running head)."""
    flat = lambda value: re.sub(r"[\s-]", "", value)
    text, paragraph = flat(text), flat(paragraph)
    if paragraph in text:
        return True
    for split in range(1, len(paragraph)):
        head, tail = paragraph[:split], paragraph[split:]
        start = text.find(head)
        while start >= 0:
            end = start + len(head)
            if 0 <= text.find(tail, end) - end <= gap:
                return True
            start = text.find(head, start + 1)
    return False


def verify(slug, path, statement):
    facts = pdf_facts(path)
    paragraph = " ".join(statement.splitlines()[1:])
    problems = []
    found = leaks(path)
    if found:
        problems.append(f"PDF bytes contain {', '.join(found)}")
    if facts["author"] != " and ".join(AUTHORS):
        problems.append(f"PDF author is {facts['author']!r}")
    for author in AUTHORS:
        if author not in facts["titleBlock"]:
            problems.append(f"title block lacks {author}")
    if "Contributions and AI use" not in facts["text"] or not contains_statement(
        facts["text"], paragraph
    ):
        problems.append("contribution statement missing from text")
    named = [name for name in PRODUCTS if name in facts["text"]]
    if named:
        problems.append(f"text names {', '.join(named)}")
    if problems:
        raise RuntimeError(f"{slug}: " + "; ".join(problems))
    return facts


def release_hashes():
    return json.loads(RELEASE_HASHES.read_text())


def original_record(package, frozen, omitted, previous):
    """Describe the archival paper.pdf, present or a declared, hash-bound omission."""
    path = f"{package}/paper.pdf"
    original = ROOT / path
    if original.is_file():
        digest = sha256(original)
        if frozen.get(path) != digest:
            raise ValueError(f"{path} differs from the release record")
        facts = pdf_facts(original)
        return {
            "path": path,
            "sha256": digest,
            "matchesReleaseRecord": True,
            "inExport": True,
            "pages": facts["pages"],
            "author": facts["author"],
        }
    declared = omitted.get(path, {}).get("sha256")
    if not declared or declared != frozen.get(path):
        raise ValueError(f"{path} is missing and not a declared, hash-bound omission")
    # Pages and author were read from the file when it was present; keep them.
    if (
        previous.get("path") != path
        or previous.get("sha256") != declared
        or not isinstance(previous.get("pages"), int)
        or previous["pages"] < 1
        or not isinstance(previous.get("author"), str)
    ):
        raise ValueError(f"{path} is omitted but the manifest has no record of it")
    return {
        "path": path,
        "sha256": declared,
        "matchesReleaseRecord": True,
        "inExport": False,
        "pages": previous["pages"],
        "author": previous["author"],
    }


def build(slugs, check_only):
    statement = STATEMENT.read_text()
    found = papers()
    unknown = set(slugs) - set(found)
    if unknown:
        raise SystemExit(f"Unknown slugs: {', '.join(sorted(unknown))}")
    selected = slugs or list(found)
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"papers": {}}
    frozen = release_hashes()
    omitted = json.loads(EXCLUSIONS.read_text())["omit"]
    changes = json.loads((ROOT / "public-release/release-changes.json").read_text())[
        "changes"
    ]
    expected_sources = {name for name in frozen if name.endswith("/paper.tex")}
    actual_sources = {source.relative_to(ROOT).as_posix() for source in found.values()}
    if not expected_sources or actual_sources != expected_sources:
        raise SystemExit("Paper source inventory differs from the release record")
    if check_only:
        if set(manifest["papers"]) != set(found):
            raise SystemExit(
                "Paper manifest inventory differs from the source inventory"
            )
        if manifest.get("statement", {}).get("sha256") != sha256(STATEMENT):
            raise SystemExit("contributions.tex differs from the manifest")
    statementBefore = manifest.get("statement", {}).get("sha256")
    if slugs and not check_only:
        if manifest.get("statement", {}).get("sha256") != sha256(STATEMENT) or any(
            entry.get("statementSha256") != sha256(STATEMENT)
            for entry in manifest["papers"].values()
        ):
            raise SystemExit(
                "contributions.tex changed since the last full build; rebuild all papers"
            )
    started = time.monotonic()
    failures = []
    for index, slug in enumerate(selected, 1):
        source = found[slug]
        package = source.parent.relative_to(ROOT).as_posix()
        previous = manifest["papers"].get(slug, {})
        target = OUTPUT / f"{slug}.pdf"
        print(f"{index}/{len(selected)} {slug}", flush=True)
        with tempfile.TemporaryDirectory() as scratch:
            built = Path(scratch) / "paper.pdf"
            try:
                source_path = f"{package}/paper.tex"
                expected_source = changes.get(source_path, {}).get(
                    "sha256", frozen.get(source_path)
                )
                if not source.is_file() or expected_source != sha256(source):
                    raise ValueError(
                        f"{package}/paper.tex differs from its declared source record"
                    )
                original = original_record(
                    package, frozen, omitted, previous.get("original", {})
                )
                transforms, warnings = compile_pdf(slug, source, statement, built)
                facts = verify(slug, built, statement)
            except (RuntimeError, ValueError) as error:
                print(f"  FAILED {error}", flush=True)
                failures.append(slug)
                continue
            digest = sha256(built)
            if check_only:
                problems = []
                if previous.get("public", {}).get("sha256") != digest:
                    problems.append("rebuild differs from manifest")
                if not target.is_file() or sha256(target) != digest:
                    problems.append(f"{target.relative_to(ROOT)} differs from rebuild")
                elif leaks(target):
                    problems.append(
                        f"{target.relative_to(ROOT)} contains local metadata"
                    )
                if previous.get("source", {}).get("paper.tex") != sha256(source):
                    problems.append("paper.tex differs from manifest")
                if previous.get("statementSha256") != sha256(STATEMENT):
                    problems.append("paper contribution hash differs from manifest")
                if previous.get("original", {}).get("sha256") != original["sha256"]:
                    problems.append("archival paper.pdf differs from manifest")
                if previous.get("original", {}).get("inExport") != original["inExport"]:
                    problems.append("archival paper.pdf presence flag differs")
                print(f"  {'; '.join(problems) or 'matches manifest'}", flush=True)
                if problems:
                    failures.append(slug)
                continue
            shutil.copyfile(built, target)
        # Keep every superseded public build's hash, so earlier links stay verifiable.
        history = previous.get("supersededPublic", [])
        old = previous.get("public", {})
        if old.get("sha256") and old["sha256"] != digest:
            history = [
                *history,
                {
                    "sha256": old["sha256"],
                    "bytes": old.get("bytes"),
                    "author": old.get("author"),
                    "statementSha256": previous.get("statementSha256", statementBefore),
                    "transforms": previous.get("transforms"),
                },
            ]
        manifest["papers"][slug] = {
            "package": package,
            "source": {
                "paper.tex": sha256(source),
                "matchesReleaseRecord": frozen.get(f"{package}/paper.tex")
                == sha256(source),
            },
            "original": original,
            "statementSha256": sha256(STATEMENT),
            "public": {
                "path": target.relative_to(ROOT).as_posix(),
                "sha256": digest,
                "bytes": target.stat().st_size,
                "pages": facts["pages"],
                "author": facts["author"],
                "title": facts["title"],
            },
            "transforms": transforms,
            "undefinedReferenceWarnings": warnings,
            "supersededPublic": history,
        }
        print(
            f"  wrote {target.relative_to(ROOT)}: {facts['pages']} pages "
            f"(original {original['pages']}), {len(warnings)} undefined-reference warnings; "
            f"{int(time.monotonic() - started)}s elapsed",
            flush=True,
        )
    if not check_only and not failures:
        manifest.update(
            {
                "record": "Public PDFs with Harvey Yorke and Valyu DeepResearch as co-authors, derived from the recorded manuscript sources",
                "supersededPublic": "Hashes of earlier builds of each public PDF, kept as a record; those builds are not in the export",
                "generator": "tools/public_papers.py",
                "statement": {
                    "path": STATEMENT.relative_to(ROOT).as_posix(),
                    "sha256": sha256(STATEMENT),
                },
                "sourceDateEpoch": EPOCH,
                "tex": subprocess.check_output(
                    ["pdflatex", "--version"], text=True
                ).splitlines()[0],
            }
        )
        manifest["papers"] = dict(sorted(manifest["papers"].items()))
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    done = len(selected) - len(failures)
    print(f"{done}/{len(selected)} {'checked' if check_only else 'built'}", flush=True)
    if failures:
        raise SystemExit(f"Failed: {', '.join(failures)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("--only", nargs="+", default=[], metavar="SLUG")
    args = parser.parse_args()
    build(args.only, args.command == "check")


if __name__ == "__main__":
    main()
