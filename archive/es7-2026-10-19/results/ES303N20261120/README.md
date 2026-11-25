# ES303N20261120: the Z*-row and the budget-68 tree (target ES(8) ≤ 303)

> **Superseded for the bound (24 Nov 2026): ES(8) ≤ 302, see [ES302N20261124](../ES302N20261124/README.md).** The 303
> statement stays true; its budget-68 tree (b68zs, 178.5 GB) **was deleted on 24 Nov 01:57:10** with the owner's OK, after this
> update and the 302 record were pushed (data-side manifest verify-20261124/manifest_deletions.txt l.4655); this record keeps its counts, hashes and check outputs.
> No independent re-check was made before the deletion, and none can be made now: **ES(8) ≤ 303 has no re-checkable
> evidence of its own and stands through ES(8) ≤ 302** (correction 25 Nov, adversarial audit).

**Status (22 Nov 2026, 06:21 KST): ES(8) ≤ 303 ESTABLISHED. Computer-assisted and unrefereed, with the same kind of evidence as ES(8) ≤ 304.** Every 303 points in general position contain 8 points in convex position. The chain is `composition_303_zzsf : ExcludesHoleBudgetZZsF 68 → N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 303 8`, Lean-checked with standard axioms; Linux audit 22 Nov, §5. Its three hypotheses:
- the budget-68 tree, **EXACT TREE by two in-project checks** (the project's own scripts, not independent in the
  es-research sense; the tree was deleted on 24 Nov): check_tree via v5, and balcheck2, which reads every file
  whole (§5);
- `N66Bound 55`: CERTIFIED cubes plus a written model (N66N20261113);
- `ResidualBound 118`: a written, computer-assisted chain (ES307N20261118).

This is **not** Lean-checked end to end. In the literature: not found in the 21 Nov search (the public bound is
Schroeder's 319, unrefereed; the refereed bound is 408).

The budget-68 finder ran in unit `esr-bal-zbs68` (started 20 Nov 01:33:35, finished 22 Nov 01:08:17). The claim needs two things:
- both tree checks pass (check_tree and balcheck2, §5);
- the Lean chain `composition_303_zzsf` (§4), which compiles already.

What stands now, independent of the tree:
- **the Z*-row:** PROVED (written), with exact controls and a Lean proof (standard axioms only);
- **the budget-66 control tree with the Z*-row:** EXACT TREE by both checkers.

## 1. Statement (target)

ES(8) ≤ 303: every 303-point set in general position contains 8 points in convex position. The current bound is
304 (ES304N20261119).

## 2. The Z*-row (PROVED; Lean)

- **Notation.** Balanced states as in ES305N20261119 §2: f = (f(0) ≥ … ≥ f(4)) with values in [0..5], 252 states.
  The map from points to states is injective.
- **Definition.** Z* = {f(0) = 5, f(4) ≥ 1}, 70 states, closed under transpose and disjoint from Z.
- **Owners.** Its owners are the points of a balanced set H where both a 6-cup of H and a 6-cap of H end.
- **Lemma.** The owners of Z* contain no 6-cap and no 6-cup (THEORY310N20261113 Lemma B, both halves).
  - **6-cap.** Let y1 … y6 be a 6-cap among the owners and c1 … c5 y1 a 6-cup. Then (c5, y1, y2) is either a cup
    turn, which gives the 7-cup c1 … c5 y1 y2, or a cap turn, which gives the 7-cap c5 y1 … y6. H has neither.
  - **6-cup.** Mirror argument, using the 6-cap that ends at the first point of the cup.
- **Consequence.** The owners form an N66-class set (no 6-cap, no 6-cup, no convex octagon), so at most N66 ≤ 55 of
  the 70 states are occupied. This gives the row **h(Z\*) ≥ 15**, on the same hypothesis as the Z-row.
- **Lean** (`LemmaZStar.lean`, here):
  - `Zs_eq` pins the support to `data/zstar.json` (`decide +kernel`).
  - `zsOwners_no_cap` and `zsOwners_no_cup` prove the lemma. They use `rank_attained`, `rank_lt_of_avoids` and one
    `EndingPath` extension.
  - `zs_row : N66Bound 55 → … → 15 ≤ (Zs \ c.occupied).card` is the row.
  - Compile time 6.7 s. `#print axioms` shows propext, Classical.choice and Quot.sound only.
- **Budget form** (`BalancedBudgetsZZs.lean`, here):
  - `ExcludesHoleBudgetZZsF b` is the tree statement: catalog rows, cover cuts, the Z-row and the Z*-row, with
    states 0 and 1 occupied.
  - `balanced_bound_of_hole_budget_zzsf : b ≤ 249 → N66Bound 55 → ExcludesHoleBudgetZZsF b →
    BalancedBound (251 − b)`.
  - `composition_303_zzsf … composition_300_zzsf` cover budgets 68–71. Compile time 2.5 s, standard axioms.
  - States 0 and 1 are always occupied (ES305N20261119 `FixedStatesZ.lean`), so only the zero side needs a tree.
- **Parametric form** (`BalancedBudgetsZZsN.lean`, here; 20 Nov 06:31; `tools/build_zsn.sh`, rc 0, log
  `data/build_zsn.log`; standard axioms only):
  - `z_row_of`, `zs_row_of : N66Bound B → 70 − B ≤ (Z \ occupied).card`, and the same for Z*. These hold for any
    N66 bound.
  - `ExcludesHoleBudgetZZsN r b` puts both rows at demand r.
  - `balanced_bound_of_hole_budget_zzsn : b ≤ 249 → N66Bound B → ExcludesHoleBudgetZZsN (70 − B) b →
    BalancedBound (251 − b)`.
  - `zzsn_55_iff`: at B = 55 the statement is definitionally the recorded `ExcludesHoleBudgetZZsF`.
  - **Prepared, not usable yet:**
    - `composition_302_n54 : ExcludesHoleBudgetZZsN 16 69 → N66Bound 54 → ResidualBound 118 → ForcesConvexNGon 302 8`;
    - `composition_301_n53`, the same with 17, 70 and 53.
    - No N66 bound below 55 is known.
  - Each Lean step needs up to 3.8 GB RSS. Run builds with MemoryMax ≥ 5G.

## 3. Controls

All files are in `data/`.
- **Exact control** (`tools/zstar_control.py`, own code, exact integers): the cup–cap construction X(7,7) and 150 of
  its random subsets.
  - X(7,7) has 252 points with all 252 states occupied and 70 Z*-owners.
  - Injectivity, Lemma Z and the Z*-lemma hold on all 151 sets.
  - Negative controls: the owners of {f(0) = 5} alone contain a 6-cup in 151 of 151 sets, and the owners of
    {f(4) ≥ 1} alone a 6-cap in 137. So both halves of the class condition are needed.
- **Budget-66 tree with the Z*-row** (`tools/zs66_test.sh`):
  - The finder closes it in its master phase: 5,151 nodes, against 771,030 without the Z*-row.
  - Assembled by `balz_assemble_v4.py` and replayed by check_tree: EXACT TREE, 2,576 files, 3,133 rows, minimum
    margin 1.
  - balcheck2: EXACT TREE, cover complete with lemma path 0:1.
- **Root LP** (`tools/lp_zstar.py`, HEURISTIC): 60.23 → 66.00 with the Z*-row. With both rows at rhs r it is
  42 + 1.6 r, so one unit of N66 is now worth 1.6 holes at the root.
- **Production-option dives** (`tools/dives_zs3.sh`, HEURISTIC, 200 dives, seed 1; mean nodes):

  | budget | without Z* | with Z* |
  |---|---|---|
  | 68 | 9.0e8 | 1.05e8 |
  | 69 | 8.4e9 | 8.9e9 |
  | 70 | – | 1.4e11 |

## 4. Method (budget 68)

- **Driver.** `tools/zbs_run0.sh 68 14 16384` runs, in order:
  - the fastbb256 finder, zero side only (state 0 occupied), with `--ktop=16 --klow=4 --dtop=0 --dmid=0`, on
    `balzs.rows` (the 3,131 catalog rows, the Z-row and the Z*-row);
  - `balz_assemble_v4.py` plus `scripts/omission_tree.check_tree` on every file;
  - balcheck2 (own C++) with `BALCHECK_EXTRA_ROWS = data/zzs_rows.json` and lemma path 0:1.
- **Trust.** The finder is untrusted. Both replays recompute every leaf margin in exact integers.
- **Lean.** The Lean rows are the JSON rows (ES305N20261119 `tools/rows_match.py`). The Z*-support is
  `OmissionZStarRow.zsIndices` (`Zs_eq`).
- **Limits.** Unit `esr-bal-zbs68`: CPUQuota 1400 %, MemoryMax 8G, MemoryHigh 7G, MemorySwapMax 0, RuntimeMaxSec
  280,000, nice 10. Work dir `/home/jay/research/data/bal186-20261119/zrow/b68zs`.
- **Owner approval.** The owner approved 14 threads for budget 68. This run replaced the Z-row-only run at 01:33,
  which is resumable from `zrow/b68z` (ES305N20261119 §8, "Switch").
- **Restart at 10 threads (20 Nov 11:01, owner OK ~11:00).** The owner approved running the N66 level-15 cube
  campaign (`N66N20261113/cubes20261120/`) alongside budget 68, so budget 68 went from 14 to 10 threads.
  - Same unit name, `./zbs_run0.sh 68 10 16384`, CPUQuota 1000 %, RuntimeMaxSec 300,000 (ends 23 Nov 22:21), other
    limits unchanged.
  - fastbb256 reloads `occ/master.txt` (`"master_resumed": true`), so the 32,755 contexts are the same; 7,257 closed
    contexts were kept and 25,498 remain. The thread count does not enter the master.
- **Restart at 11 threads (20 Nov 14:37).** The Δ unit `esr-dlt-n8m17` ended at 14:28 and freed its thread; it went
  to budget 68 (the campaign's fifth slot stays off: the n66 memory track binds).
  - Before the restart, every input of `zbs_run0.sh 68` was hashed against §6 and ES305N20261119 (script, `balzs.rows`,
    `zzs_rows.json`, `balz_assemble_v4.py`, fastbb256, balcheck2, catalog): all equal, all modified before 11:01.
  - `./zbs_run0.sh 68 11 16384`, CPUQuota 1100 %, other limits unchanged; RuntimeMaxSec 300,000 s now ends 24 Nov
    01:57.
  - Resumed with `"master_resumed": true`: 9,875 closed contexts kept (equal to the closed events in `occ.out` at the
    stop), 22,880 remain, sum 32,755.
- **Restart at 22 threads (20 Nov 17:41; owner raised the thread cap to 80–90 % of the 32 logical CPUs at ~17:30).**
  The CPU has 16 cores with 2 threads each, so threads beyond 11 on budget 68's cores are SMT siblings.
  - `taskset -c 5-15,21-31 ./zbs_run0.sh 68 22 16384`, CPUQuota 2200 %: budget 68 owns cores 5–15 (both threads),
    and the time-limited N66 cubes keep cores 0–4. RuntimeMaxSec 300,000 s now ends 24 Nov 05:01.
  - Inputs unchanged since the 14:37 hash check (no file in `zrow/` newer than 14:37).
  - Resumed with `"master_resumed": true`: 16,695 closed contexts kept (equal to the closed events at the stop),
    16,060 remain, sum 32,755.
  - Baseline at 11 threads (17:40): 496,116 simplex iterations/s, 2,289 nodes/s over the last 30 min
    (`data/smt-20261120/rates.jsonl`). The finish window is re-quoted only from the measured rate.

## 5. Results (to be filled in)

- **Master.** 657 s, 65,529 master nodes, 32,755 contexts.
- **Progress at 05:23.** 4,128 of 32,755 contexts closed, 36.5 M nodes, 181,068 CPU-s.
- **Projection (HEURISTIC).**
  - Contexts run in index order, and the cost falls steeply with the number of holes fixed in a context: mean 661 s
    with none, 51 s with 5, 3.7 s with 9.
  - Weighting each class by its share of the contexts gives about 190 CPU-h and 1.45e8 nodes in total. That is 1.4×
    the dive estimate.
  - Remaining: about 10 h at 14 threads. Finder done about 15:30 KST, checks about 1–2 h after that.
  - **Correction at 10:35: that projection was wrong.**
    - Progress: 6,908 of 32,755 contexts closed, 88.6 M nodes, 442,486 CPU-s, 13.93 threads in use.
    - The cost per context rises along the index order, within each class. Mean seconds per context in
      successive blocks of 1,500 closed contexts:

      | holes fixed | blocks 1–5 |
      |---|---|
      | 5 | 55, 51, 85, 170, 157 |
      | 7 | 15, 18, 19, 58, 58 |
      | 8 | 6, 9, 8, 31, 37 |

    - Holdout test: class means from the first 50 % (70 %) of closed contexts predicted 99 k (66 k) CPU-s for the
      rest; the actual cost was 273 k (169 k). The method underestimates by about 2.6–2.8×.
    - New estimate, using the latest block's means per class: about 1.5 M CPU-s remain, about 30 h at 14 threads.
      Finder done about 21 Nov 17:00 KST, range about 21 Nov 06:00 to 22 Nov 12:00. Checks take 1–2 h after
      that. The unit's RuntimeMaxSec (280,000 s) ends 23 Nov 07:19; the finder is resumable.
  - **At 10 threads from 11:01:** the same 1.5 M CPU-s (range 1.0–2.5 M) take about 42 h (28–70 h). Finder done
    about 22 Nov 05:00 KST, range 21 Nov 15:00 to 23 Nov 09:00.
  - **At 11 threads from 14:37:** the 11:01 window scaled by 10/11 on what remained (about 10 % faster). Finder done
    about 22 Nov 01:30 KST, range about 21 Nov 13:00 to 23 Nov 03:00. Not a new projection: closed/todo × rate is
    not used (it failed the holdout test above).
- **Finder complete (22 Nov 01:08:17, rc = 0).** Resumed 21 Nov 19:23:11 with 7,817 contexts to do (22 threads,
  CPUQuota 1600 %). All 32,755 contexts are closed (`occ.out`: 32,755 closed events; their node counts sum to
  246,300,823; the largest context, ctx-5377, has 765,389 nodes in a 296 MB `.json.gz`, 773 MB of JSON).
- **Assembly stopped by the memory guard (clean stops, no kernel OOM kill).**
  - 01:09:41: `zbs_run0.sh` went on to `balz_assemble_v4.py` with 22 worker processes, and the unit reached 7,813 MB of
    its 8,192 MB.
  - 01:12:07: a probe that ran v4's `one()` on ctx-5377 alone also reached its 8 GB limit. Python's objects for that
    context alone exceed 8 GB, so fewer workers cannot fix it.
  - The stopped runs left partial files in `b68zs/files/`. Every file is rewritten by the re-run, and the acceptance
    check below requires every file to be newer than the re-run's start.
- **Memory-lean assembler `balz_assemble_v5.py`** (22 Nov; work dir `zrow/`; v4 unchanged):
  - Contexts with `.json.gz` ≤ 10 MB go through v4's `one()` unchanged.
  - Larger contexts (2,007 of 32,755) go through `one_big`, which streams the context once. It writes the same output
    file (byte-identical) and validates the node graph globally: indices in range, each node reached exactly once
    from the root, no unreachable node, branch fields are integers.
  - `one_big` then cuts the tree into subtrees of at most 30,000 nodes. It calls the **unchanged** `check_tree` on each
    subtree, preceded by the branch/pending prefix of the master path plus the in-context path to the subtree root,
    and requires pending = prefix length.
  - So every leaf margin is still computed by the unchanged `check_tree`, with exactly the fixings the leaf has in the
    full assembled tree. Every leaf lies in exactly one piece, and the global pass covers the structural checks that
    `contexts()` makes on the whole tree.
  - Controls (`b68zs/v5ctl/ctl.py`):
    - 9 contexts (2 to 9 MB) at cut sizes 30,000, 1,500 and 97: 27/27 gave the same `(ok, leaves, minimum margin,
      nodes)` as v4's `one()` and byte-identical output files.
    - Negative controls on modified copies of ctx-2, each caught: capacity × 1000 in one leaf ("Nonpositive leaf
      margin"), a reused child ("Repeated or invalid tree node"), an unreachable node, a leaf replaced by pending
      (ok = False), a branch on the fixed vertex 0, and booleans as a child index or vertex.
- **Acceptance rules (written before the results):**
  - v5's summary must show `bad: []` and 3,133 rows.
  - balcheck2 must show `failed 0` and cover complete.
  - v5's `nodes`, `leaves` and `minimum_margin` must equal balcheck2's.
  - Pre-registered at 01:50 from `occ.out` and `occ/master.json`:
    - files = 32,765 (32,755 contexts plus 10 master-closed weighted leaves);
    - nodes = 246,300,833 (the occ.out sum 246,300,823 plus the 10);
    - leaves = 123,166,799. Each context is a full binary tree, so it has (n_c + 1)/2 leaves; plus the 10.
  - The convention was checked on ctx-2: occ.out has 43,753 nodes, and v4's `one()` returned 43,753 nodes and 21,877
    leaves.
  - Every file in `files/` must be newer than the re-run's start, and their number must equal the summary's `files`.
- **Probes on the largest context (ctx-5377 = file 27387):**
  - `one_big`: ok, 382,695 leaves, minimum margin 1, 765,389 nodes; 101 s, max RSS 2,083 MB.
  - balcheck2 in subset mode on the same output file: FILES OK, 765,389 nodes, 382,695 leaves, minimum margin 1,
    3,133 rows; 7.4 s, 2,332 MB.
  - v4 `one()` on the largest context routed to it (ctx-30329, 10.0 MB): 3.1 s, 425 MB.
  - Files: `data/v5ctl/`.
- **Re-run (started 22 Nov 01:26:33).**
  - Assembly: unit `esr-bal-zbs68asm`, `balz_assemble_v5.py` (SHA-256 `964b00007e5b…f6ad`), NW 10, NW_BIG 3,
    BIG_BYTES 10,000,000, SUB_NODES 30,000; CPUQuota 1000 %, `taskset -c 5-14`, MemoryMax 8G.
  - The start marker is `b68zs/asm_v5_start.txt`.
  - `tools/chain303.sh` (unit `esr-bal-chain303`) then requires the EXACT TREE line, file count = summary
    `files` and no file older than the marker. Only then does it start balcheck2 (unit `esr-bal-zbs68bc`, 4 threads).
- Re-run after the stop: started 22 Nov 03:48:48 (fresh marker), same v5 SHA and parameters.
- **Check A (check_tree, via v5): PASSED** at 06:06:31, rc 0.
  - The label is "EXACT TREE (check_tree on every assembled file; files above BIG_BYTES piecewise by the unchanged
    check_tree, one_big)".
  - Results: files 32,765; nodes 246,300,833; leaves 123,166,799; minimum margin 1; `bad: []`; rows 3,133; Z-row and
    Z*-row support 70 at rhs 15; zero side only.
  - Every value equals the pre-registered one.
- **chain303 parse bug (22 Nov 06:06:53).** The v5 summary that `steps.log` receives spans several lines.
  - `chain303.sh` read only the first one, which lacks the label, so it wrote "assembly did not pass" and did not
    start balcheck2.
  - The main session redid the chain's file checks: files 32,765 = summary `files`, 0 files older than the marker.
  - It then started balcheck2 by hand with the chain's command: unit `esr-bal-zbs68bc`, 4 threads, binary
    `951b90dc…`, rows `zzs_rows.json` `dc6a410f…`, MemoryMax 9000M instead of 8G. This is logged in `steps.log`.
- **Check B (balcheck2): PASSED** at 06:21:29, rc 0: `{"verdict": "EXACT TREE (balcheck)", "budget": 68, "contexts":
  32765, "failed": 0, "nodes": 246300833, "leaves": 123166799, "min_margin": 1, "rows": 3133, "cover": "complete with 1
  lemma path(s) 0:1"}`.
  - balcheck2 reads every file whole, so the result does not rest on v5's piecewise cutting alone.
  - Memory peak 6.6 GB of 9 GB.

**Acceptance (22 Nov 06:30, main session; every criterion pre-registered at 01:50):**

| criterion | result |
|---|---|
| v5 label EXACT TREE, files = 32,765, nodes = 246,300,833, leaves = 123,166,799, minimum margin ≥ 1, `bad: []`, rows 3,133 | met: all equal (`data/accept303/v5_summary.json`) |
| balcheck2 `failed 0`, cover complete | met (`data/accept303/balcheck.json`) |
| v5 and balcheck2 agree on nodes, leaves, minimum margin | met: 246,300,833 / 123,166,799 / 1 |
| every file newer than the re-run marker; file count = summary `files` | met: 0 older, 32,765 = 32,765 |

House replay items (es-research §2):
- **The rows are exactly the stated ones.** `data/accept303/rows_binding_assert.txt` asserts it with own code, 22 Nov:
  - `balzs.rows` rows 0–3,130 equal the catalog constraints in order (catalog `acaf6323…`);
  - row 3,131 is the Z-row (`zrow.json`, 70, rhs 15) and row 3,132 the Z*-row (`data/zstar.json`, 70, rhs 15);
  - `balz.rows` is rows 0–3,131;
  - Lean's `OmissionBalanced.row r = rowChunks[r/128][r%128]` with `rowChunks = #[rows0, rows128, …]` in order;
  - with ES305's `tools/rows_match.py` (exit 0, 0 mismatches) this binds the tree rows to `ExcludesHoleBudgetZZsF 68`.
- **The extra rows are justified:** the Z-row by `z_row` (LemmaZ) and the Z*-row by `zs_row` (LemmaZStar), both Lean,
  with standard axioms. `Z_eq` and `Zs_eq` (`decide +kernel`) pin their supports.
- **The cover is complete:** balcheck2 reports "complete with 1 lemma path(s) 0:1", and v5 checks covered + upper = N in
  every file. The files are the 32,755 contexts plus the 10 master-closed weighted leaves.
- **The only pending side is "state 0 missing"** (zero side only). The statement's `holes 0 = 0 ∧ holes 1 = 0` is
  discharged by `zero_mem_occupied` and `one_mem_occupied` (FixedStatesZ, Lean).
- **Inputs re-hashed against the pins (22 Nov):** `balzs.rows` `9135465a…`, `zbs_run0.sh` `78bb3051…`, `fastbb256` `df17fa74…`,
  `scripts/omission_tree.py` `35cb3050…`, `balz_assemble_v5.py` `964b0000…`, balcheck2 `951b90dc…`, `zzs_rows.json`
  `dc6a410f…`, catalog `acaf6323…`.
- **Axioms on Linux:** the composition audit (formalize wave 1) rebuilt the nine 30x files into one olean directory with
  an import-closure check.
  - Its `BalancedBudgetsZZs.lean` copy hashes to the record's `7684a1de…`; lean rc 0.
  - `#print axioms OmissionBalancedZZsF.composition_303_zzsf` gives `[propext, Classical.choice, Quot.sound]`
    (`data/accept303/axioms_comp_audit_20261122.txt`).
  - The audit's own reviewer had not reported yet when this was filed.
- **balcheck2 assurance (wave 3, finished 22 Nov; both verifiers confirmed):**
  - Verdict: no defect can make balcheck2 print "failed 0 / cover complete" wrongly.
  - Build identity (EXACT): the production binary `951b90dc…` is `g++ -O2 -std=c++17 balcheck2.cpp -lz`, bit for bit.
  - Overflow and index bounds (EXACT) hold for lists under 2^31 entries and K + lemma paths ≤ 8,521,760. The 303 run has
    K = 32,765.
  - Sanitized runs and 77 controls (COMPUTED) found nothing; bounded model checks (COMPUTED) found nothing within their
    bounds.
  - Two findings, neither of which applies to this acceptance:
    - F1, a use-after-free in the error message for a corrupt gzip file. Error path only.
    - F2, the reported global minimum margin is wrong when some context has margin -1. Here `failed 0`, so no context is
      at -1.
  - Reports: `/home/jay/research/data/bal186-20261119/assure-wave3/` (README, `verify/`).

## 6. Files and hashes (SHA-256)

**Budget-68 run (22 Nov), work dir `/home/jay/research/data/bal186-20261119/zrow/b68zs` (143 GB; certificate; deleted 24 Nov 01:57, see the banner):**

| file | SHA-256 |
|---|---|
| `occ/master.json` | `7d00302cb81790072774ea7991485cddaad7462565e81e56e6050db2127caef2` |
| `files/summary.json` (v5) | `fb84e3ff2cd44c00ad45e20ff33257b9a71704bad7dbdd352dbd3ceae47e4c99` |
| `balcheck.json` | `c01da0306586f6fc22609b85cc17da960ca544ee5e9c70d7ce6ebd313bf5632b` |
| `balcheck.tsv` (32,766 lines) | `2a42aaa1f0a86155e666a84b196a52b4f7e6b28da21fc32030e79e4969e0589a` |
| `data/accept303/axioms_comp_audit_20261122.txt` | `52e6c7cc6c90d8d14c49101c685dd10e5bc1f315864037c5cfcd67d8d189ee24` |

| file | SHA-256 |
|---|---|
| `LemmaZStar.lean` | `47bd1f5618ee515b4f9f5c398bd6239b1c650a16dc6aa1ae687b7dafd49fd61c` |
| `BalancedBudgetsZZs.lean` | `7684a1deb0297c7444b1719d0403d1e814ddbab3623ec5c13320294f03278a8e` |
| `Composition303.lean` (docstring updated 05:30) | `bbecd6cf67b12cfa377f7f252923a0b910e27f20ea10e4174d131d358cfe426e` |
| `BalancedBudgetsZZsN.lean` (parametric) | `4cfface86e87798e34e60c98228a757505f13ea491c763a2caa67b73b41203f7` |
| `tools/build_zsn.sh` | `c645ec6a8306524c1858d0af4174c508f582e78dcab8845a2a33f379b084dd9f` |
| `data/zstar.json` (70 indices, rhs 15) | `26d8886058cc53972dfe274e04150c4aee0ff4fffafb974a8c7c89cd57cef328` |
| `data/zzs_rows.json` (Z-row and Z*-row for balcheck2) | `dc6a410f9fa164ee5565fd9827f4697af052b311afda6d806a136c0cd3d896d3` |
| `zrow/balzs.rows` (work dir; 3,133 rows) | `9135465aac32b575d3f859192891b5088b6a23c6d521687aef1b032e64e2f2b8` |
| `tools/zbs_run0.sh` | `78bb3051a544ceec059cdcc9439f018326d7c2044747d154aa6b28929cc3b9ac` |
| `tools/balz_assemble_v4.py` | `813d5f2a06d38e6ca6a519249aad5151617670fdb0cd3adfd40739e5aa7d6a7d` |
| `fastbb256` (finder, work dir) | `df17fa7471f27ab80afe34363d4945b324ac1e007e27e1f8dbadd2d342c4cc90` |
| `zrow/zs66/occ/master.json` (budget-66 control) | `d90d8a7b49c69630f12f958f3051a94198189cf357ceb0b3dce0d9b986160586` |
| `zrow/b68zs/occ/contexts.json` (32,755 contexts) | `31ac2b894f58e050e2920c1962982e5a7d232e4428ae1c313c09d2ae1e1b74da` |

The shared inputs (catalog rows, Z-row, LemmaZ, FixedStatesZ, balcheck2, check_tree) are those of ES305N20261119
§7 and ES304N20261119.

## 7. What remains

- The budget-68 finder, then both checks. After that the headline can say ES(8) ≤ 303 (computer-assisted,
  unrefereed).
- An independent re-check by another reader or agent: the Z*-lemma, both tree checks and the Lean chain (the tree
  checks can no longer be re-run: b68zs was deleted on 24 Nov).
- The next steps (HEURISTIC prices in ES305N20261119 §8):
  - budget 69 with the present rows costs about 5.5e9 nodes;
  - N66 ≤ 54 moves both capacity rows to 16 (root LP 67.6);
  - N67 ≤ 96 is the largest lever, but it needs its own campaign.
- **The N66 lever after the Z*-row (20 Nov 05:30–05:45, HEURISTIC).**
  - Both capacity rows rest on N66, so each unit of N66 now lifts both rows. Root LP: 42 + 1.6 r with both rows
    at rhs r.
  - Production-option dives (`tools/hyp_n66_dives.sh`, rows file = `balzs.rows` with both rhs raised; 200 dives,
    seed 1; mean nodes; data `data/hyp_*.last.json`). **The rows used are hypothetical: N66 ≤ 54 and N66 ≤ 53 are not
    proved.**

    | budget (ES bound) | present rows (N66 ≤ 55) | N66 ≤ 54 (rhs 16) | N66 ≤ 53 (rhs 17) |
    |---|---|---|---|
    | 68 (303) | 1.05e8 | – | – |
    | 69 (302) | 8.9e9 | **8.0e7** | – |
    | 70 (301) | 1.4e11 | 1.7e10 | not run |
    | 71 (300) | – | 2.3e11 | 4.1e9 |
    | 72 (299) | – | – | 1.6e11 |

  - So N66 ≤ 54 would make 302 cheaper than 303 is now, and each further unit of N66 is worth about one point of
    ES(8).
  - Cost of N66 ≤ 54 (level 15 of N66N20261113): ROADMAP20261115/ROUTE307_1116 extrapolated roughly 200–450
    slot-hours (×2.5–5 over level 14). The relaxation may also be SAT at level 15 even if N66 ≤ 54 is true.
  - **Level-15 pilot** started 05:45 (unit `esr-n66-p15`, 0.6 thread, 4.5 h limit; `W/p2/s15/`, see
    `data/n66_level15_pilot_README.txt`).
    - Setup: unchanged `p2_batch.py`, warm start from the 660,810 quadruples of the certified level-14 base, with
      `--tauclose --sb`.
    - It measures the cost of a level-15 iteration and whether the CEGAR loop finds a model with no violated
      quadruple. Such a model would end this route.
    - **Iteration 1 (COMPUTED):** SAT in 622 s at 0.6 thread. The 15-hole model violates 4,366 quadruples, so the
      loop progresses as it did at level 14 (4,974 and 6,403 on 13 Nov).
    - At 05:56 the memory guard stopped the unit cleanly, with no OOM kill. Its track `n66` had the 3,000 MB default.
    - The guard was restarted as `esr-memguard-1120` with `n66=6000` (total 24,000 MB unchanged). The pilot resumed
      from its saved state as `esr-n66-p15b` (`W/p2/s15/q.out`).
    - **Result (COMPUTED, 10:28, unit reached its 4.5 h limit).** Global CEGAR at L=15, 0.6 thread, wall-clock
      solve times:

      | iteration | warm quads | solve s | violated | status |
      |---|---|---|---|---|
      | p15 it1 | 660,810 (+τ) | 622 | 4,366 | SAT |
      | p15b it1 | 669,416 | 2,406 | 4,563 | SAT |
      | p15b it2 | 673,979 | 7,216 | 2,928 | SAT |
      | p15b it3 | 676,907 | > 6,500 | – | killed by RuntimeMax mid-solve |

      - No model without violated quadruples appeared, so the route is not refuted at L=15.
      - Each solve costs about 3× the one before, while the violated count falls only about a third per step. At
        L=12 and L=13 the global solve went UNSAT outright (641,229 quads, 1,998 s and 5,023 s); at L=14 the global
        iterations took 195–702 s and the campaign switched to cubes.
      - The state is saved in `W/p2/s15/q.json` (676,907 quads).
      - The killed iteration left `W/p2/b15q/it3/cert.lrat` (13.7 GB, partial, certifies nothing) and `cert.cnf`
        (0.68 GB). The partial LRAT was deleted with the owner's OK (20 Nov ~12:25); the CNF is kept.
  - **Level-15 cube calibration** (HEURISTIC timing; unit `esr-n66-cal15`, 0.6 thread, started 10:33, ends by
    18:10; `W/cal15.sh`, `W/p2/cal15/`).
    - It runs level-14 depth-0 cubes at L=15, easiest first: `hhhhhh`, `hohhhh`, `hhhhho` (L=14 solves 124, 244
      and 393 s at 1 thread). Same options as the level-14 driver; warm start from `q.json` (683,670 quads after
      τ-closure).
    - The ratio of L=15 to L=14 cube time prices the campaign: level 14 cost 43.7 process-h, 60.3 slot-h and 82 GB of
      trimmed LRATs over 200 cubes (68 split, 132 certified leaves).
    - Any UNSAT leaf is certified by `p2_cert.sh` (cake_lpr) exactly as in the level-14 campaign.
    - **Cube `hhhhhh` (CERTIFIED for this cube only, 10:44):** UNSAT at the first solve with the warm set, no CEGAR
      iteration. cake_lpr `s VERIFIED UNSAT`, p2_verify ALL_OK, `cert.json`: "CERTIFIED holes >= 16" inside the cube.
      trim.cnf `51c01ff2…`, trim.lrat `eb3070ab…` (zstd copy checked against that hash).

      | | L=14 | L=15 | ratio |
      |---|---|---|---|
      | CaDiCaL process s | 124.1 | 289.6 | 2.3 |
      | conflicts | 109,509 | 487,146 | 4.4 |
      | trimmed LRAT bytes | 40.7 M | 188.0 M | 4.6 |
      | CaDiCaL RSS | – | 2,474 MB | |

    - Next: `hohhhh`, `hhhhho` (cal15.sh), then `hhhhoo`, `ohhhho`, `hhooho` (`cal15b.sh`, unit `esr-n66-cal15b`,
      started automatically when cal15 ends).
  - **Campaign started 11:06 with the owner's OK** (record `N66N20261113/cubes20261120/`, unit `esr-n66-drv15`,
    deadline 23 Nov 12:00). By 11:11: 10 leaves certified (the 2 calibration leaves, adopted through `accept()`,
    and the 8 cubes refuted by unit propagation on the SB clauses), 4 cubes running, 24 pre-split.
  - **302 follow-up prepared (zero CPU; refuses to run until N66 ≤ 54 is verified):**
    - `zrow/balzs_n54.rows` (`9e2dc29a…`): `balzs.rows` with the Z-row and the Z*-row at rhs 16; nothing else
      differs. `zrow/zzs_rows_n54.json` (`8419984c…`) for balcheck2.
    - `zrow/balz_assemble_n54.py` (`d16733e5…`): v4 with RHS = 16, and the summary records "requires N66 <= 54".
    - `zrow/zbs54_run0.sh` (`4a2015bb…`): zbs_run0.sh on those files, output `b<B>zs54`. It exits with code 9
      unless the marker `zrow/N66_LE_54_VERIFIED` exists (tested).
    - Lean: `composition_302_n54` (BalancedBudgetsZZsN.lean, compiled) takes exactly this tree statement
      (`ExcludesHoleBudgetZZsN 16 69`), N66Bound 54 and ResidualBound 118.
    - The residual side does not gain from N66 ≤ 54 alone: at budget 36 it removes (21,15), but (19,17) and
      (20,16) remain (Knuth 2e10 and 3e11 nodes, ES306N20261119 §4).
  - **Campaign driver (prepared before the owner's OK; started 11:06 after it, see above):** `W/p2c15_driver.py` = `p2c14_driver_r7.py`
    with L 15, warm `p2/s15/q.json`, output `p2/c15`, units `esr-n66-c15-<id>`, time limits ×3 (3,600 / 7,200 s),
    MemoryMax 6500M, and `DELETE_PARTIALS` (off unless the owner agrees). Calibration leaves are adopted only
    through the level-14 `accept()` rules with L = 15. `--selftest` passes; a dry adoption accepted `hhhhhh`, and
    the 64-cube leaf cover check holds.

## 8. Resume

```bash
cd /home/jay/research/data/bal186-20261119/zrow
taskset -c 5-15,21-31 ./zbs_run0.sh 68 22 16384   # as unit esr-bal-zbs68, CPUQuota 2200 % (STATUS20261120 §6); resumes the finder
                               # (closed contexts are kept), then both checks
bash leanzs/build_zs.sh        # Lean: FixedStatesZ, LemmaZStar, BalancedBudgetsZZs
```

The finder is complete. Only the two checks remain: the re-run commands (fresh marker, v5 assembly, then
`chain303.sh`, which starts balcheck2) are in [STATUS20261121_1930](../STATUS20261121_1930/README.md) §6. Copies of
`balz_assemble_v5.py` and `chain303.sh` are in `tools/`.
