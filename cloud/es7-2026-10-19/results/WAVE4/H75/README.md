# WAVE4 H75: mop-up round 6, case U3_L

Task file `results/WAVE4/tasks/H75.json` (committed at 4b2609a), time budget 1.25 h.
Case CNF built with hullsplit.py (U=3, L empty), sha256 7ab00d97…f823, matching cases.jsonl.
F regenerated with sha256 69c1dc8f…932d. Tools and driver: `tools.txt`, `driver.diff`.
The driver (`close_march.py`, a byte-identical copy of WAVE2/F2) ran from 15:59:41 to 16:10 UTC
with `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 0.981`.

- Case: U3_L
- Cubes given: 112 (`U3_L/top.icnf`, identical to the task list in order)
- Verified leaves: 112. Each has the cake_lpr line `s VERIFIED UNSAT` (`U3_L/leaves.icnf`, `U3_L/leaves.jsonl`)
- Cubes split: 0
- Cubes still open: 0 (`U3_L/open.icnf` is empty)
- Every given cube is covered by my leaves: yes. The leaves are exactly the 112 given cubes.
- Solve time (CaDiCaL): sum 1629.3 s, median 9.6 s, max 188.3 s
- Check time (cake_lpr): sum 559.6 s, median 4.35 s, max 23.9 s
- Solve plus check per cube: sum 2189.0 s, median 14.2 s, max 212.2 s
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
