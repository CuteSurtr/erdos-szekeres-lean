# VERIFY_G: independent check of FASTBB20261113 (interim record of 19:15 KST)

Verifier G, phase 2, Friday 13 November 2026, 20:20 to 20:45 KST. My job was to try to refute the
record. I read the README line by line first. Scratch directory (not in Git):
`/home/jay/research/data/verify-G-20261113` (scripts in `scripts/`, logs next to them). I used one thread per
systemd unit (`nov13c-vfy-G-*`) and at most 1.4 GB MemoryMax. I made no git changes. The only file I wrote in
the repository is this one.

**Overall: confirmed, with corrections.** Each numbered phase-1 claim was recomputed and holds exactly as
stated. The corrections concern labels and documentation, not mathematics (section 4).

## 1. Verdict per claim

| # | claim (README, 19:15) | verdict | evidence (section 2) |
|---|---|---|---|
| 1 | fastbb builds from the recorded source; the capacity-58 tree (V1) has 28,735 nodes and replays through `assemble.py` -> `check_tree` with 14,368 leaves, 1 pending (state 0 missing), minimum margin 1 | **CONFIRMED** (EXACT TREE, conditional on the rows) | 2.1, 2.2 |
| 2 | the capacity-59 tree (V2) has 407,101 nodes; 203,551 leaves, 1 pending, minimum margin 1 | **CONFIRMED** (EXACT TREE, conditional on the rows). I also replayed it with the unchanged `assemble.py`, one context per call, not only with the record's `replay_split.py` | 2.1, 2.3 |
| 3 | extra-row files: `capx_c58_i1.json` / `capx_c59_i2.json` hold the capacity row plus cake_lpr-certified coupled rows | **CONFIRMED** (hashes match RES33N20261113; content checked row by row; coupled rows re-certified, see 2.4) | 2.4 |
| 4 | capacity-60 WITNESS (context 17): 33 holes, all 3,221 rows satisfied, state 0 occupied, 60 of 84 F-states occupied | **CONFIRMED** (my own exact check) | 2.5 |
| 5 | it violates exactly 2 pooled transported 9-state rows; both CERTIFIED (CaDiCaL LRAT + cake_lpr) and appended (`capx_c60_i23.json`, 573 rows) | **CONFIRMED** (CNFs regenerated with the committed RES33N encoder; hashes match; cake_lpr `s VERIFIED UNSAT` re-obtained) | 2.6 |
| 6 | so the 570 certified rows of iteration 22 do not close capacity 60; the morning run had not reached this region | **CONFIRMED** | 2.5 |
| 7 | V3 stopped after 17 closed contexts, 478,891 nodes, 367 s; the 17 contexts were kept on resume | **CONFIRMED** from the log and file times (statistics only, not a mathematical claim) | 2.7 |
| 8 | V5: 24 of 24 contexts closed by Python, 1,100 vs 866 nodes, 39.9 vs 0.67 s | consistent with `logs/v5_crosscheck_final.json`; **not re-run** (outside the claims I was asked to check) | – |

The trees are conditional: they prove "2,650 Lean rows + the certified coupled rows + h(F) >= 84 - c
=> at least 34 holes, given state 0 occupied". The capacity row is the unproved hypothesis N(cap <= 4) <= c
(only N5 <= 65 is certified). The README correctly says **no new bound is claimed**.

## 2. Checks run (commands and outputs)

### 2.1 Rebuild and 1-thread rerun (unit `nov13c-vfy-G-rerun`, `scripts/driver1.sh`)
- I took a snapshot of `tools/` at 20:22 (`src_snapshot.sha256`). `fastbb.cpp` SHA-256 = `4713bd5a…6afa`, the
  same as `logs/final_build.sha256` of the phase-1 work directory. The record's tools were unchanged at 20:31.
- `g++ -std=c++20 -O3 -march=native -fopenmp-simd -pthread -Wall -Wextra -Wno-unused-parameter -o build/fastbb fastbb.cpp -lz`
  -> binary SHA-256 `0430b365…0360441`, **identical** to the phase-1 `bin/fastbb`.
- I wrote the row files myself (`scripts/mkrows.py`, own code). The rows come from my copies of
  `source-2650.json.gz` (SHA-256 `8c7fe9ef…41aa`, identical to `git show HEAD:`) and of the RES33N extra-row
  files. The bodies are byte-identical to phase-1 `in/c58_i1.rows` / `in/c59_i2.rows` (3,148 and 3,164 rows).
- `fastbb solve in/c58.rows 33 1 32 runs/v1_c58`: 51 contexts, 28,663 context nodes, 24.1 s + 4.7 s master,
  45 MB RSS. All 51 `ctx-*.json.gz` are **byte-identical** to the phase-1 V1 files, and the master node lists
  are equal.
- `fastbb solve in/c59.rows 33 1 32 runs/v2_c59`: 32 contexts, 407,068 context nodes, 293.1 s, 61 MB RSS.
  All 32 ctx files are **byte-identical** to the phase-1 V2 files (which the 18:43 build had produced), and the
  master node lists are equal.

### 2.2 V1 replay
- Unchanged repository tool, run from the repo root:
  `python -B experiments/omission-final313-2026-10-11/search/assemble.py <run> <tree> <extra>` on my rerun and
  on the phase-1 directory. Both give
  `{"contexts_closed": 51, "contexts_total": 51, "nodes": 28735, "replay": {"nodes": 28735, "leaves": 14368, "pending": 1, "complete": false, "minimum_margin": 1}}`.
- The assembled tree has root = branch on vertex 0. Its `one` child (state 0 missing) is the **only** pending node
  in the file, and `hole_budget` = 33. Apart from the gzip header, its node list equals the phase-1
  `runs/v1_c58_tree.json.gz`.
- An independent checker (`scripts/indep_check.py`, own code; it does not import `omission_tree.py`) takes the
  rows from the command line, not from master.json. It also checks that every context file states the master
  path. It prints `{"leaves_weighted": 14367, "nodes": 28735, "min_margin": 1, "contexts": 51, "pending": 1, "leaves": 14368, "rows": 3148}`.

### 2.3 V2 replay (the full assemble needed 2 GB and was stopped by memguard in phase 1)
- **Unchanged `assemble.py`, piecewise** (`scripts/piecewise_assemble.sh`, unit `nov13c-vfy-G-v2replay`). Each
  of 32 calls gets a temporary directory with the phase-1 `master.json` and exactly one ctx file. Every call
  replays the full assembled tree with the other 31 contexts pending: `contexts_closed` 1 and `pending` 32 in
  every call, no exception. Summed: **407,101 nodes, 203,551 leaves, 1 pending, minimum margin 1**, largest
  context 64,701 nodes. Peak 373 MB, 17 s.
- Independent checker on the phase-1 directory:
  `{"leaves_weighted": 203550, "nodes": 407101, "min_margin": 1, "contexts": 32, "pending": 1, "leaves": 203551, "rows": 3164}` (333 MB, 9.6 s).
- master.json: source = the repo's `source-2650.json.gz`, extra = `/home/jay/research/data/fastbb-20261113/in/capx_c59_i2.json`
  (SHA-256 `e506e1bf…4552`), budget 33. Master SHA-256: V1 `70efcf24…22fe`, V2 `7d800a0e…f3c3`.

### 2.4 Extra-row files (`scripts/rows_witness_check.py`, `scripts/recert.py`)
- SHA-256: `capx_c58_i1.json` `25b9fa73d476fdb7…` and `capx_c59_i2.json` `e506e1bfc7ee68c6…` equal the
  prefixes stated in RES33N20261113 and the files in `/home/jay/research/data/res33-20261113/cert_c58|cert_c59/`.
  `capx_c60_i22.json` `ad8b7363ca449505…` equals the RES33N statement.
- F = {states with component 0 (f1) >= 5}: 84 states (56 with f1 = 5, 28 with f1 = 6, 70 with f1 <= 4, as
  in THEORY310N).
- c58: 498 rows = 1 capacity row (support exactly F, rhs 26 = 84 - 58) + 497 rows of rhs 1. c59: 514 = 1
  (rhs 25) + 513. c60_i22: 571 = 1 (rhs 24) + 570. No other row has rhs > 1, there are no duplicates, and the
  supports have 9, 13 or 14 states. Coupled sets are nested: c58 ⊂ c59 ⊂ c60_i22.
- Each coupled support has a `s VERIFIED UNSAT` entry in `res33-20261113/certified.jsonl` (570 such entries).
- **Re-certification:** I regenerated the CNFs with the committed RES33N encoder
  (`results/RES33N20261113/tools/coupled.py`, `CNF(S).dimacs()`, as `certify.py` does) and compared their hash
  with the recorded `cnf_sha256`. I then ran CaDiCaL 2.1.3 `--lrat=true --binary=false` and
  `cake_lpr --CML_HEAP_SIZE=400`.
  - **All 570** coupled supports of `capx_c60_i22.json` were done (unit `nov13c-vfy-G-all570`, 1 thread,
    671 s, LRAT at most 5.1 MB). Since c58 ⊂ c59 ⊂ c60_i22, they include every coupled row that V1 and V2 use.
  - Result: 570/570 CNF hashes equal the recorded ones, 570/570 CaDiCaL UNSAT, **570/570 cake_lpr
    `s VERIFIED UNSAT`** (`kill/all570_recert.jsonl`, SHA-256 `0e0bf7b6…6281`).
  - So every coupled row is CERTIFIED for its stated CNF. This was re-obtained today, not just read from the
    log.

### 2.5 The capacity-60 witness
- holes = the 33 listed in the README, the same as `logs/witness_c60_7.json` and
  `runs/v3_c60/WITNESS.refuted-1.json` (context 17).
- I checked them by direct set intersection against 2,650 + 571 = **3,221 rows**. Results: 33 distinct holes,
  0 not a hole, **0 rows violated**, 521 rows tight, 24 holes in F, **60 F-states occupied**. So the capacity
  row h(F) >= 24 is met with equality.
- Of the current 607-row `capx_c60_i23.json`, it violates exactly extra positions 571 and 572, the two kill rows.
- Of the 109,907 pooled transported rows (`killtools/newrows.json` + `fnewrows.json`), exactly 2 are fully
  occupied, both with 9 states, as stated.
- The witness falls in context 70 of the morning pbb_strong master (`res33-20261113/capbb_c60_i22`), which has
  no ctx file. So the morning run had not closed this region, as stated.

### 2.6 The two kill rows (unit `nov13c-vfy-G-kill`)
- [52, 67, 79, 82, 93, 103, 117, 123, 124]: regenerated CNF SHA-256 `afb621ce…4da7` = recorded (killtools
  `certified.jsonl` line 582). CaDiCaL exit 20, LRAT SHA-256 `93c2c4a1…0824` = recorded. **cake_lpr: `s VERIFIED UNSAT`**.
- [67, 77, 79, 96, 105, 114, 117, 123, 124]: CNF `9740e4fd…5e` = recorded (line 583), LRAT `23180300…f258`
  = recorded. **cake_lpr: `s VERIFIED UNSAT`**.
- The private `killtools/coupled.py` differs from the RES33N copy only in three hard-coded work-directory
  paths. `killtools/static/` is identical to `res33-20261113/static/`, and certify.py, common.py,
  transport.py, shrink_tests.py and probe_vec.py are identical.
- Lines 1–581 of `killtools/certified.jsonl` equal the RES33N `certified.jsonl`.
- `capx_c60_i22.json` is an exact prefix of `capx_c60_i23.json`, and its first 573 rows are the 571 + the 2
  kill rows. Rows were only appended.

### 2.7 Source review (fastbb.cpp, 1,632 lines; assemble.py; check_tree; replay_split.py)
- **check_tree soundness.** I re-derived the leaf margin inequality by hand. For a feasible x with x = 1 on
  M, x = 0 on O and |x| <= budget:
  sum_r w_r max(0, d_r - |S_r ∩ M|) <= sum_{i free} load_i x_i <= cap (budget - |M|) + excess.
  So a margin > 0 excludes the leaf. Over-budget leaves need |M| > budget. The tree walk rejects repeated or
  unreachable nodes and repeated branch vertices.
- **Not covered by check_tree, and therefore checked by hand above:** the row files (master.json `source` /
  `extra`, copied by fastbb from the row-file header), the `budget`, and the number and location of pending
  leaves. All are as required.
- **Context files** are written only after `expand()` returns normally. Stop, witness and too-big exceptions
  write nothing. Each file is written as `.tmp` and then renamed. An open context stays a pending slot in
  `assemble.py`, so it would raise the pending count above 1. Master nodes end as leaf, branch or context
  only. A master witness returns before master.json is written.
- **Resume** checks an FNV prefix hash, so rows may only be appended. Weights refer to row indices, so closed
  contexts stay valid under appended rows, and check_tree re-checks them anyway. `--split-open` re-expands
  only contexts that have no file.
- I found no path that makes a tree unsound without check_tree noticing.

## 3. Later claims seen (noted, not verified)
- Between 19:10 and 19:34, three further capacity-60 witnesses appeared (contexts 24, 56, 66), all with 33
  holes and 60 occupied F-states. Each was killed by 11–12 pooled rows; `capx_c60_i23.json` now has 607 rows
  (`kill2.log`).
- My only incidental check: each of these vectors satisfies all 2,650 + 571 i22 rows, so capacity 60 has at
  least 4 distinct witnesses under the i22 rows. Each violates only appended rows, and these have
  `s VERIFIED UNSAT` entries in `killtools/certified.jsonl`. I did **not** re-certify those 34 rows.
- V3 was resumed after 19:34 (contexts 17+ closed under the 607-row file), with ablations, dives for c = 61..65
  and an LP difference test. The figures "about 1,300 nodes/s per thread", "20–70x" and "Knuth 10^7.5 for
  capacity 65" are HEURISTIC and not in the README.
- My timings agree with the first of these: V1 about 1,000 nodes/s and V2 about 1,375 nodes/s, wall, 1 thread.
- Task G2 is extending fastbb (slice rule) concurrently. Nothing of it was in the record by 20:31.

## 4. Problems found (none refutes a claim)
1. **Labels.** The README calls exact tree replays "CERTIFIED". Under the phase-2 rules, CERTIFIED means a
   cake_lpr-checked LRAT proof, and a replayed tree is **EXACT TREE**. V1 and V2 should be relabelled EXACT
   TREE. For V2 the README cites `replay_split.py`, a new script. Its replay is now also confirmed by the
   unchanged `assemble.py`, run piecewise (2.3).
2. **Missing hashes.** `data/` is empty, although the README says it holds "small result files and SHA-256
   lists". The record states no hash of the extra-row files, trees, binary or source.
3. **Mutable row file.** master.json names the extra rows by a mutable path outside Git
   (`/home/jay/research/data/fastbb-20261113/in/…`), so a later replay uses the file's content at that time.
   `capx_c60_i23.json` has in fact grown from the stated 573 rows to 607. The 573-row state is recoverable as
   its prefix (2.6).
   - **Recommendation:** record the SHA-256 values in section 2 of this file in the README, and freeze copies
     of the extra-row files.
4. **Wording.** "FINDS the omission trees that pbb_strong.py finds" should read "finds trees for the same
   statements". The trees differ (60,191 vs 28,735 and 819,241 vs 407,101 nodes); the table makes this clear.
5. **Dependencies outside this record** (not checked here; unchanged from RES33N/THEORY310N):
   - the 2,650 Lean rows;
   - the Lean lemma for the pending "state 0 missing" branch (`zero_mem_residualOccupied`, cited by RES33N);
   - Lemma A (h(F) >= 84 - N5);
   - the semantic soundness of the coupled CNF encoder: "UNSAT => valid demand-1 row". The coupled rows are
     certified only at the CNF level and are not Lean-checked.
6. **My own rule deviation.** The 0.4 s kill-row re-certification unit overlapped with the V2 rerun unit (2
   threads for under a second).
