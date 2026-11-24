# REMAINS: what each bound still rests on after `combined` part 2 (23 Nov 2026, 00:05 KST)

> **Update 24 Nov 2026 03:29 (main session): H-S3519 is dropped.** `RS.s35_19` was accepted by its finish recipe
> (23 Nov 16:30) and `src/Combined/Switch3519L15.lean` compiled (lean_rc 0; statement checks: 7 / 7 / 8 / 8 hypotheses,
> none mentions N66Bound; axiom guards passed); the import audit with MARKER_SWITCH2 reports no problems. The
> remaining slice is s35_20 (its Lean campaign runs). `Combined.es302_l15_s3519`: ES(8) <= 302 modulo the 105 + 629 +
> 2,025 cake_lpr verdicts, s35_20 and the budget-69 tree (FV302 in preparation).

> **Update 24 Nov 2026 (main session):** H-T69 now has evidence: the budget-69 tree is an EXACT TREE by two in-project
> checks (ES302N20261124), so `Combined.es302_l15` states ES(8) <= 302 with every hypothesis evidenced; the tree is not in
> Lean. H-T68's tree (b68zs) is deleted on 24 Nov (owner OK, after the 302 record); 303 is superseded by 302.

Labels follow es-research §2 (PROVED / CERTIFIED / EXACT TREE / COMPUTED / HEURISTIC). "Lean-checked" means
kernel-checked with axioms exactly `propext`, `Classical.choice`, `Quot.sound` (a `#guard_msgs` guard in each module).
Lean's kernel does not re-check imported oleans against their sources; the oleans imported here are pinned by sha256
(`data/closure2.tsv`, `data/audit2.json`). Nothing here is refereed, nothing here has been independently reviewed
yet (part 2), and **no bound and no record label changes**. Part 1's version of this file is kept unchanged in
`part1/REMAINS.md`.

## The end theorems (part 2: N66 from the level-15 verdicts)

| bound | Lean theorem (module) | label |
|---|---|---|
| ResidualBound 118 | `Combined.residual_bound_118_l15` (`Combined.N66L15`) | Lean-checked modulo H-N66C, H-N66R, H-ROWS (cake_lpr verdicts; trust items E1-E6), H-S3519, H-S3520 |
| ES(8) ≤ 304 | `Combined.es304_l15` (`Combined.ES304L15`) | Lean-checked modulo H-N66C, H-N66R, H-ROWS (E1-E6), H-S3519, H-S3520 |
| ES(8) ≤ 303 | `Combined.es303_l15` (`Combined.N66L15`) | Lean-checked modulo H-T68, H-N66C, H-N66R, H-ROWS (E1-E6), H-S3519, H-S3520 |
| ES(8) ≤ 302 | `Combined.es302_l15` (`Combined.N66L15`) | Lean-checked modulo H-T69, H-N66C, H-N66R, H-ROWS (E1-E6), H-S3519, H-S3520. **Not a bound claim**: H-T69 has no evidence yet |

The hypotheses of these four theorems are exactly the rows below: named cake_lpr verdict props (H-N66C, H-N66R,
H-ROWS), the slice exclusions not yet in Lean (H-S3519, H-S3520) and the trees not in Lean (H-T68, H-T69). No
`N66Bound`, `ResidualBound`, `BlockValid` or other intermediate statement is a hypothesis; the compile checks this
mechanically (hypothesis counts 8 / 8 / 9 / 9 and no binder mentioning `OmissionZRow.N66Bound`, `logs/N66L15.log`,
`logs/ES304L15.log`).

**N66 source.** The records cite N66 ≤ 55 from the 132 level-14 cubes (N66N20261113). This Lean form takes
`N66Bound 55` (304, 303, ResidualBound 118) and `N66Bound 54` (302) from the **105 level-15 verdicts** instead
(`N66R15.n66_bound_55`, the one-line corollary of `N66R15.n66_bound_54`). The level-14 Lean route
(`RowGeo.n66_bound_55_of_cubes_rows`, n66-rowsvalid) still has the COMPUTED hypothesis `R0Parse` and cannot share a
LEAN_PATH with res118-rowblocks (both use the `RowEnc`/`RowGeo` namespaces; at file level both stores have
`RowEnc/Main.olean`, `data/roots2.json`). No record label changes.

What is no longer a hypothesis (each Lean-checked by its own project, plugged in here):
- **`N66Bound 55` and `N66Bound 54`**: `N66R15.n66_bound_55` / `N66R15.n66_bound_54 : CubesUnsat105R →
  RowCertsUnsat → N66Bound _` (n66-l15-rows; confirmed by its review `review/VERIFY_n66-l15-rows.md`: statement,
  hash binding, non-vacuity, axioms). The level-15 relaxation, cube cover, counter, lex-leader argument and geometry
  are n66-level15's Lean proofs; `RowsValid R1_15` is proved from `RowCertsUnsat` over the kernel-checked chunk
  constants (no `R0Parse`, no `RowsValid` hypothesis);
- from part 1: the budget-67 tree (304; `E304Z.Final.excludes_67`, FV304), the four `BlockValid` row blocks (from
  their per-row verdicts, res118-rowblocks), Lemma A, h(F) ≥ 18 and the gluing (Res118), the slices `s33_18`,
  `s34_18`, `s35_18`, `s34_19` (`RS.*`, res-slices-fv; `RS.s34_19`'s own review still pending, as in part 1), the
  Z-row/Z*-row compositions (`composition_303_zzsf`, `composition_302_n54`, comp-audit).

## The remaining hypotheses

| id | Lean hypothesis (exact type) | used by | label today | evidence | Lean status |
|---|---|---|---|---|---|
| H-N66C | `cubes : N66R15Enc.CubesUnsat105R`, i.e. `∀ c ∈ N66E15.leaves105, ¬ EncB.DimacsSatisfiable (N66E15.fullCnf N66R15Enc.R1_15 c)` | all four | **CERTIFIED**: 105 level-15 cube leaves, exact cover, one cake_lpr `s VERIFIED UNSAT` per certified `trim.cnf`; independent verifier vfy15: fresh cake_lpr 105/105 | N66N20261113/cubes20261120 §8; hash binding of the printed trims to the certified files 105/105 (n66-l15-rows M9; re-printed by its reviewer, 105/105 byte-identical) | a named cake_lpr verdict prop. Its meaning in terms of the certified bytes is the Lean theorem `N66R15.cubesUnsat105R_of_texts` (each leaf's printed `render nvHeader L` refuted ⇒ `CubesUnsat105R`); trust items E1-E6 |
| H-N66R | `certs : N66R15Geo.RowCertsUnsat`, i.e. `(∀ t ∈ N66R15Enc.templates, ¬ DimacsSatisfiable (certCnf t)) ∧ ∀ k ∈ N66R15Enc.cores, ¬ DimacsSatisfiable (certCnf k)` (421 templates, 208 cores) | all four | **CERTIFIED**: 629 row-certificate verdicts, namely **628 full CNFs plus the trimmed sub-CNF of template T208** (`T_849f8a5e23a1fc77`, `349b6c6c…`) | VB's records (exact line 628/628 and T208's `.trimmed.cake.out`); n66-rowsvalid's fresh cake_lpr 629/629; n66-l15-rows' fresh run on the 161 certificates the 595 new rows use, 161/161; its reviewer's fresh sample 13/13; printed texts = VB's CNFs 629/629 (m9rows; reviewer 628/628 + T208) | a named cake_lpr verdict prop; meaning via `N66R15.rowCertsUnsat_of_texts` (T208 through `subUnsat_of_text`, any index list); trust items E1-E6 |
| H-ROWS | `hP : RowGeo.RowsTextUnsat Res118.rowsP`, `hQ : … rowsQ`, `hU : … rowsU`, `hA : … rowsA` (812 + 208 + 35 + 970 = 2,025 rows, 2,021 distinct supports) | all four | **CERTIFIED** per row (one cake_lpr verdict each) | as in part 1: T4 re-check jobs ES307 v169 (1,994 accepted, `f80a720e…`) and VERIFY307 b35s19-v16 (1,057 accepted, `7b8d9eca…`); printed text = certified CNF 2,025/2,025 (res118-rowblocks M9, re-run by its reviewer); cake outputs in `FORMAL20261122/evidence/res118-rowblocks-e2/`. The cut-row LRATs named in the T4 TSVs are now stored as `.lrat.zst` (same content hash; part 1 review nit 2) | a named cake_lpr verdict prop on the bytes `rowprint row B I` writes (`rowprint` `eabe3791…`); trust items E1-E6 |
| H-S3519 | `s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19` | all four | **EXACT TREE** (fresh_replay_v3: 15,533,581 nodes, 7,763,207 leaves, minimum margin 1; tcheck_b35 + pycheck_b35, VB CONFIRMED) | tree `es308-20261114/runs/b35s19/bb` (master `249497e8…`), rows `inputs/b35s19-v16/extra.json` (`1257c4a1…`) | **Lean check running** in res-slices-fv (`RS.s35_19`; driver `esr-fvr-drv`). Its `status.json` at 00:01:07 (23 Nov): `done` = s33_18, s34_18, s34_19, s35_18; slice 3519 at 557 modules done, root and final not built; no `RS_Final3519.log`. Switch: uncompiled template `src/Combined/Switch3519L15.lean` (README §2.9 recipe) |
| H-S3520 | `s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20` | all four | **EXACT TREE by three implementations** (ES307 T5-T7: 238,116,145 nodes, 119,054,034 leaves, minimum margin 1; VR CONFIRMED) | tree `es308-20261114/runs/b35s20/bb-s1` (master `71993a47…`), rows `inputs/b35s20-v169/extra.json` (`de4bcceb…`) | **not started** (as in part 1: catalog and bridge `RS.cat3520_ok` built; cost about 360-440 CPU-h and 140-297 GB, HEURISTIC) |
| H-T68 | `tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68` | 303 | **EXACT TREE by two independent checks** (check_tree via v5 and balcheck2: 32,765 files, 246,300,833 nodes, 123,166,799 leaves, minimum margin 1, cover complete) | ES303N20261120 §5 | not started |
| H-T69 | `tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69` | 302 | **none yet** (no label: the tree does not exist) | the b69 finder `esr-bal-zbs69` is still active (checked 00:02, 23 Nov); its run directory was not read | not started |

**Trust items** (ENCBLEAN wording) for H-N66C, H-N66R and H-ROWS:
- **E1**: the printers' output equals the certified bytes. Checked: rows 2,025/2,025 (`rowprint`); N66 cube trims
  105/105 (`n66r15print` `65865b1e…`); N66 certificates 629/629 (`r15rowprint` `6b9af2c6…`).
- **E2**: the cake_lpr verdicts (exact line `s VERIFIED UNSAT`).
- **E3**: cake_lpr parses each file as `EncB.parseDimacs` / `parseDimacsBytes` does. Tested, **not proved**.
- **E4**: the Lean compiler and runtime of the three printers.
- **E5**: the kernel, Mathlib `f897ebcf` and the definitions.
- **E6**: SHA-256.

## Per bound, the exact remaining list (part 2 forms)

- **ResidualBound 118** (`Combined.residual_bound_118_l15`): H-N66C, H-N66R, H-ROWS, H-S3519, H-S3520.
- **ES(8) ≤ 304** (`Combined.es304_l15`): H-N66C, H-N66R, H-ROWS, H-S3519, H-S3520.
  Label: **Lean-checked modulo the cake_lpr verdict hypotheses `CubesUnsat105R` (105 level-15 cube verdicts),
  `RowCertsUnsat` (629 row-certificate verdicts: 628 full CNFs plus the trimmed sub-CNF of T208) and
  `RowsTextUnsat rowsP/Q/U/A` (2,025 row verdicts), trust items E1-E6 (E3 not proved), and the slice exclusions
  `s35_19` and `s35_20` (EXACT TREE, not in Lean).**
- **ES(8) ≤ 303** (`Combined.es303_l15`): H-T68 and the same five. Label: the 304 label plus **`ExcludesHoleBudgetZZsF 68`
  (EXACT TREE by two checks, not in Lean)**. The budget-67 tree is not used.
- **ES(8) ≤ 302** (`Combined.es302_l15`): H-T69 and the same five. Label: the 304 label plus
  **`ExcludesHoleBudgetZZsN 16 69` (no evidence yet)**. A conditional theorem only, until the budget-69 tree exists
  and passes its checks; **not a bound claim**.

After the s35_19 switch, H-S3519 disappears from all four (theorems `Combined.*_l15_s3519`).

## Part 1 forms (still valid, unchanged)

`Combined.residual_bound_118`, `Combined.es304`, `Combined.es303`, `Combined.es302` keep `N66Bound 55` (or 54) as a
hypothesis, with the lists of `part1/REMAINS.md` (H-N55 / H-N54 there). They remain useful for an N66 proof that is
not the level-15 one; the part 2 theorems are these four with the N66 slot filled.

## Corrections to part 1's wording (part 1 review nits)

- `RS.Lib`'s olean (`952b115c…`) was called "first recorded here". An earlier record of the same hash exists:
  res-slices-fv `verify/tools/overlay_targets.sha256` line 18 (18:14:58, 22 Nov).
- The T4 TSVs name cut-row LRATs as `system.lrat`; they are now stored as `system.lrat.zst` with the same content
  hash. Anyone re-running E2 must read the `.zst` name (affects the keep-set wording, not the evidence).
