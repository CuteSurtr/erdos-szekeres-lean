# C2P4 M03: LIST = C2P4.tsv, shard j = 3 of N = 50, H = 2.5 h, task commit a46b478d

Start 2026-10-31T13:01:45Z (epoch 1793451705); END = start + 2.5 h − 15 min = 1793459805 (15:16:45Z). Machine: 4 CPUs, 15 GB RAM (`env.txt`). One lane (`run.sh`), started 13:05:44Z, exited 15:06:53Z.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…04d8ff1` and base.json `2476faff…bf472b48`, both as expected.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (13 rows with idx ≡ 3 mod 50, `units.tsv`)

| outcome | count | units |
|---|---|---|
| certified UNSAT | 1 | P6_9-14 (P6, Q) |
| timed out (UNKNOWN) | 1 | P4_6-14 (P4, Q), at a reduced cap of 3542 s (time left before END), not its full 6000 s |
| not reached | 11 | P4 H: P4_1-6-9, P4_1-12-14, P4_2-10-11, P4_5-11-15, P4_7-9-13; P3 Q: P3_5-11; P3 H: P3_1-5-12, P3_1-10-16, P3_4-7-15, P3_5-7-10, P3_6-9-11 |
| errors / certified false | 0 | — |

By case and kind: P6 Q 1/1 certified; P4 Q 0/1 certified (1 timeout); P4 H 0/5 (5 not reached); P3 Q 0/1 (not reached); P3 H 0/5 (not reached).

Certified unit (only one, so min = median = max): P6_9-14, solve 2973.5 s (wall 2999 s), proof 6.53 GB (6533115544 bytes, sha256 7e2f9b4b…13a2006), lrat-check 107.9 s (`c VERIFIED`), cake_lpr 595.7 s at heap 8000 MB (`s VERIFIED UNSAT`). Proof deleted after checking.

P4_6-14 should be re-run with its full cap (6000 s or 7000 s now that it has timed out) on a later wave.

## Resources and anomalies
- Largest solver RSS: 4380 MB (P4_6-14); P6_9-14 4359 MB. No memory problem.
- No SAT, no proof rejection, no errors.
