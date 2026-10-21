# C3S0 S0: s = 0 roots, shard j = 0 (row ≡ 0 mod 4), H = 1.0 h

Task: `results/C3S0/TASK.md` at 702050b4. One VM, 4 cores, 15 GB, no swap (`env.txt`). Start 01:43:43 UTC, END 02:28:43; lanes started 01:45:58.

## Tools (`tools.txt`)
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified. CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch. Sanity check passed: `3 0 0` on {1},{-1} rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…6cdd6da (matches).

## Run
92 roots (`roots.tsv`), three lanes (`lane0.sh`…`lane2.sh`), --jobs 1 each, slice min(0.17 h, time to END). Lane 0 finished at 02:31:17. Lanes 1 and 2 were in slices started 02:04 and 02:15 that overran END while certifying split children; I killed them at about 02:35 to keep the README window. Their certified records up to then are in `out.jsonl` (resumable).
No SAT FOUND, no PROOF NOT ACCEPTED, no memory problem (peak about 8 GB used of 15).

## Totals
| group | closed | partial | not reached | certified nodes | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|
| H6(3,0) | 34 | 0 | 2 | 34 | 0 | 3762 | 1034 |
| H6(4,0) | 4 | 3 | 18 | 141 | 3 | 1861 | 1920 |
| H6(5,0) | 0 | 0 | 31 | 0 | 0 | 0 | 0 |
| two-orbit | 38 | 3 | 46 | 175 | 3 | 5622 | 2955 |
| one-orbit | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| all | 38 | 3 | 51 | 175 | 3 | 5622 | 2955 |

Every root touched in H6(3,0) closed at depth 2 with one certified node, no timeouts (34 of 36 in the shard; the other 2 were not reached). H6(4,0): 4 roots closed at depth 2 with no timeouts; 3 two-orbit roots timed out at 300 s at depth 2 and were split (`0s0-4s0_1s0-9s0`: 88 depth-4 nodes certified, `0s0-4s0_1s1-2s0`: 49, `0s0-4s0_3s0-5s1`: none yet), so a ≥ 4 is harder, in line with C3-S Measurements 7. H6(5,0) and the one-orbit roots were not reached.

`compose.py`: 175 certified nodes, class not covered (expected), 515 uncovered frontier nodes (`compose.txt`).

Closed (38): 0s0-3s0_1s0-10s0 0s0-3s0_1s0-5s1 0s0-3s0_1s0-7s1 0s0-3s0_1s0-9s1 0s0-3s0_1s1-2s1 0s0-3s0_1s1-5s1 0s0-3s0_1s1-7s1 0s0-3s0_1s1-9s1 0s0-3s0_2s0-4s1 0s0-3s0_2s0-6s1 0s0-3s0_2s1-10s0 0s0-3s0_2s1-5s0 0s0-3s0_2s1-7s0 0s0-3s0_2s1-9s0 0s0-3s0_4s0-5s0 0s0-3s0_4s0-7s0 0s0-3s0_4s0-9s0 0s0-3s0_4s1-5s0 0s0-3s0_4s1-7s0 0s0-3s0_5s0-10s0 0s0-3s0_5s0-7s0 0s0-3s0_5s0-9s0 0s0-3s0_5s1-6s0 0s0-3s0_5s1-8s0 0s0-3s0_6s0-10s0 0s0-3s0_6s0-8s0 0s0-3s0_6s1-10s0 0s0-3s0_6s1-8s0 0s0-3s0_7s0-8s0 0s0-3s0_7s1-10s0 0s0-3s0_7s1-9s0 0s0-3s0_8s0-9s0 0s0-3s0_8s1-9s0 0s0-3s0_9s1-10s0 0s0-4s0_1s0-2s0 0s0-4s0_1s0-5s0 0s0-4s0_1s0-7s0 0s0-4s0_1s1-5s0 | group | closed | partial | not reached | certified nodes | timeouts | solve s | check s | 

Partial (3): 0s0-4s0_1s0-9s0 0s0-4s0_1s1-2s0 0s0-4s0_3s0-5s1

## Per root
| root | stratum | orbits | status | certified by depth | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| `0s0-3s0_1s0-10s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 247.1 | 48.7 |
| `0s0-3s0_1s0-5s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 296.5 | 42.3 |
| `0s0-3s0_1s0-7s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 74.1 | 37.5 |
| `0s0-3s0_1s0-9s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 28.3 | 28.2 |
| `0s0-3s0_1s1-2s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 11.6 | 16.9 |
| `0s0-3s0_1s1-5s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 14.5 | 27.0 |
| `0s0-3s0_1s1-7s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 109.4 | 38.5 |
| `0s0-3s0_1s1-9s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 139.0 | 37.5 |
| `0s0-3s0_2s0-4s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 283.1 | 52.3 |
| `0s0-3s0_2s0-6s1` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 204.3 | 40.0 |
| `0s0-3s0_2s1-10s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 12.4 | 20.5 |
| `0s0-3s0_2s1-5s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 143.3 | 36.9 |
| `0s0-3s0_2s1-7s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 81.8 | 33.3 |
| `0s0-3s0_2s1-9s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 11.7 | 20.8 |
| `0s0-3s0_4s0-5s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 7.8 | 16.6 |
| `0s0-3s0_4s0-7s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 8.3 | 18.1 |
| `0s0-3s0_4s0-9s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 51.9 | 21.9 |
| `0s0-3s0_4s1-5s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 204.5 | 37.1 |
| `0s0-3s0_4s1-7s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 156.7 | 28.3 |
| `0s0-3s0_5s0-10s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 69.1 | 29.8 |
| `0s0-3s0_5s0-7s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 7.9 | 16.8 |
| `0s0-3s0_5s0-9s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 35.2 | 20.0 |
| `0s0-3s0_5s1-6s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 159.0 | 38.5 |
| `0s0-3s0_5s1-8s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 159.5 | 31.2 |
| `0s0-3s0_6s0-10s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 49.9 | 27.2 |
| `0s0-3s0_6s0-8s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 8.9 | 14.4 |
| `0s0-3s0_6s1-10s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 136.1 | 31.3 |
| `0s0-3s0_6s1-8s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 220.0 | 36.3 |
| `0s0-3s0_7s0-8s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 9.2 | 13.6 |
| `0s0-3s0_7s1-10s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 172.6 | 34.9 |
| `0s0-3s0_7s1-9s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 251.0 | 46.1 |
| `0s0-3s0_8s0-9s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 9.3 | 12.6 |
| `0s0-3s0_8s1-9s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 175.2 | 33.5 |
| `0s0-3s0_9s1-10s0` | H6(3,0) | two-orbit | closed | d2:1 | 0 | 0 | 212.4 | 45.6 |
| `0s0-4s0_1s0-2s0` | H6(4,0) | two-orbit | closed | d2:1 | 0 | 0 | 20.5 | 18.4 |
| `0s0-4s0_1s0-5s0` | H6(4,0) | two-orbit | closed | d2:1 | 0 | 0 | 26.1 | 21.7 |
| `0s0-4s0_1s0-7s0` | H6(4,0) | two-orbit | closed | d2:1 | 0 | 0 | 165.8 | 35.0 |
| `0s0-4s0_1s0-9s0` | H6(4,0) | two-orbit | partial | d4:88 | 1 | 8 | 666.0 | 1181.8 |
| `0s0-4s0_1s1-2s0` | H6(4,0) | two-orbit | partial | d4:49 | 1 | 8 | 523.3 | 630.2 |
| `0s0-4s0_1s1-5s0` | H6(4,0) | two-orbit | closed | d2:1 | 0 | 0 | 158.8 | 33.4 |
| `0s0-4s0_1s1-7s0` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_1s1-9s0` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_3s0-5s1` | H6(4,0) | two-orbit | partial | - | 1 | 8 | 300.1 | 0.0 |
| `0s0-4s0_3s0-7s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_3s0-9s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_3s1-5s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_3s1-7s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_3s1-9s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_5s0-6s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_5s0-8s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_5s1-10s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_5s1-7s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_5s1-9s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_6s0-7s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_6s0-9s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_6s1-7s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_6s1-9s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_7s0-8s1` | H6(4,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_1s0-10s1` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_1s0-3s1` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_1s0-6s1` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_1s0-8s1` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_1s1-10s1` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_1s1-3s1` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_2s1-7s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_2s1-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_3s0-4s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_3s0-7s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_3s0-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_3s1-4s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_3s1-7s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_3s1-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_4s0-6s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_4s0-8s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_4s1-10s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_4s1-7s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_4s1-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_6s0-7s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_6s0-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_6s1-7s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_6s1-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_7s0-8s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_7s1-10s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_7s1-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_8s0-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_8s1-9s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_9s1-10s0` | H6(5,0) | two-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-3s0_2` | H6(3,0) | one-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-3s0_9` | H6(3,0) | one-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-4s0_5` | H6(4,0) | one-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_10` | H6(5,0) | one-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |
| `0s0-5s0_7` | H6(5,0) | one-orbit | not reached | - | 0 | 0 | 0.0 | 0.0 |

