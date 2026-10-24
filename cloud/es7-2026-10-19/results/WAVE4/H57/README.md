# WAVE4 H57: U_L2

Task file `results/WAVE4/tasks/H57.json` (commit 94cc404), case U_L2 (U = [], L = [2]),
case CNF sha256 1d26b947...aaa53 (matches cases.jsonl), F sha256 69c1dc8f...ff932d.
Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`), run with
`--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.2`, 14:38:57 to about 15:08 UTC. Tools: `tools.txt`.

- Cubes given: 214 (`U_L2/top.icnf`, in the task file's order).
- Verified leaves: 214 (each with cake_lpr `s VERIFIED UNSAT`); `U_L2/leaves.icnf` = the 214 given cubes.
- Cubes split: 0.
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Every given cube is covered by a verified leaf: yes (214/214, each leaf equals its cube).
- Solve time (CaDiCaL): sum 5756.5 s, median 14.1 s, max 232.8 s.
- Check time (cake_lpr): sum 1234.9 s, median 4.5 s, max 25.5 s.
- Solve + check per cube: sum 6991.4 s, median 19.7 s, max 258.3 s.
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT or SKIP record.
