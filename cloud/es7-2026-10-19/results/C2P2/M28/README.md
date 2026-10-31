# C2P2 M28 (LIST = C2P2.tsv, shard j = 28 of N = 42, H = 2.5, TASK commit d266d2c3)

## Tools and checks
- `C2P/vendor/build_tools.sh` built from the vendored sources (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042),
  cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). cake_lpr example: `s VERIFIED UNSAT`. Sanity: the bad LRAT was
  rejected by both checkers, the good LRAT accepted by both. Nothing was cloned or downloaded.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…bf472b48` (both as required).
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; lane command in `run.sh` (END = 1793437343 = 09:02:23Z).

## Units (7: rows idx 28, 70, 112, 154, 196, 238, 280)

| unit | case | kind | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P7_2-11 | P7 | Q | certified | 4515.3 | 116.0 | 622.2 | 8 326 207 122 | 4376 |
| P6_1-4-9 | P6 | H | certified | 402.7 | 59.1 | 330.0 | 3 405 788 774 | 4411 |
| P6_1-10-13 | P6 | H | certified | 337.3 | 59.0 | 345.6 | 3 301 101 808 | 4405 |
| P6_2-4-11 | P6 | H | certified | 414.7 | 63.1 | 343.5 | 3 339 824 841 | 4400 |
| P6_2-12-15 | P6 | H | not reached | | | | | |
| P6_7-8-11 | P6 | H | not reached | | | | | |
| P6_8-9-14 | P6 | H | not reached | | | | | |

By case and kind: P7 Q: 1 certified. P6 H: 3 certified, 3 not reached (lane stopped at 08:58:13Z with 249 s left before END).
Timed out (UNKNOWN): 0. Errors: 0. `certified: false`: 0.

Certified units (4), min / median / max:
- solve s: 337.3 / 408.7 / 4515.3
- lrat-check s: 59.0 / 61.1 / 116.0
- cake_lpr s: 330.0 / 344.6 / 622.2
- proof bytes: 3.30 GB / 3.37 GB / 8.33 GB

The P7_2-11 solve (cap 6000 s) used 4515 s. P6_2-4-11 had a cap of 485 s after the END clamp but its record shows solve 414.7 s, UNSAT.

Largest solver RSS: 4411 MB (P6_1-4-9). No memory problem; disk stayed at ≥ 20 GB free.
No SAT, no proof rejection, no memory problem.
