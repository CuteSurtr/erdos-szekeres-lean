# C3H1 / X0: true solve time of two H3/one six-bit cubes (cap 18000)

**Result: `0s0_5__1s0-2s1-3s0-4s0-6s0-7s0` was certified (both checkers) after 13,708 s of solving (3.8 h) and 783 s of checking, with a 7.69 GB proof. `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` timed out at 18,000 s (5 h); it got its layer-split record (72 children, not solved). No SAT. No proof rejection, no checker `none`, no memory problem. Nothing was cut at END.**

## Setup

One cloud VM, 4 cores, 16 GB RAM, no swap (`env.txt`). Task `results/C3H1/TASK.md` at c5260b44, V = X0, H = 6.0. Start 05:31 UTC, END 11:16 UTC. Both lanes ran 05:34:08–09:36:19 (lane 0) and 05:34:08–10:34:19 (lane 1).

- Tools (`tools.txt`): C3U2 tools from a worktree of cad4e050 at `/opt/c3u2`, unmodified; CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (bundled example `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity test: the LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both. `compose.py` was not run.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Lanes (`lane0.sh`, `lane1.sh`, each started with `setsid nohup`): `close_tree.py /opt/work/base.cnf /opt/work/outK.jsonl NODE --jobs 1 --caps 18000 --cadopts=--sat --hours 0.02`. `mem.log` was written by `memlog.sh` every 15 minutes.

## Per node (`out.jsonl`: lane 0, then lane 1)

| lane | node | status | solve s | check s | proof bytes | lrat-check | cake_lpr |
|---|---|---|---|---|---|---|---|
| 0 | `0s0_5__1s0-2s1-3s0-4s0-6s0-7s0` | **certified** | 13,707.7 | 783.0 | 7,685,763,360 | c VERIFIED | s VERIFIED UNSAT |
| 1 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | timed out at 18,000 → layer split, 72 children (open) | 18,000.1 | – | (≈ 9.4 GB when killed by the cap, not kept) | – | – |

CNF sha256: lane 0 `1da9b745…9b68d3` (the same as in `C3COMP1/pilot9`), lane 1 `413b2da4…04e31b`. Two solves shared the 4 cores, so the times may be a little inflated compared with a lone job. The check time (783 s) covers both checkers run one after the other (solve ended 09:22:36, lrat-check was running at 09:23, cake_lpr at 09:33, record written 09:36:19).

## Memory and disk

- `mem.log` (every 15 min): peak used was 5,609 MB of 16,091 MB, at 09:34 while cake_lpr checked the 7.7 GB proof and lane 1 was still solving. I also sampled every 30 s from 09:33 (`/opt/work/peak.log`, not committed). Peak used there was 5,618 MB. cake_lpr's RSS was 4.2 GB (it runs with CML_HEAP_SIZE=12000) and CaDiCaL's at most 0.7 GB. lrat-check finished before the 30 s sampling started, so its peak was not measured.
- Disk: `/opt/work/ct` peaked at 15.1 GB (09:19, both proofs growing at about 1.5–2 GB/h each). The root filesystem got down to 15 GB free.

## Comparison with X1 and X2

- **X1** (σ-split of the same cube into 8 nine-bit cubes at cap 3600, `results/C3H1/X1`): all 8 were certified. Totals were 4,696 s solve + 778 s check = **5,474 core-s**, against **14,491 core-s** (13,708 + 783) for the direct six-bit solve here. So the nine-bit route costs 0.38 of the direct solve, about 2.6× cheaper. It also gave eight 0.8–1.0 GB proofs instead of one 7.7 GB proof, and finished in 35 minutes of wall time on 3 jobs instead of 4 hours.
- **X2** lane 0 (the same cube with CaDiCaL default options) had not reported when this README was written. Its default-options against `--sat` comparison is in `results/C3H1/X2`. X2 lane 1 certified all three layer children with three nested triangles at cap 3600, in 1,643–1,908 s of solving each.

## Recommendation for the 320 six-bit cubes of the H3/one roots

Do not solve the six-bit cubes directly. One took 3.8 h and the other did not finish in 5 h, so the direct cost is heavy-tailed and at least about 4 core-hours per cube, or more than 1,300 core-hours for 320. Use one more σ level instead: `--sigma-split 3 --sigma-levels 3 --caps 1,1,1,3600 --cadopts=--sat` from the root, or `--caps 1,3600` from a six-bit cube. Run each six-bit cube as its own root in a fresh OUT where an old layer-split record exists, as for `0s0_2__…` here. The nine-bit cubes of `0s0_5__…` took 450–662 s, so cap 3600 leaves a margin for harder cubes such as `0s0_2__…`.

Expected cost: about 5,500 core-s ≈ 1.5 core-hours per six-bit cube (X1), so about **490 core-hours** for the 320 cubes. Allow up to about 2× that (≈ 1,000 core-hours) if cubes like `0s0_2__…`, which did not close in 5 h directly, are 2–3× harder. Memory per job: CaDiCaL under 1 GB, plus a checker on a ~1 GB proof (about 2 GB per job in X1). 3 jobs fit in 16 GB, with about 1 GB of proof disk per running job. If any cube is still solved directly, allow 4–5 GB per job for cake_lpr on a 7–10 GB proof, plus 10 GB of disk per job.

## Files

`env.txt`, `tools.txt`, `lane0.sh`, `lane1.sh`, `memlog.sh`, `mem.log`, `out.jsonl`, `driver0.log.tail`, `driver1.log.tail`.
