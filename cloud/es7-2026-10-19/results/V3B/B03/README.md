# V3B B03: shard 3 of 16, second acceptance pass of mirror sub-case (ii)

Run from 2026-10-20 11:25 to 13:55 UTC on 4 cores with 15 GB RAM.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical)
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (/opt/bin/cake_lpr). Its bundled example prints `s VERIFIED UNSAT`.
- F.cnf, regenerated from scratch: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- Input commit Z = 066eaa9; verify/v3 at bdf319c
- v3_manifest: leaves 35153, cases with leaves 253, problems 0. M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
- VERIFIED keys from V3T and V3A (21 JSONL files; no V3B out.jsonl at Z): 10121. Mt.jsonl has n = 25032 records, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7. These values match the inputs.txt of B04, B09 and B13.
- Shard 3 of 16 (idx % 16 == 3): 1565 leaves. Run with --skip-covers, so no covers were checked.

See tools.txt, inputs.txt and mkMt.py (the step-3 script).

## Results (out.jsonl)
| verdict | count |
|---|---|
| VERIFIED | 1565 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

- Unchecked leaves in this shard: 0. The run finished on its own.
- Every record has rc 20 and cake_lpr `s VERIFIED UNSAT`. No REJECTED records with an empty cake_lpr field came up, so step 5 needed no rechecks.
- Solve time (CaDiCaL): sum 28897.9 s, median 10.51 s, max 348.85 s
- Check time (cake_lpr): sum 6432.2 s, median 2.99 s, max 24.61 s
- Largest proof: 250 MB (text LRAT; not committed)

There were no SAT, REJECTED or TIMEOUT leaves.
