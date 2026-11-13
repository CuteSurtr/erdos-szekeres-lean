# WAVE4 H72 (mop-up round 5): case U3_L

- Task: `results/WAVE4/tasks/H72.json` (commit 754b984), case U3_L, 208 cubes given (all of length 25).
- Case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823 (matches cases.jsonl); F sha256 matches.
- Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see driver.diff), run 2026-10-20 15:28:51Z with
  `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.069 --top top.icnf --name U3_L`; it finished with `open 0`
  in under 20 minutes.

Results (`U3_L/`):
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record.
- Verified leaves: 208 (every leaf has cake_lpr output exactly `s VERIFIED UNSAT`).
- Cubes split: 0. Cubes still open: 0 (`open.icnf` is empty).
- Every given cube is covered by the leaves: `leaves.icnf` equals the set of the 208 given cubes.
- Solve time (CaDiCaL 3.0.1): sum 1679.0 s, median 8.20 s, max 24.72 s.
- Check time (cake_lpr): sum 809.9 s, median 3.64 s, max 8.57 s. Largest LRAT proof 29.1 MB (not committed).
