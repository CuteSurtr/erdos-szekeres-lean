# WAVE4 H32: case U_L2

- Case: U_L2 (CASE.cnf sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53, matches cases.jsonl).
- Cubes given: 327 (results/WAVE4/tasks/H32.json at 4bfd8e7; top.icnf sha256 7f1ce496a9368652b623989d68b7f0a8f06a4e5302e912ff01acfb65f37de633).
- Verified leaves: 327 (each with cake_lpr line exactly `s VERIFIED UNSAT`).
- Cubes split: 0 (no cube hit the 300 s cap).
- Cubes still open: 0 (open.icnf is empty).
- Coverage: every given cube is covered; the 327 leaves in leaves.icnf are exactly the 327 given cubes.
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record.
- Times over the 327 leaves (seconds, wall per job):
  - solve: sum 4637.1, median 12.13, max 255.84
  - check (cake_lpr): sum 1486.9, median 4.30, max 22.64
- Driver started 13:31:33 UTC, all cubes closed by 13:57 UTC (4 jobs).
- Driver: close_march.py, byte-identical copy of results/WAVE2/F2/close_march.py (see driver.diff). Tools: tools.txt.
