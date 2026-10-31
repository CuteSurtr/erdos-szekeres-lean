# V3C Q04 (shard 4 of 16)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its bundled example prints `s VERIFIED UNSAT`). Binary hashes are in tools.txt.
- F regenerated from source: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit 71bcca7; verify/v3 at bdf319c.
- worklist.jsonl sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches).
- Cross-check at fdd0393: Mfd.jsonl has 47533 lines, sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb (matches), 0 problems. All 12380 work-list (case, lits) records appear in it. Details are in inputs.txt.
- Run: v3_check.py --shard 4 --nshards 16 --skip-covers --jobs 4 --cap 1800, 13:57 to about 15:05 UTC.

## Results
- Leaves in shard: 774. Checked: 774. Unchecked: 0.
- VERIFIED 774, REJECTED 0, SAT 0, TIMEOUT 0. Every cake_lpr field is `s VERIFIED UNSAT`, so no rechecks were needed (step 4).
- Solve time: sum 13358.9 s, median 10.11 s, max 294.25 s.
- Check time: sum 3195.2 s, median 3.01 s, max 22.89 s.
- No SAT, REJECTED or TIMEOUT leaves.
