# V3A V02: shard 2 of 16, first pass of the v3 acceptance check of mirror sub-case (ii)

Run 2026-10-20, 09:05 to 10:49 UTC, on 4 cores with 15 GB RAM (`env.txt`). The run was stopped at 10:49 so the README could be written within the time budget.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, built with `make cake_lpr`. Its bundled example prints `s VERIFIED UNSAT`. Binary sha256s are in `tools.txt`.
- F was regenerated with gen_etv.py and mirgen.py. Its sha256 is 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, which matches the expected value.
- verify/v3 scripts are taken from commit 7c6d70c, and the inputs are pinned at commit a033a13.
- v3_jsonl_leaves.py reported 72 dirs, 17942 leaf lines and 47 skipped records.
- v3_manifest.py reported 17,989 leaves in 100 cases with 0 problems, the same as the other machine.
  - M.jsonl sha256: 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e
- Mr.jsonl removes the 40 ACCEPTED cases of V3T/accepted.tsv (357 records) and renumbers idx. Script: `mkmr.py`.
  - n = 17632 records in 60 cases.
  - sha256: 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def
- Shard 2/16 has 1102 leaves and 4 covers (U10_L2, U4-5_L, U7_L15, U_L2-3).

## Results (`out.jsonl`)
- Leaves: 1065 VERIFIED, 0 REJECTED, 0 SAT, 0 TIMEOUT.
- 37 leaves are still unchecked: U_L4 1, U_L5 14, U_L8 22. These are left for the second pass.
- Covers: 3 VERIFIED (U4-5_L, U7_L15, U_L2-3) and 1 NOT_COVERED (U10_L2).
  - U7_L15 is VERIFIED without solving because the empty cube is one of its leaves.
- Solve time over the 1065 leaves: sum 19605 s, median 15.0 s, max 240 s.
- Check time over the 1065 leaves: sum 4472 s, median 3.15 s, max 26.5 s.

## Non-VERIFIED
- Cover U10_L2 is NOT_COVERED: CaDiCaL returned rc 10 on the cover CNF of its 125 leaves.
  - Sources: results/WAVE1/W32/U10_L2 and jtree/W32/U10_L2.
  - At a033a13 that directory still has 1 cube in open.icnf, so the case was not finished at the input commit. This is expected, not an error.
- There are no SAT, REJECTED or TIMEOUT leaves.
