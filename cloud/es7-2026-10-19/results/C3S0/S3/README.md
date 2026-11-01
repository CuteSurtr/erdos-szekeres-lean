# C3S0 / S3: shard j = 3 (rows ≡ 3 mod 4), H = 1.0 h, task at 702050b4

**Result: 58 of my 91 roots closed, 2 partial, 31 not reached. No SAT, no proof rejection, no memory problem.**
Every closed root closed at depth 2 as a single node with no timeout (mean 91 core-s solve per root).
The 2 timeouts (300 s cap) were both in H6(5,0).

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 01:43:48 UTC, END = 02:28:48 UTC. Lanes ran 01:46:53 to 02:33:33.
Tools are listed in `tools.txt`: C3-S tools from a worktree of 132398c (unmodified), CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8
(the example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch (sanity check passed: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both).
Base CNF `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
Three lanes (`lane0.sh`–`lane2.sh`), each `close_tree.py … --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`.

All 90 certified nodes have `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr). `compose.txt`: 90 certified nodes, class not covered (as expected); compose recomputed the CNF sha256 of every certified node.

**Incident (time only):** lane 2's last root `0s0-5s0_1s1-3s0` was still running at 02:36, past END, inside the README window. I stopped it by hand (SIGTERM).
Its 32 certified depth-4 records are in `out.jsonl`, so it can be resumed. The record stream is intact: the last line parses.
Lanes 0 and 1 stopped by themselves at 02:33:33 and 02:28:51.

## Totals per stratum

| stratum | roots | closed | partial | not reached |
|---|---|---|---|---|
| H6(3,0) | 35 | 33 | 0 | 2 |
| H6(4,0) | 25 | 24 | 0 | 1 |
| H6(5,0) | 31 | 1 | 2 | 28 |
| all | 91 | 58 | 2 | 31 |
| one-orbit | 5 | 0 | 0 | 5 |
| two-orbit | 86 | 58 | 2 | 26 |

H6(3,0) and H6(4,0): every root that was reached closed as one node. H6(5,0) (≥ 3, the case the task asked about): the first 3 roots reached gave 1 closed and 2 timeouts at 300 s:
- `0s0-5s0_1s0-10s0`: timeout at d2, split into 91 children (8 split records, with pre-splits). 546 frontier nodes are still open, and no child was certified in the slice.
- `0s0-5s0_1s1-3s0`: timeout at d2, split. 32 depth-4 nodes were certified at the 600 s cap before the manual stop.

This is a small sample, but it agrees with C3-S Measurements 7: a ≥ 3 is harder. The 5 one-orbit roots in my shard were not reached.

## Per root

Columns: certified nodes by depth (roots at depth 2), timeouts, split records, summed solve and check seconds (per node, not wall clock), open frontier at the end of the slice.

| row | idx | root | status | certified by depth | timeouts | splits | solve s | check s | open |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 338 | `0s0-3s0_1s0-4s1` | closed | 2: 1 | 0 | 0 | 284 | 47 | 0 |
| 7 | 343 | `0s0-3s0_1s0-7s0` | closed | 2: 1 | 0 | 0 | 117 | 43 | 0 |
| 11 | 347 | `0s0-3s0_1s0-9s0` | closed | 2: 1 | 0 | 0 | 230 | 52 | 0 |
| 15 | 351 | `0s0-3s0_1s1-2s0` | closed | 2: 1 | 0 | 0 | 218 | 51 | 0 |
| 19 | 355 | `0s0-3s0_1s1-5s0` | closed | 2: 1 | 0 | 0 | 98 | 41 | 0 |
| 23 | 359 | `0s0-3s0_1s1-7s0` | closed | 2: 1 | 0 | 0 | 52 | 26 | 0 |
| 27 | 363 | `0s0-3s0_1s1-9s0` | closed | 2: 1 | 0 | 0 | 14 | 24 | 0 |
| 31 | 368 | `0s0-3s0_2s0-4s0` | closed | 2: 1 | 0 | 0 | 17 | 27 | 0 |
| 35 | 372 | `0s0-3s0_2s0-6s0` | closed | 2: 1 | 0 | 0 | 26 | 27 | 0 |
| 39 | 378 | `0s0-3s0_2s0-9s0` | closed | 2: 1 | 0 | 0 | 164 | 37 | 0 |
| 43 | 383 | `0s0-3s0_2s1-4s1` | closed | 2: 1 | 0 | 0 | 14 | 23 | 0 |
| 47 | 387 | `0s0-3s0_2s1-6s1` | closed | 2: 1 | 0 | 0 | 20 | 27 | 0 |
| 51 | 391 | `0s0-3s0_2s1-8s1` | closed | 2: 1 | 0 | 0 | 119 | 33 | 0 |
| 55 | 396 | `0s0-3s0_4s0-10s1` | closed | 2: 1 | 0 | 0 | 14 | 30 | 0 |
| 59 | 400 | `0s0-3s0_4s0-6s1` | closed | 2: 1 | 0 | 0 | 106 | 41 | 0 |
| 63 | 404 | `0s0-3s0_4s0-8s1` | closed | 2: 1 | 0 | 0 | 80 | 26 | 0 |
| 67 | 408 | `0s0-3s0_4s1-10s1` | closed | 2: 1 | 0 | 0 | 121 | 37 | 0 |
| 71 | 412 | `0s0-3s0_4s1-6s1` | closed | 2: 1 | 0 | 0 | 18 | 24 | 0 |
| 75 | 418 | `0s0-3s0_4s1-9s1` | closed | 2: 1 | 0 | 0 | 115 | 30 | 0 |
| 79 | 423 | `0s0-3s0_5s0-6s1` | closed | 2: 1 | 0 | 0 | 122 | 38 | 0 |
| 83 | 427 | `0s0-3s0_5s0-8s1` | closed | 2: 1 | 0 | 0 | 96 | 30 | 0 |
| 87 | 431 | `0s0-3s0_5s1-10s1` | closed | 2: 1 | 0 | 0 | 81 | 27 | 0 |
| 91 | 435 | `0s0-3s0_5s1-7s1` | closed | 2: 1 | 0 | 0 | 15 | 29 | 0 |
| 95 | 439 | `0s0-3s0_5s1-9s1` | closed | 2: 1 | 0 | 0 | 54 | 24 | 0 |
| 99 | 444 | `0s0-3s0_6s0-7s1` | closed | 2: 1 | 0 | 0 | 111 | 29 | 0 |
| 103 | 448 | `0s0-3s0_6s0-9s1` | closed | 2: 1 | 0 | 0 | 99 | 31 | 0 |
| 107 | 452 | `0s0-3s0_6s1-7s1` | closed | 2: 1 | 0 | 0 | 9 | 18 | 0 |
| 111 | 458 | `0s0-3s0_7s0-10s0` | closed | 2: 1 | 0 | 0 | 8 | 12 | 0 |
| 115 | 463 | `0s0-3s0_7s0-9s1` | closed | 2: 1 | 0 | 0 | 117 | 33 | 0 |
| 119 | 467 | `0s0-3s0_7s1-8s1` | closed | 2: 1 | 0 | 0 | 8 | 29 | 0 |
| 123 | 472 | `0s0-3s0_8s0-10s1` | closed | 2: 1 | 0 | 0 | 106 | 29 | 0 |
| 127 | 476 | `0s0-3s0_8s1-10s1` | closed | 2: 1 | 0 | 0 | 9 | 26 | 0 |
| 131 | 481 | `0s0-3s0_9s0-10s1` | closed | 2: 1 | 0 | 0 | 154 | 45 | 0 |
| 135 | 640 | `0s0-4s0_1s0-10s1` | closed | 2: 1 | 0 | 0 | 25 | 21 | 0 |
| 139 | 644 | `0s0-4s0_1s0-3s1` | closed | 2: 1 | 0 | 0 | 269 | 41 | 0 |
| 143 | 648 | `0s0-4s0_1s0-6s1` | closed | 2: 1 | 0 | 0 | 206 | 48 | 0 |
| 147 | 652 | `0s0-4s0_1s0-8s1` | closed | 2: 1 | 0 | 0 | 37 | 24 | 0 |
| 151 | 656 | `0s0-4s0_1s1-10s1` | closed | 2: 1 | 0 | 0 | 174 | 33 | 0 |
| 155 | 660 | `0s0-4s0_1s1-3s1` | closed | 2: 1 | 0 | 0 | 10 | 26 | 0 |
| 159 | 664 | `0s0-4s0_1s1-6s1` | closed | 2: 1 | 0 | 0 | 67 | 39 | 0 |
| 163 | 668 | `0s0-4s0_1s1-8s1` | closed | 2: 1 | 0 | 0 | 198 | 37 | 0 |
| 167 | 703 | `0s0-4s0_3s0-5s0` | closed | 2: 1 | 0 | 0 | 25 | 21 | 0 |
| 171 | 707 | `0s0-4s0_3s0-7s0` | closed | 2: 1 | 0 | 0 | 27 | 34 | 0 |
| 175 | 711 | `0s0-4s0_3s0-9s0` | closed | 2: 1 | 0 | 0 | 144 | 33 | 0 |
| 179 | 715 | `0s0-4s0_3s1-5s0` | closed | 2: 1 | 0 | 0 | 172 | 42 | 0 |
| 183 | 719 | `0s0-4s0_3s1-7s0` | closed | 2: 1 | 0 | 0 | 128 | 44 | 0 |
| 187 | 723 | `0s0-4s0_3s1-9s0` | closed | 2: 1 | 0 | 0 | 49 | 26 | 0 |
| 191 | 728 | `0s0-4s0_5s0-6s0` | closed | 2: 1 | 0 | 0 | 9 | 22 | 0 |
| 195 | 732 | `0s0-4s0_5s0-8s0` | closed | 2: 1 | 0 | 0 | 8 | 16 | 0 |
| 199 | 736 | `0s0-4s0_5s1-10s0` | closed | 2: 1 | 0 | 0 | 80 | 27 | 0 |
| 203 | 740 | `0s0-4s0_5s1-7s0` | closed | 2: 1 | 0 | 0 | 176 | 33 | 0 |
| 207 | 744 | `0s0-4s0_5s1-9s0` | closed | 2: 1 | 0 | 0 | 118 | 29 | 0 |
| 211 | 749 | `0s0-4s0_6s0-7s0` | closed | 2: 1 | 0 | 0 | 8 | 12 | 0 |
| 215 | 753 | `0s0-4s0_6s0-9s0` | closed | 2: 1 | 0 | 0 | 8 | 13 | 0 |
| 219 | 757 | `0s0-4s0_6s1-7s0` | closed | 2: 1 | 0 | 0 | 180 | 41 | 0 |
| 223 | 761 | `0s0-4s0_6s1-9s0` | closed | 2: 1 | 0 | 0 | 228 | 44 | 0 |
| 227 | 766 | `0s0-4s0_7s0-8s0` | closed | 2: 1 | 0 | 0 | 8 | 12 | 0 |
| 231 | 945 | `0s0-5s0_1s0-10s0` | partial | – | 1 | 8 | 300 | 0 | 546 |
| 235 | 949 | `0s0-5s0_1s0-3s0` | not reached | – | – | – | – | – | – |
| 239 | 953 | `0s0-5s0_1s0-6s0` | closed | 2: 1 | 0 | 0 | 92 | 29 | 0 |
| 243 | 957 | `0s0-5s0_1s0-8s0` | not reached | – | – | – | – | – | – |
| 247 | 961 | `0s0-5s0_1s1-10s0` | not reached | – | – | – | – | – | – |
| 251 | 965 | `0s0-5s0_1s1-3s0` | partial | 4: 32 | 1 | 8 | 441 | 417 | (stopped) |
| 255 | 969 | `0s0-5s0_1s1-6s0` | not reached | – | – | – | – | – | – |
| 259 | 1003 | `0s0-5s0_2s1-8s1` | not reached | – | – | – | – | – | – |
| 263 | 1008 | `0s0-5s0_3s0-10s1` | not reached | – | – | – | – | – | – |
| 267 | 1012 | `0s0-5s0_3s0-6s1` | not reached | – | – | – | – | – | – |
| 271 | 1016 | `0s0-5s0_3s0-8s1` | not reached | – | – | – | – | – | – |
| 275 | 1020 | `0s0-5s0_3s1-10s1` | not reached | – | – | – | – | – | – |
| 279 | 1024 | `0s0-5s0_3s1-6s1` | not reached | – | – | – | – | – | – |
| 283 | 1028 | `0s0-5s0_3s1-8s1` | not reached | – | – | – | – | – | – |
| 287 | 1033 | `0s0-5s0_4s0-10s1` | not reached | – | – | – | – | – | – |
| 291 | 1037 | `0s0-5s0_4s0-7s1` | not reached | – | – | – | – | – | – |
| 295 | 1041 | `0s0-5s0_4s0-9s1` | not reached | – | – | – | – | – | – |
| 299 | 1045 | `0s0-5s0_4s1-6s1` | not reached | – | – | – | – | – | – |
| 303 | 1049 | `0s0-5s0_4s1-8s1` | not reached | – | – | – | – | – | – |
| 307 | 1054 | `0s0-5s0_6s0-10s1` | not reached | – | – | – | – | – | – |
| 311 | 1058 | `0s0-5s0_6s0-8s1` | not reached | – | – | – | – | – | – |
| 315 | 1062 | `0s0-5s0_6s1-10s1` | not reached | – | – | – | – | – | – |
| 319 | 1066 | `0s0-5s0_6s1-8s1` | not reached | – | – | – | – | – | – |
| 323 | 1071 | `0s0-5s0_7s0-10s1` | not reached | – | – | – | – | – | – |
| 327 | 1075 | `0s0-5s0_7s0-9s1` | not reached | – | – | – | – | – | – |
| 331 | 1079 | `0s0-5s0_7s1-8s1` | not reached | – | – | – | – | – | – |
| 335 | 1084 | `0s0-5s0_8s0-10s1` | not reached | – | – | – | – | – | – |
| 339 | 1088 | `0s0-5s0_8s1-10s1` | not reached | – | – | – | – | – | – |
| 343 | 1093 | `0s0-5s0_9s0-10s1` | not reached | – | – | – | – | – | – |
| 347 | 332 | `0s0-3s0_10` | not reached | – | – | – | – | – | – |
| 351 | 470 | `0s0-3s0_8` | not reached | – | – | – | – | – | – |
| 355 | 700 | `0s0-4s0_3` | not reached | – | – | – | – | – | – |
| 359 | 943 | `0s0-5s0_1` | not reached | – | – | – | – | – | – |
| 363 | 1052 | `0s0-5s0_6` | not reached | – | – | – | – | – | – |

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (out0+out1+out2, resumable), `driver0.log`–`driver2.log` (last 100 lines each), `compose.txt`.
