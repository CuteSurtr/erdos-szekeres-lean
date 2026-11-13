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

All on the conv CNF, CaDiCaL 3.0.1 with `--lrat --binary=false`, 2 to 4 solvers on 4 vCPUs.

| cube level | leaves tried | result |
|---|---|---|
| plain (no cubes) | 1 | open after 1,200 s |
| march depth 8 | 0, 1 | open after 1,200 s each |
| march depth 12 | 0, 256, 512, 768 | open after 1,500 s each |
| depth-12 leaf 0, then `march_cu -d 6` (depth 18) | 22 of 64 | all UNSAT and all certified: solve 172–439 s, mean 290 s; dual LRAT check mean 176 s; proofs mean 1.94 GB |

For the chain CNF (the encoding the task specified): the 1,024 σ cubes (depth 10) stay open
after 3,600 s (cubes 0 and 1023), and march_cu is slow on it (depth 8 did not finish in 33 min).
The conv CNF is the better target.

Extrapolation, if every depth-12 leaf costs what leaf 0 does: 64 × 290 s ≈ 5.2 core-hours
of solving per depth-12 leaf, plus about 3.1 core-hours of checking. Over 4,096 leaves that is
about 21,000 core-hours of solving plus 13,000 of checking. This rests on ONE depth-12 leaf
(22 of its 64 sub-leaves) and could be off by a large factor either way. It is not a
"closable soon" instance. Better targets: (a) a cheaper split (a different march depth, or
cubing on σ first), measured on more than one leaf; (b) a stronger encoding; (c) mirror
symmetry breaking, which would halve the work and is not yet used.

## Recipe for N machines

Deterministic, with no coordination between machines beyond the shard index:

1. Build CaDiCaL 3.0.1 (c607304), drat-trim lrat-check (2e3b2dc) with
   `results/E2/tools/lrat-check-E2.patch`, cake_lpr, and the patched march_cu (above).
2. `python3 c3cnf.py 11 7 --gon conv -o v3_m11_k7.cnf` and check the sha256.
3. `march_cu v3_m11_k7.cnf -d 12 -o d12.icnf` (538 s) and check the sha256 against
   `cubes/conv_m11k7_d12.icnf`, or simply use that file.
4. Machine j of N takes the depth-12 leaves i with i mod N = j. For each leaf i:
   build `leaf_i.cnf` = CNF + its 12 literals as units (the header clause count goes up by 12);
   run `march_cu leaf_i.cnf -d 6 -o sub_i.icnf`; then
   `python3 cnc_run.py leaf_i.cnf sub_i.icnf out_i work_i --jobs <cores> --limit 1800`.
   That certifies coverage of sub_i, solves each sub-leaf, and accepts it only when both
   checkers accept. Run each checker one at a time, or give it about 5 GB of RAM: cake_lpr
   needs about 4.2 GB on these proofs.
5. A depth-12 leaf is closed when all 64 sub-leaves are certified (`summarize_leaves.py`
   reports relative weight 1). Sub-leaves still open at the limit get re-split by march_cu
   on their own leaf CNF, the same way. Any SAT: decode with `decode.py` (map from
   `c3cnf.py ... --map`), commit at once, then realize (`to_sig.py`, `tools/realizer`).
6. Done when all 4,096 depth-12 leaves are closed. The depth-12 cube coverage proof is
   already certified (`logs/conv_d12_cubes.json`).

Already done: depth-12 leaf 0 (`cubes/conv_m11k7_d12leaf0_d6.icnf`), sub-leaves listed in
`leaves.jsonl`; the remaining sub-leaves of leaf 0 are open.
