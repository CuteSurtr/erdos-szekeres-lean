# C2P4 M04 (LIST = C2P4.tsv, j = 4, N = 50, H = 2.5, task commit a46b478d)

Start 2026-10-31 13:01:37 UTC (epoch 1793451697), END 15:16:37 UTC (epoch 1793459797). Lane started 13:05:11, finished 15:11:08 ("stop: 328 s left").
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8),
  lrat-check (2e3b2dc + E2 patch) built from the vendored sources, nothing downloaded.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both checkers; good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`).
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…f2b48`, both as required.
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (13 rows, idx ≡ 4 mod 50)

| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P5 | Q | 1 | 1 (P5_1-4) | 0 | 0 | 0 |
| P4 | Q | 1 | 1 (P4_6-15) | 0 | 0 | 0 |
| P4 | H | 5 | 1 (P4_1-6-10) | 0 | 4 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 |
| P3 | H | 5 | 0 | 0 | 5 | 0 |
| total | | 13 | 3 | 0 | 10 | 0 |

Certified (both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`):

| unit | cap s | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|
| P5_1-4 | 7000 | 1207.48 | 68.2 | 396.3 | 4469772372 | 4367.5 |
| P4_6-15 | 5587 (lane-capped from 6000) | 3982.86 | 131.0 | 734.0 | 7793756617 | 4420.5 |
| P4_1-6-10 | 680 (lane-capped from 1800) | 507.51 | 63.7 | 364.6 | 3521372916 | 4408.6 |

min / median / max: solve 507.51 / 1207.48 / 3982.86 s; lrat-check 63.7 / 68.2 / 131.0 s; cake_lpr 364.6 / 396.3 / 734.0 s;
proof 3.52 / 4.47 / 7.79 GB.

Not reached (time): P4_1-12-15, P4_5-6-7, P4_5-12-13, P4_7-9-14 (H); P3_5-12 (Q); P3_1-5-13, P3_1-11-12, P3_4-7-16, P3_5-7-11, P3_6-9-12 (H).

## Other
- Largest solver RSS: 4420.5 MB (P4_6-15). cake_lpr reached about 8.2 GB RSS (heap 8000 MB); no memory problem.
- No SAT, no proof rejection, no ERROR record, no timeout.
- Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.
