# W31: wave 1, mirror sub-case (ii), entry kind "cases" (U_L14, U_L13)

Result: **both cases closed.** Every leaf is checked by cake_lpr `s VERIFIED UNSAT`, and the leaves of each case cover it (covercheck.py `s COVERED 128`). No SAT answers.

## Environment and tools
- Machine: one cloud VM, 4 cores, 15 GB RAM, Linux 6.18 x86_64 (`env.txt`). Run on 2026-10-20 from 06:56 to 07:52 UTC.
- CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04.
- march_cu (CnC) at 705b60c6491ef2b61988b3ce6ac674be1b90571d, built with `-O3 -fcommon`.
- cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). The bundled example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check was not used.

## Hash checks (all match)
- Base CNF `m33k7int.sub.cnf`, regenerated with `results/C/scripts/make_cnfs.sh`: 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d
- `verify/ii_wave1.json`: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e
- U_L14 (`hullsplit.py case BASE "" 14`): 6c2de6339e8cae7cde5068bf305cbe4ac426592bd370162ff066d55b0fbf84f7
- U_L13 (`hullsplit.py case BASE "" 13`): 7cf7c8926f574d1d20d948a019b3995cf28d78012f914c2b00171433660bd7a6

## Method
1. Plain CaDiCaL with `-t 60` on each whole case. Both returned UNKNOWN, so nothing was accepted from this step.
2. `close_march.py` (a copy of `results/Mii-S/scripts/close_march.py`; the changes are listed in its docstring) ran with `--depth 7 --timeout 300 --split-depth 6 --jobs 4`. Both cases shared one 4-worker pool, with U_L14 cubes taking priority.
   - The changes: resume from `leaves.jsonl` and `top.icnf`; `leaves.icnf` lists only leaves with cake_lpr `s VERIFIED UNSAT`; `open.icnf` is written at the end; SPLIT records store their children; an empty split is never treated as closed; the `--shard`/`--nshards` options were added but not used here.
3. Every cube with a CaDiCaL UNSAT answer was checked with cake_lpr against CASE + the cube's units (3000 MB heap; no retries were needed). No cube hit the 300 s timeout, so no `-d 6` splits happened.

| case | top.icnf sha256 | top cubes (refuted) | leaves verified | open | cover | CaDiCaL s | cake_lpr s | march s | total core-h |
|---|---|---|---|---|---|---|---|---|---|
| U_L14 | 247f3692dad82b8e402d1c13083ee2698546d6e9df1baf3529445506aec46ff0 | 128 (0) | 128 | 0 | COVERED | 2588 | 619 | 319 | 0.98 |
| U_L13 | 87ba94f18f5c07c5a0234b46fef82529e66b50984e3e00836fec923f336993c3 | 128 (0) | 128 | 0 | COVERED | 3027 | 557 | 432 | 1.12 |

- Longest single solve: 84.8 s for U_L14 and 228.2 s for U_L13.
- Largest LRAT proof: 88 MB for U_L14 and 208 MB for U_L13. Proofs were deleted after checking.
- The planning estimate was 13.2 core-h; the actual cost was about 2.1 core-h, plus 2 × 60 s for the plain attempts.

## Incident: deleted log files (no effect on results)
- What happened: the run first wrote straight into this repo directory. The `git pull --rebase` before a push replaced the tracked `leaves.jsonl` files on disk, and the running process kept appending to the deleted copies.
- Recovery: the 104 records written by then were copied out of the process's open file handles (`/proc/PID/fd`). The run was stopped and resumed from those records, with output going to a directory outside the repo. Snapshots are copied in for each commit.
- Records lost: none. The 4 cubes that were running at the stop were solved again. Each cube has exactly one record (128 distinct per case).
