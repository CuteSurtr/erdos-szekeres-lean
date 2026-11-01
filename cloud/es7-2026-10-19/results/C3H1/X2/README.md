# C3H1 / X2: CaDiCaL default options vs `--sat` on one H3/one six-bit cube, and three nested-triangle layer children at cap 3600

**Result:**
- All 3 three-nested-triangle layer children were **certified** at cap 3600 with `--sat`, in 1643–1908 s of solving each (both checkers accept).
- The six-bit cube `0s0_5__1s0-2s1-3s0-4s0-6s0-7s0` with CaDiCaL's **default options timed out at 18000 s**. With `--sat`, X0 certified the same cube in 13,707.7 s.
- No SAT. No proof rejection, no checker `none`, no memory problem, no solve cut at END.

## Setup
- Tools (`tools.txt`): C3U2 tools at cad4e050, used unmodified; `compose.py` not run. CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Checker sanity test: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF: `gen_case.py 11 7 none`, header `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Machine: 4 cores, 16 GB, no swap (`env.txt`). Task `results/C3H1/TASK.md` at c5260b44, with H = 6.0. Start 05:31:09 UTC, END 11:16:09 UTC.
- `lane0.sh` and `lane1.sh` were started with `setsid nohup`, both at 05:34:07. `memlog.sh` logs memory and disk every 15 minutes. `watchdog.sh` (added at 06:30 as a safety net, after the session's tool-permission checks failed several times) pushed progress every 25 minutes and would have killed the lanes at END. It never had to kill anything: both lanes finished before END.
- `out.jsonl` holds lane 0 first, then lane 1.

## Per node
| lane | node | options, cap | status | solve s | check s | proof bytes | lrat-check | cake_lpr |
|---|---|---|---|---|---|---|---|---|
| 0 | `0s0_5__1s0-2s1-3s0-4s0-6s0-7s0` | default, 18000 | **timed out** (UNKNOWN). Layer split record, 72 children, none solved (`open_frontier` 72) | 18000.1 | – | – (≈ 8 GB of LRAT written when the cap hit) | – | – |
| 1 | `0s0_5_2__1s0-2s1-3s0-4s0-6s0-7s0` | `--sat`, 3600 | **certified** | 1703.5 | 126.9 | 1,144,489,239 | c VERIFIED | s VERIFIED UNSAT |
| 1 | `0s0_2_3__1s0-3s1-4s0-5s0-6s1-7s0` | `--sat`, 3600 | **certified** | 1643.4 | 138.2 | 1,237,762,617 | c VERIFIED | s VERIFIED UNSAT |
| 1 | `0s0_1_3__2s0-3s1-4s0-5s0-6s0-7s0` | `--sat`, 3600 | **certified** | 1908.1 | 142.8 | 1,255,990,271 | c VERIFIED | s VERIFIED UNSAT |

Each lane-1 node closes its own subtree (`open_frontier` 0, no unsplittable node). All three had timed out at 600 s in C3W4.

## Memory and disk (`mem.log`)
- Peak memory use logged: 5,616 MB used of 16,091 MB, at 06:34. At that time the lane-0 solve was running and a lane-1 proof had just been checked. Available memory never went below 10.4 GB. These are 15-minute samples, not a true peak.
- Peak `/opt/work/ct`: 8.1 GB at 10:19. Almost all of it was the lane-0 LRAT proof, which grew by about 0.45 GB per 15 minutes. The node CNFs are about 110 MB each. The root disk never went below 20 GB free.

## Default options against `--sat` (same cube, `0s0_5__1s0-2s1-3s0-4s0-6s0-7s0`)
| run | options | result | solve s | check s | proof |
|---|---|---|---|---|---|
| X0 lane 0 | `--sat` | certified | 13,707.7 | 783.0 | 7.69 GB |
| X2 lane 0 (this run) | default | timed out | > 18,000 | – | > 8 GB at the cap |

So `--sat` is at least 1.31× faster on this cube. Keep `--sat`.

## Context from the other machines (read from the branch at 10:35 UTC)
- **X1**: the same six-bit cube, σ-split into 8 nine-bit cubes (bits 8, 9, 10), all certified at cap 3600 with `--sat`. Solve times were 450–662 s each: 4,696 s of solving and 778 s of checking in total (5,474 core-s, about 1.5 core-hours), with proofs of about 0.8–1.0 GB each.
- **X0** solved the same cube directly with `--sat`: 13,708 s of solving and 783 s of checking (14,491 core-s, about 4.0 core-hours), with a 7.7 GB proof. **The nine-bit route costs 0.38× as much** as the direct solve, and runs as 8 parallel jobs.
- **X0 lane 1**: the cube `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` timed out at 18000 s even with `--sat`, so the direct cost varies by more than 1.3× between cubes.
- **Layer route** for comparison (C3W4 records of `0s0_5__…`): 72 children. The ones that are not nested triangles closed at about 170 s of solving plus 40 s of checking each (23 of them). The nested-triangle children (third layer a single orbit, about 9–10 per cube) take 1,640–1,910 s plus about 135 s of checking each (this run). Estimate: about 10 × 2,000 + 62 × 210 ≈ 33,000 core-s ≈ 9 core-hours per cube, about 6× the nine-bit route.

## Recommendation for the 320 six-bit cubes of the H3/one roots
- **Method:** a third σ level on every six-bit cube, solving its 8 nine-bit cubes directly. Use X1's command, per cube: `close_tree.py base out CUBE --sigma-split 3 --sigma-levels 3 --caps 1,3600 --cadopts=--sat`, with `--sat` always.
  - Do not use the direct solve. It takes 4 to more than 5 hours, needs proofs of 8 GB or more, and one cube did not finish in 18000 s.
  - Do not use the layer split: it costs about 6×.
  - Keep cap 3600. The slowest nine-bit cube took 662 s, so the cap leaves a margin of 5×, and the cap costs nothing on cubes that close.
- **Expected cost:** 320 × 8 = 2,560 nine-bit cubes × about 685 core-s (590 s solve + 97 s check) ≈ **490 core-hours**, or about 165 VM-hours at 3 jobs per 4-core VM. This is measured on one cube only, and `0s0_2__…` is harder than `0s0_5__…` when solved directly, so plan a margin of up to 2× (≈ 500–1,000 core-hours). Nine-bit cubes that time out at 3600 s need a fourth σ level (12 bits), not the layer split.
- A cheap first step: run the nine-bit cubes of `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` (the cube X0 could not close) before planning the whole wave.
- **Memory per job:** about 2 GB, including the checkers (X1 peaked at 6.4 GB with 3 jobs). A checker run on a 1–1.3 GB proof fits easily. **3 jobs on a 16 GB VM is safe.**
- **Disk per job:** about 1.1–1.3 GB of proof plus the 110 MB CNF, while it runs.
