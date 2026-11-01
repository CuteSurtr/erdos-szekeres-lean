# V3A V12: shard 12 of 16, first pass of the from-scratch acceptance check of mirror sub-case (ii)

Run 2026-10-20 09:07-10:50 UTC on a 4-core, 15 GB VM (env.txt). The run was stopped at the time limit.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical)
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its bundled example prints `s VERIFIED UNSAT`.
- F = m33k7int.sub.cnf, regenerated: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- inputs at commit a033a13; verify/v3 at commit 7c6d70c
- v3_jsonl_leaves: dirs 72, leaf lines 17942, skipped records 47
- v3_manifest: 17,989 leaves in 100 cases, 0 problems (same as the other machine).
  M.jsonl sha256 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e
- Mr.jsonl (40 ACCEPTED cases removed, 357 records): n = 17632 leaves in 60 cases,
  sha256 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def (same as the other V3A machines)
- Shard 12/16: 1102 leaves and 3 covers (U6_L, U3-9_L, U_L14). Run with --jobs 4 --cap 1800.

## Results (out.jsonl)
- Leaves: VERIFIED 982, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 120 {'U_L4': 76, 'U_L5': 21, 'U_L6': 1, 'U_L8': 22}
- Covers: VERIFIED 2 (U3-9_L, U_L14), NOT_COVERED 1: **U6_L** (868 leaves, cover CNF SAT, rc 10).
  U6_L leaves come from W16, which was still running U6_L at a033a13 ("W16: U6_L shard 1 progress 08:53").
  The leaf set is incomplete at this commit. This is not a counterexample.
- Solve time over the 982 leaves: sum 20330.6 s, median 18.85 s, max 387.34 s
- cake_lpr check time: sum 4219.2 s, median 3.23 s, max 31.28 s

Every VERIFIED record has cake_lpr output `s VERIFIED UNSAT`. The leaves that are still unchecked have no record, so the second pass will pick them up.
