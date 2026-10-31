# V3C Q02 (shard 2 of 16)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its bundled example prints `s VERIFIED UNSAT`). See tools.txt.
- F.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit 71bcca7; verify/v3 at commit bdf319c.
- worklist.jsonl sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches).
- Cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (matches). All 12380 work-list (case, lits) occur in it. See inputs.txt.

## Results (out.jsonl)

- Shard leaves: 774. VERIFIED 774, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0.
- Every record has cake_lpr = `s VERIFIED UNSAT`, so step 4 had no re-checks.
- Solve time: sum 15024.3 s, median 11.04 s, max 290.71 s.
- Check time: sum 3366.3 s, median 3.23 s, max 21.87 s.
- Run: v3_check.py --jobs 4 --cap 1800 --skip-covers, 13:50 to about 15:15 UTC on 2026-10-20, on 4 cores with 15 GB RAM.

There were no SAT, REJECTED or TIMEOUT leaves.
