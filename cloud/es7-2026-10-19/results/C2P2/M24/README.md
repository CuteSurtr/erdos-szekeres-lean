# C2P2 M24 (LIST C2P2.tsv, j = 24, N = 42, H = 2.5, Z = d266d2c3)

Start 2026-10-31 06:47:01Z (epoch 1793429221), END = 1793437321 (09:02:01Z). One lane, `run.sh`.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources: manifest 196/196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…bf472b48` (both as expected).
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (7 rows: idx ≡ 24 mod 42)

| idx | unit | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| 24 | P7_1-10 | Q | 6000 | UNSAT, certified | 5330.7 | 146.5 | 742.5 | 9.43 GB | 4437.9 |
| 66 | P6_1-3-16 | H | 1800 (run cap 1074) | UNSAT, certified | 216.9 | 53.8 | 307.2 | 3.21 GB | 4399.2 |
| 108 | P6_1-9-16 | H | 1800 (run cap 486) | UNSAT, certified | 399.3 | 56.9 | 325.7 | 3.50 GB | 4414.9 |
| 150 | P6_2-4-7 | H | 1800 | not reached | | | | | |
| 192 | P6_2-11-16 | H | 1800 | not reached | | | | | |
| 234 | P6_3-11 | Q | 2400 | not reached | | | | | |
| 276 | P6_8-9-10 | H | 1800 | not reached | | | | | |

Counts:
- Certified 3: P7 Q 1 (P7_1-10, a first-wave full-cap timeout, now closed); P6 H 2.
- Timed out (UNKNOWN) 0. Errors 0. Proof rejections 0.
- Not reached 4: P6 H 3, P6 Q 1 (lane stopped at 08:57:07Z with 293 s left before END).

Certified units (n = 3), min / median / max:
- solve: 216.9 / 399.3 / 5330.7 s
- lrat-check: 53.8 / 56.9 / 146.5 s
- cake_lpr (heap 8000 MB, no retry needed): 307.2 / 325.7 / 742.5 s
- proof size: 3.21 / 3.50 / 9.43 GB (proofs deleted after checking; sizes and sha256 in `out.jsonl`)

Largest solver RSS: 4437.9 MB (P7_1-10); cake_lpr peaked about 8.2 GB. No memory problem (15 GB machine), disk peak about 21 GB used of the allowance.

No SAT, no proof rejection, no ERROR record.
