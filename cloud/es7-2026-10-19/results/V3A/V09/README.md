# V3A V09: first pass, shard 9 of 16, from-scratch acceptance check of mirror sub-case (ii)

Ran 2026-10-20, 09:05–10:48 UTC, on 4 cores with 15 GB RAM (`env.txt`).

## Tools (`tools.txt`)
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, at /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its bundled example prints `s VERIFIED UNSAT`.
- F regenerated with gen_etv.py and mirgen.py (`--interior --yflip-unit`). sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d matches.
- verify/v3 scripts run from a worktree at 7c6d70c. Inputs from a worktree at a033a13.

## Inputs (`inputs.txt`)
- v3_jsonl_leaves.py: 72 dirs, 17942 leaf lines, 47 skipped records
- v3_manifest.py: 17989 leaves in 100 cases, 0 problems. This is the same as the other machine.
  - M.jsonl sha256 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e
  - C.jsonl sha256 8724fba58ba65d45c331522be734f781199a55e7abaaec42fe0e60a77f89b82b
- Mr.jsonl drops the 40 ACCEPTED cases of V3T/accepted.tsv (357 records, script in `mkmr.py`). It has n = 17632 leaves in 60 cases.
  - sha256 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def
- Shard 9/16 has 1102 leaves and 4 covers: U14_L, U5_L16, U9_L6, U_L5.

## Results (`out.jsonl`)
- Leaves: 972 VERIFIED, 0 REJECTED, 0 SAT, 0 TIMEOUT. 130 of the shard's 1102 leaves are still unchecked; the run was stopped at the time limit, so they go to the second pass.
- Covers: 3 VERIFIED (U14_L with 128 leaves, U5_L16 with 104, U9_L6 with 115) and 1 NOT_COVERED (U_L5).
- Leaf solve time: sum 20437 s, median 16.5 s, max 258.9 s.
- Leaf check time: sum 3829 s, median 3.06 s, max 20.1 s.

## Non-VERIFIED records
- **U_L5 cover: NOT_COVERED** (CaDiCaL rc 10; nleaves 349; leaves_sha256 395f1365…fc1a).
  - All 349 leaves come from one source, `jtree/W28/U_L5`, which was built from `results/WAVE1/W28/U_L5/leaves.jsonl`.
  - That directory has only `leaves.jsonl` and `top.icnf`, with no `leaves.icnf` and no report. Its run was most likely still in progress at a033a13, so the leaf set is incomplete.
  - The `W33/W34/W35 U_L5-<k>` directories are separate cases.
  - U_L5 cannot be accepted until a complete leaf set exists, so its cover must be re-run on a later manifest.
- No SAT, REJECTED or TIMEOUT records.

## Notes
- The run was stopped by killing the process. Each record is written when its job finishes, so the in-flight jobs simply have no record.
- When I stopped it, my `pkill -f` pattern also killed my own waiting shell. I then killed the one remaining cake_lpr process by hand. Nothing was recorded for those jobs.
- Pushes to es7-cloud hit races with other machines a few times. Retrying with pull --rebase fixed each one.
  - Once, at 09:47, the fallback also pushed a copy to `claude/es7-v3a-v09`. The same commit then reached es7-cloud, so that branch is stale and has nothing extra.
