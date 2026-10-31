# C3W6 P28: shard 28 of 44 of W6.tsv (93 units), cap 900

Task: `results/C3W6/TASK.md` at c5260b44, with V = P28, LIST = W6.tsv, j = 28, N = 44, H = 4.5.
Start 2026-10-25 05:31:25 UTC, END 09:46:25 UTC. All three lanes had finished by 07:57:44 UTC, so nothing was killed at END.

## Tools and base check

- C3U2 tools: worktree of cad4e050 (cad4e050d778aa37c9ea23afcbe704c94db3e890) at /opt/c3u2, used unmodified; `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check passed: on {1},{-1}, `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches; also the `base_sha256` of every record).
- Details are in `tools.txt`.

## Run

Units are the W6.tsv rows with row ≡ 28 (mod 44) (`units.tsv`, 93 units, all six-bit σ-cubes). There were 3 lanes (`lane0.sh` to `lane2.sh`), and lane k took the positions ≡ k (mod 3). Each unit was run with
`close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
No records were seeded. `out.jsonl` holds lanes 0, 1 and 2 in that order: 93 solve records and no split records.

## Result

- **All 93 units certified at cap 900.** Every record has status UNSATISFIABLE, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT` and `certified: true`.
- 0 timed out at 900, 0 not reached, 0 split records, 0 unsplittable. Every close_tree run ended with `open_frontier` 0.
- No SAT, no proof rejection, no cake_lpr `none`, so no rechecks were needed (no `recheck.jsonl`). No memory problem: at most about 8 GB of 15 GB was in use.
- No unit ended early without a certificate. 17 units were solved in under 72 s, and all of them were certified.

Solve-time distribution of the 93 certified units (s): min 15.6, Q1 92.9, median 237.9, Q3 343.7, p90 418.7, max 503.5. **34 were certified above 300 s**, all of them H3/two.
Check time: min 19.4, median 39.8, max 65.4 s. In total that is 21,466 s of solving and 3,735 s of checking. The largest proof was 596 MB (deleted, not committed).

Totals per stratum (units / certified / median solve s / max solve s / certified above 300 s):

| stratum | units | certified | median | max | >300 s |
|---|---|---|---|---|---|
| H3/two | 76 | 76 | 275.7 | 503.5 | 34 |
| H6(1,1)/one | 1 | 1 | 241.2 | 241.2 | 0 |
| H6(2,1)/one | 4 | 4 | 280.8 | 282.4 | 0 |
| H6(3,1)/one | 2 | 2 | 195.2 | 195.2 | 0 |
| H6(4,0)/one | 2 | 2 | 58.4 | 58.4 | 0 |
| H6(5,0)/one | 3 | 3 | 60.4 | 101.1 | 0 |
| H6(5,1)/one | 3 | 3 | 159.5 | 237.9 | 0 |
| H6(5,1)/two | 2 | 2 | 41.8 | 41.8 | 0 |
| total | 93 | 93 | 237.9 | 503.5 | 34 |

Totals per prior:

| prior | units | certified | median | max | >300 s |
|---|---|---|---|---|---|
| timeout300 | 26 | 26 | 340.4 | 503.5 | 15 |
| presplit | 57 | 57 | 137.8 | 480.8 | 15 |
| never_ran | 10 | 10 | 269.0 | 475.9 | 4 |

## Per unit

| pos | row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 0 | 28 | `0s0_1s0-2s0__3s0-4s0-5s1-6s1-7s1-8s1` | H3/two | presplit | 0 | certified | 25.0 | 35.1 |
| 1 | 72 | `0s0_1s0-2s0__3s1-4s1-5s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 37.7 | 37.6 |
| 2 | 116 | `0s0_1s0-2s1__3s1-4s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 364.8 | 65.4 |
| 3 | 160 | `0s0_1s0-4s1__2s0-3s0-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 286.8 | 53.1 |
| 4 | 204 | `0s0_1s0-4s1__2s1-3s1-5s0-6s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 323.6 | 54.8 |
| 5 | 248 | `0s0_1s0-5s1__2s1-3s1-4s1-6s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 325.6 | 61.2 |
| 6 | 292 | `0s0_1s0-7s0__2s1-3s1-4s0-5s1-6s0-8s0` | H3/two | timeout300 | 0 | certified | 148.7 | 46.1 |
| 7 | 336 | `0s0_1s1-2s0__3s1-4s0-5s0-6s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 371.2 | 59.9 |
| 8 | 380 | `0s0_1s1-4s0__2s1-3s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 2 | certified | 341.7 | 49.4 |
| 9 | 424 | `0s0_1s1-5s0__2s1-3s1-4s0-6s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 275.7 | 43.2 |
| 10 | 468 | `0s0_1s1-5s1__2s1-3s0-4s0-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 137.8 | 36.7 |
| 11 | 512 | `0s0_1s1-7s1__2s0-3s1-4s1-5s0-6s1-8s1` | H3/two | timeout300 | 2 | certified | 367.5 | 50.5 |
| 12 | 556 | `0s0_1s1-8s0__2s0-3s0-4s1-5s0-6s0-7s1` | H3/two | presplit | 0 | certified | 76.7 | 42.3 |
| 13 | 600 | `0s0_1s1-8s0__2s1-3s1-4s0-5s1-6s0-7s1` | H3/two | presplit | 1 | certified | 106.3 | 50.9 |
| 14 | 644 | `0s0_1s1-8s1__2s1-3s1-4s1-5s1-6s0-7s1` | H3/two | timeout300 | 2 | certified | 503.5 | 58.0 |
| 15 | 688 | `0s0_1s1-9s1__2s1-3s1-4s0-5s1-6s1-7s0` | H3/two | never_ran | 0 | certified | 475.9 | 58.0 |
| 16 | 732 | `0s0_2s0-3s1__1s1-4s0-5s0-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 376.6 | 63.0 |
| 17 | 776 | `0s0_2s0-4s1__1s0-3s0-5s1-6s1-7s1-8s0` | H3/two | presplit | 2 | certified | 371.7 | 62.0 |
| 18 | 820 | `0s0_2s0-4s1__1s1-3s1-5s1-6s0-7s1-8s0` | H3/two | presplit | 0 | certified | 460.4 | 56.3 |
| 19 | 864 | `0s0_2s0-5s0__1s1-3s0-4s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 92.9 | 38.7 |
| 20 | 908 | `0s0_2s0-5s1__1s0-3s1-4s1-6s0-7s0-8s1` | H3/two | timeout300 | 2 | certified | 370.1 | 61.8 |
| 21 | 952 | `0s0_2s0-6s1__1s0-3s0-4s0-5s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 268.0 | 46.4 |
| 22 | 996 | `0s0_2s0-6s1__1s1-3s1-4s0-5s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 412.4 | 52.3 |
| 23 | 1040 | `0s0_2s0-7s0__1s0-3s1-4s1-5s1-6s1-8s1` | H3/two | presplit | 2 | certified | 89.0 | 29.4 |
| 24 | 1084 | `0s0_2s0-7s1__1s0-3s0-4s1-5s0-6s1-8s1` | H3/two | presplit | 0 | certified | 233.4 | 38.1 |
| 25 | 1128 | `0s0_2s0-7s1__1s1-3s1-4s0-5s1-6s1-8s1` | H3/two | presplit | 1 | certified | 302.3 | 50.4 |
| 26 | 1172 | `0s0_2s0-8s0__1s1-3s1-4s0-5s1-6s0-7s1` | H3/two | presplit | 2 | certified | 184.7 | 33.9 |
| 27 | 1216 | `0s0_2s1-3s0__1s1-4s0-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 378.1 | 42.5 |
| 28 | 1260 | `0s0_2s1-3s1__1s0-4s0-5s1-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 61.0 | 26.0 |
| 29 | 1304 | `0s0_2s1-3s1__1s1-4s1-5s1-6s0-7s1-8s0` | H3/two | presplit | 2 | certified | 42.4 | 20.8 |
| 30 | 1348 | `0s0_2s1-4s0__1s1-3s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 418.7 | 47.5 |
| 31 | 1392 | `0s0_2s1-5s0__1s0-3s1-4s1-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 291.0 | 40.1 |
| 32 | 1436 | `0s0_2s1-6s0__1s0-3s0-4s0-5s1-7s0-8s0` | H3/two | presplit | 2 | certified | 193.0 | 42.9 |
| 33 | 1480 | `0s0_2s1-6s0__1s1-3s1-4s0-5s0-7s0-8s0` | H3/two | presplit | 0 | certified | 170.2 | 33.4 |
| 34 | 1524 | `0s0_2s1-6s1__1s0-3s1-4s1-5s1-7s0-8s0` | H3/two | presplit | 1 | certified | 266.0 | 38.2 |
| 35 | 1568 | `0s0_2s1-7s0__1s0-3s0-4s1-5s1-6s1-8s0` | H3/two | timeout300 | 2 | certified | 259.8 | 41.1 |
| 36 | 1612 | `0s0_2s1-7s0__1s1-3s1-4s1-5s1-6s0-8s0` | H3/two | never_ran | 0 | certified | 269.0 | 39.7 |
| 37 | 1656 | `0s0_2s1-8s1__1s0-3s0-4s1-5s0-6s1-7s1` | H3/two | presplit | 1 | certified | 292.7 | 37.4 |
| 38 | 1700 | `0s0_2s1-8s1__1s1-3s1-4s0-5s1-6s1-7s1` | H3/two | presplit | 2 | certified | 480.8 | 46.5 |
| 39 | 1744 | `0s0_2s1-9s0__1s1-3s0-4s0-5s0-6s1-7s1` | H3/two | presplit | 0 | certified | 137.5 | 33.6 |
| 40 | 1788 | `0s0_3s0-4s1__1s0-2s0-5s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 217.0 | 37.4 |
| 41 | 1832 | `0s0_3s0-4s1__1s1-2s1-5s1-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 343.7 | 43.9 |
| 42 | 1876 | `0s0_3s0-5s0__1s1-2s0-4s0-6s1-7s1-8s1` | H3/two | presplit | 0 | certified | 64.0 | 27.6 |
| 43 | 1920 | `0s0_3s0-5s1__1s0-2s1-4s1-6s1-7s0-8s1` | H3/two | timeout300 | 1 | certified | 420.8 | 46.3 |
| 44 | 1964 | `0s0_3s0-6s0__1s0-2s0-4s1-5s0-7s0-8s1` | H3/two | presplit | 2 | certified | 39.7 | 19.4 |
| 45 | 2008 | `0s0_3s0-6s0__1s1-2s1-4s0-5s1-7s0-8s1` | H3/two | presplit | 0 | certified | 99.4 | 29.9 |
| 46 | 2052 | `0s0_3s0-6s1__1s1-2s0-4s0-5s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 271.0 | 38.5 |
| 47 | 2096 | `0s0_3s0-7s0__1s0-2s0-4s1-5s1-6s0-8s1` | H3/two | presplit | 2 | certified | 65.0 | 26.3 |
| 48 | 2140 | `0s0_3s0-7s0__1s1-2s1-4s1-5s0-6s0-8s1` | H3/two | presplit | 0 | certified | 160.4 | 31.6 |
| 49 | 2184 | `0s0_3s0-7s1__1s1-2s0-4s0-5s1-6s0-8s1` | H3/two | presplit | 1 | certified | 352.4 | 43.5 |
| 50 | 2228 | `0s0_3s0-8s0__1s1-2s0-4s0-5s1-6s1-7s1` | H3/two | presplit | 2 | certified | 89.2 | 25.5 |
| 51 | 2272 | `0s0_3s0-8s1__1s1-2s1-4s0-5s1-6s1-7s0` | H3/two | never_ran | 0 | certified | 216.7 | 52.8 |
| 52 | 2316 | `0s0_3s1-4s0__1s1-2s0-5s0-6s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 380.3 | 42.9 |
| 53 | 2360 | `0s0_3s1-4s1__1s0-2s1-5s0-6s0-7s0-8s0` | H3/two | presplit | 2 | certified | 78.6 | 27.4 |
| 54 | 2404 | `0s0_3s1-4s1__1s1-2s1-5s1-6s1-7s0-8s0` | H3/two | presplit | 0 | certified | 42.9 | 22.3 |
| 55 | 2448 | `0s0_3s1-5s0__1s1-2s0-4s1-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 334.9 | 42.4 |
| 56 | 2492 | `0s0_3s1-5s1__1s0-2s1-4s0-6s1-7s0-8s0` | H3/two | presplit | 2 | certified | 70.9 | 28.5 |
| 57 | 2536 | `0s0_3s1-6s0__1s1-2s0-4s1-5s1-7s0-8s1` | H3/two | timeout300 | 0 | certified | 439.0 | 46.5 |
| 58 | 2580 | `0s0_3s1-7s0__1s1-2s1-4s1-5s0-6s1-8s0` | H3/two | never_ran | 1 | certified | 317.8 | 39.8 |
| 59 | 2624 | `0s0_3s1-8s0__1s0-2s0-4s1-5s1-6s0-7s1` | H3/two | presplit | 2 | certified | 135.3 | 30.3 |
| 60 | 2668 | `0s0_3s1-8s0__1s1-2s1-4s1-5s0-6s0-7s1` | H3/two | presplit | 0 | certified | 210.1 | 34.4 |
| 61 | 2712 | `0s0_4s0-5s1__1s1-2s0-3s0-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 381.7 | 45.9 |
| 62 | 2756 | `0s0_4s0-6s1__1s0-2s1-3s0-5s0-7s0-8s1` | H3/two | presplit | 2 | certified | 338.0 | 44.3 |
| 63 | 2800 | `0s0_4s0-6s1__1s1-2s1-3s1-5s1-7s0-8s1` | H3/two | presplit | 0 | certified | 427.2 | 46.1 |
| 64 | 2844 | `0s0_4s0-7s0__1s1-2s0-3s1-5s0-6s0-8s1` | H3/two | presplit | 1 | certified | 89.3 | 43.0 |
| 65 | 2888 | `0s0_4s0-7s1__1s0-2s1-3s1-5s1-6s1-8s0` | H3/two | presplit | 2 | certified | 343.4 | 43.9 |
| 66 | 2932 | `0s0_4s1-5s0__1s0-2s0-3s1-6s0-7s1-8s0` | H3/two | never_ran | 0 | certified | 397.1 | 47.4 |
| 67 | 2976 | `0s0_4s1-5s0__1s1-2s1-3s0-6s1-7s1-8s0` | H3/two | never_ran | 1 | certified | 443.6 | 48.6 |
| 68 | 3020 | `0s0_4s1-6s0__1s0-2s1-3s1-5s0-7s0-8s1` | H3/two | presplit | 2 | certified | 430.9 | 48.6 |
| 69 | 3064 | `0s0_4s1-6s1__1s0-2s0-3s0-5s1-7s0-8s1` | H3/two | presplit | 0 | certified | 82.3 | 28.0 |
| 70 | 3108 | `0s0_4s1-6s1__1s1-2s1-3s0-5s0-7s0-8s1` | H3/two | presplit | 1 | certified | 93.9 | 33.0 |
| 71 | 3152 | `0s0_4s1-7s0__1s0-2s1-3s1-5s1-6s0-8s1` | H3/two | presplit | 2 | certified | 320.0 | 45.4 |
| 72 | 3196 | `0s0_5s0-6s0__1s0-2s0-3s1-4s0-7s0-8s1` | H3/two | presplit | 0 | certified | 15.6 | 32.5 |
| 73 | 3240 | `0s0_5s0-6s0__1s1-2s1-3s0-4s1-7s0-8s1` | H3/two | presplit | 1 | certified | 39.6 | 21.0 |
| 74 | 3284 | `0s0_5s0-6s1__1s1-2s0-3s0-4s0-7s0-8s1` | H3/two | presplit | 2 | certified | 352.9 | 43.3 |
| 75 | 3328 | `0s0_5s1-6s0__1s1-2s1-3s0-4s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 340.4 | 51.3 |
| 76 | 3372 | `0s0-1s1_5__2s0-3s1-4s1-6s0-7s0-8s0` | H6(1,1)/one | timeout300 | 1 | certified | 241.2 | 40.2 |
| 77 | 3416 | `0s0-2s1_3__1s1-4s0-5s1-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 282.4 | 40.9 |
| 78 | 3460 | `0s0-2s1_5__1s0-3s0-4s0-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | 0 | certified | 198.1 | 35.8 |
| 79 | 3504 | `0s0-2s1_5__1s1-3s1-4s1-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | 1 | certified | 280.8 | 37.7 |
| 80 | 3548 | `0s0-2s1_6__1s1-3s0-4s0-5s1-7s1-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 178.0 | 38.5 |
| 81 | 3592 | `0s0-3s1_4__1s1-2s0-5s1-6s0-7s1-8s1` | H6(3,1)/one | never_ran | 0 | certified | 195.2 | 38.1 |
| 82 | 3636 | `0s0-3s1_5__1s0-2s1-4s0-6s1-7s1-8s1` | H6(3,1)/one | presplit | 1 | certified | 155.2 | 33.2 |
| 83 | 3680 | `0s0-4s0_6__1s0-2s0-3s0-5s0-7s1-8s1` | H6(4,0)/one | presplit | 2 | certified | 28.7 | 24.8 |
| 84 | 3724 | `0s0-4s0_6__1s1-2s0-3s1-5s1-7s1-8s1` | H6(4,0)/one | presplit | 0 | certified | 58.4 | 24.9 |
| 85 | 3768 | `0s0-5s0_6__1s0-2s1-3s0-4s1-7s1-8s0` | H6(5,0)/one | presplit | 1 | certified | 60.4 | 29.1 |
| 86 | 3812 | `0s0-5s0_7__1s0-2s0-3s0-4s0-6s1-8s0` | H6(5,0)/one | presplit | 2 | certified | 50.5 | 25.6 |
| 87 | 3856 | `0s0-5s0_7__1s1-2s0-3s1-4s1-6s1-8s0` | H6(5,0)/one | presplit | 0 | certified | 101.1 | 35.1 |
| 88 | 3900 | `0s0-5s1_1__2s1-3s0-4s1-6s0-7s0-8s0` | H6(5,1)/one | presplit | 1 | certified | 142.7 | 30.9 |
| 89 | 3944 | `0s0-5s1_2__1s0-3s1-4s0-6s1-7s0-8s0` | H6(5,1)/one | presplit | 2 | certified | 159.5 | 34.5 |
| 90 | 3988 | `0s0-5s1_6__1s1-2s0-3s0-4s0-7s0-8s1` | H6(5,1)/one | never_ran | 0 | certified | 237.9 | 37.0 |
| 91 | 4032 | `0s0-5s1_1s1-10s1__2s0-3s1-4s0-6s0-7s1-8s1` | H6(5,1)/two | never_ran | 1 | certified | 41.8 | 24.2 |
| 92 | 4076 | `0s0-5s1_1s1-10s1__2s1-3s1-4s1-6s1-7s1-8s1` | H6(5,1)/two | never_ran | 2 | certified | 18.7 | 21.0 |
