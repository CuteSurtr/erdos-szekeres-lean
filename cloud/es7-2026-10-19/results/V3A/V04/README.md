# V3A V04: first pass, machine 4 of 16 (shard 4 / 16), mirror sub-case (ii)

Run 2026-10-20, 09:05–10:48 UTC, on 4 cores, 15 GB RAM (`env.txt`).

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 → /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`) → /opt/bin/cake_lpr. The bundled example prints `s VERIFIED UNSAT`. Binary sha256 values are in `tools.txt`.
- F regenerated (gen_etv.py 33 7 7 7 --mirror; mirgen.py --interior --yflip-unit). sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d. This matches.
- Input commit a033a13; verify/v3 scripts at commit 7c6d70c.
- v3_jsonl_leaves: 72 dirs, 17942 leaf lines, 47 skipped records.
- v3_manifest: 17,989 leaves in 100 cases with 0 problems. This matches the other machine.
  - M.jsonl sha256 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e
  - C.jsonl sha256 8724fba58ba65d45c331522be734f781199a55e7abaaec42fe0e60a77f89b82b
- Mr.jsonl drops the 40 ACCEPTED cases of V3T/accepted.tsv (357 records), keeps the order and renumbers idx. It has n = 17,632 records in 60 cases, sha256 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def. This equals the Mr.jsonl sha256 another V3A machine committed. The script is `mkmr.py`.

## Results (`out.jsonl`, `summary.txt`)
- Shard 4/16 holds 1102 leaves and 4 covers (U10_L8, U4_L14, U7_L6, U_L2-5).
- Leaf verdicts: VERIFIED 947, REJECTED 0, SAT 0, TIMEOUT 0.
- Cover verdicts: VERIFIED 4 (U10_L8 has the empty cube as its leaf), NOT_COVERED 0, others 0.
- 155 leaves are still unchecked: no record, because the run was stopped at 10:48. They are left for the second pass.
- Leaf solve time: sum 20306.5 s, median 18.46 s, max 379.54 s.
- Leaf check time (cake_lpr): sum 3828.4 s, median 2.93 s, max 28.8 s.
- No SAT, REJECTED, TIMEOUT or NOT_COVERED record.

## Notes
- OUT was kept at /opt/work/out/out.jsonl, outside the checkout (RISK-7), and copied here at each commit.
- The run was stopped with SIGTERM to v3_check.py and its solver/checker children. The stop left no partial or REJECTED record: all 951 lines parse, and the file ends with a newline.
