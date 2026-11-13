# C2P2 M07: shard j = 7 of N = 42 of C2P2.tsv (task commit d266d2c3, H = 2.5 h)

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (no clone or download): all 196 files match
  `MANIFEST.sha256`; CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both checkers, good LRAT accepted by both.
- Base CNF `p cnf 838032 16653336`, sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…bf472b48: both match.
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`. Details in `tools.txt`.

## Units (8 in `units.tsv`; one lane, END = start + 2.25 h)
| unit | case | kind | status | cap given (s) | solve (s) | lrat-check (s) | cake_lpr (s) | proof (GB) |
|---|---|---|---|---|---|---|---|---|
| P8_2-12 | P8 | Q | certified | 6000 | 4043.15 | 118.1 | 633.8 | 7.87 |
| P6_1-2-12 | P6 | H | certified | 1800 | 293.84 | 53.0 | 299.2 | 3.26 |
| P6_1-7-15 | P6 | H | certified | 1800 | 442.66 | 57.8 | 325.7 | 3.62 |
| P6_1-14-16 | P6 | H | certified | 1023 (time-limited) | 217.24 | 51.5 | 297.2 | 3.19 |
| P6_2-9-11 | P6 | H | certified | 448 (time-limited) | 340.01 | 54.7 | 321.1 | 3.36 |
| P6_3-8 | P6 | Q | not reached | | | | | |
| P6_7-11-12 | P6 | H | not reached | | | | | |
| P6_9-10-11 | P6 | H | not reached | | | | | |

Counts: certified 5 (P8 Q 1; P6 H 4), timed out (UNKNOWN) 0, errors 0, not reached 3 (P6 Q 1, P6 H 2).

Certified units, min / median / max: solve 217.2 / 340.0 / 4043.2 s; lrat-check 51.5 / 54.7 / 118.1 s;
cake_lpr 297.2 / 321.1 / 633.8 s; proof 3.19 / 3.36 / 7.87 GB. Every record has `"certified": true`
(lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`).

Largest solver RSS: 4385 MB (cake_lpr ran with an 8000 MB heap, about 8 GB RSS). Disk peaked near 19 GB used of ~29 GB.

No SAT, no proof rejection, no memory or disk problem. P8_2-12, the first-wave timeout, closed in 4043 s under the 6000 s cap.
