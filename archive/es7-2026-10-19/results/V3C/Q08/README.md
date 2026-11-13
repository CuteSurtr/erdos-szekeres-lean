# V3C Q08: shard 8 of 16

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F = /opt/work/F.cnf regenerated from source, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit 71bcca7456f44fb27385fa0e0f8b2ac1c4c2a42c; verify/v3 at bdf319cfb8b20bfacc951a0d6032ceeda85b8bf5.
- worklist.jsonl sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches).
- Cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (matches); all 12380 work-list (case, lits) pairs occur in it. Details in inputs.txt.
- Run: `v3_check.py --shard 8 --nshards 16 --skip-covers --jobs 4 --cap 1800`, 14:02 to about 15:10 UTC.

## Result
- Leaves in shard: 774. Records: 774 (one per leaf).
- VERIFIED 774, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0.
- No REJECTED leaf with an empty cake_lpr field, so step 4 had nothing to re-check.
- Solve time: sum 13539.8 s, median 9.715 s, max 297.01 s.
- Check time (cake_lpr): sum 3222.5 s, median 2.99 s, max 23.04 s.

No SAT, REJECTED or TIMEOUT leaves.
