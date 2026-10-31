# C2P / M18 (LIST C2P.tsv, shard 18 of 42, H = 3.0, Z = 01909a07)

Restart of an earlier M18 attempt (TASK at fb2c59af) that stopped at step 1; its files were replaced.
Start 2026-10-31T03:23:17Z, END 06:08:17Z (`run.sh`). One lane, 4 cores / 15 GB.

## Tools and checks (`tools.txt`)
- `vendor/build_tools.sh`: manifest of 196 vendored files matches. Built CaDiCaL c6073042 (3.0.1),
  cake_lpr a36874a8 and lrat-check 2e3b2dc with the E2 patch. Nothing was downloaded.
- Sanity checks: both checkers reject the bad LRAT and accept the good one. The cake_lpr example gives `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. Both sha256 match (base.cnf b0061e90…, base.json 2476faff…).
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (53: 44 H, 9 Q, no cover; `units.tsv`, records in `out.jsonl`)
| case | certified | UNKNOWN (timeout) | not reached |
|---|---|---|---|
| P8 | 5 H | – | – |
| P7 | 6 H | 1 Q (P7_2-8, cap 2400 s, solve 2380 s) | – |
| P1 | – | – | 6 H, 1 Q |
| P2 | – | – | 5 H, 1 Q |
| P3 | – | – | 6 H, 1 Q |
| P4 | – | – | 5 H, 2 Q |
| P5 | – | – | 6 H, 1 Q |
| P6 | – | – | 5 H, 2 Q |
| **total** | **11 (11 H)** | **1 (1 Q)** | **41 (33 H, 8 Q)** |

Errors: none. Every UNSAT record has `certified: true`: lrat-check gave `c VERIFIED` and cake_lpr gave
`s VERIFIED UNSAT`, both at heap 8000 MB.

The lane stopped at 06:03:15Z with 301 s left, after the last unit P7_3-10-13. Its solve cap had been cut to 455 s,
and it finished in 377 s.

Certified units, min / median / max:
- solve 20.0 / 291.7 / 519.3 s
- lrat-check 11.6 / 50.9 / 55.1 s
- cake_lpr 105.3 / 296.8 / 319.7 s
- LRAT proof 0.21 / 3.34 / 3.71 GB (all proofs were deleted after checking)

## Memory, SAT, rejections
- Largest solver RSS was 4424 MB, on P7_2-8. cake_lpr peaked at about 8.2 GB RSS (8000 MB heap).
  No memory problem.
- No SAT, no proof rejection.
