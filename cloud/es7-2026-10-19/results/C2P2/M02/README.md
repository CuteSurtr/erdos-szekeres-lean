# C2P2 M02 — shard j=2 of N=42 of C2P2.tsv (H = 2.5 h, task commit d266d2c3)

## Tools and checks
- `C2P/vendor/build_tools.sh`: built from the vendored sources (manifest: all 196 files match) CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch). Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`. No code cloned or downloaded.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`): header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as required.
- Cubes: `l2cubes.py` for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; machine in `env.txt` (4 cores, 15 GB RAM).

## Units (8 assigned: idx 2, 44, 86, 128, 170, 212, 254, 296)
Lane started 06:50:15Z, END = 09:01:52Z (start + 2.5 h − 15 min).

| status | P8 Q | P6 H | P6 Q | total |
|---|---|---|---|---|
| certified UNSAT | 1 (P8_1-10) | 0 | 0 | 1 |
| timed out (UNKNOWN) | 0 | 0 | 0 | 0 |
| not reached | 0 | 6 | 1 | 7 |
| errors / uncertified | 0 | 0 | 0 | 0 |

Not reached (the first unit took the whole budget; lane stopped at 08:46:52Z with 899 s < 15 min left before END):
P6_1-2-5, P6_1-7-10, P6_1-13-14, P6_2-8-14, P6_3-7-12, P6_7-10-13 (H, cap 1800) and P6_8-13 (Q, cap 2400).

Certified unit (only one, so min = median = max):
- **P8_1-10** (Q, cap 6000, a first-wave full-cap timeout): UNSATISFIABLE in 5935.4 s solve (5990.8 s wall), just under the cap; proof 9,984,634,396 bytes (sha256 `d50827a7…d216`); lrat-check `c VERIFIED` in 161.0 s; cake_lpr `s VERIFIED UNSAT` in 823.5 s (heap 8000 MB). Proof deleted after checking.

## Resources and anomalies
- Largest solver RSS: 4437.5 MB (P8_1-10). No memory problem.
- No SAT, no proof rejection, no errors.
