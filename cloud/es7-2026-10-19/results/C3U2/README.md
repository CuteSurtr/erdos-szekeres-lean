# C3U2: σ-cube composer fix (C3AUDIT3 finding 1) and the official open-root list

Task `results/C3U2/TASK.md` at 3fd8a4d8, H = 2.0. Run 2026-10-24 from 11:31 UTC on one cloud VM (4 cores, 15 GB,
no swap; `env.txt`), from branch head 3fd8a4d8. Tools built here: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8),
lrat-check (drat-trim 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`). Sanity check: on {1},{−1}, LRAT `3 0 0` is
rejected by both checkers and `3 0 1 2 0` is accepted by both. The m = 11 base, `gen_case.py 11 7 none`, has header
`p cnf 168399 4154921` and sha256 `bf0e502e…dd6da`, as required.

**Future waves and the final composition should use `results/C3U2/tools` at commit cad4e050**, the last commit that
changes `tools/`. Commit c546c2c0 is the unmodified copy of `results/C3U/tools` at 95cafa93.
`git diff c546c2c0 cad4e050 -- results/C3U2/tools` shows every change: 2 files, +42 / −8. `hullcase.py` and every other
tool are unchanged.

## Changes (line numbers in `results/C3U2/tools` at cad4e050)

| file:line | change |
|---|---|
| `compose.py:248-250` | **Finding 1.** The plain branch of `covered2` now computes `ch = children(layers)`. If `ch` is empty, it adds the node to the frontier and returns not covered, even when the node is in `prefixes`. A plain node without children is therefore covered only if it is certified (line 221). At 95cafa93 the loop `ok = True; for c in children(layers): …` stayed True for a fully layered node in `prefixes`. C3U puts L itself into `prefixes` for every certified cube `L__C`, so that node counted as covered. |
| `compose.py:226-229` | Same pattern, σ-split route. A σ-split is used only if `sigma_children` returns exactly 2^K > 0 children (`res` starts False otherwise). The bits are checked earlier, so this cannot fail on valid input today, but no route can now succeed through an empty loop. |
| `compose.py:169-170` | Same pattern, implied σ-split from `sigma_cubes.py` records. It needs K > 0 and a non-empty set of exactly 2^K expected cubes, all certified. |
| `compose.py:236` | Cube branch, unchanged: C3U already refused a cube node without layer children (`not ch`). |
| `compose.py:41-48` | Docstring: the C3U2 changes. The unused helper `covered` (lines 189-199) already refuses a node without children (`if not ch`) and is unchanged. |
| `close_tree.py:121-126` | **Finding 3.** On restart, a record with a `cube` field (`sigma_cubes.py` format: `node` = parent N) marks N__C as done, with C sorted by residue as `compose.py` reads it, and never N. Such records are not read as split records. |
| `close_tree.py:210-214` | **Finding 2.** A timed-out node without layer children, and with no σ-split possible, gets no `{"split": true, "children": 0}` record. It goes on the `unsplittable` list (one stdout line `{"node", "unsplittable": true}`) and stays open. |
| `close_tree.py:218-219` | The final line is `{"root", "open_frontier": frontier + unsplittable, "unsplittable": n, "unsplittable_nodes": [...]}`. |
| `close_tree.py:156-159` | Restart on an old OUT file: a split record whose children list is empty (the 0-children records that C3U and C3T wrote) splits nothing, so the node is open again and gets re-solved. |
| `close_tree.py:28-33` | Docstring: the C3U2 changes. |

I checked every other coverage path in `compose.py`. Certified is a base case. A σ-split now needs 2^K > 0 children.
The cube layer split needs a layer split record and ≥ 1 child. The plain layer split now needs ≥ 1 child. Root:
`children([])` is never empty. Each accepted split is one of C3U's two complete covers, and a node with no children
needs its own certificate.

`C3U_README.md` and `sigma_split.md` are copies of `results/C3U/README.md` and `results/C3U/sigma_split.md` (f710546d).
I corrected the statements that finding 1 shows to be false (marked "C3U2 correction"). These are the plain-node rule,
which C3U called "the C3T rule unchanged" (`C3U_README.md` "Choices", `sigma_split.md` "What compose.py checks"), the
claim that `compose.py` "does not count such a node as covered", and the recommended commit. `sigma_split.md` also
carries C3U2 line numbers now. I kept C3U's README under a different name because this file is C3U2's report.

## Tests (scripts in `tests/`, outputs in `tests/logs/`)

### 1. C3AUDIT3's tests: old (`results/C3U/tools`, 95cafa93) and new (`results/C3U2/tools`) `compose.py`

`tests/c3audit3_tests.sh` → `logs/c3audit3_tests.txt`. `tests/frontier_cmp.py` → `logs/natural_frontier.txt`.
`frontier_cmp.py` imports a `compose.py` and C3AUDIT3's fixed `mycompose.py` unchanged and replaces each module's
`json` with a shim that captures the full frontier list and the memo when the summary is printed. It then compares
the summaries, the full frontier sets and the status of every depth-2 root.

| input (m = 5 / 6 / 7, k = 6, real proofs, sha checks on) | old compose 95cafa93 | **new compose (C3U2)** | mycompose (C3AUDIT3, fixed) |
|---|---|---|---|
| `forge.py` on t1 (m = 7, K = 2), t2 (m = 7, K = 3), t3 (m = 6, K = 2): 18 forged cases each | 18/18 pass (×3) | **18/18 pass (×3)** | 18/18 (part of each case) |
| `childless_real_m5k6.jsonl` | **covered: true** (wrong) | **not covered**, frontier 1: `0s0_1s0-2s0_3_4` | not covered, frontier 1: `0s0_1s0-2s0_3_4` |
| natural A | not covered, frontier 52 | not covered, frontier 52 | not covered, 52; sets equal |
| **natural A + C** | not covered, frontier **31**; the 5 fully layered nodes **covered** (wrong) | not covered, frontier **52**, **frontier set equal to mycompose's**; **the 5 nodes not covered** | not covered, 52; the 5 nodes not covered |
| natural A + B + C | not covered, 31 | not covered, 31; sets equal | 31 |

The 5 nodes are `0s0_2_1_3s0-4s1`, `0s0_2_1s1-4s0_3`, `0s0_2_3_1s1-4s0`, `0s0_2_3s0-4s1_1` and `0s0_2_3s1-4s1_1`
(from `logs/natural/README.txt`). On A + C the old compose's memo has all 5 True, and the new one and mycompose have all
5 False. On A + B + C none of them is visited: `0s0_2` is covered through its σ-split before the plain route is tried.
`forge.py` has no childless case, so the old compose passes it too. The old compose fails on exactly the two
finding-1 inputs, the childless file and natural A + C, and the new one passes both.

### 2. `close_tree.py` findings 2 and 3 (`tests/close_tree_tests.sh` → `logs/close_tree_tests.txt`)
- **Finding 2.** I re-ran C3AUDIT3's run A with the new `close_tree` (m = 5, k = 6, root `0s0`, `--caps 600 --cadopts=-c,1`,
  no σ-split). It wrote 0 split records with 0 children, where C3U's run A wrote 52. The last line reads
  `open_frontier: 52, unsplittable: 52`, and `unsplittable_nodes` is exactly the set of C3U's 52 zero-children nodes.
  The other 173 records equal C3U's run A apart from timings.
- **Finding 2, restart on an old OUT** (C3U's run A file, `--hours 0`): the old `close_tree` prints `open_frontier: 0`,
  the new one prints 52.
- **Finding 3.** OUT holds one certified `sigma_cubes.py` record `{node: 0s0_1, cube: {2: 0}}`, run with `--hours 0`. For
  ROOT `0s0_1` the old tool prints `open_frontier: 0` (wrong) and the new one prints 1. For ROOT `0s0_1__2s0` the old
  tool prints 1 and the new one prints 0 (correct).

### 3. C3U's tests with the C3U2 tools
These are C3U's scripts, copied to `tests/` with only the tool paths changed: `run_small.sh` (`NEW`, `SN`; the σ runs
are also split into two lanes, `sigA` / `sigB`), `restart_test.sh` (`T`), `small.py`, `check_small.py`,
`compose_reject.py` and `compare_small.py`. The CaDiCaL `-c` conflict limits keep every run deterministic. I ran
`run_small.sh cmp`, `sigA` and `sigB` in parallel. The checks ran through `tests/post_small.sh` on a copy of `tests/`
outside the repository (logs written to /opt/work, then copied into `logs/`).

- **Old against new without σ-splits** (`logs/compare_small.txt`). C3T `close_tree`, C3U2 `close_tree` with defaults, and
  C3U2 with `--sigma-split 0`: m = 6 c300, m = 7 c3000, m = 7 c300 and m = 8 c3000 give 130 / 38 / 205 / 51 records.
  They are identical apart from timings, `proof_sha256` included. **FAILURES 0.**
- **σ-split trees** (`logs/check_small.txt`). All 6 runs closed with `open_frontier 0` and `unsplittable 0`. The C3U2
  `compose.py` reports covered, and the brute force finds 0 holes. The numbers are C3U's:

  | run (m, k, `-c`, K) | σ-splits | nested | max \|C\| | cube layer splits | rule-3 dropped | certified / cubes | covered, σ used | holes |
  |---|---|---|---|---|---|---|---|---|
  | 6, 6, 300, 2 | 8 | 5 | 4 | 1 | 18 | 58 / 36 | yes, 8 | 0 |
  | 7, 6, 300, 2 | 6 | 3 | 4 | 4 | 104 | 126 / 93 | yes, 6 | 0 |
  | 7, 6, 300, 3 | 3 | 0 | 3 | 7 | 147 | 218 / 185 | yes, 3 | 0 |
  | 7, 6, 100, 2 | 15 | 12 | 4 | 69 | 1,554 | 1,104 / 1,071 | yes, 15 | 0 |
  | 8, 6, 300, 2 | 12 | 8 | 4 | 14 | 468 | 506 / 461 | yes, 12 | 0 |
  | 8, 6, 300, 3 | 17 | 13 | 6 | 4 | 180 | 248 / 203 | yes, 17 | 0 |

- **Same records as C3U** (`logs/same_as_C3U.txt`, `tests/same_records.py`). Every one of the 18 record files (6 `sig_*`
  and 12 `cmp_*`) equals C3U's committed file in `results/C3U/tests/logs/small/` as a multiset of records, apart from
  timings and `base_sha256`. That covers cnf_sha256, proof_sha256, the split records and σ bits. **18/18.** No small run
  had a childless timeout, so the `close_tree` change does not show here.
- **compose.py rejections** (`logs/compose_reject.txt`, m = 6 K = 2, m = 7 K = 3, m = 8 K = 3). The unchanged input is
  covered with 0 holes. A missing cube gives not covered (66 / 864 / 3,690 holes). A wrong cube `cnf_sha256`, reversed
  `sigma_bits`, non-smallest bits and a σ-split at depth 1 each give rc 1. A non-conflicting rule-3 child dropped gives
  not covered (3 / 22 / 66 holes). **FAILURES 0** in all three, the same as C3U.
- **Restart** (`logs/restart_test.txt`). The m = 6 K = 2 run was cut after 40 of its 78 lines and re-run. It gives 78
  records, equal to the uninterrupted run, compose covered, 0 holes.
- Records of all small runs are in `tests/logs/small/` (JSON only). Some lines of `logs/run_small_*.txt` were rebuilt:
  the runner's stdout files sat in the repository, and a `git pull --rebase --autostash` replaced them while the runs
  were writing. I recovered the text from the still-open descriptors. For the last run of each lane
  (`cmp_m8k6c3000_new0`, `sig_m8k6c300K3`, `sig_m8k6c300K2`) the final line was gone, and I rebuilt it from that run's
  own `.log` (rc is not known). Their record files are complete and pass every check above.

## Official composition (step 3)

Records at **3fd8a4d8**, the head I started from, snapshotted with `git archive`. There are 127 files, listed in
`compose_m11/files.txt`: 28 C3WAVE1 (24 `out.jsonl`, 4 recheck files), 46 C3WAVE2 (45 + `K36/recheck.jsonl`), 4 C3S0,
37 C3W3, 4 C3W3S (`S0`, `S4`: `out_direct.jsonl`, `out_sigma.jsonl`), 4 C3SIG and 4 C3SIG2. No C3W3 or C3W3S recheck
files and no C3S0 recheck files exist. **`results/C3W4` had no record files at 3fd8a4d8**, only its TASK and lists.
Base `/opt/work/base.cnf` as above. All sha checks were on. Commands are in `compose_m11/run.sh` and outputs in
`compose_m11/` (`*_stdout.txt`, `*.json`, `*_roots.tsv`).

| | C3U2 compose | mycompose (fixed) | old C3U compose (95cafa93) |
|---|---|---|---|
| certified records / nodes / cube nodes | 90,447 / 90,441 / 532 | 90,447 / 90,441 / 532 | 90,447 / 90,441 / 532 |
| cnf_sha256 re-derived and equal | 90,447 | 90,447 | 90,447 |
| records with `proof_sha256` | 0 (no wave record carries one) | – | 0 |
| **no mirror**: covered / frontier / σ-splits used | not covered / **11,025** / 36 | not covered / 11,025 / 36 | not covered / 11,025 / 36 |
| no mirror: depth-2 roots / open | 1,630 / **750** | 1,630 / 750 | 1,630 / 750 |
| no mirror: full frontier set and per-root frontier sizes | equal to mycompose | – | equal |
| **`--mirror-h6`**: covered / frontier / σ-splits used | not covered / **8,765** / 31 | (no H6 mirror; read on the same 910 roots) | not covered / 8,765 / 31 |
| `--mirror-h6`: depth-2 roots / open | **910 / 313** | 910 / 313, 0 status differences, 0 frontier-size differences | 910 / 313 |

- On every root the C3U2 and mycompose answers agree: the same status and the same frontier size, 0 differences in
  both runs.
- mycompose has no `--mirror-h6`, so in the reduced cut I compared it root by root on the 910 kept roots.
- The H6 mirror only changes which depth-2 roots exist. On the 910 kept roots, (status, frontier size) is identical
  between the `--mirror-h6` and the no-mirror runs (`logs/mirror_vs_nomirror_roots.txt`).
- The old compose gives the same answers as the new one on all of today's m = 11 records. Its root tables are
  byte-identical. Finding 1 stays latent at m = 11, as C3AUDIT3 said: no record is fully layered yet.

`open_roots.tsv` lists the 910 roots of the reduced cut (`--mirror-h6`) with their stratum (`top/l2type` as in
`results/C3PLAN/scripts/stats.py`, cross-checked against every row of the C3W4 lists: 0 mismatches), status (closed /
open) and, for open roots, the frontier size. It was made by `tests/make_open_roots.py`, which refuses to write if
compose and mycompose disagree on any root. **313 open, 597 closed, frontier 8,765.**

| stratum | roots | open | closed | open frontier |
|---|---|---|---|---|
| H3/one | 5 | 5 | 0 | 5 |
| H3/two | 95 | 95 | 0 | 2789 |
| H6(1,0)/one | 5 | 0 | 5 | 0 |
| H6(1,0)/two | 76 | 0 | 76 | 0 |
| H6(1,1)/one | 5 | 4 | 1 | 1146 |
| H6(1,1)/two | 76 | 0 | 76 | 0 |
| H6(2,0)/one | 5 | 1 | 4 | 35 |
| H6(2,0)/two | 76 | 7 | 69 | 7 |
| H6(2,1)/one | 5 | 5 | 0 | 264 |
| H6(2,1)/two | 76 | 0 | 76 | 0 |
| H6(3,0)/one | 5 | 3 | 2 | 98 |
| H6(3,0)/two | 76 | 0 | 76 | 0 |
| H6(3,1)/one | 5 | 5 | 0 | 243 |
| H6(3,1)/two | 76 | 21 | 55 | 705 |
| H6(4,0)/one | 5 | 5 | 0 | 105 |
| H6(4,0)/two | 76 | 10 | 66 | 616 |
| H6(4,1)/one | 5 | 5 | 0 | 357 |
| H6(4,1)/two | 76 | 43 | 33 | 315 |
| H6(5,0)/one | 5 | 5 | 0 | 5 |
| H6(5,0)/two | 76 | 39 | 37 | 1896 |
| H6(5,1)/one | 5 | 5 | 0 | 124 |
| H6(5,1)/two | 76 | 55 | 21 | 55 |
| **total** | **910** | **313** | **597** | **8,765** |

## Not done / limits
- I did not re-run C3U's m = 11 `close_tree` test (C3U test 4, 2 × 8 cubes, about 40 minutes with checks). The only
  `close_tree.py` changes are in restart reading and in childless timeouts, and neither can occur in that test.
- I did not re-run C3AUDIT3's brute force (`mybrute.py`). The frontier comparison with its fixed `mycompose.py` was
  enough for the task's checks, and C3AUDIT3's brute-force counts on the natural inputs stand (A + C: 36 holes, all
  inside the 52-node frontier that the new compose reports, since the 5 wrongly covered nodes are now open).
- `--mirror-h6` was used as the task asks. It still rests on Lemma H6M (C3AUDIT2). mycompose has no H6 mirror, so the
  reduced-cut comparison is root by root, on the 910 roots.
- No wave record carries `proof_sha256` (they predate C3T), so `certified_with_proof_sha256` is 0.
- The official composition covers the records at 3fd8a4d8. C3W4 records pushed after that commit are not in it.
- `close_node.py`, `hullcase.py` and the other tools are unchanged. The checker memory note (C3AUDIT3 finding 4) still
  applies: keep `--jobs` ≤ 3 for m = 11 cube proofs.
