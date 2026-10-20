# WAVE4 H21: case U_L6

Task file `results/WAVE4/tasks/H21.json` (commit e0f250b): case U_L6, 196 open cubes.
Driver `close_march.py` (byte copy of `results/WAVE2/F2/close_march.py`, sha256 2e0975aa…c855; see driver.diff),
run 2026-10-20 12:56:54 to 13:51:00 UTC on 4 cores (`--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.22`).
Case CNF sha256 741c7fe0…5424 (matches cases.jsonl); F sha256 69c1dc8f…932d. Tools: tools.txt.

Results (`U_L6/`):
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT record.
- Cubes given: 196 (`top.icnf`, task file order).
- Verified leaves: 519 (`leaves.icnf`; each with cake_lpr `s VERIFIED UNSAT`). 195 of the 196 given cubes are leaves themselves.
- Cubes split: 6 (one given cube, length 25, split into 58 by march_cu -d 6; then 5 of its descendants split again into 31, 59, 53, 64, 64).
- Cubes still open: 0 (`open.icnf` is empty; driver printed `open 0`).
- Every given cube is covered by the leaves (checked by walking the SPLIT records of leaves.jsonl from each top cube down to verified leaves; every leaves.icnf line ends in ` 0`, no duplicates).
- Time: CaDiCaL solve over 525 runs sum 9411 s, median 7.05 s, max 300.0 s (the 6 split cubes timed out);
  cake_lpr check over 519 leaves sum 1971 s, median 2.65 s, max 24.9 s;
  solve+check per verified leaf sum 9583 s, median 9.64 s, max 239.4 s; march_cu splits sum 1461 s, median 208 s, max 497 s.
