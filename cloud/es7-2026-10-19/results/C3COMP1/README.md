# C3COMP1: composition after wave 4, and a cap experiment on timed-out 6-bit cubes

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`), 16:56 to about 19:20 UTC on 2026-10-24 (H = 2.5).
Task `results/C3COMP1/TASK.md` at 1cb98b52. Start head: 5392150c.

## Tools (`tools.txt`)

- C3U2 tools: a worktree of cad4e050 at `/opt/c3u2`, used unmodified (`compose.py`, `close_tree.py`).
- Composer comparison: `results/C3U2/tests/frontier_cmp.py`, which imports C3U2 `compose.py` and
  `results/C3AUDIT3/tools/mycompose.py` (the fixed version, 5336f631) without changing them. Neither tools dir changed
  between cad4e050 and 5392150c.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch.
  Sanity check passed: on {1},{-1} the LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).

## Part 1: composition

Inputs (`compose_files.txt`): 187 record files at commit 5392150c, taken as a `git archive` snapshot. They are the 127 files of
`results/C3U2/compose_m11/files.txt`, plus 49 `results/C3W4/*/out.jsonl`, `results/C3W4/H01/recheck.jsonl` and 10
`results/C3W5/M00`–`M09/out.jsonl` (238 records; C3W5 was still running, so these are its progress pushes as of 5392150c).
That is 117,395 records. Runner: `compose_run.sh`. Sha checks were on: all 109,215 certified records were re-derived and matched.

| | C3U2 compose.py `--mirror-h6` | mycompose (fixed), same roots | C3U2 compose.py, no mirror | mycompose, no mirror |
|---|---|---|---|---|
| certified records / nodes | 109,215 / 109,073 | 109,215 / 109,073 | 109,215 / 109,073 | 109,215 / 109,073 |
| certified cube nodes | 19,103 | 19,103 | 19,103 | 19,103 |
| σ splits used | 676 | 681 (no H6 mirror) | 681 | 681 |
| class covered | **no** | **no** | **no** | **no** |
| depth-2 roots / open | 910 / **137** | 910 / **137** | 1,630 / 574 | 1,630 / 574 |
| root status differences | 0 | | 0 | |
| uncovered frontier (in roots) | 232,498 | 232,220 | 234,758 | 234,480 |

**The two composers agree on coverage (not covered) and on the set of open depth-2 roots in both modes: 0 differences.**
Their frontier sets differ, though: in the no-mirror run compose.py lists 278 more nodes, mycompose lists no node that
compose.py lacks (`compose/frontier_diff_nomirror.json`, produced with `tools/frontier_cmp_full.py`, which is frontier_cmp.py
writing the full difference lists). All 278 are 3-bit σ cubes (`R__a-b-c`) that have a σ-split record, an open σ split, and
no layer split. In `compose.py:224-237`, once a σ split fails, a cube node falls through to the layer branch, and with no
layer split it is appended to `missing`. So the node itself is listed beside the open leaves of its 8 sub-cubes. This is a
double count in the report only: the node is uncovered either way, and covered/uncovered never changes. The same 278
account for the whole mirror-mode difference too (47 roots, 1 to 8 nodes each). `open_roots.tsv` therefore gives
mycompose's leaf frontier as `frontier_size` and compose.py's as `compose_frontier`. `tools/make_open_roots.py` is C3U2's
script with the frontier-equality exit removed. It still exits on any status difference.

The frontier size measures the record tree, not remaining work. It counts every never-run layer child under a
timed-out cube (51 to 72 per cube), and also the open leaves of older layer-split trees from waves 1 to 3.

### Open roots per stratum (`open_roots.tsv`, `open_roots_strata.txt`; 910 roots of the reduced cut)

| stratum | roots | open | closed | open frontier (mycompose) | (compose.py) | open, touched | open, no record at all |
|---|---|---|---|---|---|---|---|
| H3/one | 5 | 5 | 0 | 23,028 | 23,060 | 4 | 1 (0s0_4) |
| H3/two | 95 | 65 | 30 | 165,027 | 165,214 | 35 | 30 |
| H6(1,1)/one | 5 | 2 | 3 | 8,310 | 8,322 | 2 | 0 |
| H6(2,1)/one | 5 | 4 | 1 | 25,851 | 25,876 | 4 | 0 |
| H6(3,1)/one | 5 | 2 | 3 | 962 | 969 | 1 | 1 |
| H6(4,0)/one | 5 | 1 | 4 | 1 | 1 | 0 | 1 |
| H6(4,1)/one | 5 | 1 | 4 | 8,101 | 8,103 | 1 | 0 |
| H6(5,0)/one | 5 | 2 | 3 | 2 | 2 | 0 | 2 |
| H6(5,1)/one | 5 | 3 | 2 | 272 | 276 | 2 | 1 |
| H6(4,0)/two | 76 | 1 | 75 | 1 | 1 | 0 | 1 |
| H6(4,1)/two | 76 | 7 | 69 | 436 | 444 | 4 | 3 |
| H6(5,0)/two | 76 | 11 | 65 | 11 | 11 | 0 | 11 |
| H6(5,1)/two | 76 | 33 | 43 | 218 | 219 | 2 | 31 |
| all other H6 strata (10) | 380 | 0 | 380 | 0 | 0 | | |
| **total** | **910** | **137** | **773** | **232,220** | **232,498** | 55 | 82 |

Compared with C3U2 (`results/C3U2/open_roots.tsv`, head 3fd8a4d8, 313 open), 176 roots closed since and none went from closed
to open. The 82 roots with no record are the C3W4 list rows that C3W4 did not reach. All 46 two-orbit ones are in
`results/C3W5/lists/W5_two.tsv`, which C3W5 is running now. The other 36 (30 H3/two, 1 H3/one, 5 one-orbit H6) are in no
current wave. All 6 touched open two-orbit H6 roots (frontier 93 to 135) are also in C3W5's shards.

## Part 2: what the open H3 and one-orbit roots need (`part2_*`, `tools/part2.py`)

The 85 open H3 or one-orbit roots (70 H3, 15 one-orbit H6) were read from the C3W4 and C3SIG2 records. Their 64 six-bit
cubes follow the C3U definition: two `sigma_children(·, 3)` steps from the root, which is what close_tree.py builds.
sigma_cubes.py records were read as records of node__C. Per root: `part2_cubes.tsv`. Per timed-out cube: `part2_subtrees.tsv`.

| stratum | open roots | 6-bit cubes certified | timed out at 300 s | never ran |
|---|---|---|---|---|
| H3/one | 5 | 0 | 231 | 89 |
| H3/two | 65 | 670 | 1,029 | 2,461 |
| H6(1,1)/one | 2 | 42 | 86 | 0 |
| H6(2,1)/one | 4 | 59 | 160 | 37 |
| H6(3,1)/one | 2 | 23 | 16 | 89 |
| H6(4,0)/one | 1 | 0 | 0 | 64 |
| H6(4,1)/one | 1 | 50 | 14 | 0 |
| H6(5,0)/one | 2 | 0 | 0 | 128 |
| H6(5,1)/one | 3 | 47 | 0 | 145 |
| total | 85 | 891 | 1,536 | 3,013 |

(36 of these roots have no record at all, which accounts for 2,304 of the "never ran" cubes. No cube has records only at
other caps. C3SIG2 cubes on other σ bits do not occur among these roots.)

- **Solve times of the 891 certified 6-bit cubes**: min 52, p10 114, p25 175, median 234, p75 269, p90 289, max 300 s,
  mean 217 s. Check time mean 46 s. The histogram climbs toward the cap: 181 cubes in [275, 300) s, 164 in [250, 275),
  142 in [225, 250), only 41 below 75 s. In these hard roots the 300 s cap cuts through the middle of the distribution.
  (Over all 138 W4-list H3/one-orbit roots, open or not, the median is 137 s.)
- **Layer subtrees under the 1,536 timed-out cubes**: 1,534 got a layer split (2 have none, from runs cut at END).
  Together they have 84,350 layer nodes (51 per cube, up to 585 with a second level). 10,464 were certified at cap 600,
  22 timed out (all but one in H3/one), and 73,864 never ran. Only 194 of 1,534 subtrees are fully certified.
  Certified first-layer children: solve median 16.8 s, p90 54 s, mean 24.9 s; check mean 26.6 s. So a fully certified
  layer subtree costs about 51 × 51.5 ≈ 2,600 core-s per cube.
  By stratum (timed-out cubes, layer nodes, certified, timed out, open, subtrees fully certified):
  H3/one 231, 17,865, 23, 21, 17,821, 0. H3/two 1,029, 52,409, 7,565, 1, 44,843, 142.
  H6(1,1)/one 86, 4,386, 843, 0, 3,543, 16. H6(2,1)/one 160, 8,160, 1,560, 0, 6,600, 27.
  H6(3,1)/one 16, 816, 0, 0, 816, 0. H6(4,1)/one 14, 714, 473, 0, 241, 9.

### Cap experiment (`cap_summary.tsv`, `cap_summary.txt`, `cap/out_lane*.jsonl`, `cap/lane*.log`)

Each cube ran alone as the root: `close_tree.py base out_laneL.jsonl CUBE --caps 1800 --jobs 3 --cadopts=--sat --hours 0.01`
(C3U2 tools at cad4e050, no σ split). `--hours 0.01` stops close_tree after level 0, the cube itself. A timed-out cube
therefore gets its layer-split record, but its children are not run. Three lanes ran in parallel (`cap_lane.sh`) with the
15 cubes of rows 0–14 of `cap_cubes.tsv`, picked as the first two cubes in file order that timed out at 300 s in C3W4, over
8 roots. When two lanes finished early, I added 6 more cubes (rows 15–20, 4 more roots) in two more lanes, with the same
settings and 3 lanes at a time. Row 17 (0s0_3) was not started because the last-start time (18:31) had passed.

| result | cubes | roots | solve s | check s |
|---|---|---|---|---|
| H3/two, H6 one-orbit: **certified** | **15 of 15** | 10 (3 H3/two, 7 H6 one-orbit) | 240.5, 250.7, 264.1, 268.1, 276.8, 288.4, 294.3, 294.5, 304.0, 306.7, 320.2, 330.1, 338.1, 342.6, 366.9 (mean 299) | 37.6–69.6 (mean 54) |
| H3/one: **timed out at 1800 s** | **5 of 5** | 3 (0s0_1, 0s0_2, 0s0_5) | 1800.1 each | |

Every certified cube got `c VERIFIED` and `s VERIFIED UNSAT`. There was no SAT and no rejected proof. In all, 20 cubes ran
over 13 roots.
- Every non-H3/one cube that timed out at 300 s in C3W4 closed directly, in 240–367 s. Its whole direct cost (solve +
  check) was 280–440 core-s. For 14 of these 15 cubes, C3W4 had already certified all 51 layer children (the 15th, 0s0-3s1_4, had none certified). Those subtrees
  took 813–1,921 s of solve plus a similar check time (`part2_subtrees.tsv`), so they cost 4 to 8 times as much as the
  direct solve at a larger cap.
- H3/one cubes are a different class. None closed in 1800 s here, none of 231 closed in 300 s, and their layer children
  time out at 600 s about half the time (21 of 44 run).

### Extra pilot (beyond the task): a third σ level on one H3/one cube

PILOT9_PLACEHOLDER

## Recommendation for the remaining roots

1. **Two-orbit roots (52 open: 6 touched, 46 untouched)**: all are in C3W5's shards. Leave them to C3W5
   (`--caps 300,300,600 --sigma-split 3 --sigma-levels 2 --split-singles`). The touched ones are almost done (frontier
   93–135). Compose again when C3W5 has pushed its final `out.jsonl`.
2. **H3/two and one-orbit H6 roots (35 + 10 touched, 30 + 5 untouched)**: change the 6-bit cube cap from 300 to 600:
   `--sigma-split 3 --sigma-levels 2 --caps 1,1,600,600 --cadopts=--sat`, with the layer split at 600 only as the fallback.
   Evidence: the certified-time histogram piles up at the 300 s cap, and 15 of 15 timed-out cubes closed in ≤ 367 s, at
   about a quarter of the cost of their layer subtree. For the 1,111 timed-out cubes whose layer subtree is not fully
   certified, run each cube **as its own root in a fresh OUT** (as this experiment did). A restart on the old OUT would
   follow the old split record into its 51 children. The composer accepts either route.
   Expected cost: 1,111 open timed-out cubes + 2,924 never-run cubes ≈ 4,035 cubes × ≈ 350 core-s ≈ **390 core-hours**.
   Add up to about 150 core-hours if ≈ 5% still need the layer fallback (≈ 2,600 core-s each). 0 of 15 did here, so
   5% is a margin, not a measured rate. Total **≈ 400–550 core-hours**, or about 130–180 VM-hours at 3 jobs per 4-core VM.
3. **H3/one (5 roots, 320 six-bit cubes)**: neither raising the cap (0 of 5 at 1800 s) nor the layer split (21 of 44
   children time out at 600 s) works. Use a third σ level, `--sigma-levels 3 --caps 1,1,1,600,600` (512 nine-bit cubes
   per root). Size it from the pilot above before committing machines. PILOT9_COST
4. Compose again after C3W5 and these runs. Report frontier sizes from mycompose, or note compose.py's double count
   of σ-split cube nodes described in Part 1.

## Not done / notes

- C3W5 was still running at 5392150c. Only its progress `out.jsonl` (238 records) was composed.
- Row 17 of the cap list was not run (last-start time).
- The cap-experiment records (`cap/out_lane*.jsonl`) are valid C3U2 records and can be composed. They certify 15 more cubes.
