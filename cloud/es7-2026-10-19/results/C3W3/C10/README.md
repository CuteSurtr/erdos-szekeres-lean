# C3W3 C10: list C_s1two.tsv, shard 10 of 18

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-21 04:42:56 UTC, budget 6 h, END = 10:27:56 UTC.
One lane (`lane0.sh`), `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(2.0, hours left before END). Task file at 640a56c2.

## Tools and base CNF (details in `tools.txt`)

- C3-S tools: worktree of 132398c at /opt/c3s, unmodified
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa; bundled example prints `s VERIFIED UNSAT`
- lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch; sanity check passed (`3 0 0` rejected by both, `3 0 1 2 0` accepted by both)
- base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches)

## Roots

33 roots (rows ≡ 10 mod 18, `roots.tsv`). 2 of them were `partial` and were seeded.

Seeded records: 1,091 at the start of out0.jsonl
- 0s0-1s1_4s0-8s1: 538 certified + 8 split, from C3WAVE2/K08/out.jsonl
- 0s0-1s1_7s1-10s0: 537 certified + 8 split, from C3WAVE2/K38/out.jsonl (this root was not reached, so its seed was not used)

`out.jsonl` has only the 2,368 new records.

Root 0s0-4s1_1s1-5s0 was still running at END. Its batch went on past END, so I killed it at 10:32 UTC to leave time for this README. No record was written with `cake_lpr: none`. The killed in-flight nodes have no record, so nothing needs a re-check.

## Per root (new records only; depth = number of layers, roots are depth 2)

| # | root | stratum | status | certified by depth (new) | timeouts (new) | splits (new) | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 1 | 0s0-1s1_4s0-8s1 | H6(1,1)/two | closed | d4: 8 | – | – | 63 | 156 |
| 2 | 0s0-2s1_1s0-10s0 | H6(2,1)/two | closed | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 5415 | 7822 |
| 3 | 0s0-2s1_3s1-5s1 | H6(2,1)/two | closed | d2: 1 | – | – | 38 | 19 |
| 4 | 0s0-2s1_4s1-8s0 | H6(2,1)/two | closed | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 5610 | 8437 |
| 5 | 0s0-3s1_1s0-2s1 | H6(3,1)/two | closed | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 6407 | 8478 |
| 6 | 0s0-3s1_1s1-6s1 | H6(3,1)/two | closed | d2: 1 | – | – | 270 | 33 |
| 7 | 0s0-3s1_4s0-9s1 | H6(3,1)/two | closed | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 4079 | 7740 |
| 8 | 0s0-3s1_5s0-9s0 | H6(3,1)/two | closed | d2: 1 | – | – | 151 | 28 |
| 9 | 0s0-4s1_1s0-2s0 | H6(4,1)/two | closed | d2: 1 | – | – | 25 | 18 |
| 10 | 0s0-4s1_1s1-5s0 | H6(4,1)/two | partial | d4: 128 | d2: 1 | d2: 1, d3: 7 | 836 | 1673 |
| 11 | 0s0-4s1_2s0-8s0 | H6(4,1)/two | not reached | – | – | – | 0 | 0 |
| 12 | 0s0-4s1_5s1-7s1 | H6(4,1)/two | not reached | – | – | – | 0 | 0 |
| 13 | 0s0-5s1_1s0-10s1 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |
| 14 | 0s0-5s1_1s1-2s1 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |
| 15 | 0s0-5s1_2s0-7s0 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |
| 16 | 0s0-5s1_6s0-10s1 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |
| 17 | 0s0-5s1_7s1-8s0 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |
| 18 | 0s0-1s1_7s1-10s0 | H6(1,1)/two | not reached | – | – | – | 0 | 0 |
| 19 | 0s0-2s1_1s1-6s0 | H6(2,1)/two | not reached | – | – | – | 0 | 0 |
| 20 | 0s0-2s1_6s0-10s1 | H6(2,1)/two | not reached | – | – | – | 0 | 0 |
| 21 | 0s0-2s1_7s1-8s0 | H6(2,1)/two | not reached | – | – | – | 0 | 0 |
| 22 | 0s0-3s1_2s0-10s1 | H6(3,1)/two | not reached | – | – | – | 0 | 0 |
| 23 | 0s0-3s1_2s1-6s1 | H6(3,1)/two | not reached | – | – | – | 0 | 0 |
| 24 | 0s0-3s1_6s1-10s1 | H6(3,1)/two | not reached | – | – | – | 0 | 0 |
| 25 | 0s0-3s1_8s0-9s0 | H6(3,1)/two | not reached | – | – | – | 0 | 0 |
| 26 | 0s0-4s1_2s1-5s1 | H6(4,1)/two | not reached | – | – | – | 0 | 0 |
| 27 | 0s0-4s1_3s0-8s1 | H6(4,1)/two | not reached | – | – | – | 0 | 0 |
| 28 | 0s0-4s1_6s1-10s0 | H6(4,1)/two | not reached | – | – | – | 0 | 0 |
| 29 | 0s0-4s1_8s1-9s0 | H6(4,1)/two | not reached | – | – | – | 0 | 0 |
| 30 | 0s0-5s1_3s0-7s0 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |
| 31 | 0s0-5s1_4s0-10s0 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |
| 32 | 0s0-5s1_4s1-9s0 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |
| 33 | 0s0-5s1_9s1-10s0 | H6(5,1)/two | not reached | – | – | – | 0 | 0 |

Solve and check times are summed per node over the new records. They are not wall clock: 3 jobs share 4 cores.
"Timeouts" counts UNKNOWN records at their cap.

## Totals per stratum

| stratum | roots | closed | partial | not reached | new certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 2 | 1 | 0 | 1 | 8 | 0 | 63 | 156 |
| H6(2,1)/two | 6 | 3 | 0 | 3 | 1093 | 2 | 11063 | 16279 |
| H6(3,1)/two | 8 | 4 | 0 | 4 | 1094 | 2 | 10907 | 16279 |
| H6(4,1)/two | 8 | 1 | 1 | 6 | 129 | 1 | 860 | 1691 |
| H6(5,1)/two | 9 | 0 | 0 | 9 | 0 | 0 | 0 | 0 |

Totals: 9 closed, 1 partial (0s0-4s1_1s1-5s0), 23 not reached. 2,368 new records, 2,324 of them certified.

Closed: 0s0-1s1_4s0-8s1, 0s0-2s1_1s0-10s0, 0s0-2s1_3s1-5s1, 0s0-2s1_4s1-8s0, 0s0-3s1_1s0-2s1, 0s0-3s1_1s1-6s1, 0s0-3s1_4s0-9s1, 0s0-3s1_5s0-9s0, 0s0-4s1_1s0-2s0.
Partial: 0s0-4s1_1s1-5s0. Not reached: rows 11–33 of `roots.tsv`, including the seeded partial root 0s0-1s1_7s1-10s0.

## Incidents

There were no SAT answers, no `PROOF NOT ACCEPTED`, and no memory problems. Peak used memory was about 9 GB of 15 GB.

`compose.txt`: output of `compose.py` on `out.jsonl`. The class is not expected to be covered.
Result: 2,324 certified nodes; `class_covered: false`, with 850 uncovered frontier nodes (as expected).
