# C2P / M08 (LIST C2P.tsv, shard 8 of 42, H = 3.0, Z = 01909a07)

Start 2026-10-31 03:22:55 UTC; END 06:07:55 UTC; lane ran 03:35–05:58 UTC. This is a restart: the earlier M08 attempt (Z = fb2c59af) stopped at step 1 and its files were replaced.

**Result: 8 units certified, 2 timed out (UNKNOWN), 44 not reached, 0 errors. No SAT, no proof rejection, no memory problem.**

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (drat-trim 2e3b2dc) with the E2 patch. Nothing was cloned or downloaded.
- Sanity checks: the cake_lpr example gives `s VERIFIED UNSAT`. Both checkers reject the bad LRAT and accept the good one.
- Base CNF: header `p cnf 838032 16653336`; both sha256 values match (base.cnf `b0061e90…`, base.json `2476faff…`).
- Cubes P1..P8: all 8 are byte-identical to `C2P/cubes/`.

## Units (`units.tsv`, idx ≡ 8 mod 42; 54 units, 43 H and 11 Q, no cover)

| case | kind | certified | timed out | not reached | errors |
|---|---|---|---|---|---|
| P8 | H | 4 | 0 | 0 | 0 |
| P8 | Q | 1 | 1 | 0 | 0 |
| P7 | H | 3 | 0 | 2 | 0 |
| P7 | Q | 0 | 1 | 0 | 0 |
| P6 | H / Q | 0 | 0 | 5 / 2 | 0 |
| P5 | H / Q | 0 | 0 | 6 / 1 | 0 |
| P4 | H / Q | 0 | 0 | 5 / 2 | 0 |
| P3 | H / Q | 0 | 0 | 6 / 1 | 0 |
| P2 | H / Q | 0 | 0 | 6 / 1 | 0 |
| P1 | H / Q | 0 | 0 | 6 / 1 | 0 |
| **all** | | **8** | **2** | **44** | **0** |

- Certified (both lrat-check and cake_lpr accepted): P8_2-5-16, P8_1-12-14, P8_1-2-7, P8_3-5 (Q), P8_3-11-12, P7_1-5-15, P7_1-2-9, P7_2-11-14.
- Timed out (UNKNOWN):
  - P8_1-10 (Q), at its full cap of 2400 s.
  - P7_9-10 (Q). Its cap was cut to 583 s by the END limit, so it did not get its full 2400 s.
- Not reached: the remaining 44 units of `units.tsv`, from P7_* (2 H) through P1.

Certified units, min / median / max:
- solve: 25.5 / 341 / 883 s
- lrat-check: 10.9 / 45.1 / 53.9 s
- cake_lpr: 115 / 299 / 344 s (heap 8000 MB every time; no retry)
- proof size: 0.22 / 3.27 / 3.92 GB (proofs deleted after checking; their sizes and sha256 are in `out.jsonl`)

Largest solver RSS: 4438 MB (P8_1-10). That is far below the 15 GB of the machine.

## SAT, proof rejection, memory
None.
