# C3W7 Q33: nine-bit σ-cubes of the H3/one roots at cap 900

Task `results/C3W7/TASK.md` at 39bb1bac, with V = Q33, LIST = W7.tsv, j = 33, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 10:46:40 UTC, END 15:01:40 UTC (start + 4.5 h − 15 min).

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 (cad4e050d778aa37c9ea23afcbe704c94db3e890) at `/opt/c3u2`, used unmodified (clean worktree). `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity test: on the CNF {1},{−1}, LRAT `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

## Run

Units are the rows of `lists/W7.tsv` with row ≡ 33 (mod 36): 53 nine-bit cubes (`units.tsv`), nothing seeded. I ran 3 lanes (`lane0.sh` to `lane2.sh`, started with `setsid nohup`). Lane k took positions ≡ k (mod 3) and ran `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02` for each unit. At END the three lanes' process groups were killed; at that moment each lane had one solve in progress (started 14:48 to 14:51 UTC). `out.jsonl` holds the records of lanes 0, 1 and 2 in that order: 89 records, made up of 48 solve records and 41 layer-split records. There is no `recheck.jsonl` because no re-check was needed.

**Outcome: 7 certified, 41 timed out at 900 s, 5 not reached.**

- No SAT.
- No `PROOF NOT ACCEPTED`. No record looks certified while having cake_lpr `none`, because no checker was killed: the three solves killed at END never got as far as a check, and they left no record.
- No memory problems: at most about 2 to 3 GB was in use, with 7 GB or more free.
- No unit ended early. Every solve without a certificate ran the full 900.1 s.
- Each of the 41 timed-out units got its layer-split record (45 children, left unsolved). Those units are open and appear in `open_frontier` (45 each). No record has `children: 0` and no node is unsplittable.

## Per unit

| pos | row | node | lane | result | details |
|---|---|---|---|---|---|
| 0 | 33 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | 0 | certified | solve 713.6 s, check 103.4 s |
| 1 | 69 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | 1 | certified | solve 838.8 s, check 114.7 s |
| 2 | 105 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 3 | 141 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 4 | 177 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 5 | 213 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 6 | 249 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 7 | 285 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 8 | 321 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | 2 | certified | solve 836.7 s, check 102.4 s |
| 9 | 357 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 10 | 393 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 11 | 429 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 12 | 465 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 13 | 501 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 14 | 537 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 15 | 573 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 16 | 609 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 17 | 645 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 18 | 681 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 19 | 717 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 20 | 753 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 21 | 789 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 22 | 825 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 23 | 861 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | 2 | timed out at 900 | solve 900.3 s; layer-split record, 45 children (open) |
| 24 | 897 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | 0 | certified | solve 859.6 s, check 112.6 s |
| 25 | 933 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 26 | 969 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 27 | 1005 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 28 | 1041 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | 1 | certified | solve 695.7 s, check 96.8 s |
| 29 | 1077 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 30 | 1113 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 31 | 1149 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 32 | 1185 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 33 | 1221 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 34 | 1257 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 35 | 1293 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 36 | 1329 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 37 | 1365 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 38 | 1401 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 39 | 1437 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 40 | 1473 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 41 | 1509 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 42 | 1545 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1-8s0-9s0-10s1` | 0 | certified | solve 704.2 s, check 93.7 s |
| 43 | 1581 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1-8s1-9s0-10s1` | 1 | certified | solve 771.1 s, check 97.2 s |
| 44 | 1617 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0-8s0-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 45 | 1653 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0-8s1-9s0-10s1` | 0 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 46 | 1689 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1-8s0-9s0-10s1` | 1 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 47 | 1725 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1-8s1-9s0-10s1` | 2 | timed out at 900 | solve 900.1 s; layer-split record, 45 children (open) |
| 48 | 1761 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0-8s0-9s0-10s1` | 0 | not reached | started 14:48–14:51 UTC, solve killed at END (no record) |
| 49 | 1797 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s1-9s0-10s1` | 1 | not reached | started 14:48–14:51 UTC, solve killed at END (no record) |
| 50 | 1833 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1-8s0-9s0-10s1` | 2 | not reached | started 14:48–14:51 UTC, solve killed at END (no record) |
| 51 | 1869 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s1-9s0-10s1` | 0 | not reached | not started before END |
| 52 | 1905 | `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s0-9s0-10s1` | 1 | not reached | not started before END |

## Totals per root

| root | units here | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1` | 14 | 3 | 11 | 0 |
| `0s0_2` | 14 | 1 | 13 | 0 |
| `0s0_3` | 14 | 1 | 13 | 0 |
| `0s0_4` | 11 | 2 | 4 | 5 |

## Totals per parent six-bit cube

| parent six-bit cube | units here | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 0 | 1 |

Parents all of whose units on this machine were certified: 7
- `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0` (1 unit)
- `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0` (1 unit)
- `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0` (1 unit)
- `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0` (1 unit)
- `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0` (1 unit)
- `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1` (1 unit)
- `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1` (1 unit)

## Solve times of the certified units

7 certified: min 695.7, Q1 708.9, median 771.1, Q3 837.8, p90 847.1, max 859.6 s; 7 of 7 above 300 s. Check times 93.7–114.7 s (sum 721 s). All solve times: [695.7, 704.2, 713.6, 771.1, 836.7, 838.8, 859.6].

Totals: {'certified': 7, 'timed out at 900': 41, 'not reached': 5}
