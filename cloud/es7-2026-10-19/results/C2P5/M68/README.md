# C2P5 M68: list C2P5B.tsv, shard j = 18 of N = 50, H = 5.25, TASK commit 81cb025f

## Tools and checks
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored `tools-src.tar.xz`; manifest: all 196 files match. Nothing was cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…f2b48` (both as expected).
- Cubes P1..P8 from `l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`. Lane start 2026-10-31 15:09:33Z (epoch 1793459373), END 1793477373 (20:09:33Z); command in `run.sh`.

## Units (19)
| case | kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P2 | Q | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 0 | 0 | 0 |
| P3 | H | 1 | 0 | 4 | 0 |
| **total** | | **15** | **0** | **4** | **0** |

Certified: P2_3-15, P1_2-15, P2_1-3-10, P2_1-7-12, P2_3-7-8, P2_3-14-15, P2_4-9-13, P2_5-9-14, P1_2-4-7, P1_2-9-12, P1_3-7-8, P1_4-7-10, P1_6-7-11, P3_5-14, P3_1-5-15.
P3_5-14 (list cap 8000) ran with the END-shortened cap 4730 s and P3_1-5-15 (list cap 2400) with 1045 s; both finished UNSAT well inside.
Not reached (lane stopped with 862 s left before END): P3_1-11-14, P3_4-8-10, P3_5-7-13, P3_6-9-14.

Certified units, min / median / max:
- solve: 26.45 / 334.65 / 2959.9 s (Q units: 2305.4, 2855.1, 2959.9 s)
- lrat-check: 13.5 / 60.1 / 108.5 s
- cake_lpr: 111.0 / 345.8 / 611.4 s
- proof size: 0.22 / 3.34 / 6.55 GB

## Resources and anomalies
- Largest solver RSS: 4451 MB (P2_5-9-14). No memory problem.
- No SAT, no proof rejection, no `certified: false`, no ERROR record.
