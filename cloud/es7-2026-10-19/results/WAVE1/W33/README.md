# W33: wave 1, mirror sub-case (ii), 65 cases (kind "cases")

Machine: a cloud VM with 4 cores and 15 GB RAM (see `env.txt`). It ran 2026-10-20 from 06:56 to 10:45 UTC.

## Tools (`tools.txt`)
- CaDiCaL c6073042 (3.0.1); march_cu from CnC 705b60c6, built with `-O3 -fcommon`; cake_lpr a36874a8 (`make cake_lpr`).
- The bundled cake_lpr example prints `s VERIFIED UNSAT`. A sanity check: cake_lpr rejects an LRAT file that only adds an unjustified empty clause.
- Only cake_lpr verdicts count. drat-trim was not used.

## Hash checks (`sha_checks.txt`, `case_sha.txt`)
- Base `m33k7int.sub.cnf` was regenerated with the make_cnfs.sh commands (gen_etv.py 33 7 7 7 --mirror, then mirgen.py --interior --yflip-unit). Its sha256 is 69c1dc8f…932d, as expected.
- `verify/ii_wave1.json` sha256 is 6df36dab…c72e, as expected. `Mii-S/cases.jsonl` sha256 is bf77e23c…6f58, as the json states.
- 65 of 65 case CNFs built with `hullsplit.py case` match both the W33 entry and cases.jsonl.

## Method (`close_march_w33.py`, a modified copy of Mii-S/scripts/close_march.py)
- Per case, in the listed order: plain `cadical --lrat -t 60` on the whole case. The result is accepted only if cake_lpr prints `s VERIFIED UNSAT`.
- Otherwise: `march_cu CASE -d 7 -o <case>/top.icnf`. Each cube runs `cadical --lrat -t 300` and every UNSAT is checked with cake_lpr. On a timeout the cube is split with `march_cu -d 6`.
- All cases share one pool of 4 workers, a priority queue keyed on case index, so cases close in the listed order. There is no sharding (the default 0 of 1).
- `leaves.jsonl` holds every record: the whole-case attempt with the case CNF sha256, the top record with the cube count, refuted count and top.icnf sha256, and the cube records. SPLIT records list their children, so the run can resume.
- `leaves.icnf` holds only cake_lpr-verified leaves. It is `a 0` when the whole case was closed directly.
- `open.icnf` holds the cubes that are not closed. It is `a 0` when no top split exists yet.
- The driver was restarted twice. The first restart moved its output outside the git tree. The second changed the pool from FIFO to the priority queue. The march runs that were in flight then were lost and redone. Each restart resumed from leaves.jsonl.
- `covercheck.txt`: `covercheck.py leaves.icnf` per case. For the open cases, leaves+open covers as a sanity check.

## Result
- **59 of 65 cases are CLOSED.** 32 closed by plain CaDiCaL plus cake_lpr. 27 closed by cubes: every leaf is cake_lpr-verified and covercheck says leaves.icnf is `s COVERED`.
- **6 are OPEN**, because the time budget ran out. U13_L5, U15_L4 and U9_L4 have their top.icnf but no cube processed yet. U4-16_L, U5_L11 and U11_L6 have had only the failed 60 s attempt. Their open.icnf files list what remains.
- No SAT answer. No UNSAT that failed cake_lpr.

| case | result | how | top cubes (refuted) | top.icnf sha256 (prefix) | cake_lpr-verified leaves | splits | open cubes | covercheck(leaves) | CPU s |
|---|---|---|---|---|---|---|---|---|---|
| U5_L10 | CLOSED | march cubes | 108 (14) | acefde4d538cd40f | 108 | 0 | 0 | COVERED | 923 |
| U_L2-5 | CLOSED | march cubes | 123 (3) | 1e81e041cdae5693 | 123 | 0 | 0 | COVERED | 4451 |
| U_L2-9 | CLOSED | march cubes | 122 (4) | 7eb2250e8a0e1e72 | 122 | 0 | 0 | COVERED | 2370 |
| U_L2-12 | CLOSED | march cubes | 125 (1) | 64392c3b333dcf76 | 125 | 0 | 0 | COVERED | 1854 |
| U_L2-16 | CLOSED | march cubes | 117 (7) | a0ce9cd5fe74fab6 | 117 | 0 | 0 | COVERED | 2460 |
| U3-6_L | CLOSED | march cubes | 119 (7) | 0723009b1cc94f20 | 119 | 0 | 0 | COVERED | 2752 |
| U3-9_L | CLOSED | march cubes | 128 (0) | a544085cab70bfc3 | 128 | 0 | 0 | COVERED | 2076 |
| U3-12_L | CLOSED | march cubes | 128 (0) | 569b2c9ca48b4dd7 | 128 | 0 | 0 | COVERED | 2118 |
| U4-5_L | CLOSED | march cubes | 128 (0) | 56232a9c7e770d14 | 128 | 0 | 0 | COVERED | 1074 |
| U_L4-6 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 60 |
| U4-8_L | CLOSED | march cubes | 108 (14) | 4c6cfa4e3f4866e8 | 108 | 0 | 0 | COVERED | 1149 |
| U_L4-9 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 47 |
| U_L4-11 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 41 |
| U_L4-13 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 34 |
| U4-15_L | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 61 |
| U_L5-6 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 26 |
| U5-8_L | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 35 |
| U_L5-9 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 24 |
| U_L5-11 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 24 |
| U_L5-13 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 17 |
| U_L5-15 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 22 |
| U6-8_L | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 23 |
| U6-12_L | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 22 |
| U3_L2 | CLOSED | march cubes | 128 (0) | b9d20603180c7232 | 315 | 3 | 0 | COVERED | 10558 |
| U3_L7 | CLOSED | march cubes | 125 (3) | 0351953a74be3a95 | 125 | 0 | 0 | COVERED | 2056 |
| U3_L11 | CLOSED | march cubes | 117 (3) | 676e545a104eaed5 | 117 | 0 | 0 | COVERED | 1276 |
| U3_L15 | CLOSED | march cubes | 123 (3) | d8d41ea91b6476c7 | 123 | 0 | 0 | COVERED | 1352 |
| U4_L6 | CLOSED | march cubes | 112 (13) | 98cc382349ffe437 | 112 | 0 | 0 | COVERED | 1264 |
| U4_L11 | CLOSED | march cubes | 96 (12) | 443687393f1f5290 | 96 | 0 | 0 | COVERED | 923 |
| U4_L15 | CLOSED | march cubes | 126 (2) | 3f04bf192a74d2d2 | 126 | 0 | 0 | COVERED | 882 |
| U5_L6 | CLOSED | march cubes | 108 (16) | 7d1a94a9c7fe66f4 | 108 | 0 | 0 | COVERED | 1025 |
| U5_L12 | CLOSED | march cubes | 108 (10) | 444974f01844d4f3 | 108 | 0 | 0 | COVERED | 859 |
| U6_L4 | CLOSED | march cubes | 108 (12) | d11657f812c6f78b | 108 | 0 | 0 | COVERED | 1329 |
| U6_L9 | CLOSED | march cubes | 113 (9) | 8e5757ab22a6eeb8 | 113 | 0 | 0 | COVERED | 792 |
| U6_L15 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 62 |
| U7_L5 | CLOSED | march cubes | 111 (9) | 45a203fd03e8ba98 | 111 | 0 | 0 | COVERED | 1010 |
| U7_L11 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 59 |
| U7_L16 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 44 |
| U8_L7 | CLOSED | march cubes | 113 (9) | 9be493a1313c7f4e | 113 | 0 | 0 | COVERED | 741 |
| U8_L13 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 38 |
| U9_L7 | CLOSED | march cubes | 116 (8) | 7a98379e6ca09b25 | 116 | 0 | 0 | COVERED | 722 |
| U9_L14 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 30 |
| U10_L4 | CLOSED | march cubes | 128 (0) | 5edc6068476ce950 | 128 | 0 | 0 | COVERED | 1160 |
| U10_L9 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 45 |
| U10_L14 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 23 |
| U11_L4 | CLOSED | march cubes | 128 (0) | 36c5c5cbbc76871d | 128 | 0 | 0 | COVERED | 1164 |
| U11_L9 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 36 |
| U11_L14 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 21 |
| U12_L5 | CLOSED | march cubes | 128 (0) | 0c950980adc2b07d | 128 | 0 | 0 | COVERED | 942 |
| U12_L13 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 16 |
| U13_L5 | OPEN | - | 128 (0) | 9e38058379640ed3 | 0 | 0 | 128 | NOT COVERED | 318 |
| U13_L9 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 29 |
| U14_L6 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 65 |
| U14_L10 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 19 |
| U15_L6 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 62 |
| U15_L12 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 16 |
| U16_L7 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 45 |
| U6_L13 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 65 |
| U4-16_L | OPEN | - | - | - | 0 | 0 | 1 | NOT COVERED | 60 |
| U15_L4 | OPEN | - | 128 (0) | e8291cb3d0c1bd8f | 0 | 0 | 128 | NOT COVERED | 333 |
| U7_L13 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 49 |
| U12_L7 | CLOSED | plain CaDiCaL 60 s | - | - | 1 | 0 | 0 | COVERED | 57 |
| U9_L4 | OPEN | - | 117 (10) | 40b590be62ef67e8 | 0 | 0 | 117 | NOT COVERED | 254 |
| U5_L11 | OPEN | - | - | - | 0 | 0 | 1 | NOT COVERED | 60 |
| U11_L6 | OPEN | - | - | - | 0 | 0 | 1 | NOT COVERED | 60 |

Total CPU (solve+check+march) 14.33 h; cake_lpr-verified UNSAT leaves/whole-case proofs: 3413.
