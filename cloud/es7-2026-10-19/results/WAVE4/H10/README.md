# WAVE4 H10: U_L2

Task file `results/WAVE4/tasks/H10.json` (as of e0f250b): case **U_L2** (U = "", L = "2"), **325 cubes**.
I ran the driver from 12:54:30 to about 13:38 UTC with `--hours 2.219`. It finished early with `open 0`.

## Result
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record. No TIMEOUT record.
- Cubes given: 325 (`U_L2/top.icnf` has one line per listed cube, in the file's order).
- Verified leaves: **451**. cake_lpr printed `s VERIFIED UNSAT` for every leaf, and `U_L2/leaves.icnf` has 451 lines.
- Cubes split: **2**. Each one hit the 300 s cap and march_cu split it at depth 6 into 64 sub-cubes, 0 refuted.
- Cubes still open: **0**, and `U_L2/open.icnf` is empty.
- Cover: all 325 given cubes are covered by these leaves. I rebuilt the split tree from the SPLIT records in `leaves.jsonl`. Every node in the tree has a subset leaf, or its children are all covered.
- Times:
  - Solve time, CaDiCaL wall: 453 runs, sum 7766.5 s, median 10.17 s, max 300.01 s. These figures include the two timed-out runs.
  - Solve time, UNSAT leaves only: sum 7166.5 s, median 10.17 s, max 160.59 s.
  - Check time, cake_lpr: 451 runs, sum 1909.0 s, median 3.35 s, max 18.17 s.
  - Splitting with march_cu: 745 s in total.

## Files
- `env.txt`: the environment.
- `tools.txt`: the tool commits and binary sha256s, plus the F and case sha256 checks. Both match.
- `driver.diff`: what I checked in the driver.
- `close_march.py`: a byte-for-byte copy of `results/WAVE2/F2/close_march.py`, sha256 2e0975aa…c855. I ran an identical copy at `/opt/work/close_march.py` (checked with cmp) so that nothing in the git checkout was used while the driver ran. The output directory was `/opt/work/out/U_L2`.
- `U_L2/`: `top.icnf`, `leaves.icnf`, `open.icnf` and `leaves.jsonl`, copied from that output directory after the driver ended.
