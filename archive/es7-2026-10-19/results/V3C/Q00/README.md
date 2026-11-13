# V3C Q00 (shard 0 of 16)

Third acceptance pass of mirror sub-case (ii), shard 0 of 16 of `results/V3C/worklist.jsonl`.

## Setup
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, as /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); its bundled example prints `s VERIFIED UNSAT`
- F regenerated from source: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- input commit 71bcca7; verify/v3 from commit bdf319c
- worklist.jsonl sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (both match)
- cross-check at fdd0393: Mfd.jsonl sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb, 47533 lines (both match); all 12380 work-list (case, lits) pairs occur in it. PASS. Details are in inputs.txt.

## Run
`v3_check.py --shard 0 --nshards 16 --skip-covers --jobs 4 --cap 1800` on 4 cores, 15 GB RAM, from 13:43 to about 14:58 UTC.

## Results
- leaves in shard: 774; checked: 774; unchecked: 0
- VERIFIED 774, REJECTED 0, SAT 0, TIMEOUT 0
- every record has cake_lpr = `s VERIFIED UNSAT`
- 40 distinct cases
- solve time: sum 13715.3 s, median 9.45 s, max 346.97 s
- check time: sum 3225.8 s, median 2.87 s, max 27.81 s
- No REJECTED leaves with an empty cake_lpr field, so step 4 had no rechecks to run.

The records are in out.jsonl.
