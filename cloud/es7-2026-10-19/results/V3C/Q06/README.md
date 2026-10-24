# V3C Q06: shard 6 of 16

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). Details in `tools.txt`.
- F = /opt/work/F.cnf regenerated with gen_etv.py + mirgen.py: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit 71bcca7; verify/v3 at bdf319c.
- Work list `results/V3C/worklist.jsonl`: sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (match).
- Cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (match); all 12380 work-list (case, lits) records occur in it. PASS. See `inputs.txt`.

## Result

Run: `v3_check.py --shard 6 --nshards 16 --skip-covers --jobs 4 --cap 1800`, 13:57 to about 15:12 UTC, finished.

| verdict | leaves |
|---|---|
| VERIFIED | 774 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Unchecked leaves of this shard: 0 of 774. Every record has rc 20 and cake_lpr `s VERIFIED UNSAT`. No rechecks were needed (no REJECTED record with an empty cake_lpr field).

Times (seconds): solve sum 13933.4, median 9.86, max 323.15; check sum 3351.9, median 3.22, max 27.99.

`out.jsonl` holds all 774 records.
