# C2P2 M00: shard j = 0 of N = 42 of C2P2.tsv (task commit d266d2c3, H = 2.5)

Started 2026-10-31 06:46:43Z (epoch 1793429203); lane END 1793437303 (09:01:43Z). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`; CaDiCaL 3.0.1, cake_lpr and lrat-check (E2 patch) built from `tools-src.tar.xz`, nothing downloaded or cloned. Sanity: the bad LRAT was rejected by both checkers, the good one accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 of base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes: `C2C34/l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 8 rows: idx 0, 42, …, 294)
| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P8_1-6 | P8 | Q | 6000 | UNSATISFIABLE | 3716.65 | 119.6 | 617.5 | 7.95 | 4372.8 | True |
| P6_1-2-3 | P6 | H | 1800 | UNSATISFIABLE | 71.74 | 24.1 | 159.4 | 1.11 | 3162.45 | True |
| P6_1-7-8 | P6 | H | 1800 | UNSATISFIABLE | 303.8 | 50.9 | 291.1 | 3.27 | 4411.48 | True |
| P6_1-12-16 | P6 | H | 1800 | UNSATISFIABLE | 242.64 | 51.7 | 299.7 | 3.25 | 4374.82 | True |
| P6_2-8-12 | P6 | H | 1329 | UNSATISFIABLE | 507.29 | 57.5 | 326.0 | 3.58 | 4366.76 | True |
| P6_3-7-10 | P6 | H | 424 | UNSATISFIABLE | 346.36 | 52.5 | 302.2 | 3.39 | 4393.65 | True |

- **Certified: 6** (1 P8 Q, 5 P6 H). Timed out (UNKNOWN): 0. Errors / certified false: 0.
- **Not reached: 2**: P6_7-10-11 (P6 H, cap 1800), P6_8-12-13 (P6 H, cap 1800). The lane stopped at 08:56:31Z with 311 s left (< 15 min).
- P8_1-6 (Q, timed out at its full cap in the first wave) is now certified: solve 3716.65 s, proof 7.95 GB, lrat-check 119.6 s, cake_lpr 617.5 s.
- Certified, min / median / max: solve s 71.74 / 325.08 / 3716.65; lrat-check s 24.1 / 52.1 / 119.6; cake_lpr s 159.4 / 300.95 / 617.5; proof GB 1.11 / 3.33 / 7.95.
- Caps of the last two units were shortened by the lane (1329 s and 424 s) because END was near; both still finished UNSAT and certified.
- Largest solver RSS: 4411.48 MB. cake_lpr ran with heap 8000 MB everywhere (no retry at 11000 MB).
- No SAT, no proof rejection, no memory problem. Disk: the 7.95 GB proof of P8_1-6 left about 20 GB free; no disk problem.
