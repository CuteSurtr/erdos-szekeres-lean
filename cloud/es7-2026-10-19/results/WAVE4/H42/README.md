# WAVE4 H42: U3_L

- Case: U3_L (U = [3], L = []), case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823 (matches cases.jsonl).
- Cubes given: 191 (`results/WAVE4/tasks/H42.json` at 3ed048e), written to `U3_L/top.icnf` (191 lines, sha256 21824620...49ab8).
- Verified leaves: 191, each with cake_lpr `s VERIFIED UNSAT` (no heap retries).
- Cubes split: 0.
- Cubes still open: 0 (`U3_L/open.icnf` is empty).
- Every given cube is covered by my leaves: yes (each top cube is itself a verified leaf).
- Solve time (CaDiCaL, wall): sum 4678.3 s, median 14.8 s, max 284.9 s.
- Check time (cake_lpr): sum 1089.3 s, median 4.8 s, max 25.5 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Driver run 14:14:41 - ~14:40 UTC, 4 jobs; `close_march.py` is a byte copy of WAVE2/F2 (see driver.diff); tools in tools.txt; environment in env.txt.
