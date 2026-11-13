# C2P5 M63 — LIST C2P5B.tsv, shard j = 13 of N = 50, H = 5.25 h (TASK.md at 81cb025f)

**Result: all 19 units are certified UNSAT** (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` for each). There was no SAT, no proof rejection, no ERROR status, no timeout and no memory problem.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz`; all 196 files matched `MANIFEST.sha256`. Nothing was cloned or downloaded.
  - CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc) with the E2 patch.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`.
  - sha256 of base.cnf: `b0061e90…d8ff1`. sha256 of base.json: `2476faff…bf472b48`. Both match the expected values.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P*_cubes.txt`.

## Run
- One lane (`run.sh`), started 2026-10-31 15:13Z, with END = 1793477428 (start 1793459428 + 5.25 h − 15 min).
- The lane finished all units at 19:21:46Z.
- One cap was cut by END: P3_5-9 ran with cap 6579 s instead of 8000 s. It still finished, in 817 s.

## Units (19): certified 19, timed out (UNKNOWN) 0, not reached 0, errors 0

| case | Q certified | H certified |
|---|---|---|
| P1 | 1 (P1_2-10) | 5 |
| P2 | 1 (P2_3-10) | 6 |
| P3 | 1 (P3_5-9) | 5 |

Certified units, min / median / max:

| | solve s | lrat-check s | cake_lpr s | proof size |
|---|---|---|---|---|
| all 19 | 26.2 / 290.0 / 1349.8 | 12.2 / 54.1 / 74.5 | 114.1 / 313.5 / 425.7 | 0.22 / 3.35 / 4.67 GB |
| Q (3) | 817.5 / 1254.9 / 1349.8 | 67.0 / 70.2 / 74.5 | 362.7 / 417.8 / 425.7 | 3.98 / 4.60 / 4.67 GB |
| H (16) | 26.2 / 272.8 / 530.2 | 12.2 / 52.2 / 63.2 | 114.1 / 311.1 / 340.1 | 0.22 / 3.30 / 3.71 GB |

Per unit (solve s, lrat-check s, cake_lpr s, proof GB):

| unit | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| P2_3-10 Q | 1254.9 | 70.2 | 417.8 | 4.60 |
| P1_2-10 Q | 1349.8 | 74.5 | 425.7 | 4.67 |
| P2_1-3-5 | 261.3 | 54.1 | 311.5 | 3.28 |
| P2_1-6-13 | 530.2 | 59.8 | 337.9 | 3.71 |
| P2_3-6-12 | 262.6 | 51.7 | 303.6 | 3.27 |
| P2_3-12-13 | 283.0 | 52.0 | 318.3 | 3.35 |
| P2_4-8-14 | 366.2 | 57.5 | 329.1 | 3.42 |
| P2_5-8-14 | 256.0 | 49.2 | 298.5 | 3.23 |
| P1_2-3-14 | 361.5 | 59.3 | 328.7 | 3.52 |
| P1_2-8-14 | 481.9 | 63.2 | 340.1 | 3.67 |
| P1_3-6-11 | 104.0 | 32.1 | 185.2 | 1.40 |
| P1_4-6-12 | 203.4 | 51.8 | 309.9 | 3.14 |
| P1_5-10-12 | 32.6 | 13.3 | 119.1 | 0.22 |
| P3_5-9 Q | 817.5 | 67.0 | 362.7 | 3.98 |
| P3_1-5-10 | 472.3 | 60.4 | 334.3 | 3.61 |
| P3_1-10-14 | 343.1 | 52.3 | 310.6 | 3.42 |
| P3_4-7-13 | 290.0 | 56.0 | 313.5 | 3.33 |
| P3_5-7-8 | 26.2 | 12.2 | 114.1 | 0.22 |
| P3_6-8-14 | 222.8 | 50.8 | 294.5 | 3.16 |

**Largest solver RSS:** 4426.6 MB (P1_2-3-14). The cake_lpr heap was 8000 MB. The machine has 15 GB and no swap, and memory was never short.

## SAT / rejections / memory
- No SAT answer (`SAT_FOUND` never appeared).
- No `"certified": false` record and no ERROR status.
- No memory problem.

Files in this directory: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (19 records), `lane.log.tail`, `README.md`.
