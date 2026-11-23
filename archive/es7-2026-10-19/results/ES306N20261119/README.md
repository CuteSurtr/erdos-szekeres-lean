# ES306N20261119: steps toward ES(8) ≤ 306 (19 November 2026)

> **Retention update (23 Nov 2026, owner OK):** the open-partial budget-65 campaign is abandoned. The context files
> of 37 contexts in bal186-20261119/runs (ctx-<id>-b65.json.gz and .result.json; cleanup set C37) were deleted;
> campaign/ctx-N.log and ctx-3, ctx-1291, ctx-1548 stay. Exact paths: ~/research/data/cleanup-20261123/manifest.txt.


> **Superseded for the bound (17:42): ES(8) ≤ 305, see [ES305N20261119](../ES305N20261119/README.md).** One extra
> balanced row from N66 ≤ 55 (the Z-row) shrinks the balanced trees by about 1e4. The Lean-rows-only budget-65
> campaign below was stopped at 17:19 with 40 contexts done. It would still give a 306 that does not use Lemma Z.
> The tools, the state-0 analysis, the determinism results and the disk proposal below remain valid.

**Status (16:00 KST, 19 Nov): no bound changed; ES(8) ≤ 307 stands.**
- **EXACT TREE: the budget-36 slice (18,18).** It is checked by two implementations (`fresh_replay_v4` / `check_tree`
  and `tcheck_b36` + `pycheck_b36`).
- **HEURISTIC: size estimates for all four budget-36 slices.** They show that the remaining slices (19,17), (20,16) and
  (21,15) are out of reach by trees (2e10 to 3e11 nodes).
- **HEURISTIC: calibration of the balanced-186 route.** *Correction at 16:20:* the "state 0 free" arm of 15:40 was
  not free. `fastbb256` itself fixes state 0 occupied at every root (`Mask o0; o0.set(0)`, residual convention), so both
  arms measured the same restricted problem. The real cost of the sound setting is being measured with an explicit
  state-0 branch (§6).

Labels as in es-research §2. Work directories (not in Git): W = `/home/jay/research/data/es308-20261114` (slices),
`/home/jay/research/data/bal186-20261119` (balanced route).

## 1. Statement

**(18,18) at budget 36.** There is no admissible hole vector with |H| ≤ 36 and state 0 occupied that has h(F) ≥ 18
and h(Lo) ≥ 18. The rows are the 2,650 Lean rows, then the capacity rows (F, 18) and (Lo, 18), then the 1,990 coupled
and appended rows of `b35s20-v169`. Each of those 1,990 rows is CERTIFIED (cake_lpr, re-certified fresh on 18 Nov,
VERIFY307 T4).

## 2. Model and soundness

- The model is the one of ES307N20261118 §3 and ROUTE307_1116 §1, with the budget raised from 35 to 36.
  - A slice tree with capacity rows (F, T) and (Lo, 36 − T) shows: no admissible vector with |H| ≤ 36 and state 0
    occupied has h(F) ≥ T and h(Lo) ≥ 36 − T.
  - The only branch the tree leaves pending is "state 0 missing". Lean discharges it with `zero_mem_residualOccupied`.
- **What ES(8) ≤ 306 needs on this route.** With h(F) ≥ 18 (Lean rows) and h(Lo) ≥ 15 (N66 ≤ 55, Lemma A), h(C) = 36
  leaves the four cases (18,18), (19,17), (20,16) and (21,15). All four excluded give h(C) ≥ 37, then
  |S| ≤ 1 + 187 + 117 = 305, so ES(8) ≤ 306.
  - This record excludes the first case only.
  - The other three are far out of reach (§4).

## 3. Method

- **Inputs.**
  - Folders: `W/inputs/b36s{18,19,20,21}-v{1000,2000,3000,4000}`, made by `tools/prepare_union_v2.py 36 T b36sT-vK
    b35s20-v169`.
  - `prepare_union_v2.py` is a copy of `prepare_union.py`. Only its assert line (budget 36, `-v` names allowed) and the
    docstring note differ.
  - The `-u1` folders, used by the dives, hold byte-identical rows.
  - Version numbers start at 1000 so that cut batches can never collide with the existing `cuts-v2…v701`.
- **Finder.**
  - Command: `tools/run_tree_v8.py 18 --budget=36 --input-folder=b36s18-v1000 --tag=a --threads=8 --on-witness=continue
    --max-ctx-nodes=1000000 --seconds=6900`, unit `esr-b36-s18a`, MALLOC_ARENA_MAX=2.
  - `run_tree_v8.py` is `run_tree_v7.py` with only `choices=[34,35,36]` changed.
  - Result: 3,099 of 3,099 contexts closed, 3,277,895 nodes, no witness, 576 s (finder receipt `runs/b36s18/a.json`).
- **Replay 1.**
  - Command: `audit/fresh_replay_v4.py b36s18/bb b36s18-v1000 fresh-b36s18-v1000 8`. `fresh_replay_v4.py` is
    `fresh_replay_v3.py` with only `assert BUD in (34, 35, 36)` changed.
  - The replay asserts that the capacity rows are exactly (F, 18) and (Lo, 18), and that the master is built on this row
    version. It then checks every context from scratch with `scripts/omission_tree.check_tree`.
- **Replay 2.**
  - Command: `VERIFY307/tools/final_tree_check_b36.sh runs/b36s18/bb b36s18-v1000 W/verify-b36s18-v1000 8 18 18`. It
    runs `prep_rows`, then `tcheck_b36` (C++, own leaf-rule derivation), then `pycheck_b36` (pure Python) in 8 shards,
    then `compare_py`.
  - Copies with asserted diffs:
    - `tcheck_b36.cpp` (= `tcheck_b35.cpp` with `B = 36` and its error message);
    - `pycheck_b36.py` (the constant `B = 36` and the docstring note);
    - `final_tree_check_b36.sh` (only the checker names).

## 4. Results

| item | value | label |
|---|---|---|
| (18,18) replay 1 (`check_tree`) | 3,099 contexts, 3,284,654 nodes (master 6,759), 1,640,779 leaves, minimum margin 1, pending 1 = state 0 missing | **EXACT TREE** |
| (18,18) replay 2 (`tcheck_b36` + `pycheck_b36`) | verdict "EXACT TREE (tcheck_b36 + pycheck_b36)", no problems; 3,099 contexts, 3,284,654 nodes, 1,640,778 leaves (the pending leaf is not counted), min margin 1, 4,642 rows, py nodes = tc nodes | **EXACT TREE** |
| Knuth estimate (18,18), 200 dives | 1.24e7 nodes (actual tree 3.28e6: the estimate was 3.8× high) | HEURISTIC |
| Knuth estimate (19,17) | 2.12e10 (stderr 1.2e10; one heavy dive; 4.5e9 at 50 dives) | HEURISTIC |
| Knuth estimate (20,16) | 3.09e11 (stderr 2.0e11) | HEURISTIC |
| Knuth estimate (21,15) | 2.90e11 (stderr 6.6e10) | HEURISTIC |

No dive hit a witness. For scale, the (20,15) budget-35 tree had 2.38e8 nodes and took about four days of loop time at
6-14 threads. Even with the 3.8× overestimate seen at (18,18), (19,17) is about 20 times that tree. **The budget-36
trees are not a near-term route to 306.**

## 5. Controls

- Budget swap, tcheck (W/verify-b36s18-v1000/negctrl):
  - (1) `tcheck_b35` on the b36 packet: NOT CONFIRMED (1 error, the budget);
  - (2) `tcheck_b36` on the b35 (18,17) packet with its own rows: NOT CONFIRMED (205,806 leaf errors), so the
    budget enters the leaf rule, not only the header check;
  - (3) `tcheck_b35` on the b35 (18,17) packet: EXACT TREE (positive control).
- The replays read every context file; both report the same node total.

## 6. The balanced-186 route (calibration; HEURISTIC)

- **Arithmetic.** |H| ≤ 186 together with the 307 chain (|R| ≤ 118) gives |S| ≤ 305 and so ES(8) ≤ 306: the threshold
  is 186 + 118 + 2 = 306 in `Partition.forces_of_population_bounds`.
  - |H| ≤ 186 means a balanced budget-65 tree (h(H) ≥ 66 of 252 states).
  - Its rows are the 3,131 Lean-proved balanced rows (`balanced-v2-source.json`, SHA-256 `acaf6323…`). The copy
    `bal.rows` was checked equal to it row for row.
  - So no LRAT proof is needed, which keeps the disk use small.
- **The blocking caveat of SYNTHESIS §2.1 item 4.** The 15 Nov probe (`leaf65ab.py`) added state 0 to every context's
  occupied set. The production balanced trees leave state 0 free (run_context.py: ROOT_OCC empty; no b64 node
  branches on state 0).
  - `leaf65free.py` is a copy with only that fixing made switchable.
  - Same 160 leaves (seed 20261115), arm B flags:

  | setting | s/leaf (ctx-weighted) | projected CPU-h for 7,048,218 leaves | mean nodes | rc |
  |---|---|---|---|---|
  | state 0 fixed (probe's setting, rerun) | 0.136 | 266 | 27.4 | 160 × 0 |
  | **state 0 free (sound setting)** | **0.134** | **262** | 26.7 | 160 × 0 |

  **Correction (16:20): this comparison is void.** `fastbb256` fixes state 0 occupied internally at the root of every
  solve (the reduced context file reads `"occupied": [0]`; fastbb2.cpp lines 1683, 1844, 1918 `Mask o0; o0.set(0)`),
  and its single-context master records no pending "state 0 missing" branch. Both rows above therefore measure the
  restricted problem, which explains the ratio 0.995. The sound budget-65 tree must branch on state 0 explicitly at
  every re-solved leaf: occupied → the fastbb subtree, missing → a second solve with 0 in M and budget 65 − |M| − 1.
  The stored budget-64 certificate is tried first on each side; the replay checks everything.
- A direct whole-context solve at budget 65 (`ctx65.py`) is far slower: its first context ran for minutes.
- **Grafting is exact.** The reduction keeps row and state indices, so a reduced weighted leaf has the same margin in
  the original instance. The trusted `check_tree` replay on the assembled budget-65 tree, with the original rows,
  decides anyway.

**The Lean link (checked by reading the sources, 16:25).**
- `experiments/omission-global-assembly-2026-10-10/BalancedBudgets.lean` defines `ExcludesHoleBudget b`: no 0/1
  vector on the 252 states with at most b holes meets every balanced row. State 0 is unconstrained there.
- In the same file, `balanced_bound_of_hole_budget : ExcludesHoleBudget b → Partition.BalancedBound (251 − b)`. The 310
  assembly (`Final310Compact.lean`) uses it with b = 64 to get `BalancedBound 187`.
- `Partition.forces_of_population_bounds` (`PopulationBounds.lean`) takes `BalancedBound B` and `ResidualBound R` as
  plain hypotheses.

So an EXACT TREE for budget 65, with state 0 free as here, gives `BalancedBound 186`. With the 307 chain's residual
118 it gives `ForcesConvexNGon 306 8`. The budget-65 trees are not Lean-checked (the 307 standard: two
implementations).

### 6.1 The campaign (started 15:58 KST, unit `esr-bal-campaign65`; COMPUTED until replayed)

- **First launch stopped by the memory guard (16:04, no OOM kill).** The 64 lowest-LP contexts, started first, include
  the largest trees (up to 8,481 leaves), and 12 of them reached the 12 GB `bal` track. Relaunched at 16:09 with
  memory-aware admission: the estimated memory of all running jobs is kept at or below 10 GB, at 150 MB + 0.2 MB per
  budget-64 leaf.
- **v3.1 held whole trees in memory (about 0.33 MB per budget-64 leaf, so up to about 3 GB for the largest
  contexts).** The campaign was stopped cleanly at 16:16 before reaching the guard.
- **v4 driver (`graft65.py` SHA-256 `ffd41eae…`), campaign relaunched 16:19 with 12 workers (≈ 2.2 GB in all).**
  - Decomposed replay. `check_tree` runs on every grafted subtree, under an envelope of exactly its attachment-point
    literals. The skeleton (path envelope, state-0 branch, copied budget-64 trees with kept leaves, attachment points
    pending) is checked once.
  - Each subtree is serialized to text at once. Peak memory is 61-86 MB on 290-342-leaf contexts.
  - The v3.1 fallback bug (a reserved slot left empty) is fixed.
- **Cross-checks of v4.**
  - Context 2464: content SHA-256 equal to v3.1's (`28a39c77…`), so the numbering and every node are identical.
  - Context 3 with the fallback forced (`--cap0 1`): closed, replay ok.
  - Both files also pass an undecomposed whole-tree `check_tree` replay (`wholecheck.py`: pending 12 = path length;
    4,780 and 3,798 leaves; minimum margin 1).
  - `balcheck` subset mode accepts both, with identical counts, and the three v3.1 campaign contexts (3, 1291, 1548).
  - At B = 66, with the header check off, both are rejected ("leaf margin < 1").
- **v4.1 (16:40, `graft65.py` SHA-256 `6eb208b5…`).** The file and its content hash are streamed node by node.
  v4's final join briefly held about three copies of the tree text (about 1 GB at the end of a 5,000-leaf context).
  Context 2464 still gives `28a39c77…`, and the hash recomputed from the file agrees. Contexts started before 16:40
  ran v4, with the same bytes.
- **Finisher unit `esr-bal-finish65` (`finish65.sh`, SHA-256 `134dfa3a…`).** It waits for the campaign, then:
  - checks all 4,096 result files (closed, replay ok, margin ≥ 1, no witness);
  - writes `final/content_sha256.tsv`;
  - runs `balcheck` on all 4,096 files with the cover check;
  - writes `final/VERDICT.json`.
- **First large contexts under v4 (16:36):** 4029 (4,993 leaves, 902 s), 983 (4,918, 916 s) and 4087 (5,555, 999 s):
  all closed, replay ok, minimum margin 1; about 0.18 s per budget-64 leaf.
- **Lean composition (compiled 16:25).** `Composition306.lean` in this record: `composition_306 : BalancedBound 186 →
  ResidualBound 118 → ForcesConvexNGon 306 8` and `avoiding_305`. `lake env lean` gives rc 0; axioms only propext,
  Classical.choice and Quot.sound.
- **Disk.** See `DISK_POLICY_PROPOSAL.md`: proofs and trees are reproducible bit for bit, so storage can be replaced
  by regeneration. This is for the owner's decision; nothing has been deleted.
- **Determinism (16:15).** Context 2464 was run three times. The decompressed tree JSON was identical each time
  (SHA-256 `28a39c77…`); only gzip's header time differed. From v3.1 (16:20) the driver writes gzip with mtime 0 and
  records `tree_content_sha256` and `driver_sha256`. Contexts started before 16:20 have only the file hash, and their
  content hash can be recomputed. So every context tree can be regenerated bit for bit.

- **Driver.** `bal186-20261119/graft65.py` v3 (SHA-256 `4652ebd3…`) does one context:
  - the root is a branch on state 0;
  - the zero child (0 occupied) is the budget-64 tree, with every leaf that no longer closes re-solved by fastbb256;
  - the one child (0 missing) is one direct fastbb256 solve (cap 300k nodes, 300 s), falling back to leaf-wise if it
    is capped;
  - then `check_tree` replays the whole context at budget 65 with the path envelope of run_context.py.
- **Campaign.** `campaign65.py` (SHA-256 `493ae65a…`) runs 12 workers.
  - The 64 lowest-LP contexts run first; the rest follow in a fixed random order (seed 20261119).
  - New jobs stop at the cutoff (40 h); the unit stops at 48 h.
- **Pilot, five contexts.**
  - Contexts 0, 2464, 1000 and 3000: closed, replay ok, minimum margin 1. They took 0.165-0.182 s per budget-64
    leaf, and the trees took 3.6-29.6 MB (about 11.8 KB per budget-64 leaf).
  - Context 4095 was stopped unfinished.
  - **Projection (HEURISTIC): about 350 CPU-h, about 29 h on 12 workers, and about 84 GB of gzip trees.**
- **Second checker `balcheck.cpp`** (own C++, SHA-256 `846051ff…`; leaf rule derived from the inequality in its
  header; exact `__int128`). It also checks that the 4,096 context paths are the leaves of one complete binary decision
  tree. Controls on the budget-64 trees behind 310:
  - B = 64: EXACT TREE (balcheck), 4,096 contexts, 14,092,340 nodes, 7,048,218 leaves (= the campaign's leaf
    total), minimum margin 1, cover complete (41 s, 3 threads);
  - B = 65 with the header check switched off (control-only environment switch): all 4,096 files fail with
    "leaf margin < 1";
  - only 4,095 contexts: "incomplete cover".

## 7. Files and hashes

| file | SHA-256 |
|---|---|
| `W/inputs/b36s18-v1000/rows.txt` | `7e7da700189e6639ef32af774bfc3777660594baa299fc7859515c5d50fe6a0a` |
| `W/inputs/b36s18-v1000/extra.json` | `e68d01287241d0c4cc8e7b33724acee71f6f4ca6a3dd6c48f11c0ded92b50b14` |
| `W/inputs/b35s20-v169/extra.json` (row source) | `de4bcceba6d0c80ce6f63cbef15822cac8300780607c738569999a7d94b81916` |
| `W/inputs/source-2650.json.gz` | `8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa` |
| `W/runs/b36s18/bb/master.json` | `558b0bfba91310027de1aa374a3091de3bc0637b92e43c081033216ca523a5ba` |
| `W/bin/fastbb2` (finder) | `39b724a2b5f5b08b56f3e9aedb24886c08ae2716301008410aaba9a1452b33b5` |
| `tcheck_b36` binary (g++ 15.2.0) | `c0747dcffdaaf3b41f593d45a1becdf245c620bd9d8e498cf09fc470f3e97c31` |
| `LO33N…/budget34/tools/prepare_union_v2.py` | `8ff925524614f69a796c0620b48da47817516248c42f74a4d905f95d0a6cd06a` |
| `LO33N…/budget34/tools/run_tree_v8.py` | `42ec0e152490fcba41c32a89eaf7a8d0cb54fed3963902dda166945a03f567c8` |
| `LO33N…/budget34/audit/fresh_replay_v4.py` | `9b17123d1787a116aacd6f64790346cbf9ab31da6cb7e08dd1fc915e58daab29` |
| `LO33N…/budget34/VERIFY307/tools/tcheck_b36.cpp` | `8845a12a926dd659e8f0efba34ff5c1bc5da0c533c6c3c5eba8579b707db1704` |
| `LO33N…/budget34/VERIFY307/tools/pycheck_b36.py` | `0a2d86c8c3cc4de69106d9c14751425063a21f8fc8db96b98e4088e9f096ef8d` |
| `LO33N…/budget34/VERIFY307/tools/final_tree_check_b36.sh` | `5c2db1581e8fe49cf477c3451ecc2840518461ee98f2e07940c3e0c68bfdca97` |
| `bal186-20261119/fastbb256` | `df17fa7471f27ab80afe34363d4945b324ac1e007e27e1f8dbadd2d342c4cc90` |
| `bal186-20261119/bal.rows` | `927081bcb8206cf13a77eadbda0c6aec52b85497db108a83627a83086447764d` |

The (18,18) packet uses 558 MB (3,103 files). The replay summaries are in
`LO33N…/budget34/audit/fresh-b36s18-v1000/` and `W/verify-b36s18-v1000/`. The dives are in `W/probe36/`.

## 7.1 Beyond 306: the cost of a balanced budget-66 step (HEURISTIC probe, 16:50)

- **Growth.** The budget-64 → budget-65 leaf multiplier is 16.76 on the first 14 closed contexts. The finished
  budget-65 trees will therefore hold about 1.18e8 leaves.
- **Probe.** `bal186-20261119/probe66/probe66.py` re-solved 90 sampled budget-65 leaves (contexts 3, 1548, 1291;
  state 0 already fixed on every leaf) at budget 66.
  - None closed by its stored certificate; all 90 solves rc 0.
  - 0.130 s per leaf (median 0.126), 22.6 subtree nodes per leaf.
- **Projection.** About **4,300 CPU-h**, roughly 12 × the budget-65 campaign or about 15 days at 12 threads. The
  trees would hold about 2.7e9 nodes, well over 1 TB of gzip, unless they are checked on the fly and regenerated
  instead of stored.
- So |H| ≤ 185 (and with it ES(8) ≤ 305 on this route) is not a near-term computation. ES(8) ≤ 305 needs a new idea:
  stronger rows, or a different split, not more budget steps.

## 8. What remains

- The other three budget-36 slices: not feasible by trees (§4).
- The balanced-186 campaign, about 260-280 CPU-h before tails (§6). It needs:
  - a grafting driver;
  - a trusted per-context replay at budget 65;
  - an independent second checker for 252-state trees;
  - the owner's OK for a multi-day run.

## 9. Resume

```bash
W=/home/jay/research/data/es308-20261114; B=<repo>/archive/es7-2026-10-19/results/LO33N20261113/budget34
$B/VERIFY307/tools/final_tree_check_b36.sh $W/runs/b36s18/bb b36s18-v1000 <outdir> 8 18 18
cd $B/audit && <venv python> fresh_replay_v4.py b36s18/bb b36s18-v1000 <outname> 8
```
