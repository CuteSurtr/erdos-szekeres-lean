# WAVE2 S1: back end of W35's list, sub-case (ii) hull cases

Run 2026-10-20, 10:35–12:44 UTC on one cloud VM (4 cores, 15 GB; see env.txt). Tools are in tools.txt;
the driver is close_march.py, a byte-identical copy of WAVE2/F2's, reviewed in driver.diff; the
orchestration is in runner.py.

## Result

- **SAT results: none.** **cake_lpr rejections: none**: every CaDiCaL UNSAT answer was checked by
  cake_lpr, and each check printed `s VERIFIED UNSAT`.
- **All 30 assigned cases are closed**: each has a non-empty leaves.icnf and an empty open.icnf.
  - 22 were closed whole by CaDiCaL within the 120 s cap (leaves.icnf = `a 0`).
  - 8 were closed by the driver: march_cu -d 7 top cubes, CaDiCaL with a 300 s cap per cube, and split depth 6.
- Cases skipped because they were closed elsewhere: none. Before each case was started, every
  `results/WAVE1/W35/<case>/` directory held only the placeholder `open.icnf` = `a 0`, with no
  leaves and no top.icnf, and no other WAVE1/WAVE2 directory had the case.
- Cases started but not closed: none. Cases not reached: none.

## Method

1. Each case CNF was built with `hullsplit.py case F.cnf U L` (F sha256 69c1dc8f…932d), and its sha256
   was asserted equal to cnf_sha256 in Mii-S/cases.jsonl.
2. **Phase A** (10:38–10:48): every case got a whole-case CaDiCaL run (`--lrat --binary=false -t 120`),
   4 at a time, and each UNSAT proof was checked by cake_lpr.
3. **Phase B** (10:48–12:44): the 8 cases left unknown went in list order through
   `close_march.py CASE.cnf S1/<case> --name <case> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours H`.
   - Only one cube timed out in all of phase B: U8_L2 cube `-2572 -2247 -1896 3281 3265 3248 3230`.
     march_cu split it into 64 sub-cubes, and all 64 were verified.
   - Some top files have fewer than 128 cubes (march_cu stopped some branches early). The cubes
     march_cu counts as "refuted" are still written in the file and were solved and verified like the others.
4. Sanity check on each case (not a replacement for the v3 cover check):
   - every leaves.icnf line has the form `a ... 0`;
   - no leaf repeats, and no leaf repeats a variable;
   - any two leaves clash (they share a variable with opposite signs);
   - the leaves' measures sum to exactly 1 (sum of 2^-|cube|), so together they cover the whole case;
   - every leaf extends a top.icnf cube.

   All 30 cases pass.

## Per case

leaves = verified leaves; open = open cubes left; split / timeout = number of SPLIT / TIMEOUT records.
The time columns add up per-cube wall times in seconds (CaDiCaL solve, cake_lpr check, march_cu split).
The march time for the top cubes is given in the last column.

| case | closed | leaves | open | split | timeout | solve s | check s | split s | method |
|---|---|---|---|---|---|---|---|---|---|
| U9_L10 | yes | 1 | 0 | 0 | 0 | 37 | 12 | 0 | direct (whole case, 120 s cap) |
| U3-16_L | yes | 112 | 0 | 0 | 0 | 773 | 331 | 0 | march_cu -d 7: number of cubes 112, including 10 refuted (511.6 s) |
| U16_L4 | yes | 112 | 0 | 0 | 0 | 295 | 245 | 0 | march_cu -d 7: number of cubes 112, including 13 refuted (310.9 s) |
| U8_L14 | yes | 1 | 0 | 0 | 0 | 30 | 15 | 0 | direct (whole case, 120 s cap) |
| U8_L9 | yes | 1 | 0 | 0 | 0 | 60 | 16 | 0 | direct (whole case, 120 s cap) |
| U9_L11 | yes | 1 | 0 | 0 | 0 | 33 | 15 | 0 | direct (whole case, 120 s cap) |
| U_L2-15 | yes | 128 | 0 | 0 | 0 | 1228 | 439 | 0 | march_cu -d 7: number of cubes 128, including 0 refuted (308.7 s) |
| U9_L5 | yes | 118 | 0 | 0 | 0 | 540 | 293 | 0 | march_cu -d 7: number of cubes 118, including 8 refuted (289.4 s) |
| U16_L8 | yes | 1 | 0 | 0 | 0 | 31 | 13 | 0 | direct (whole case, 120 s cap) |
| U16_L2 | yes | 126 | 0 | 0 | 0 | 1325 | 386 | 0 | march_cu -d 7: number of cubes 126, including 2 refuted (448.3 s) |
| U15_L7 | yes | 1 | 0 | 0 | 0 | 38 | 14 | 0 | direct (whole case, 120 s cap) |
| U14_L11 | yes | 1 | 0 | 0 | 0 | 15 | 9 | 0 | direct (whole case, 120 s cap) |
| U14_L7 | yes | 1 | 0 | 0 | 0 | 45 | 7 | 0 | direct (whole case, 120 s cap) |
| U13_L10 | yes | 1 | 0 | 0 | 0 | 17 | 9 | 0 | direct (whole case, 120 s cap) |
| U13_L6 | yes | 1 | 0 | 0 | 0 | 69 | 14 | 0 | direct (whole case, 120 s cap) |
| U12_L16 | yes | 1 | 0 | 0 | 0 | 13 | 7 | 0 | direct (whole case, 120 s cap) |
| U12_L6 | yes | 1 | 0 | 0 | 0 | 67 | 10 | 0 | direct (whole case, 120 s cap) |
| U11_L15 | yes | 1 | 0 | 0 | 0 | 13 | 8 | 0 | direct (whole case, 120 s cap) |
| U11_L10 | yes | 1 | 0 | 0 | 0 | 25 | 9 | 0 | direct (whole case, 120 s cap) |
| U11_L5 | yes | 128 | 0 | 0 | 0 | 634 | 370 | 0 | march_cu -d 7: number of cubes 128, including 0 refuted (235.9 s) |
| U10_L15 | yes | 1 | 0 | 0 | 0 | 16 | 5 | 0 | direct (whole case, 120 s cap) |
| U10_L11 | yes | 1 | 0 | 0 | 0 | 26 | 8 | 0 | direct (whole case, 120 s cap) |
| U10_L5 | yes | 128 | 0 | 0 | 0 | 714 | 405 | 0 | march_cu -d 7: number of cubes 128, including 0 refuted (184.4 s) |
| U9_L15 | yes | 1 | 0 | 0 | 0 | 21 | 4 | 0 | direct (whole case, 120 s cap) |
| U9_L8 | yes | 1 | 0 | 0 | 0 | 57 | 11 | 0 | direct (whole case, 120 s cap) |
| U8_L15 | yes | 1 | 0 | 0 | 0 | 30 | 7 | 0 | direct (whole case, 120 s cap) |
| U8_L10 | yes | 1 | 0 | 0 | 0 | 54 | 11 | 0 | direct (whole case, 120 s cap) |
| U8_L2 | yes | 191 | 0 | 1 | 0 | 2706 | 620 | 692 | march_cu -d 7: number of cubes 128, including 0 refuted (636.1 s) |
| U7_L12 | yes | 1 | 0 | 0 | 0 | 50 | 10 | 0 | direct (whole case, 120 s cap) |
| U7_L8 | yes | 1 | 0 | 0 | 0 | 96 | 14 | 0 | direct (whole case, 120 s cap) |

The first line of each leaves.jsonl is `{"case": ..., "case_sha256": ...}`.
- Direct cases: the second record holds the solve and check data.
- Driver cases: leaves.jsonl holds every cube record (cube, status, solve_s, proof_bytes, cake_lpr,
  check_s; SPLIT records carry the sub-cubes).

No CNF or LRAT file was committed.
