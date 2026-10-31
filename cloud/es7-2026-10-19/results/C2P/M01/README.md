# C2P / M01 (LIST C2P.tsv, shard 1 of 42, H = 3.0, Z = 01909a07)

**Result: 11 of 54 units certified UNSAT (both checkers), 0 timed out, 0 errors, 43 not reached. No SAT.**

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (drat-trim 2e3b2dc + E2 patch).
- Sanity: cake_lpr example `s VERIFIED UNSAT`; the bad LRAT was rejected by both checkers and the good one accepted by both.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes: P1..P8 all byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- The earlier attempt's files (from Z = fb2c59af, stopped at step 1) were replaced.

## Units (`units.tsv`, idx ≡ 1 mod 42: 54 units, 45 H and 9 Q, no cover)
Lane: start 03:23:24Z, END 06:08:24Z (`run.sh`). It finished at 06:05:30Z ("stop: 173 s left").

| case | certified | timed out | not reached |
|---|---|---|---|
| P8 | 6 H | 0 | 0 |
| P7 | 4 H + 1 Q | 0 | 2 H |
| P1–P6 | 0 | 0 | all 39 (32 H, 7 Q) |

Certified units: P8_1-5-9, P8_1-10-15, P8_2-11-15, P8_2-9-15, P8_1-12-16, P8_2-9-10, P7_1-11-15, P7_9-10-11,
P7_1-9-12, P7_1-8-10, P7_3-14 (Q).

| certified (11) | min | median | max |
|---|---|---|---|
| solve s | 26.2 | 346.2 | 2237.2 (P7_3-14, Q) |
| lrat-check s | 13.0 | 55.2 | 92.0 |
| cake_lpr s | 110.0 | 311.2 | 513.1 |
| proof size | 0.22 GB | 3.37 GB | 5.88 GB |

Without the Q unit, the H units took 26 to 458 s to solve (most 260 to 460 s).
All cake_lpr runs passed with an 8000 MB heap; none needed the retry at 11000 MB.

## Memory and anomalies
- Largest solver RSS: 4412 MB (P8_2-9-15). Peak process RSS seen during the run: cake_lpr about 8.2 GB. No memory problem and no OOM.
- No SAT, no proof rejection, no `certified: false` record, no ERROR status.
