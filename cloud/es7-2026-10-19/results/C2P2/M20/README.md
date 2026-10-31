# C2P2 M20: shard j = 20 of N = 42 of `C2P2.tsv`, H = 2.5 h, task commit d266d2c3

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored `tools-src.tar.xz`; manifest: all 196 files match. Nothing was cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
One lane (`run.sh`), started 06:49:19Z, END = 09:04:19Z (start + 2.5 h − 15 min). The lane stopped at 08:54:24Z with 594 s left, so no further unit was started.

## Units (8 rows with idx ≡ 20 mod 42)
| idx | unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 | P7_1-5 | P7 | Q | 6000 | UNSAT, certified | 2075.05 | 82.0 | 452.1 | 6.02 | 4357 |
| 62 | P6_1-3-12 | P6 | H | 1800 | UNSAT, certified | 294.61 | 50.3 | 287.8 | 3.37 | 4400 |
| 104 | P6_1-9-12 | P6 | H | 1800 | UNSAT, certified | 316.48 | 49.7 | 284.8 | 3.38 | 4362 |
| 146 | P6_2-3-14 | P6 | H | 1800 | UNSAT, certified | 221.07 | 45.8 | 278.1 | 3.20 | 4361 |
| 188 | P6_2-11-12 | P6 | H | 1800 | UNSAT, certified | 289.31 | 48.9 | 283.2 | 3.27 | 4361 |
| 230 | P6_3-10 | P6 | Q | 2400 → 2372 (END-shortened) | UNKNOWN (timed out) | 2352.54 | – | – | – | 4415 |
| 272 | P6_7-14-15 | P6 | H | 1800 | not reached | | | | | |
| 314 | P6_10-11-13 | P6 | H | 1800 | not reached | | | | | |

Counts by case and kind:
- P7 Q: 1 certified.
- P6 H: 4 certified, 2 not reached (P6_7-14-15, P6_10-11-13).
- P6 Q: 1 timed out (P6_3-10, at 2372 s rather than the full 2400 s cap, because the lane shortens the last solve to keep 10 minutes for checks before END).
- Errors: none. Every certified record has `lrat_check` `c VERIFIED` and `cake_lpr` `s VERIFIED UNSAT`.

Certified units (5), min / median / max:
- solve: 221.07 / 294.61 / 2075.05 s
- lrat-check: 45.8 / 49.7 / 82.0 s
- cake_lpr: 278.1 / 284.8 / 452.1 s
- proof size: 3.20 / 3.37 / 6.02 GB (3198042882 / 3372653615 / 6021853861 bytes)

## Resources and problems
- Largest solver RSS: 4415 MB (P6_3-10). The largest cake_lpr RSS seen was about 8.2 GB (heap 8000 MB). No memory problem.
- Disk: free space never dropped below about 22 GB. The largest proof was 6.0 GB.
- No SAT, no proof rejection, no `certified: false` and no ERROR records.
