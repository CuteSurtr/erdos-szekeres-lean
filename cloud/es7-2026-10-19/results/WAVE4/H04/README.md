# WAVE4 H04: case U_L2

Task file `results/WAVE4/tasks/H04.json` at e0f250b. Budget 2.5 h; driver ran 12:54-14:02 UTC (4 cores).

- Case U_L2 (U = {}, L = {2}). Case CNF sha256 1d26b947...aaa53, matches cases.jsonl. F sha256 69c1dc8f...ff932d.
- Cubes given: 325 (`U_L2/top.icnf`, 325 lines, in the task file's order; top_sha256 e7bb995d...f781).
- Verified leaves: 640. Every one has cake_lpr output exactly `s VERIFIED UNSAT` (`U_L2/leaves.icnf`, 640 distinct lines, each ending ` 0`).
- Cubes split: 5 (3 given cubes, plus 2 of their children), each into 64 sub-cubes by march_cu -d 6 (0 refuted). 322 given cubes closed directly.
- Cubes still open: 0 (`U_L2/open.icnf` is empty; driver printed `open 0`).
- Cover: every one of the 325 given cubes is covered by these leaves (checked by walking SPLIT records: each frontier cube contains a verified leaf).
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
- Solve time (CaDiCaL wall, all 645 runs incl. the 5 that hit the 300 s cap): sum 11892.7 s, median 11.34 s, max 300.04 s.
- Check time (cake_lpr, 640 proofs): sum 2307.6 s, median 2.84 s, max 20.25 s. Largest LRAT proof 241 MB (not committed).

Files: env.txt, tools.txt, driver.diff (driver checks; close_march.py is a byte-identical copy of WAVE2/F2/close_march.py),
close_march.py, U_L2/{top.icnf, leaves.icnf, open.icnf, leaves.jsonl}.
