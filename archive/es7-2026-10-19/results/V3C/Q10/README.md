# V3C Q10: shard 10 of 16

Third acceptance pass of mirror sub-case (ii), task `results/V3C/TASK.md` at commit 71bcca7. Values: V = Q10, i = 10, N = 16, H = 2, Z = 71bcca7.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source as /opt/bin/cadical.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its bundled example prints `s VERIFIED UNSAT`.
- F.cnf was regenerated with gen_etv.py and mirgen.py: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit: 71bcca7. verify/v3 commit: bdf319c.
- Work list `results/V3C/worklist.jsonl`: sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches).
- Cross-check at fdd0393: v3_manifest gave Mfd.jsonl with sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb and 47533 lines (matches). All 12380 work-list (case, lits) pairs occur in it (0 missing). PASS.

Details are in `tools.txt` and `inputs.txt`.

## Results (`out.jsonl`)
Command: `v3_check.py --shard 10 --nshards 16 --skip-covers --jobs 4 --cap 1800`, run 14:02 to about 15:25 UTC on 2026-10-20.

- Leaves in shard: 774 (the work-list idx values with idx % 16 == 10). All 774 have a record, and none are unchecked.
- VERIFIED: 774. REJECTED: 0. SAT: 0. TIMEOUT: 0. Every record has cake_lpr = `s VERIFIED UNSAT`.
- Solve time: 16544.4 s in total, median 11.86 s, max 284.01 s.
- Check time: 3231.0 s in total, median 2.99 s, max 24.8 s.
- No REJECTED leaf with an empty cake_lpr field, so step 4 had nothing to recheck.
