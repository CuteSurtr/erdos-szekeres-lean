# C2P2 M01: shard j = 1 of N = 42 of C2P2.tsv

TASK `results/C2P2/TASK.md` at commit d266d2c3; V = M01, LIST = C2P2.tsv, j = 1, N = 42, H = 2.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31 06:47:29 UTC (epoch 1793429249),
END = 1793437349 (09:02:29 UTC), one lane (`run.sh`).

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh`: manifest of all 196 vendored files matches; CaDiCaL 3.0.1 (c6073042), cake_lpr
  (a36874a8) and lrat-check (2e3b2dc, E2 patch) built from `vendor/tools-src.tar.xz`. Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`): header `p cnf 838032 16653336`, sha256 of base.cnf
  `b0061e90…d8ff1` and base.json `2476faff…bf472b48`, both as required.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all eight byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 8 units: idx ≡ 1 mod 42)

| unit | case | kind | cap s | result | solve s | RSS MB | proof GB | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|---|---|
| P8_1-7 | P8 | Q | 6000 | certified | 5219.6 | 4378 | 9.92 | 136.8 | 708.1 |
| P6_1-2-4 | P6 | H | 1800 (run with 1211) | certified | 65.4 | 3146 | 1.12 | 22.3 | 147.1 |
| P6_1-7-9 | P6 | H | 1800 (run with 972) | certified | 314.6 | 4407 | 3.36 | 55.7 | 326.5 |
| P6_1-13 | P6 | Q | 2400 | not reached | | | | | |
| P6_2-8-13 | P6 | H | 1800 | not reached | | | | | |
| P6_3-7-11 | P6 | H | 1800 | not reached | | | | | |
| P6_7-10-12 | P6 | H | 1800 | not reached | | | | | |
| P6_8-12-14 | P6 | H | 1800 | not reached | | | | | |

The caps of the 2nd and 3rd units were lowered by lane.py to the time left before END minus 10 minutes; both
finished well inside them. The lane stopped at 08:48:05 UTC with 863 s left (< 15 min, no new unit).

Counts by case and kind:
- P8 Q: 1 certified (P8_1-7, the first-wave timeout, now closed in 5220 s at cap 6000).
- P6 H: 2 certified, 4 not reached.
- P6 Q: 1 not reached.
- Timed out (UNKNOWN): 0. Errors: 0. `certified: false`: 0.

Certified units (3): solve s min 65.4 / median 314.6 / max 5219.6; lrat-check s 22.3 / 55.7 / 136.8;
cake_lpr s 147.1 / 326.5 / 708.1 (all at heap 8000 MB); proof bytes 1.12 / 3.36 / 9.92 GB. Every proof was
accepted by both checkers (`c VERIFIED`, `s VERIFIED UNSAT`) and deleted.

Largest solver RSS: 4407 MB (P6_1-7-9). cake_lpr used about 8.3 GB RSS. No memory problem, no disk problem
(min free 18 GB), no SAT, no proof rejection.

Files: `out.jsonl` (records with CNF and proof sha256), `lane.log.tail`, `units.tsv`, `run.sh`, `tools.txt`, `env.txt`.
