# Optional SAT proof replay

The primary bundled lower-bound proof is the exhaustive subspace search. This is an additional check using a different encoding: a length-eight decomposition would satisfy 64 coefficient equations over F2. AND and XOR gates encode these equations. Sorting the eight triples of coefficient vectors lexicographically is sound because the summands may be permuted freely. Zero summands allow decompositions of length less than eight.

`satenc.py` generates the formula using:

```sh
python3 satenc.py 21 8 replay.cnf --lex
```

On 26 October 2026 the regenerated formula was byte-identical to both the solved input and `certificates/sat_A2_rank8.cnf`: 1,268 variables, 4,273 clauses. The hashes and sizes are in `certificates/sat_A2_rank8.manifest.json`.

The archived run used CaDiCaL 3.0.1 and returned `UNSATISFIABLE` (exit 20). Its 628,254,455-byte DRAT proof was checked by `drat-trim`, which reported `s VERIFIED`, with 2,415,525 of 4,105,809 lemmas in the proof core. The original checker output is `logs/drat_A2_rank8.txt`. The proof file is retained at the archive path in the manifest and is not bundled here. Thus the log is a record of a completed check, not a substitute for the proof file.

With `cadical` and `drat-trim` installed, a fresh optional replay is:

```sh
python3 satenc.py 21 8 replay.cnf --lex
cadical replay.cnf replay.drat > replay-solver.log
# CaDiCaL's expected successful UNSAT exit code is 20, not 0.
drat-trim replay.cnf replay.drat > replay-checker.log
```

Require both `s UNSATISFIABLE` from the solver and `s VERIFIED` from the checker. Record solver/checker versions and hashes for a fresh run; a different solver version may produce a different valid proof. These jobs can take many minutes. Run them with a supervisor that emits progress or heartbeats, as the campaign runner does for exhaustive searches.

An accepted DRAT proof verifies the formula's unsatisfiability. The mathematical translation from multiplication to that formula remains a separate, inspectable argument in `satenc.py`; it is not a Lean formalization of the rank theorem.
