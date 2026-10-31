# C2P / M17 (LIST C2P.tsv, shard 17 of 42, H = 3.0, Z = 01909a07)

Restart of the earlier M17 attempt, which had stopped at step 1 (its README was replaced). Start 03:22:50Z,
END 06:07:50Z (start + 3 h − 15 min); the lane stopped at 06:00:17Z with 452 s left.

**Result: 13 of 53 units run; 12 certified, 1 timed out (UNKNOWN), 40 not reached. No SAT, no proof rejection,
no errors, no memory problem.**

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match); nothing cloned or downloaded.
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json both match.
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: rows with idx ≡ 17 mod 42; 53 units, 42 H, 11 Q, no cover)

| case | kind | units | certified | UNKNOWN | not reached |
|---|---|---|---|---|---|
| P8 | H | 4 | 4 | 0 | 0 |
| P8 | Q | 1 | 0 | 1 | 0 |
| P7 | H | 6 | 6 | 0 | 0 |
| P7 | Q | 1 | 1 | 0 | 0 |
| P6 | H | 6 | 1 | 0 | 5 |
| P6 | Q | 1 | 0 | 0 | 1 |
| P5 | H / Q | 5 / 2 | 0 | 0 | 7 |
| P4 | H / Q | 6 / 1 | 0 | 0 | 7 |
| P3 | H / Q | 5 / 2 | 0 | 0 | 7 |
| P2 | H / Q | 5 / 1 | 0 | 0 | 6 |
| P1 | H / Q | 5 / 2 | 0 | 0 | 7 |
| **total** | | 53 | 12 | 1 | 40 |

- Timed out: **P8_9-15** (Q, cap 2400 s, solve 2381 s, UNKNOWN).
- Certified (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, heap 8000 MB every time):
  P8_1-6-15, P8_1-14-15, P8_2-6-12, P8_9-11-13, P7_8-10-15, P7_3-10-16, P7_2-4 (Q), P7_9-11-13, P7_3-8-9,
  P7_10-12-13, P7_2-4-8, P6_3-8-9.
- Certified units (min / median / max): solve 25.0 / 230.7 / 808.1 s; lrat-check 10.2 / 40.8 / 49.8 s;
  cake_lpr 103.8 / 266.3 / 314.7 s; LRAT proof 0.22 / 3.20 / 4.00 GB (216,390,785 / 3,199,315,982 / 4,004,444,870 bytes).
- No record with `"certified": false` and no `ERROR` status.

## Resources
- Largest solver RSS: 4395 MB (P6_3-8-9); well under the 15 GB of the machine. No memory problem.
- No `SAT_FOUND`, no proof rejection.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (13 records), `lane.log.tail`.
