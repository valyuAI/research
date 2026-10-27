#!/usr/bin/env python3
"""Compile the determinant certificates sequentially and audit their axioms."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
MODULES = (
    ["MinorCore"]
    + [f"MinorBatch{i:02}" for i in range(1, 22)]
    + ["SplitMinorIdentities", "SplitMinorAudit"]
)
MAX_RSS_BYTES = 6_000_000_000
MIN_FREE_BYTES = 1_000_000_000
MAX_SECONDS = 45 * 60


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def verify_sources():
    manifest = json.loads((ROOT / "source-manifest.json").read_text())
    expected_paths = {f"lean/{name}.lean" for name in MODULES} | {
        "lean/verify_lean_translation.py",
        "minor_dimension_certificates.json",
        "verify_certificates.py",
    }
    paths = [item["path"] for item in manifest["files"]]
    if len(paths) != len(set(paths)) or set(paths) != expected_paths:
        raise ValueError("Source manifest inventory mismatch")
    expected_certificates = [
        f"ValyuResearch.ElasticityMinorCertificates.certificate_{rank}_{target}"
        for rank, targets in [
            (2, [19, 32, 58, 92, 98, 101]),
            (3, [68, 135, 198, 210, 213]),
        ]
        for target in targets
    ]
    if manifest["expected_certificates"] != expected_certificates:
        raise ValueError("Certificate inventory mismatch")
    for item in manifest["files"]:
        path = ROOT / item["path"]
        if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            raise ValueError(f"Source hash mismatch: {item['path']}")
    lean_paths = {path.name for path in (ROOT / "lean").glob("*.lean")}
    if lean_paths != {name + ".lean" for name in MODULES}:
        raise ValueError("Unexpected or missing Lean source module")
    for name in MODULES:
        source = (ROOT / "lean" / f"{name}.lean").read_text()
        if re.search(r"\b(sorry|admit|native_decide|axiom)\b", source):
            raise ValueError(f"Forbidden proof placeholder or declaration in {name}")
    print(
        f"Source hashes verified: {len(paths)} files, eleven certificate targets",
        flush=True,
    )
    return manifest


def resources(process_group, output):
    rows = subprocess.check_output(
        ["ps", "-eo", "pid=,pgid=,rss="], text=True, timeout=10
    )
    rss = [
        int(fields[2]) * 1024
        for row in rows.splitlines()
        if len(fields := row.split()) == 3 and int(fields[1]) == process_group
    ]
    available = None
    meminfo = Path("/proc/meminfo")
    if meminfo.is_file():
        match = re.search(r"^MemAvailable:\s+(\d+) kB$", meminfo.read_text(), re.M)
        if match:
            available = int(match[1]) * 1024
    return {
        "processes": len(rss),
        "maximum_process_rss_bytes": max(rss, default=0),
        "process_group_rss_bytes": sum(rss),
        "free_disk_bytes": shutil.disk_usage(output).free,
        "host_memory_available_bytes": available,
    }


def stop_process(process):
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()


def latest_line(path):
    with path.open("rb") as stream:
        stream.seek(max(0, path.stat().st_size - 4096))
        lines = stream.read().decode(errors="replace").splitlines()
    return lines[-1] if lines else "No compiler output yet"


def run_step(name, command, project, output, environment, deadline):
    diagnostics = output / "diagnostics"
    log_path = diagnostics / f"{name}.log"
    started = time.monotonic()
    record = {"step": name, "command": command, "status": "RUNNING"}
    print(f"START {name}", flush=True)
    process = None
    try:
        with log_path.open("w") as log:
            process = subprocess.Popen(
                command,
                cwd=project,
                env=environment,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            next_progress = 0
            while process.poll() is None:
                snapshot = resources(process.pid, output)
                now = time.monotonic()
                snapshot.update(
                    {"step": name, "elapsed_seconds": round(now - started, 2)}
                )
                if snapshot["maximum_process_rss_bytes"] > MAX_RSS_BYTES:
                    raise RuntimeError(
                        f"Resource limit: {name} exceeded 6 GB process RSS"
                    )
                if snapshot["free_disk_bytes"] < MIN_FREE_BYTES:
                    raise RuntimeError(
                        f"Resource limit: {name} has less than 1 GB free disk"
                    )
                if now > deadline:
                    raise RuntimeError(
                        "Resource limit: the 45-minute compilation budget expired"
                    )
                if now >= next_progress:
                    snapshot["latest_compiler_line"] = latest_line(log_path)
                    print(json.dumps(snapshot), flush=True)
                    with (diagnostics / "resources.jsonl").open("a") as stream:
                        stream.write(json.dumps(snapshot) + "\n")
                    next_progress = now + 30
                time.sleep(2)
            record["exit_code"] = process.returncode
            if process.returncode:
                raise RuntimeError(
                    f"{name} exited {process.returncode}; see {log_path.name}"
                )
            record["status"] = "PASS"
    except BaseException as error:
        record.update({"status": "FAIL", "error": str(error)})
        if process is not None:
            stop_process(process)
            record["exit_code"] = process.returncode
        print(f"FAIL {name}: {error}", flush=True)
        print(
            latest_line(log_path) if log_path.exists() else "No log created", flush=True
        )
        raise
    finally:
        record["elapsed_seconds"] = round(time.monotonic() - started, 2)
        write_json(diagnostics / f"{name}.json", record)
    print(f"PASS {name}: {record['elapsed_seconds']} seconds", flush=True)
    return record


def audit_inventory(path, expected):
    text = path.read_text()
    names = re.findall(r"^PASS ([^\s:]+):", text, re.M)
    counts = re.findall(
        r"Audited all (\d+) module theorems and all 11 expected certificates\.", text
    )
    if len(counts) != 1 or len(names) != int(counts[0]) or len(names) < 300:
        raise ValueError("Completed axiom audit inventory is missing or inconsistent")
    if len(set(names)) != len(names) or not set(expected).issubset(names):
        raise ValueError("Axiom audit omitted or duplicated certificate declarations")
    return {
        "owned_theorems": len(names),
        "certificate_theorems": expected,
        "allowed_axioms": ["propext", "Classical.choice", "Quot.sound"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify-sources-only", action="store_true")
    args = parser.parse_args()
    manifest = verify_sources()
    translation = [
        sys.executable,
        "-B",
        "-O",
        str(ROOT / "lean/verify_lean_translation.py"),
    ]
    if args.verify_sources_only:
        subprocess.run(translation, check=True)
        print(
            "SOURCE_PREFLIGHT_PASS: no Lean compilation or proof acceptance claimed",
            flush=True,
        )
        return
    if args.project is None or args.output is None:
        parser.error("--project and --output are required for compilation")
    project, output = args.project.resolve(), args.output.resolve()
    if (
        output == ROOT
        or ROOT in output.parents
        or project == output
        or project in output.parents
    ):
        parser.error(
            "Compilation output must be outside the source package and Lean project"
        )
    if (project / "lean-toolchain").read_text().strip() != "leanprover/lean4:v4.35.0":
        raise ValueError(
            "The replay requires the repository's pinned Lean 4.35.0 toolchain"
        )
    diagnostics, compiled = output / "diagnostics", output / "compiled"
    diagnostics.mkdir(parents=True, exist_ok=True)
    compiled.mkdir(parents=True, exist_ok=True)
    if any(compiled.iterdir()):
        raise ValueError(
            "Use a fresh output directory; stale compiled modules are not accepted"
        )
    environment = dict(os.environ, LEAN_NUM_THREADS="2", LEAN_ABORT_ON_PANIC="1")
    environment["LEAN_PATH"] = str(compiled) + (
        os.pathsep + environment["LEAN_PATH"] if environment.get("LEAN_PATH") else ""
    )
    result = {
        "status": "RUNNING",
        "scope": "Determinant identities and owned-theorem axiom audit",
        "independent_checker_replay": False,
        "full_elasticity_theorem_formalized": False,
        "manifest_sha256": digest(ROOT / "source-manifest.json"),
        "modules": [],
    }
    deadline = time.monotonic() + MAX_SECONDS
    try:
        if shutil.disk_usage(output).free < MIN_FREE_BYTES:
            raise RuntimeError(
                "Resource limit: less than 1 GB free disk before compilation"
            )
        run_step(
            "translation",
            translation + [str(diagnostics / "translation.json")],
            project,
            output,
            environment,
            deadline,
        )
        for index, name in enumerate(MODULES, 1):
            print(f"MODULE {index}/{len(MODULES)}: {name}", flush=True)
            source, artifact = (
                ROOT / "lean" / f"{name}.lean",
                compiled / f"{name}.olean",
            )
            command = [
                "lake",
                "env",
                "lean",
                "-R",
                str(ROOT / "lean"),
                "-o",
                str(artifact),
                str(source),
            ]
            record = run_step(name, command, project, output, environment, deadline)
            record.update(
                {
                    "source_sha256": digest(source),
                    "artifact_sha256": digest(artifact),
                    "artifact_bytes": artifact.stat().st_size,
                }
            )
            result["modules"].append(record)
            write_json(diagnostics / "result.json", result)
        result["audit"] = audit_inventory(
            diagnostics / "SplitMinorAudit.log", manifest["expected_certificates"]
        )
        result["status"] = "COMPILATION_AND_AXIOM_AUDIT_PASS"
        print(json.dumps(result["audit"], indent=2), flush=True)
        print(result["status"], flush=True)
    except BaseException as error:
        result.update({"status": "FAIL", "error": str(error)})
        raise
    finally:
        write_json(diagnostics / "result.json", result)


if __name__ == "__main__":

    def interrupted(signum, _frame):
        raise RuntimeError(f"Interrupted by signal {signum}")

    signal.signal(signal.SIGTERM, interrupted)
    main()
