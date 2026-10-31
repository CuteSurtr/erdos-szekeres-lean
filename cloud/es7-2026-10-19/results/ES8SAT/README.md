# ES8SAT: one-point extensions of 64-point sets with no convex octagon (2026-10-31)

**Question.** Is there a 65-point set in general position with no 8 points in convex position? That would disprove
ES(8) = 65. Every 64-point subset of such a set would be an octagon-free 64-point set to which one point can be added.

**Method.** `walk.py` walks through octagon-free 64-point sets, starting from `witness8.txt` (the 64-point
construction behind ES(8) ≥ 65). It moves one point at a time, accepting only positions where the moved point lies in no
convex octagon (`sat test`). The Mac's walkers `v2w*` and `v3w*` start instead from the octagon-free 64-point sets
`v8_2` and `v8_3` of `experiments/es8-lower-bound-search-2026-10-11/anneal/` on the main branch (copied to `LOCAL/start_v8_*.txt`;
exactly checked: no collinear triple, largest convex subset 7). After every 10 accepted moves, `sat.c` (copied unchanged from
`experiments/es8-lower-bound-search-2026-10-11/saturation/` on the main branch, where it is cross-checked by `verify.c`)
decides exactly whether some point can be added. It tests one symbolic point in every face of the arrangement of the 2,016
lines through pairs of points and counts the faces reached against Euler's formula. `bad > 0` would mean an addable
point, that is, a 65-point octagon-free set. All coordinates stay below 2^27, the tool's exact-arithmetic bound (moved points stay below 2^26).

## Result

- 5169 exact saturation tests: 2149 on 8 cloud machines (4 walkers each, `TASK.md`) and 3020 on a Mac.
- Faces per test: 1,909,869–1,912,104; every face was reached in every test (faces reached = Euler count).
- **No test found an addable point**: `bad` is 0 in every test. Lines with bad > 0 or an incomplete face count: 0.
- CPU seconds per test: 20–94.

This is a finite search, not a proof of anything about ES(8). The sets tested are octagon-free 64-point sets reached
from the standard construction by single-point moves (consecutive tests differ by 10 accepted moves, so neighbouring sets
may share most of their structure). A 65-point octagon-free set, if one exists, need not contain any of them.

Per walker (log: tests): w1 (E00): 64, w2 (E00): 64, w3 (E00): 64, w4 (E00): 64, w101 (E01): 74, w102 (E01): 74, w103 (E01): 73, w104 (E01): 74, w201 (E02): 73, w202 (E02): 73, w203 (E02): 73, w204 (E02): 74, w301 (E03): 64, w302 (E03): 64, w303 (E03): 64, w304 (E03): 64, w401 (E04): 64, w402 (E04): 64, w403 (E04): 64, w404 (E04): 64, w501 (E05): 63, w502 (E05): 64, w503 (E05): 64, w504 (E05): 64, w601 (E06): 66, w602 (E06): 66, w603 (E06): 66, w604 (E06): 66, w701 (E07): 69, w702 (E07): 68, w703 (E07): 68, w704 (E07): 69, v2w21 (LOCAL): 653, v2w22 (LOCAL): 639, v3w31 (LOCAL): 662, v3w32 (LOCAL): 661, w1 (LOCAL): 198, w2 (LOCAL): 206, w3 (LOCAL): 1.

## Files

`TASK.md` (cloud task), `walk.py`, `sat.c`, `witness8.txt`, `MANIFEST.sha256`; per cloud machine `E00`–`E07/`
(`env.txt` with the control run on `witness8.txt`, `run.sh`, `w*.log`, `README.md`); `LOCAL/`: the Mac's walk logs and
the last set of each Mac walker.
