# WAVE2 S3: hull cases of mirror sub-case (ii) taken from the back of W34's list

**Result: all 30 assigned cases are CLOSED. 0 skipped, 0 started-but-open, 0 not reached.
No SAT answer. No cake_lpr rejection: every UNSAT record (21 whole-case proofs and 1,091 cube proofs)
has the exact line `s VERIFIED UNSAT`. No cube timed out, so nothing was split.**

## Run
- One cloud VM, 4 cores, 15 GB (`env.txt`). Run from 10:32 to 12:10 UTC (budget until 13:32).
- Tools (`tools.txt`), built from source: CaDiCaL 3.0.1 c6073042, march_cu CnC 705b60c6 (`-O3 -fcommon`),
  cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`).
- F regenerated (gen_etv 33 7 7 7 --mirror; mirgen --interior --yflip-unit): sha256
  69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, as required.
- Every case CNF was built with `hullsplit.py case F U L` and its sha256 equals `cnf_sha256` in
  `results/Mii-S/cases.jsonl` (asserted by the runner; also `case_sha256` in the first record of each
  `leaves.jsonl`, re-checked when writing this README).
- Driver: `close_march.py`, a byte-identical copy of `results/WAVE2/F2/close_march.py`. What I checked
  (fresh mkdtemp directory per solver/checker/march job; atomic tmp+rename of leaves.icnf and open.icnf;
  `case` and `case_sha256` in the first leaves.jsonl record; leaf only on `s VERIFIED UNSAT`) is in
  `driver.diff`, together with the diff against `results/WAVE1/W19/scripts/close_march.py`.
- Runner: `run_s3.py`. Phase 1: for all 30 cases (4 in parallel) a skip check against other machines'
  directories after `git pull`, the case CNF build and sha check, then CaDiCaL `--lrat -t 120` on the whole
  case and cake_lpr. Phase 2, one case at a time: another pull and skip check, then
  `close_march.py CASE.cnf S3/<case> --name <case> --depth 7 --timeout 300 --split-depth 6 --jobs 4
  --hours H --top <march_cu CASE -d 7 output>`. The top cubes were made ahead of time with exactly
  `march_cu CASE.cnf -d 7` (some by the runner, some by hand in parallel to use idle cores); `tops.txt`
  lists their sha256 and refuted counts. The driver's `top_sha256` record matches.
- Skip check: at the start and before each phase-2 case, W34's directories for all 30 cases held the
  "not started" placeholder (empty leaves.icnf, open.icnf `a 0`, no top.icnf). No WAVE1/WAVE2 directory
  other than mine had leaves or a top file for any of them, so none was skipped or moved.

## Files per case (`<case>/`)
- `leaves.icnf`: the verified cubes, one `a l1 .. lk 0` per line, over F's variable numbering, relative to
  the case CNF (the case's unit literals are not repeated). Whole-case closures are the single line `a 0`.
- `open.icnf`: empty for every case.
- `leaves.jsonl`: first record `{"case", "case_sha256"}`, then every solver record (solve_s, proof_bytes,
  cake_lpr line, check_s). For the 9 cube cases also the whole-case attempt is in `run.log`
  (rc 0 = 120 s timeout).
- `top.icnf` for the 9 cube cases (all lines of march's output, refuted branches included; every line
  was solved and verified).
- No CNF or LRAT file is committed; proofs were deleted after checking.

`covercheck.py leaves.icnf` prints `s COVERED` for every case.

## Per case
Solve and check are sums of CaDiCaL and cake_lpr wall seconds over the case's leaves (the 120 s
whole-case timeouts of the 9 cube cases are not included: 9 x 120 s).

| case | state | method | top cubes | verified leaves | open | non-verified UNSAT | cover | solve s | check s | other machines | CNF sha256 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U16_L11 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 13 | 12 | W34:not started | `b0e1e462d17adc59…` |
| U13_L11 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 14 | 12 | W34:not started | `b629c081a1ebeb48…` |
| U15_L9 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 22 | 6 | W34:not started | `0ca18e6bc3cfb617…` |
| U_L4-10 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 33 | 7 | W34:not started | `29d071af222928e8…` |
| U3-15_L | **CLOSED** | close_march | 127 | 127 | 0 | 0 | s COVERED 127 | 1832 | 481 | W34:not started | `807503f07d05b9ac…` |
| U12_L9 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 27 | 11 | W34:not started | `06fc299e03c39789…` |
| U8_L6 | **CLOSED** | close_march | 114 | 114 | 0 | 0 | s COVERED 114 | 389 | 271 | W34:not started | `8b9a7b2623919b41…` |
| U12_L2 | **CLOSED** | close_march | 118 | 118 | 0 | 0 | s COVERED 118 | 861 | 353 | W34:not started | `b9682378a8d04291…` |
| U4_L10 | **CLOSED** | close_march | 110 | 110 | 0 | 0 | s COVERED 110 | 454 | 304 | W34:not started | `ad8dd1313dcfce89…` |
| U5_L15 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 86 | 19 | W34:not started | `3821d2b7b16397bc…` |
| U16_L9 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 20 | 10 | W34:not started | `f23d7cc4f8512afb…` |
| U16_L5 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 95 | 13 | W34:not started | `951a2b019d0f4fe1…` |
| U15_L8 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 29 | 11 | W34:not started | `8f43b73987827335…` |
| U15_L2 | **CLOSED** | close_march | 125 | 125 | 0 | 0 | s COVERED 125 | 3638 | 699 | W34:not started | `447c1bffda0db049…` |
| U14_L8 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 30 | 4 | W34:not started | `17d405efd503e379…` |
| U14_L2 | **CLOSED** | close_march | 127 | 127 | 0 | 0 | s COVERED 127 | 1053 | 344 | W34:not started | `958298bab41721c5…` |
| U13_L7 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 47 | 11 | W34:not started | `236d7c018afc24ee…` |
| U13_L2 | **CLOSED** | close_march | 127 | 127 | 0 | 0 | s COVERED 127 | 931 | 320 | W34:not started | `0b97bf91e121fcb5…` |
| U12_L8 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 37 | 9 | W34:not started | `3d437ea9e6d03476…` |
| U11_L16 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 13 | 7 | W34:not started | `d7eba12c5d24f766…` |
| U11_L12 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 15 | 4 | W34:not started | `efdd078d99c71e4c…` |
| U11_L7 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 54 | 11 | W34:not started | `21655eec4eb8ab51…` |
| U10_L16 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 15 | 6 | W34:not started | `222a236988fe6051…` |
| U10_L12 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 22 | 7 | W34:not started | `a49a1a8ee65cac9f…` |
| U10_L6 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 85 | 12 | W34:not started | `b1d2080b3359849a…` |
| U9_L16 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 21 | 10 | W34:not started | `4a5f6a508f1a6f8f…` |
| U9_L12 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 28 | 6 | W34:not started | `aa1943829e9dff43…` |
| U9_L2 | **CLOSED** | close_march | 127 | 127 | 0 | 0 | s COVERED 127 | 1350 | 332 | W34:not started | `388407e393036f6e…` |
| U8_L11 | **CLOSED** | whole CaDiCaL 120 s | - | 1 | 0 | 0 | s COVERED 1 | 38 | 8 | W34:not started | `d4351e1ffe158baa…` |
| U8_L4 | **CLOSED** | close_march | 116 | 116 | 0 | 0 | s COVERED 116 | 738 | 292 | W34:not started | `35e0a411c0863fd4…` |

Totals: 1,112 verified leaves (21 whole cases + 1,091 cubes), 0 open; solve 11,990 s, check 3,591 s.
The longest single cube was 273 s (U9_L2), under the 300 s cap. The hardest case by CPU was U15_L2
(10,086 CPU s over 125 cubes).

## Summary lists
- Closed (30): U16_L11, U13_L11, U15_L9, U_L4-10, U3-15_L, U12_L9, U8_L6, U12_L2, U4_L10, U5_L15, U16_L9,
  U16_L5, U15_L8, U15_L2, U14_L8, U14_L2, U13_L7, U13_L2, U12_L8, U11_L16, U11_L12, U11_L7, U10_L16,
  U10_L12, U10_L6, U9_L16, U9_L12, U9_L2, U8_L11, U8_L4.
  Of these 21 by the whole-case attempt and 9 (U3-15_L, U8_L6, U12_L2, U4_L10, U15_L2, U14_L2, U13_L2,
  U9_L2, U8_L4) by the 128-way march cubes with no split needed.
- Skipped because closed elsewhere: none.
- Started but not closed: none.
- Not reached: none.

## Notes
- W34 (whose list these are) still shows them as "not started"; its directories should not be counted
  for these cases.
- `run.log` lost its lines after 12:04:48: `git pull --autostash` replaced the file while the runner held
  it open. It was restored from the runner's open file handle; the missing tail (U8_L4 driver exit with
  open 0) is in U8_L4/leaves.jsonl and the commit log. The phase-1 driver commits were also delayed until
  10:48 because a pathspec exclusion in the runner's first `git add` matched nothing; fixed in `run_s3.py`
  and the runner restarted, reusing the phase-1 results from `run.log` (no case was re-solved).
- `status.json` is the runner's final per-case state.
