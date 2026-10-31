# C2P5 M51 — LIST C2P5B.tsv, shard j = 1 of N = 50, H = 5.25 (TASK.md at 81cb025f)

Start 2026-10-31 15:10:33 UTC (epoch 1793459433), END 1793477433. Lane finished all units at 18:08:40 UTC, well before END.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042),
  cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…8ff1` and base.json `2476faff…2b48`: both match.
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (14 = rows of C2P5B.tsv with idx ≡ 1 mod 50)
| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 4 | 0 | 0 | 0 |
| P2 | Q | 2 | 2 | 0 | 0 | 0 |
| P2 | H | 1 | 1 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **14** | **14** | 0 | 0 | 0 |

All 14 were UNSATISFIABLE and certified: both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`) accepted every proof.

Certified units (min / median / max):
- solve: 21.15 / 300.93 / 1709.72 s
- lrat-check: 13.5 / 56.3 / 81.8 s
- cake_lpr: 113.6 / 319.45 / 448.1 s
- proof size: 0.217 / 3.26 / 5.12 GB

| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|
| P2_1-4 | Q | 1709.72 | 81.8 | 448.1 | 5.12 | 4390 |
| P2_7-12 | Q | 1084.29 | 72.8 | 403.8 | 4.19 | 4399 |
| P1_6-8 | Q | 419.81 | 57.1 | 319.1 | 3.32 | 4365 |
| P2_8-9-10 | H | 21.15 | 15.1 | 121.0 | 0.22 | 2646 |
| P1_2-7-10 | H | 263.17 | 57.5 | 319.8 | 3.19 | 4401 |
| P1_3-5-8 | H | 82.22 | 26.8 | 174.8 | 1.18 | 3182 |
| P1_4-5-8 | H | 25.95 | 14.3 | 120.4 | 0.22 | 2652 |
| P1_5-7-12 | H | 33.51 | 14.9 | 120.8 | 0.25 | 2646 |
| P3_4-8 | Q | 985.78 | 74.8 | 385.0 | 4.05 | 4367 |
| P3_1-4-9 | H | 421.76 | 67.5 | 338.9 | 3.42 | 4414 |
| P3_1-8-15 | H | 500.94 | 61.4 | 339.3 | 3.62 | 4378 |
| P3_4-6-10 | H | 79.61 | 25.9 | 174.5 | 1.11 | 3145 |
| P3_4-13-14 | H | 338.69 | 55.5 | 320.8 | 3.35 | 4418 |
| P3_6-7-8 | H | 26.09 | 13.5 | 113.6 | 0.22 | 2666 |

Largest solver RSS: 4418 MB (P3_4-13-14).

No SAT, no proof rejections, no errors, no memory or disk problems (the most disk used at once was about 17 GB, with at least 23 GB still free).
All proofs were deleted after checking, and no CNF or proof files are committed.
