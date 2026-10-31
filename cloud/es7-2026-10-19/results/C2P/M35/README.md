# C2P / M35 (LIST C2P.tsv, shard j = 35 of N = 42, H = 3.0, Z = 01909a07)

Restart of the earlier attempt that stopped at step 1 (its files were replaced). Start 1793417019
(2026-10-31 03:23:39 UTC), END 1793426919 (06:08:39 UTC). One lane, `run.sh`.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8),
  lrat-check (2e3b2dc + E2 patch) built from the vendored sources, nothing downloaded or cloned.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`);
  cake_lpr example `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match.
- Cubes P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (53: 43 H, 10 Q, no cover)
| | certified | UNKNOWN | not reached |
|---|---|---|---|
| P8 | 5 H | – | – |
| P7 | 6 H, 1 Q | – | – |
| P6 | – | 1 Q (P6_2-7) | 5 H, 1 Q |
| P5 | – | – | 5 H, 1 Q |
| P4 | – | – | 5 H, 2 Q |
| P3 | – | – | 6 H, 1 Q |
| P2 | – | – | 6 H, 1 Q |
| P1 | – | – | 5 H, 2 Q |
| total | 12 (11 H, 1 Q) | 1 Q | 40 (32 H, 8 Q) |

- Every certified unit is UNSATISFIABLE with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- P6_2-7 (Q, list cap 2400 s) got a cap of only 855 s because END was near (lane cap = time left − 10 min);
  it ended UNKNOWN after 848 s. It is a short-cap timeout, not a hard result; re-run it at its full cap.
- Errors: none. No `"certified": false` record.

Certified units (12), min / median / max:
- solve: 29.2 / 262.2 / 1402.0 s (P7_8-12, the only Q, took 1402 s)
- lrat-check: 12.9 / 51.9 / 74.1 s
- cake_lpr: 114.3 / 296.3 / 400.6 s (heap 8000 MB)
- proof size: 0.22 / 3.24 / 4.93 GB (proofs deleted after checking)

Largest solver RSS: 4418 MB (P6_2-7); the largest among certified units was 4399 MB.

No SAT, no proof rejection, no memory problem.
