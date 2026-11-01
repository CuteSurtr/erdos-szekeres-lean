# C2P5 M64: list C2P5B.tsv, shard 14 of 50

Task `results/C2P5/TASK.md` at commit 81cb025f with V = M64, LIST = C2P5B.tsv, j = 14, N = 50, H = 5.25.
Start 2026-10-31 15:12:26 UTC (epoch 1793459546), END = 1793477546 (20:12:26 UTC). The lane finished all units at 19:46:01 UTC.

## Tools and checks (`tools.txt`)

- Built by `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (all 196 manifest hashes match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity: the bad LRAT is rejected by both checkers, the good one is accepted by both; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476fafff…bf472b48`, both as expected.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19 = rows of C2P5B.tsv with idx ≡ 14 mod 50)

All 19 are **certified** (UNSATISFIABLE; lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`). None timed out, none was left unreached, and there were no errors.

| case | Q certified | H certified |
|---|---|---|
| P2 | 1 (P2_3-11) | 6 |
| P1 | 1 (P1_2-11) | 5 |
| P3 | 1 (P3_5-10) | 5 |
| total | 3 | 16 |

The lane cut P3_5-10's cap to 5596 s, P3_4-7-14's to 2067 s and P3_6-9-10's to 1133 s because END was close. All three still finished well inside those caps.

Certified units, as min / median / max:

| | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| Q (3) | 1348.5 / 1629.3 / 1644.5 | 76.0 / 78.6 / 90.1 | 398.6 / 448.4 / 464.1 | 4.58 / 4.97 / 5.03 |
| H (16) | 25.2 / 304.4 / 537.4 | 13.0 / 56.7 / 63.3 | 109.5 / 323.8 / 375.5 | 0.22 / 3.31 / 3.73 |
| all (19) | 25.2 / 334.6 / 1644.5 | 13.0 / 58.6 / 90.1 | 109.5 / 335.1 / 464.1 | 0.22 / 3.37 / 5.03 |

Per-unit records are in `out.jsonl`.

## Other

- Largest solver RSS: 4433 MB (P1_2-11). The largest cake_lpr resident memory seen was about 8.2 GB (heap 8000 MB).
- No SAT, no proof rejection, no memory problem. Disk usage peaked at about 17 GB used, with 23 GB free.
