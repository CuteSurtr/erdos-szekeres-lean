# ES307N20261118: ES(8) ≤ 307 (route A), 18 November 2026

## 1. Headline

**Every set of 307 points in general position in the plane contains a convex octagon: ES(8) ≤ 307.**

- **Label: PROVED, computer-assisted.** It is a written chain whose inputs are labelled PROVED (Lean or written),
  CERTIFIED or EXACT TREE, each listed in §1.1. The trust level is that of the ES(8) ≤ 308 chain
  ([VERIFY308](../LO33N20261113/budget34/VERIFY308/README.md)).
- **Not** Lean-checked as a whole, unrefereed, unpublished and uncommitted. "New" means only "not found in this search":
  the public bound found by the novelty checks is 319 (Schroeder, Zenodo, unrefereed) and the refereed bound is 408
  ([NOVELTY20261115](../NOVELTY20261115/README.md), [WATCH_1118](../NOVELTY20261115/WATCH_1118.md)).
- Status 10:55 KST, 18 November 2026: every computational item of the checklist
  [VERIFY307 §1](../LO33N20261113/budget34/VERIFY307/README.md) has passed (§5). Its C1 cell and §6a still ask for a
  second reviewer of the Lean-side composition links 1, 2 and 4; VR's read of 12:04 (below) is one more reading of them.
- **Final independent read: claim `es307-final-1118` CONFIRMED by VR** ([VERIFY_ES307_FINAL.md](VERIFY_ES307_FINAL.md)):
  - VR re-derived the chain and read the Lean signatures;
  - every evidence file and hash matches;
  - its own rebuild of `tcheck_b35` gives EXACT TREE, with output byte-identical to the 09:31 run;
  - the split was checked node for node.
  VR's wording notes W1-W8 were applied to this record at about 12:40.

### 1.1 Inputs and their labels

| # | input | label | where |
|---|---|---|---|
| L1-L5 | \|S\| ≤ 1 + \|H\| + \|R\| and the forcing step; \|H\| ≤ 187; the 2,650 rows, \|R\| + h(C) = 154, h_0 = 0; h(F) ≥ 18; Lemma A h(Lo) ≥ 70 − N66 | PROVED (Lean / written) | as in the 308 chain ([ROUTE307_1116 §1.2](../ROADMAP20261115/ROUTE307_1116.md)) |
| L7-L9 | budget-33 slices (18,15), (19,14); 1,020 coupled rows; budget-34 slices (18,16), (19,15), (20,14) | EXACT TREE / CERTIFIED | VERIFY308 |
| L10 | budget-35 slices (18,17) and (19,16) | EXACT TREE (tcheck_b35 + fresh_replay_v3, 15 Nov; pycheck_b35 0 differences, claim `p307v-l10-pycheck`, VB CONFIRMED) | budget34 README; VERIFY307 §4.1 |
| **L11** | **budget-35 slice (20,15)**, rows `b35s20-v169`, packet `runs/b35s20/bb-s1` | **EXACT TREE by three implementations** (§5) | this record |
| **L13** | **N66 ≤ 55** (level-14 cubes) | **CERTIFIED** per cube + PROVED model soundness; cover complete; claim `n66-le55-cubes-1118` CONFIRMED by VS and VN | [N66N20261113](../N66N20261113/README.md), [cubes20261115](../N66N20261113/cubes20261115/STATUS_campaign.md) |

N66 ≤ 56 (L6) is superseded by L13. N5 is not used: the chain is N5-free, like the 308 chain.

## 2. Statement

ES(8) ≤ 307, i.e. every 307 points in general position contain 8 points in convex position.

The conditional form was already PROVED (ROUTE307_1116 §1.4 (A); claim `p307-chain`, VS CONFIRMED 16 Nov):
**N66 ≤ 55 and the exclusion of the budget-35 slice (20,15) imply ES(8) ≤ 307.** Both inputs are now in hand.

## 3. Model and soundness

The model is that of the 308 bridge ([bridge/README.md](../LO33N20261113/budget34/bridge/README.md) §2-4) and ROUTE307 §1.

1. S is octagon-free, so |S| ≤ 1 + |H| + |R|, |H| ≤ 187 and |R| + h(C) = 154. The rows (Lean, coupled and appended)
   hold for the hole vector of every actual nonempty R.
2. Budget 33, then 34 (the 309 and 308 chains) give h(C) ≥ 35.
3. Budget 35. h(F) ≥ 18 (nine Lean rows), and h(Lo) ≥ 70 − N66 ≥ 15 by Lemma A with **N66 ≤ 55**. So h(C) = 35 leaves
   only (h(F), h(Lo)) ∈ {(18,17), (19,16), (20,15)}.
   - A slice tree with capacity rows (F, T) and (Lo, 35 − T) shows that no admissible hole vector with |H| ≤ 35 and
     state 0 occupied has h(F) ≥ T and h(Lo) ≥ 35 − T.
   - (18,17) and (19,16) are excluded (L10), and **(20,15) is excluded (L11)**.
   - Hence h(C) ≥ 36, |R| ≤ 118 and |S| ≤ 1 + 187 + 118 = 306.
4. Forcing (`Partition.forces_of_population_bounds` with 187 and 118) gives the threshold 187 + 118 + 2 = **307**.

The only branch the slice trees leave pending is "state 0 missing". Lean discharges it with
`zero_mem_residualOccupied`.

## 4. Method (18 November 2026, 02:24-10:51 KST)

- **N66 ≤ 55.** The level-14 relaxation is split into cubes on the states 25 12 16 29 17 37 and the re-split states
  (cube plan [cubes20261115/README.md](../N66N20261113/cubes20261115/README.md)).
  - Each leaf is certified by a CaDiCaL 2.1.3 LRAT accepted by cake_lpr, after p2_verify ALL_OK.
  - Driver copies r2-r7 ran on 15-18 Nov. Today's r7 certified the last 22 leaves; its final state at 04:28:08 was
    **132 of 132 leaves accepted, COVER_OK**. No cube was SAT in the whole campaign.
- **(20,15).** The omission branch-and-bound tree was built by fastbb2 (finder only) with these loops and passes:
  - continue34_v11, then continue34_v12 with the reviewed inbox ([V12_REVIEW.md](../LO33N20261113/budget34/tools/V12_REVIEW.md),
    READY WITH NOTES), at 6+1 → 9+3 → 10+4 threads;
  - the concurrent high-cap side pass `highcap_v1.py`;
  - the standalone high-cap pass `run_tree_v6.py --too-big-only` (cap 1,000,000). Both runs are finder receipts only:
    - `hc169a` closed 10 contexts, then exited −6 (fastbb2 `std::bad_alloc` under run_tree's 1,400 MB address-space
      limit with 14 threads);
    - `hc169b` (6 threads, `MALLOC_ARENA_MAX=2`) closed 17 and exited 4 (PARTIAL: 4782 too big);
  - a successor-packet split of the last open context 4782 into 16 contexts (`prepare_successor_b35.py`, a copy of
    the 14 Nov tool that differs only in the packet path, its docstring and one comment; `run_tree_v6.py --bb=bb-s1 --split-open=4`).
  - Rows `b35s20-v169` = 2,650 Lean rows + 2 capacity rows + 1,020 coupled rows + 970 appended rows (69 rounds, 111
    batches), each row certified and audited.
  - Progress today: 1,652 contexts closed at 02:24 → 8,037 at 08:56 → 8,064 at 09:24 → all 8,080 of `bb-s1` at 09:30.

## 5. Results: the VERIFY307 checklist, all passed

| item | check | result |
|---|---|---|
| C1 | written chain (ROUTE307 §1.3-1.4) | PROVED (`p307-chain`, VS CONFIRMED 16 Nov) |
| C2 | L10 slices | done (§1.1) |
| N1 | N66 cover by accepted certificates | **COVER COMPLETE**: 132 accepted, 0 rejected, 0 of 16,384 assignments of the 14 split states uncovered (P307V's `n66_cover_check.py --deep`, run by the main session at 04:28) |
| N2 | four checks per accepted cube (fresh cake_lpr + hashes; trim ⊆ cert; cert = F_c + cube units; every clause generated by own code, rows re-justified) | **132/132** (U1 76, VB 23 + 6 + 27); VB's full pass over all 132 cubes ([VERIFY_N66CUBES_1118_ALL.md](../N66N20261113/cubes20261115/VERIFY_N66CUBES_1118_ALL.md); the round record is VERIFY_N66CUBES_1118.md) |
| N3 | claim `n66-le55-cubes-1118` | **CONFIRMED** by VS (04:33) and by VN (08:32: the cubes partition the split exactly, 0 double; every cert.cnf = F_c + its units byte for byte; fresh cake_lpr on `hooooo` and a random cube) ([VERIFY_N66LE55_FINAL_VN.md](../N66N20261113/cubes20261115/VERIFY_N66LE55_FINAL_VN.md)) |
| T1 | capacity rows exactly (F, 20) and (Lo, 15); supports F (84) / Lo (70); every other row rhs 1 | ok (prep_rows rc 0) |
| T2 | the rows are exactly the stated ones (base 1,020 + each round's accepted batch rows, in order) | **ok** (`rows_stated.py`: v169 = 4,642 rows, 970 appended rows from 111 batch folders over 69 rounds, no problem) |
| T3 | every appended batch audited (own encoder byte-identical CNF, fresh cake_lpr, witness cut) | **111/111 batches CERTIFIED, 970 rows** (main session's count over `audit/cuts-*/summary.json`) |
| T4 | every rhs-1 row of the final extra file has a retained CNF + LRAT with the recorded SHA-256 and a fresh `s VERIFIED UNSAT` | **1,990/1,990 rows certified**; 1,994 jobs ACCEPTED; 0 hash mismatch, 0 rejection |
| T5 | tree replay 1: `tcheck_b35` (C++, own leaf rules, `__int128`; binary `a8c4f810…`, as in VERIFY308) | **EXACT TREE**, 0 errors, 0 pending |
| T6 | tree replay 2: `pycheck_b35` (pure Python, 6 shards), compared per context with T5 | **0 differences**; verdict **EXACT TREE (tcheck_b35 + pycheck_b35)**: **8,080 contexts, 238,116,145 nodes, 119,054,033 leaves, minimum margin 1** |
| T7 | the project's trusted replay (`audit/fresh_replay_v3.py`, `check_tree` via `replay34_v2`, no receipts reused) | **EXACT TREE (fresh full replay, no receipts reused)**: 8,080/8,080 contexts, 238,116,145 nodes (= T5, T6), 119,054,034 leaves (T5 + 1, the state-0 convention), minimum margin 1, **global pending 1 = "state 0 missing" only**; 09:57-10:51 ([summary](../LO33N20261113/budget34/audit/fresh-b35s20-v169-bbs1/summary.json)) |
| T8 | single-defect controls for T5 and T6 | 24/24 as expected (VERIFY307 §4.3) |
| T9 | packet integrity: no finder on `bb-s1` during T5-T7 (the last one ended 09:30, T5 started 09:31); master `extra` = v169 (`de4bcceb…`); master contexts = ctx files = 8,080 (the original labels 0-8064 except 4782, i.e. 8,064 labels, plus the 16 new labels 8065-8080) | ok |
| T10 | "state 0 missing" is the only excluded branch | ok (T5/T6: pending is an error; T7: global pending 1, state 0) |
| F1 | threshold and equality case against the Lean statements | done (VS) |
| F2 | literature refresh before any wording outside the records; commit, push and publication | **open: the owner's decisions** |

**Equality case** (PROVED necessary condition, the analogue of ROUTE307 §1.4 one step down): an octagon-free set of 306
points in general position, if one exists, has |H| = 187, |R| = 118 and h(C) = 36, since 306 ≤ 1 + |H| + |R| ≤ 1 + 187 +
118. The lower bound ES(8) ≥ 65 is unchanged.

## 6. Controls

- **Tree checkers.** `mutation_tests_b35` has 24 controls: 21 single defects, each rejected by both T5 and T6, and 3
  valid variants (a positive control and two valid rewrites), each accepted. There is also the rehearsal of
  `final_tree_check.sh` on (18,17), which returns NOT CONFIRMED for wrongly stated demands (VERIFY307 §4.3, §4.5).
- **N66 cover.** `n66_cover_negctrl.py` (mutated certificates and a dropped cube are caught), and VN's own negative
  controls.
- **Rows.** The batch audits (each row cuts its witness), and the T4 re-certification of all 1,990 rows.
- **Early checks.** 580 and then 2,093 closed contexts passed both checkers before the end (`p307v-early2015-0316`,
  `pm1115/p307v/chain2.status`).

## 7. Files and hashes

**Tree inputs (live work directory W = `/home/jay/research/data/es308-20261114`, not in Git)**

| file | SHA-256 |
|---|---|
| catalog `inputs/source-2650.json.gz` | `8c7fe9ef52641825…` |
| `inputs/b35s20-v169/extra.json` | `de4bcceba6d0c80ce6f63cbef15822cac8300780607c738569999a7d94b81916` |
| `inputs/b35s20-v169/rows.txt` | `68fda5efe179143c…` |
| `runs/b35s20/bb-s1/master.json` | `71993a47f134ff06afa1d0029f39b7f6feceaf23bfee17b945e32329498e9dea` |
| `bb-s1/contexts.json` | `1923b8eefcd4511a…` |
| `bb-s1/master.txt` | `d2ccbbba32ea7800…` |

The packet is 8,080 `ctx-*.json.gz` files, 32 GB. The 8,064 inherited ones are hard links to `runs/b35s20/bb`, with
their hashes in `bb-s1/SUCCESSOR.json`.

**Tools**

| file | SHA-256 |
|---|---|
| `tcheck_b35` binary | `a8c4f810…` |
| `fresh_replay_v3.py` | `466aa324…` |
| `omission_tree.check_tree` | `35cb3050…` |
| `prepare_successor_b35.py` | `10fad935…` |
| `highcap_v1.py` | `1642fb3b…` |
| `continue34_v12.py` | `ab93d16f…` |
| `run_tree_v7.py` | `7bde01a9…` |
| `run_tree_v6.py` | `d6608ce9…` |
| `continue34_v11.py` | `81d2c9e2…` |

**Small outputs, copied into [data/](data/)** (SHA-256 in `data/SHA256SUMS`):
- `final_tree_check_verdict_v169.json`, `final_tree_check_inputs.sha256`, `final_tree_check_steps.log` (T1, T5, T6);
- `lrat_recheck_v169_summary.json` (T4);
- `rows_stated_v169.json` (T2);
- `n66_cover_final.json` (N1);
- `bb-s1_SUCCESSOR.json`;
- the receipts `hc169a_receipt.json`, `hc169b_receipt.json` and `s1split_receipt.json`.

**Project replay output:** `../LO33N20261113/budget34/audit/fresh-b35s20-v169-bbs1/`, with `summary.json`
(`85566fc3…`) and `contexts.jsonl`.

**Keep:**
- every ctx file of `bb` and `bb-s1`;
- the row CNF + LRAT pairs (`cuts-*`, `audit/`);
- the 132 N66 certificate directories (`/home/jay/research/data/n66-20261113/p2/c14/`, 145 GB, trim LRATs zstd);

until the owner decides otherwise.

## 8. What remains

- **The owner's decisions:** commit, push, publication, and e-mails (e.g. to Schroeder).
- **A literature refresh** before any public wording.
- **A Lean-side review of the chain.**
  - Lean-checked: the forcing step and the 2,650 catalog rows.
  - Not Lean-checked: the 1,990 other rows (1,020 coupled and 970 appended). They are CERTIFIED by cake_lpr and rest on
    the written encoder argument.
  - L5, L8, L10, L11 and L13 are outside the Lean theorem.
- **Optional:** a second full run of T7 on another machine, or by another person.

## 9. Resume

Commands: [VERIFY307 §8](../LO33N20261113/budget34/VERIFY307/README.md). In them, use
`--packet runs/b35s20/bb-s1` and `FIN=b35s20-v169`, and the project replay `fresh_replay_v3.py b35s20/bb-s1 b35s20-v169
<outdir> 3`.
