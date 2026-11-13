# WAVE4 H05: case U_L2

Task file `results/WAVE4/tasks/H05.json` (at e0f250b): case **U_L2** (U = none, L = 2), 325 open cubes.

- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no cake_lpr heap retry.
- Cubes given: 325 (`U_L2/top.icnf`, sha256 073f4b09…, same order as the task file).
- Verified leaves: 325. Each has CaDiCaL exit 20 and cake_lpr printing `s VERIFIED UNSAT`.
- Cubes split: 0. Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Every given cube is covered by my leaves: yes. Each given cube is itself a verified leaf (`leaves.icnf` = the 325 given cubes).
- Solve time (CaDiCaL, wall s): sum 5035.7, median 11.52, max 177.74.
- Check time (cake_lpr, wall s): sum 1563.7, median 4.43, max 17.85. Largest LRAT proof 130.4 MB (not committed).
- Run: 12:52:46 to 13:20 UTC 2026-10-20, 4 jobs, `--timeout 300 --split-depth 6`, driver `close_march.py` (byte-for-byte copy of WAVE2/F2, see `driver.diff`).
- Case CNF sha256 1d26b947…aaa53 matches cases.jsonl. F sha256 69c1dc8f…ffff932d matches. Tools are listed in `tools.txt`, the environment in `env.txt`.
