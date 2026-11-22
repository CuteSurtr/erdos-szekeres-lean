# VERIFY res118-lean: statement-fidelity review (22 Nov 2026, slot lrev)

## 1. Verdict

**CONFIRMED (statement fidelity).** `Res118.residual_bound_118_of_slices` states `ResidualBound 118` exactly. Its eleven
hypotheses have the same form as the evidence that exists today. Each one is bound to its data by sha256, none is
vacuous, and the axioms are the standard three. The same holds for `Res118.forces_304_of_slices`.

Scope of the claim:
- Correct label: **Lean-checked modulo** `N66Bound 55`, six `ResSliceExcludes` and four `BlockValid`.
  - For 304, add `ExcludesHoleBudgetZ 67`.
- No bound and no label changes. `ResidualBound 118` itself stays **PROVED (written, computer-assisted)**:
  - the hypotheses are EXACT TREE (slices), CERTIFIED plus the written encoder soundness (rows), and CERTIFIED plus the
    written model (N66);
  - none of them is Lean-checked.
- What this review did not re-run:
  - the trees, cake_lpr and the encoder;
  - the written soundness arguments (VERIFY309N (c), the N66 model), which I read but did not re-derive.
- Corrections to the worker's README are listed in §7. They are documentation slips only. None affects the Lean result.

Reviewer's work directory (the only place written): `/home/jay/research/data/formalize-20261122/res118/review`.
- One Lean compile: unit `esr-ag-lrev-ax1`, 06:56:51–06:57:14 KST, rc 0, no errors.
  - cgroup `memory.peak` 437 MB, 12 % of MemoryMax 3500M.
  - `/usr/bin/time` maximum RSS 3.45 GB. This is mostly mapped olean pages: the page cache is shared, so it is not
    charged to the unit.
  - Gates before the start: no YIELD file, Tctl 79.1 °C, and the slot was free. Another reviewer's
    `esr-ag-lrev-axioms` had already ended, so the gates opened at once and no wait was needed.
- No `lake` and no lean-lsp.
- `find -newermt 06:35` over the repo `.lake/build/lib/lean`, `build/` (chain311 and CompactChecker), `leanz/olean` and
  the worker's `olean/` found 0 files.

## 2. (4) Axioms, re-run by me (logs/audit.log)

The audit file `lean/Res118Review.lean` (sha256 `af7bd1b1…`) imports `Res118.Final`, `Res118.Compose304` and
`Res118.Adapter` from the worker's oleans. It uses the worker's LEAN_PATH, read-only.

| declaration | axioms |
|---|---|
| `residual_bound_118_of_slices`, `forces_304_of_slices`, `residual_bound_118_of_blocks`, `slice_false`, `slice_of_root`, `lo_row`, `hLo`, `hF18`, `three_hF`, `nine_mult`, `loOwners_no_cup`, `loOwners_no_cap`, `loOwners_card_le`, `five_le_column_of_cup`, `Lo_eq`, `F_eq`, `Lo_card`, `F_card`, `sum_Lo_add_sum_F`, `BlockValid.append` | propext, Classical.choice, Quot.sound |
| `nine_demands` | propext, Quot.sound |
| `rows_lengths` | none |
| the inputs `composition_304_z`, `all_rows_2650`, `holes_sum_add_population`, `zero_mem_residualOccupied`, `Partition.forces_of_population_bounds` | propext, Classical.choice, Quot.sound |
| my restatement (§3): `Rev.rev_residual_118`, `Rev.rev_304`, `Rev.excl_of_tree`, `Rev.valid_of_holds`, `Rev.S_f`, `Rev.S_lo`, the three `*_unfold` | propext, Classical.choice, Quot.sound |
| `Rev.fIdx_eq`, `Rev.loIdx_eq` (`rfl`) | none |

Hidden-assumption scan of the six worker sources and `BalancedBudgetsZ.lean` (saved in `data/rev_hidden_scan.txt`):
- No `axiom`, `sorry`, `native_decide`, `opaque`, `implemented_by`, `extern`, `unsafe`, `macro` or `notation`.
- The only options are `maxRecDepth`.
- The only instance is `DecidablePred InLo`, which does not change `Finset.filter` membership.

Shadowing check (`data/rev_shadow_check.txt`): 9,646 modules across the LEAN_PATH roots, and none is provided by two
roots.

Copies:
- `BalancedBudgetsZ.lean` is byte-identical to ES305N20261119 (`3e0651a0…`).
- Its olean `38d8f8ae…` equals FV304's `fv304-20261120/olean/BalancedBudgetsZ.olean`.

## 3. (1) The statements say what the written chain says

**Stored statements.** I printed every declaration from the oleans, not from the sources (`#check`/`#print` with
`pp.fullNames`). They match the sources:
- the main theorems' types;
- `ResSliceExcludes`, `ValidUnitRow`, `BlockValid`, `lsupp`, `F`, `Lo`, `InLo`, `loProfile`, `SliceCatalog`;
- `N66Bound`, `ResidualBound`, `ExcludesHoleBudgetZ`, `ForcesConvexNGon`, `Configuration`, `holesOf`,
  `residualOccupied`.

Every constant resolves to the intended one: `Res118.F`/`Lo`, `OmissionResidual32Bridge2650.support2650`/`demand2650`,
and `OmissionResidual32Transfer.holesOf`.

**Unfolded definitions** (kernel, `Iff.rfl`):
- `Partition.ResidualBound B ↔ ∀ n (c : Configuration n), ¬c.HasCap 6 → ¬HasConvexNGon 8 (univ.image c.point) →
  NoJunctionOn c.cup (range n) → n ≤ B`;
- `N66Bound B ↔ … ¬c.HasCap 6 → ¬c.HasCup 6 → ¬HasConvexNGon 8 … → n ≤ B`;
- `ForcesConvexNGon N k ↔ ∀ s : Finset Point, GeneralPosition s → N ≤ s.card → HasConvexNGon k s`.

So the conclusions are the library predicates that `composition_304_z` consumes, and they say what the written chain
says (ES307 §3; ROUTE307 §1.3).

**Independent restatement, kernel-checked** (`Rev`, §3 of the audit file). I wrote my own reading of the evidence:
- `TreeSystem units B T`: no 0/1 vector with `h 0 = 0`, the 2,650 base rows, `T ≤ h(F)` and `B − T ≤ h(Lo)`, every unit
  row, and `Σh ≤ B`.
  - F and Lo are literal lists that my script generated from `source-2650.json.gz` states (`s[0] ≥ 5`, `s[0] ≤ 4`).
- `RowHolds s`: the conclusion of the written encoder soundness ("an UNSAT support CNF proves that at least one support
  state is missing"), stated as `¬ supp s ⊆ residualOccupied`, with no `0 < n`.

The kernel accepts `TreeSystem → ResSliceExcludes` and `RowHolds → ValidUnitRow`. Hence it accepts:
- `Rev.rev_residual_118` (`N66Bound 55` + `RowHolds` for all block rows + the six `TreeSystem` → `ResidualBound 118`);
- `Rev.rev_304`.

So the worker's hypotheses are implied by (no stronger than) what the evidence states.

**The gluing is faithful to the written chain.**
- With h(F) ≥ 18 (L4) and h(Lo) ≥ 70 − 55 = 15 (L5 + L13), and h(C) = 154 − n ≤ 35 when n ≥ 119, the possible splits
  are exactly (18,15) at h(C) = 33, then (18,16) and (19,15) at 34, then (18,17), (19,16) and (20,15) at 35.
- (19,14) and (20,14) need h(Lo) = 14, and N66 ≤ 55 excludes that.
- No budget-32 exclusion is needed, since 18 + 15 = 33.
- The worker's finding that 6 slices suffice is correct, and the theorem compiles without the other three.
- The (18,16) slice at budget 34 keeps the chain N5-free, as in ROUTE307 §1.3.

**Lemmas.**
- `lo_row`: `70 − B ≤ (Lo \ occupied).card` from `N66Bound B`. This is bridge eq. (A) and THEORY310N Lemma A (ii).
  - It has no other premise.
  - Lo is pinned to the capacity-row list by `Lo_eq` (kernel), and that list equals my JSON list by `rfl`.
- `hF18`: the nine rows 973, 1165, …, 2315.
  - In the olean, `support2650 r` equals `constraints[r]` (dump, §4).
  - My own JSON check of those rows: demand 6, supports inside F, F covered exactly 3 times, Lo 0 times.
- `slice_of_root` has the form of `Bridge311Res.residual_of_root` plus the capacity and unit rows:
  - 154 states, mask `[(0,2)]`, which means `holes 0 = 0`;
  - `m = 2652 + rows.length`;
  - its numbering is that of `rows.txt` (`replay34.input_rows`: constraints, then extra in file order).

## 4. (2) The hypotheses have the form the evidence has, and are bound to its data

**Tree semantics** (read in `scripts/omission_tree.py`, sha `35cb3050…`; `audit/replay34*.py`; `fresh_replay_v2/v3.py`):
- Rows: `ROWS = source constraints + extra.json`, in order.
- The capacity rows are asserted to be exactly `extra[0] == (F, T)` and `extra[1] == (Lo, B − T)`, with F and Lo
  recomputed from the source states.
- `check_tree` checks 0/1 vectors with `Σh ≤ budget`, and the master budget is asserted.
- The master is wrapped under the path `((0,0),)`, which fixes state 0 occupied. Exactly one global pending leaf,
  "state 0 missing", is required.

That is `ResSliceExcludes`, provided that the unit rows have rhs 1 and the base rows are `support2650`/`demand2650`.
Both are checked below.

**My data checks** (`tools/rev_check_data.py` → `data/rev_check_data.json`, ok). Own parser of `Rows.lean` and
`LemmaA.lean`; nothing from the worker's tools.

| hypothesis | row file (sha256) | master: budget, extra, source | unit rows |
|---|---|---|---|
| `ResSliceExcludes [] 33 18` | `extra_66_55_leanrows.json` `1d6141af…` (2 rows) | inside `contexts_66_55_leanrows.tar` (`52fc93b1…`, 111 members): budget 33. Its extra path (lo33 work copy) has the same hash; its source raw hash is `e800d5f8…` | none |
| `… (P ++ Q) 34 18` | `s18-v13` `1b72eb93…` | `runs/s18/bb` `72c5a954…`: 34 | 1,020 = P ++ Q |
| `… P 34 19` | `s19` `770d276d…` | `runs/s19/bb` `1e956e2b…`: 34 | 812 = P |
| `… (P ++ Q) 35 18` | `b35s18-v13` `c9c922c0…` | `runs/b35s18/bb` `e1f3cfb9…`: 35 | 1,020 = P ++ Q |
| `… (P ++ Q ++ U) 35 19` | `b35s19-v16` `1257c4a1…` | `runs/b35s19/bb` `249497e8…`: 35 | 1,055 = P ++ Q ++ U |
| `… (P ++ Q ++ A) 35 20` | `b35s20-v169` `de4bcceb…` | `runs/b35s20/bb-s1` `71993a47…`: 35 | 1,990 = P ++ Q ++ A |

The checks above passed for every slice:
- (F, T) and (Lo, B − T), with B − T ≥ 15 (no ℕ truncation);
- every unit row has rhs 1, a sorted distinct support in range, and size ≥ 9;
- no master root branches on state 0;
- the replay summaries record EXACT TREE with min margin 1 and global pending 1 at the stated budget [R, fields read]:
  - `fresh-s18-v13`, `s19-summary` (whose `input_sha256` holds the master `1e956e2b…`), `fresh-b35s18-v13`,
    `fresh-b35s19-v16` and `fresh-b35s20-v169-bbs1`;
  - VERIFY_LO §3.1 for b33.

**Olean → JSON** (audit §4 dumps → `tools/rev_cmp_dumps.py` → `data/rev_cmp_dumps.json`, ok; COMPUTED). This
does not rely on the Lean sources. Everything below matches:
- `fIndices`, `loIndices` and the evaluated Finsets `F`, `Lo` equal the JSON F/Lo.
- `ResidualCatalog.catalog` equals the JSON `states` in order. This is the indexing that `residualOccupied` and the
  CNFs share.
- All 2,650 `(support2650 r, demand2650 r)` equal `constraints[0..2649]`.
- `rowsP/Q/U/A` equal the unit rows of s19, s18-v13, b35s19-v16 and b35s20-v169, as nested above.
- Distinct supports: 2,021 of the 2,025 block rows (|U ∩ A| = 4). The worker's count is right; LEAN_STATUS's 1,990
  undercounts H3 by the 31 rows of U outside v169.

**Row certificates** (`tools/rev_check_rows_cert.py` → `data/rev_check_rows_cert.json`). A row counts only if all of
the following hold:
- some job with its exact support is ACCEPTED;
- `sha_ok`, with recorded CNF/LRAT sha equal to the actual;
- the raw `cake/<job>.out` contains the exact line `s VERIFIED UNSAT`.

| block | covered by | result |
|---|---|---|
| P (812) | v169, b35s19-v16 and VERIFY308 tables | 812/812 |
| Q (208) | v169, b35s19-v16 and VERIFY308 | 208/208 |
| U (35) | b35s19-v16; 4 also by v169 | 35/35. The 31 rows outside v169 are covered by the b35s19-v16 table |
| A (970) | v169 | 970/970 |

The tables:

| table | sha256 | jobs | bound to |
|---|---|---|---|
| `roadmap-20261115/pm1115/p307v/lrat-b35s20-v169/lrat-results.tsv` | `a80cbba5…` | 1,994 | v169 `extra_index` → support for all rows; summary = record copy `f80a720e…` |
| `…/p307v/lrat-b35s19-v16/lrat-results.tsv` | `3b3155e9…` | 1,057 | b35s19-v16; summary = record copy `7b8d9eca…` |
| `verify308-20261114/out/lrat/lrat-results.tsv` | `8c87f057…` | 1,020 | s18-v13; same as the record copy in VERIFY308/data |

Every job binds its `extra_index` to the right support of the stated row file (saved in
`data/rev_lrat_index_binding.json`).

**Form of `BlockValid`.** `ValidUnitRow s` = for every `Configuration n` with the three predicates of `ResidualBound`,
and `0 < n`, `1 ≤ Σ_{i ∈ lsupp s} holesOf (residualOccupied) i`.
- This is demand 1, matching rhs 1.
- The `0 < n` premise only weakens the hypothesis. It is in fact equivalent here: for n = 0, `residualOccupied = ∅`
  and every support is nonempty.
- What is not checked by me: that each CNF is the encoder's CNF for its support. That is [R] from the batch audits
  (`cuts-v14/15/16 summary.json`: own encoder matches, fresh cake) and `pool_summary.json` (812 reconstructions). The
  soundness of the encoder against these Lean predicates is the written VERIFY309N (c) [R, read].

**`N66Bound 55` and `ExcludesHoleBudgetZ 67`** are the same constants that `composition_304_z` already takes. They
add no new form. Their evidence is [R] (LEAN_STATUS §4.2, §4.4).

## 5. (3) Non-vacuity

- **Each hypothesis is a closed proposition** (¬∃ over 0/1 vectors, or ∀ over configurations). The conjunction is
  consistent if each one is true, and each is certified true by its evidence (§4).
- **No trivial falsity.** Things that would make a hypothesis false outright, and do not occur:
  - an empty or out-of-range support (all have size ≥ 9 and indices < 154);
  - B − T truncated in ℕ (it never is: 15, 16, 15, 17, 16, 15);
  - a capacity row on the wrong set (kernel `rfl` to the JSON lists).
- **Positive control** (`tools/rev_realsets.py` → `data/rev_realsets.json`; HEURISTIC).
  - Test objects: seven point files were read. `witness8.txt` and `ot0000.txt` are the same file (same sha256), so there
    are six distinct 64-point sets, and the 42 charts include the duplicate's charts twice.
  - Total: 42 residual parts plus random subsets, 1,302 configurations.
  - My code re-checked every residual part in exact rationals: distinct x, no collinear triple, longest cap ≤ 5, no
    junction, largest convex polygon ≤ 7. Subsets inherit these. I did not check that the full 64-point sets are
    octagon-free; the control does not need it.
  - Result: 0 violations of the 2,650 base rows, 0 violations of any of the 2,025 block rows, and state 0 never a hole.
  - The test has some bite: 204 configurations have a block row with exactly one hole.
  - Minimum 97 holes, so all lie outside every slice (≤ 35 holes).
  - The states were computed with the Lean definitions, which I read in the sources:
    - `ResidualRanks.labels` = (6 − `ResidualRanks.rank n cup false u v`, the longest cap starting with (u,v),
      `ActualRanks.rank cup true u v` − 1, the longest cup ending with (u,v));
    - `ResidualStates.column` = the sup over u < v;
    - `ownerIndex` = `catalog.idxOf (stateList ++ [0])`;
    - `Configuration.cup` = `0 < orient`, with the same cross product that my code uses.
  - This extends VERIFY_LO §3.4, which tested only the 578 rows certified on 13 Nov.
- **Consistency with known structures.**
  - The hypotheses imply `ResidualBound 118`, and with the trees `ForcesConvexNGon 304 8`.
  - This is compatible with the largest known residual part (57 points), with the Lean-checked ES(8) ≥ 65, and with
    N66 ≥ 50 (ETV).
  - `N66Bound 70` holds by Erdős–Szekeres for cups and caps, so 55 is not trivially false.

- **`slice_of_root`.** By inspection (not Lean-checked), its premises are satisfiable and its root premise is exactly
  as strong as the slice statement.
  - `FCat` is a free binary trie: `empty | row supp dem code | node l r`. `get` follows the key's bits, lowest first, and
    a `row` leaf returns its own data. So any finite row table indexed 0..m−1 can be represented.
  - `SliceCatalog` constrains only supports and demands (no `wf`, no `code`), so it is satisfiable for every rows, B, T.
    `Bridge311Res.fcat2650` already meets its base-row half (`res_support`, `res_demand`).
  - Given `SliceCatalog`, the `FFeas` system with mask `[(0,2)]` is the `ResSliceExcludes` system. Its root premise is
    therefore equivalent to the slice statement, so it is true exactly when the tree's claim is true.
  - The main theorem does not use the adapter.

## 6. Checks of the worker's other claims

- **6 slices suffice; 2,021 distinct rows; nesting s19 = P, s18-v13 = b35s18-v13 = P ++ Q, b35s19-v16 = P ++ Q ++ U,
  b35s20-v169 = P ++ Q ++ A:** all confirmed by my own code.
- **LEAN_STATUS §7 cost slip** (HEURISTIC arithmetic): confirmed.
  - 143,447,786 leaves × 0.0185–0.0253 s = 2.65–3.63 M s, which is 737–1,008 CPU-h, not 2,650–3,630.
  - The 303 row: 123,166,799 leaves gives 633–866 CPU-h.
  - The worker's six-slice figure: 127,875,211 leaves gives 657–899 CPU-h.
- **Negative controls:**
  - `BadGlue` differs from the real proof only in budget 34 for (20,15), and `omega` rejects it.
  - `BadLo` is rejected by `decide`.

## 7. Corrections to the worker's README (documentation only; no effect on the Lean result)

1. §4 says that s19's "summary records no master hash". In fact `audit/s19-summary.json` → `input_sha256` holds
   `runs/s19/bb/master.json: 1e956e2b…`. The binding is direct, not only via VERIFY308.
2. §4/§8.6 cite "`export_es304z.py:459` asserts `m.bit_length() == 12`". The assertion is at `export_es310.py:459`;
   `export_es304z.py` (138 lines) reuses `export_es310.export_context` unchanged. The substance is right: 4,642 rows
   need 13 bits.
3. Bind the three per-job LRAT tables of §4 above by sha256 in README §4. The record copy of the v169 summary does not
   name its row file; the support-level binding lives in these work-directory tables and their `cake/*.out` files.
   - Add them to the keep-set for vQ/vU/vA: `pm1115/p307v/lrat-b35s20-v169/`, `pm1115/p307v/lrat-b35s19-v16/` and
     `verify308-20261114/out/lrat/`.
4. §4 "b33s18 … Nothing inside the tar was checked here". This review checked that `master.json` inside the tar has
   budget 33, an extra file with hash `1d6141af…` and source hash `e800d5f8…`. Optional.
5. §4 credits the `s34_18` replay to `fresh_replay_v3`. The `tool_sha256` in `audit/fresh-s18-v13/summary.json`,
   `ef0fe84d…`, is that of `audit/fresh_replay_v2.py` (budget fixed at 34; the same `check_tree`). The substance is
   unchanged.

## 8. Files (review/)

- `VERIFY_res118-lean_fidelity.md` (this file) and `README.md`.
- `lean/Res118Review.lean` `af7bd1b1…`.
- `logs/audit.log` `f21293e9…`, `logs/audit.time`, `logs/audit.meta` (rc 0, peak 436,555,776 B).
- Tools and their outputs:

| tool | output |
|---|---|
| `tools/rev_check_data.py` `30bda7e0…` | `data/rev_check_data.json` `aac5b7c2…` |
| `tools/rev_check_rows_cert.py` `6bda7e5f…` | `data/rev_check_rows_cert.json` `487f5de4…` |
| `tools/rev_cmp_dumps.py` `5b50f6bb…` | `data/rev_cmp_dumps.json` `8d98da9d…` |
| `tools/rev_realsets.py` `23dc233e…` | `data/rev_realsets.json` `c8cbe914…` |
| (inline) | `data/rev_shadow_check.txt`, `data/rev_lrat_index_binding.json`, `data/rev_hidden_scan.txt` |

- `tools/run_audit.sh` and `tools/start_unit.sh` (gates: YIELD, Tctl < 86 °C, no active `esr-ag-lrev-*`).
- Resume:

```bash
cd /home/jay/research/data/formalize-20261122/res118/review
python3 -I tools/rev_check_data.py data/rev_check_data.json
python3 -I tools/rev_check_rows_cert.py data/rev_check_rows_cert.json
python3 -I tools/rev_realsets.py data/rev_realsets.json 30
tools/start_unit.sh ax1 60 /bin/bash $PWD/tools/run_audit.sh && python3 -I tools/rev_cmp_dumps.py data/rev_cmp_dumps.json
```
