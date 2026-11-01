# C2P / M12 (LIST C2P.tsv, shard 12 of 42, H = 3.0, Z = 01909a07)

**Result: 12 of 53 units certified UNSAT (both checkers), 0 timed out, 0 errors, 41 not reached. No SAT.**
(This replaces an earlier attempt at fb2c59af that stopped at step 1.)

## Tools and checks (`tools.txt`)
- Built with `vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (drat-trim 2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `p cnf 838032 16653336`, sha256 of base.cnf and base.json match.
- All 8 cube files P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Lane
Started 03:35:21Z (session start 03:22:50Z), END = 06:07:50Z (`run.sh`); lane stopped at 05:58:38Z with 551 s left
(less than 15 min before END, so no further unit started). Records: `out.jsonl`, log: `lane.log.tail`.

## Units (53: 44 H, 9 Q, no cover)
| case | certified | timed out | not reached |
|---|---|---|---|
| P8 | 5 H | 0 | 0 |
| P7 | 6 H + 1 Q | 0 | 0 |
| P6 | 0 | 0 | 6 H + 1 Q |
| P5 | 0 | 0 | 5 H + 2 Q |
| P4 | 0 | 0 | 6 H + 1 Q |
| P3 | 0 | 0 | 5 H + 2 Q |
| P2 | 0 | 0 | 6 H + 1 Q |
| P1 | 0 | 0 | 5 H + 1 Q |
| total | 12 (11 H, 1 Q) | 0 | 41 (33 H, 8 Q) |

Certified: P8_2-5-12, P8_1-4-10, P8_1-4-11, P8_4-10-14, P8_1-9-14, P7_2-10-13, P7_1-5-11, P7_10-11 (Q),
P7_9-11-12, P7_1-3-16, P7_3-10-11, P7_3-9-12. Every record: `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT`
(cake_lpr, heap 8000 MB, no retry needed).

Certified units (min / median / max):
- solve: 19.4 / 417.7 / 607.6 s (the Q unit P7_10-11: 607.6 s)
- lrat-check: 10.8 / 46.0 / 47.9 s
- cake_lpr: 103.7 / 286.7 / 300.2 s
- proof size: 0.22 / 3.47 / 3.66 GB (proofs deleted after checking)

The last two units ran with reduced caps (1330 s and 715 s) because of the END limit, and both finished well inside them.

Not reached (in file order from P6_7-8-11 to P1_2-8-15): the 41 rows of `units.tsv` after P7_3-9-12.

## Resources and problems
- Largest solver RSS: 4468 MB (P7_2-10-13); 15 GB machine, no memory problem.
- No SAT, no proof rejection, no `certified: false` record, no ERROR status.
