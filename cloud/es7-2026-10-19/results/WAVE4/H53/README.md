# WAVE4 H53: U3_L

Case U3_L (case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823, matches cases.jsonl).
Task list `results/WAVE4/tasks/H53.json` (commit 94cc404): 218 cubes, written to `U3_L/top.icnf` in file order.

Driver `close_march.py` (byte copy of WAVE2/F2, see driver.diff) ran 14:38:36 - 15:38 UTC with
`--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.2`; it ended with `open 0`.

- Verified leaves: 520 (every one with cake_lpr `s VERIFIED UNSAT`); `U3_L/leaves.icnf` has exactly these 520 cubes.
- Cubes split (CaDiCaL 300 s timeout, then march_cu -d 6): 5 (3 given cubes at 25 literals, 2 of their children at 31 literals).
  march lines: 64/0 refuted, 63/1 refuted, 64/0, 52/10 refuted, 64/0.
- Cubes still open: 0 (`U3_L/open.icnf` is empty).
- Every given cube is covered: checked from leaves.jsonl that each of the 218 cubes is a verified leaf or
  SPLIT with every child (recursively) a verified leaf: 218/218.
- Solve time (525 CaDiCaL runs): sum 10264 s, median 10.2 s, max 300.0 s (the timeouts that were split).
- Check time (520 cake_lpr runs): sum 1634 s, median 2.5 s, max 20.4 s.
- Solve+check per cube: sum 11898 s, median 12.9 s, max 309.7 s.
- No SAT result, no cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT record.
