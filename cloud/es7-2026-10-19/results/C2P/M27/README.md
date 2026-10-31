# C2P / M27 (LIST C2P.tsv, shard 27 of 42, H = 3.5, Z = fb2c59af)

**Result: 11 units certified UNSAT, 1 timed out (UNKNOWN), 41 not reached. No SAT, no proof rejection, no error, no memory problem.**

## Tools and checks (`tools.txt`)
- CaDiCaL 3.0.1 c60730422e75 (`./configure && make -j4`); cake_lpr a36874a8b750 (`make cake_lpr`); drat-trim lrat-check 2e3b2dc0ecf9 with `results/E2/tools/lrat-check-E2.patch`.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; on {1},{-1} the LRAT `3 0 0` is rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all 8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Lane: `C2P/tools/lane.py` at fb2c59af, unmodified (`run.sh`); 03:00:06 to 06:06:49 UTC, END 1793427118 (06:11:58 UTC).

## Units (53 rows of C2P.tsv with idx ≡ 27 mod 42; `units.tsv`, records in `out.jsonl`)

| case | kind | units | certified | UNKNOWN | not reached |
|---|---|---|---|---|---|
| P8 | H | 3 | 3 | 0 | 0 |
| P8 | Q | 2 | 1 | 1 | 0 |
| P7 | H | 6 | 6 | 0 | 0 |
| P7 | Q | 1 | 1 | 0 | 0 |
| P6 | H/Q | 6/1 | 0 | 0 | 7 |
| P5 | H/Q | 6/1 | 0 | 0 | 7 |
| P4 | H/Q | 6/1 | 0 | 0 | 7 |
| P3 | H/Q | 4/2 | 0 | 0 | 6 |
| P2 | H/Q | 6/1 | 0 | 0 | 7 |
| P1 | H/Q | 5/2 | 0 | 0 | 7 |
| **total** | | **53** (45 H, 8 Q, no cover) | **11** (9 H, 2 Q) | **1** (Q) | **41** (33 H, 8 Q) |


- Certified (11): P8_1-13-14, P8_2-5-14, P8_2-5, P8_4-11-12, P7_8-11-15, P7_3-8-10, P7_3-16, P7_3-10-12, P7_8-9-14, P7_1-2-4, P7_3-12-16.
- Timed out (UNKNOWN): **P8_2-10** (Q, cap 2400 s, stopped at 2377.7 s).
- Not reached: all 41 units of P6, P5, P4, P3, P2, P1 in `units.tsv`.
- Errors / `"certified": false`: none.

## Certified units: min / median / max
- solve: 24.7 / 311.4 / 1500.0 s (Q units: 967.3 and 1500.0 s)
- lrat-check: 12.9 / 54.0 / 80.6 s
- cake_lpr: 111.4 / 308.0 / 445.8 s
- proof size (LRAT text): 0.21 / 3.30 / 5.10 GB (214,855,250 / 3,295,287,172 / 5,101,986,228 bytes)

## Memory
Largest solver RSS 4414 MB (P7_3-16). cake_lpr heap 8000 MB. No memory problem.

## SAT / rejections
No SAT answer, no proof rejected by either checker.
