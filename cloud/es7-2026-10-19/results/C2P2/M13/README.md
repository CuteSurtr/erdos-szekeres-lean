# C2P2 M13

TASK `results/C2P2/TASK.md` (commit d266d2c3) with V = M13, LIST = C2P2.tsv, j = 13, N = 42, H = 2.5.
Start 2026-10-31 06:47:58 UTC (epoch 1793429278), END = 1793437378 (09:02:58 UTC). One lane (`run.sh`), 4 vCPU, 15 GB RAM.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch) built from the vendored sources only. Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…f2b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows with idx ≡ 13 mod 42: 8 units)

| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P8 | Q (cap 6000) | 1 | 1 | 0 | 0 | 0 |
| P6 | H (cap 1800) | 7 | 5 | 0 | 2 | 0 |
| total | | 8 | 6 | 0 | 2 | 0 |

Certified (both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`):

| unit | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P8_4-10 | Q | 6000 | 2972.1 | 87.2 | 527.0 | 6.41 | 4374 |
| P6_1-3-4 | H | 1800 | 67.6 | 20.8 | 155.1 | 1.11 | 3135 |
| P6_1-8-13 | H | 1800 | 633.5 | 53.3 | 321.1 | 3.68 | 4411 |
| P6_2-3-7 | H | 1800 | 232.3 | 45.1 | 288.0 | 3.19 | 4365 |
| P6_2-10-11 | H | 1800 | 333.9 | 47.9 | 298.4 | 3.27 | 4398 |
| P6_3-8-15 | H | 1220 (time-limited) | 647.6 | 51.9 | 345.9 | 3.72 | 4371 |

Min / median / max over the 6 certified units: solve 67.6 / 483.7 / 2972.1 s; lrat-check 20.8 / 49.9 / 87.2 s; cake_lpr 155.1 / 309.8 / 527.0 s; proof 1.11 / 3.48 / 6.41 GB.
H only (5 units): solve 67.6 / 333.9 / 647.6 s.

Not reached (lane stopped at 08:50:16 UTC with 761 s left before END, under the 15-minute rule): P6_7-12-13, P6_9-11-14.

Largest solver RSS: 4411 MB (P6_1-8-13); cake_lpr ran with an 8000 MB heap (about 8.2 GB RSS).

No SAT, no proof rejection, no `certified: false` record, no ERROR, no memory problem. Disk peaked at about 18 GB used (22 GB free) during the P8_4-10 proof.
