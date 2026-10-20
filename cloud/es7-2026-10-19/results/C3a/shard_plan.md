# Shard plan: C3 class, m = 11 (33 points), k = 7

Status: NOT closed. This is a deterministic recipe for finishing the conv-variant instance on more
machines, and the timing data measured so far. All numbers are from a 4-core cloud VM
(`env.txt`), with 2–5 solver processes sharing those cores.

## Exact inputs

- Generator: `cloud/es7-2026-10-19/results/C3a/c3cnf.py` at commit `0473a37` on branch es7-cloud
  (Python 3.11; no randomness).
- CNF (recommended, conv variant): `python3 c3cnf.py 11 7 --gon conv -o v3_m11_k7.cnf`
  - p cnf 466697 2115323; sha256 `023f8228ed2c43c6d42f8e9e527d61e974696411cd8b44e568fe5599c4b826b0`
- CNF (chain variant, the encoding the task asked for): `python3 c3cnf.py 11 7 -o c3_m11_k7.cnf`
  - p cnf 168399 4154921; sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`
- Cubes: march_cu from https://github.com/marijnheule/CnC at commit 705b60c, built with
  `-fcommon` added to CFLAGS and with one patch: in `march_cu/microsat.c` set
  `S->mem_max = 600000000;` (the default 10000000 overflows on these CNFs, and the realloc path
  leaves dangling pointers, causing a segfault on any CNF with m >= 9). Run with
  `ulimit -s unlimited`.
  - `march_cu v3_m11_k7.cnf -d 12 -o conv_m11k7_d12.icnf` → 4,096 cubes, 0 refuted by march,
    sha256 `62dcd656d5412793d80bde5ccfa5fcf614d54c933940438d3ea60dd12b3bc395`, 538 s wall.
  - `march_cu v3_m11_k7.cnf -d 8 -o conv_m11k7_d8.icnf` → 256 cubes, sha256
    `4cd7e31465e80c83539e9d8ab27738947d64faaf93ed370411bc1a90db10230b`, 120 s wall; a re-run gave
    the identical file (`logs/march_determinism.log`).
  - Both cube files are in `cubes/` (`cubes/SHA256SUMS`). Coverage (the negated cubes form an
    UNSAT formula) is certified for both by CaDiCaL + lrat-check (E2 patch) + cake_lpr.
- Leaf i = the CNF plus the literals of cube i (line i of the cube file, 0-based) as unit
  clauses. `cnc_run.py` builds it, runs `cadical -q --lrat --binary=false -t LIMIT`, and accepts
  an UNSAT leaf only if lrat-check (E2 patch) and cake_lpr both accept the proof. Each leaf has
  weight 2^-12; the instance is closed when all 4,096 are.

## Measured per-cube times

TIMES_PLACEHOLDER

## Recipe for N machines

SHARD_RECIPE_PLACEHOLDER
