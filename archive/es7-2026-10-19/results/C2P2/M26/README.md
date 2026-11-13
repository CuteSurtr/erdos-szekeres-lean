# C2P2 M26 (LIST = C2P2.tsv, j = 26, N = 42, H = 2.5, TASK at d266d2c3)

Start 2026-10-31 06:47:19 UTC; lane END = start + 2.5 h - 15 min = 09:02:19 UTC (epoch 1793437339). One lane (`run.sh`), lane done at 08:52:22 UTC.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`).
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…2b48, both match.
- Cubes `C2C34/l2cubes.py` for a = 1..8: all byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (7: idx ≡ 26 mod 42)

| idx | unit | case | kind | cap (list / used) | status | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|---|---|---|---|
| 26 | P7_2-8 | P7 | Q | 6000 / 6000 | certified | 3609.5 | 120.9 | 625.7 | 8,088,567,859 |
| 68 | P6_1-4-7 | P6 | H | 1800 / 1800 | certified | 231.2 | 52.5 | 297.2 | 3,229,701,591 |
| 110 | P6_1-10-11 | P6 | H | 1800 / 1800 | certified | 276.6 | 53.5 | 305.4 | 3,252,742,416 |
| 152 | P6_2-4-9 | P6 | H | 1800 / 1706 | certified | 261.1 | 54.1 | 301.1 | 3,231,277,326 |
| 194 | P6_2-12-13 | P6 | H | 1800 / 1079 | certified | 288.5 | 56.4 | 306.5 | 3,262,176,586 |
| 236 | P6_7-8 | P6 | Q | 2400 / 417 | UNKNOWN (timed out at the time-limited cap 417 s, not the full 2400 s) | 413.2 | – | – | – |
| 278 | P6_8-9-12 | P6 | H | 1800 | not reached (596 s left < 900 s) | – | – | – | – |

Counts by case and kind:
- P7 Q: 1 certified.
- P6 H: 4 certified, 1 not reached (P6_8-9-12).
- P6 Q: 1 timed out at a reduced cap (P6_7-8; only 417 s of its 2400 s were available) — should be re-run with its full cap elsewhere.
- Errors / certified false: none.

Certified units (5): solve s min 231.2 / median 276.6 / max 3609.5; lrat-check s 52.5 / 54.1 / 120.9; cake_lpr s 297.2 / 305.4 / 625.7 (all with heap 8000 MB, no retry); proof bytes 3.23 GB / 3.25 GB / 8.09 GB.

Largest solver RSS: 4423 MB (P7_2-8). cake_lpr peaked at about 8.2 GB RSS on the 8.1 GB proof. Peak disk use during P7_2-8 was about 20 GB of 39 GB writable (proof 8.1 GB); no disk or memory problem.

No SAT, no proof rejection, no memory problem.
