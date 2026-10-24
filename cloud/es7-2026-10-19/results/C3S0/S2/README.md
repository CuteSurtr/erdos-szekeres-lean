# C3S0 / S2: shard j = 2 of the s = 0 roots (task commit 702050b4, H = 1.0)

## Setup
- One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 01:43:08 UTC, END = 02:28:08 UTC, lanes started 01:44:51.
- Tools (`tools.txt`): C3-S tools worktree 132398c (unmodified); CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc + E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Matches.
- Roots: the 92 rows of `C3S0/roots.tsv` with row ≡ 2 (mod 4) (`roots.tsv`). Three lanes (`lane0.sh` … `lane2.sh`), `--jobs 1`, lane k takes positions ≡ k (mod 3).
- Every certified node has `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT` in `out.jsonl`. 157 certified nodes in total.

## Incidents
- No SAT FOUND, no PROOF NOT ACCEPTED, no memory problem (peak about 6 GB used of 15).
- Lane 0 stopped on time (02:28:38). Lanes 1 and 2 were still inside `close_tree.py` past END: their last slices had started at 02:18 (0.169 h) and 02:20 (0.133 h), and close_tree was still certifying the children it had split. I killed them at 02:33 so the README deadline could still be met. Lane 1's last root `0s0-4s0_7s0-10s1` had already closed. Lane 2's last root `0s0-5s0_1s0-4s1` stays partial. The records it had written are kept, so a later run can resume it.
- `compose.txt`: 157 certified nodes, every CNF sha256 recomputed, class not covered (expected).

## Per root
Depth = number of layers; the roots are at depth 2. Timeouts are nodes that hit their cap (300 s at d2) and were split. Solve and check times are per-node sums in seconds.

| # | root | stratum | orbits | status | certified by depth | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0s0-3s0_1s0-2s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 202 | 44 |
| 2 | 0s0-3s0_1s0-6s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 128 | 35 |
| 3 | 0s0-3s0_1s0-8s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 27 | 30 |
| 4 | 0s0-3s0_1s1-10s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 106 | 36 |
| 5 | 0s0-3s0_1s1-4s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 11 | 26 |
| 6 | 0s0-3s0_1s1-6s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 53 | 32 |
| 7 | 0s0-3s0_1s1-8s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 99 | 37 |
| 8 | 0s0-3s0_2s0-10s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 23 | 30 |
| 9 | 0s0-3s0_2s0-5s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 210 | 46 |
| 10 | 0s0-3s0_2s0-8s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 82 | 25 |
| 11 | 0s0-3s0_2s1-4s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 100 | 38 |
| 12 | 0s0-3s0_2s1-6s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 80 | 25 |
| 13 | 0s0-3s0_2s1-8s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 40 | 33 |
| 14 | 0s0-3s0_4s0-10s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 67 | 24 |
| 15 | 0s0-3s0_4s0-6s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 6 | 12 |
| 16 | 0s0-3s0_4s0-8s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 12 | 18 |
| 17 | 0s0-3s0_4s1-10s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 9 | 20 |
| 18 | 0s0-3s0_4s1-6s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 144 | 42 |
| 19 | 0s0-3s0_4s1-8s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 65 | 25 |
| 20 | 0s0-3s0_5s0-6s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 6 | 11 |
| 21 | 0s0-3s0_5s0-8s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 6 | 11 |
| 22 | 0s0-3s0_5s1-10s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 45 | 32 |
| 23 | 0s0-3s0_5s1-7s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 133 | 30 |
| 24 | 0s0-3s0_5s1-9s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 82 | 30 |
| 25 | 0s0-3s0_6s0-7s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 8 | 17 |
| 26 | 0s0-3s0_6s0-9s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 8 | 12 |
| 27 | 0s0-3s0_6s1-7s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 101 | 27 |
| 28 | 0s0-3s0_6s1-9s1 | H6(3,0) | two | closed | d2: 1 | – | 0 | 8 | 14 |
| 29 | 0s0-3s0_7s0-9s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 6 | 13 |
| 30 | 0s0-3s0_7s1-8s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 127 | 28 |
| 31 | 0s0-3s0_8s0-10s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 9 | 20 |
| 32 | 0s0-3s0_8s1-10s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 128 | 30 |
| 33 | 0s0-3s0_9s0-10s0 | H6(3,0) | two | closed | d2: 1 | – | 0 | 6 | 15 |
| 34 | 0s0-4s0_1s0-10s0 | H6(4,0) | two | closed | d2: 1 | – | 0 | 263 | 38 |
| 35 | 0s0-4s0_1s0-3s0 | H6(4,0) | two | closed | d2: 1 | – | 0 | 17 | 21 |
| 36 | 0s0-4s0_1s0-6s0 | H6(4,0) | two | closed | d2: 1 | – | 0 | 58 | 20 |
| 37 | 0s0-4s0_1s0-8s0 | H6(4,0) | two | closed | d2: 1 | – | 0 | 172 | 37 |
| 38 | 0s0-4s0_1s1-10s0 | H6(4,0) | two | closed | d2: 1 | – | 0 | 16 | 20 |
| 39 | 0s0-4s0_1s1-3s0 | H6(4,0) | two | closed | d2: 1 | – | 0 | 234 | 44 |
| 40 | 0s0-4s0_1s1-6s0 | H6(4,0) | two | closed | d2: 1 | – | 0 | 104 | 28 |
| 41 | 0s0-4s0_1s1-8s0 | H6(4,0) | two | closed | d2: 1 | – | 0 | 16 | 17 |
| 42 | 0s0-4s0_3s0-10s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 32 | 20 |
| 43 | 0s0-4s0_3s0-6s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 300 | 43 |
| 44 | 0s0-4s0_3s0-8s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 106 | 34 |
| 45 | 0s0-4s0_3s1-10s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 113 | 27 |
| 46 | 0s0-4s0_3s1-6s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 18 | 22 |
| 47 | 0s0-4s0_3s1-8s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 69 | 30 |
| 48 | 0s0-4s0_5s0-10s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 63 | 24 |
| 49 | 0s0-4s0_5s0-7s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 119 | 33 |
| 50 | 0s0-4s0_5s0-9s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 92 | 24 |
| 51 | 0s0-4s0_5s1-6s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 18 | 15 |
| 52 | 0s0-4s0_5s1-8s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 18 | 23 |
| 53 | 0s0-4s0_6s0-10s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 83 | 24 |
| 54 | 0s0-4s0_6s0-8s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 136 | 33 |
| 55 | 0s0-4s0_6s1-10s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 56 | 26 |
| 56 | 0s0-4s0_6s1-8s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 16 | 20 |
| 57 | 0s0-4s0_7s0-10s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 104 | 26 |
| 58 | 0s0-4s0_7s0-9s1 | H6(4,0) | two | closed | d2: 1 | – | 0 | 115 | 29 |
| 59 | 0s0-5s0_1s0-2s1 | H6(5,0) | two | partial | d4: 66 | d2: 1 | 8 | 529 | 827 |
| 60 | 0s0-5s0_1s0-4s1 | H6(5,0) | two | partial | d4: 30 | d2: 1 | 8 | 403 | 356 |
| 61 | 0s0-5s0_1s0-7s1 | H6(5,0) | two | closed | d2: 1 | – | 0 | 98 | 26 |
| 62 | 0s0-5s0_1s0-9s1 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 63 | 0s0-5s0_1s1-2s1 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 64 | 0s0-5s0_1s1-4s1 | H6(5,0) | two | closed | d2: 1 | – | 0 | 11 | 15 |
| 65 | 0s0-5s0_2s1-8s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 66 | 0s0-5s0_3s0-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 67 | 0s0-5s0_3s0-6s0 | H6(5,0) | two | closed | d2: 1 | – | 0 | 24 | 21 |
| 68 | 0s0-5s0_3s0-8s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 69 | 0s0-5s0_3s1-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 70 | 0s0-5s0_3s1-6s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 71 | 0s0-5s0_3s1-8s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 72 | 0s0-5s0_4s0-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 73 | 0s0-5s0_4s0-7s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 74 | 0s0-5s0_4s0-9s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 75 | 0s0-5s0_4s1-6s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 76 | 0s0-5s0_4s1-8s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 77 | 0s0-5s0_6s0-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 78 | 0s0-5s0_6s0-8s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 79 | 0s0-5s0_6s1-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 80 | 0s0-5s0_6s1-8s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 81 | 0s0-5s0_7s0-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 82 | 0s0-5s0_7s0-9s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 83 | 0s0-5s0_7s1-8s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 84 | 0s0-5s0_8s0-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 85 | 0s0-5s0_8s1-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 86 | 0s0-5s0_9s0-10s0 | H6(5,0) | two | not reached | – | – | 0 | 0 | 0 |
| 87 | 0s0-3s0_1 | H6(3,0) | one | not reached | – | – | 0 | 0 | 0 |
| 88 | 0s0-3s0_6 | H6(3,0) | one | not reached | – | – | 0 | 0 | 0 |
| 89 | 0s0-4s0_10 | H6(4,0) | one | not reached | – | – | 0 | 0 | 0 |
| 90 | 0s0-4s0_7 | H6(4,0) | one | not reached | – | – | 0 | 0 | 0 |
| 91 | 0s0-5s0_4 | H6(5,0) | one | not reached | – | – | 0 | 0 | 0 |
| 92 | 0s0-5s0_9 | H6(5,0) | one | not reached | – | – | 0 | 0 | 0 |

| group | roots | closed | partial | not reached | certified nodes | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(3,0) | 35 | 33 | 0 | 2 | 33 | 0 | 2139 | 868 |
| H6(4,0) | 27 | 25 | 0 | 2 | 25 | 0 | 2338 | 677 |
| H6(5,0) | 30 | 3 | 2 | 25 | 99 | 2 | 1064 | 1245 |
| all | 92 | 61 | 2 | 29 | 157 | 2 | 5541 | 2790 |
| one-orbit | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| two-orbit | 86 | 61 | 2 | 23 | 157 | 2 | 5541 | 2790 |

## Findings
- H6(3,0): every one of the 33 roots reached closed as a single node (d2), with no timeout.
- H6(4,0): 25 of the 25 roots reached closed as single nodes, with no timeout.
- H6(5,0): 5 roots were reached. 3 closed as single nodes. 2 (`0s0-5s0_1s0-2s1` and `0s0-5s0_1s0-4s1`) timed out at d2 within 300 s and were pre-split. Their d4 children certify in a few seconds each: 66 and 30 so far, and both are still open. So a = 5 is harder than a ≤ 4 in this shard. In this shard H6(4,0) had no timeout.
- None of the 6 one-orbit roots were reached, because they come last in the file.
