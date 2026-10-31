# C2P5 M88: LIST = C2P5B.tsv, shard j = 38 of N = 50, H = 5.25 (TASK commit 81cb025f)

**Result: all 14 units certified UNSAT (lrat-check and cake_lpr both accepted). No SAT, no timeouts, no errors, no proof rejections, no memory problems.**

Start 2026-10-31T15:10:26Z, END 1793477426 (20:10:26Z). Lane started 15:13:26Z and finished all units at 19:13:10Z ("lane done").

## Tools and checks (details in `tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check with the E2 patch (2e3b2dc). No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, base.cnf sha256 b0061e90…d8ff1, base.json sha256 2476faff…bf472b48 (both as expected).
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (rows of C2P5B.tsv with idx ≡ 38 mod 50)

| case | kind | outcome | n |
|---|---|---|---|
| P1 | H | certified | 4 |
| P1 | Q | certified | 1 |
| P2 | H | certified | 6 |
| P2 | Q | certified | 1 |
| P3 | Q | certified | 2 |

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P2_5-13 | P2 | Q | 8000 | UNSATISFIABLE | 1955.84 | 94.7 | 469.1 | 5.14 | 4488.44 | True |
| P1_4-11 | P1 | Q | 8000 | UNSATISFIABLE | 1671.11 | 82.5 | 480.7 | 4.75 | 4376.04 | True |
| P2_1-5-8 | P2 | H | 2400 | UNSATISFIABLE | 318.23 | 65.3 | 355.2 | 3.27 | 4409.42 | True |
| P2_3-5-9 | P2 | H | 2400 | UNSATISFIABLE | 80.96 | 25.7 | 174.0 | 1.12 | 3156.87 | True |
| P2_3-9-13 | P2 | H | 2400 | UNSATISFIABLE | 452.74 | 60.2 | 369.7 | 3.47 | 4372.61 | True |
| P2_4-7-8 | P2 | H | 2400 | UNSATISFIABLE | 31.27 | 14.7 | 141.6 | 0.22 | 2652.09 | True |
| P2_5-6-14 | P2 | H | 2400 | UNSATISFIABLE | 335.82 | 57.0 | 358.9 | 3.26 | 4366.27 | True |
| P2_6-9-12 | P2 | H | 2400 | UNSATISFIABLE | 22.2 | 13.7 | 124.0 | 0.22 | 2645.32 | True |
| P1_2-5-16 | P1 | H | 2400 | UNSATISFIABLE | 396.32 | 60.5 | 373.9 | 3.51 | 4378.38 | True |
| P1_3-4-5 | P1 | H | 2400 | UNSATISFIABLE | 34.6 | 14.2 | 129.3 | 0.22 | 2654.25 | True |
| P1_3-9-15 | P1 | H | 2400 | UNSATISFIABLE | 604.08 | 64.9 | 392.9 | 3.67 | 4368.64 | True |
| P1_4-11-13 | P1 | H | 2400 | UNSATISFIABLE | 297.15 | 67.7 | 373.7 | 3.28 | 4408.15 | True |
| P3_1-7 | P3 | Q | 6499 | UNSATISFIABLE | 2148.89 | 104.8 | 615.2 | 5.45 | 4413.35 | True |
| P3_9-10 | P3 | Q | 3594 | UNSATISFIABLE | 381.14 | 55.4 | 310.7 | 3.29 | 4375.81 | True |

Certified (14), min / median / max:
- solve s: 22.20 / 358.48 / 2148.89
- lrat-check s: 13.70 / 60.35 / 104.80
- cake_lpr s: 124.00 / 364.30 / 615.20
- proof GB: 0.22 / 3.29 / 5.45
- largest solver RSS: 4488 MB (P2_5-13)
- cake_lpr heaps used: [8000]
- non-certified non-UNKNOWN records: none

Unit P3_1-7 ran with cap 6499 s and P3_9-10 with cap 3594 s (the lane trimmed the caps against END); both finished well inside them.

## Problems
None. No `SAT_FOUND`, every record `"certified": true`, all cake_lpr runs succeeded at the first heap (8000 MB), and the peak solver RSS was 4.5 GB of 15 GB. Largest proof 5.45 GB; free disk never fell below 22 GB.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.
