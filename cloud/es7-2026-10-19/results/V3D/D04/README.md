# V3D D04: shard 4 of 24

Tools (built from source; see tools.txt):
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`)

Inputs:
- F regenerated: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- input commit Z = a71d30d5; verify/v3 from commit bdf319c
- work list results/V3D/worklist.jsonl: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (both match)
- cross-check at 3e4dbaae3: rebuilt manifest Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (matches); all 22682 work-list (case, lits) occur in it. Details in inputs.txt.

Run: `v3_check.py --shard 4 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:27 to about 16:55 UTC, run to completion.

Results (out.jsonl, 945 records = all 945 leaves of the shard):
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0
- unchecked leaves of this shard: 0
- no REJECTED leaf with an empty cake_lpr field, so no rechecks (step 4) were needed
- leaves by case: U_L2 516, U3_L 177, U_L7 119, U_L6 84, U4_L 32, U_L5 17
- solve time: sum 16417.6 s, median 10.56 s, max 272.79 s
- check time (cake_lpr): sum 3588.1 s, median 2.92 s, max 26.49 s
