# WAVE4 H02: case U_L2

- Task: `results/WAVE4/tasks/H02.json` (committed at e0f250b), case U_L2, 325 cubes given.
- Case CNF sha256 1d26b947...aaa53 matches cases.jsonl; F sha256 69c1dc8f...932d matches.
- Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see driver.diff); depth 7 (top cubes from
  --top), timeout 300 s, split depth 6, 4 jobs, run 12:53-about 15:05 UTC. Driver printed `open 0`.
- No SAT result. No cake_lpr rejection and no UNSAT_UNCHECKED record.
- Verified leaves (cake_lpr `s VERIFIED UNSAT`): 1079 (U_L2/leaves.icnf).
- Cubes split (CaDiCaL timed out at 300 s, march_cu -d 6): 12.
- Cubes still open: 0 (U_L2/open.icnf is empty).
- Cover: all 325 given cubes are covered by my verified leaves (each top cube is a leaf, or is split
  and every sub-cube is recursively covered; checked from leaves.jsonl).
- Solve time over the 1079 verified leaves: sum 16009 s, median 9.48 s, max 198.29 s.
  Check time (cake_lpr): sum 3984 s, median 2.82 s, max 24.35 s.
  Plus 12 x 300 s solver timeouts on the split cubes.
- Files: U_L2/{top.icnf, leaves.icnf, open.icnf, leaves.jsonl}; env.txt, tools.txt, close_march.py, driver.diff.
