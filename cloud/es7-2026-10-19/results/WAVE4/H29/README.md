# WAVE4 H29: case U3_L (mop-up round 1)

- Case: U3_L (case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823, matches cases.jsonl).
  F regenerated, sha256 69c1dc8f...ff932d checked.
- Task: `results/WAVE4/tasks/H29.json` at 4bfd8e7, 288 cubes, written to `U3_L/top.icnf` in list order
  (288 lines; top_sha256 e7c585889e8a6f2048f0db1e4b52bfc5836aa401d976219ee0ae4d4f2a4b8698).
- Driver: `close_march.py` (byte copy of WAVE2/F2), `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.222`,
  13:31-15:45 UTC on 4 cores. Tools in `tools.txt`, driver checks in `driver.diff`.

Result:
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no cake_lpr heap retry.
- Verified leaves (cake_lpr `s VERIFIED UNSAT`): 1041 (`U3_L/leaves.icnf`, 1041 lines).
- Cubes split: 20 (all by march_cu -d 6 into 64 sub-cubes, 0 refuted): top cubes #1, #23, #24, #25, #26,
  and 15 sub-cubes of #1 (14 at depth 19, one at depth 25).
- Top cubes closed directly: 283; top cubes covered through splits: #23-#26.
- Still open: 507 cubes in `U3_L/open.icnf`, all descendants of top cube #1
  (`-1420 -552 -2013 -1824 -2029 -1996 -1959 -1978 -1849 -1939 -1918 -1896 -1873`).
  `open.icnf` was checked to equal the frontier rebuilt from `top.icnf` and the SPLIT/verified-UNSAT records.
- Coverage: 287 of the 288 given cubes are fully covered by my leaves; cube #1 is not (507 open sub-cubes).
- Times: UNSAT solves sum 15692.4 s, median 9.44 s, max 296.86 s; cake_lpr checks sum 3712.5 s, median 2.88 s,
  max 30.15 s; 20 solver timeouts at 300 s (6000.5 s) before splitting; march_cu splits sum 5408.8 s,
  median 304.4 s, max 482.0 s.
