# V3C Q12: shard 12 of 16 (third acceptance pass, mirror sub-case (ii))

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). Details in `tools.txt`.
- F regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit 71bcca7; verify/v3 at bdf319c.
- Work list `results/V3C/worklist.jsonl`: sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (match).
- Cross-check at fdd0393: rebuilt manifest Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (match); all 12380 work-list (case, lits) pairs occur in it. PASS.

## Result

Command: `v3_check.py --shard 12 --nshards 16 --skip-covers --jobs 4 --cap 1800`, run 14:21Z to 15:31Z on 2026-10-20.

| verdict | leaves |
|---|---|
| VERIFIED | 773 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

All 773 leaves of the shard (idx = 12 mod 16) were checked; each record's key, case and lits match the work list, and every cake_lpr field is `s VERIFIED UNSAT`. No re-checks were needed (no REJECTED leaf).

Times (seconds, over 773 leaves):

| | sum | median | max |
|---|---|---|---|
| solve | 13428.8 | 10.11 | 217.31 |
| check | 3198.9 | 3.08 | 21.66 |

Largest proof: 176887826 bytes. Records: `out.jsonl`.
