# C2P2 M37 (LIST = C2P2.tsv, j = 37, N = 42, H = 2.5, Z = d266d2c3)

Start 2026-10-31 06:47:01Z (epoch 1793429221), END 09:02:01Z (epoch 1793437321). One lane (`run.sh`), 4 cores, 15 GB.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest all 196 files match; CaDiCaL 3.0.1, cake_lpr, lrat-check (E2 patch) built from the vendored sources (upstream c6073042, a36874a8, 2e3b2dc). No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base: `p cnf 838032 16653336`, base.cnf sha256 b0061e90…d8ff1 and base.json sha256 2476faff…2b48, both as required.
- Cubes: P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (18 in `units.tsv`)
| | P7 Q | P7 H | P4 cover | P6 H | total |
|---|---|---|---|---|---|
| in list | 2 | 9 | 1 | 6 | 18 |
| certified | 1 (P7_1-2) | 8 | 0 | 0 | 9 |
| timed out (UNKNOWN) | 0 | 0 | 0 | 0 | 0 |
| errors / not certified | 0 | 0 | 0 | 0 | 0 |
| not reached | 1 (P7_9-12) | 1 (P7_8-11-14) | 1 | 6 | 9 |

Certified: P7_1-2, P7_1-4-10, P7_1-5-14, P7_1-9-11, P7_1-12-13, P7_2-3-16, P7_2-10-15, P7_2-15-16, P7_3-9-15.
Not reached: P7_8-11-14, P7_9-12, P4_cover, P6_1-5-8, P6_1-11-16, P6_2-7-16, P6_2-15-16, P6_7-9-12, P6_8-11-12.
(The lane stopped at 08:53:21Z with 519 s left before END.)

Certified units (min / median / max):
- solve: 222.1 / 383.7 / 778.2 s (P7_1-2, the Q unit, was the slowest)
- lrat-check: 52.1 / 55.0 / 63.8 s
- cake_lpr: 303.1 / 317.0 / 368.6 s
- proof size: 3.18 / 3.40 / 3.93 GB

Largest solver RSS: 4402 MB (P7_3-9-15).

No SAT, no proof rejection, and no memory problem.
