# WAVE3 / G3: open cubes of U_L2

Task: `results/WAVE3/tasks/G3.json` (at 9a26cc2). It lists 740 open cubes of case U_L2.
Run on 2026-10-20 from 10:56 to 13:57 UTC on 4 cores (`env.txt`). Tools and hashes are in `tools.txt`.
The driver `close_march.py` is a byte-identical copy of WAVE2/F2's; `driver.diff` records the checks.

## Result

| case | cubes given | given cubes fully closed | verified leaves | cubes still open | every given cube covered? |
|---|---|---|---|---|---|
| U_L2 | 740 | 709 | 1060 | 1948 | yes, by leaves + open; **not closed** |

- The case CNF has sha256 1d26b947…aaa53, which equals cases.jsonl.
- No SAT result. No cake_lpr rejection: all 1060 UNSAT answers printed `s VERIFIED UNSAT`, and there is no UNSAT_UNCHECKED or TIMEOUT record.
- 704 given cubes were closed directly, each by one CaDiCaL run under 300 s.
- 36 given cubes timed out at 300 s and were split with `march_cu -d 6`, 64 sub-cubes each.
  - Of those 2304 sub-cubes, 356 are verified. The other 1948 never started before the deadline and are listed in `U_L2/open.icnf`.
  - 5 of the 36 split cubes ended up fully closed. The 31 given cubes that remain open are exactly those split cubes with open sub-cubes left.
- Time:
  - CaDiCaL wall time over all runs: 29 327 s. Of that, 18 526 s went to the 1060 UNSAT leaves, and the rest to the 36 runs that hit the 300 s timeout.
  - cake_lpr: 3878 s.
  - march_cu splits: 4909 s.
  - The `cpu_s` field in leaves.jsonl is not usable. It is taken from process-wide `os.times()` across threads, so concurrent jobs overlap.

## Cover check (done after the driver stopped)
- Every line of `leaves.icnf`, `open.icnf` and `top.icnf` matches `a … 0`.
- `top.icnf` equals the 740 G3.json cubes in file order.
- The first record of `leaves.jsonl` is `{"case": "U_L2", "case_sha256": "1d26b947…"}`.
- leaves.icnf is exactly the set of cubes whose records have cake_lpr = `s VERIFIED UNSAT`.
- leaves and open are disjoint.
- Starting from each given cube and expanding SPLIT records gives verified leaves and open.icnf cubes only. The totals are 1060 leaves and 1948 open, so no cube is missing or extra.

## Files
- `U_L2/top.icnf`: the 740 given cubes.
- `U_L2/leaves.icnf`: 1060 verified leaves. These are full cubes over F's variables, without the case units, which hullsplit adds.
- `U_L2/open.icnf`: 1948 open cubes. All of them are depth-6 sub-cubes of the 31 open given cubes.
- `U_L2/leaves.jsonl`: one record per job, with solve and check times, and the sub-cubes for each SPLIT.

Next step: the 1948 open sub-cubes. Judging from the 356 that closed, most should close within the 300 s cap. At about 20 s solve plus 4 s check each on 4 cores, that is roughly 3 hours.
