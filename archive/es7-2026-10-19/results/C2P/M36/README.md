# C2P / M36 (LIST C2P.tsv, shard 36 of 42, H = 3.0, Z = 01909a07)

Restart of the earlier M36 attempt (TASK at fb2c59af), which stopped at step 1. Its files were replaced.
Started 03:23:19Z. END was 06:08:19Z. The lane ran from 03:30Z to 05:56Z and stopped because 732 s remained, which is
less than the 15 minutes needed to start a unit.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources; nothing was cloned or downloaded. All 196
  manifest hashes match. Versions: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, and lrat-check from drat-trim 2e3b2dc
  with the E2 patch.
- Sanity checks: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints
  `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`, and the sha256 of base.cnf and base.json both match.
- Cubes: P1..P8 are all byte-identical to `C2P/cubes`.

## Units (53: 42 H, 11 Q, no cover; `units.tsv`, `out.jsonl`)
| | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|
| P8 (3 H, 2 Q) | 3 H | 2 Q (P8_10-15, P8_4-11) | 0 | 0 |
| P7 (5 H, 2 Q) | 0 | 1 Q (P7_1-6) | 6 (5 H, 1 Q) | 0 |
| P6 (6 H, 1 Q) | 0 | 0 | 7 | 0 |
| P5 (5 H, 1 Q) | 0 | 0 | 6 | 0 |
| P4 (6 H, 1 Q) | 0 | 0 | 7 | 0 |
| P3 (6 H, 1 Q) | 0 | 0 | 7 | 0 |
| P2 (5 H, 2 Q) | 0 | 0 | 7 | 0 |
| P1 (6 H, 1 Q) | 0 | 0 | 7 | 0 |
| **total** | **3 (H)** | **3 (Q)** | **47 (37 H, 10 Q)** | **0** |

- The certified units are P8_2-12-16, P8_3-14-15 and P8_10-12-15. lrat-check printed `c VERIFIED` and cake_lpr printed
  `s VERIFIED UNSAT` for each, with heap 8000 MB.
  - Solve time: min 30.4 s, median 259.3 s, max 359.8 s.
  - lrat-check time: min 13.2 s, median 53.8 s, max 55.4 s.
  - cake_lpr time: min 111.6 s, median 307.9 s, max 316.0 s.
  - Proof size: min 215 MB, median 3.19 GB, max 3.33 GB. Every proof was deleted after the checks.
- Each of the 3 Q units ran to its 2400 s cap (solve about 2382 s) and timed out.

## Resources and anomalies
- The largest solver RSS was 4416 MB (P8_10-15). There was no memory problem.
- No SAT result, no proof rejection, no `certified: false` record and no ERROR.
