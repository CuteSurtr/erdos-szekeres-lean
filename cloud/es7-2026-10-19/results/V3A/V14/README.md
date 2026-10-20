# V3A V14: first pass, shard 14 of 16, from-scratch acceptance check of mirror sub-case (ii)

Run 2026-10-20, 09:06Z to 10:47Z (stopped at the time limit), 4 cores, 15 GB RAM (env.txt).

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr commit
  a36874a8b750b43fe4b385b8ddbf5b033e46a3fa. Both built from source. The bundled example prints
  `s VERIFIED UNSAT` (tools.txt).
- F = /opt/work/F.cnf, regenerated with gen_etv.py and mirgen.py: sha256
  69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches), `p cnf 47002 515121`.
- verify/v3 scripts from commit 7c6d70c; inputs from commit a033a13.
- v3_jsonl_leaves.py: dirs 72, leaf lines 17942, skipped records 47.
- v3_manifest.py: leaves 17989, cases with leaves 100, problems 0 (same as the other machine).
  - M.jsonl sha256 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e
  - C.jsonl sha256 8724fba58ba65d45c331522be734f781199a55e7abaaec42fe0e60a77f89b82b
- Mr.jsonl is M.jsonl without the 40 cases marked ACCEPTED in V3T/accepted.tsv: n = 17632 leaves,
  60 cases, sha256 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def.

## Run
`v3_check.py --shard 14 --nshards 16 --jobs 4 --cap 1800`. OUT was kept at /opt/work/out/out.jsonl
and copied to out.jsonl here at each commit.

## Results (out.jsonl, 826 records)
- My shard has 1102 leaves (idx ≡ 14 mod 16).
  - Leaf verdicts: VERIFIED 823, REJECTED 0, SAT 0, TIMEOUT 0.
  - Still unchecked: 279. The second pass picks them up.
- My shard has 3 covers: U3_L10, U6_L2 and U_L2-11. All 3 are VERIFIED; none are NOT_COVERED.
- Leaf solve time: sum 20431.7 s, median 17.90 s, max 330.08 s.
- Leaf check time (cake_lpr): sum 3545.9 s, median 3.14 s, max 25.29 s.
- Largest proof: 231 MB of text LRAT.
- No SAT, REJECTED, TIMEOUT or NOT_COVERED records. Every verdict is cake_lpr `s VERIFIED UNSAT`.
- Three CaDiCaL jobs were killed at the stop (leaves 13182, 13214 and 13230). No records were
  written for them, so they count as unchecked.
