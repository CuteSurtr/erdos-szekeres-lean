# WAVE4 H61: case U3_L

Task: `results/WAVE4/tasks/H61.json` (committed at 1d3a72c), case U3_L (U = 3, L = none), 205 cubes (lengths 25-31). Time budget 1.5 h. The driver started at 15:03 UTC and finished at about 15:51 UTC.

- Case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823 matches cases.jsonl. F sha256 matches 69c1dc8f…932d.
- Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`). Tools are listed in `tools.txt`.
- Run: `--top top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.2`.

Result:
- Cubes given: 205.
- Verified leaves (cake_lpr `s VERIFIED UNSAT`): 331. That is 203 of the given cubes solved directly, plus the 128 sub-cubes of 2 split cubes.
- Cubes split: 2 (two length-25 cubes timed out at 300 s; march_cu -d 6 gave 64 cubes for each, none refuted. All 128 are closed as length-31 leaves).
- Cubes still open: 0 (`U3_L/open.icnf` is empty).
- Every given cube is covered by these leaves. Checked: each top cube has a verified leaf that is a subset of it, or it is a split cube whose 64 sub-cubes each have one; the 64 sub-cubes of each split cover all assignments (covercheck.py `cover`). The cover check re-checks this.
- No SAT result, no cake_lpr rejection, and no UNSAT_UNCHECKED record.
- Solve time over the 331 leaves: sum 6557.9 s, median 16.48 s, max 132.29 s (plus the 2 split cubes at 300 s each).
- cake_lpr check time over the 331 leaves: sum 1520.9 s, median 3.59 s, max 23.1 s.

Files in `U3_L/`: top.icnf (the 205 given cubes), leaves.icnf, open.icnf and leaves.jsonl, copied from the driver output after it ended.
