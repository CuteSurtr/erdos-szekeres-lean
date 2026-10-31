# V3C Q03: shard 3 of 16

Third acceptance pass of mirror sub-case (ii), task `results/V3C/TASK.md` at 71bcca7.

- Tools (built from source, see `tools.txt`): CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F regenerated: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = 71bcca7; verify/v3 used from commit bdf319c.
- Work list `results/V3C/worklist.jsonl`: sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches).
- Cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (matches); all 12380 work-list (case, lits) occur in it.

## Result

Shard 3 of 16 has 774 leaves; all 774 checked (0 unchecked), each output record matched against the shard's work-list records (none missing, none extra).

| verdict | count |
|---|---|
| VERIFIED (cake_lpr `s VERIFIED UNSAT`) | 774 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

No REJECTED leaf with an empty `cake_lpr` field, so step 4 (rechecks) was not needed.

Times (seconds): solve sum 16551.0, median 10.91, max 320.33; check sum 3514.8, median 3.32, max 26.74.

Run: `v3_check.py --shard 3 --nshards 16 --skip-covers --jobs 4 --cap 1800`, 13:50 to about 15:20 UTC 2026-10-20, 4 cores, 15 GB RAM. Output: `out.jsonl`.
