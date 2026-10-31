# C2P5 M54

Task `results/C2P5/TASK.md` at commit 81cb025f, with V = M54, LIST = C2P5B.tsv, j = 4, N = 50, H = 5.25.
Started 2026-10-31 15:09 UTC (epoch 1793459387). END = 1793477387 (20:09:47 UTC). The lane finished at 18:41:50 UTC.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest check passed (all 196 files match). The script built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc with the E2 patch) from the vendored sources. No code was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. base.cnf sha256 b0061e90…d8ff1 and base.json sha256 2476faff…2b48 both match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: rows of C2P5B.tsv with idx ≡ 4 mod 50, 14 units)

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | Q | 2 | 2 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| all | | 14 | 14 | 0 | 0 | 0 |

Every unit is UNSATISFIABLE. Both checkers accepted every proof: lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`.

| unit | case | kind | cap s | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P2_1-7 | P2 | Q | 8000 | 1951.06 | 86.3 | 486.0 | 5.15 GB | 4430.35 |
| P2_8-11 | P2 | Q | 8000 | 492.95 | 64.8 | 354.8 | 3.38 GB | 4374.96 |
| P1_6-11 | P1 | Q | 8000 | 951.99 | 70.6 | 402.5 | 3.94 GB | 4372.68 |
| P1_2-3-5 | P1 | H | 2400 | 87.5 | 27.8 | 176.4 | 1.15 GB | 3171.0 |
| P1_2-7-13 | P1 | H | 2400 | 508.6 | 71.0 | 379.9 | 3.56 GB | 4369.91 |
| P1_3-5-11 | P1 | H | 2400 | 126.05 | 31.9 | 203.7 | 1.43 GB | 3415.64 |
| P1_4-5-11 | P1 | H | 2400 | 94.42 | 30.7 | 199.1 | 1.25 GB | 3194.43 |
| P1_5-8-10 | P1 | H | 2400 | 21.92 | 13.7 | 127.1 | 0.22 GB | 2647.45 |
| P3_4-11 | P3 | Q | 8000 | 2059.13 | 101.3 | 525.5 | 5.23 GB | 4423.95 |
| P3_1-4-12 | P3 | H | 2400 | 465.44 | 63.8 | 374.9 | 3.57 GB | 4383.63 |
| P3_1-9-11 | P3 | H | 2400 | 362.96 | 61.0 | 373.6 | 3.32 GB | 4469.6 |
| P3_4-6-13 | P3 | H | 2400 | 320.69 | 59.6 | 361.4 | 3.25 GB | 4408.14 |
| P3_5-6-7 | P3 | H | 2400 | 29.26 | 14.3 | 125.1 | 0.21 GB | 2652.97 |
| P3_6-7-11 | P3 | H | 2400 | 27.93 | 14.7 | 120.5 | 0.22 GB | 2649.2 |

Certified units, min / median / max:
- solve: 21.92 / 341.825 / 2059.13 s
- lrat-check: 13.7 / 60.3 / 101.3 s
- cake_lpr: 120.5 / 358.1 / 525.5 s
- proof size: 0.21 GB / 3.28 GB / 5.23 GB

## Resources and anomalies
- Largest solver RSS: 4469.6 MB (unit P3_1-9-11). There were no memory problems.
- The largest proof was 5.2 GB. Free disk never fell below about 23 GB.
- No SAT, no proof rejection, no ERROR status and no uncertified record.

