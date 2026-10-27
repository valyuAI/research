"""Mutation tests: the checker must reject corrupted or overstated certificates.

usage: python3 negative_checks.py      (from the verification directory or anywhere)
Each of the ten cases writes a modified copy of a shipped certificate to a temporary file
and requires check_cert.py to exit without printing VERIFIED.
"""
import gzip
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "py", "check_cert.py")


def load(name):
    with gzip.open(os.path.join(HERE, "certs", name), "rt") as fh:
        return fh.read().splitlines()


def verdict(lines):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        fh.write("\n".join(lines) + "\n")
        path = fh.name
    try:
        out = subprocess.run([sys.executable, CHECK, path], capture_output=True, text=True)
    finally:
        os.unlink(path)
    text = (out.stdout + out.stderr).strip().splitlines()
    return text[-1] if text else ""


def header_with(lines, key, value):
    parts = [p if not p.startswith(key + "=") else f"{key}={value}" for p in lines[0].split()]
    return [" ".join(parts)] + lines[1:]


def replace_move(lines, index, new_move):
    m, b, rel, _ = lines[index].split()
    out = list(lines)
    out[index] = f"{m} {b} {rel} {new_move}"
    return out


def main():
    blue_l6 = load("n5L6_12.txt.gz")
    red_l5 = load("n5L5_12_red.txt.gz")
    blue_d7 = load("n5D7_12.txt.gz")
    red_d6 = load("n5D6_12_red.txt.gz")
    m, b, rel, mv = blue_l6[1].split()
    occupied = (int(b, 16) & -int(b, 16)).bit_length() - 1  # a Blue cell in the key
    cases = [
        ("Blue Hex(5,6) certificate relabelled as Hex(5,5)", header_with(blue_l6, "bound", 5)),
        ("Blue Hex_7(5) certificate relabelled as Hex_6(5)", header_with(blue_d7, "bound", 6)),
        ("Red Hex(5,5) certificate relabelled as Hex(5,6)", header_with(red_l5, "bound", 6)),
        ("Red Hex_6(5) certificate relabelled as Hex_7(5)", header_with(red_d6, "bound", 7)),
        ("Blue certificate with its first entry deleted", [blue_l6[0]] + blue_l6[2:]),
        ("Blue certificate with a move onto a Blue stone", replace_move(blue_l6, 1, occupied)),
        ("Blue certificate with a move off the board", replace_move(blue_l6, 1, 25)),
        ("Red certificate with its first entry deleted", [red_l5[0]] + red_l5[2:]),
        ("Blue certificate claimed for another opening", header_with(blue_l6, "first", 0)),
        ("Empty certificate on a 1x1 board", ["# n=1 mode=L bound=0 first=0"]),
    ]
    failures = 0
    for name, lines in cases:
        v = verdict(lines)
        ok = not v.startswith("VERIFIED")
        failures += not ok
        print(f"{'rejected' if ok else 'ACCEPTED (bad)'}: {name}: {v[:100]}")
    if failures:
        print(f"NEGATIVE CHECKS FAILED: {failures} corrupted certificates accepted")
        sys.exit(1)
    print(f"ALL {len(cases)} CORRUPTED CERTIFICATES REJECTED")


if __name__ == "__main__":
    main()
