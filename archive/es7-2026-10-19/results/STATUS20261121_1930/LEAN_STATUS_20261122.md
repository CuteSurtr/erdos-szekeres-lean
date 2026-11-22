> Agent inventory (ledger workflow `ledger-1122`, Lean-status agent, 22 Nov 04:25-04:50 KST), copied unchanged from
> `/home/jay/research/data/ledger-20261122/lean/LEAN_STATUS.md`. Not evidence; claims tagged [R] are from records.
> Correction (main session, 05:50): the 303 and 302 tree costs in section 7 confuse kiloseconds with hours. At
> 0.0185-0.0253 s per leaf, 123.2M leaves take about 630-870 CPU-h and about 4e7 leaves about 205-280 CPU-h (HEURISTIC).
> The binding cost of the 303 check is disk: about 530 GB at 4.3 KB per leaf.

# LEAN_STATUS: what is Lean-checked in erdos-szekeres-lean, and what each ES(8) bound rests on (22 Nov 2026)

Read-only inventory, 22 Nov 2026, about 04:25–04:50 KST. Nothing was built, compiled, run, moved, renamed or deleted. No
`lean` process and no lean-lsp tool was started. The only file written is this one.

Tags used below:
- **[R]**: read from a record. Not re-verified here.
- **[D hh:mm]**: checked on disk at that time with read-only commands (ls, sha256sum, git ls-files/show, du, python -I).
- Labels follow es-research §2: PROVED, CERTIFIED, EXACT TREE, COMPUTED, HEURISTIC. "Lean-checked" means kernel-checked
  with only `propext`, `Classical.choice` and `Quot.sound`. "Lean-checked modulo X" means the Lean theorem takes X as
  a hypothesis.
- This file gives no deletion verdicts. Where nothing depends on a folder it says "no Lean dependency found", which
  is not permission to delete.

## 0. Headline

| bound | formal status today | what is outside Lean |
|---|---|---|
| **ES(8) ≤ 310** | **Lean-checked end to end**: `ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310 : ForcesConvexNGon 310 8`, standard axioms. Receipt dated 10 Nov 23:17 KST (`logs/es310/final310-compact.json`, verified: true). Not refereed. | Nothing, mathematically. **The build cannot be loaded now**: the chunk oleans and sources were deleted on 19 Nov. A re-check costs about 36.7 CPU-h of Lean plus the chain build, and needs the campaign data (§4.1). |
| ES(8) ≤ 311 | Lean-checked twice (19 Oct: old pipeline; 6 Nov: compact checker). Superseded. | Nothing. The 311 balanced tree `tree-63` is not in the main snapshot; it survives in tag `history-2026-11-14` and on branches `history` and `origin/history`. |
| **ES(8) ≤ 304** (current best) | **Lean-checked modulo three hypotheses**: `OmissionBalancedZ.composition_304_z : ExcludesHoleBudgetZ 67 → N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 304 8`. Axiom log on Linux, 20 Nov (`fv304-20261120/logs/lean/bbz.log`); also compiled on the Mac, 21 Nov (unmerged branch). | (1) the budget-67 tree: EXACT TREE, two implementations; the FV304 Lean check is running. (2) N66 ≤ 55: CERTIFIED cubes plus a written model. (3) ResidualBound 118: a written computer-assisted chain over trees, 1,990 CERTIFIED rows, N66 ≤ 55 and Lemma A. |
| ES(8) ≤ 303 (pending) | `OmissionBalancedZZsF.composition_303_zzsf : ExcludesHoleBudgetZZsF 68 → N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 303 8` compiles. | The budget-68 tree: its finder is complete; check A is running (1,018 of 32,765 files at about 04:37 [D]); check B has not started. **No claim.** |
| ES(8) ≤ 302 (prepared) | `OmissionBalancedZZsN.composition_302_n54 : ExcludesHoleBudgetZZsN 16 69 → N66Bound 54 → ResidualBound 118 → ForcesConvexNGon 302 8` compiles. | **Neither new hypothesis has evidence yet.** For N66 ≤ 54, the L15 campaign has 63 leaves certified and its certified cover is incomplete (04:30:33 [D]). The budget-69 tree has not started. |

**FV304** is the Lean check of `ExcludesHoleBudgetZ 67` with the compact checker. Status at 04:38:01 [D]: 1,667 chunk
modules done, 6,537 ready, 6 running, 0 failed. `run.tsv` holds 1,647 modules with 2,914,364 leaves, 26.6 % of
10,941,091, every one with lean_rc 0 and the standard axiom line. When its `E304Z.Final` compiles, 304 becomes
**Lean-checked modulo `N66Bound 55` and `ResidualBound 118`**. Nothing is claimed before then.

The path to a fully Lean-checked 304:
- The tree hypotheses are feasible now: FV304 runs, and the 303 and 302 trees cost the same per leaf. The 303 tree
  has about 11× the leaves (pre-registered count); the 302 tree does not exist yet.
- `ResidualBound 118` and `N66Bound` are the hard part.
  - "Lean modulo cake_lpr verdicts" (the ENCBLEAN pattern) is feasible but big.
  - A pure kernel check of the SAT proofs is infeasible with today's tools under the axiom rule (§7).

---

## 1. Toolchain, packages and build state

- **Lake project** [D]:
  - `lakefile.toml`: package `erdos_szekeres`, default target the library `ErdosSzekeres`, `weakLeanArgs = ["-j1"]`.
  - It requires Mathlib at `rev = "v4.24.0"`; RESULTS.md gives commit `f897ebcf`.
  - `lean-toolchain`: `leanprover/lean4:v4.24.0`. elan's default has been 4.24.0 since 22 Nov 04:13 (cleanup-20261122;
    toolchains 4.35.0 and 4.36.0 removed).
- **Library** `ErdosSzekeres` [D]:
  - 209 `.lean` files; `ErdosSzekeres.lean` imports 67 modules.
  - `.lake/build` is 324 MB, `.lake/packages` 6.2 GB.
  - `ErdosSzekeres.olean` was built on 4 Nov 23:45. No library source is newer than that olean, and `git diff
    8621eb159 2d1cb6baa` shows no change under `ErdosSzekeres/`, the lakefile, the manifest or the toolchain.
  - CI audit: `scripts/AxiomAudit.lean`, 587 `#print axioms` lines [R RESULTS.md §B].
  - **The large certificate imports are not in the library build**: BalancedRows, BalancedCoverCutsV2, Residual32Bridge2650
    and the 30x composition files. The comment on `Partition.BalancedBound` says so.
- **Record-level Lean is built outside Lake.** It is compiled with bare `lean -j1 -R . [-o …]` and an explicit
  `LEAN_PATH` over these olean stores:

  | olean store | what it holds | size / state [D] | used by |
  |---|---|---|---|
  | repo `.lake/build` and `.lake/packages` | the library and Mathlib (4,952 oleans pinned in `build/chain311/library.json`; FV304's `check_pins_es304z.py` checked them against the 6 Nov pins) | 6.5 GB | everything below |
  | `experiments/omission-compact-checker-2026-11-05/build/chain311/olean` | 196-module geometric chain: `BalancedRows`, `BalancedCoverCutsV2`, `BalancedBudgets`, `Residual32Bridge2650.Rows`, … (built 5–6 Nov from sources pinned in git archives) | 335 MB for the whole `build/chain311` | every 30x composition, FV304, 310/311 assembly |
  | `…/build/CompactChecker`, `…/build/ext` | checker oleans (`Fast2`, `Path`, `Split`, `Bridge311*`, `Fcat2650`, …) and the three catalogs | 53 MB + 72 MB | FV304 (symlinks in `fv304-20261120/olean/CompactChecker/`), 310/311 |
  | `/home/jay/research/data/bal186-20261119/zrow/leanz/olean` | `LemmaZ.olean` (sha256 `ef249ba1…` = ES305 §7 [D]) | 0.5 MB | BalancedBudgetsZ, FixedStatesZ, FV304 |
  | `/home/jay/research/data/bal186-20261119/zrow/leanzs/olean` | `FixedStatesZ`, `LemmaZStar`, `BalancedBudgetsZZs` | 1 MB | 303/302 files |
  | `/home/jay/research/data/fv304-20261120/olean` | `BalancedBudgetsZ.olean`, `CompactChecker/{FcatZ,BridgeZ}`, `E304Z/*` | 7.0 GB of chunk oleans at 04:38 | FV304 |
  | `~/.elan/toolchains/leanprover--lean4---v4.24.0` | the pinned compiler (FV304 calls this binary by absolute path) | | all |

- **Other Lake packages inside the repo** [D]:
  - `archive/…/LEANLB20261111/.lake`: 6.2 GB, its own Mathlib copy.
  - `archive/…/ENCBLEAN/.lake`: 26 MB, Std only.
  - `archive/…/ENCBLEAN/geo/.lake`: 6.2 GB, Mathlib `f897ebcf`, the same revision as the repo.
- **Rebuild memory floors** [D, from `build/chain311/build.tsv` and the import graph of `build/chain311/src`]:
  - The 30x compositions import an 87-module closure (`BalancedRows`, `BalancedCoverCutsV2`). The heaviest module is
    `BalancedCoverCutsV2` at **16.35 GiB** cgroup peak; every other is ≤ 5.5 GiB.
  - The full 310/311 closure has 195 modules. Its peak is `ResidualCoverCutsV2` at **28.68 GiB** (built at a 43G cap),
    then `RankCoreFour` at 16.2 GiB.
  - The Mac rebuild of the 87-module closure matched the chain311 hashes byte for byte (ES8CHECK20261121 §4, unmerged
    branch `origin/es-mac-2026-11-21` [R via git show]).

## 2. The definitions the chains use (verbatim, from the sources [D])

```lean
-- ErdosSzekeres/Definitions.lean (library)
def ForcesConvexNGon (N n : ℕ) : Prop :=
  ∀ s : Finset Point, GeneralPosition s → N ≤ s.card → HasConvexNGon n s
-- ErdosSzekeres/Omission/Partition.lean (library)
def BalancedBound (B : ℕ) : Prop := ∀ n, ∀ c : Configuration n, ¬ c.HasCap 7 → ¬ c.HasCup 7 →
    ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B
def ResidualBound (B : ℕ) : Prop := ∀ n, ∀ c : Configuration n, ¬ c.HasCap 6 →
    ¬ HasConvexNGon 8 (Finset.univ.image c.point) → NoJunctionOn c.cup (Finset.range n) → n ≤ B
-- ErdosSzekeres/Omission/PopulationBounds.lean (library)
theorem forces_of_population_bounds {B R : ℕ} (positive : 1 ≤ B + R)
    (balanced : BalancedBound B) (residual : ResidualBound R) : ForcesConvexNGon (B + R + 2) 8
-- ES305N20261119/LemmaZ.lean (record)
def N66Bound (B : ℕ) : Prop := ∀ n, ∀ c : Configuration n, ¬ c.HasCap 6 → ¬ c.HasCup 6 →
    ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B
-- ES305N20261119/BalancedBudgetsZ.lean (record): the 304 tree statement
def ExcludesHoleBudgetZ (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
    (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧        -- 2,685 rows
    (∀ r, BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧  -- 446 cuts
    15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ (∑ i, holes i) ≤ budget                          -- Z-row
-- ES303N20261120/BalancedBudgetsZZs.lean: the same plus `holes 0 = 0 ∧ holes 1 = 0` and `15 ≤ ∑ i ∈ Zs, holes i`
--   (ExcludesHoleBudgetZZsF b)
-- ES303N20261120/BalancedBudgetsZZsN.lean: ExcludesHoleBudgetZZsN r b, both rows at demand r;
--   zzsn_55_iff : ExcludesHoleBudgetZZsN (70 - 55) b ↔ ExcludesHoleBudgetZZsF b := Iff.rfl
```

`Configuration n` (`Omission/Realization.lean`) means n real points with strictly increasing x-coordinates and every
increasing triple non-collinear. `Configuration.ofGeneralPosition` builds one from the library's
`GeneralPosition`.

## 3. Lean files of the 30x compositions: identity and compile evidence

All nine are tracked in git at main 2d1cb6baa (= origin/main) [D]. The sha256 of every file equals the value
the record gives [D]. The work copies in `zrow/leanzs/` that `build_zsn.sh` compiles are byte-identical to the
record copies [D 04:48]; that settles Mac finding 1 for this machine.

| file (record) | key theorems | sha256 (= record) | compile evidence |
|---|---|---|---|
| ES305N20261119/LemmaZ.lean | `OmissionZRow.Z_eq` (decide +kernel), `zOwners_no_cap/cup`, `z_row : N66Bound 55 → … → 15 ≤ (Z \ c.occupied).card` | `e6b28efa…` | ES305 §3 [R]; Mac rc 0, standard axioms [R] |
| ES305N20261119/BalancedBudgetsZ.lean | `feasible_holes_z`, `balanced_bound_of_hole_budget_z`, `composition_305_z`, **`composition_304_z`** | `3e0651a0…` | **`fv304-20261120/logs/lean/bbz.log`** [D]: all three standard, 20 Nov; Mac rc 0 [R] |
| ES305N20261119/FixedStatesZ.lean | `zero_mem_occupied`, `one_mem_occupied`, `ExcludesHoleBudgetZF`, `composition_304_zf`, `composition_303_zf` | `20945f03…` | `ES303N20261120/data/build_zsn.log` [D]: standard |
| ES305N20261119/Composition305.lean | `composition_305 : BalancedBound 185 → ResidualBound 118 → …` | `d7d1b2c3…` | ES305 §5 [R]; Mac [R] |
| ES304N20261119/Composition304.lean | `composition_304 : BalancedBound 184 → ResidualBound 118 → ForcesConvexNGon 304 8`, `avoiding_303` | `a58df4a7…` | ES304 §4 [R]; Mac [R] |
| ES303N20261120/LemmaZStar.lean | `Zs_eq`, `zsOwners_no_cap/cup`, `zs_row` | `47bd1f56…` | build_zsn.log [D]: standard |
| ES303N20261120/BalancedBudgetsZZs.lean | `balanced_bound_of_hole_budget_zzsf`, **`composition_303_zzsf`**, `composition_302/301/300_zzsf` | `7684a1de…` | build_zsn.log [D]: rc 0. The file's own `#print axioms` covers only `balanced_bound_of_hole_budget_zzsf` and `composition_301_zzsf`. **`composition_303_zzsf` was printed only on the Mac** (extra print file, standard axioms; ES8CHECK §4 [R]) |
| ES303N20261120/BalancedBudgetsZZsN.lean | `z_row_of`, `zs_row_of`, `balanced_bound_of_hole_budget_zzsn`, **`composition_302_n54`**, `composition_301_n53` | `4cfface8…` | build_zsn.log [D]: standard |
| ES303N20261120/Composition303.lean | `composition_303 : BalancedBound 183 → ResidualBound 118 → …` | `bbecd6cf…` | no Linux compile record; Mac rc 0, standard [R] |

Note on build discipline:
- These compiles used bare `lean -R` across three olean directories (chain311, `leanz`, `leanzs`/fv304). Nothing
  stamped them, and no import audit like `assemble_final310.sh` ran.
- Lean does not check an imported `.olean` against its source.
- The FV304 launch checked the pins (`check_pins_es304z.py` [R PLAN.md]), but there is no final audit of the import
  closure yet (§5).

---

## 4. The formal chain of each bound

Column key:
- **Lean?** names the declaration and file.
- **git?** says whether the source is tracked.
- **build dep** names the olean stores needed to re-check it.
- **evidence** gives the path and size [D].
- **re-checked?** asks whether the evidence was re-run independently.
- **keep-set** lists the minimal artefacts that keep the link verifiable.

### 4.1 ES(8) ≤ 310 (Lean-checked end to end; build not loadable now)

`Final310Compact.lean` (pinned `7a91d397…`) [D]:
`forces_convex_octagon_310 := forces_of_population_bounds (by omega) balanced_population_187 residual_population_121`.
Here `balanced_population_187` comes from `E310.balanced_excludes_64`, and `residual_population_121` from
`E310.residual_excludes_32`.

| link | Lean? | git? | build dep | label | evidence [D] | re-checked? | keep-set |
|---|---|---|---|---|---|---|---|
| composition, geometry, rows | library + chain311 | yes [D 04:48]: all 51 origin paths (46 files, 4 tar archives and 1 gz, together the 196 modules) and the 12 `include_str` data files of `build/chain311/closure.json` are tracked at 2d1cb6baa. The 46 plain files match their pinned sha256; the tar members were not re-hashed here | chain311 (195 modules; peak 28.68 GiB) | Lean-checked | `logs/es311/final311-compact.json`, `logs/es310/final310-compact.json` (committed) | Mac rebuilt the 87 balanced modules byte-identically; the 195-module closure only on Linux | git; chain311 olean (335 MB) or a rebuild of about 3.4 CPU-h with a 29 GiB module |
| budget-64 balanced tree, 4,096 contexts, 7,048,218 leaves | yes, compiled into Lean (E310B chunks, `checkF2_sound`) | scripts yes; tree data **no** | Fast2/Path/Split oleans | Lean-checked (10 Nov) | campaign dir `/home/jay/research/data/es8-b64-pilot-20261105` (5.0 GB: `runs/` 3.9 GB holding 4,096 `ctx-*-b64.json.gz` + 4,096 `.result.json`, `contexts.jsonl`, `run_context.py`, `campaign/campaign.log`); **second copy** `/home/jay/research/data/zenodo-310-20261114/upload` (6 tar.zst, 4.13 GB, 8,195 files, byte-identical per its `CHECK.md` [R]) | the Lean check is the check; 1,982 contexts came from Linux and 2,114 from the Mac (ES8B64MAC20261110) | one of the two copies. **The frozen scripts read the absolute path `/home/jay/research/data/es8-b64-pilot-20261105`** (`assemble_final310.sh:118`, `drive_es310.py:100`, `export_es310.py:98`, `coverage_es310.py:80`), so a restore must use that path. The Zenodo bundle is not uploaded; CHECK.md finding A (personal data in files) is blocking |
| residual budget-32 tree, 437,579 leaves | yes (E311R chunks) | **yes**: `experiments/omission-final313-2026-10-11/certificate/tree-2650-32.json.xz.part-aa/ab` | as above | Lean-checked | in git | Lean twice (12 Oct, 6 Nov) | git |
| chunk oleans and sources | – | – | – | – | **deleted 19 Nov** (`cleanup-20261119/manifest.tsv`): es310 olean 16.4 GB + src 11.1 GB, es311 olean 6.5 GB + src 1.7 GB, test dirs | – | regenerable: about 36.7 CPU-h (E310B) + about 7.3 CPU-h (E311) of Lean [R] |

ES(8) ≤ 311:
- `Compact311.forces_convex_octagon_311` (6 Nov) and `ErdosSzekeres.Omission.forces_convex_octagon_311` (19 Oct).
- The header of `Final311Compact.lean` still says "NOT COMPILED". That is deliberate: its sha256 `b41a996a…` is pinned
  by `assemble_final311.sh` and recorded in `final311-compact.json`.
- The 311 balanced tree `tree-63` is not in the main snapshot (`archive/DROPPED.tsv`). It survives in tag
  `history-2026-11-14` and on branches `history` and `origin/history` (both at b80567cee) [D].

**What 304 does not use from this section:** `BalancedBound 187`, the budget-64 trees and the b64 campaign data.
- 304's signature contains none of them. The 307/308 chains used `BalancedBound 187` (L2); 304 replaces it with
  `BalancedBound 184`.
- **What it does use from this pipeline:**
  - The chain311 olean store: every 30x file imports `BalancedRows` and `BalancedCoverCutsV2`.
  - The L3 Lean pieces of `ResidualBound 118` (§4.3): `Residual32Bridge2650/Rows.lean` and
    `E310.residual_excludes_32`. These sit in the 195-module closure (peak 28.68 GiB), which the Mac did not
    rebuild.

### 4.2 ES(8) ≤ 304 (current best): Lean-checked modulo three hypotheses

**Update 23 Nov 00:45 (formalization wave 5, `FORMAL20261122`).** H1 is discharged by FV304
(`E304Z.Final.excludes_67`, 22 Nov 12:19). `Combined.es304_l15` takes only cake_lpr verdicts and two slices: ES(8) ≤ 304
is Lean-checked modulo the 105 level-15 cube verdicts, the 629 row-certificate verdicts and the 2,025 Res118 row
verdicts (trust items E1-E6), and the slice exclusions s35_19 and s35_20 (EXACT TREE, not in Lean; s35_19's Lean check
is running). Review of part 2: 8 confirmed, 2 not confirmed (H-T69 has no evidence; the s35_19 switch template is
not compiled); no fixes. The table below is the 04:25 inventory.

| link | Lean? | git? | build dep | label | evidence [D] | re-checked? | keep-set |
|---|---|---|---|---|---|---|---|
| composition `composition_304_z` | yes, ES305N20261119/BalancedBudgetsZ.lean | yes | chain311 (87-module closure, 16.35 GiB peak), `LemmaZ.olean`, library | Lean-checked (bbz.log, 20 Nov) | – | second machine: Mac agent, all 9 files rc 0 (ES8CHECK20261121 §4; agent, unmerged branch, not a person) | git, plus chain311 olean or its rebuild |
| Lemma Z (Z-row) | yes, `OmissionZRow.z_row` | yes | as above | Lean-checked | exact controls `zrow/lemmaz_control.py` [R] | Mac agent re-derived it (§1 of ES8CHECK) [R] | git |
| rows = JSON rows | **no**: `tools/rows_match.py` (Python, 0 mismatches [R]). Mac finding 4: it prints the indexing instead of asserting it | yes | – | COMPUTED match | – | Mac agent's own parser on the 446 cuts [R] | removed by FV304 (`BridgeZ.fcatZ_rows` is kernel-checked) |
| **H1: `ExcludesHoleBudgetZ 67`** | **not yet**; FV304 running (§5) | `scripts/omission_tree.py` is in git (sha256 `35cb3050…` = the record pin [D]). **Disk only, not in git** [D 04:48]: the row files `zrow/balz.rows` (`7076dd82…`), `balz_m0.rows`, `zrow.json`; the v2 assembler `zrow/balz_assemble.py` (`ae0411c1…`); `zb_run.sh`, `zb_check.sh`, `lemmaz_control.py`; `../balcheck/balcheck.cpp` (`554814fa…`) and its binary. All hashes equal ES305 §7 | – | **EXACT TREE** (check_tree + balcheck: 8,192 files, 21,873,990 nodes, 10,941,091 leaves, minimum margin 1, cover complete) [R] | `/home/jay/research/data/bal186-20261119/zrow/b67` (17 GB): `files/ctx-<k>-zb67.json.gz` (8,192), `occ/master.json`, `mis/master.json`, `balcheck.json`, `balcheck.tsv` (hashes in ES304 §4) | two in-project implementations; **no independent person or agent re-ran them** (ES304 §5); FV304 will be the third check | `zrow/b67` (the certificate itself and FV304's input), **plus every disk-only file named in the "git?" cell** (a re-check needs them; the rows files could be regenerated from `balanced-v2-source.json` + `zIndices`, but they are the hash-pinned inputs), plus `../balcheck/` |
| **H2: `N66Bound 55`** | **no** | records and tools yes; certificates no | – | **CERTIFIED** (132 cube leaves, cake_lpr) + **PROVED (written)** model soundness (N66N §2, §6.3) | §4.4 | yes for the verdicts and the cover (VS, VN, VB, U1; §4.4) | §4.4 |
| **H3: `ResidualBound 118`** | **no** (only its composition skeleton is Lean) | records yes; trees and certificates no | – | **PROVED, computer-assisted** (written chain; VR CONFIRMED `es307-final-1118`) | §4.3 | yes (VR's own tcheck_b35 rebuild; T4 re-certified 1,990/1,990 rows) | §4.3 |

What FV304 removes from trust once `E304Z.Final` compiles:
- `check_tree`, `balcheck`, the v2 assembler, `rows_match.py` and the Z-row support pin, which becomes kernel-checked
  through FcatZ/BridgeZ.

What stays outside Lean: H2 and H3, unchanged.

Alternative statement, not needed: `composition_304_zf` (FixedStatesZ) takes `ExcludesHoleBudgetZF 67`, the zero side
only.

### 4.3 `ResidualBound 118`, link by link (the chain of ES307N20261118 §1.1 and ROUTE307_1116 §1.2)

Derivation [R]:
- `forces_of_population_bounds` is not used inside this chain; it is the outer step.
- For nonempty R: |R| + h(C) = 154.
- h(F) ≥ 18 (L4) and h(Lo) ≥ 70 − 55 = 15 (L5 + L13).
- The budget-33, -34 and -35 slice trees exclude every split (h(F), h(Lo)) with h(C) ≤ 35.
- Hence h(C) ≥ 36 and |R| ≤ 118.
- Every tree leaves "state 0 missing" pending; Lean discharges that with `zero_mem_residualOccupied`.

| link | content | Lean? | label | evidence location [D] | re-checked? |
|---|---|---|---|---|---|
| L3 | 2,650 rows `all_rows_2650`, `holes_sum_add_population`, `zero_mem_residualOccupied`, `E310.residual_excludes_32` | **yes** (`Residual32Bridge2650/Rows.lean`, chain311; the budget-32 tree as in §4.1) | Lean-checked | git | – |
| L4 | h(F) ≥ 18: nine Lean rows (973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315), each of demand 6, cover F three times | rows yes; **the sum is written** | PROVED (arithmetic over Lean rows) | – | VR re-derived it |
| L5 | Lemma A: h(Lo) ≥ 70 − N66 (Lo owners have no 6-cap and no 6-cup) | **no** (THEORY310N20261113 Lemma A, written). The balanced analogue, Lemma Z, is Lean | PROVED (written) | – | CHAIN_REVIEW link 3, VERIFY_LO §2.6 [R] |
| L7 | budget-33 slices (18,15): 3,815 nodes, 1,908 leaves; (19,14): 186,077 nodes, 93,039 leaves. Lean rows plus capacity rows only | no | EXACT TREE | `/home/jay/research/data/lo33-20261113` (1.2 GB; `bb_66_55*`, `bb_65_56*`), `/home/jay/research/data/verify-LO-20261113` (58 MB) | VERIFY_LO (independent replay) [R] |
| L8 | 1,020 coupled rows (rhs 1). 812 of them are the "pool" | no; CNFs from RES33N `coupled.py` | CERTIFIED + written encoder soundness (VERIFY309N link (c)) | the **812 pool LRATs are in `/home/jay/research/data/fastbb-20261113/p2/proofs` (705) and `…/killtools` (107)** [D: 812 of 812 present, dir 12 GB]; the inventory is `LO33N20261113/budget34/audit/pool_inventory.json`; the other rows are under `/home/jay/research/data/es308-20261114/{cuts-*,audit/cuts-*}` | VERIFY308: 1,020 of 1,020 re-run by cake_lpr [R]; T4 below |
| L9 | budget-34 slices (18,16): 20,769 leaves; (19,15): 829,241; (20,14): 15,479,541 | no | EXACT TREE (project replay + tcheck + pycheck) | `es308-20261114/runs/s18` (35 MB), `s19` (282 MB), `s20` (4.4 GB) | VERIFY308 [R] |
| L10 | budget-35 slices (18,17): 206,049 leaves; (19,16): 7,763,206 | no | EXACT TREE (fresh_replay_v3 + tcheck_b35 + pycheck_b35) | `es308-20261114/runs/b35s18` (94 MB), `b35s19` (2.3 GB) | VB CONFIRMED `p307v-l10-pycheck` [R] |
| L11 | budget-35 slice (20,15): 8,080 contexts, 238,116,145 nodes, 119,054,033 leaves. Rows `b35s20-v169` = 2,650 + 2 capacity rows + 1,020 coupled + 970 appended | no | EXACT TREE by three implementations | `es308-20261114/runs/b35s20` (47 GB: packets `bb` + `bb-s1`; 8,064 of the `bb-s1` files are hard links into `bb`), `inputs/b35s20-v169/extra.json` (`de4bcceb…`) | VR CONFIRMED; the Mac verifier rebuilt `extra.json` byte-identically (ES8CHECK §4b) [R] |
| T4 | all 1,990 extra rows: retained CNF + LRAT with recorded sha256 and a fresh `s VERIFIED UNSAT` | no | CERTIFIED (1,994 jobs accepted, 0 rejected) | `ES307N20261118/data/lrat_recheck_v169_summary.json` [D]: 812 rows from `pool` + 1,178 rows from 127 `cuts-*` folders (1,182 attributions, since 4 rows have two candidates). Presence [D 04:48]: pool 812/812 files exist (`fastbb-20261113`). All 127 cut folders exist under `es308-20261114/` with 1,213 LRAT files, at least as many as each folder's row count. Counts only; hashes not re-checked. Sizes (1,288 LRATs found at depth ≤ 3 outside `runs/`): median 358 KB, p90 514 KB, max 987 KB, total 485 MB | yes (fresh cake_lpr) |
| L13 | N66 ≤ 55 | no | §4.4 | §4.4 | §4.4 |

- **Keep-set for H3** [R ES307 §7 "Keep" plus what was found here]:
  - every ctx file of `runs/b35s20/bb` and `bb-s1`;
  - `runs/b35s19`, `runs/b35s18`, `runs/s18`, `runs/s19`, `runs/s20`;
  - `inputs/`;
  - every row CNF + LRAT pair (`es308-20261114/cuts-*`, `audit/`);
  - **`fastbb-20261113/p2/proofs` and `fastbb-20261113/killtools`** (the 812 pool rows). These are not named in
    ES307 §7;
  - `lo33-20261113` and `verify-LO-20261113` (L7);
  - the tools in git under `LO33N20261113/budget34/`;
  - the N66 evidence (§4.4).
- `es308-20261114/runs` was once taken for superseded 307/308 evidence (STATUS20261121_1930 §6). It is an input of
  304 and of the pending 303 and 302.

### 4.4 `N66Bound 55` (304, 303 and H3) and `N66Bound 54` (302)

**Update 22 Nov ~20:50 (formalization wave 3, `FORMAL20261122`).** `RowGeo.n66_bound_55_of_cubes_rows :
CubesUnsat132 → RowCertsUnsat → R0Parse → N66Bound 55` compiles with standard axioms: N66Bound 55 is Lean-checked
modulo the 132 cube verdicts, the 629 row-CNF verdicts and the named hypothesis R0Parse (`N66Enc.R0 = R1`, COMPUTED,
E4-class). At level 15, `N66G15.n66_bound_54_of_cubes` still takes `RowsValid R0_15` as a hypothesis.

**Update 23 Nov 00:45 (wave 5).** `N66R15.n66_bound_54 : CubesUnsat105R → RowCertsUnsat → N66Bound 54` (and `_55`)
compiles with standard axioms. It has no R0Parse and no RowsValid hypothesis: the level-15 rows are kernel-checked chunk
constants, and the cube printer reads the same constants. N66 ≤ 54 is therefore Lean-checked modulo the 105 level-15
cube verdicts and the 629 row-certificate verdicts (E1-E6). Review: 13 confirmed, 1 not confirmed (off the label's path).

- **N66 ≤ 55** [R N66N20261113, cubes20261115]:
  - The level-14 relaxation is split into cubes; all 132 leaves have a CaDiCaL 2.1.3 LRAT accepted by cake_lpr, and
    the cover is complete (0 of 16,384 assignments uncovered).
  - The model soundness is written: §2 covers labels, states, cycle rows, coupled rows, the mirror lemma and
    transport; §6.3 covers the monolithic families. The rows carry their own certificates (templates and cores).
  - Re-checked by VS (own cover code), VN (own code: exact partition; every `cert.cnf` = F_c + its cube units, byte
    for byte; fresh cake_lpr on 2 cubes), and U1/VB (four checks per cube, all 132, including fresh cake_lpr).
  - Not Lean-checked.
- **Evidence** [D]:
  - `/home/jay/research/data/n66-20261113/p2/c14` (105 GB) has 176 cube directories. 132 of them hold LRAT files,
    18.9 GB compressed.
  - `c14/campaign_status.json` lists 200 cubes: 132 `certified`, 68 `split`. The certified set equals the set of
    directories with an LRAT. The 44 directories without one all have status `split`.
  - The base inputs, the row justifications and U1's verifier sit in the same work dir: `static` 1.2 GB, `mono`,
    `lm`, `b12*`/`b13g`, `vfy_u1` 2.5 GB.
  - Which of these files `p2_verify` needs for a re-check was **not traced here**; the record's own lists govern.
- **N66 ≤ 54 (needed for 302)**: the L15 campaign is in `/home/jay/research/data/n66-20261113/p2/c15` (83 GB) and
  verified by `vfy15` (3.5 GB). At 04:30:33 [D]: 63 certified, 7 running, 28 queued, 34 split; leaf cover ok,
  certified cover **not** complete. The driver's deadline is 24 Nov 08:00.
- **Lean side today:**
  - `N66Bound` is a plain Lean `Prop` (§2). It enters `z_row`, `zs_row`, `z_row_of`/`zs_row_of` and the
    compositions as a hypothesis.
  - Through Lemma A (L5) it also enters `ResidualBound 118`, which is not formalised.
  - No Lean statement mentions the N66 CNF.
- **Lean precedent for the encoder link:** ENCBLEAN does it for the sixfold case (§6).

### 4.5 ES(8) ≤ 303 (pending)

| link | Lean? | label / state | evidence [D] | keep-set |
|---|---|---|---|---|
| composition `composition_303_zzsf` (and `composition_303_zf`, `composition_303`) | yes (§3) | compiles; axioms of `composition_303_zzsf` printed on the Mac only | git | git, chain311, `leanz`/`leanzs` oleans (regenerable in minutes) |
| Z*-row `zs_row` | yes (LemmaZStar) | Lean-checked; exact controls in `data/zstar_control.log` | git | git |
| **`ExcludesHoleBudgetZZsF 68`** | no | finder complete (22 Nov 01:08, rc 0; 32,755 contexts, 246,300,823 nodes). **Check A** (`balz_assemble_v5.py` + check_tree) restarted 03:48:48; 1,018 of the 32,765 expected files written by about 04:37. **Check B** (balcheck2) not started. Pre-registered acceptance values: ES303 §5 | `zrow/b68zs` (143 GB) | `zrow/b68zs`; `data/zzs_rows.json`, `tools/zbs_run0.sh` and `tools/balz_assemble_v4.py` (in git). **Disk only** [D]: `zrow/balzs.rows` (`9135465a…`); `../balcheck/balcheck2.cpp` (`83d14a9f…`) and its binary `951b90dc…`; and `tools/balz_assemble_v5.py` (`964b0000…`), `tools/chain303.sh`, `tools/v5ctl.py` and `data/v5ctl/`, which are **untracked** in the record directory. The `zrow/` copies of v5 and chain303.sh are byte-identical to the record copies. The claim would rest on these files |
| N66Bound 55, ResidualBound 118 | no | as in 4.3 and 4.4 | as in 4.3 and 4.4 | as in 4.3 and 4.4 |

### 4.6 ES(8) ≤ 302 (prepared; no evidence yet)

| link | Lean? | state | evidence | keep-set |
|---|---|---|---|---|
| `composition_302_n54` | yes (BalancedBudgetsZZsN.lean) | compiles, standard axioms (build_zsn.log [D]) | git | git |
| `ExcludesHoleBudgetZZsN 16 69` | no | **not started**. `zrow/zbs54_run0.sh` exits 9 unless the marker `zrow/N66_LE_54_VERIFIED` exists [R]. Dive estimate with hypothetical rows: 8.0e7 nodes (HEURISTIC) | `zrow/balzs_n54.rows`, `data/zzs_rows_n54.json`, `tools/balz_assemble_n54.py` (git), `zrow/hyp54` (324 KB) | those files |
| `N66Bound 54` | no | L15 campaign running (4.4) | `n66-20261113/p2/c15`, `vfy15` | those |
| `ResidualBound 118` | no | as 4.3 (N66 ≤ 54 alone does not improve it, ES303 §7 [R]) | as 4.3 | as 4.3 |

Alternative statement: `composition_302_zzsf : ExcludesHoleBudgetZZsF 69 → N66Bound 55 → ResidualBound 118 → …`
(budget 69 at rhs 15). Its dive estimate is 8.9e9 nodes [R], far costlier.

### 4.7 Superseded compositions (for completeness)

| file | statement | compiled? |
|---|---|---|
| ES306N20261119/Composition306.lean | `BalancedBound 186 → ResidualBound 118 → ForcesConvexNGon 306 8` | yes, 19 Nov 16:25 [R] |
| ES305N20261119/Composition305.lean, `composition_305_z` | 305 | yes [R], [D bbz.log] |
| LO33N20261113/budget34/VERIFY307/tools/Composition307.lean | `BalancedBound 187 → ResidualBound 118 → ForcesConvexNGon 307 8` | **never compiled** (its header: "DRAFT … NOT compiled") |
| ES8SLACK/review/C1_certificates/Composition311.lean | 311 | not checked here |

---

## 5. FV304: the Lean check of the 304 tree (running)

- **Goal** (PLAN.md [R]):
  - `E304Z.Final.excludes_67 : OmissionBalancedZ.ExcludesHoleBudgetZ 67 := BridgeZ.balanced_z_of_root E304Z.root`;
  - `forces_304_of_n66_res : N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 304 8`. This is the template in
    `drive_es304z.py:33–42` [D].
  - `E304Z.root : ¬ ∃ holes, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) []) holes`, at the empty path, so both sides
    are covered.
- **Already done** [R PLAN.md, D logs]:
  - `FcatZ` (`fcatZ_wf`; axioms [propext]).
  - `BridgeZ` (`fcatZ_rows`, `balanced_z_of_root`; standard).
  - Pilot chunks.
  - The corruption control: `control/logs/C334301.log` shows the deliberate failure with `sorryAx`; that is the
    control, not a defect.
  - `FinalTest.forces_304_of_root`, standard (`logs/lean/finaltest.log`).
  - Export complete: 8,192 contexts, 8,211 chunk sources, 20.7 GB.
- **Progress at 04:38:01** [D]:
  - 1,667 modules done, 6,537 ready, 6 running (`FV_JOBS=6`), 0 failed.
  - `run.tsv`: 1,647 modules, 2,914,364 leaves (26.6 %), all lean_rc 0, axiom line standard on every row.
  - Wall time: 0.0253 s per leaf. Peak anonymous memory: 1,060 MB.
  - Oleans: 2,406 bytes per leaf, 7.0 GB so far. Sources: 1,893 bytes per leaf.
- **Remaining** (HEURISTIC): 8.03 M leaves × 0.0185 s (idle rate of the 310 run) to 0.0253 s (rate measured here) =
  **about 41–56 CPU-h** of chunk compiles. Then come the per-context joins, 8 sub-roots, the Root and Final. No
  clock time is quoted.
  - Unknown: a Root over 8,211 modules is untested. The 310 Root (4,096 modules) took 61 s, 20.7 GB RSS and a
    1.9 GB cgroup peak. FV's memory budget is `FV_MEM=5500` over all FV jobs, inside the `esv` guard of 6,000 MB.
- **Live dependencies** (do not move or rebuild while it runs): every olean store of §1, the pinned elan 4.24.0
  binary, `fv304-20261120/` (26 GB), `zrow/b67/files` (the contexts.jsonl sha256 pins the export's input files), and
  `experiments/omission-compact-checker-2026-11-05/{drive_es304z.py, export_es304z.py, root_es304z.py,
  CompactChecker/*.lean}`, which are tracked in git.
- **After it finishes:**
  - **`zrow/b67/files` is still the certificate.** ES304 says the tree files are "kept until an independent check".
    FV304 finishing is not that trigger.
  - The regenerable part is `fv304-20261120/export/src` (20.7 GB) and the chunk oleans (about 26 GB at the end), at
    about 75–80 CPU-h in total (HEURISTIC). The olean pins, `run.tsv` and the logs are small and should be kept.
- **Missing final step:**
  - The driver has no closing audit like `assemble_final310.sh`. That script re-checks the library pins, lists every
    imported module with its sha256, and refuses a module provided by two `LEAN_PATH` roots.
  - Re-running `check_pins_es304z.py` after Final and recording the import closure would bring FV304 to the 310
    standard.

## 6. Other Lean-checked results in the repository

Per RESULTS.md (12 Nov), not re-verified here unless marked [D].

| result | status | declaration | build | external hypotheses |
|---|---|---|---|---|
| Suk 2016; HMPT 2020; ES(n) ≥ 2^(n−2)+1, so ES(8) ≥ 65; ES(n) ≤ C(2n−4, n−2)+1; mixed-cap counterexample; the omission row geometry (B1–B5) | Lean-checked (library, CI) | `Suk.theorem2016`, `HMPT.theorem2020`, `octagon_lower_bound`, `sixtyFive_le_esNumber_eight`, `esNumber_le_choose`, `HMPT.MixedCap.mixed_cap_budget_counterexample`, `ErdosSzekeres.Omission.*` | repo `.lake` | none |
| ES(8) ≤ 312 … 317 (A4–A7) | Lean-checked, superseded; their certificates are left out of the snapshot (`archive/DROPPED.tsv`; tag `history-2026-11-14`) | `forces_convex_octagon_312` … `_317` | – | none |
| **Sixfold case of ES(8) = 65** (D1): ≥ 61 points invariant under a rotation of order 6 force an octagon | **Lean-checked modulo `EncB.CubesUnsat64`** (64 cake_lpr verdicts) **and trust items E1–E6** (emitter output, verdicts, DIMACS semantics, compiler and runtime, kernel/Mathlib/notions, SHA-256) | `EncB.Geo.sixfold_es8`, `sixfold_es8_of_texts`, `sixfold_es8_order6` (ENCBLEAN/geo) | `ENCBLEAN/.lake` (26 MB), `ENCBLEAN/geo/.lake` (6.2 GB) | the 64 verdicts: `/home/jay/research/data/c6upper-replay-20261106` (31 GB) and `c6upper-noty12-20261106` (16 GB). ENCBLEAN says `scripts/resolve.sh` re-ran 2 of the 64 [R]. The replay records themselves were not read here |
| Lean-checked octagon-free sets (D4): 6-fold 60, 7-fold 64, half-turn 64, 3-fold 61, 5-fold 56, 4-fold 52, mirror 46 | Lean-checked (`decide +kernel`) | `LeanLB.sixfold60`, … | `LEANLB20261111/.lake` (6.2 GB; own package, about 11 min to rebuild [R]) | none |
| Symmetric heptagon results (C1–C8): mirror classes, the reduction, C3 cover, C2 orbits, the layer lemma, MIRRORETV | Lean-checked pieces; the SAT classes rest on verdicts (see RESULTS.md §C) | `SymReduction.*`, `MirrorOdd.*`, `C3LEAN/C3Cover.lean`, `LayerLemma.lean`, … | repo `.lake` | per RESULTS.md |
| 7-fold octagon case (D2), PRIMEFOLD core, ALGAN identities | partly Lean (reduction / identities only) | `sevenfold_octagon` (from `Sevenfold70`), `PCompatCore.lean`, `ALGAN20261112/lean/Identities.lean` | repo `.lake` | per RESULTS.md |

RESULTS.md stops at 12 Nov: it lists ES(8) ≤ 310 as the best bound and has no rows for 309–304. Update it when the
304 chain is formalised.

---

## 7. What it would take to make each chain fully Lean-checked (all costs HEURISTIC)

Scaling basis, measured here [D]:
- 0.0185–0.0253 s of Lean per leaf (310 run idle / FV304 under SMT load).
- 2.4 KB of olean and 1.9 KB of exported source per leaf.
- Disk: 834 GB free at about 04:36 (`df`: 906 GB of 1.8 TB used).
- An untested risk for every tree above about 1e7 leaves: whether one Root can import about 1e5 chunk modules
  holding about 300 GB of oleans.

Three tiers per hypothesis: **(a) as is**, **(b) Lean modulo cake_lpr verdicts** (the ENCBLEAN / empty-hexagon
pattern), **(c) full kernel check, standard axioms**.

| hypothesis | (a) as is | (b) Lean modulo verdicts | (c) full kernel | verdict |
|---|---|---|---|---|
| `ExcludesHoleBudgetZ 67` (304) | EXACT TREE ×2 | not applicable (no SAT step) | **FV304 running**; about 41–56 CPU-h left, then the Root | **feasible, in progress** |
| `ExcludesHoleBudgetZZsF 68` (303) | finder done; checks running | – | new `FcatZZs`/`BridgeZZs` (Z*-row as row 3132), and the export must start every path with the state-0 literal (the zero side only; `holes 0 = 0` in the statement makes that sufficient). **123,166,799 leaves (pre-registered, not yet confirmed by a check)** → about 2,300–3,100 CPU-h, about 300 GB of oleans + 230 GB of sources | **feasible but big**; Root scale unknown |
| `ExcludesHoleBudgetZZsN 16 69` (302) | tree not built | – | as 303, on a tree of roughly 4e7 leaves (dive estimate 8.0e7 nodes on hypothetical rows) → roughly 750–1,000 CPU-h | feasible once the tree exists |
| **`ResidualBound 118`** | written chain (VR CONFIRMED) | (i) Lemma A in Lean: **small** (it mirrors `LemmaZ`; THEORY310N20261113 §6 item 4 calls Lemma A(i) one of the "small Lean additions"). (ii) h(F) ≥ 18 and the slice-gluing arithmetic: **small**. (iii) The 1,990 extra rows as Lean facts. The library already has a Lean semantics for coupled residual CNFs (`ErdosSzekeres.Omission.Coupled`: atoms before/capGe/cupGe/positive/convex over the 154 residual states, plus the `CoupledLrat` wrapper of Mathlib's `Sat.FromLRAT`). A Lean model of RES33N `coupled.py`, proved sound against that semantics and hash-bound to the 1,990 texts, would make the rows hypotheses on cake_lpr verdicts: **big** (weeks; that the clause families match has not been checked). (iv) Compact-checker runs on all 8 slice trees: **143,447,786 leaves** (L7 + L9–L11; (20,15) alone 119 M) → about 2,650–3,630 CPU-h, about 345 GB of oleans + 270 GB of sources, plus a 154-state catalog per slice (up to 4,644 rows + 2 capacity rows); per-leaf cost may be higher than on the balanced side | (iii) by in-kernel LRAT: **unknown, probably infeasible under the current caps**. The in-repo precedent (`RankCore*`, LRAT files of 16–104 KB) compiled at a 9–16 GiB cgroup peak, and that memory is not due to the LRAT step alone. The row LRATs here have a median of 358 KB (up to 987 KB; 1,990 rows). A reflective LRAT checker in the style of the compact checker would be a research project of unknown cost | **(b) big but feasible; (c) not feasible today** |
| **`N66Bound 55` / `54`** | CERTIFIED cubes + written model | A Lean definition of the N66 relaxation CNF: the mono66 families of §6.3, the cardinality counter, the SB clauses, and the row clauses together with their template/core justifications. Then a satisfiability theorem for every `Configuration` in the N66 class (against `OmissionZRow.N66Bound`), hash binding of the 132 cube texts, and a Lean cube-cover theorem. **Big**: larger than ENCBLEAN (FORMAL_OPTIONS.md agrees). One Lean N66 encoder would serve the Z/Z* rows (304–302) and Lemma A (H3) | **Infeasible today.** The level-14 cube LRATs alone are 18.9 GB compressed on disk (the record gives 82 GB trimmed for the campaign), 10^4–10^6 × beyond any in-kernel precedent. The streaming route (lrat-catcher, arXiv 2607.00815) adds a native-evaluation axiom per chunk, which fails the house axiom rule | **(b) big; (c) infeasible** |

Net, in order of cost:
1. **Cheapest formalization step, now:**
   - rebuild the nine 30x composition files in **one** olean directory, with a logged import audit (the
     `assemble_final310.sh` pattern);
   - add the missing `#print axioms composition_303_zzsf` line on Linux.
   - Minutes of CPU. It needs the 87-module chain (16.35 GiB peak) only if chain311 is rebuilt.
2. **FV304 to completion, plus a closing pin/import audit.**
   - Result: 304 Lean-checked modulo `N66Bound 55` and `ResidualBound 118`.
3. **Small Lean lemmas:**
   - Lemma A;
   - h(F) ≥ 18;
   - a Lean statement of the residual slice system with the extra rows as explicit hypotheses
     (`ExcludesResidualSlice …`);
   - the gluing theorem giving `ResidualBound 118` from the slice statements, `N66Bound 55` and the row hypotheses.
   - This turns the written chain of §4.3 into a Lean theorem modulo trees and rows. Hours to a day or two.
4. **FV of the 303 tree, once both checks have passed:** about 2,300–3,100 CPU-h. Risk: the scale of the Root.
5. **ENCBLEAN-style encoders**, one for N66 and one for the residual coupled rows, plus compact-checker runs on the
   slice trees.
   - Result: 304 (and 303) **Lean-checked modulo cake_lpr verdicts and E1–E6-type trust items**.
   - This is the realistic end state, of the kind of the published empty-hexagon verification.
6. A pure-kernel N66 or row-LRAT check is **not feasible** with today's tools under the axiom rule.

---

## 8. Dependency edges for the cleanup (no deletion verdicts)

**Inputs that look like caches but are live** (each is an input of the running FV304 and/or of every 30x compile):
- the repo `.lake/` (6.5 GB). Its 4,952 library and Mathlib oleans are hash-pinned (`build/chain311/library.json`).
  A rebuild with other hashes makes the pin checks of `assemble_final310.sh` and `check_pins_es304z.py` refuse.
- `experiments/omission-compact-checker-2026-11-05/build/chain311` (335 MB). A rebuild takes about 3.4 CPU-h with a
  28.7 GiB module, or 16.35 GiB for the 87-module balanced closure alone.
- `…/build/CompactChecker` (53 MB; FV304 links into it) and `…/build/ext` (72 MB).
- `/home/jay/research/data/bal186-20261119/zrow/leanz/olean` and `…/leanzs/olean`.
- `~/.elan/toolchains/leanprover--lean4---v4.24.0`.
- `/home/jay/research/data/fv304-20261120` (26 GB, running).

**Certificates (inputs of current or pending claims):**

| path [D size] | needed by |
|---|---|
| `bal186-20261119/zrow/b67` (17 GB) | 304 H1 (EXACT TREE) and FV304's input |
| `bal186-20261119/zrow/b68zs` (143 GB) | 303 (checks running) |
| `n66-20261113/p2/c14` (105 GB) + base and row inputs in `n66-20261113` (rest of the 208 GB) | N66 ≤ 55 → 304, 303, H3 |
| `n66-20261113/p2/c15` (83 GB), `vfy15` (3.5 GB) | N66 ≤ 54 → 302 (running) |
| `es308-20261114` (64 GB; `runs/` 54 GB, `cuts-*`, `audit/`, `inputs/`) | H3 (L9–L11, rows), hence 304, 303, 302 |
| `fastbb-20261113` (12 GB; at least `p2/proofs` and `killtools`) | H3 (L8: the 812 pool rows) |
| `lo33-20261113` (1.2 GB), `verify-LO-20261113` (58 MB) | H3 (L7) |
| `es8-b64-pilot-20261105` (5.0 GB) **or** `zenodo-310-20261114` (3.9 GB) | re-check of ES(8) ≤ 310 (absolute path pinned in the frozen scripts). The "or" holds for the 8,195 files the 310 re-check reads, and only for them. The pilot dir also holds `mac-bundle-20261110` (1.2 GB), `import-mac-runs.tsv`, `witness/` (b64/b71 hunt logs), `validate63/`, `calib/` and b63 runs: **not traced** |
| `c6upper-replay-20261106` (31 GB), `c6upper-noty12-20261106` (16 GB) | sixfold_es8 (`CubesUnsat64`); `resolve.sh` re-ran 2 of 64 (replay records not read here) |

**Regenerable builds of Lean results** (sources and manifests in git; rebuilding them restores the result):
- `archive/…/LEANLB20261111/.lake` (6.2 GB): `LeanLB.*` sets; about 11 min plus Mathlib [R].
- `archive/…/ENCBLEAN/geo/.lake` (6.2 GB, Mathlib `f897ebcf`) and `ENCBLEAN/.lake` (26 MB): `EncB.Geo.sixfold_es8`.
- `fv304-20261120/export/src` and its chunk oleans, once FV304 has finished and its records are kept (§5).
- The deleted es310/es311 chunk builds (§4.1).

**Found here, no Lean dependency** (not a deletion verdict; records cite some of these as evidence or controls):
- `zrow/b68z` (15 GB): the Z-row-only budget-68 run, stopped at 2,754 of 16,384 contexts and resumable. It would
  feed only `composition_303_zf` if finished.
- `zrow/b66` (1.1 GB): evidence of the superseded 305.
- `zrow/fix` (313 MB) and `zrow/zs66` (20 MB): controls cited in ES305 §5b and ES303 §3.
- `es311-full-20261106` (108 KB of logs).

## 9. Findings and caveats (numbered)

1. 304's tree-to-Lean link (`rows_match.py`) is a Python comparison that prints rather than asserts (Mac finding 4).
   FV304 replaces it with kernel-checked identities.
2. On Linux, `composition_303_zzsf` has no `#print axioms` line; only the Mac's extra print file shows it, with the
   standard axioms. `Composition303.lean` has no Linux compile record.
3. The 30x Lean files were compiled across three olean directories with no stamp or import audit (§3). The Mac
   rebuild (agent, unmerged branch) is the only second build.
4. The pending 303 rests on `tools/balz_assemble_v5.py`, `tools/chain303.sh` and `tools/v5ctl.py`. They are
   **untracked** in git and exist on disk only (also in `zrow/`).
5. `ResidualBound 118` uses the 812 pool-row certificates in `fastbb-20261113`. ES307 §7's keep list names only
   `cuts-*` and `audit/`.
6. FV304 has no closing audit of the import closure. The pins were checked at launch only.
7. `Composition307.lean` was never compiled. Nothing depends on it.
8. The 310 build cannot be loaded now. Its re-check needs the campaign data at the exact absolute path, and the
   Zenodo copy is not uploaded (blocking finding A: personal data).
9. RESULTS.md (12 Nov) is out of date for 309–304, and its §A still calls 310 the best bound.
10. **The hash-pinned inputs of the 304 and 303 tree checks are not in git.** That covers `zrow/balz.rows`,
    `balz_m0.rows`, `balzs.rows`, `zrow.json`, the v2/v3/v5 assemblers, `zb_run.sh`, `zb_run0.sh`, `zb_check.sh`,
    `lemmaz_control.py`, `../balcheck/balcheck.cpp` and `balcheck2.cpp` (with binaries).
    - ES305 §7 and ES303 §6 pin them by sha256 (all equal on disk [D]), but the only copies are in
      `/home/jay/research/data/bal186-20261119/`.
    - The record directories in git hold only `rows_match.py`, `build*.sh`, `balz_assemble_v4.py`,
      `balz_assemble_n54.py`, `zbs_run0.sh`, `zbs54_run0.sh`, `zzs_rows*.json` and `zstar.json`.
11. The chain311 sources are all recoverable from the git snapshot (51 origins, 12 data files; §4.1). The 46 plain
    files were hash-checked and the tar members were not. So `build/chain311/src` is not the only copy.
12. `FORMAL_OPTIONS.md` says "the final 311 assembly … peaked at 28.7 GB". Per the compact-checker README, that peak
    belongs to the chain module `ResidualCoverCutsV2`; the assembly itself peaked at 0.39 GB cgroup. Also, the
    24 GB cap it cites was superseded by the 80 % rule (22 Nov 03:55).

## 10. Not checked here

- No Lean compile, axiom query or tree replay was run; every compile claim comes from a log or a record.
- The written soundness arguments themselves were not re-read: N66 §2/§6.3, VERIFY309N link (c), Lemma A.
- Not traced: which files in `n66-20261113` outside `p2/c14` a `p2_verify` re-check needs. Neither were the exact
  contents of `fastbb-20261113` beyond the 812 pool LRATs.
- Not checked: whether RES33N `coupled.py` clause families match the library's `ErdosSzekeres.Omission.Coupled`
  semantics.
- The #810 Lean projects are out of scope: `~/research/tools/e810-lean/research/hall-reduction/.lake` (6.2 GB), and
  the `lean-formalization` branch of `~/research/sat/erdos-810-research`.
- Sized but not placed in any chain here [D]: `/home/jay/research/data/verify308-20261114` (595 MB),
  `theory310-20261113` (2.6 GB; THEORY310N's CNF/LRAT files) and `encblean-m9` (380 MB; ENCBLEAN M9 work).
  The verifier work folders under `/home/jay/research/data/roadmap-20261115/pm1115/` (e.g. VR's `vr1118`, VB's
  `vb1116`) were neither sized nor placed. Some of them may hold independent-check evidence that records cite.
- Only counts were checked for the tar members of the chain311 sources and for the cut-row LRATs; hashes were not.
