# V3B B12: shard 12 of 16, second acceptance pass of mirror sub-case (ii)

Result: all 1564 leaves in shard 12 VERIFIED (cake_lpr printed `s VERIFIED UNSAT` for each one). None are SAT, REJECTED or TIMEOUT, and none are left unchecked.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source as /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`), as /opt/bin/cake_lpr; its bundled example prints `s VERIFIED UNSAT`
- verify/v3 taken from commit bdf319c; input commit Z = 066eaa9
- F.cnf, regenerated from scratch: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- M.jsonl: 35153 leaves, 253 cases with leaves, 0 problems; sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
- 10121 VERIFIED keys from V3T and V3A (there were no V3B out.jsonl files at Z)
- Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7 (the same as B04 and B13)
- Counts are in inputs.txt, tools in tools.txt. mkmt.py is the step-3 filter.

## Run
`v3_check.py --shard 12 --nshards 16 --skip-covers --jobs 4 --cap 1800`. It ran from 11:28 to 13:58 UTC on 4 cores with 15 GB RAM.

| verdict | count |
|---|---|
| VERIFIED | 1564 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

- Solve time: sum 28978.4 s, median 10.54 s, max 328.68 s
- Check time: sum 6422.4 s, median 3.03 s, max 34.65 s
- Largest proof: 262 MB
- No REJECTED leaf had an empty cake_lpr field, so step 5 had nothing to re-check.
- out.jsonl has one record for each Mt idx with idx % 16 == 12: none missing, none extra.
