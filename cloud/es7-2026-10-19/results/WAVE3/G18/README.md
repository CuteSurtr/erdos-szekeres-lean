# WAVE3 G18: open cubes of U9_L

Task: `results/WAVE3/tasks/G18.json` (at 9a26cc2), 59 open cubes of case U9_L, each of 7 literals.

| case | cubes given | verified leaves | cubes still open | every given cube covered | solve / check time |
|------|------------:|----------------:|-----------------:|:------------------------:|--------------------|
| U9_L | 59 | 433 | 0 | yes (closed) | wall 67 min on 4 cores (11:15:46 to 12:22:55 UTC); CaDiCaL on the 433 leaves 10,328 s, on the 6 split cubes 6 x 300 s; march splits 1,128 s; cake_lpr 1,899 s |

- No SAT results. No cake_lpr rejection: all 433 leaf records have `cake_lpr: "s VERIFIED UNSAT"`, with no heap retries.
  The largest LRAT proof was 178 MB (not committed).
- Splits: 6 cubes timed out at 300 s and were split by march_cu at split depth 6 (64 sub-cubes each, 0 refuted).
  All 6 are inside the given cube `-1134 -1155 8933 -1245 -1212 -1229 -1194`. The leaves go to depth 25.
- Case CNF: `hullsplit.py case F.cnf 9 "" U9_L.cnf`, sha256 379250e6…22e5, which matches cases.jsonl.
  F sha256 69c1dc8f…932d matches the expected value.
- Cover check (my own script, strict parse that rejects any line not ending in ` 0`): every cube in
  `U9_L/given.icnf` is covered by the union of `U9_L/leaves.icnf`, and every leaf extends a given cube.
  `open.icnf` is empty. The driver's own frontier also reports `open 0`.
- Files: `U9_L/given.icnf` (= `top.icnf`, the 59 task cubes in file order), `leaves.icnf`, `leaves.jsonl`
  (its first record holds case and case_sha256), `open.icnf` (empty).
  Tools are in `tools.txt` and the driver check is in `driver.diff`. `close_march.py` is identical to WAVE2/F2's.
- The `cpu_s` field in leaves.jsonl comes from process-wide `os.times()` children counters. With 4 threads it
  over-counts, so use `solve_s`/`check_s` for timing.
