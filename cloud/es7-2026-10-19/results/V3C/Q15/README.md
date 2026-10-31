# V3C Q15: shard 15 of 16

Leaves of `results/V3C/worklist.jsonl` with idx % 16 == 15, checked with `verify/v3/v3_check.py --skip-covers --jobs 4 --cap 1800`.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa; its bundled example prints `s VERIFIED UNSAT`
- F.cnf regenerated from source, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- input commit 71bcca7; verify/v3 commit bdf319c
- worklist.jsonl sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches)
- cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (matches); all 12380 work-list (case, lits) occur in it. PASS. Details are in inputs.txt.

## Results
- leaves in shard: 773 (40 cases)
- VERIFIED 773, REJECTED 0, SAT 0, TIMEOUT 0
- unchecked: 0
- leaves with an empty cake_lpr field (step 4 rechecks): none
- solve time: sum 16458.9 s (4.57 h), median 11.57 s, max 351.90 s
- check time: sum 3876.9 s (1.08 h), median 3.41 s, max 29.41 s
- wall time: 14:23 to 15:49 UTC on 2026-10-20 (about 1 h 26 min, 4 cores)

No SAT, REJECTED or TIMEOUT leaves. Every record in out.jsonl has `cake_lpr` = `s VERIFIED UNSAT`.
