"""Render, check and export the public presentation layer of the collection.

docs/collection.json defines the retained findings and catalog/findings.json adds
plain-language summaries and formal links. Research packages are never modified.

  python3 tools/catalog.py render              # rewrite FINDINGS.md
  python3 tools/catalog.py check               # links, files, release and paper hashes
  python3 tools/catalog.py export --out DIR    # paper/video bundle outside Git

Release files may differ from docs/artifact-hashes.json only as declared, with the
exact current hash, in public-release/release-changes.json, and may be absent only
if listed in public-release/export-exclusions.json.
"""

import argparse
import datetime
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
COLLECTION = ROOT / "docs/collection.json"
CATALOG = ROOT / "catalog/findings.json"
FINDINGS = ROOT / "FINDINGS.md"
PAPERS = "public-release/papers"
PRESENTATION = [
    "README.md",
    "FINDINGS.md",
    "CONTRIBUTING.md",
    "docs/README.md",
    "docs/collection.md",
    "docs/significance.md",
]
GENERATOR = "tools/catalog.py"

KINDS = {
    "new_result_candidate": "New-result candidate",
    "new_proof_and_correction": "New proof of a known theorem, with a correction",
    "independent_verification": "Independent verification; no priority claim",
}
DISCIPLINES = {
    "maths": "Mathematics",
    "physics": "Physics",
    "chemistry": "Chemistry",
    "economics": "Economics",
}
# Text that must never reach a public surface: dashes we avoid, local paths and
# signed or authenticated URLs.
FORBIDDEN = {
    "em dash": "\u2014",
    "local home path": "/Users/",
    "local home path (Linux)": "/home/",
    "signed URL": "X-Amz-",
    "URL signature": "Signature=",
    "access token": "access_token=",
}
STATUS_NOTE = (
    "These are research drafts. None has been externally peer reviewed. Novelty is "
    "judged against recorded literature searches, which cannot establish priority. "
    "Each entry states what is proved, how it was checked and what remains open."
)


def loadFindings():
    collection = json.loads(COLLECTION.read_text())["entries"]
    catalog = json.loads(CATALOG.read_text())
    overlay = {item["id"]: item for item in catalog["findings"]}
    ids = [entry["id"] for entry in collection]
    if sorted(ids) != sorted(overlay) or len(set(ids)) != len(ids):
        raise SystemExit(
            f"catalog/findings.json ids differ from docs/collection.json: "
            f"missing {sorted(set(ids) - set(overlay))}, extra {sorted(set(overlay) - set(ids))}"
        )
    findings = []
    for entry in collection:
        path = entry["path"]
        parts = path.split("/")
        package = ROOT / path
        readiness = next(
            (
                name
                for name in ["readiness.md", "READINESS.md"]
                if exactPath(package / name)
            ),
            None,
        )
        checks = "verification/README.md"
        if not exactPath(package / checks):
            checks = "verification/"
        findings.append(
            {
                **entry,
                **overlay[entry["id"]],
                "slug": parts[-1],
                "discipline": parts[0],
                "field": " / ".join(label(part) for part in parts[1:-1]),
                "readiness": readiness,
                "checks": checks,
            }
        )
    # Group by discipline, keeping collection order within each.
    findings.sort(key=lambda finding: list(DISCIPLINES).index(finding["discipline"]))
    slugs = [finding["slug"] for finding in findings]
    if len(set(slugs)) != len(slugs):
        raise SystemExit("Finding folder names must be unique for export")
    return catalog, findings


def label(part):
    return part.replace("-", " ").capitalize()


def anchor(heading):
    """GitHub's heading anchor for plain-text headings."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def summaryLine(findings):
    counts = {kind: 0 for kind in KINDS}
    for finding in findings:
        counts[finding["kind"]] += 1
    return (
        f"{len(findings)} findings: {counts['new_result_candidate']} new-result candidates, "
        f"{counts['new_proof_and_correction']} new proof of a known theorem and "
        f"{counts['independent_verification']} independent verification notes. "
        f"Every finding has a paper and a narrated video."
    )


def formalLine(finding):
    if not finding["formal"]:
        return "No Lean formalization; the evidence is the written proof and the exact checks."
    items = []
    for item in finding["formal"]:
        name = Path(item["path"].rstrip("/")).name
        items.append(
            f"[{name}]({item['path']}) ({item['scope'][0].lower()}{item['scope'][1:]})"
        )
    return "; ".join(items) + ". See [formal coverage](docs/formal-coverage.md)."


def render(findings):
    lines = [
        "# Findings",
        "",
        "<!-- Generated by tools/catalog.py from docs/collection.json and catalog/findings.json. Do not edit by hand. -->",
        "",
        summaryLine(findings),
        "",
        f"> {STATUS_NOTE}",
        "",
        "| Finding | Field | Status | Paper | Video |",
        "|---|---|---|---|---|",
    ]
    for finding in findings:
        lines.append(
            f"| [{finding['title']}](#{anchor(finding['title'])}) "
            f"| {DISCIPLINES[finding['discipline']]} | {KINDS[finding['kind']]} "
            f"| [PDF]({PAPERS}/{finding['slug']}.pdf) | [MP4]({finding['path']}/video/video.mp4) |"
        )
    for discipline, name in DISCIPLINES.items():
        group = [finding for finding in findings if finding["discipline"] == discipline]
        if not group:
            continue
        lines += ["", f"## {name}"]
        for finding in group:
            path = finding["path"]
            checks = f"[Verification]({path}/{finding['checks']})"
            if finding["readiness"]:
                checks += f" · [Review state]({path}/{finding['readiness']})"
            lines += [
                "",
                f"### {finding['title']}",
                "",
                f'<a href="{path}/video/video.mp4"><img src="{path}/video/poster.png" width="360" alt="Video still: {html.escape(finding["title"])}"></a>',
                "",
                f"**{KINDS[finding['kind']]}** · {finding['field']}",
                "",
                finding["plain"],
                "",
                f"- **Result.** {finding['result']}",
                f"- **Boundary.** {finding['limits']}",
                f"- **Paper:** [PDF]({PAPERS}/{finding['slug']}.pdf) · [LaTeX]({path}/paper.tex)",
                f"- **Video:** [MP4]({path}/video/video.mp4) · [Subtitles]({path}/video/subtitles.srt) · [Script and QA]({path}/video/README.md)",
                f"- **Checks:** {checks}",
                f"- **Formal:** {formalLine(finding)}",
                f"- **Package:** [{path}]({path}/)",
            ]
    return "\n".join(lines) + "\n"


def exactPath(target):
    """Return True only if every path component exists with exact spelling."""
    try:
        relative = target.resolve().relative_to(ROOT)
    except ValueError:
        return target.exists()
    current = ROOT
    for part in relative.parts:
        if not current.is_dir() or part not in {
            child.name for child in current.iterdir()
        }:
            return False
        current = current / part
    return True


LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|(?:src|href)=\"([^\"]+)\"")


def brokenLinks(document):
    text = document.read_text()
    broken = []
    for match in LINK.finditer(text):
        target = match.group(1) or match.group(2)
        if re.match(r"[a-z]+:", target):
            continue
        location, _, fragment = unquote(target).partition("#")
        resolved = (document.parent / location) if location else document
        if not exactPath(resolved):
            broken.append(target)
        elif fragment and resolved.suffix == ".md":
            headings = re.findall(r"^#+\s+(.+)$", resolved.read_text(), re.MULTILINE)
            if fragment not in {anchor(heading) for heading in headings}:
                broken.append(target)
    return broken


def check(args):
    catalog, findings = loadFindings()
    errors = []
    required = [
        "README.md",
        "paper.tex",
        "video/video.mp4",
        "video/poster.png",
        "video/subtitles.srt",
        "video/README.md",
    ]
    for finding in findings:
        package = ROOT / finding["path"]
        for name in required + [finding["checks"]]:
            if not exactPath(package / name):
                errors.append(f"{finding['id']}: missing {finding['path']}/{name}")
        for item in finding["formal"]:
            if not exactPath(ROOT / item["path"]):
                errors.append(f"{finding['id']}: missing formal source {item['path']}")
        if not finding["plain"].strip():
            errors.append(f"{finding['id']}: empty plain-language summary")
    print(f"findings: {len(findings)} checked for paper, video, subtitles and checks")

    if not FINDINGS.is_file() or FINDINGS.read_text() != render(findings):
        errors.append("FINDINGS.md is stale; run python3 tools/catalog.py render")

    for name in PRESENTATION:
        document = ROOT / name
        if not document.is_file():
            errors.append(f"missing {name}")
            continue
        errors += [f"{name}: broken link {target}" for target in brokenLinks(document)]
        text = document.read_text()
        errors += [
            f"{name}: contains {what}"
            for what, token in FORBIDDEN.items()
            if token in text
        ]
    print(f"presentation: {len(PRESENTATION)} documents checked for links and hygiene")

    errors += checkRelease(catalog["releaseSnapshot"])
    errors += checkPapers(catalog["releaseSnapshot"], findings)
    for error in errors:
        print(f"ERROR {error}")
    print("check passed" if not errors else f"check failed: {len(errors)} errors")
    return 1 if errors else 0


def loadJson(path):
    return json.loads((ROOT / path).read_text())


def checkRelease(snapshot):
    """Every file in the release inventory must be byte-identical, unless it is a
    declared change with exactly the recorded current hash, or a declared export
    omission that is absent. Anything else fails."""
    manifest = loadJson(snapshot["manifest"])
    changes = loadJson(snapshot["changes"])["changes"]
    omit = loadJson(snapshot["exclusions"])["omit"]
    errors = [
        f"declared change {path} is not in the release manifest"
        for path in set(changes) - set(manifest)
    ]
    errors += [
        f"declared omission {path} is not in the release manifest"
        for path in set(omit) - set(manifest)
    ]
    errors += [
        f"declared omission {path} has a hash other than the release record"
        for path, entry in omit.items()
        if path in manifest and entry["sha256"] != manifest[path]
    ]
    errors += [
        f"{path} is declared both changed and omitted"
        for path in set(changes) & set(omit)
    ]
    counts = {"identical": 0, "changed": 0, "omitted": 0}
    for index, (path, digest) in enumerate(sorted(manifest.items()), 1):
        target = ROOT / path
        isLinked = linked(target)
        if path in omit and (target.exists() or isLinked):
            errors.append(f"excluded file is present in public release: {path}")
        if isLinked or not target.is_file():
            if path in omit and not isLinked and not target.exists():
                counts["omitted"] += 1
            else:
                errors.append(f"release file missing: {path}")
            continue
        current = sha256(target)
        if path in changes:
            if current == digest:
                errors.append(
                    f"declared change is stale (file matches the release record): {path}"
                )
            elif current != changes[path]["sha256"]:
                errors.append(
                    f"release file differs from its declared change: {path} is {current}"
                )
            else:
                counts["changed"] += 1
        elif current != digest:
            errors.append(f"release file changed: {path} is {current}")
        else:
            counts["identical"] += 1
        if index % 1000 == 0:
            print(f"  hashed {index}/{len(manifest)}", flush=True)
    print(
        f"release: {len(manifest)} files from {snapshot['commit'][:12]}; {counts['identical']} identical, "
        f"{counts['changed']} declared changes at their recorded hash, {counts['omitted']} declared omissions absent"
    )
    return errors


def checkPapers(snapshot, findings):
    """Each finding's public PDF must match the public-paper manifest, which must in
    turn match the current paper source, the archival PDF and the statement."""
    record = loadJson(snapshot["publicPapers"])
    omissions = loadJson(snapshot["exclusions"])["omit"]
    release = loadJson(snapshot["manifest"])
    papers = record["papers"]
    errors = []
    statement = record["statement"]
    statementDigest = sha256(ROOT / statement["path"])
    if statementDigest != statement["sha256"]:
        errors.append(
            f"{statement['path']} differs from {snapshot['publicPapers']}; rebuild the public papers"
        )
    for finding in findings:
        entry = papers.get(finding["slug"])
        if not entry or entry["package"] != finding["path"]:
            errors.append(f"{finding['id']}: no public paper for {finding['path']}")
            continue
        public = ROOT / entry["public"]["path"]
        pairs = [
            (public, entry["public"]["sha256"]),
            (ROOT / finding["path"] / "paper.tex", entry["source"]["paper.tex"]),
        ]
        original = entry["original"]
        originalPath = ROOT / original["path"]
        if original.get("inExport") != originalPath.is_file():
            errors.append(f"{finding['id']}: archival PDF presence flag is stale")
        if entry.get("statementSha256") != statementDigest:
            errors.append(f"{finding['id']}: paper contribution hash is stale")
        if originalPath.exists() or linked(originalPath):
            pairs.append((originalPath, original["sha256"]))
        elif (
            omissions.get(original["path"], {}).get("sha256") != original["sha256"]
            or release.get(original["path"]) != original["sha256"]
        ):
            errors.append(f"{finding['id']}: archival PDF omission is not hash-bound")
        for path, digest in pairs:
            if not path.is_file() or path.is_symlink() or sha256(path) != digest:
                errors.append(
                    f"{finding['id']}: {path.relative_to(ROOT)} does not match {snapshot['publicPapers']}"
                )
        if entry["public"]["path"] != f"{PAPERS}/{finding['slug']}.pdf":
            errors.append(
                f"{finding['id']}: unexpected public paper path {entry['public']['path']}"
            )
    extra = set(papers) - {finding["slug"] for finding in findings}
    errors += [f"public paper {slug} is not a finding" for slug in sorted(extra)]
    print(
        f"public papers: {len(findings)} checked against source, archival PDF and manifest hashes"
    )
    return errors


def git(*command):
    return subprocess.run(
        ["git", *command], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def insideGit(path):
    return any((parent / ".git").exists() for parent in [path, *path.parents])


def linked(path):
    """True if the path or any parent inside the checkout is a symlink."""
    return any(
        part.is_symlink() for part in [path, *path.parents] if ROOT in part.parents
    )


def place(source, destination):
    # APFS copy-on-write clone where available, otherwise an ordinary copy.
    if subprocess.run(
        ["cp", "-c", str(source), str(destination)], capture_output=True
    ).returncode:
        shutil.copyfile(source, destination)


def exportSources(catalog, finding, tracked):
    """The allowlist for one finding: its public paper, verified against the
    public-paper manifest, and tracked media, verified against the release record."""
    snapshot = catalog["releaseSnapshot"]
    release = loadJson(snapshot["manifest"])
    paper = loadJson(snapshot["publicPapers"])["papers"][finding["slug"]]["public"]
    package = finding["path"]
    sources = {"paper.pdf": (paper["path"], paper["sha256"], snapshot["publicPapers"])}
    if finding["slug"] == "marked-polyform-heesch-numbers":
        notice = f"{package}/verification/basic/NOTICE.md"
        if notice not in tracked:
            raise SystemExit(f"{notice} is not tracked by Git")
        sources["NOTICE.md"] = (notice, sha256(ROOT / notice), "sourceCommit")
    media = {
        "video.mp4": "video/video.mp4",
        "poster.png": "video/poster.png",
        "subtitles.srt": "video/subtitles.srt",
        "subtitles.vtt": "video/subtitles.vtt",
    }
    for name, relative in media.items():
        path = f"{package}/{relative}"
        if name == "subtitles.vtt" and path not in tracked:
            continue
        if path not in tracked:
            raise SystemExit(f"{path} is not tracked by Git")
        sources[name] = (path, release.get(path), snapshot["manifest"])
    for name, (path, digest, record) in sources.items():
        source = ROOT / path
        if not digest:
            raise SystemExit(f"{path} has no hash in {record}")
        if "private-cache" in path or linked(source):
            raise SystemExit(f"{path} is a symlink or private cache")
    return sources


def exportReadme(finding, files, repoUrl):
    source = f"{repoUrl.rstrip('/')}/{finding['path']}" if repoUrl else finding["path"]
    sourceReference = f"[full package]({source})" if repoUrl else f"`{source}`"
    lines = [
        f"# {finding['title']}",
        "",
        f"**{KINDS[finding['kind']]}** · {DISCIPLINES[finding['discipline']]} / {finding['field']}",
        "",
        finding["plain"],
        "",
        f"- **Result.** {finding['result']}",
        f"- **Boundary.** {finding['limits']}",
        "- **Formal.** "
        + (
            "; ".join(f"{item['path']} ({item['scope']})" for item in finding["formal"])
            if finding["formal"]
            else "No Lean formalization; written proof and exact checks."
        ),
        "",
        "Files: " + ", ".join(f"[{name}]({name})" for name in files),
        "",
        "The paper lists Harvey Yorke and Valyu DeepResearch as co-authors. The LaTeX source, "
        f"proofs and verification are in the full source collection: {sourceReference}.",
        "",
        "Papers and original media: [CC BY 4.0](../LICENSES/CC-BY-4.0.txt), subject to "
        "the exceptions in [LICENSE](../LICENSE). Retain [NOTICE](../NOTICE) when reusing the material.",
        "",
        f"> {STATUS_NOTE}",
    ]
    if finding["slug"] == "marked-polyform-heesch-numbers":
        lines += [
            "",
            "The complete video and adapted patch illustrations are licensed under "
            "[CC BY-SA 4.0](../LICENSES/CC-BY-SA-4.0.txt). They use Bojan Bašić's "
            "Heesch-number-6 patch, recovered from the Wikimedia Commons illustration "
            "and snapped to a trihexagonal grid. Preserve the attribution and change "
            "description in [NOTICE.md](NOTICE.md). The paper remains CC BY 4.0.",
        ]
    return "\n".join(lines) + "\n"


def exportIndex(findings, repoUrl):
    cards = []
    for finding in findings:
        slug = html.escape(finding["slug"])
        cards.append(f"""<article>
  <a href="{slug}/video.mp4"><img src="{slug}/poster.png" alt="Video still: {html.escape(finding['title'])}" loading="lazy"></a>
  <p class="kind">{html.escape(KINDS[finding['kind']])} · {html.escape(DISCIPLINES[finding['discipline']])}</p>
  <h2>{html.escape(finding['title'])}</h2>
  <p>{html.escape(finding['plain'])}</p>
  <p class="limits"><strong>Boundary.</strong> {html.escape(finding['limits'])}</p>
  <p class="links"><a href="{slug}/paper.pdf">Paper (PDF)</a> <a href="{slug}/video.mp4">Video</a> <a href="{slug}/README.md">Details</a></p>
</article>""")
    source = (
        f' Sources, proofs and verification: <a href="{html.escape(repoUrl)}">repository</a>.'
        if repoUrl
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Valyu Research findings</title>
<style>
  body {{ margin: 0 auto; max-width: 64rem; padding: 3rem 1.5rem; font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; color: #1d1d1f; background: #fff; }}
  header p {{ max-width: 44rem; color: #444; }}
  main {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr)); gap: 2.5rem 2rem; margin-top: 2.5rem; }}
  article img {{ width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border: 1px solid #e5e5e5; }}
  h1 {{ font-size: 1.9rem; margin: 0 0 0.75rem; }}
  h2 {{ font-size: 1.1rem; margin: 0.25rem 0 0.5rem; }}
  .kind {{ margin: 0.75rem 0 0; font-size: 0.8rem; color: #666; }}
  .limits {{ font-size: 0.9rem; color: #555; }}
  .links a {{ margin-right: 1rem; }}
  a {{ color: #0b5cad; }}
</style>
</head>
<body>
<header>
<h1>Valyu Research findings</h1>
<p>{html.escape(summaryLine(findings))}</p>
<p>{html.escape(STATUS_NOTE)}{source}</p>
</header>
<main>
{chr(10).join(cards)}
</main>
</body>
</html>
"""


def export(args):
    """Build the bundle in a sibling staging folder, verify every file, then swap it
    in. A previous export is moved aside, never deleted."""
    catalog, findings = loadFindings()
    out = Path(args.out).expanduser().resolve()
    if insideGit(out):
        raise SystemExit(f"Refusing to export inside a Git checkout: {out}")
    if out.exists() or out.is_symlink():
        marker = out / "manifest.json"
        isExport = (
            out.is_dir()
            and not out.is_symlink()
            and marker.is_file()
            and json.loads(marker.read_text()).get("generator") == GENERATOR
        )
        if not (args.replace and isExport):
            raise SystemExit(
                f"{out} exists; pass --replace to move a previous export aside"
            )
    head = git("rev-parse", "HEAD").strip()
    dirty = bool(git("status", "--porcelain").strip())
    if dirty and not args.allow_dirty:
        raise SystemExit(
            "Source tree has uncommitted changes; commit first or pass --allow-dirty"
        )
    tracked = set(git("ls-files", "-z").split("\0"))
    out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{out.name}.staging-", dir=out.parent))
    try:
        manifest = writeExport(
            catalog, findings, tracked, staging, head, dirty, args.repo_url
        )
        verifyExport(staging, manifest)
    except BaseException:
        shutil.rmtree(staging)
        raise
    previous = None
    if out.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        previous = out.with_name(f"{out.name}.previous-{stamp}")
        out.rename(previous)
    staging.rename(out)
    total = sum(f["bytes"] for entry in manifest["findings"] for f in entry["files"])
    print(
        f"exported {len(findings)} findings, {total / 1e6:.0f} MB, every file hash-verified, to {out}"
    )
    if previous:
        print(f"previous export kept at {previous}")
    if dirty:
        print(
            "note: source tree has uncommitted changes; sourceCommit is the base commit and file hashes bind the content"
        )
    return 0


def writeExport(catalog, findings, tracked, out, head, dirty, repoUrl):
    snapshot = catalog["releaseSnapshot"]
    notices = {}
    for path in [
        "LICENSE",
        "NOTICE",
        "LICENSES/Apache-2.0.txt",
        "LICENSES/CC-BY-4.0.txt",
        "LICENSES/CC-BY-SA-4.0.txt",
        "public-release/THIRD_PARTY.md",
        "public-release/export-exclusions.json",
    ]:
        source = ROOT / path
        if path not in tracked or linked(source):
            raise SystemExit(f"Notice is untracked or a symlink: {path}")
        destination = out / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        place(source, destination)
        notices[path] = sha256(source)
    entries = []
    for index, finding in enumerate(findings, 1):
        folder = out / finding["slug"]
        folder.mkdir()
        files = []
        for name, (path, digest, record) in exportSources(
            catalog, finding, tracked
        ).items():
            source = ROOT / path
            if sha256(source) != digest:
                raise SystemExit(f"{path} differs from {record}")
            place(source, folder / name)
            files.append(
                {
                    "name": name,
                    "source": path,
                    "record": record,
                    "bytes": source.stat().st_size,
                    "sha256": digest,
                }
            )
        (folder / "README.md").write_text(
            exportReadme(finding, [f["name"] for f in files], repoUrl)
        )
        entries.append(
            {
                "id": finding["id"],
                "slug": finding["slug"],
                "title": finding["title"],
                "kind": finding["kind"],
                "discipline": finding["discipline"],
                "field": finding["field"],
                "plain": finding["plain"],
                "result": finding["result"],
                "limits": finding["limits"],
                "formal": finding["formal"],
                "source": finding["path"],
                "files": files,
            }
        )
        print(f"  {index}/{len(findings)} {finding['slug']}", flush=True)
    (out / "index.html").write_text(exportIndex(findings, repoUrl))
    manifest = {
        "generator": GENERATOR,
        "sourceCommit": head,
        "sourceTreeDirty": dirty,
        "releaseSnapshotCommit": snapshot["commit"],
        "records": {
            path: sha256(ROOT / path)
            for path in [
                snapshot["manifest"],
                snapshot["changes"],
                snapshot["exclusions"],
                snapshot["publicPapers"],
            ]
        },
        "statusNote": STATUS_NOTE,
        "notices": notices,
        "findings": entries,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    )
    return manifest


def verifyExport(out, manifest):
    """The bundle holds exactly the manifest's files plus generated text, no links,
    and no forbidden text."""
    expected = {"index.html", "manifest.json"}
    for path, digest in manifest["notices"].items():
        expected.add(path)
        if sha256(out / path) != digest:
            raise SystemExit(f"Exported notice differs from source: {path}")
    for entry in manifest["findings"]:
        expected.add(f"{entry['slug']}/README.md")
        for item in entry["files"]:
            relative = f"{entry['slug']}/{item['name']}"
            expected.add(relative)
            if sha256(out / relative) != item["sha256"]:
                raise SystemExit(f"Exported {relative} differs from {item['source']}")
    found = {
        path.relative_to(out).as_posix()
        for path in out.rglob("*")
        if not path.is_dir() or path.is_symlink()
    }
    links = [path for path in out.rglob("*") if path.is_symlink()]
    if found != expected or links:
        raise SystemExit(
            f"Export file set is wrong: extra {sorted(found - expected)}, missing {sorted(expected - found)}, links {links}"
        )
    leaks = [
        f"{path.relative_to(out)}: {what}"
        for path in sorted(out.rglob("*"))
        if path.suffix in (".md", ".html", ".json", ".srt", ".vtt")
        for what, token in FORBIDDEN.items()
        if token in path.read_text()
    ]
    if leaks:
        raise SystemExit("Export contains forbidden text:\n" + "\n".join(leaks))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("render", help="rewrite FINDINGS.md")
    commands.add_parser(
        "check",
        help="validate the presentation layer, public papers and release inventory",
    )
    exporter = commands.add_parser(
        "export", help="write a paper and video bundle outside Git"
    )
    exporter.add_argument(
        "--out", required=True, help="destination directory outside any Git checkout"
    )
    exporter.add_argument(
        "--allow-dirty",
        action="store_true",
        help="export from uncommitted changes; every file is still hash-verified",
    )
    exporter.add_argument(
        "--repo-url", default="", help="public repository URL for source links"
    )
    exporter.add_argument(
        "--replace",
        action="store_true",
        help="swap in a new export; the previous one is moved aside, not deleted",
    )
    args = parser.parse_args()
    if args.command == "render":
        _, findings = loadFindings()
        FINDINGS.write_text(render(findings))
        print(f"wrote FINDINGS.md ({len(findings)} findings)")
        return 0
    return check(args) if args.command == "check" else export(args)


if __name__ == "__main__":
    sys.exit(main())
