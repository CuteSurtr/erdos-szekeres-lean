# WAVE4 H39: case U_L7

Task file `results/WAVE4/tasks/H39.json` (commit 4bfd8e7): case U_L7, 196 open cubes.
Driver: `close_march.py` (byte-for-byte copy of `results/WAVE2/F2/close_march.py`, sha256 2e0975aa...c855; see `driver.diff`),
run 13:43:37-14:12 UTC with `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.2` on 4 cores. Tools: `tools.txt`.

Result:
- Cubes given: 196 (`U_L7/top.icnf`, sha256 57c2751eb22be09e34ba40f7ef6160a961793d16bab705bcedf6ebe268354638).
- Verified leaves: 196, each CaDiCaL UNSAT with cake_lpr printing `s VERIFIED UNSAT` (no heap retries).
- Cubes split: 0. Cubes still open: 0 (`U_L7/open.icnf` is empty).
- Cover: every given cube is now covered; `leaves.icnf` equals `top.icnf` as a set of cubes (each given cube closed directly).
- Solve time (CaDiCaL, wall s): sum 4354.9, median 9.18, max 259.3.
- Check time (cake_lpr, wall s): sum 1058.0, median 3.65, max 23.64.
- Solve+check per cube: sum 5412.8, median 13.09, max 281.34. Largest LRAT proof 213.5 MB (not committed).
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED or TIMEOUT record.

Files: `U_L7/leaves.jsonl` (all records; first record names the case and its CNF sha256 c6d1c840...f099, matching cases.jsonl),
`U_L7/leaves.icnf`, `U_L7/open.icnf`, `U_L7/top.icnf`, `env.txt`, `tools.txt`, `driver.diff`, `close_march.py`.
