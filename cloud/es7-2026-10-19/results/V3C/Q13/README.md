# V3C Q13: shard 13 of 16

Tools (see tools.txt):
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: s VERIFIED UNSAT)
- F regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- input commit 71bcca7, verify/v3 at commit bdf319c

Inputs (see inputs.txt):
- worklist.jsonl sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (both match)
- cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (match); all 12380 work-list (case, lits) pairs occur in it (PASS)

Run: v3_check.py --shard 13 --nshards 16 --skip-covers --jobs 4 --cap 1800, about 14:22 to 16:00 UTC on 2026-10-20.
The shard has 773 leaves (2 covers skipped because of --skip-covers).

Verdicts (out.jsonl, 773 records, one per leaf):
- VERIFIED 773 (every one has cake_lpr "s VERIFIED UNSAT")
- REJECTED 0, SAT 0, TIMEOUT 0
- unchecked leaves: 0
- no rechecks were needed (no REJECTED with an empty cake_lpr field)

Times (seconds, over 773 leaves):
- solve: sum 17795.4, median 12.5, max 357.46
- check: sum 3539.7, median 3.08, max 25.74
