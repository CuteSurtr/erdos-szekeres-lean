# V3C Q01 (shard 1 of 16)

Shard finished: 774 of 774 work-list leaves checked, all VERIFIED.

## Setup
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical)
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); the bundled example prints `s VERIFIED UNSAT`
- F.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- Input commit 71bcca7456f44fb27385fa0e0f8b2ac1c4c2a42c; verify/v3 at bdf319cfb8b20bfacc951a0d6032ceeda85b8bf5
- worklist.jsonl sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches)
- Cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (matches); all 12380 work-list (case, lits) pairs occur in it. Details in inputs.txt.

## Run
`v3_check.py --shard 1 --nshards 16 --skip-covers --jobs 4 --cap 1800`, 13:50 to about 14:58 UTC on 2026-10-20.

| verdict | count |
|---|---|
| VERIFIED | 774 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

Every record has rc 20 and cake_lpr `s VERIFIED UNSAT`. No leaf had an empty cake_lpr field, so step 4 had no rechecks to do.

| time (s) | sum | median | max |
|---|---|---|---|
| solve | 12935.39 | 9.76 | 296.06 |
| check | 3291.76 | 3.065 | 23.54 |

No SAT, REJECTED or TIMEOUT leaves.
