# WAVE4 H11: U_L2

Task file: `results/WAVE4/tasks/H11.json` (at e0f250b): case U_L2, 324 open cubes.
Driver: `close_march.py`, a byte-for-byte copy of WAVE2/F2 (see `driver.diff`). Tools are in `tools.txt`.
Run: 2026-10-20 12:54:26 to about 14:35 UTC, 4 jobs, timeout 300 s, split depth 6, with `--hours 2.22`.
Case CNF sha256 is 1d26b947…aa53 and matches cases.jsonl.

Results (`U_L2/`):
- No SAT results. No cake_lpr rejection. No UNSAT_UNCHECKED records.
- Cubes given: 324 (`top.icnf`, sha256 c555d48d…202b).
- Verified leaves: 765 (`leaves.icnf`). For each, cake_lpr printed `s VERIFIED UNSAT`.
- Cubes split: 7. Each split hit the 300 s timeout and march_cu -d 6 gave 64 sub-cubes, 0 refuted; 448 sub-cubes in all.
- Cubes still open: 0 (`open.icnf` is empty; the driver printed `open 0`).
- Cover: every one of the 324 given cubes is covered by the verified leaves. I checked this by walking each top cube's SPLIT tree down to the leaves in leaves.icnf. Every line ends in ` 0`, and leaves.icnf equals the set of verified records in leaves.jsonl.
- Solve time over 772 CaDiCaL runs, including the 7 timeouts: sum 14346.8 s, median 9.50 s, max 300.02 s.
- Check time over 765 cake_lpr runs: sum 3215.4 s, median 3.21 s, max 23.17 s.
- march_cu split time: sum 1304.3 s.
