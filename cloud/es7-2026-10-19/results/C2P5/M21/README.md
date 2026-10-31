# C2P5 M21: list C2P5A.tsv, shard j = 21 of N = 37, H = 4.5 h (TASK commit 81cb025f)

**Result: all 5 units are certified UNSAT. There are no timeouts, unreached units, errors, SAT answers or proof rejections.**

## Tools and checks (`tools.txt`)
- The tools were built by `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz`. All 196 files matched `MANIFEST.sha256`. Nothing was cloned or downloaded.
  - CaDiCaL 3.0.1 (c6073042)
  - cake_lpr (a36874a8)
  - lrat-check (2e3b2dc, with the E2 patch)
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476fafff…) both match the expected values.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: rows of C2P5A.tsv with idx ≡ 21 mod 37)
The lane started at 18:52:32Z and finished at 19:49:51Z, with END = 1793487925 (23:05:25Z).

| idx | unit | kind | cap | status | solve s | RSS MB | proof bytes | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|---|---|
| 21 | P4_5-7 | Q | 8000 | certified | 528.32 | 4413 | 3501252295 | 59.3 | 331.3 |
| 58 | P4_2-5-14 | H | 2400 | certified | 425.03 | 4380 | 3591580589 | 57.7 | 346.0 |
| 95 | P4_2-9-10 | H | 2400 | certified | 301.64 | 4412 | 3271390865 | 60.0 | 323.4 |
| 132 | P4_5-10-13 | H | 2400 | certified | 251.70 | 4403 | 3277796534 | 56.1 | 316.7 |
| 169 | P4_6-11-13 | H | 2400 | certified | 110.02 | 3409 | 1395767489 | 30.0 | 184.3 |

Counts by case and kind:

| case | kind | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|
| P4 | Q | 1 | 0 | 0 | 0 |
| P4 | H | 4 | 0 | 0 | 0 |

For every unit, lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT`. Each proof was deleted after it was checked.

Over the 5 certified units (minimum / median / maximum):
- solve: 110.02 / 301.64 / 528.32 s
- lrat-check: 30.0 / 57.7 / 60.0 s
- cake_lpr: 184.3 / 323.4 / 346.0 s
- proof size: 1.40 / 3.28 / 3.59 GB

The largest solver RSS was 4413 MB (P4_5-7).

There were no SAT answers, no proof rejections, no `certified: false` records, no ERROR statuses and no memory problems. The machine has 15 GB of RAM and 4 cores.
