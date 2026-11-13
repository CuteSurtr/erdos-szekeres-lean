# WAVE4 H09: case U_L2

- Case: U_L2 (CASE.cnf sha256 1d26b947...aa53, matches cases.jsonl). Cubes given: 325 (`tasks/H09.json` at e0f250b), written in order to `U_L2/top.icnf` (325 lines).
- Result: **all 325 given cubes are closed.** Every top cube is covered by the verified leaves through the recorded split tree, and `open.icnf` is empty.
- Verified leaves: 815 (CaDiCaL exit 20, cake_lpr printed `s VERIFIED UNSAT`). `leaves.icnf` lists exactly these 815 cubes.
- Cubes split: 8 (300 s timeouts, split with march_cu -d 6), giving 498 sub-cubes. TIMEOUT records left open: 0.
- No SAT results, no cake_lpr rejections, no UNSAT_UNCHECKED records, and no cake_lpr heap retries.
- Solve time over the verified leaves: sum 13910.6 s, median 9.73 s, max 296.6 s. Check time (cake_lpr): sum 2700.4 s, median 2.49 s, max 22.36 s. On top of that, the 8 split cubes used 2400.2 s of CaDiCaL timeouts and 1731.9 s of march_cu splitting.
- Wall time: driver ran 12:53–14:2x UTC (about 1.5 h of the 2.5 h budget) with 4 jobs.
- Tools and driver: see `tools.txt` and `driver.diff`. The driver is an unmodified copy of WAVE2/F2/close_march.py (sha256 2e0975aa...), run from an identical copy at /opt/work/close_march.py. Its output directory /opt/work/out/U_L2 was outside the git checkout.
- Files: `U_L2/{top.icnf, leaves.icnf, open.icnf, leaves.jsonl}` were copied verbatim from the driver's output directory.
