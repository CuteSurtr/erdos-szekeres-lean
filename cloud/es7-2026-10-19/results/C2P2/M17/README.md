# C2P2 M17 — shard j = 17 of N = 42 of C2P2.tsv, H = 2.5 h, task commit d266d2c3

## Tools and checks
- `C2P/vendor/build_tools.sh` built from the vendored sources (manifest: all 196 files match; nothing cloned or downloaded): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch).
- Sanity: the bad LRAT was rejected by both checkers, the good one was accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`), and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF `zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476fafff…bf472b48`. Both match.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`. The machine is in `env.txt` (4 cores, 15 GB, no swap).

## Units (8 rows: idx 17, 59, 101, 143, 185, 227, 269, 311)
One lane ran from 06:49Z to 08:51Z, with END at 1793437306 (08:55:06Z).

| unit | case | kind | status | cap | solve s | lrat-check s | cake_lpr s | proof | RSS |
|---|---|---|---|---|---|---|---|---|---|
| P8_9-15 | P8 | Q | UNSAT, **certified** | 6000 | 5430.4 | 148.6 | 745.4 | 9.26 GB | 4361 MB |
| P6_1-3-9 | P6 | H | UNSAT, **certified** | 974 (shortened by END) | 298.5 | 55.1 | 307.5 | 3.29 GB | 4398 MB |
| P6_1-9 | P6 | Q | UNKNOWN (timed out at the shortened cap) | 301 (shortened; listed cap 2400) | 298.1 | – | – | – | 4404 MB |
| P6_2-3-11, P6_2-10-15, P6_3-9-12, P6_7-13-14 | P6 | H | not reached | 1800 | | | | | |
| P6_9-14 | P6 | Q | not reached | 2400 | | | | | |

Counts:
- P8: Q certified 1/1.
- P6: H certified 1 and not reached 4; Q timed out 1 and not reached 1.
- Totals: 2 certified, 1 timed out, 5 not reached, 0 errors.

The certified units give solve 298.5 / 5430.4 s, lrat-check 55.1 / 148.6 s, cake_lpr 307.5 / 745.4 s and proofs 3.29 / 9.26 GB (minimum / maximum; with n = 2 the median is the mean of these two values: solve 2864.5 s, lrat-check 101.9 s, cake_lpr 526.5 s, proof 6.27 GB).

The P6_1-9 timeout only reflects the 301 s cap left before END, not its listed cap of 2400 s. It should be run again at its full cap.

## Resources and problems
- The largest solver RSS was 4404 MB. cake_lpr used about 8.2 GB RSS (heap 8000 MB). There were no memory problems.
- The largest proof was 9.26 GB, against at least 19 GB of free disk.
- No SAT, no proof rejection and no `ERROR` record.
