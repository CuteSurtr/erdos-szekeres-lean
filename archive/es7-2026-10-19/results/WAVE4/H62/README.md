# WAVE4 H62: case U3_L

Task: the 205 open cubes of case U3_L in `results/WAVE4/tasks/H62.json` (commit 1d3a72c), mop-up round 4.
Case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823 (matches cases.jsonl).
Driver: `close_march.py` (byte copy of WAVE2/F2, see driver.diff), `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.214`,
started 15:03:35 UTC, finished 15:45 UTC with `open 0`.

Result:
- cubes given: 205
- verified leaves: 331 (every one `s VERIFIED UNSAT` by cake_lpr); listed in `U3_L/leaves.icnf`
- cubes split: 2 (both depth-25 cubes timed out at 300 s; march_cu -d 6 gave 64 sub-cubes each, 0 refuted)
- cubes still open: 0 (`U3_L/open.icnf` is empty)
- every given cube is covered by my leaves: yes (checked from leaves.jsonl: each top cube is a verified leaf, or split with all children verified)
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

Time over the 331 verified leaves (seconds): solve sum 6990.7, median 12.9, max 218.0;
check sum 1572.0, median 2.89, max 27.2. The 2 timed-out solves before splitting: 600.0 s.
