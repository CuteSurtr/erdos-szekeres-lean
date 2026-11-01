# V3C Q11 (shard 11 of 16)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example prints `s VERIFIED UNSAT`). Both built from source.
- F = /opt/work/F.cnf regenerated with gen_etv.py + mirgen.py: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit 71bcca7; verify/v3 at commit bdf319c.
- Work list sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches).
- Cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (matches); all 12380 work-list (case, lits) pairs occur in it. PASS.

## Result

Run: `v3_check.py --shard 11 --nshards 16 --skip-covers --jobs 4 --cap 1800`, finished in full (14:01-15:27 UTC).

| verdict | count |
|---|---|
| VERIFIED | 774 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

All 774 leaves of the shard (idx % 16 == 11) have `cake_lpr` = `s VERIFIED UNSAT`. No rechecks were needed (no REJECTED leaf with empty cake_lpr field).

Times (seconds): solve sum 14989.5, median 10.4, max 376.6; check sum 3084.4, median 2.8, max 25.6.

Files: env.txt, tools.txt, inputs.txt, out.jsonl (774 records), run.log.
