# V3A V00 — first pass, shard 0 of 16, sub-case (ii) acceptance check

Run 2026-10-20 09:05–10:56 UTC on one 4-core VM (env.txt), `--jobs 4 --cap 1800`. Stopped at the time budget.

## Tools (tools.txt)
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); bundled `example.cnf example.lpr` prints `s VERIFIED UNSAT`; an empty proof is refused.
- F regenerated (gen_etv.py 33 7 7 7 --mirror; mirgen.py --interior --yflip-unit): sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d — matches.

## Inputs (inputs.txt)
- input commit a033a13; verify/v3 scripts from commit 7c6d70c (worktree /opt/v3src).
- v3_jsonl_leaves.py: dirs 72, leaf lines 17942, skipped records 47.
- v3_manifest.py: leaves 17989, cases with leaves 100, problems 0 — same as the other machine.
- M.jsonl sha256 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e (17989 records); C.jsonl sha256 8724fba58ba65d45c331522be734f781199a55e7abaaec42fe0e60a77f89b82b.
- Mr.jsonl: 40 ACCEPTED cases of results/V3T/accepted.tsv removed (357 records), idx renumbered: n = 17632 leaves in 60 cases, sha256 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def (script: mkmr.py).
- Shard 0: 1102 leaves (idx ≡ 0 mod 16) and 4 covers.

## Results (out.jsonl, summary.txt)
- Leaves: **1064 VERIFIED**, 0 REJECTED, 0 SAT, 0 TIMEOUT. Every VERIFIED record matches its manifest leaf by idx, case and lits.
- **38 leaves unchecked** (stopped at the time budget): 16 of U_L5, 22 of U_L8. The second pass picks them up.
- Covers: 1 VERIFIED (U10_L, 437 leaves), 3 NOT_COVERED (CaDiCaL rc 10 on the cover CNF):
  - U_L2-14 (82 leaves; sources results/WAVE1/W34/U_L2-14 + jtree)
  - U3_L2 (40 leaves; sources results/WAVE1/W33/U3_L2 + jtree)
  - U7_L (63 leaves; source jtree/W26/U7_L only, from leaves.jsonl)
  At a033a13 these wave directories were still running: W33/U3_L2 and W34/U_L2-14 contain open.icnf, and W26/U7_L has no leaves.icnf yet. So NOT_COVERED means "the wave had not finished these cases at the input commit", not a failure of any leaf.
- Leaf solve time: sum 21533.9 s, median 16.23 s, max 265.04 s. cake_lpr check time: sum 4328.6 s, median 3.13 s, max 25.82 s. Largest LRAT proof 218 MB (deleted after checking).
- Cover solve/check times are all under 0.1 s.

No CNF or proof files are committed.
