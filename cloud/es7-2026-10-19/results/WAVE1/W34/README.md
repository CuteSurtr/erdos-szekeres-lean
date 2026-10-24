# W34 — wave 1, mirror sub-case (ii), entry kind "cases" (68 cases)

**Result: 24 cases closed, 4 started but still open, 40 not started. No SAT answers.**

## What ran where
- One cloud VM: Linux x86_64, 4 cores, 15 GB RAM (`env.txt`). The run went from 06:56 to 10:28 UTC.
- Tools (`tools.txt`): CaDiCaL c6073042 (master), march_cu from CnC 705b60c6 (built with `-fcommon`), and cake_lpr
  a36874a8. The bundled cake_lpr example prints `s VERIFIED UNSAT`.
- Driver: `run_w34.py`, adapted from `results/Mii-S/scripts/close_march.py` (the original is copied to `close_march.orig.py`).
  It keeps one global queue on 4 workers, and cases earlier in the listed order go first. Each case runs in three steps:
  1. Plain CaDiCaL for 60 s with `--lrat` on the whole case. An UNSAT counts only with cake_lpr `s VERIFIED UNSAT`.
  2. Otherwise `march_cu CASE -d 7` makes the top cubes. They are saved as `<case>/top.icnf`; the record has the cube count,
     the refuted count and the sha256.
  3. Each cube runs CaDiCaL with a 300 s timeout and `--lrat`, and every UNSAT is checked by cake_lpr. A cube that times out
     is split with `march_cu -d 6`.
- The run can resume: the driver rebuilds its state from `leaves.jsonl` and `top.icnf`. The stop time was 10:28 UTC.
  `driver.log` is empty apart from the final line (no errors). `summary.json` holds every number below.

## sha256 checks (`hashes.txt`, `assign.json`)
- `m33k7int.sub.cnf` was regenerated (gen_etv 33 7 7 7 --mirror; mirgen --interior --yflip-unit) and matches:
  69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d.
- `verify/ii_wave1.json` 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e: OK.
  `Mii-S/cases.jsonl` bf77e23c...: OK.
- All 68 case CNFs built with `hullsplit.py case` match the W34 entry and cases.jsonl.

## Files per case (`<case>/`)
- `leaves.jsonl`: every record (whole attempt, top, cubes, splits with their children).
- `leaves.icnf`: only the leaves with cake_lpr `s VERIFIED UNSAT`, relative to the case CNF. A whole-case closure is `a 0`.
- `open.icnf`: the cubes still open.
- `top.icnf`: the march -d 7 top cubes.
No CNF or LRAT files are committed (proofs were deleted after checking).

## Per case
"cover" is `covercheck.py leaves.icnf`. "cover+open" is `covercheck.py leaves.icnf open.icnf`, a consistency check that the
open cubes are exactly the rest of the case. No record has an UNSAT without `s VERIFIED UNSAT`, so cake_lpr covers 100% of
the leaves. CPU is the sum of solve, check and march wall times per job.

| # | case | state | method | top cubes (refuted) | verified leaves | splits | open | cover | cover+open | CPU s | CNF sha256 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | U10_L7 | **CLOSED** | close_march | 128 (0) | 128 | 0 | 0 | COVERED | COVERED | 1043 | `41e676c57d30172e…` |
| 1 | U_L2-4 | **CLOSED** | close_march | 128 (0) | 379 | 4 | 0 | COVERED | COVERED | 10973 | `081c41c1aa74e5c4…` |
| 2 | U_L2-7 | **CLOSED** | close_march | 125 (3) | 377 | 4 | 0 | COVERED | COVERED | 8232 | `f76ee990689cd20c…` |
| 3 | U_L2-11 | **CLOSED** | close_march | 124 (2) | 124 | 0 | 0 | COVERED | COVERED | 2131 | `61d093828f5f745a…` |
| 4 | U_L2-14 | **CLOSED** | close_march | 128 (0) | 128 | 0 | 0 | COVERED | COVERED | 2276 | `be0eb78d84326b2c…` |
| 5 | U3-5_L | **CLOSED** | close_march | 122 (2) | 247 | 2 | 0 | COVERED | COVERED | 7772 | `75e1bcbefb5c578e…` |
| 6 | U3-8_L | **CLOSED** | close_march | 128 (0) | 128 | 0 | 0 | COVERED | COVERED | 2775 | `287f06f94215e784…` |
| 7 | U3-11_L | **CLOSED** | close_march | 128 (0) | 128 | 0 | 0 | COVERED | COVERED | 2131 | `742bf58a41f55315…` |
| 8 | U3-14_L | **CLOSED** | close_march | 127 (1) | 127 | 0 | 0 | COVERED | COVERED | 2405 | `25ef5307af30c825…` |
| 9 | U4-6_L | **CLOSED** | close_march | 128 (0) | 128 | 0 | 0 | COVERED | COVERED | 1416 | `e5c33fd4ec6daa44…` |
| 10 | U_L4-7 | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 49 | `4aca76fc6d024e6d…` |
| 11 | U4-9_L | **CLOSED** | close_march | 103 (18) | 103 | 0 | 0 | COVERED | COVERED | 1313 | `6f9a6c9f7e9858b8…` |
| 12 | U4-11_L | **CLOSED** | close_march | 118 (8) | 118 | 0 | 0 | COVERED | COVERED | 1468 | `7aef39be65c8c4b2…` |
| 13 | U4-13_L | **CLOSED** | close_march | 96 (16) | 96 | 0 | 0 | COVERED | COVERED | 1012 | `c4cecbbb3f9655f4…` |
| 14 | U_L4-14 | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 35 | `6d5982c326758b0a…` |
| 15 | U5-6_L | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 40 | `c9affc9eba35dd79…` |
| 16 | U_L5-7 | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 26 | `fc2cb4472ea5da76…` |
| 17 | U5-9_L | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 40 | `0cb40ca2b57a2dc4…` |
| 18 | U_L5-10 | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 21 | `f0220ebea391d38d…` |
| 19 | U_L5-12 | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 22 | `88b18f7af5d89f45…` |
| 20 | U_L5-14 | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 25 | `527c39bb0d1dfda3…` |
| 21 | U_L5-16 | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 22 | `aaa1b402a8c9baf6…` |
| 22 | U6-10_L | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 22 | `db2f312ea46e2dfb…` |
| 23 | U6-15_L | **CLOSED** | whole cadical 60s | - | 1 | 0 | 0 | COVERED | COVERED | 20 | `0c2b8910f670c31c…` |
| 24 | U3_L5 | **OPEN** | close_march | 123 (3) | 65 | 0 | 58 | NOT | COVERED | 2086 | `677daf53a7fba5fd…` |
| 25 | U3_L9 | **OPEN** | close_march | 125 (1) | 93 | 0 | 32 | NOT | COVERED | 1121 | `a140d67e032a0118…` |
| 26 | U3_L13 | **OPEN** | close_march | 127 (1) | 0 | 0 | 127 | - | COVERED | 485 | `d5d61f5d85a89106…` |
| 27 | U4_L2 | **OPEN** | close_march | 128 (0) | 0 | 0 | 128 | - | COVERED | 398 | `abbb78a38138b8a3…` |
| 28 | U4_L8 | not started | - | - | - | - | whole | - | - | 0 | `f911b34ab8872a5a…` |
| 29 | U4_L13 | not started | - | - | - | - | whole | - | - | 0 | `9b8c5773d8fee200…` |
| 30 | U5_L2 | not started | - | - | - | - | whole | - | - | 0 | `d011c0d3790f5645…` |
| 31 | U5_L8 | not started | - | - | - | - | whole | - | - | 0 | `f886d5c7def6c32d…` |
| 32 | U5_L14 | not started | - | - | - | - | whole | - | - | 0 | `051b29d9aa2d0944…` |
| 33 | U6_L7 | not started | - | - | - | - | whole | - | - | 0 | `182be1fd03cc2810…` |
| 34 | U6_L11 | not started | - | - | - | - | whole | - | - | 0 | `4f371489645ea81a…` |
| 35 | U7_L2 | not started | - | - | - | - | whole | - | - | 0 | `c4c67a045375816d…` |
| 36 | U7_L9 | not started | - | - | - | - | whole | - | - | 0 | `115cd608c561aef3…` |
| 37 | U7_L14 | not started | - | - | - | - | whole | - | - | 0 | `8029b51cbc0518a7…` |
| 38 | U8_L4 | not started | - | - | - | - | whole | - | - | 0 | `35e0a411c0863fd4…` |
| 39 | U8_L11 | not started | - | - | - | - | whole | - | - | 0 | `d4351e1ffe158baa…` |
| 40 | U9_L2 | not started | - | - | - | - | whole | - | - | 0 | `388407e393036f6e…` |
| 41 | U9_L12 | not started | - | - | - | - | whole | - | - | 0 | `aa1943829e9dff43…` |
| 42 | U9_L16 | not started | - | - | - | - | whole | - | - | 0 | `4a5f6a508f1a6f8f…` |
| 43 | U10_L6 | not started | - | - | - | - | whole | - | - | 0 | `b1d2080b3359849a…` |
| 44 | U10_L12 | not started | - | - | - | - | whole | - | - | 0 | `a49a1a8ee65cac9f…` |
| 45 | U10_L16 | not started | - | - | - | - | whole | - | - | 0 | `222a236988fe6051…` |
| 46 | U11_L7 | not started | - | - | - | - | whole | - | - | 0 | `21655eec4eb8ab51…` |
| 47 | U11_L12 | not started | - | - | - | - | whole | - | - | 0 | `efdd078d99c71e4c…` |
| 48 | U11_L16 | not started | - | - | - | - | whole | - | - | 0 | `d7eba12c5d24f766…` |
| 49 | U12_L8 | not started | - | - | - | - | whole | - | - | 0 | `3d437ea9e6d03476…` |
| 50 | U13_L2 | not started | - | - | - | - | whole | - | - | 0 | `0b97bf91e121fcb5…` |
| 51 | U13_L7 | not started | - | - | - | - | whole | - | - | 0 | `236d7c018afc24ee…` |
| 52 | U14_L2 | not started | - | - | - | - | whole | - | - | 0 | `958298bab41721c5…` |
| 53 | U14_L8 | not started | - | - | - | - | whole | - | - | 0 | `17d405efd503e379…` |
| 54 | U15_L2 | not started | - | - | - | - | whole | - | - | 0 | `447c1bffda0db049…` |
| 55 | U15_L8 | not started | - | - | - | - | whole | - | - | 0 | `8f43b73987827335…` |
| 56 | U16_L5 | not started | - | - | - | - | whole | - | - | 0 | `951a2b019d0f4fe1…` |
| 57 | U16_L9 | not started | - | - | - | - | whole | - | - | 0 | `f23d7cc4f8512afb…` |
| 58 | U5_L15 | not started | - | - | - | - | whole | - | - | 0 | `3821d2b7b16397bc…` |
| 59 | U4_L10 | not started | - | - | - | - | whole | - | - | 0 | `ad8dd1313dcfce89…` |
| 60 | U12_L2 | not started | - | - | - | - | whole | - | - | 0 | `b9682378a8d04291…` |
| 61 | U8_L6 | not started | - | - | - | - | whole | - | - | 0 | `8b9a7b2623919b41…` |
| 62 | U12_L9 | not started | - | - | - | - | whole | - | - | 0 | `06fc299e03c39789…` |
| 63 | U3-15_L | not started | - | - | - | - | whole | - | - | 0 | `807503f07d05b9ac…` |
| 64 | U_L4-10 | not started | - | - | - | - | whole | - | - | 0 | `29d071af222928e8…` |
| 65 | U15_L9 | not started | - | - | - | - | whole | - | - | 0 | `0ca18e6bc3cfb617…` |
| 66 | U13_L11 | not started | - | - | - | - | whole | - | - | 0 | `b629c081a1ebeb48…` |
| 67 | U16_L11 | not started | - | - | - | - | whole | - | - | 0 | `b0e1e462d17adc59…` |

Totals: 24 closed (11 by the whole-case 60 s run, 13 by close_march),
2222 verified leaves in closed cases, and about 13.7 core-hours.
The full CNF and top-cube sha256 values are in `summary.json`.

## Still open (to hand on)
- **U3_L5, U3_L9, U3_L13, U4_L2**: the top cubes and part of the leaves are done. `open.icnf` lists the cubes left, and the
  driver resumes from them.
- **Not started** (40 cases, from U4_L8 to U16_L11 in the listed order): `whole` is untried, so each one needs the full recipe.

## Why it fell short
The 10.1 core-hour estimate counted 600 s for each case without an estimate. The U_L2-x and U3-x 6-gon cases cost 2,000 to
11,000 core-s each. In addition, `march_cu -d 7` takes about 3 to 10 minutes per case on one core before any cube runs.
No case of this entry was closed by `drat-trim lrat-check`.

## SAT
None. No cube or whole case returned SAT.
