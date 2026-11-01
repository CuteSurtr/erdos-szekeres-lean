# WAVE4 H65: case U3_L

- Task file: `results/WAVE4/tasks/H65.json` (at 1d3a72c), case **U3_L** (case CNF sha256 7ab00d97…f823, matches cases.jsonl).
- Cubes given: **204** (`U3_L/top.icnf`, 204 lines, sha256 1aaa752e…8efb).
- Verified leaves: **204** — every given cube solved UNSAT by CaDiCaL 3.0.1 within the 300 s cap and its LRAT proof accepted by cake_lpr (`s VERIFIED UNSAT`).
- Cubes split: **0**. Cubes still open: **0** (`U3_L/open.icnf` is empty).
- Cover: every given cube is now covered by my leaves (leaves.icnf equals top.icnf as a set; every line ends in `0`).
- Solve time (CaDiCaL wall, 204 leaves): sum 4420.0 s, median 18.69 s, max 138.76 s.
- Check time (cake_lpr): sum 1093.0 s, median 4.31 s, max 17.81 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Driver ran 15:07:55–15:31 UTC (`--jobs 4 --timeout 300 --split-depth 6 --hours 1.18`).
- Note: a first launch at 15:07:40 UTC ran without the --top file (my mistake); it was killed within seconds
  during the initial march, its output directory deleted, and the driver restarted cleanly (see driver.diff).
