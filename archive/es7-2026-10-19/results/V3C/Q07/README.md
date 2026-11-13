# V3C Q07 (shard 7 of 16)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). Details in tools.txt.
- F = m33k7int.sub.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Inputs at commit 71bcca7; verify/v3 at commit bdf319c.
- Work list sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches).
- Cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (matches); all 12380 work-list (case, lits) occur in it. Details in inputs.txt.

## Result

v3_check.py --shard 7 --nshards 16 --skip-covers --jobs 4 --cap 1800: 774 leaves in the shard, all 774 checked.

| verdict | count |
|---|---|
| VERIFIED | 774 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

Every record has cake_lpr output `s VERIFIED UNSAT`. No REJECTED leaf with an empty cake_lpr field, so no rechecks were needed.

Times (seconds, 774 leaves):
- solve: sum 15284.6, median 11.25, max 288.59
- check: sum 3444.79, median 3.29, max 25.49

Run wall time about 1h15m (13:58 to 15:13 UTC, 2026-10-20). Output: out.jsonl.
