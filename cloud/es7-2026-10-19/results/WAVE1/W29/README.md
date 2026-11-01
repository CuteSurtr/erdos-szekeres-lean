# W29: wave 1, mirror sub-case (ii), kind "cases" (U4_L, U15_L, U_L15, U8_L)

**Result: no case closed, all four still OPEN. No SAT.** U4_L is partly done: 1,348 leaves verified
by cake_lpr and 665 cubes open. U15_L, U_L15 and U8_L were never started past their top cubes,
because the cases are taken in the listed order and U4_L used the whole budget.

## Environment and tools
- One cloud VM with 4 cores and 15 GB RAM (`env.txt`). Run from 2026-10-20 06:56 to 10:31 UTC.
- `tools.txt`: CaDiCaL c60730422e75 (3.0.1); march_cu from CnC 705b60c6 built with `-O3 -fcommon`;
  cake_lpr a36874a8 (`make cake_lpr`), whose bundled example prints `s VERIFIED UNSAT`.
- No drat-trim/lrat-check was used. The only proof checker was cake_lpr.

## sha256 checks (`sha256_checks.txt`), all OK
- Regenerated base `m33k7int.sub.cnf`: 69c1dc8f…932d.
- `verify/ii_wave1.json`: 6df36dab…c72e. `Mii-S/cases.jsonl`: bf77e23c…6f58.
- Case CNFs from `hullsplit.py case`: each matches the W29 entry.
  - U4_L ab728682…f991
  - U15_L 3f479f9f…dc8e
  - U_L15 226600f0…f8bc
  - U8_L 84d46852…9a882

## What ran
1. Plain CaDiCaL for 60 s on each whole case (`--lrat`, 4 runs in parallel). All four timed out
   (UNKNOWN) and none was accepted (`plain_60s.jsonl`).
2. `close_march.py` here: a copy of `Mii-S/scripts/close_march.py`, changed in three ways.
   - All four cases share one 4-worker pool. A cube of an earlier-listed case always starts first.
   - The run is resumable. It keeps `top.icnf` and stores each split's children in the SPLIT record.
   - It has `--shard/--nshards`, which this run did not use, and `--stop-at`.

   The recipe is otherwise unchanged: `march_cu -d 7` top cubes, `cadical --lrat -t 300`, and
   cake_lpr on every UNSAT, with timeouts split by `march_cu -d 6`.
   - A leaf goes into `leaves.icnf` only if cake_lpr printed `s VERIFIED UNSAT`.
   - New cubes stopped starting at 10:15 UTC. A short resume ran from 10:15 to 10:30.
3. Live output was kept outside the git tree and copied in to commit. An early `git pull --rebase` had
   replaced the open `leaves.jsonl` files. The 4 top records were recovered from /proc and the run
   restarted, losing about 2 minutes.

## Per case
| case | top.icnf sha256 (128 cubes, 0 refuted) | verified leaves | open cubes | CPU |
|---|---|---|---|---|
| U4_L | d8d70ee7920665ddf52ccc5d103c3f8a9f57d1c2e2f679d9763c78f482294c38 | 1348 (104 at depth 7, 1244 at depth 13) | 665 (286 at depth 13, 5 at 18, 374 at 19) | 13.5 core-h |
| U15_L | 20d96de2f698309b8d70c3492b1ebc225f9c9f782b590f2762949be5fd9d6b6a | 0 | 128 | top march only |
| U_L15 | b1a4f6297d37699eec6d20b18b61b4818ba3f6a8dfbe63aa2a2b3b106c56ae87 | 0 | 128 | top march only |
| U8_L | 1f96896ce06fd10f923e6f02ba62d489ef4bea30c741cb761a443045a0cf987f | 0 | 128 | top march only |

- U4_L CPU breakdown: 11.4 core-h CaDiCaL, 1.3 core-h cake_lpr, 0.75 core-h march splits, plus
  173 s for the top march.
- U4_L splits: 24 of 128 top cubes and 6 depth-13 cubes timed out at 300 s and were split.
- The top marches took 297 s (U15_L), 352 s (U_L15) and 205 s (U8_L).
- Every UNSAT that CaDiCaL reported was checked by cake_lpr and VERIFIED; no check failed. The largest
  proof was 237 MB, and proofs were deleted after checking.
- U4_L was estimated at 7.3 core-h and has already used 13.5 without closing.

## Cover checks (`final_checks.txt`, with `Mii-S/scripts/covercheck.py`)
- `top.icnf` is COVERED for every case, so march's 128 cubes form a full partition.
- `leaves.icnf` alone is NOT COVERED for every case, so no case is closed.
- `leaves.icnf` + `open.icnf` is COVERED for every case (2013 cubes for U4_L). The bookkeeping loses
  no part of the case.

## Resuming
Rerun `close_march.py OUTROOT U4_L=U4_L.cnf …` with this directory's `<case>/` folders as OUTROOT.
It rebuilds the queue from `top.icnf` and `leaves.jsonl` and works only on `open.icnf`'s cubes.
`solve_s`/`check_s`/`split_s` in `leaves.jsonl` are wall seconds of single-threaded runs, about equal to CPU.
