# ES304N20261119: ES(8) ≤ 304 (computer-assisted, unrefereed; 19 November 2026)

> **Retention update (25 Nov 2026, owner):** asked whether FV304 (the Lean check `E304Z.Final.excludes_67`, standard
> axioms, closing audit in FORMAL20261122/fv304-audit) may count as the independent check named in section 4, the
> owner answered "delete unnecessary files please". So the finder's raw contexts `zrow/b67/occ/ctx-*.json.gz` and
> `zrow/b67/mis/ctx-*.json.gz` (8,192 files, 8.76 GB) are deleted after `receipts/b67_finder_contexts_20261125.tsv`
> (path, size and SHA-256 of each file) is pushed, with the guarded `verify-20261124/delete_proofs.py`. Kept: `files/`
> (the 8,192 assembled files, FV304's input and check B's), both pinned `master.json`, `contexts.json`, `master.txt`,
> `fastbb.log.jsonl`, `occ.out`, `mis.out`. Lost: re-running check A exactly as recorded (assembly from the finder
> output); check B and FV304 still run from `files/`. ES(8) <= 304 is superseded by ES(8) <= 302 (ES302N20261124).

**Status (20:55 KST).** ES(8) ≤ 304. The balanced budget-67 tree is an **EXACT TREE**, checked by two
implementations (§3). Together with N66 ≤ 55 (CERTIFIED) and the residual half of ES(8) ≤ 307, this gives the bound.
- Lean checks everything except those three computational inputs:
  `OmissionBalancedZ.composition_304_z : ExcludesHoleBudgetZ 67 → N66Bound 55 → ResidualBound 118 →
  ForcesConvexNGon 304 8` (ES305N20261119/BalancedBudgetsZ.lean). Standard axioms only.
- Not refereed, not committed. No independent re-check by another person or agent yet.

**Every 304-point set in general position contains 8 points in convex position.** The previous bound was 305
(ES305N20261119, 17:42 today).

## 1. Statement and method

ES(8) ≤ 304. The model, Lemma Z (PROVED, and a Lean theorem), the rows, the Lean composition and every tool are those
of ES305N20261119 (§2–§5 there). Only the balanced budget changes, from 66 to 67:
- no 0/1 vector on the 252 states with at most 67 holes satisfies the 3,131 catalog rows and the Z-row;
- hence 252 − |H| ≥ 68, i.e. **BalancedBound 184**, and 184 + 118 + 2 = 304.

## 2. Inputs

| input | label | source |
|---|---|---|
| `ExcludesHoleBudgetZ 67` | EXACT TREE (two implementations) | §3 |
| `N66Bound 55` | CERTIFIED (cake_lpr) | N66N20261113 |
| `ResidualBound 118` | as in ES(8) ≤ 307 | ES307N20261118 |
| composition | Lean, standard axioms | `composition_304_z` (ES305N20261119/BalancedBudgetsZ.lean); `Composition304.lean` here |

## 3. The budget-67 tree (EXACT TREE)

- **Finder.** `zb_run.sh 67 12 4096` (unit `esr-bal-zb67`, 12 threads). Work dir
  `/home/jay/research/data/bal186-20261119/zrow/b67`, 17 GB.
  - Zero side (state 0 occupied; `balz.rows`, budget 67): 17:42–19:37, rc 0, no witness. 4,096 contexts,
    13,724,576 nodes; the largest context has 63,569 nodes.
  - One side (state 0 missing; `balz_m0.rows`, budget 66): 19:37–20:45, rc 0, no witness. 4,096 contexts,
    8,149,414 nodes; the largest context has 17,939 nodes.
- **Check A** (`balz_assemble.py` v2 plus `scripts/omission_tree.check_tree` on every file; original rows plus the
  Z-row at budget 67; pending == path length): **EXACT TREE**.
  - 8,192 files, 21,873,990 nodes, 10,941,091 leaves, minimum margin 1, no bad file. 20:45–20:49.
- **Check B** (`balcheck`, own C++, the Z-row via `BALCHECK_EXTRA_ROWS`): **"EXACT TREE (balcheck)"**.
  - 8,192 contexts, 0 failed, the same nodes and leaves, minimum margin 1.
  - The cover is **complete**: the 8,192 paths are the leaves of one complete binary decision tree. 20:49–20:53.
- The node counts agree: 13,724,576 + 8,149,414 = 21,873,990 in both checks.
- **Conclusion: `ExcludesHoleBudgetZ 67`.** The Lean rows are the JSON rows, checked by
  ES305N20261119/tools/rows_match.py, and the Z-row support is `OmissionZRow.zIndices` (`Z_eq`).
- Cost and the Knuth estimate: the zero side was 3.0× its dive estimate (`dz_b67`: 4.5e6). For budget 66 it was
  2.6×.

## 4. Files and hashes

| file | SHA-256 |
|---|---|
| `Composition304.lean` (here; `lake env lean` rc 0, standard axioms) | `a58df4a713d6c37247f9930accbf46d7f9dd31db351bf463b21ff8150f34fe96` |
| `b67/occ/master.json` | `607609f72bf8e7786b6d8c407879f362b0e380a196f41be4da24704d931f14d3` |
| `b67/mis/master.json` | `b8fa7b5333960f6fa1a0962d8fa635d8ad872349739596260941bff862300af7` |
| `b67/files/summary.json` (check A) | `194211b267558d00c30bb97ba1443cfce9aa1b421c87e57bb19d54e84d3d4711` |
| `b67/balcheck.json` (check B) | `1da669bce11ac115d33fb898912f076d73d0d4841dda709dfa4ccf09b92c19c5` |
| `b67/balcheck.tsv` (8,192 rows, all ok) | `05beb660ae9df54e54b557a8a54ce949f85af5fe118173c0bd2c84c1b7a81315` |

All shared tools and inputs (rows, Z-row, finder, assembler v2, balcheck, Lean files): ES305N20261119 §7. The tree
files (8,192 assembled `.json.gz`, plus the finder's contexts) are kept until an independent check.

## 5. What remains

- An independent re-check (another reader or agent): both checks re-run, Lemma Z.
- A literature check before any public wording: the quick re-check of 19 Nov 19:50 found nothing new
  (ES305N20261119 §8). The last full check is NOVELTY20261113B.
- **Budget 68 (gives 303), running.** Zero side only, which is enough by `FixedStatesZ.zero_mem_occupied`
  (ES305N20261119 §5b).
  - The owner gave the OK about 20:15, for 14 threads.
  - Unit `esr-bal-zb68` (`zb_run0.sh 68 14 16384`, dir `zrow/b68z`) started at 20:53:41 through `esr-bal-chain68`.
  - HEURISTIC estimate about 23 h, plus about 3 h of checks, about 120 GB.

## 6. Resume

```bash
cd /home/jay/research/data/bal186-20261119/zrow
./zb_check.sh 67 12          # re-run assembly + check_tree + balcheck on the kept packets
./zb_run0.sh 68 14 16384     # budget 68 (resumable: rerun with the same arguments)
```
