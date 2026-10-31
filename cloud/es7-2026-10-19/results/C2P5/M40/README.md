# C2P5 M40

Machine M40, list `C2P5C.tsv`, shard j = 3 of N = 13, budget H = 4.5 h, TASK commit 81cb025f.
The lane started at 20:09:00Z on 2026-10-31 with END = 1793492495 (2026-11-01 00:21:35Z). It finished both units by 20:32:49Z.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- Built `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz`, with no clone or download. The manifest check matched all 196 files.
  - CaDiCaL 3.0.1 (c6073042)
  - cake_lpr (a36874a8)
  - lrat-check (2e3b2dc, E2 patch)
- Sanity checks as expected:
  - Both checkers rejected the bad LRAT.
  - Both checkers accepted the good LRAT (`c VERIFIED`, `s VERIFIED UNSAT`).
  - The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF matched what TASK requires:
  - header `p cnf 838032 16653336`
  - sha256 `b0061e90…d8ff1` (base.cnf) and `2476faff…f2b48` (base.json)
- Cubes P1..P8 from `C2C34/l2cubes.py` were byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows idx ≡ 3 mod 13 of C2P5C.tsv)

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P3_1-5-16 | P3 | H | 2400 | UNSAT, certified | 384.47 | 57.9 | 341.7 | 3.54 GB | 4390.7 |
| P3_5-7-13 | P3 | H | 2400 | UNSAT, certified | 232.58 | 56.6 | 330.0 | 3.19 GB | 4367.5 |

Totals:
- certified: 2 (P3 H: 2)
- timed out (UNKNOWN): 0
- not reached: 0
- errors: 0

Certified-unit statistics (min / median / max):
- solve: 232.58 / 308.53 / 384.47 s
- lrat-check: 56.6 / 57.25 / 57.9 s
- cake_lpr: 330.0 / 335.85 / 341.7 s
- proof size: 3,193,589,386 / 3,368,194,075 / 3,542,798,764 bytes

Largest solver RSS: 4390.7 MB. cake_lpr ran with an 8000 MB heap and peaked at about 8.2 GB RSS.

There was no SAT result, no proof rejection and no memory problem. Each proof was deleted after both checks. No CNF or proof files are committed.
