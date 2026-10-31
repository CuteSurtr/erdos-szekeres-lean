# WAVE3 / G14: open cubes of case U_L7

Task: `results/WAVE3/tasks/G14.json` (9a26cc2). It holds 64 open cubes of case U_L7. Run on 2026-10-20, 11:20–14:07 UTC, on
4 cores (see `env.txt`). Tools and hashes are in `tools.txt` and the driver check is in `driver.diff`.

- F sha256 69c1dc8f…932d OK. U_L7.cnf (`hullsplit.py case F "" 7`) sha256 c6d1c840…f099 = cases.jsonl OK.
- Driver: `close_march.py` (= WAVE2/F2, unchanged), run as `--name U_L7 --top <64 cubes in file order> --depth 7
  --timeout 300 --split-depth 6 --jobs 4 --hours 2.722`, one call, fresh output directory, no `--skip`.

## Result per case

| case | cubes given | verified leaves | cubes still open | every given cube covered? |
|------|-------------|-----------------|------------------|---------------------------|
| U_L7 | 64 | 285 | 1725 | **no**. 63 of 64 are covered; given cube #52 (0-based) is not |

- **No SAT result.** No cake_lpr rejection: all 285 UNSAT answers print `s VERIFIED UNSAT`, and none are UNSAT_UNCHECKED.
- 63 of the 64 given cubes are closed, each by one verified leaf, with no split. Per-cube detail is in `leaves.jsonl`.
- Given cube #52 (`top.icnf` line 53, `a 1089 524 -508 1245 -507 -506 -505 0`) is hard. It timed out at 300 s, and so did one of its
  depth-13 sub-cubes. Of that sub-cube's 64 depth-19 sub-cubes, 8 timed out. Their depth-25 sub-cubes in turn split
  again (32 SPLIT records in total). All 1725 open cubes lie under #52. Open depths: 31: 1180, 25: 502, 30: 34,
  29: 4, 24: 2, 23: 2, 27: 1.
- Time (summed over jobs):
  - CaDiCaL: 23 748 s in total, 14 147 s on verified leaves and 9 601 s on 300 s timeouts;
  - cake_lpr: 1 794 s;
  - march_cu splits: 10 805 s;
  - total child CPU: 139 243 s.
- `open.icnf` lists exactly the frontier still open. I re-derived it from `leaves.jsonl` after the driver exited (top
  cubes expanded through the SPLIT `subs`, minus the verified leaves), and it equals the file. `leaves.icnf` equals the
  set of records with `s VERIFIED UNSAT`. Every line of both files is well formed (`a … 0`).

## Files
`U_L7/top.icnf` (the 64 given cubes), `U_L7/leaves.icnf` (285 verified leaves, full cubes over F's variables),
`U_L7/open.icnf` (1725 open cubes), `U_L7/leaves.jsonl` (the first record has case and case_sha256).
