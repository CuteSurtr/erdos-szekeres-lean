# WAVE4 H30 (mop-up round 1): case U3_L

- Task: `results/WAVE4/tasks/H30.json` at 4bfd8e7, case U3_L, 288 cubes given (top.icnf, sha256 4b13ca01c005860890e084b164657b0ef6e32cbb9172605457513a2b5db04334).
- Case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823 (matches cases.jsonl); F sha256 matches.
- Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see driver.diff), `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.21`, started 2026-10-20T13:31:44Z, finished about 15:00Z with `open 0` (one run, no restart).

Results (`U3_L/`):
- Verified leaves: 666, every one with cake_lpr `s VERIFIED UNSAT` (282 given cubes closed directly, 384 sub-cubes).
- Cubes split: 6 (each into 64 sub-cubes by march_cu -d 6; all 384 sub-cubes closed).
- Cubes still open: 0 (`open.icnf` is empty).
- Every given cube is covered by the leaves in `U3_L/leaves.icnf` (checked: each top cube is a verified leaf or split, and all of its sub-cubes are verified leaves; every leaves.icnf line ends in ` 0`).
- Solve time (CaDiCaL, wall): sum 14793 s, median 10.3 s, max 300.0 s (the timeouts that led to splits).
- Check time (cake_lpr): sum 2774 s, median 3.5 s, max 24.1 s.
- Split time (march_cu): 143.5, 163.7, 365.3, 381.6, 440.8, 228.3 s.
- No SAT result, no cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT record.
