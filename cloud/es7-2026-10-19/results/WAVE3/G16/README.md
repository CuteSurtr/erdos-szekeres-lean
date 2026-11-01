# WAVE3 / G16

Task: `results/WAVE3/tasks/G16.json` (U_L9: 64 open cubes). Environment in `env.txt` (4 cores, 15 GB).
Tools in `tools.txt`: CaDiCaL 3.0.1 (c6073042), march_cu (CnC 705b60c6, `-fcommon`), cake_lpr (a36874a8,
bundled example gives `s VERIFIED UNSAT`). F regenerated, sha256 69c1dc8f…ffff932d (matches).
Driver: `close_march.py`, a byte copy of `WAVE2/F2/close_march.py`; checks (a) mkdtemp per job,
(b) atomic leaves/open writes, (c) case + case_sha256 in the first leaves.jsonl record are recorded in `driver.diff`.

## Results

| case | case CNF sha256 | cubes given | verified leaves | still open | all given cubes covered |
|---|---|---|---|---|---|
| U_L9 | 887d573e…53df928fb4 (matches cases.jsonl) | 64 | 64 | 0 | yes: **closed** |

- Run: `close_march.py U_L9.cnf U_L9 --top <64 given cubes> --name U_L9 --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.65`
  (`U_L9/top.icnf` = the 64 given cubes in file order, top_sha256 09ebf26d…).
- Every given cube was solved directly (no split, no timeout). `leaves.icnf` equals the set of given cubes.
  Each of the 64 records has cake_lpr `s VERIFIED UNSAT`.
- Time: wall 11:14–11:32 UTC (about 18 min); CaDiCaL wall total 1640 s (max 255 s on one cube), cake_lpr total
  428 s, CPU 7163 s. Largest LRAT proof 186 MB (not committed).
- No SAT results. No cake_lpr rejections.
