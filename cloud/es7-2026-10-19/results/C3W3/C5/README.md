# C3W3 / C5: wave 3, list C_s1two.tsv, shard 5 of 18

**Result: 8 of my 33 roots are closed. 1 is partial (stopped at END) and 24 were not reached. No SAT. No proof was rejected.** 2,055 new certified nodes. Every one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Started 04:42:20 UTC on 2026-10-21. END was 10:27:20. There was one lane, run with `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles` and a slice of min(2.0 h, time left) per root (`lane0.sh`).
- C3-S tools: worktree of 132398c, unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. The sanity check passed: `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both (`tools.txt`).
- Base CNF: `p cnf 168399 4154921`, sha256 `bf0e502e…d6da` (matches).
- Roots: rows of `C_s1two.tsv` with row ≡ 5 (mod 18), giving 33 roots: 3 partial and 30 untouched (`roots.tsv`).
- **Seeded records: 324.** These are certified or split records from C3WAVE1/C3WAVE2/C3S0 for the 3 partial roots: 0s0-1s1_3s1-5s0 has 123, 0s0-2s1_4s0-6s1 has 135 and 0s0-1s1_6s1-10s0 has 66. They went at the head of `/opt/work/out0.jsonl`. The committed `out.jsonl` holds only the 2,082 new records that come after them.

## Per root

Certified counts are new records only. Depth = number of layers. Timeouts are UNKNOWN results at the cap. Solve and check times are summed per node, not wall-clock.

| row | root | stratum | status | certified (new) by depth | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 5 | 0s0-1s1_3s1-5s0 | H6(1,1)/two | closed | d3: 84, d4: 347 | 0 | 0 | 4801 | 7374 |
| 23 | 0s0-2s1_4s0-6s1 | H6(2,1)/two | closed | d3: 84, d4: 335 | 0 | 0 | 5085 | 7678 |
| 41 | 0s0-2s1_3s0-8s0 | H6(2,1)/two | closed | d2: 1 | 0 | 0 | 253 | 47 |
| 59 | 0s0-2s1_4s0-9s1 | H6(2,1)/two | closed | d2: 1 | 0 | 0 | 274 | 40 |
| 77 | 0s0-2s1_6s0-7s0 | H6(2,1)/two | closed | d2: 1 | 0 | 0 | 35 | 24 |
| 95 | 0s0-3s1_1s1-4s0 | H6(3,1)/two | closed | d3: 84, d4: 462 | d2: 1 | 8 | 5854 | 9357 |
| 113 | 0s0-3s1_4s0-7s0 | H6(3,1)/two | closed | d2: 1 | 0 | 0 | 38 | 24 |
| 131 | 0s0-3s1_5s0-6s1 | H6(3,1)/two | closed | d3: 84, d4: 462 | d2: 1 | 8 | 5992 | 9545 |
| 149 | 0s0-3s1_6s1-7s0 | H6(3,1)/two | partial (stopped at END) | d4: 109 | d2: 1 | 8 | 930 | 1678 |
| 167 | 0s0-4s1_1s1-10s0 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 185 | 0s0-4s1_2s0-5s1 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 203 | 0s0-4s1_5s0-9s1 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 221 | 0s0-4s1_6s1-9s1 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 239 | 0s0-5s1_1s0-9s0 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 257 | 0s0-5s1_2s0-10s1 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 275 | 0s0-5s1_2s1-8s0 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 293 | 0s0-5s1_6s1-9s1 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 311 | 0s0-1s1_6s1-10s0 | H6(1,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 329 | 0s0-1s1_9s0-10s0 | H6(1,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 347 | 0s0-2s1_5s1-10s0 | H6(2,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 365 | 0s0-2s1_7s0-8s1 | H6(2,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 383 | 0s0-2s1_9s0-10s1 | H6(2,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 401 | 0s0-3s1_2s1-10s0 | H6(3,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 419 | 0s0-3s1_6s0-10s0 | H6(3,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 437 | 0s0-3s1_7s1-8s1 | H6(3,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 455 | 0s0-4s1_2s1-10s0 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 473 | 0s0-4s1_3s0-6s0 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 491 | 0s0-4s1_3s1-9s0 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 509 | 0s0-4s1_8s0-10s1 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 527 | 0s0-5s1_3s0-10s1 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 545 | 0s0-5s1_3s1-7s1 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 563 | 0s0-5s1_4s1-6s1 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 581 | 0s0-5s1_8s1-10s1 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |

| stratum | roots | closed | partial | not reached | certified (new) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 3 | 1 | 0 | 2 | 431 | 0 | 4801 | 7374 |
| H6(2,1)/two | 7 | 4 | 0 | 3 | 422 | 0 | 5646 | 7790 |
| H6(3,1)/two | 7 | 3 | 1 | 3 | 1202 | 3 | 12814 | 20604 |
| H6(4,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |


The partial root 0s0-3s1_6s1-7s0 started at 10:16:51 with a 0.175 h slice. It was still draining its last batch after END, and I killed it at about 10:31–10:35 UTC. Every record that was written is complete. No record has `cake_lpr: none`, so nothing needed a re-check. Its certified and split nodes in `out.jsonl` can be resumed.

Partial root 0s0-1s1_6s1-10s0 (row 311) was not reached. Its 66 seeded records were not used.

## compose.py

`compose.txt`: 2,055 certified nodes, `class_covered: false` (as expected for one shard), 682 uncovered frontier nodes.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problems. Used memory peaked at about 9 GB of 15 GB.
- Incident: while building the tools, the cake_lpr and drat-trim clones briefly landed in the repository root because of a shell `&` grouping mistake. I moved them to /opt/src before anything was committed, and their commits were verified afterwards. A `pkill -f` at the stop also ended my own shell once. The workers were then killed by PID. Neither incident affects any result.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `compose.txt`.
