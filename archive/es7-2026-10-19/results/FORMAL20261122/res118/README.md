# res118-lean: ResidualBound 118 as a Lean theorem modulo explicit hypotheses (22 Nov 2026)

## 1. Headline

- **`Res118.residual_bound_118_of_slices`: `ResidualBound 118` is Lean-checked modulo explicit hypotheses**, with
  only `propext`, `Classical.choice` and `Quot.sound`. The hypotheses are:
  - `N66Bound 55`;
  - six slice exclusions `ResSliceExcludes`, which are EXACT TREE today;
  - the validity of four blocks of unit rows `BlockValid`, which are CERTIFIED CNFs plus a written encoder argument
    today.
- **Now Lean-checked** (they were written steps before):
  - Lemma A, Lo half: h(Lo) ≥ 70 − N66;
  - h(F) ≥ 18 from the nine base rows;
  - the identity |R| + h(C) = 154 together with the gluing of the six splits.
- **`Res118.forces_304_of_slices`: ES(8) ≤ 304 is Lean-checked modulo** `ExcludesHoleBudgetZ 67` (FV304 is checking it
  now), `N66Bound 55`, the six slices and the four row blocks. Standard axioms.
- **No bound and no label changes.**
  - `ResidualBound 118` itself stays **PROVED (written, computer-assisted)**.
  - The trees, the 2,021 extra rows and N66 ≤ 55 are still outside Lean, as hypotheses.
  - Nothing was committed. No command wrote into the repository or into an existing olean store: at 06:26,
    `find -newermt '2026-11-22 05:45'` gave 0 files in the repo `.lake/build/lib/lean`, every
    `.lake/packages/*/.lake/build/lib/lean`, `chain311/olean`, `build/CompactChecker` and `leanz/olean`.
- **No gap was found in the formalised steps** (L4, Lemma A's Lo half, the identity and the gluing): they compiled as
  written. I did not re-read the encoder soundness argument, the N66 model or the tree semantics. The findings are
  about scope (§8):
  - Under `N66Bound 55` the task's slices (19,14) and (20,14), and the budget-32 exclusion, are not needed.
  - The extra rows used are **2,021**, not 1,990.

Work directory, the only place written: `/home/jay/research/data/formalize-20261122/res118`.
- Everything ran 05:50–06:30 KST, in units `esr-ag-lres-*` (CPUQuota 100 %, MemoryMax 3500M, MemorySwapMax 0).
- No `lake` and no lean-lsp were used.

## 2. Statement (Lean, `lean/Res118/Final.lean`)

```lean
theorem Res118.residual_bound_118_of_slices
    (n66 : OmissionZRow.N66Bound 55)
    (vP : BlockValid rowsP) (vQ : BlockValid rowsQ) (vU : BlockValid rowsU) (vA : BlockValid rowsA)
    (s33_18 : ResSliceExcludes [] 33 18)
    (s34_18 : ResSliceExcludes (rowsP ++ rowsQ) 34 18)
    (s34_19 : ResSliceExcludes rowsP 34 19)
    (s35_18 : ResSliceExcludes (rowsP ++ rowsQ) 35 18)
    (s35_19 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsU) 35 19)
    (s35_20 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118
```

The definitions are in `lean/Res118/Glue.lean`. Nothing asserts them.

```lean
def lsupp (s : List ℕ) : Finset (Fin 154) := Finset.univ.filter (fun i : Fin 154 => i.val ∈ s)   -- = CompactChecker.fsupp
def ValidUnitRow (s : List ℕ) : Prop :=
  ∀ n, ∀ c : Configuration n, ∀ (noCap : ¬ c.HasCap 6) (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)), 0 < n →
      1 ≤ ∑ i ∈ lsupp s, holesOf (c.residualOccupied noCap noOctagon noJunction) i
def BlockValid (rows : List (List ℕ)) : Prop := ∀ s ∈ rows, ValidUnitRow s
def ResSliceExcludes (rows : List (List ℕ)) (B T : ℕ) : Prop :=
  ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
    (∀ r, demand2650 r ≤ ∑ i ∈ support2650 r, holes i) ∧
    T ≤ ∑ i ∈ F, holes i ∧ B - T ≤ ∑ i ∈ Lo, holes i ∧
    (∀ s ∈ rows, 1 ≤ ∑ i ∈ lsupp s, holes i) ∧ (∑ i, holes i) ≤ B
```

How to read the definitions:

- **`ResSliceExcludes`** is the statement a slice tree proves. It has the shape of `Excludes2650Zero` (Residual32Bridge2650/Rows.lean)
  plus the slice's extra rows, in the order of its row file:
  - rows 0..2649 are `support2650`/`demand2650`;
  - row 2650 is the capacity row (F, T) and row 2651 is (Lo, B − T);
  - rows 2652 + j are the unit rows.
  - State 0 is occupied (`holes 0 = 0`). That is the root path `(0,0)` of every slice packet; `zero_mem_residualOccupied`
    discharges "state 0 missing".
- **`F` and `Lo`** are defined from the Lean residual catalog: f₁ ≥ 5 and f₁ ≤ 4. `F_eq` and `Lo_eq` (`decide +kernel`) pin them to the
  literal supports of the capacity rows.
- **`rowsP` (812), `rowsQ` (208), `rowsU` (35) and `rowsA` (970)** are literal supports. They are generated from the row files
  (`lean/Res118/Rows.lean`) and pinned by `rows_lengths`.
- **`ValidUnitRow`** has the premise `0 < n`, which makes the hypothesis weaker: it speaks only about actual nonempty
  residual configurations, as the evidence does. All extra rows have demand 1 (asserted by `tools/gen_rows.py`).

Corollary (`lean/Res118/Compose304.lean`): `Res118.forces_304_of_slices`.
- It takes `ExcludesHoleBudgetZ 67`, `N66Bound 55` and the same ten hypotheses, and concludes `ForcesConvexNGon 304 8`.
  The proof is `OmissionBalancedZ.composition_304_z trees n66 (residual_bound_118_of_slices …)`.
- `BalancedBudgetsZ.lean` was compiled here from a byte-identical copy (sha256 `3e0651a0…`).
- The olean it produced, `38d8f8ae…`, is **byte-identical to FV304's** `fv304-20261120/olean/BalancedBudgetsZ.olean`.

Compact-checker form (`lean/Res118/Adapter.lean`), the mirror of `Bridge311Res.residual_of_root` and FV304's
`BridgeZ.balanced_z_of_root`:

```lean
structure SliceCatalog (cat : FCat) (rows : List (List ℕ)) (B T : ℕ) : Prop where
  base_supp : ∀ r : Fin 2650, fsupp cat 154 r.val = support2650 r
  base_dem  : ∀ r : Fin 2650, cat.dem r.val = demand2650 r
  f_supp : fsupp cat 154 2650 = F      f_dem : cat.dem 2650 = T
  lo_supp : fsupp cat 154 2651 = Lo    lo_dem : cat.dem 2651 = B - T
  unit_supp : ∀ j (hj : j < rows.length), (cat.get (2652 + j)).1 = rows[j]
  unit_dem : ∀ j, j < rows.length → cat.dem (2652 + j) = 1
theorem slice_of_root (hc : SliceCatalog cat rows B T)
    (h : ¬ ∃ holes : Fin 154 → ℕ, FFeas cat (2652 + rows.length) 154 B (pmask (zerosF 154) [(0, 2)]) holes) :
    ResSliceExcludes rows B T
```

## 3. Model and soundness: the written chain, link by link

| written step | where it is written | Lean now | status |
|---|---|---|---|
| \|S\| ≤ 1 + \|H\| + \|R\|, forcing | ES307 §3 item 1 and item 4; ROUTE307 §1.2 L1 | `Partition.forces_of_population_bounds`, inside `composition_304_z` | Lean (library) |
| 2,650 rows, \|R\| + h(C) = 154, h₀ = 0 | ROUTE307 §1.2 L3; bridge §2 | `all_rows_2650`, `holes_sum_add_population`, `zero_mem_residualOccupied` (chain311), used in `slice_false` and `residual_bound_118_of_blocks` | Lean (existing) |
| F/Lo partition (84 + 70) | ROUTE307 §1.1; VERIFY_LO §2.5 | `F_eq`, `Lo_eq`, `F_card`, `Lo_card`, `sum_Lo_add_sum_F` | **Lean, new** |
| **L4**: h(F) ≥ 18 from rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315 (demand 6; F covered 3 times) | ROUTE307 §1.2 L4; bridge §3 "Baseline 309" (lines 68–74); VERIFY_LO §2.4 | `nine_demands`, `nine_mult` (one `decide +kernel` over the 154 states), `three_hF`, `hF18` | **Lean, new** (was PROVED arithmetic) |
| **L5, Lemma A (Lo half)**: Lo owners have no 6-cup (the last point of a 6-cup has f₁ ≥ 5) and no 6-cap, so h(Lo) ≥ 70 − N66 | THEORY310N §2 Lemma A (ii) (lines 65–91); bridge §2 eq. (A) (line 49); VERIFY_LO §2.6; THEORY310N §6 item 4 (lines 349–363) | `five_le_column_of_cup`, `loOwners_no_cup`, `loOwners_no_cap`, `loOwners_card_le`, `lo_row : N66Bound B → 70 − B ≤ (Lo \ occupied).card`, `hLo` | **Lean, new** (was PROVED, written), for general B |
| gluing: h(F) ≥ 18 and h(Lo) ≥ 15 leave exactly six splits with h(C) ≤ 35, each excluded, so h(C) ≥ 36 and \|R\| ≤ 118 | ES307 §3 items 2–3; ROUTE307 §1.2 (slice semantics, line 71) and §1.3 items 1–4 | `slice_false`, `residual_bound_118_of_blocks` | **Lean, new** (was PROVED, written) |
| the six slice trees | L7, L9, L10, L11 | hypotheses `s33_18` … `s35_20` | EXACT TREE (§4) |
| the extra rows (coupled and appended) | L8, ES307 T3–T4, VERIFY307 T4 | hypotheses `vP`, `vQ`, `vU`, `vA` | CERTIFIED + written encoder soundness (§4) |
| N66 ≤ 55 | L13 | hypothesis `n66` | CERTIFIED + PROVED written model [R] |

Lemma A(i) is not formalised here: F owners have no 5-cap, so h(F) ≥ 84 − N5. The chain is N5-free and does not
need it.

## 4. The hypotheses: data, evidence today, and what a later run must prove

Each slice hypothesis below is bound to its row file and packet. The data are in `data/rows_manifest.json`,
`data/check_rows.json` and `data/evidence.json`.
- **s18, b35s18, b35s19 and b35s20** pass every check: the master hash equals the replay summary's, the ctx-file count
  equals the master's and the receipts', the extra-file hash equals the summary's, and three ctx files match their
  replay receipts.
- **s19:** its summary records no master hash. The extra hash, the count and the three-file spot check against
  `s19-contexts.jsonl` pass. The master hash `1e956e2b…` equals the one in VERIFY308 §5 (README line 140).
- **b33s18** is a tar. Only file hashes were compared: the repo copy equals the work copy, and both equal the hashes
  in VERIFY_LO §3.1 and its `verify_stream.out`. Nothing inside the tar was checked here.

| hypothesis | slice (B; F, Lo) | row file (sha256) | packet / tree (sha256) | evidence today |
|---|---|---|---|---|
| `s33_18 : ResSliceExcludes [] 33 18` | 33; 18, 15 | `LO33N20261113/data/cert_66_55_leanrows/extra_66_55_leanrows.json` `1d6141afc91e3a4a…` (2 capacity rows only) | `contexts_66_55_leanrows.tar` `52fc93b18eb0c165…`; `verify_stream.out` `7b88742cf8457d18…` (repo copy = W copy) | **EXACT TREE** over the Lean rows alone: 110 contexts, 3,815 nodes, 1,908 leaves, minimum margin 1, only "state 0 missing" pending (VERIFY_LO §3.1, independent replay) [R + D: hashes] |
| `s34_18 : ResSliceExcludes (P ++ Q) 34 18` | 34; 18, 16 | `es308/inputs/s18-v13/extra.json` `1b72eb934e00c7f5…` | `runs/s18/bb` master `72c5a954820f6880…`, 4,296 ctx | **EXACT TREE**: fresh_replay_v3, 45,833 nodes, 20,770 leaves, min margin 1; VERIFY308 tcheck + pycheck [R + D] |
| `s34_19 : ResSliceExcludes P 34 19` | 34; 19, 15 | `es308/inputs/s19/extra.json` `770d276db7b51d36…` | `runs/s19/bb` master `1e956e2b60891f38…`, 3,643 ctx | **EXACT TREE**: `audit/s19-summary.json`, 1,658,483 nodes, 829,242 leaves, min margin 1; VERIFY308 [R + D] |
| `s35_18 : ResSliceExcludes (P ++ Q) 35 18` | 35; 18, 17 | `es308/inputs/b35s18-v13/extra.json` `c9c922c0a113c78e…` | `runs/b35s18/bb` master `e1f3cfb9570ec360…`, 4,838 ctx | **EXACT TREE**: fresh_replay_v3 (416,935 nodes, 206,050 leaves) + VERIFY308 tcheck_b35 + pycheck_b35 (VB CONFIRMED) [R + D] |
| `s35_19 : ResSliceExcludes (P ++ Q ++ U) 35 19` | 35; 19, 16 | `es308/inputs/b35s19-v16/extra.json` `1257c4a15a52d894…` | `runs/b35s19/bb` master `249497e821641bd3…`, 7,170 ctx | **EXACT TREE**: fresh_replay_v3 (15,533,581 nodes, 7,763,207 leaves) + tcheck_b35 + pycheck_b35 [R + D] |
| `s35_20 : ResSliceExcludes (P ++ Q ++ A) 35 20` | 35; 20, 15 | `es308/inputs/b35s20-v169/extra.json` `de4bcceba6d0c80c…` | `runs/b35s20/bb-s1` master `71993a47f134ff06…`, 8,080 ctx | **EXACT TREE by three implementations** (ES307 T5–T7: 238,116,145 nodes, 119,054,034 leaves, min margin 1) [R + D] |

Row blocks:
- The six row files nest exactly (`tools/row_blocks.py`, asserted):
  - s19 = P;
  - s18-v13 = b35s18-v13 = P ++ Q;
  - b35s19-v16 = P ++ Q ++ U;
  - b35s20-v169 = P ++ Q ++ A.
- The 2,025 block rows hold 2,021 distinct supports, because U ∩ A = 4 rows.
- In the hypotheses `vP`, `vQ`, `vU` and `vA`, each row means: for every actual nonempty residual configuration (as in
  `ResidualBound`), at least one state of the support is unoccupied.

| hypothesis | rows | sources | evidence today |
|---|---|---|---|
| `vP : BlockValid rowsP` | 812 (the pool) | `inputs/pool812.json` `91a4e36f…`, equal in order to P | **CERTIFIED**: `audit/pool_summary.json` (`018d0003…`): 812 own-encoder reconstructions, 812 retained LRATs, exact `s VERIFIED UNSAT`; ES307 T4 again. Plus the **written encoder soundness** (VERIFY309N link (c)) [R] |
| `vQ : BlockValid rowsQ` | 208 (128 `cuts-near9` + 80 `cuts-v2`…`v13`) | rows 813–1020 of the 1,020 coupled rows | **CERTIFIED**: VERIFY308 re-ran 1,020/1,020; ES307 T4. Plus the written encoder soundness [R] |
| `vU : BlockValid rowsU` | 35 (`cuts-v14/v15/v16`, 11 + 13 + 11) | b35s19-v16 rows 1021–1055 | **CERTIFIED**: the batch audits cuts-v14/15/16 (own encoder = CNF hash, fresh cake_lpr; VERIFY_P307_CHAIN); VERIFY307 T4 on b35s19-v16, 1,055/1,055 rows, 1,057 jobs ACCEPTED (`VERIFY307/data/lrat-b35s19-v16/lrat-summary.json` `7b8d9eca…`). **31 of these 35 rows are not in v169**, so ES307's T4 (1,990 rows) does not cover them. Plus the written encoder soundness [R] |
| `vA : BlockValid rowsA` | 970 appended rows (111 batches, 69 rounds) | b35s20-v169 rows 1021–1990 | **CERTIFIED**: ES307 T3 111/111 batches; T4 1,990/1,990 rows, 1,994 jobs ACCEPTED (`ES307N20261118/data/lrat_recheck_v169_summary.json` `f80a720e…`). Plus the written encoder soundness [R] |
| `n66 : N66Bound 55` | – | N66N20261113, cubes20261115 | **CERTIFIED** (132 cubes, cover complete) + PROVED written model; claim `n66-le55-cubes-1118` CONFIRMED by VS and VN [R, not re-read here] |

The `[R]` items were read from records and not re-run. `[D]` means I recomputed the hashes, counts and replay fields
on disk (`tools/bind_evidence.py`).

What a later run must prove to remove each hypothesis:
- **Slices: a compact-checker run per slice.**
  - The run proves `¬ ∃ holes, FFeas cat (2652 + rows.length) 154 B (pmask (zerosF 154) [(0, 2)]) holes` for a
    catalog `cat` with `SliceCatalog cat rows B T`. `Res118.slice_of_root` then gives the slice hypothesis exactly.
  - The identities in `SliceCatalog` are the run's own obligation, for example `decide +kernel` as in Bridge311Res.
    Not built here: `fcat2650_wf` peaked at 6.7 GB cgroup and Bridge311Res at 3.2 GB, both above this slot's cap.
  - Exporter changes needed:
    - 154 states, mask `[(0, 2)]`, budgets 33/34/35;
    - catalogs of 2,652–4,642 rows. `export_es304z.py:459` asserts `m.bit_length() == 12`, but b35s20 has 4,642
      rows, which needs 13 bits.
  - Size: about 127.9 M leaves (1,908 + 20,770 + 829,242 + 206,050 + 7,763,207 + 119,054,034).
    - At FV304's 0.0185–0.0253 s per leaf that is about **660–900 CPU-h** (HEURISTIC; the per-leaf cost on residual
      trees is unmeasured).
    - Disk: about 310 GB of oleans and 240 GB of sources.
- **Rows: an encoder formalisation** (the ENCBLEAN pattern).
  - Needed: a Lean model of RES33N `coupled.py` proved sound against `Configuration`, hash binding of the CNF texts,
    and the cake_lpr verdicts.
  - That would make `ValidUnitRow s` Lean-checked modulo verdicts for all 2,021 supports.
  - Whether `coupled.py`'s clause families match `ErdosSzekeres.Omission.Coupled` is not checked (LEAN_STATUS §10).
- **N66: an N66 encoder.** Out of scope here (LEAN_STATUS §7).

## 5. Results

All modules compile with the bare `~/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1`. The `#print axioms`
lines are in `logs/*.log`.

| module | theorems | axioms | cgroup peak / time |
|---|---|---|---|
| `Res118.Rows` (data, core only) | `rowsP/Q/U/A` | – | b1: 877.8 MB for Rows + LemmaA; 13 s |
| `Res118.LemmaA` | `Lo_eq`, `F_eq`, `Lo_card`, `F_card`, `sum_Lo_add_sum_F`, `loOwners_no_cup`, `loOwners_no_cap`, `lo_row` | propext, Classical.choice, Quot.sound | 8 s |
| `Res118.Glue` | `nine_mult`, `three_hF`, `hF18`, `hLo`, `slice_false`, `residual_bound_118_of_blocks` | standard; `nine_demands`: [propext, Quot.sound] | b2: 1.4 GB; 15 s |
| `Res118.Final` | `rows_lengths` (no axioms), **`residual_bound_118_of_slices`** | standard | b3: 416.8 MB; 4 s |
| `Res118.Adapter` | `slice_of_root` | standard | 2 s |
| `BalancedBudgetsZ` (copy) | `feasible_holes_z`, `composition_305_z`, `composition_304_z` | standard | b4: 348 MB; 3 s |
| `Res118.Compose304` | **`forces_304_of_slices`** | standard | 4 s |

- `/usr/bin/time -v` maximum RSS was 0.8–4.4 GB per module. It is mostly mapped olean pages; the cgroup peaks above
  are the binding numbers, all below 2,800 MB (80 % of MemoryMax).
- Glue, LemmaA, Adapter and Compose304 compiled at the first attempt.
- Final first failed in `rows_lengths` (`decide` hit maxRecDepth). It passed with `decide +kernel`.

## 6. Controls

- **Lean negative controls** (`controls/run_controls.sh`, unit `esr-ag-lres-ctl1`). Both files are rejected as expected.
  - `BadLo.lean`: Lo pinned to a wrong list (120 replaced by 121). Rejected with "Tactic `decide` proved that the
    proposition … is false".
  - `BadGlue.lean`: the same proof as `residual_bound_118_of_blocks`, with the (20,15) hypothesis weakened to budget
    34. Rejected by `omega` at the budget goal of the (20,15) branch (line 38). The gluing really needs the budget-35
    (20,15) slice.
- **Data binding** (`tools/check_rows.py`, an own parser independent of `gen_rows.py`).
  - Checked: every slice's capacity rows equal (fIndices, T) and (loIndices, B − T), as parsed from LemmaA.lean; its unit
    rows equal the block concatenation in file order; and the nine L4 rows cover F exactly three times (recounted from
    the JSON). Result `ok`.
  - Four mutated copies were each rejected (rc 1): one entry +1, a dropped row, two rows swapped, a wrong fIndices
    entry (`controls/data/*.out`).
- **Base rows** (`tools/check_base_rows.py`, own parser).
  - The 2,650 rows of chain311's `Residual32Bridge2650/Catalog.lean` (sha256 `5b97f861…`) equal `constraints[0..2649]`
    of `source-2650.json.gz` in order, as sets and demands. The raw sha256 is `e800d5f8…`, which is also the hash
    recorded in the Lean comment.
  - That source hash is the `src_sha256` of the `build.tsv` row whose olean hash `4fe35a09…` is the olean on disk. So
    JSON → source → olean is bound.
- **Resume test** (06:26, unit `esr-ag-lres-b5`, cgroup 1.3 GB). The §9 commands were run as written: regenerate,
  three checks, a rebuild of all seven modules, and controls `ctl2`.
  - **Every olean reproduced byte for byte** (`data/olean_sha256_{before,after}_resume.txt`), with the same axiom lines.
  - The controls were again rejected as expected.
- **Olean pins.** The directly imported chain311 oleans match their last `ok` row of `build/chain311/build.tsv`:
  Residual32Bridge2650.{Catalog, Matches, Rows}, ZeroState, Transfer, BalancedRows, BalancedCoverCutsV2. `LemmaZ.olean`
  is `ef249ba1…` (= ES305 §7 per LEAN_STATUS).

## 7. Files and hashes

Lean sources (`lean/`):

| file | sha256 |
|---|---|
| `Res118/Rows.lean` (generated) | `d19bbdbd252441324d36e60bd34801a2d7f4b52025a831b802790b01a34e41a8` |
| `Res118/LemmaA.lean` | `dea2773271e556bbfbbf5d1cf27c2ab0dbf7b8f2e98dfd24a163cfc6bd083a85` |
| `Res118/Glue.lean` | `50f9d6c10691f8376edea80f67b1e2ac0e5384718ec4c5017e2e6f7c3ab13a29` |
| `Res118/Final.lean` | `7f9198b7660c2ff6329fe5ac3a640b1efa0e09d68f60b65c263cb3cc2713d83b` |
| `Res118/Adapter.lean` | `04f1e18ae6fc2d8cf29e9058d233b58d41edf00c0da5a679953154f929f0ebe3` |
| `Res118/Compose304.lean` | `e8040287f5be312858f6a625f9b9685627ba0e366c1cb9abbab7161f2b87b699` |
| `BalancedBudgetsZ.lean` (copy of ES305N20261119) | `3e0651a023a58df5a9a0fff4c7d0fc1c5859dfe40b67e9a4e17cdc313224ab1a` |

Oleans (`olean/`):

| olean | sha256 |
|---|---|
| Res118.Rows | `7d8fa1d2…` |
| Res118.LemmaA | `135216d0…` |
| Res118.Glue | `64b1888f…` |
| Res118.Final | `0d325186…` |
| Res118.Adapter | `70e2e0ef…` |
| Res118.Compose304 | `64af03ba…` |
| BalancedBudgetsZ | `38d8f8ae…` |

`LEAN_PATH`, read-only (`tools/build.sh`):
- repo `.lake/build/lib/lean` and `.lake/packages/*/.lake/build/lib/lean`;
- the toolchain `lib/lean`;
- `experiments/omission-compact-checker-2026-11-05/build/chain311/olean`;
- `bal186-20261119/zrow/leanz/olean` (LemmaZ);
- this directory's `olean/`.

**Disclosure.** `olean/CompactChecker/{Packed,Fast,WordPack,Split,Fast2,Path}.olean` are symlinks into the existing
store `experiments/omission-compact-checker-2026-11-05/build/CompactChecker/`, as FV304 does. That store is not in the
task's list. Only `Res118.Adapter` imports them.

| olean | sha256 |
|---|---|
| Packed | `d0186d83…` |
| Fast | `1e55d4aa…` |
| WordPack | `bbd6dbe5…` |
| Split | `9d6e752b…` |
| Fast2 | `14ce7ba1…` |
| Path | `c0e64d18…` (= `hardcap-rebuild.tsv`) |

Tools (`tools/`):
- `slice_inputs.py`, `row_blocks.py`, `gen_rows.py` (writes `Rows.lean` and `data/rows_manifest.json`), `check_rows.py`,
  `check_base_rows.py` and `bind_evidence.py` (writes `data/evidence.json`). All are read-only on their inputs and run
  with `python3 -I`.
- `build.sh` and `start_unit.sh` (gates: no YIELD file, Tctl < 86 °C, no other `esr-ag-lres-*` unit active).

Data (`data/`): `slice_inputs.json`, `rows_manifest.json`, `check_rows.json`, `check_base_rows.json`, `evidence.json`.

Inputs, read-only (sha256 of the uncompressed files):
- `source-2650.json.gz`: `8c7fe9ef…` gz, `e800d5f8…` raw;
- the six extra files (§4);
- `pool812.json` `91a4e36f…`.

## 8. What remains, gaps and findings

1. **Not Lean-checked.**
   - The six slice trees: EXACT TREE.
   - The 2,021 extra rows: CERTIFIED + written encoder soundness.
   - `N66Bound 55`.
   - The Lean ↔ JSON binding of `rowsP/Q/U/A`, F and Lo is by my own Python checks (COMPUTED), as `rows_match.py` was
     for 304 before FV304. A compact-checker run with `SliceCatalog` identities would make it kernel-checked.
2. **The task's slice list is longer than needed.**
   - With `N66Bound 55`, h(Lo) ≥ 15, so the budget-33 slice (19,14) and the budget-34 slice (20,14) serve only
     h(Lo) = 14, which N66 ≤ 55 rules out.
   - 18 + 15 = 33, so no budget-32 exclusion (`E310.residual_excludes_32`) is needed either.
   - The six slices used: (18,15) at budget 33; (18,16) and (19,15) at 34; (18,17), (19,16) and (20,15) at 35. This
     agrees with ES307 §3, ROUTE307 §1.3 and VERIFY_P307_CHAIN's case enumeration. LEAN_STATUS §4.3 lists L7/L9 with all
     five budget-33/34 slices.
3. **Row count.**
   - `ResidualBound 118` depends on **2,021** distinct extra rows (2,025 in blocks), not the 1,990 that ES307 §8 and
     LEAN_STATUS §4.3/T4 name.
   - The 31 rows of the (19,16) slice that are outside v169 are certified by the cuts-v14/15/16 audits and VERIFY307's
     T4 on b35s19-v16, not by ES307's T4. This is a scope note, not a soundness gap.
   - The 812 pool rows' LRATs are in `fastbb-20261113` (LEAN_STATUS §4.3).
4. **Cost slip in LEAN_STATUS §7** (HEURISTIC arithmetic).
   - Its residual figure: "143,447,786 leaves → about 2,650–3,630 CPU-h". But 143.4 M × 0.0185–0.0253 s is 2.65–3.63 M
     **seconds**, which is about **737–1,008 CPU-h**.
   - The 303 row has the same slip: 123.2 M leaves gives about 633–866 CPU-h, not 2,300–3,100.
   - The olean and source sizes there are right.
5. **`ValidUnitRow` has the premise `0 < n`.** This makes it weaker than the task's wording ("for every configuration
   as in ResidualBound"). It still suffices, because the gluing applies it only at n ≥ 119.
6. **The adapter is untested on a concrete catalog.** `SliceCatalog` has never been instantiated, so
   `slice_of_root` is proved but not exercised.
   - A later run's root carries a literal row count `m`, while the adapter states `2652 + rows.length`.
   - The six values are 2652 (b33s18), 3672 (b34s18), 3464 (b34s19), 3672 (b35s18), 3707 (b35s19) and 4642 (b35s20).
   - The bridge is `rows_lengths` plus `List.length_append`.
7. **Trust items outside the kernel.**
   - Lean does not check imported oleans against their sources. Pins are compared in §6 for the directly imported
     chain311 modules only, not for the whole import closure.
   - There is no closing import audit in the style of `assemble_final310.sh`.

## 9. Resume

```bash
cd /home/jay/research/data/formalize-20261122/res118
python3 -I tools/gen_rows.py && python3 -I tools/check_rows.py && python3 -I tools/check_base_rows.py
python3 -I tools/bind_evidence.py data/evidence.json
tools/start_unit.sh b5 30 /bin/bash tools/build.sh Rows LemmaA Glue Final Adapter BalancedBudgetsZ Compose304
tools/start_unit.sh ctl2 30 /bin/bash controls/run_controls.sh      # both must report "rejected as expected"
```

When FV304's `E304Z.Final.excludes_67 : ExcludesHoleBudgetZ 67` compiles, `Res118.forces_304_of_slices excludes_67`
removes the first hypothesis. Both use the same `BalancedBudgetsZ.olean` (`38d8f8ae…`).
