# WAVE4 H07: case U_L2

Task file `results/WAVE4/tasks/H07.json` (commit e0f250b): case U_L2, 325 open cubes.

- Case CNF: sha256 1d26b947...aaa53, which matches cases.jsonl. F: sha256 69c1dc8f...ffff932d (regenerated).
- Tools: see `tools.txt`. Driver: an unmodified copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`).
  Run: `--top top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.2`, started 12:53:49 UTC.
  It ended with `open 0` well before its deadline.

## Result
- Cubes given: 325 (top.icnf; 325 lines).
- Verified leaves: 765. Each one is CaDiCaL UNSAT, and cake_lpr printed `s VERIFIED UNSAT` on its LRAT proof.
- Cubes split: 7. Each timed out at 300 s and was split by march_cu -d 6, giving 447 sub-cubes. 325 - 7 + 447 = 765.
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Cover: every one of the 325 given cubes is covered by the leaves in `U_L2/leaves.icnf`, through the
  SPLIT records in `leaves.jsonl`. The check was a tree walk; all leaf lines are well formed (`a ... 0`).
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
- Solve time over the 765 leaves: sum 21874.4 s, median 22.1 s, max 217.97 s.
- cake_lpr check time: sum 3473.7 s, median 3.69 s, max 20.19 s.
- The 7 split cubes took 2100.1 s of solver time before their timeouts and 1768.3 s in march_cu.

Files in `U_L2/`: `top.icnf`, `leaves.icnf`, `open.icnf` and `leaves.jsonl`, copied from the driver's output directory.
