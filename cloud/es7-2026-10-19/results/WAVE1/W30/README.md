# W30 — wave 1, mirror sub-case (ii): cases U_L8, U9_L

Entry in `verify/ii_wave1.json`: kind "cases", cases U_L8 then U9_L, est. 13 core-h.
**Result: both cases OPEN** after the 4 h budget. No SAT. Everything is resumable.

## Machine and tools
- Cloud session VM, 4 cores, 15 GB RAM, Linux 6.18 x86_64 (`env.txt`). Run 07:01–10:15 UTC 2026-10-20.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (master).
- march_cu from CnC 705b60c6491ef2b61988b3ce6ac674be1b90571d, built with `-fcommon` added to CFLAGS.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`; bundled example prints `s VERIFIED UNSAT`.
- UNSAT is accepted only with cake_lpr `s VERIFIED UNSAT`. drat-trim lrat-check was not used.

## Hash checks (all match)
- Base CNF `m33k7int.sub.cnf` regenerated with `results/C/scripts/make_cnfs.sh`: 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d.
- `verify/ii_wave1.json`: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e.
- U_L8 (`hullsplit.py case BASE "" 8`): 6c05114f422e02810378941f606a0b34f9c2e943b042880a1a2f065dc7f1bfd5.
- U9_L (`hullsplit.py case BASE 9 ""`): 379250e6c59f018258b0449ba5da7d5ddc75c6ae5959100d330065e4633922e5.

## Method
`close_march.py` is copied unchanged from `results/Mii-S/scripts/`. `close_multi.py` is the version that ran:
- Same per-case recipe: plain `cadical --lrat -t 60` on the whole case (counts only with a cake_lpr check);
  then `march_cu CASE -d 7` top cubes (`<case>/top.icnf`); each cube gets `cadical --lrat -t 300` and cake_lpr;
  a timeout is split with `march_cu CASE+cube -d 6`.
- One 4-worker pool for both cases, served in the listed order (U_L8 cubes always before U9_L cubes).
- SPLIT records store their children, so a run can be resumed from `leaves.jsonl`.
- No new solve after 10:15 UTC. Cubes left in the queue got `{"status":"OPEN","reason":"deadline"}` records; they are re-queued on resume.

Command:
`BIN=/home/user/bin close_multi.py W30 --case U_L8 U_L8.cnf --case U9_L U9_L.cnf --jobs 4 --direct 60 --timeout 300 --depth 7 --split-depth 6 --deadline <10:15 UTC>`.
Resume with the same command and a later deadline. `--snapshot` rewrites leaves.icnf and open.icnf.

## Results
| case | direct 60 s | top cubes (refuted) | top.icnf sha256 | cake-verified leaves | splits | open cubes | CPU (solve+check+march) |
|---|---|---|---|---|---|---|---|
| U_L8 | timeout | 128 (0) | 75b7a4a7f2bb1a2d5aa8122a9652c77869a91c8dae3f4858a968cd70d8d72162 | 724 (depths 7:126, 13:126, 18:1, 19:114, 25:357) | 33 | 1450 | 30875+3102+10863 s = 12.5 h |
| U9_L | timeout | 128 (0) | 2ecc9b69f4026f62d3cb605766b503667ae2ad20677fdcc16e7a4b90fccfaa00 | 10 (depth 7) | 0 | 118 | 416+48+294 s = 0.2 h |

- Every UNSAT answer (734 of 734) was confirmed by cake_lpr `s VERIFIED UNSAT`. There were no failed checks. The largest LRAT proof was 254 MB; proofs were deleted after checking.
- Cover check (`results/Mii-S/scripts/covercheck.py`):
  - leaves.icnf alone: NOT COVERED for either case (expected, both are open);
  - leaves.icnf + open.icnf: COVERED for both cases (U_L8 2174 cubes, U9_L 128);
  - top.icnf: COVERED for both.
- U_L8: 127 of the 128 top cubes are closed. All 1450 open cubes lie under the single top cube at 0-based line 95,
  `1112 524 -508 1245 -507 -506 -505`. That subtree splits again and again: open depths are 25 (394), 29–30 (26) and 31 (1030).
  Its leaves take 100–300 s each, and the depth-6 march splits took 56–913 s each.
- U9_L: only reached after the hard U_L8 subtree had used up the time. 10 top cubes are closed and 118 are untouched.
- No SAT answer.

## Files
- `<case>/leaves.jsonl`: all records (whole-case attempt with the CNF sha256, top record, UNSAT/SPLIT/OPEN records).
- `<case>/leaves.icnf`: the cake-verified leaves only.
- `<case>/open.icnf`: the open frontier.
- `<case>/top.icnf`: the march_cu `-d 7` top cubes.
