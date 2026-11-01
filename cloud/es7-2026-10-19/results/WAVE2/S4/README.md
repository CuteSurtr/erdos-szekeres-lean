# S4: wave 2, mirror sub-case (ii), the 29 W34 cases before S3's share (taken from the back)

**Result: 10 cases closed, 15 skipped (W34 had already closed them), 1 started but not closed (U4_L2, 66 open cubes),
3 not reached (U3_L13, U3_L9, U3_L5). No SAT answers. cake_lpr rejected no proof.**

## Setup
- One cloud VM: 4 cores, 15 GB RAM (`env.txt`). The run went from 10:30 to 13:10 UTC.
- Tools (`tools.txt`): CaDiCaL c6073042 (3.0.1), march_cu CnC 705b60c6 (built with `-fcommon`), cake_lpr a36874a8.
  The bundled cake_lpr example prints `s VERIFIED UNSAT`.
- F was regenerated (gen_etv 33 7 7 7 --mirror; mirgen --interior --yflip-unit). Its sha256 matches 69c1dc8f…ffff932d.
  Every case CNF was built with `hullsplit.py case` and its sha256 checked against cases.jsonl in `whole.sh`.
  The checked sha is the `case_sha256` in each `leaves.jsonl` and in `whole.jsonl`, and there were no mismatches.
- Driver: `close_march.py` is a byte copy of `WAVE2/F2/close_march.py`. `driver.diff` records the review: (a) every job
  gets its own `mkdtemp` directory, (b) leaves.icnf and open.icnf are written to a temp file and then renamed, (c) the
  first leaves.jsonl record has `case` and `case_sha256`. A leaf goes to leaves.icnf only on the exact line
  `s VERIFIED UNSAT` (BUG-1). `--skip` was never used. Every case started in an empty directory (RISK-3c).
- Orchestration (`run_s4.sh`, `whole.sh`, `status.py`, `commit.sh`):
  1. Step (a), checked again before each driver run: `status.py` looks at every other `WAVE1/*/<case>` and
     `WAVE2/*/<case>` directory.
  2. Steps (b) and (c): the whole-case CaDiCaL attempts (120 s, `--lrat`, then cake_lpr) ran 4 at a time.
  3. Step (d): `close_march.py --depth 7 --timeout 300 --split-depth 6 --jobs 4`, one case at a time, with a deadline
     of 13:08 UTC.
- Cover: `covercheck.py leaves.icnf` prints `s COVERED` for every closed case. For U4_L2, `leaves.icnf` + `open.icnf`
  together print `s COVERED 128`. Every line of every leaves.icnf ends in ` 0`.
  Leaves are relative to the case CNF (F + the case units), the same convention as WAVE1/W34.

## Per case
Times are sums over the jobs, in wall seconds: solve = CaDiCaL, check = cake_lpr, march = top cubes plus splits.
`summary.json` has the same data.

| case | state | method | top cubes | verified leaves | splits | open | unchecked/rejected | SAT | solve s | check s | march s | cover |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U7_L14 | **CLOSED** | whole cadical 120s | - | 1 | 0 | 0 | 0 | 0 | 47.0 | 18.3 | 0 | COVERED |
| U7_L9 | **CLOSED** | whole cadical 120s | - | 1 | 0 | 0 | 0 | 0 | 90.8 | 24.0 | 0 | COVERED |
| U7_L2 | **CLOSED** | close_march | 125 | 188 | 1 | 0 | 0 | 0 | 3405.5 | 838.7 | 1019.9 | COVERED |
| U6_L11 | **CLOSED** | whole cadical 120s | - | 1 | 0 | 0 | 0 | 0 | 98.2 | 19.8 | 0 | COVERED |
| U6_L7 | **CLOSED** | close_march | 108 | 108 | 0 | 0 | 0 | 0 | 466.8 | 268.9 | 302.4 | COVERED |
| U5_L14 | **CLOSED** | whole cadical 120s | - | 1 | 0 | 0 | 0 | 0 | 90.1 | 19.6 | 0 | COVERED |
| U5_L8 | **CLOSED** | close_march | 112 | 112 | 0 | 0 | 0 | 0 | 445.4 | 275.2 | 337.2 | COVERED |
| U5_L2 | **CLOSED** | close_march | 123 | 247 | 2 | 0 | 0 | 0 | 5347.4 | 866.1 | 1634.3 | COVERED |
| U4_L13 | **CLOSED** | close_march | 113 | 113 | 0 | 0 | 0 | 0 | 373.7 | 253.2 | 539.0 | COVERED |
| U4_L8 | **CLOSED** | close_march | 113 | 113 | 0 | 0 | 0 | 0 | 585.0 | 265.3 | 409.8 | COVERED |
| U4_L2 | **OPEN** | close_march | 128 | 62 | 0 | 66 | 0 | 0 | 2214.1 | 297.6 | 346.4 | NOT |
| U3_L13 | not reached / not started by S4 | - | - | - | - | - | - | - | - | - | - | - |
| U3_L9 | not reached / not started by S4 | - | - | - | - | - | - | - | - | - | - | - |
| U3_L5 | not reached / not started by S4 | - | - | - | - | - | - | - | - | - | - | - |
| U6-15_L | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U6-10_L | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U_L5-16 | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U_L5-14 | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U_L5-12 | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U_L5-10 | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U5-9_L | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U_L5-7 | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U5-6_L | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U_L4-14 | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U4-13_L | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U4-11_L | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U4-9_L | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U_L4-7 | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |
| U4-6_L | skipped (closed by W34) | - | - | - | - | - | - | - | - | - | - | - |

## Cases closed (10)
- Whole case at once (`leaves.icnf` = `a 0`): U7_L14, U7_L9, U6_L11, U5_L14.
- Cube-and-conquer: U7_L2 (188 leaves), U6_L7 (108), U5_L8 (112), U5_L2 (247), U4_L13 (113), U4_L8 (113).
  - U7_L2 had 1 split and U5_L2 had 2. Each split was a top cube that hit the 300 s cap and was split by march_cu
    -d 6 into 62–64 sub-cubes.
  - Top files where march_cu itself refuted some cubes: U7_L2 (1 of 125), U5_L2 (5 of 123), U4_L13 (11 of 113).
    These still appear as cubes in top.icnf, and CaDiCaL closed each one as a leaf.

## Cases skipped, closed elsewhere (15)
All 15 were closed by WAVE1/W34: U6-15_L, U6-10_L, U_L5-16, U_L5-14, U_L5-12, U_L5-10, U5-9_L, U_L5-7, U5-6_L,
U_L4-14, U4-13_L, U4-11_L, U4-9_L, U_L4-7, U4-6_L. Details are in `skipped.txt`.

## Started but not closed (1)
- **U4_L2**: W34 had started it (top.icnf, 0 leaves), so it went to the end of my list. I ran it from scratch in my own
  directory.
  - My top file has 128 cubes. Its sha is in leaves.jsonl.
  - 62 cubes were verified. **66 are left open**, listed exactly in `U4_L2/open.icnf`.
  - The driver stopped because no new cube may start within 300 s of the deadline. No cube was split and none timed out.

## Not reached (3)
U3_L13, U3_L9 and U3_L5. W34 had started all three (U3_L5: 65 leaves and 58 open; U3_L9: 93 and 32; U3_L13: 0 and 127),
so they went to the end. The 120 s whole-case attempt timed out on each (`whole.jsonl`). The driver did not run, because
less than 10 minutes were left, and I created no S4 directory for them (`notreached.txt`). A continuation can resume
from W34's open cubes.

## SAT / rejections
There were no SAT results, either whole-case or for a cube. No proof came back with a cake_lpr line other than
`s VERIFIED UNSAT`: there are 0 `UNSAT_UNCHECKED` records.
No CNF or LRAT files are committed. All scratch files were in /opt/work/tmp and were removed after each job.
