# WAVE4 H74: case U_L2

Task file `results/WAVE4/tasks/H74.json` (commit 754b984): case U_L2, 13 open cubes.
Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`), tools in `tools.txt`.
Run 2026-10-20 15:18:27 UTC to 15:21 UTC, 4 jobs, timeout 300 s, split depth 6.

- Cubes given: 13
- Verified leaves: 13 (every one with cake_lpr `s VERIFIED UNSAT`)
- Cubes split: 0
- Cubes still open: 0 (`U_L2/open.icnf` is empty; driver printed `open 0`)
- Cover: every given cube is covered by the leaves; `U_L2/leaves.icnf` equals `U_L2/top.icnf` as a set of cubes.
- Solve time (CaDiCaL): sum 580.0 s, median 46.7 s, max 76.6 s
- Check time (cake_lpr): sum 136.4 s, median 11.3 s, max 14.6 s
- Solve + check per cube: sum 716.4 s, median 57.9 s, max 91.2 s
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

Files in `U_L2/`: `top.icnf` (the 13 given cubes), `leaves.icnf`, `open.icnf`, `leaves.jsonl`
(first record: case U_L2, case_sha256 1d26b947...aaa53).
