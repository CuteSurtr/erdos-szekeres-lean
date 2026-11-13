# WAVE4 H23: U_L6

- Case: U_L6 (U = {}, L = {6}); CASE.cnf sha256 741c7fe0917c292eb9401859b03204fd879df0b38a737819360924e44a105424 (matches cases.jsonl).
- Cubes given: 196 (`results/WAVE4/tasks/H23.json` at e0f250b), written in order to `U_L6/top.icnf` (196 lines, sha256 6aba4283...1f2bad).
- Verified leaves: 196. Every given cube was solved directly by CaDiCaL (UNSAT within the 300 s cap) and its LRAT proof checked by cake_lpr with the exact line `s VERIFIED UNSAT`.
- Cubes split: 0. Cubes still open: 0 (`U_L6/open.icnf` is empty; driver printed `open 0`).
- Cover: every given cube is covered by a leaf (`leaves.icnf` equals the set of given cubes, no duplicates, every line ends in ` 0`).
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. cake_lpr heap retries: 0.
- Solve time (wall, per cube): sum 3589.4 s, median 11.9 s, max 176.2 s.
- Check time (cake_lpr, per cube): sum 979.2 s, median 3.9 s, max 22.9 s. Largest LRAT proof 165 MB (not committed).
- (The `cpu_s` field in leaves.jsonl uses process-wide os.times() and so includes other jobs running concurrently; it overstates per-cube CPU.)
- Run: driver started 2026-10-20 12:56:42 UTC with --jobs 4 --timeout 300 --split-depth 6 --hours 2.217, finished about 13:16 UTC.
- Tools and checks: `tools.txt`; driver copy and checks: `driver.diff`; environment: `env.txt`.
