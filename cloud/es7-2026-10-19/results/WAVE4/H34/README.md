# WAVE4 H34: U_L6 (mop-up round 1)

Case U_L6 (CASE.cnf sha256 741c7fe0917c292eb9401859b03204fd879df0b38a737819360924e44a105424), task list `results/WAVE4/tasks/H34.json` at 4bfd8e7.

- Cubes given: 279 (`U_L6/top.icnf`, sha256 1859d27c3560a0b9a6e74f6376582b2fbea3a15cfb27c9cdd89ac78e3e93b08d).
- Verified leaves: 479 (each CaDiCaL UNSAT with cake_lpr `s VERIFIED UNSAT`), listed in `U_L6/leaves.icnf`.
- Cubes split: 4 (300 s timeouts; march_cu split depth 6 gave 62, 50, 40 and 52 sub-cubes). 275 top cubes closed directly + 204 sub-cubes = 479 leaves.
- Cubes still open: 0 (`U_L6/open.icnf` is empty).
- Every given cube is covered by my leaves: yes, 279/279 (checked by walking the SPLIT records of `leaves.jsonl` down to verified leaves).
- Solve time of the 479 leaves: sum 7583.6 s, median 7.41 s, max 227.77 s. Check time (cake_lpr): sum 1834.6 s, median 2.71 s, max 24.93 s. The 4 split cubes used 300 s each in CaDiCaL plus 541.8, 253.5, 182.0 and 369.6 s of march_cu.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Wall time: driver started 13:39:29 UTC, one run (no resume), finished about 14:30 UTC on 4 cores.

Tools and checks: `tools.txt`, `driver.diff`, `env.txt`. Driver: `close_march.py`, a byte-for-byte copy of `results/WAVE2/F2/close_march.py`.
