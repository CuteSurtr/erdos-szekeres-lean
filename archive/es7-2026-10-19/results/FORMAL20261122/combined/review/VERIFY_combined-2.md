# VERIFY combined (part 2): independent review, slot rv5 (23 Nov 2026, 00:10–00:45 KST)

Worker result: `/home/jay/research/data/formalize-20261122/combined`, part 2. That is README §2 of 00:08, REMAINS.md of 00:07, the sources
`src/Combined/{N66L15,ES304L15,Switch3519L15}.lean`, `controls/BadN66.lean`, and the oleans `out/Combined/{N66L15,ES304L15}.olean`.

All reviewer files are in `/home/jay/research/data/formalize-20261122/combined/review/part2`, plus this file. The reviewer wrote nowhere else.
The one exception is the harness's own background-task output files under the session scratchpad
(`/tmp/claude-1000/…/tasks/*.output`), which the harness writes. Part 1's review files in `combined/review/` were not
touched.

The checks use the reviewer's own code only:
- `lean/RV5P2Review.lean`, the ONE compile;
- `tools/rv5p2_audit.py`;
- `tools/rv5p2_bind.py`;
- `tools/{env,start,unit_ax}.sh`.

No lake, no lean-lsp, no git writes, no olean output, and no other unit touched.

## 1. Verdict

**CONFIRMED: the four part-2 end theorems.** This covers each statement, the binding of the CNF-verdict hypotheses,
the axioms, and non-vacuity for every hypothesis except H-T69 of `es302_l15`. H-T69 has no evidence yet, so it is
**not confirmed**. Also confirmed: the import audit, REMAINS.md, and the decision not to plug in `s35_19`.
`Switch3519L15.lean` is **not confirmed**: it is uncompiled and cannot compile yet. No bound and no record label changes.

| key | verdict | core evidence |
|---|---|---|
| `Combined.residual_bound_118_l15` | **confirmed** | My own `RV5P2.rb118` re-elaborates it by a different route: N66 via `n66_bound_54_of_rows` + `rowsValid_R15`, the blocks via `blockValid_*`/`rowsUnsat_of_texts`, then RS slices into `Res118.residual_bound_118_of_slices`. Its type is alpha-equal (`==`) and defeq to the worker's. 8 hypotheses, standard axioms. |
| `Combined.es304_l15` | **confirmed** | Alpha-equal to my `RV5P2.es304`, defined as `composition_304_z excludes_67 (n55 …) (rb118 …)`. Accepted against my hand-unfolded plain-geometry statement. 8 hypotheses; the budget-67 tree is a Lean theorem. Standard axioms (the E304Z walk). |
| `Combined.es303_l15` | **confirmed** | Alpha-equal to my `RV5P2.es303`, built via `composition_303_zzsf`. 9 hypotheses, standard axioms. |
| `Combined.es302_l15` | **confirmed** for statement, axioms and binding. The label "not a bound claim" is right. | Alpha-equal to my `RV5P2.es302`, built via `composition_302_n54` with `N66Bound 54`. 9 hypotheses, standard axioms. |
| `Combined.es302_l15`: non-vacuity of H-T69 (`ExcludesHoleBudgetZZsN 16 69`) | **not confirmed** | No evidence: the budget-69 tree does not exist. Its finder `esr-bal-zbs69` (`zbs54_finder.sh 69 16 …`) was active at 00:10. |
| CNF binding of `CubesUnsat105R`, `RowCertsUnsat`, `RowsTextUnsat rowsP/Q/U/A` | **confirmed** (sample) | Own re-print with the three frozen exes: 14/14 items byte-identical to the certified files (5 cube leaves, 4 distinct trim texts; 3 templates; 1 core; the T208 sub-list; 4 rows). Fresh cake_lpr on the printed bytes: 5/5 `s VERIFIED UNSAT`. Negative control rejected. |
| Import audit | **confirmed** | 13,786 modules, each with exactly one provider, equal to Lean's own `findOLean`. Every sha256 equals every earlier record. ctime bounds hold. The component environments resolve every shared module to the same file (§7). |
| REMAINS.md (part-2 lists and labels) | **confirmed** | The per-bound lists equal the compiled binders (8/8/9/9). The labels and figures match the records (§8). Wording notes only. |
| `s35_19` not plugged in | **confirmed correct** | `RS.s35_19` is MISSING from the environment. `status.json` at 00:37:20 shows `done` = s33_18, s34_18, s34_19, s35_18, and 3519 at 651 modules with no root and no final. There is no `RS_Final3519.log`. |
| Lean negative control `BadN66` | **no own verdict**: worker log read, not re-run | `logs/ctl_BadN66.log`: lean_rc 1, "N66Bound 55 … expected … N66Bound 54". Not re-run because the review was limited to one compile. My B6 lines show independently that `n66_bound_54` and `n66_bound_55` carry their exact bounds. |
| `Switch3519L15.lean` | **not confirmed** | Uncompiled. It imports `RS.Final3519`, which does not exist yet. |

**Labels.** The worker's labels in REMAINS.md, confirmed as worded:
- **ES(8) ≤ 304** (`Combined.es304_l15`) is Lean-checked modulo:
  - the cake_lpr verdict hypotheses `CubesUnsat105R` (105 level-15 cube verdicts) and `RowCertsUnsat` (629
    row-certificate verdicts: 628 full CNFs plus the trimmed sub-CNF of T208);
  - `RowsTextUnsat rowsP/Q/U/A` (2,025 row verdicts);
  - trust items E1–E6 (E3 not proved);
  - the slice exclusions `s35_19` and `s35_20` (EXACT TREE, not in Lean).
- **ES(8) ≤ 303** (`Combined.es303_l15`): the same, plus `ExcludesHoleBudgetZZsF 68` (EXACT TREE by two checks, not
  in Lean).
- **ES(8) ≤ 302** (`Combined.es302_l15`): the same, plus `ExcludesHoleBudgetZZsN 16 69`, which has no evidence yet.
  It is a conditional theorem, **not a bound claim**.
- **ResidualBound 118** (`Combined.residual_bound_118_l15`): the same five hypotheses as 304.

Unrefereed; computer-assisted. These forms take N66 from the 105 level-15 verdicts, not from the 132 level-14 cubes
that the 304/303 records cite. The record label of N66 ≤ 54 stays CERTIFIED.

**Required fixes: none.** Wording notes are in §8.

## 2. Method and units

**LEAN_PATH.** `tools/env.sh` lists the worker's 20 roots. The `diff` of its expansion against `combined/tools/env2.sh`
is empty, and the audit re-checked this inside its unit. The roots are:
- FV304's 14 (`lean_path.txt`, sha256 `65463fd5…`, checked before every start);
- ENCBLEAN, res118-rowblocks, the worker's `links/` and `out/`;
- `n66-level15/build/olean` and `n66-l15-rows/build/olean`.

All roots are read-only.

| unit (KST) | job | result | memory |
|---|---|---|---|
| `esr-ag-rv5-p2ax`, 00:24:51–00:34:28 | THE ONE compile: `lean -j1 -R lean lean/RV5P2Review.lean` (sha256 `c441ce98…`), no `-o` | **lean_rc 0**, 9:37 wall; no error or warning in the log | anon+shmem peak **611 MB** (0.2 s sampler; stop level 4,915 MB). `time -v` max RSS 20.0 GB (mapped oleans). cgroup `memory.peak` 6,444,548,096 B; memory.events `high` 66,098, `max` 0, `oom` 0, `oom_kill` 0 |
| `esr-ag-rv5-p2aud`, 00:35:09–00:35:50 | `tools/rv5p2_audit.py` (O_DIRECT hashing of 13,786 oleans and 3,464 companions; `sha256sum -c` of the four N66 manifests) | rc 0, **0 problems**, 41 s | max RSS 62 MB |
| `esr-ag-rv5-p2bind`, 00:36:19–00:37:08 | `tools/rv5p2_bind.py` (own re-print sample, fresh cake_lpr) | rc 0, **0 problems**, 49 s | max RSS 3.00 GB (T208 sub-list print), MemoryMax 5G |

**Gates before every start** (`logs/gates.log`):
- no YIELD file;
- Tctl 84–85 °C;
- `cpu_free.sh esr` = 4;
- ag-track anon 0 MB plus the expected peak ≤ 6,800 MB;
- no other `esr-ag-rv5-*` unit.

The memory guard lifted each unit (`memguard.log`: `LIFT esr-ag-rv5-p2*`) and stopped none.

**Disclosure: `memory.peak` above MemoryMax.** The compile's cgroup `memory.peak` passed 6 GiB by 2 MB. As in the
worker's ES304/ES304L15 compiles and in part 1's review compile, this is page cache of mapped oleans held at the guard's
`memory.high` brake, with `memory.max` lifted. Anonymous memory was 611 MB, and no OOM event occurred.

## 3. (4) Axioms (the ONE compile, `logs/RV5P2Review.log`)

Every one of the following printed exactly `[propext, Classical.choice, Quot.sound]`:
- **The four worker constants, from the worker's oleans:**
  - `Combined.residual_bound_118_l15`, `Combined.es303_l15` and `Combined.es302_l15` (B1);
  - `Combined.es304_l15` (B12; this walk goes through all of E304Z).
- **My own re-elaborations**, kernel-checked in my compile:
  - `RV5P2.n54`, `n55`, `rb118`, `es303`, `es302` and `es304`;
  - the explicit forms `rb118_explicit`, `es303_explicit` and `es302_explicit`, and `forces_iff`.
- **The pieces:**
  - `N66R15.n66_bound_54` and `n66_bound_55`;
  - `N66R15Geo.n66_bound_54_of_rows` and `rowsValid_R15`;
  - `N66R15.rowCertsUnsat_of_texts`;
  - part 1's `Combined.residual_bound_118`, `es303` and `es302`.

`N66R15.cubesUnsat105R_of_texts` printed `[propext, Quot.sound]`, a subset of the three.

`#print axioms` walks the whole proof DAG, so `sorryAx` and `Lean.ofReduceBool` occur nowhere below these theorems.

## 4. (1) Statements

**Type equality.** I wrote my own statements and re-elaborated them in the compile by a different route. Each is
compared with the worker's constant, and in every case `Expr` equality (`==`, alpha) and `isDefEq` are both true (B3):

| worker constant | reviewer constant | route |
|---|---|---|
| `Combined.residual_bound_118_l15` | `RV5P2.rb118` | N66 from the generic theorem, not `N66R15.n66_bound_55`; blocks and RS slices straight into `Res118.residual_bound_118_of_slices`, not part 1's `Combined.residual_bound_118` |
| `Combined.es304_l15` | `RV5P2.es304` | `composition_304_z excludes_67`, not `Combined.es304` |
| `Combined.es303_l15` | `RV5P2.es303` | `composition_303_zzsf` |
| `Combined.es302_l15` | `RV5P2.es302` | `composition_302_n54` with `N66Bound 54` |
| `N66R15.n66_bound_54` | `RV5P2.n54` | |
| `N66R15.n66_bound_55` | `RV5P2.n55` | |

So each worker statement is proved, inside my compile, from the hash-pinned pieces by a term the kernel checked there.
This does not depend on the worker's `Combined.*` oleans.

**Binders** (B4, from the oleans).
- Kind `theorem`, 0 universe parameters.
- Binder counts: 8 (residual, 304), 9 (303, 302).
- Every binder is explicit (`default`) and non-dependent, and every conclusion is closed.
- The binders, in order:
  - `tree68 : ExcludesHoleBudgetZZsF 68` (303 only) or `tree69 : ExcludesHoleBudgetZZsN 16 69` (302 only);
  - `cubes : CubesUnsat105R`, `certs : RowCertsUnsat`;
  - `hP/hQ/hU/hA : RowsTextUnsat rowsP/Q/U/A`;
  - `s35_19 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsU) 35 19`, `s35_20 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsA) 35 20`.
- No binder type mentions any intermediate statement. I checked for `N66Bound`, `ResidualBound`, `BlockValid`,
  `RowsUnsat`, `RowsValid`, `RowValid`, `ExcludesHoleBudgetZ`, `ForcesConvexNGon`, `N66E15.CubesUnsat105`, `R0_15`,
  `N66Enc.R0` and `R0Parse`.
- These are exactly the hypotheses the task allows:
  - named cake_lpr verdict props;
  - the slices that are not in Lean;
  - the trees that are not in Lean (68 for 303; 16, 69 for 302).

  The budget-67 tree of 304 is `E304Z.Final.excludes_67`.

**Values** (B6). Each worker theorem is the one-line instance its README states. For example:
`es304_l15 = fun cubes certs hP hQ hU hA s35_19 s35_20 => Combined.es304 (N66R15.n66_bound_55 cubes certs) …`, and
`es302_l15` passes `N66R15.n66_bound_54`.

**Hand-unfolded statements** (B8). Each is accepted with the worker's constant as its proof term, so the elaborator
checked the statement against the worker's type.
- `RV5P2.es304_explicit` (and `es303_`, `es302_`, `rb118_explicit`) restate the hypotheses in my own words, as
  transparent definitions:
  - `rvUnsat F` means that no ν : ℕ → Bool satisfies every clause, where a literal l > 0 holds iff ν |l| and a
    literal l < 0 holds iff ¬ν |l|;
  - the cubes become `∀ c ∈ leaves105, rvUnsat (fullCnf R1_15 c)`;
  - the certificates become `(∀ t ∈ templates, rvUnsat (certCnf t)) ∧ (∀ k ∈ cores, rvUnsat (certCnf k))`;
  - the rows become `∀ s ∈ rows, ∀ nv F, parseDimacsBytes (rowText s).toUTF8 bytes = some (nv, F) → rvUnsat F`.
- They restate the conclusion as `rvForces 304 8`: every s : Finset (Fin 2 → ℝ) with no three distinct points
  collinear and 304 ≤ |s| has t ⊆ s with |t| = 8 and `ConvexIndependent ℝ` on t.
- `forces_iff : rvForces N n ↔ ForcesConvexNGon N n` holds by `Iff.rfl`.

**Declaring modules** (B5). The conclusion is the genuine library constant, and every module has one provider (§7).

| constants | module |
|---|---|
| `ForcesConvexNGon`, `HasConvexNGon`, `GeneralPosition`, `ConvexPosition`, `Point` | `ErdosSzekeres.Definitions` (repo library) |
| `ResidualBound` | `ErdosSzekeres.Omission.Partition` |
| `N66Bound` | `LemmaZ` |
| `CubesUnsat105R` | `N66R15Enc.Bridge` |
| `RowCertsUnsat` | `N66R15Geo.Assembly` |
| `leaves105` / `tree15` | `N66E15.Cover` |
| `fullCnf` | `N66E15.Full` |
| `R1_15` / `rowsAll` | `N66R15Enc.RowList` |
| `templates` | `N66R15Enc.DataT` |
| `cores` | `N66R15Enc.DataC` |
| `certCnf` | `N66R15Enc.Gen` |
| `DimacsSat(isfiable)` | `EncB.Dimacs` |
| `RowsTextUnsat` | `RowGeo.Blocks` |
| `ResSliceExcludes` | `Res118.Glue` |
| the two tree statements | `BalancedBudgetsZZs`, `BalancedBudgetsZZsN` |

- Every constant in this table is a `def`; nothing in it is an axiom or opaque.
- `RS.s35_19`, `RS.s35_20`, `Combined.*_l15_s3519`, `RowGeo.R0Parse` and `N66Enc.R0` are MISSING.

**Definitions** (B7, printed from the oleans). The following agree with the records and with part 1's review:
- `ForcesConvexNGon`, `N66Bound`, `ResidualBound`, `CubesUnsat105R`, `RowCertsUnsat`, `R1_15 = R1nat15.map (·.map toFin70)`
  and `R1nat15 = rowsAll.flatten`;
- `ResSliceExcludes`, which has the fixed ≤ 1 bound, `holes 0 = 0`, the 2,650 bridge rows, the F/Lo capacity rows,
  ≥ 1 per row of the list, and the budget;
- `ExcludesHoleBudgetZZsF b`: both rows at 15;
- `ExcludesHoleBudgetZZsN r b`: both rows at r. So `ZZsN 16 69` is the b69 finder's "69 16" form.

## 5. (2) Binding of the CNF-verdict hypotheses

**Lean-defined CNFs and the bridges.**
- `CubesUnsat105R` is about `fullCnf R1_15 c` and `RowCertsUnsat` about `certCnf`. The certified files are the
  per-leaf trims and, for T208, a trimmed sub-CNF.
- The reviewed bridges (`cubesUnsat105R_of_texts`, `rowCertsUnsat_of_texts`) derive both props from exactly the
  verdict shapes E1–E3 deliver: a printed trim per leaf, the printed certificate texts, and T208 through `subCnfChecked`.
- I composed them myself. `RV5P2.es304_texts` is ES(8) ≤ 304 with the two N66 props replaced by those verdict-shaped
  hypotheses, and it elaborated with lean_rc 0 (B8).
- `RowsTextUnsat` is already in text form, on the bytes of `RowEnc.rowText`.

**Exes.** All three are frozen. Each was hashed at the start, before every print, and after the last print, before
the cake runs. The `leaves` and `list` calls ran after the start check only. Each hash is the one in its freeze
manifest, and both n66-l15-rows manifests re-check clean (§7).

| exe | sha256 | manifest |
|---|---|---|
| `n66r15print` | `65865b1e…` | n66-l15-rows `logs/freeze_manifest.sha256` |
| `r15rowprint` | `6b9af2c6…` | n66-l15-rows `logs/freeze_manifest.sha256` |
| `rowprint` | `eabe3791…` | res118-rowblocks `data/manifest.sha256` |

**Own sample** (`data/bind_rv5p2.tsv`, seed 20261123): **14/14 bound**.
- **Cubes, 5 leaves** (1, 73, 83, 96, 100 = `…_39h`, `hooooh`, `hohoho`, `hhohhh`, `hhhohh`). They give 4 distinct
  texts, 3 of them non-trivial. The UP-refuted leaves 73 and 100 print the same 112-byte trim, `93548e48…`, and their
  certified files have that same hash.
  - My own leaf map, from `n66r15print leaves` against campaign_status (sha256 `4802dc9a…`, as in the record), is a
    bijection with the 105 certified cubes.
  - For each leaf, `n66r15print trim i desc/i.txt` gives bytes identical to the certified `trim.cnf`. The sha256 equals
    campaign `trim_cnf_sha256` and a fresh sha256 of the file.
  - Each `cake.out` has the exact line.
- **Certificates.**
  - Templates 81, 88, 253 (`T_353be094…`, `T_3b1b391e…`, `T_9ef27b31…`) and core 143 (`C_a9efadb3…`). For each,
    `r15rowprint t|c k` gives bytes identical to `zstd -dc` of VB's `.cnf.zst`, the hash equals the json
    `cnf_sha256`, and the json has `cake_lines == ["s VERIFIED UNSAT"]` and `cake_exact 1`.
  - The index → id map comes from my own parse of the `DataT*`/`DataC*` docstrings: 421 + 208 ids.
  - **T208**: `r15rowprint st 208 trim208.idx` printed 245,753 bytes, identical to VB's trimmed CNF. The sha256 is
    `349b6c6c…` = `.trimmed.sha256`, and `.trimmed.cake.out` has the exact line.
- **Rows** P 90, Q 138, U 24, A 397: `rowprint row B I` has the sha256 of every T4 job of that support (2, 2, 3 and 1
  jobs). Each of these jobs:
  - is ACCEPTED;
  - has recorded = actual = printed = fresh sha256 of the retained CNF;
  - has the exact line in its cake output.

**Fresh cake_lpr** (`c14ff498…`, `--CML_HEAP_SIZE=2000`) on the **printed bytes themselves**. Each LRAT stream hash
equals the recorded LRAT hash. Evidence is the exact line, grepped; the exit code is not used.
- `cube_hhhohh` (UP-refuted): ACCEPT.
- `cube_oooooo_40o_52o_46o_44o_45o_39h` (236 MB LRAT, 7.2 s): ACCEPT.
- `T_353be094…`: ACCEPT.
- `C_a9efadb3…`: ACCEPT.
- `row_A397`: ACCEPT.
- **Negative control**: the CNF of `T_353be094…` with the LRAT of `C_a9efadb3…` gave 0 exact lines (cake rc 0), so it
  was rejected.

**Data seen by the theorems.** The interpreter, reading the oleans on this LEAN_PATH, produced (B9; COMPUTED):
- an `R1_15` dump equal to `rows_used15.txt`, sha256 `f45e25f1…`;
- a `leaves105` dump equal to the n66-l15-rows reviewer's dump, `5f188424…`;
- the counts `rowsAll` 109, `R1_15` 10,859, `leaves105` 105, templates 421, cores 208 and `nvHeader` 1,647,847;
- the row counts `rowsP` 812, `rowsQ` 208, `rowsU` 35 and `rowsA` 970.

**Earlier full binding.**
- 105/105 trims and 628/628 certificates plus T208: n66-l15-rows M9/M3, re-printed in full by its reviewer.
- 2,025/2,025 rows: res118-rowblocks M9, re-run by its reviewer; part 1's review re-printed 20.

I re-printed only the sample above.

## 6. (3) Hypotheses not vacuous

- **H-N66C and H-N66R are true under E1–E6.**
  - The record cubes20261120 §8 is CERTIFIED: 105 leaves of an exact cover, vfy15 105/105.
  - VB's records hold the exact line for 628/628, plus T208's trimmed verdict.
  - My 4/4 fresh runs above add to the 17/17 fresh runs of the n66-l15-rows review and to 161/161 + 629/629 earlier.
  - N66 ≤ 54 is consistent with the known lower bound N66 ≥ 50.
- **H-ROWS** is true by 2,025 verdicts. Part 1's `RV5.text_iff` shows that it says exactly "every row CNF is
  unsatisfiable".
- **H-S3519** is EXACT TREE: fresh_replay_v3, 15,533,581 nodes, 7,763,207 leaves (res118 README line 137). Its Lean
  check is running.
- **H-S3520** is EXACT TREE by three implementations: 238,116,145 nodes, 119,054,034 leaves (line 138).
- **H-T68** is EXACT TREE by two independent checks: 32,765 files, 246,300,833 nodes, 123,166,799 leaves (ES303N20261120).
- **H-T69: no evidence.** It stays open, and the 302 theorem is conditional.
- No two hypotheses constrain the same object in conflicting ways. They concern N66 relaxation CNFs, certificate CNFs,
  row CNFs, residual slice hole vectors and balanced hole vectors.

## 7. Import audit (own code: `tools/rv5p2_audit.py`, `data/audit_rv5p2.json`, `data/closure_rv5p2.tsv`)

**Closure.** My compile printed 13,786 modules: the worker's `closure2.tsv` (13,784, the same set) plus
`Combined.N66L15` and `Combined.ES304L15`. This contains part 1's reviewed closure (`closure_rv5.tsv`, 13,638) and
the 146 imported N66 oleans: 32 from n66-level15 and 114 from n66-l15-rows.

**One provider.**
- For every module, Lean's `findOLean` path equals my emulation of Lean's rule: the first root holding `<pkg>/` or
  `<pkg>.olean`.
- Exactly one distinct file `<root>/<mod>.olean` exists over all 20 roots plus the sysroot.

**Component environments.** For each environment, every module of my closure that resolves to an existing file there
resolves to the same file as here. **Mismatches: 0.**

| environment | modules that resolve there |
|---|---|
| n66-l15-rows `tools/env.sh` | 5,115 |
| n66-level15 `geo_env.sh` | 5,001 |
| n66-level15 `build.sh` (ENCB + its store + sysroot) | 1,780 |
| part 1 `tools/env.sh` | 13,640 |

So LemmaZ, EncB.\*, the repo library, Mathlib and the toolchain resolve to the same files here as in the environments
the N66 oleans and part 1's oleans were compiled in.

**Dependency ages along the chain part 2 adds** (per-root mtime and ctime ranges from `data/closure_rv5p2.tsv`):

| step | newest ctime of the inputs | oldest mtime of the oleans compiled on them |
|---|---|---|
| n66-level15 store | toolchain 4 Nov 23:38:34; packages and repo library 4 Nov 23:45:14; ENCBLEAN 6 Nov 20:57:46; leanz 19 Nov 19:28:05 | 22 Nov 17:46:27 |
| n66-l15-rows store | the same, plus n66-level15 22 Nov 17:48:47 | 21:20:47 |
| part-2 `out/` oleans | the same, plus n66-l15-rows 21:57:15; part 1's stores (links 19:10:41, fv304 12:19:19, res118-rowblocks 18:18:24, chain311 6 Nov) and part 1's `out/` oleans (newest ctime 21:30:23) | 23:51:54 |

So no input of these three steps changed after the oleans that depend on it were written. I make no claim of this form
for the prebuilt package caches. Those rest on the hash equalities above.

**Hashes.** All 13,786 files were read with O_DIRECT and hashed. Every earlier record agrees:
- **Part 1's review closure:** 13,638 of 13,638 equal.
- **The worker's `closure2.tsv`:** 13,784 of 13,784 equal.
- **The 146 N66 oleans:**
  - all equal to the worker's `n66_oleans2.tsv`, which was written before its compiles;
  - 9 of them (6 N66 oleans, LemmaZ, EncB.Render, EncB.Dimacs) equal the n66-level15 review compile log.
- **Part 1's `out/` oleans:** all four match VERIFY_combined §7 (`cdadeb8c…`, `ebf1b4b3…`, `57476735…`, `fac38b7e…`)
  and the worker's `manifest.sha256`.
- **`Res118.Rows`:** `7d8fa1d2…`.
- **The two part-2 oleans:** equal to `manifest2.sha256` and to README §2.6 (`974e24e6…`, `3325c03b…`).
- **E304Z:** 8,217 modules, digest `fa02576e…`, equal to fv304-audit's.
- **Companions:** 3,464 `.olean.server`/`.olean.private` files, all equal to fv304-audit's table.
- **Digest** over all 13,786 sorted "module\tsha256" lines: `f0623546…`.

**ctime** (inode change time; it cannot be set back by `touch`).
- **N66 stores.** The newest ctime is 17:48:47 in n66-level15 and 21:57:15 in n66-l15-rows. Both are before the
  n66-l15-rows review started (22:47). So the bytes imported here are the bytes that review compiled against. This
  closes the worker's "unless rewritten with an old mtime" caveat for the 140 oleans with no earlier pin.
- **Every other imported file except the two part-2 oleans** has a ctime before 22:00, when part 1's review started.
  The newest is `RS/Final3419.olean`, 19:10:41, through `links/`.
- **The two part-2 oleans** have ctimes of 23:51:54 and 23:59:03.

**Manifests** (coreutils `sha256sum -c`, all rc 0):
- n66-l15-rows `source_manifest` (148 entries) and `freeze_manifest` (152);
- n66-level15 `final_source_manifest` (59) and `freeze_manifest` (39).

The worker's `data/manifest2.sha256` checks clean (30 entries). Its part-1 `data/manifest.sha256` fails only on
README.md and REMAINS.md, as the worker states.

## 8. REMAINS.md, README and the worker's other claims

- **The per-bound lists equal the compiled binders exactly:**
  - ResidualBound 118 and 304: H-N66C, H-N66R, H-ROWS ×4, H-S3519, H-S3520 (8);
  - 303: H-T68 plus those 8;
  - 302: H-T69 plus those 8.

  No intermediate statement remains (§4).
- **The figures match the records:**
  - campaign_status `4802dc9a…`;
  - 105 leaves, vfy15 105/105;
  - T208 `T_849f8a5e23a1fc77`, `349b6c6c…`;
  - 812 + 208 + 35 + 970 = 2,025 rows;
  - s35_19, s35_20 and budget-68 tree sizes as in §6;
  - the b69 finder running.
- **Sources** `N66L15.lean` and `ES304L15.lean` contain none of the following: `sorry`, `admit`, `axiom` (outside
  `#print axioms`), `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`, `partial`, `macro`/`elab`, or
  attributes. Their hashes equal README §2.6.
- **The worker's disclosed stray file** `/tmp/x_unused` exists, has 0 bytes and is dated 00:01:02. It is harmless; the
  owner may delete it.
- **s35_19.** The worker checked at 23:40 and 00:01. I re-read `status.json` once, read-only, at 00:37:29, after the
  last unit. It is still not done, and the driver `esr-fvr-drv` is active. The switch is correctly left as a template.
- **Wording notes** (non-blocking; for the worker or the main session):
  1. README §2.1/STATUS2 and REMAINS.md say "part 2 not reviewed yet". This file is that review.
  2. The labels are right as worded. `CubesUnsat105R` and `RowCertsUnsat` are Lean statements about the full
     relaxation and certificate CNFs. The certified files are the trims and T208's sub-CNF, linked by the reviewed
     bridges. One sentence saying so, with a pointer to `RV5P2.es304_texts` (§5), would make that explicit. The
     n66-l15-rows label already names T208's trimmed sub-CNF.
  3. Repo records (FORMAL20261122 README, LEAN_STATUS) still need the main session's update. Rule 1 forbids that here.

## 9. What I did not check

- I did not re-run the trees (s35_19, s35_20, budget-68), the N66 campaign, or the full 105/628/2,025 bindings; I
  re-printed only a sample.
- I did not verify E3 (cake_lpr's parser = `parseDimacs`/`parseDimacsBytes`).
- I did not re-run the worker's `BadN66` control; I read its log.
- I imported the sibling and worker oleans. Lean does not re-check imported proofs, so my trust in the pieces rests on
  their hash pins and their own reviews. My re-elaborations re-check only the top-level compositions.
- `Switch3519L15.lean` (and part 1's `Switch3519.lean`) cannot be compiled before `RS.Final3519` exists.
- `RS.s34_19`'s own review is still pending, as carried over from part 1.

## 10. Files (sha256; all in `review/part2/`)

| file | sha256 |
|---|---|
| `lean/RV5P2Review.lean` | `c441ce9876438caa0235f6d9b2584d82a74f73d44c2ffefc881e9501e1b220fb` |
| `logs/RV5P2Review.log` | `66702a815fae4810cabe5a4f182e7874fdc5dc10b2f2d586eed129a720be68d1` |
| `data/audit_rv5p2.json` / `data/closure_rv5p2.tsv` | `304be1c7…` / `a84bae02…` |
| `data/bind_rv5p2.json` / `data/bind_rv5p2.tsv` | `b10de122…` / `8878cc67…` |
| `data/rv5p2_R1_15.txt` / `data/rv5p2_leaves105.txt` | `f45e25f1…` / `5f188424…` |
| `tools/rv5p2_audit.py` / `tools/rv5p2_bind.py` | `450d74d5…` / `c822a89a…` |
| `tools/env.sh` / `start.sh` / `unit_ax.sh` | `7fec3b28…` / `a92694c6…` / `eac3aaa6…` |

Other files: the fresh cake_lpr outputs are `logs/cake/*.out` (6), and the unit outputs are
`logs/{p2ax,p2aud,p2bind}.out` and `logs/gates.log`.

The temporary CNF/LRAT copies in `data/tmp/` were deleted after each run; the directory is empty.
