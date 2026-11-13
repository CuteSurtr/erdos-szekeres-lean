# SATOPEN20261113: two open SAT problems, pushed for 3.5 hours (13 November 2026, 02:00–05:50 KST)

Problems: **C** = is there an 8-fold rotationally symmetric set of 128 points in general position without a convex
9-gon (`LBK9OCT20261111`; best known 120)? **N(9)** = is the PRIMEFOLD Theorem E relaxation UNSAT at m = 9, n = 29,
i.e. is B(4) = 28 maximal for single-orbit clusters (`PRIMEFOLD` §4, `CATALAN20261110`)?

**Outcome.**
- **C, PROVED** (every cube cake_lpr-verified; on the written, unrefereed soundness of `LBK9OCT20261111`).
  *Theorem 5:* the longest monotone subsequence of the phases psi_1..psi_15 has length at most 13 (no spiral with one
  displaced layer; 9 new cubes). *Theorem 6:* psi_1..psi_15 is not a cyclic spiral (layer 0 displaced; 8 cubes).
  *Theorems 6′, 6″:* psi_1..psi_14 (whatever psi_15) and psi_2..psi_15 (whatever psi_1) are not cyclic spirals
  (18 cubes). With Theorem 1: **the cyclic order of the 16 layer phases is never a spiral with at most one layer
  displaced.** Eight further cases of the next ring (two displaced layers) are certified. 128 points stay open; no
  model was found.
- **C, HEURISTIC.** Random full phase orders with their bins are refuted in 12–38 s; descent pattern + bins in
  2–4 minutes; the descent pattern alone not within 30 minutes; near-spiral cubes take 6–23 minutes. The full next
  ring (two displaced layers, 270 cases) would cost about 55 CPU-hours.
- **N(9), PROVED:** F = `clsat2.py 9 29 1` is invariant under the reflection sigma (script check), so F is UNSAT iff
  F ∧ ¬G[8,5] is (Lemma N1). **N(9), open:** the lookahead cube-and-conquer under ¬G[8,5] (1,324 nodes, 597
  cake_lpr-verified leaves, 65 open) did not converge, and one 2-hour CaDiCaL run on F ∧ ¬G[8,5] gave no verdict
  (14.5 M conflicts).

Rigor labels: **PROVED** = every UNSAT cube accepted by cake_lpr ("s VERIFIED UNSAT", bound to the SHA-256 of the
cube formula and of the proof) and the case split covered by a written argument and a script check; it inherits the
unrefereed written soundness of the clause families (`LBK9OCT20261111/SOUNDNESS.md`, with its one floating-point step
with explicit error bounds, for C; `clsat2.py` and `PRIMEFOLD/cluster/PROOFS.md` for N). Nothing here is refereed or
independently reviewed. **COMPUTED** = solver verdict only. **HEURISTIC** = timings, statistics, estimates.

Resources: at most 5 threads and 20 GB (decimal) in total, all in systemd user units `nov13-sat-*` (nice 10): one k9
scheduler unit (`nov13-sat-k9`: CPUQuota 400 %, 300 % from 02:41 to 02:55; MemoryMax 16,785 MiB) and one m9 unit at
a time (CPUQuota 100 %, 200 % from 02:41 to 02:55; MemoryMax 2,098 MiB). CaDiCaL 2.1.3 (`/usr/bin/cadical`, SHA-256
`4acf586001aa…`), cake_lpr (`~/.local/bin/cake_lpr`, SHA-256 `c14ff49853e8…`); lrat-check was not used. Work
directory (outside Git): `/home/jay/research/data/satopen-20261113` (`k9/`, `m9/`). Copies of all scripts:
`tools/k9/`, `tools/m9/`; full hashes of every certified cube: `HASHES.txt`; logs: `logs/`.

## C. k = 9, 8-fold symmetric 128-point set

### C.1 Base formula; no new clause family

`k9/BASE0.cnf` = encoder A (8, 9, 16) + chord + cone + threshold-order + cell (B = 2) + bin-order, i.e. the base
formula of `LBK9OCT20261111` Theorems 1–4 **without** Y units: 497,712 variables, 29,778,662 clauses, SHA-256
`b2a30933e5f760f57680c0bbf376c2364337259756ba7d8604649821ae555d1f`. It is the first 29,778,662 clauses of the
record's `sat/S8/S8.cnf`, whose last 105 lines were checked to equal `cnf/mono16.units` byte for byte:

```sh
{ echo "p cnf 497712 29778662"; tail -n +2 <lb-k9oct-work-dir>/sat/S8/S8.cnf | head -n 29778662; } > BASE0.cnf
```

Exact cross-checks: the body of BASE0 followed by `cnf/mono3to13.units` has the SHA-256 of the body of the certified
Theorem 3 base `S14.cnf` (`f6c391a5…`), and BASE0 + the record's Theorem 1 cube c_7 units, assembled the way
`solve.sh` does it, reproduces the record's cube hash `ed75abca144b…`. Variables: Y(i, j) = [psi_i < psi_j] (JSON map
`cnf/A_m8K9t16.cnf.json`, variable 42,673 + lexicographic index of (i, j)), Z_i = 497,697 + i = [psi_i < 22.5°].
**No clause family was added**: every cube only adds unit clauses (case assumptions), whose cover is argued below.
The record's gate already tested every family on non-monotone real configurations (98 of its 446 exact
configurations; 0 violations) and with cube-level SAT controls at t = 15, so its positive controls apply unchanged.

Pipeline per cube (`k9/tools/`): `mkcube.py` writes `cube.units`; `solve.sh DIR LIMIT` writes `cube.cnf` = BASE0 +
units (header adjusted; hash in `cnf.sha256`) and runs `cadical -t LIMIT --lrat --binary=false cube.cnf proof.lrat`;
`check.sh DIR` runs `cake_lpr --CML_HEAP_SIZE=8500 --CML_STACK_SIZE=1000 cube.cnf proof.lrat` (8.8 GB resident,
1–2 minutes), records both hashes, the solver statistics and the number of "s VERIFIED UNSAT" lines in `result.txt`,
and only after exactly one such line compresses the proof (`zstd -3`; hash appended) and deletes the cube CNF
(rebuildable from BASE0 + units, hash recorded). `sched.py` runs the jobs (4 solvers, or 2 solvers + 1 checker).

### C.2 Theorem 5: no spiral with one displaced layer (PROVED)

**Theorem 5.** Let S be an 8-fold rotationally symmetric set of 128 points in general position with no 9 points in
convex position (by the layer lemma, `LAYERLEAN`, 16 nested regular octagons). Then for no layer j in {1, …, 15} are
the 14 phases psi_i, i ≠ j, (weakly) increasing or (weakly) decreasing. Equivalently, the longest weakly monotone
subsequence of psi_1, …, psi_15 has length at most 13.

*Proof.* A monotone subsequence of length 14 omits exactly one index j (length 15 is Theorem 1).
(i) j in {1, 2, 3}: the other phases contain psi_4..psi_15, impossible by Theorem 4 (window 4..15, certified in
`LBK9OCT20261111`); j in {13, 14, 15}: they contain psi_1..psi_12 (Theorem 4, window 1..12).
(ii) j in {4, …, 12}: by the perturbation lemma (`SOUNDNESS.md` §0: ties among the 14 phases are separated in the
monotone direction, a zero phase moves to a small positive value, psi_j moves to a generic value; the order type is
kept) and the reflection (`SOUNDNESS.md` §5, which turns "decreasing on a set of layers" into "increasing on it"),
there would be a configuration with (H), (G), (N) and psi strictly increasing on {1..15} \ {j}. Its intended
assignment satisfies BASE0 (`SOUNDNESS.md` §1–§4) and the 91 units Y(a, b), a < b, a, b ≠ j: cube `exJ_all` (no Z
units). All nine cubes are UNSAT with cake_lpr-verified proofs. `k9/tools/verify_ex_all.py BASE0.cnf` checks that
each cube file consists of exactly these 91 literals (recomputed from the JSON map) and that SHA-256(BASE0 + units)
equals the recorded cube hash: 9/9 MATCH (`logs/verify_ex_all.txt`). ∎

| cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 | proof.lrat.zst SHA-256 |
|---|---:|---:|---:|---|---|---|---|
| ex4_all | 1114 | 159,935 | 1.82 | verified, 109 s (heap 8500) | `710bf643af17…` | `8dc5d63c489b…` | `271135f2e49b…` |
| ex5_all | 1170 | 156,612 | 1.90 | verified, 106 s (heap 8500) | `c1ae4153289d…` | `5a06e064ed5c…` | `fe5156d65eb8…` |
| ex6_all | 1069 | 162,280 | 1.87 | verified, 108 s (heap 8500) | `fc19a4bd56f8…` | `c3c6ba77181b…` | `2a8561bf92d4…` |
| ex7_all | 1238 | 167,186 | 1.95 | verified, 105 s (heap 8500) | `c3711c0c1ea1…` | `6b636ef91e09…` | `5f5fec6b5976…` |
| ex8_all | 1042 | 147,598 | 1.79 | verified, 102 s (heap 8500) | `292d77f8edc3…` | `2a18ce194b98…` | `417029df296a…` |
| ex9_all | 1130 | 161,517 | 1.84 | verified, 108 s (heap 8500) | `4019440ffb63…` | `21c4e23d046b…` | `143b5b6d64e9…` |
| ex10_all | 1172 | 155,140 | 1.83 | verified, 106 s (heap 8500) | `33ea87ab5dad…` | `678a755b2059…` | `1cf21a3ea529…` |
| ex11_all | 1358 | 179,881 | 1.94 | verified, 104 s (heap 8500) | `2a6234e05dd6…` | `ebdc45c69639…` | `e664372365b9…` |
| ex12_all | 1123 | 158,084 | 1.97 | verified, 114 s (heap 8500) | `3d29ff961b4f…` | `2db87eb639e5…` | `cf250027555c…` |

Totals: 10,416 s of CaDiCaL (1,448,233 conflicts), 16.9 GB of LRAT (kept zstd-compressed as
`k9/cubes/exJ_all/proof.lrat.zst`), 16 minutes of cake_lpr.

For j = 8 the bin split was also tried first: cubes `ex8_r0`, `ex8_r7`, `ex8_r14` of the decision list
c_r = (Z_{s_1..s_r} true, Z_{s_{r+1}} false) over the sorted layers s of {1..15} \ {8} (cover of all 2^14
assignments checked by `verify_cover_ex.py 8`) took 185, 399 and 345 s (all cake_lpr-verified): the 15 bin cubes
would have cost about 75 minutes against 17 for the unsplit cube. They are redundant now.

### C.3 Theorem 6: the inner 15 layers are not a cyclic spiral (PROVED)

Only the cyclic order of the phases on R/45° matters geometrically, and psi is measured from layer 0, so
psi_1..psi_15 is the cyclic order of all 16 phases cut at layer 0. Theorem 5 says that deleting a layer j in {1..15}
never leaves the cyclic spiral (0, 1, …, 15) minus j, in either orientation. The case j = 0:

**Theorem 6.** In every such set there is no p in {0, …, 14} with psi_{p+1} < … < psi_15 < psi_1 < … < psi_p, nor
one with all these inequalities reversed (weak inequalities included).

*Proof.* p = 0 is Theorem 1. p in {1, 2, 3}: psi_4 < … < psi_15, Theorem 4; p in {12, 13, 14}: psi_1 < … < psi_12,
Theorem 4. p in {4, …, 11}: perturbation and reflection as above (the reflection reverses the whole order) give a
configuration whose intended assignment satisfies BASE0 and the 105 Y units of one total order: cube `cycP`.
`k9/tools/verify_cyc.py BASE0.cnf` rebuilds the order from the 105 literals, checks that it is total and equal to the
cyclic spiral cut after p, and recomputes the cube hash: 8/8 (`logs/verify_cyc.txt`). All eight cubes are UNSAT
with cake_lpr-verified proofs. ∎

| cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 | proof.lrat.zst SHA-256 |
|---|---:|---:|---:|---|---|---|---|
| cyc4 | 448 | 51,965 | 1.18 | verified, 83 s (heap 8500) | `c6dcc2b55187…` | `dbc9b45de754…` | `d3f3800faf29…` |
| cyc5 | 390 | 46,623 | 1.04 | verified, 83 s (heap 8500) | `7976983d87bb…` | `1fbc5462d85f…` | `2bac69ac26a0…` |
| cyc6 | 386 | 44,394 | 1.10 | verified, 89 s (heap 8500) | `089e1907ddc0…` | `8d8ea4ca6dd3…` | `cfc48b83b0d6…` |
| cyc7 | 372 | 47,860 | 1.06 | verified, 80 s (heap 8500) | `ecbb6ee88708…` | `625f0ed04496…` | `031f8095a38f…` |
| cyc8 | 365 | 54,086 | 1.27 | verified, 86 s (heap 8500) | `0e76fa31477f…` | `4c30d320e51a…` | `8ccaf4533e73…` |
| cyc9 | 414 | 46,686 | 1.14 | verified, 83 s (heap 8500) | `078fb5ddb06f…` | `8fff6d2a1ef9…` | `6be62474e431…` |
| cyc10 | 490 | 61,201 | 1.25 | verified, 91 s (heap 8500) | `e8613478dde1…` | `3ec6e10e12af…` | `8e70192b07fb…` |
| cyc11 | 442 | 55,141 | 1.21 | verified, 97 s (heap 8500) | `4459a2c7159f…` | `d80073ed12b6…` | `3f783b0f7969…` |

Totals: 3,307 s of CaDiCaL (407,956 conflicts), 9.3 GB of LRAT, 11.5 minutes of cake_lpr.

**Together (Theorems 1, 5, 6):** in an 8-fold 128-point set without a convex 9-gon, the cyclic order of the 16 layer
phases is never a spiral with at most one layer displaced. The four known 120-point sets and both 128-point near
misses are exact spirals. This is still a tiny part of the 15!/2 orders.

### C.3b Theorems 6′ and 6″: the same with the innermost or the second layer free (PROVED)

**Theorem 6′ (innermost layer free) and 6″ (layer 1 free).** In every such set, psi_1..psi_14 is not in cyclic
spiral order (no P in {0, …, 13} with psi_{P+1} < … < psi_14 < psi_1 < … < psi_P, nor reversed), whatever psi_15
is; and psi_2..psi_15 is not in cyclic spiral order (psi_{P+2} < … < psi_15 < psi_2 < … < psi_{P+1}, or reversed),
whatever psi_1 is.

*Proof.* 6′: P = 0 is Theorem 5 (j = 15); P in {1, 2}: psi_3..psi_14 increasing, Theorem 3; P in {12, 13}:
psi_1..psi_12 increasing, Theorem 4. 6″: P = 0 and P in {1, 2}: psi_4..psi_15 increasing, Theorem 4; P in {12, 13}:
psi_2..psi_13 increasing, Theorem 3. P in {3, …, 11}: perturbation and reflection as in C.2 give a configuration
whose intended assignment satisfies BASE0 and the 91 Y units of the total order of the 14 layers (the free layer
unconstrained): cubes `cycx_k15_pP` and `cycx_k1_pP`. `k9/tools/verify_cycx.py BASE0.cnf NAME…` rebuilds each order
from its literals, checks that it is the stated cyclic spiral cut after P with no literal on the free layer, and
recomputes the cube hash. ∎

| cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 | proof.lrat.zst SHA-256 |
|---|---:|---:|---:|---|---|---|---|
| cycx_k15_p3 | 416 | 47,151 | 1.09 | verified, 84 s (heap 8500) | `ea0f55a6eb28…` | `8b94542b4078…` | `bbb11537ded1…` |
| cycx_k15_p4 | 388 | 46,550 | 1.09 | verified, 82 s (heap 8500) | `64c085f2dd97…` | `422c21375726…` | `ae380698efa7…` |
| cycx_k15_p5 | 404 | 45,473 | 1.06 | verified, 77 s (heap 8500) | `8e31abc65a3f…` | `0201fc566fe6…` | `8133283fd1f3…` |
| cycx_k15_p6 | 352 | 47,818 | 1.11 | verified, 95 s (heap 8500) | `06b25e50987d…` | `371dd4d50e45…` | `7651ce816049…` |
| cycx_k15_p7 | 366 | 45,861 | 1.10 | verified, 84 s (heap 8500) | `b847e1683e31…` | `1238321afe66…` | `180bf30bc8db…` |
| cycx_k15_p8 | 382 | 44,042 | 1.05 | verified, 86 s (heap 8500) | `a04eb0f03e7b…` | `212bce44e318…` | `2779e7e74d7e…` |
| cycx_k15_p9 | 503 | 62,577 | 1.25 | verified, 88 s (heap 8500) | `e5267df61341…` | `f9116a31a8df…` | `d484209b43b2…` |
| cycx_k15_p10 | 431 | 55,564 | 1.27 | verified, 88 s (heap 8500) | `6862661617aa…` | `3b1cbea6ce9b…` | `822922276868…` |
| cycx_k15_p11 | 456 | 59,489 | 1.23 | verified, 91 s (heap 8500) | `83f556f01814…` | `7485f38f2a56…` | `7f7341bb2667…` |
| cycx_k1_p3 | 419 | 49,112 | 1.04 | verified, 88 s (heap 8500) | `5ff9b67ed471…` | `f2fcde7119cd…` | `1a76b0d9a27b…` |
| cycx_k1_p4 | 391 | 50,410 | 1.10 | verified, 81 s (heap 8500) | `8e74c9b6b61b…` | `71cff2a3c41a…` | `4f3ad0fda223…` |
| cycx_k1_p5 | 428 | 50,955 | 1.10 | verified, 84 s (heap 8500) | `af16af8edea4…` | `838b511a81f9…` | `ff045ca24dfa…` |
| cycx_k1_p6 | 392 | 50,562 | 1.10 | verified, 86 s (heap 8500) | `90dbcb5e1228…` | `b1f220eb3d69…` | `36b6d3368e2c…` |
| cycx_k1_p7 | 356 | 45,153 | 1.02 | verified, 82 s (heap 8500) | `433d4d336e1f…` | `6f289e70b28b…` | `cf3ed2d12453…` |
| cycx_k1_p8 | 456 | 55,826 | 1.24 | verified, 89 s (heap 8500) | `72323b7e6fca…` | `0243f0208f77…` | `df138be4d35a…` |
| cycx_k1_p9 | 476 | 53,906 | 1.20 | verified, 84 s (heap 8500) | `54721f7d7bb2…` | `5193db9cf9ad…` | `7e153207a39c…` |
| cycx_k1_p10 | 494 | 59,331 | 1.16 | verified, 89 s (heap 8500) | `6af56a00d066…` | `4b8af5dbc1bf…` | `8cd4f1c0bbd9…` |
| cycx_k1_p11 | 505 | 59,915 | 1.14 | verified, 89 s (heap 8500) | `2336ad6ef16d…` | `2cb27c174251…` | `fa82b7148efd…` |

Totals (18 verified cubes): 7,615 s of CaDiCaL (929,695 conflicts), 20.4 GB of LRAT, 25.8 minutes of cake_lpr.

### C.4 Hardness probes (HEURISTIC)

Random phase vectors (`random.Random(seed)`, 15 iid uniform phases in (0°, 45°)), cubes made from them: "YZ" = all
105 Y units + 15 Z units (full order and bins), "DZ" = the 14 consecutive Y units (descent pattern) + Z, "D" = the
descent pattern alone, "Y" = the full order alone, "B<w>Z" = Y(i, j) for 1 <= j − i <= w, plus Z. "noproof" = run
without LRAT (statistics only, no certificate).

| probe | cube | units | result | CaDiCaL s | conflicts | certificate |
|---|---|---:|---|---:|---:|---|
| p1_YZ | seed 1: full order + Z | 120 | UNSAT | 18 | 1,869 | cake_lpr verified |
| p2_YZ … p9_YZ | seeds 2–9: full order + Z | 120 | UNSAT (all 8) | 12, 14, 16, 17, 23, 25, 34, 38 | 879–2,611 | noproof |
| p1_Y | seed 1: full order, no Z | 105 | UNSAT | 51 | 7,300 | noproof |
| p1_B3Z | seed 1: Y(i,j) for j−i <= 3, + Z | 54 | UNSAT | 66 | 6,021 | noproof |
| p1_B2Z | seed 1: Y(i,j) for j−i <= 2, + Z | 42 | UNSAT | 113 | 13,059 | noproof |
| p1_DZ | seed 1: descent pattern + Z | 29 | UNSAT | 234 | 36,367 | cake_lpr verified |
| p2_DZ | seed 2: descent pattern + Z | 29 | UNSAT | 132 | 14,960 | noproof |
| p1_D | seed 1: descent pattern only | 14 | unknown at the limit | 1,800 | 262,946 | noproof |
| p1_Z | seed 1: bins only | 15 | unknown at the limit | 900 | 152,674 | noproof |
| ex8_r0 | j = 8, 91 Y units + bin cube r = 0 | 92 | UNSAT | 185 | 15,196 | cake_lpr verified |
| ex8_r7 | j = 8, 91 Y units + bin cube r = 7 | 99 | UNSAT | 399 | 45,969 | cake_lpr verified |
| ex8_r14 | j = 8, 91 Y units + bin cube r = 14 | 105 | UNSAT | 345 | 39,552 | cake_lpr verified |
| ex8_all | j = 8, 91 Y units, no Z | 91 | UNSAT | 1,042 | 147,598 | cake_lpr verified |

Reading (seed 1 throughout, plus samples): the full order kills a random case in under a minute with or without the
bins (18 s / 51 s); with the bins, local order information suffices (pairs at distance <= 3: 66 s, <= 2: 113 s,
consecutive pairs only: 132–234 s), while the descent pattern alone (> 30 minutes) or the bins alone (> 15 minutes)
do not. The hard cases are the near-spiral orders (6–23 minutes per unsplit cube in C.2–C.5). A complete proof by
fully specified (descent pattern, bins) cubes would need about 4.8 million cubes (2·3^14 consistent pairs, halved by
the reflection) at minutes each; by descent patterns or by bin patterns alone, 8,192 or 16,384 cubes (up to
reflection) of more than 15–30 minutes each. None of these is in reach without stronger clauses or a smarter split.

### C.5 The next ring: two displaced layers (partial, PROVED cases + timing)

"A spiral with two displaced layers" splits into 95 linear cases (layers j < k in {1..15}; the other 13 phases
increasing: 78 Y units, cube `ex2_J_K`) and 175 cyclic cases (layer 0 and layer k displaced: the other 14 phases a
cyclic spiral cut after position P: 91 Y units, cube `cycx_kK_pP`), after removing the cases covered by Theorems 3–5
(counted by script). Cases run tonight (each UNSAT cube is a certified case; the families' soundness and the
perturbation/reflection argument are as in C.2):

| cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 | proof.lrat.zst SHA-256 |
|---|---:|---:|---:|---|---|---|---|
| ex2_7_9 | 1399 | 172,164 | 1.97 | verified, 109 s (heap 8500) | `ed1a9e504bfc…` | `61ad834d0cb2…` | `064b9abbdc71…` |
| ex2_6_10 | 1355 | 167,863 | 2.00 | verified, 112 s (heap 8500) | `688c4d5c4a1b…` | `00d71cdb5770…` | `92f7af45dda1…` |
| cycx_k8_p7 | 346 | 47,654 | 1.01 | verified, 81 s (heap 8500) | `d6190771aa8f…` | `14c4b462ccb4…` | `cca935dacf06…` |
| cycx_k4_p8 | 341 | 43,149 | 1.08 | verified, 84 s (heap 8500) | `956b2c917134…` | `5dfded1efaa4…` | `30d8c99f05fa…` |
| cycx_k12_p5 | 344 | 49,104 | 1.07 | verified, 82 s (heap 8500) | `61f900df1b79…` | `c1429a7fbb2d…` | `6633fa98fe3e…` |
| cycx_k14_p5 | 361 | 43,246 | 1.07 | verified, 81 s (heap 8500) | `ac1c728233c6…` | `cd92864b03db…` | `f77de70030e2…` |
| cycx_k2_p7 | 461 | 54,605 | 1.19 | verified, 88 s (heap 8500) | `4ea514395f2e…` | `ca1847baf543…` | `1ab827c17559…` |
| cycx_k13_p6 | 359 | 47,447 | 1.05 | verified, 78 s (heap 8500) | `754973daffa1…` | `ffc84d42614b…` | `c8d9a3f89962…` |

Cost of the whole ring (HEURISTIC): linear cases take about 23 minutes (1,355 and 1,399 s), cyclic cases about
6–8 minutes (341–505 s over 24 cases, including the 18 of C.3b), each plus 1.5–2 minutes of cake_lpr. All 270
cases: about 95 × 23 + 175 × 6.5 minutes ≈ 55 CPU-hours of CaDiCaL plus about 8 hours of cake_lpr (one checker
at a time, 9 GB). Done so far: 2 linear and 24 cyclic cases (`logs/verify_cycx.txt`: 24/24 orders and hashes).

### C.6 Next step for C

- **Finish the ring "two displaced layers"** (the 95 linear and 175 cyclic cases of C.5; `mkcube.py ex2 J K` and
  `mkcube.py cycx K P` write them; the 18 cases of Theorems 6′/6″ and eight further cases are done). At tonight's
  rates that is about 55 CPU-hours of CaDiCaL plus 8 hours of cake_lpr, two to three nights at the present 5-thread
  cap. Result: "no spiral with two displaced layers", the next level after Theorems 1, 5 and 6.
- **Fewer, larger cases.** One unsplit cube was 4 times cheaper than its 15 bin cubes. The cut positions of a cyclic
  family (up to 14 cubes) could likewise go into one formula (clauses saying "these phases form a cyclic spiral")
  instead of one cube each; worth a timing test before the ring.
- **The bulk.** A random order dies quickly once local order information and the bins are fixed (C.4: pairs at
  distance <= 3 plus bins, 66 s), but neither the descent pattern alone (> 30 minutes) nor the bins alone
  (> 15 minutes) suffice. A split that fixes the bins and the order of nearby layers first, with a lookahead deciding
  where more order is needed, is the natural experiment towards a complete proof.
- **No model.** Every non-spiral order tried (9 random full orders, two random descent patterns with bins and all
  cases above) was refuted. 128 points look impossible, but nothing beyond the stated families is proved.

## N. PRIMEFOLD Theorem E relaxation, m = 9, n = 29

### N.1 Formula and a symmetry-breaking unit (PROVED: written argument + exact script check)

F = `clsat2.py 9 29 1` (`PRIMEFOLD/cluster/clsat2.py`, SHA-256 `29240aba…`; sig = 1, with the signotope axiom):
11,902 variables, 377,002 clauses, SHA-256 `75227ecb758e773e04dfee2e259ab4917361c7f976562eb22128e4089da0d39f`
(regenerated tonight byte-identical to `m9-cluster-20261110/m9_n29_s1.cnf`). UNSAT of F would mean that no generic
29-point cluster satisfies Proposition C (i), hence N(9) = 28 (B(4) = 28 is attained by the rule cluster).

**Symmetry.** sigma: L[i,j,v] -> ¬L[i,j,B−v] (B = m − 2 = 7), T[i,j,k] -> ¬T[i,j,k], CU[i,j,l] <-> CA[i,j,l],
G[x,a] <-> H[x,a] (geometrically the reflection y -> −y in the frame of `PROOFS.md`: t -> m − t, left <-> right
turns, cups <-> caps, g <-> h). `m9/tools/sigma.py 9 29 F` rebuilds the variable numbering of `clsat2.py` and checks
that sigma maps the multiset of clauses of F (literals sorted) onto itself: **INVARIANT** (also for sig = 0).

**Lemma N1.** If F is satisfiable, so is F ∧ ¬G[8,5] (variable 11834: "a cup with all t < 8 and at least 5 points").
*Proof.* Let M be a model of F with M(G[8,5]) = true. F contains (¬G[8,5] ∨ ¬H[8,5]) (line 376,968; `clsat2.py`
emits ¬G[x,a] ∨ ¬H[x,b] whenever a + b > x + 1), so M(H[8,5]) = false. Put M'(l) := M(sigma(l)) (consistent, since
sigma commutes with negation). M' satisfies a clause C iff M satisfies sigma(C), a clause of F; so M' is a model of F,
and M'(¬G[8,5]) = M(¬H[8,5]) = true. ∎ Hence F is UNSAT iff F ∧ ¬G[8,5] is.

### N.2 What was run

**Adaptive cube-and-conquer** (`m9/tools/m9cc.py`; 02:16–03:20). Root cube [¬G[8,5]]. An open cube (unit clauses)
gets CaDiCaL without proof for TL seconds (30 s until 02:24, 8 s until 02:27, 4 s until 02:34, then 2 s). If UNSAT it
is solved again with text LRAT and checked at once by cake_lpr (heap 1,500 MB, 800 MB from 02:41; a 15 MB m9 cube proof
needs 0.62 GB); hashes and verdict go to `nodes/<id>/result.txt`, the proof is kept zstd-compressed
only after "s VERIFIED UNSAT". Otherwise the cube is split on the variable v that maximises
(n(v) − n0)(n(¬v) − n0) + n(v) + n(¬v), n(·) = number of literals implied by MiniSat 2.2 propagation (pysat
1.9.dev20), children cube + [v] (id + "0") and cube + [¬v] (id + "1"); depth first. `m9/tools/verify_tree.py OUT`
checks the decision-tree structure (each split node has exactly these two children, so the leaves cover the root
cube), the cake_lpr line of each verified leaf, and delegated leaves recursively. From 02:41 to 02:55 the subtree
r10 = [¬G[8,5], ¬H[8,6], G[2,2]] ran as a second tree `cc2` (`delegate.py`; a 60 s CaDiCaL probe had not decided it),
then it was stopped because its open set kept growing and Problem C needed the thread.

**Tree result (COMPUTED, partial; every leaf certificate PROVED).** `m9/cc1` (root [¬G[8,5]]): 1,021 nodes, 510
splits, 501 leaves verified by cake_lpr, 9 open, 1 delegated (r10). `m9/cc2` (root r10): 303 nodes, 151 splits, 96
leaves verified, 56 open. All 597 verified leaves carry "s VERIFIED UNSAT" bound to their cube and proof hashes
(`verify_tree.py`: structure OK for both trees; `logs/m9_verify_tree.txt`; every node with its hashes in
`logs/m9_cc1_tree.tsv`, `logs/m9_cc2_tree.tsv`). Leaf cubes have 4–103 literals; a leaf took 1.1 s to solve
(median, at most 5.1 s); proofs 0.2–15.9 MB (3.9 GB of LRAT in total, kept zstd-compressed). The splits first fix
profile variables (G, H), then cup/cap (CU, CA) and slope (L) variables of the last points of the cluster; most splits
peel off one
child that dies in under a second, and the open nodes sit at depths up to 95. No SAT leaf. Apart from single leaves,
no closed subtree has a short cube, so the partial tree proves no statement of independent interest; it is a
measurement. The other root branch r0 = [¬G[8,5], H[8,6]] was decided UNSAT by a separate 1.5 s probe (no proof),
as Erdős–Szekeres predicts (it forces g(8) <= 3, so g(8) + h(8) <= 9 allows at most C(7,2) = 21 points).

**One long run** (03:20–05:24): `cadical -t 7400 --lrat --binary=false` on F ∧ ¬G[8,5] (`m9/root/root.cnf`,
SHA-256 `dd983a117d8e…`). Result (COMPUTED): **no verdict** within the limit (7,392 s of process time,
14,516,496 conflicts; `cadical exit 0 seconds 7400`). The partial LRAT (13.6 GB) cannot be certified and is kept in
`m9/root/root.lrat` (deletion is the author's decision). For comparison, the 13 runs of 10–11 November (5,400 s each,
without the symmetry-breaking unit, on the n = 29 and n = 30 formulas) reached 9.4–26.9 M conflicts without a
verdict.

### N.3 Next step for N(9)

- The cube tree did not converge: about 1,300 nodes and 600 cake_lpr-verified leaves in about 80 minutes of one
  thread, with open subtrees at depths up to 95. The branch G[2,2] (a segment in the first direction bin), searched
  separately as `cc2`, is bushy. Plain DFS with a fixed short TL is not a viable route at this size.
- Suggested: (1) a real lookahead cuber (march_cu, or the cuber used for the empty-hexagon problem) with a cutoff on
  the number of free variables, on F ∧ ¬G[8,5], with many cores; each verified leaf stays a valid certificate for its
  cube and can be reused by any later tree that contains that cube. (2) Satisfiability-preserving extra clauses
  before cubing: profile monotonicity G[x,a] → G[x+1,a] and H[x,a] → H[x+1,a] (written argument: replacing CU, CA,
  G, H by their least values forced by L and T keeps every clause of F true and satisfies these implications, because
  le(i,j,x−1) → le(i,j,x)); a SAT control at n = 28 is needed before use. (3) For scale: the largest certified
  Theorem E proof (m = 8, n = 15) has 25 MB (`PRIMEFOLD` §4); at m = 9, n = 29 one 2-hour run (14.5 M conflicts)
  wrote 13.6 GB of LRAT without a verdict.

## Incidents and deviations

- **In-place script edits (02:19).** `k9/tools/solve.sh` and `k9/tools/check.sh` were rewritten in place while jobs
  were executing them (the mistake `LBK9OCT20261111/logs/notes.txt` records for 23:07 on 11 November). After its
  CaDiCaL run had ended, the shell of cube `ex8_r7` read the tail of the new file: it overwrote `solved` and deleted
  `cube.cnf`. The proof was complete (`cadical.out`: "s UNSATISFIABLE", exit 20, 397.81 s); the cube CNF was rebuilt
  from BASE0 + `cube.units` (`sha256sum -c cnf.sha256`: OK), the `solved` line was rewritten with a note, and
  cake_lpr then accepted the proof. The check shell of `p1_YZ` exited with status 2 after its record was complete
  (verdict and hashes intact). The open inode of the only other affected shell (ex8_all) was restored to the original
  559 bytes before its run ended (its `solved` line is correct); every later change was installed by `mv`.
- **Memory caps (02:26).** The first caps were MiB values summing to 20.97 GB; they were lowered at run time to
  16,785 MiB (k9) + 2,098 MiB (m9) = 19.80 GB. Measured peaks: CaDiCaL on a 29.8 M-clause cube 3.9–4.0 GB;
  cake_lpr heap 8,500 MB: 8.8 GB resident (heap 11,000 MB: 11.4 GB; 8,500 sufficed for every proof tonight).
- **m9 restarts** (02:24, 02:26, 02:33, 02:36, 02:41, 02:55) changed TL, the cake_lpr heap or the number of drivers;
  the tree is saved after every node, so a restart only repeats the node in progress. At 03:20 the DFS was stopped
  for good and the thread given to one long run on the symmetry-broken root (N.2).
- Lead-agent units (`nov13-res33-*`, `nov13-theory-*`) were not touched.

## Files

In this directory (`SATOPEN20261113/`):
- `README.md` (this file); `HASHES.txt`: full SHA-256 of the cube CNF, the LRAT proof and its `.zst` for every k9 cube
  with a cake_lpr verdict (from each `result.txt`).
- `tools/k9/`: `mkcube.py` (cube unit files: kinds `ex`, `ex2`, `cyc`, `cycx`, `perm`), `solve.sh`, `check.sh`,
  `sched.py` (as on disk; the running scheduler was started at 02:13 from the version without the `noproof` filter in
  its check queue, which `check.sh` handles instead), `verify_ex_all.py`, `verify_cyc.py`, `verify_cycx.py`,
  `verify_cover_ex.py`, `table.py`, `probetable.py`, `hashes.py`, `summary.sh`.
- `tools/m9/`: `sigma.py` (symmetry check), `m9cc.py` (cube-and-conquer driver), `verify_tree.py`, `treestats.py`,
  `decode.py`, `delegate.py`, `run2.sh`, `root_run.sh` (the long run). `tools/SHA256SUMS.txt` hashes all of them.
- `logs/`: `k9_sched.log`, `k9_queue.txt`, `k9_results.txt` (every k9 `result.txt` and `solved` line),
  `verify_ex_all.txt`, `verify_cyc.txt`, `verify_cycx.txt`, `verify_cover_ex8.txt`, `m9_cc1_tree.tsv`,
  `m9_cc2_tree.tsv` (every node: cube, status, cube CNF and LRAT hashes, verdict), `m9_cc1_log.txt`,
  `m9_cc2_log.txt`, `m9_verify_tree.txt`, `m9_sigma.txt`, `m9_root_cadical.out`.

In the work directory (outside Git): `k9/BASE0.cnf`; `k9/cubes/<name>/` (`cube.units`, `cube.desc`, `cnf.sha256`,
`cadical.out`, `solved`, `result.txt`, `cake.out`, `cake.err`, `proof.lrat.zst`); `m9/cc1/`, `m9/cc2/` (trees and
`nodes/<id>/result.txt`, `proof.lrat.zst`); `m9/root/` (the long run; its partial LRAT `root.lrat`, 13.6 GB,
cannot be certified and is kept: deletion is the author's decision). Disk use about 29 GB (k9 16 GB, m9 14 GB, of
which 13.6 GB is the partial root LRAT). The 70 GB of old partial proofs in `m9-cluster-20261110` were not touched.

Reproduction (from the work directory; Python 3, CaDiCaL 2.1.3, cake_lpr, zstd; pysat for the m9 driver):

```sh
# C: one case, e.g. Theorem 5, j = 8
python3 k9/tools/mkcube.py ex 8 -1 k9/cubes/ex8_all          # or: cyc 8 k9/cubes/cyc8; cycx 15 6 k9/cubes/cycx_k15_p6
sh k9/tools/solve.sh k9/cubes/ex8_all 5400                   # cube CNF SHA-256 292d77f8…, about 17 minutes
HEAP=8500 sh k9/tools/check.sh k9/cubes/ex8_all              # result.txt must say VERIFIED_LINES 1
python3 k9/tools/verify_ex_all.py k9/BASE0.cnf; python3 k9/tools/verify_cyc.py k9/BASE0.cnf
python3 k9/tools/verify_cycx.py k9/BASE0.cnf cycx_k15_p3 … cycx_k1_p11
# N
python3 <R>/PRIMEFOLD/cluster/clsat2.py 9 29 1 m9/m9_n29_s1.cnf      # SHA-256 75227ecb…
python3 m9/tools/sigma.py 9 29 m9/m9_n29_s1.cnf                     # INVARIANT
OUT=m9/cc1 TL=2 PL=600 CAKEHEAP=800 python m9/tools/m9cc.py          # resumes the tree
python3 m9/tools/verify_tree.py m9/cc1; python3 m9/tools/treestats.py m9/cc1 1
```
