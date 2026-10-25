# C3H1 / X1: the nine-bit cubes of one H3/one six-bit cube at cap 3600

**Result: all 8 nine-bit cubes of `0s0_5__1s0-2s1-3s0-4s0-6s0-7s0` were certified (both checkers), so this six-bit cube is closed: open frontier 0, no unsplittable node. No SAT. No proof rejection, no checker `none`, no memory problem.** Solve times were 450–662 s per nine-bit cube; 4,696 s of solving and 778 s of checking in total (1.52 core-hours), 35 minutes of wall time with 3 jobs.

## Setup

One cloud VM, 4 cores, 16 GB RAM, no swap (`env.txt`). Task `results/C3H1/TASK.md` at c5260b44, V = X1, H = 4.0. Start 05:31:48 UTC, END 09:16:48 UTC; the run itself took 05:34:24–06:09:36, so nothing was cut.

- Tools (`tools.txt`): C3U2 tools from a worktree of cad4e050 at `/opt/c3u2`, unmodified; CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (bundled example `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity test: the LRAT `3 0 0` on {1},{-1} is rejected by both checkers, `3 0 1 2 0` is accepted by both. `compose.py` was not run.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Run (`lane0.sh`, started with `setsid nohup`): `close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl 0s0_5__1s0-2s1-3s0-4s0-6s0-7s0 --jobs 3 --sigma-split 3 --sigma-levels 3 --caps 1,3600 --cadopts=--sat --hours 0.05`. The cube timed out at cap 1 and was σ-split with `"sigma_bits": [8, 9, 10]` (checked), 8 children. All 8 were submitted at once and solved 3 at a time at cap 3600.

## Per node (`out.jsonl`)

| node (suffix after `0s0_5__1s0-2s1-3s0-4s0-6s0-7s0`) | status | solve s | check s | proof bytes | lrat-check | cake_lpr |
|---|---|---|---|---|---|---|
| (the six-bit cube, cap 1) | UNKNOWN → σ split [8, 9, 10] | 1.0 | – | – | – | – |
| `-8s0-9s0-10s0` | certified | 449.9 | 94.6 | 818,487,944 | c VERIFIED | s VERIFIED UNSAT |
| `-8s0-9s1-10s0` | certified | 571.6 | 102.6 | 938,685,504 | c VERIFIED | s VERIFIED UNSAT |
| `-8s0-9s0-10s1` | certified | 592.4 | 108.1 | 976,181,958 | c VERIFIED | s VERIFIED UNSAT |
| `-8s0-9s1-10s1` | certified | 564.2 | 95.9 | 895,289,998 | c VERIFIED | s VERIFIED UNSAT |
| `-8s1-9s0-10s0` | certified | 662.2 | 97.9 | 963,334,427 | c VERIFIED | s VERIFIED UNSAT |
| `-8s1-9s0-10s1` | certified | 636.4 | 105.1 | 979,441,564 | c VERIFIED | s VERIFIED UNSAT |
| `-8s1-9s1-10s0` | certified | 629.6 | 93.9 | 1,008,959,138 | c VERIFIED | s VERIFIED UNSAT |
| `-8s1-9s1-10s1` | certified | 589.6 | 79.9 | 952,483,428 | c VERIFIED | s VERIFIED UNSAT |
| **total (8 cubes)** | 8 / 8 certified | **4,695.9** | **778.0** | 7.53 GB | | |

Times are per node with 3 jobs sharing 4 cores, so they are somewhat inflated compared with a lone job. Solve times: min 450, median 591, max 662 s. Every cube needed more than 300 s and none more than 662 s, so a cap of 900 s would have closed all 8, and 600 s only 4 of them.

## Memory and disk (`mem.log`, plus my own samples every few minutes)

- Peak memory seen: 6,366 MB used of 16,091 MB (05:45:57, while three proofs were being checked), i.e. about 2.1 GB per job including the checkers; available memory never went under 9.7 GB. CaDiCaL itself used about 0.6–0.7 GB per solve early on. These are samples, not a true peak.
- Peak `/opt/work/ct` seen: 2.1 GB (proofs of about 0.8–1.0 GB each are deleted after checking). Root disk use peaked at 14 GB of the allowance.

## Against the six-bit cube (X0 lane 0)

X0 lane 0 solves the same six-bit cube directly at cap 18000; its result is in `results/C3H1/X0/` (not available to me when this README was written). Comparison: the σ route here cost 4,696 s solve + 778 s check = 5,474 s ≈ 1.52 core-hours, and 35 minutes of wall time on one machine. Earlier, this six-bit cube family did not close at 300 s nor (for 5 cubes) at 1800 s, so the direct solve is at least 1800 s of solving with a single proof that is likely much larger than 1 GB; if X0 lane 0 needs more than about 1.5 h, the nine-bit route is the cheaper one, and it is in any case 3× more parallel with small, safely checkable proofs.

## Recommendation for the 320 six-bit cubes of the H3/one roots

From this one cube: split every six-bit cube once more on σ (cap 1 at the six-bit level, `--sigma-split 3 --sigma-levels 3`) and solve the nine-bit cubes at **cap 900** (`--caps 1,900` or, inside a wave, `--caps 1,1,1,900`), with a layer split at 600 only as a fallback. Expected cost: about 8 × (590 s solve + 97 s check) ≈ 5,500 s ≈ 1.5 core-hours per six-bit cube, so about **490 core-hours** (≈ 2,560 nine-bit cubes) for all 320, or about 165 machine-hours at 3 jobs per 4-core machine. Memory: about 2 GB per job (CaDiCaL ≤ 1 GB plus the checker on a ~1 GB proof), so 3 jobs fit safely in 16 GB; disk about 1 GB of proof per running job. Caveat: this is one cube of root `0s0_5`; the other roots, and the cubes whose third layer is again a single orbit (X2 lane 1), may be harder.
