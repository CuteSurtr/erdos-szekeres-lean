# C3H1 task: what the H3/one roots (two nested triangles) really cost, one machine

Your prompt gives these values: V (your machine name: X0, X1 or X2), H (your time budget in hours) and Z (the commit of this file). Replace {V}, {H} and {Z} by those values. Everything else in this file is to be followed exactly.

This is part of the search for a counterexample to ES(7) = 33 (a 3-fold-symmetric 33-point set in general position with no 7 points in convex position). Every SAT answer is a candidate counterexample.

General rules: exactly as in `results/C3W6/TASK.md`, with `results/C3H1/{V}/` as your only directory and the fallback branch `es7-fallback-c3h1-{V}` (lower case). Tools and base CNF exactly as its step 1 (C3U2 tools at cad4e050, unmodified; do not run `compose.py`); record them in `tools.txt`.

## Background

The five H3/one roots `0s0_1` … `0s0_5` (the hull is a triangle and so is the second layer) have 320 six-bit σ-cubes, and they are now the critical path of the 3-fold class (`results/C3COMP1/README.md`). None of their six-bit cubes closed at 300 s (291 tried), none of 5 at 1800 s, all 8 nine-bit cubes of one of them timed out at 600 s (`results/C3COMP1/pilot9/`), and the layer children that timed out at 600 s are the ones whose third layer is again a single orbit (three nested triangles). This pilot measures the real cost before any wave is planned.

## Steps

Each close_tree call below solves its node once and stops (`--hours 0.02`, or `0.05` where a cap-1 σ split comes first); a node that times out gets its split record and its children stay unsolved. Every call writes to its own out file under `/opt/work/`. Start each lane with `setsid nohup` from a script that you copy to your directory. Run `cd $TOOLS` first.

- **X0** (true solve time of a six-bit cube; 2 lanes, so that memory stays safe):
  - lane 0: `python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl 0s0_5__1s0-2s1-3s0-4s0-6s0-7s0 --jobs 1 --caps 18000 --cadopts=--sat --hours 0.02`
  - lane 1: the same with `out1.jsonl` and `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0`.
- **X1** (nine-bit cubes at a long cap): `python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl 0s0_5__1s0-2s1-3s0-4s0-6s0-7s0 --jobs 3 --sigma-split 3 --sigma-levels 3 --caps 1,3600 --cadopts=--sat --hours 0.05`. The cube (cap 1) times out at once and is σ-split on residues 8, 9, 10 (check `"sigma_bits": [8, 9, 10]`); its 8 nine-bit cubes are solved at cap 3600, 3 at a time; then close_tree stops.
- **X2** (solver options, and three nested triangles at a long cap; 2 lanes):
  - lane 0: `python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl 0s0_5__1s0-2s1-3s0-4s0-6s0-7s0 --jobs 1 --caps 18000 --hours 0.02` (CaDiCaL's default options, no `--sat`: compare with X0 lane 0).
  - lane 1, one after the other while time is left: `0s0_5_2__1s0-2s1-3s0-4s0-6s0-7s0`, `0s0_2_3__1s0-3s1-4s0-5s0-6s1-7s0`, `0s0_1_3__2s0-3s1-4s0-5s0-6s0-7s0`, each with `python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl NODE --jobs 1 --caps 3600 --cadopts=--sat --hours 0.02`. These layer children timed out at 600 s in C3W4.

In every machine: every 15 minutes, log the time, the free memory (`free -m`) and the size of `/opt/work/ct/` to `mem.log`. END = your start + {H} hours − 15 minutes; kill everything still running then (whole process groups) and note which solves were cut. SAT, `PROOF NOT ACCEPTED` and checker-`none` handling exactly as in `results/C3W6/TASK.md` step 3. A checker that runs out of memory gives `none`: re-check that node alone if time allows and report it in either case.

Every 25 minutes and at the end, copy the out files to `results/C3H1/{V}/out.jsonl` (lane 0, then lane 1), plus `mem.log`, commit and push.

README.md and final message: the tool commits and the base check; for every node: status, solve and check seconds, proof bytes, and both checker verdicts; peak memory and disk use. X1: how many of the 8 nine-bit cubes were certified, and their total solve + check time against the six-bit cube's (X0 lane 0). X2: default options against `--sat` on the same cube. Then a short recommendation for the 320 six-bit cubes of the H3/one roots (which method and cap), with the expected core-hours and the memory needed per job.
