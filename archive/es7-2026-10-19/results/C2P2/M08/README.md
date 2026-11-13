# C2P2 M08: shard j = 8 of N = 42 of C2P2.tsv (H = 2.5, TASK commit d266d2c3)

Lane start 06:49:20Z, END = 1793437306 (09:01:46Z); lane stopped 08:54:24Z (441 s left, no unit started).

## Tools and checks

- Built with `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match); CaDiCaL 3.0.1, cake_lpr, lrat-check (E2 patch). No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details and binary hashes: `tools.txt`; environment: `env.txt` (4 CPUs, 15 GB RAM).

## Units (8)

| idx | unit | case | kind | cap s | result | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 8 | P8_3-9 | P8 | Q | 6000 (run 6000) | certified | 3403.37 | 118.2 | 620.1 | 7.63 | 4413.55 |
| 50 | P6_1-2-13 | P6 | H | 1800 (run 1800) | certified | 284.94 | 52.8 | 305.2 | 3.26 | 4350.48 |
| 92 | P6_1-7-16 | P6 | H | 1800 (run 1800) | certified | 417.72 | 57.0 | 330.3 | 3.55 | 4369.54 |
| 134 | P6_1-15 | P6 | Q | 2400 (run 1684) | certified | 1320.18 | 77.3 | 420.7 | 4.74 | 4419.28 |
| 176 | P6_2-9-13 | P6 | H | 1800 | not reached | | | | | |
| 218 | P6_3-8-10 | P6 | H | 1800 | not reached | | | | | |
| 260 | P6_7-11-13 | P6 | H | 1800 | not reached | | | | | |
| 302 | P6_9-10-12 | P6 | H | 1800 | not reached | | | | | |

Counts by case and kind:

- P6 H: 2 certified
- P6 H: 4 not reached
- P6 Q: 1 certified
- P8 Q: 1 certified

Total: 4 certified, 0 timed out (UNKNOWN), 4 not reached, 0 errors.

Certified units (min / median / max):

- solve s: 284.9 / 869.0 / 3403.4
- lrat-check s: 52.8 / 67.2 / 118.2
- cake_lpr s: 305.2 / 375.5 / 620.1 (heap 8000 MB for all)
- proof bytes: 3262701066 / 4142313709 / 7627239738

Largest solver RSS: 4419.28 MB (P6_1-15).

## Notable

- P8_3-9 (Q, a first-wave full-cap timeout) is certified at cap 6000: solve 3403 s, proof 7.6 GB.
- No SAT, no proof rejection, no `certified: false` record, no ERROR status, no memory problem (peak cake_lpr ≈ 8.2 GB RSS, solver ≤ 4.4 GB; disk never below 20 GB free).
- Not reached (time budget): P6_2-9-13, P6_3-8-10, P6_7-11-13, P6_9-10-12 (all H, cap 1800).

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.
