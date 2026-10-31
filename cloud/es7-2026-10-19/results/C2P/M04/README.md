# C2P M04 (LIST = C2P.tsv, j = 4, N = 42, H = 3.0, Z = 01909a07)

Start 2026-10-31 03:23:33 UTC (epoch 1793417013); END = 1793426913 (06:08:33 UTC). The earlier M04 attempt (at fb2c59af), which stopped at step 1, was replaced. Machine: 4 cores, 15 GB (`env.txt`).

## Tools and checks (`tools.txt`)
- `vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) from `vendor/tools-src.tar.xz` in 33 s. All 196 manifest hashes matched. Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, and both sha256 values (base.cnf `b0061e90…`, base.json `2476faff…`) match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/`.

## Units (`units.tsv`, 54 units, idx ≡ 4 mod 42)
| | certified | timed out (UNKNOWN) | not reached |
|---|---|---|---|
| P8 H | 5 | 0 | 0 |
| P8 Q | 1 | 0 | 0 |
| P7 Q | 0 | 1 (P7_1-9, cap 2400) | 1 |
| P7 H | 0 | 0 | 4 |
| P1..P6 H | 0 | 0 | 33 (P1 6, P2 5, P3 6, P4 6, P5 5, P6 5) |
| P1..P6 Q | 0 | 0 | 8 (P1 1, P2 2, P3 1, P4 1, P5 2, P6 1) |
| P6 cover | 0 | 0 | 1 |
| **total** | **6** | **1** | **47** |

Certified units: P8_3-4-10, P8_2-5-11, P8_1-5-11, P8_1-5 (Q), P8_3-4-14 and P8_2-9-13. For all 6, lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT` at an 8000 MB heap, with no retries.

| certified (n = 6) | min | median | max |
|---|---|---|---|
| solve s | 302.2 | 484.8 | 2091.3 (P8_1-5, Q) |
| lrat-check s | 44.1 | 49.2 | 72.3 |
| cake_lpr s | 281.6 | 309.1 | 451.0 |
| proof size | 3.24 GB | 3.48 GB | 5.39 GB |

P7_1-9 (Q) reached its 2400 s cap (status UNKNOWN). The lane then stopped with 710 s left before END, since less than 15 minutes remained.

## Errors, SAT, rejection, memory
- Errors: none, and no record with `"certified": false`.
- SAT: none (no `SAT_FOUND`).
- Proof rejections: none.
- Memory: no problems. The largest solver RSS was 4417 MB (P7_1-9), and free memory never ran short.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (7 records), `lane.log.tail`.
