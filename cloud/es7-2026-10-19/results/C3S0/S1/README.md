# C3S0 / S1: shard j = 1 of the s = 0 roots (m = 11, k = 7)

**Result: 51 of my 92 roots are closed, 2 are partial, 39 were not reached. No SAT. No proof rejection. No memory problem.**
Every one of the 155 certified nodes has lrat-check (E2 patch) `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 01:43:41 UTC on 2026-10-21, H = 1.0 h, END = 02:28:41.
Tools (`tools.txt`): C3-S tools from a worktree of commit 132398c at /opt/c3s, used unmodified; CaDiCaL 3.0.1 (c6073042);
cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`
(sanity check passed: `3 0 0` on {1},{-1} rejected by both, `3 0 1 2 0` accepted by both).
Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
Roots: rows of `C3S0/roots.tsv` with row ≡ 1 (mod 4), 92 roots (`roots.tsv`: 87 two-orbit, then 5 one-orbit).
Three lanes (`lane0.sh` … `lane2.sh`), `--jobs 1` each, lane k = positions ≡ k (mod 3).

## Incident (time only, not results)

`close_tree.py` checks `--hours` only between tree levels. Lane 2 began root `0s0-4s0_1s0-5s1` at 02:00:51 with a 0.17 h slice;
its d2 node timed out at 300 s and was split, and the whole next batch was submitted at once, so the lane was still running at 02:35,
past END. I killed it by hand at about 02:35 (noted at the end of `driver2.log`). Every finished node was already flushed to
`out2.jsonl`; only the node in flight (its cake_lpr check) was lost. The root is resumable from `out.jsonl`. Lanes 0 and 1 stopped on their own (02:28:58, 02:30:11).

## Per root

Depth = number of layers (roots are at depth 2). "splits" counts split records (timeouts and pre-splits). Solve and check times are summed over nodes.
Partial: `0s0-4s0_1s0-5s1` (d2 timed out at 300 s; 104 depth-4 nodes certified when killed) and
`0s0-5s0_1s1-4s0` (d2 timed out at 300 s; split; 546 open frontier nodes at the end of its slice, none attempted).

| # | row | root | kind | status | certified by depth | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 0s0-3s0_1s0-2s0 | two-orbit | closed | d2: 1 | 0 | 0 | 18 | 29 |
| 2 | 5 | 0s0-3s0_1s0-6s0 | two-orbit | closed | d2: 1 | 0 | 0 | 58 | 35 |
| 3 | 9 | 0s0-3s0_1s0-8s0 | two-orbit | closed | d2: 1 | 0 | 0 | 150 | 42 |
| 4 | 13 | 0s0-3s0_1s1-10s0 | two-orbit | closed | d2: 1 | 0 | 0 | 14 | 34 |
| 5 | 17 | 0s0-3s0_1s1-4s0 | two-orbit | closed | d2: 1 | 0 | 0 | 99 | 31 |
| 6 | 21 | 0s0-3s0_1s1-6s0 | two-orbit | closed | d2: 1 | 0 | 0 | 79 | 34 |
| 7 | 25 | 0s0-3s0_1s1-8s0 | two-orbit | closed | d2: 1 | 0 | 0 | 14 | 31 |
| 8 | 29 | 0s0-3s0_2s0-10s0 | two-orbit | closed | d2: 1 | 0 | 0 | 218 | 42 |
| 9 | 33 | 0s0-3s0_2s0-5s0 | two-orbit | closed | d2: 1 | 0 | 0 | 20 | 24 |
| 10 | 37 | 0s0-3s0_2s0-7s1 | two-orbit | closed | d2: 1 | 0 | 0 | 132 | 47 |
| 11 | 41 | 0s0-3s0_2s1-10s1 | two-orbit | closed | d2: 1 | 0 | 0 | 111 | 33 |
| 12 | 45 | 0s0-3s0_2s1-5s1 | two-orbit | closed | d2: 1 | 0 | 0 | 15 | 22 |
| 13 | 49 | 0s0-3s0_2s1-7s1 | two-orbit | closed | d2: 1 | 0 | 0 | 68 | 30 |
| 14 | 53 | 0s0-3s0_2s1-9s1 | two-orbit | closed | d2: 1 | 0 | 0 | 125 | 39 |
| 15 | 57 | 0s0-3s0_4s0-5s1 | two-orbit | closed | d2: 1 | 0 | 0 | 161 | 35 |
| 16 | 61 | 0s0-3s0_4s0-7s1 | two-orbit | closed | d2: 1 | 0 | 0 | 103 | 32 |
| 17 | 65 | 0s0-3s0_4s0-9s1 | two-orbit | closed | d2: 1 | 0 | 0 | 58 | 32 |
| 18 | 69 | 0s0-3s0_4s1-5s1 | two-orbit | closed | d2: 1 | 0 | 0 | 17 | 30 |
| 19 | 73 | 0s0-3s0_4s1-8s0 | two-orbit | closed | d2: 1 | 0 | 0 | 98 | 31 |
| 20 | 77 | 0s0-3s0_5s0-10s1 | two-orbit | closed | d2: 1 | 0 | 0 | 60 | 25 |
| 21 | 81 | 0s0-3s0_5s0-7s1 | two-orbit | closed | d2: 1 | 0 | 0 | 106 | 31 |
| 22 | 85 | 0s0-3s0_5s0-9s1 | two-orbit | closed | d2: 1 | 0 | 0 | 76 | 36 |
| 23 | 89 | 0s0-3s0_5s1-6s1 | two-orbit | closed | d2: 1 | 0 | 0 | 11 | 15 |
| 24 | 93 | 0s0-3s0_5s1-8s1 | two-orbit | closed | d2: 1 | 0 | 0 | 20 | 21 |
| 25 | 97 | 0s0-3s0_6s0-10s1 | two-orbit | closed | d2: 1 | 0 | 0 | 79 | 30 |
| 26 | 101 | 0s0-3s0_6s0-8s1 | two-orbit | closed | d2: 1 | 0 | 0 | 111 | 33 |
| 27 | 105 | 0s0-3s0_6s1-10s1 | two-orbit | closed | d2: 1 | 0 | 0 | 35 | 20 |
| 28 | 109 | 0s0-3s0_6s1-9s0 | two-orbit | closed | d2: 1 | 0 | 0 | 154 | 32 |
| 29 | 113 | 0s0-3s0_7s0-8s1 | two-orbit | closed | d2: 1 | 0 | 0 | 104 | 28 |
| 30 | 117 | 0s0-3s0_7s1-10s1 | two-orbit | closed | d2: 1 | 0 | 0 | 8 | 18 |
| 31 | 121 | 0s0-3s0_7s1-9s1 | two-orbit | closed | d2: 1 | 0 | 0 | 7 | 13 |
| 32 | 125 | 0s0-3s0_8s0-9s1 | two-orbit | closed | d2: 1 | 0 | 0 | 157 | 41 |
| 33 | 129 | 0s0-3s0_8s1-9s1 | two-orbit | closed | d2: 1 | 0 | 0 | 7 | 17 |
| 34 | 133 | 0s0-3s0_9s1-10s1 | two-orbit | closed | d2: 1 | 0 | 0 | 9 | 25 |
| 35 | 137 | 0s0-4s0_1s0-2s1 | two-orbit | closed | d2: 1 | 0 | 0 | 267 | 42 |
| 36 | 141 | 0s0-4s0_1s0-5s1 | two-orbit | partial | d4: 104 | 1 | 8 | 666 | 1367 |
| 37 | 145 | 0s0-4s0_1s0-7s1 | two-orbit | closed | d2: 1 | 0 | 0 | 98 | 41 |
| 38 | 149 | 0s0-4s0_1s0-9s1 | two-orbit | closed | d2: 1 | 0 | 0 | 22 | 19 |
| 39 | 153 | 0s0-4s0_1s1-2s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 40 | 157 | 0s0-4s0_1s1-5s1 | two-orbit | closed | d2: 1 | 0 | 0 | 10 | 18 |
| 41 | 161 | 0s0-4s0_1s1-7s1 | two-orbit | closed | d2: 1 | 0 | 0 | 118 | 33 |
| 42 | 165 | 0s0-4s0_3s0-10s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 43 | 169 | 0s0-4s0_3s0-6s0 | two-orbit | closed | d2: 1 | 0 | 0 | 25 | 22 |
| 44 | 173 | 0s0-4s0_3s0-8s0 | two-orbit | closed | d2: 1 | 0 | 0 | 70 | 25 |
| 45 | 177 | 0s0-4s0_3s1-10s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 46 | 181 | 0s0-4s0_3s1-6s0 | two-orbit | closed | d2: 1 | 0 | 0 | 170 | 34 |
| 47 | 185 | 0s0-4s0_3s1-8s0 | two-orbit | closed | d2: 1 | 0 | 0 | 107 | 33 |
| 48 | 189 | 0s0-4s0_5s0-10s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 49 | 193 | 0s0-4s0_5s0-7s0 | two-orbit | closed | d2: 1 | 0 | 0 | 8 | 16 |
| 50 | 197 | 0s0-4s0_5s0-9s0 | two-orbit | closed | d2: 1 | 0 | 0 | 29 | 16 |
| 51 | 201 | 0s0-4s0_5s1-6s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 52 | 205 | 0s0-4s0_5s1-8s0 | two-orbit | closed | d2: 1 | 0 | 0 | 250 | 47 |
| 53 | 209 | 0s0-4s0_6s0-10s0 | two-orbit | closed | d2: 1 | 0 | 0 | 46 | 28 |
| 54 | 213 | 0s0-4s0_6s0-8s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 55 | 217 | 0s0-4s0_6s1-10s0 | two-orbit | closed | d2: 1 | 0 | 0 | 126 | 30 |
| 56 | 221 | 0s0-4s0_6s1-8s0 | two-orbit | closed | d2: 1 | 0 | 0 | 297 | 44 |
| 57 | 225 | 0s0-4s0_7s0-10s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 58 | 229 | 0s0-4s0_7s0-9s0 | two-orbit | closed | d2: 1 | 0 | 0 | 11 | 21 |
| 59 | 233 | 0s0-5s0_1s0-2s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 60 | 237 | 0s0-5s0_1s0-4s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 61 | 241 | 0s0-5s0_1s0-7s0 | two-orbit | closed | d2: 1 | 0 | 0 | 182 | 38 |
| 62 | 245 | 0s0-5s0_1s0-9s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 63 | 249 | 0s0-5s0_1s1-2s0 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 64 | 253 | 0s0-5s0_1s1-4s0 | two-orbit | partial | – | 1 | 8 | 300 | 0 |
| 65 | 257 | 0s0-5s0_2s1-7s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 66 | 261 | 0s0-5s0_2s1-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 67 | 265 | 0s0-5s0_3s0-4s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 68 | 269 | 0s0-5s0_3s0-7s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 69 | 273 | 0s0-5s0_3s0-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 70 | 277 | 0s0-5s0_3s1-4s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 71 | 281 | 0s0-5s0_3s1-7s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 72 | 285 | 0s0-5s0_3s1-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 73 | 289 | 0s0-5s0_4s0-6s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 74 | 293 | 0s0-5s0_4s0-8s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 75 | 297 | 0s0-5s0_4s1-10s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 76 | 301 | 0s0-5s0_4s1-7s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 77 | 305 | 0s0-5s0_4s1-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 78 | 309 | 0s0-5s0_6s0-7s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 79 | 313 | 0s0-5s0_6s0-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 80 | 317 | 0s0-5s0_6s1-7s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 81 | 321 | 0s0-5s0_6s1-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 82 | 325 | 0s0-5s0_7s0-8s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 83 | 329 | 0s0-5s0_7s1-10s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 84 | 333 | 0s0-5s0_7s1-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 85 | 337 | 0s0-5s0_8s0-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 86 | 341 | 0s0-5s0_8s1-9s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 87 | 345 | 0s0-5s0_9s1-10s1 | two-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 88 | 349 | 0s0-3s0_4 | one-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 89 | 353 | 0s0-4s0_1 | one-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 90 | 357 | 0s0-4s0_6 | one-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 91 | 361 | 0s0-5s0_3 | one-orbit | not reached | – | 0 | 0 | 0 | 0 |
| 92 | 365 | 0s0-5s0_8 | one-orbit | not reached | – | 0 | 0 | 0 | 0 |

## Totals

| group | roots | closed | partial | not reached | certified nodes | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(3,0) | 35 | 34 | 0 | 1 | 34 | 0 | 2501 | 1016 |
| H6(4,0) | 26 | 16 | 1 | 9 | 120 | 1 | 2320 | 1837 |
| H6(5,0) | 31 | 1 | 1 | 29 | 1 | 1 | 482 | 38 |
| two-orbit | 87 | 51 | 2 | 34 | 155 | 2 | 5303 | 2891 |
| one-orbit | 5 | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| all | 92 | 51 | 2 | 39 | 155 | 2 | 5303 | 2891 |

Measurement: all 34 reached H6(3,0) roots closed at their d2 node with no timeout (mean solve 74 s, check 30 s). In H6(4,0), 16 of 17 reached closed
at d2; one (`0s0-4s0_1s0-5s1`) timed out. In H6(5,0), 1 of 2 reached closed; one (`0s0-5s0_1s1-4s0`) timed out. So both timeouts
are at a ≥ 4, consistent with C3-S Measurements 7. None of the 5 one-orbit roots was reached.

## compose.py

`compose.txt`: `{"certified_nodes": 155, "class_covered": false, "uncovered_frontier_nodes": 532, …}`. The class is not
expected to be covered by one shard; compose recomputed the CNF sha256 of all 155 certified nodes.

## SAT / proof rejections / memory

None. No SATISFIABLE result, no `PROOF NOT ACCEPTED`, no memory failure (peak about 4 GB used of 15 GB with three lanes).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (out0+out1+out2, 173 records, resumable), `driver0.log`–`driver2.log` (last 100 lines), `compose.txt`.
