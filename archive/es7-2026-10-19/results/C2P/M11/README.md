# C2P / M11 (LIST C2P.tsv, shard 11 of 42, H = 3.5, Z = fb2c59af)

**Result: 11 of 53 units run: 9 certified UNSAT, 2 timed out (UNKNOWN), 42 not reached. No SAT, no proof rejection, no error, no memory problem.**

## Tools and checks (`tools.txt`)
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (`make cake_lpr`), drat-trim lrat-check 2e3b2dc with the E2 patch; links in `/opt/work/bin/`.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; on {1},{-1} LRAT `3 0 0` rejected by both checkers (lrat-check exit 1), `3 0 1 2 0` accepted by both.
- Base CNF `p cnf 838032 16653336`, sha256 of base.cnf and base.json match; all 8 cube files byte-identical.
- Lane: `lane.py` at fb2c59af unmodified (`run.sh`), 03:00:17 to 06:05:50 UTC, END 06:11:58 UTC; it stopped with 367 s left (< 15 min).

## Units (`units.tsv`, `out.jsonl`)

| case | kind | units | certified | UNKNOWN | not reached |
|------|------|------:|----------:|--------:|------------:|
| P8 | H | 4 | 4 | 0 | 0 |
| P8 | Q | 1 | 0 | 1 (P8_3-9, cap 2400) | 0 |
| P7 | H | 5 | 4 | 0 | 1 (P7_1-4-5) |
| P7 | Q | 2 | 1 (P7_2-5, cap 1186) | 1 (P7_2-11, cap 2400) | 0 |
| P6 | H/Q | 6/1 | 0 | 0 | 7 |
| P5 | H/Q | 6/1 | 0 | 0 | 7 |
| P4 | H/Q | 5/2 | 0 | 0 | 7 |
| P3 | H/Q | 6/1 | 0 | 0 | 7 |
| P2 | H/Q | 5/2 | 0 | 0 | 7 |
| P1 | H/Q | 5/1 | 0 | 0 | 6 |
| **total** | | **53** | **9** | **2** | **42** |

No cover unit in this shard.

Certified: P8_2-3-12, P8_9-12-13, P8_2-4-9, P8_1-3-15, P7_8-12-16, P7_1-5-16, P7_2-9-16, P7_1-2-11 (H), P7_2-5 (Q).
All with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` at heap 8000 MB (no retry needed).

| certified (9) | min | median | max |
|---|---:|---:|---:|
| solve s | 104.2 | 261.6 | 964.2 |
| lrat-check s | 33.3 | 50.4 | 65.2 |
| cake_lpr s | 192.1 | 293.2 | 370.6 |
| proof bytes | 1,770,498,623 | 3,252,023,220 | 4,292,036,532 |

Timed out: P8_3-9 (Q, 2377 s) and P7_2-11 (Q, 2381 s), both at the 2400 s cap; the Q units are the hard ones here (1 of 3 run closed, at 964 s).

Largest solver RSS: 4,413 MB (P8_3-9). Free memory never fell below about 6 GB available.

No SAT (`SAT_FOUND` never appeared), no proof rejection, no `ERROR` status, no memory problem.
