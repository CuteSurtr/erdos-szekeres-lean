# REMAINS: what each bound still rests on after `combined` part 2 (23 Nov 2026, 00:05 KST)

> **Update 26 Nov 2026 10:50 (main session): part 3 accepted. ES(8) ≤ 302 has an end theorem whose only hypotheses
> are cake_lpr verdict props.** `Combined.es302_verdicts` (`src/Combined/ES302Final.lean`, `950be932…`, PART3.md)
> compiled: lean_rc 0, three axiom guards [propext, Classical.choice, Quot.sound], four type-pinning `example`s, and
> the `#check` equal to PART3.md §2. Its six hypotheses are H-N66C, H-N66R and H-ROWS (`hP`, `hQ`, `hU`, `hA`), so the
> budget-69 tree (H-T69) and the slice s35_20 (H-S3520) are no longer hypotheses. The control `controls/Bad302.lean`,
> the same term at 301, fails with exactly one error, the type mismatch. The import audit over the 69,731-module
> closure reports `"problems": []`: every module comes from one root, every olean hash equals its pin, and part 2's
> 15,205-module closure is inside with the same files and hashes. PART3.md §6 items 1-3 hold, and the advisor was
> consulted (es-research §7).
> **Label (PART3.md §6.4): ES(8) ≤ 302, Lean-checked modulo 2,759 cake_lpr verdicts (H-N66C 105, H-N66R 629,
> H-ROWS 2,025) and trust items E1-E6 (E3 tested, not proved).**
> Limits:
> - Unrefereed; part 3 has had no review of any kind (parts 1 and 2 each had an in-project review,
>   `review/VERIFY_combined*.md`).
> - One build on one machine; the imported oleans are hash-pinned, not recompiled.
> - The 105 N66 cube proofs (H-N66C), deleted on 24 Nov, were re-solved with the proofs kept: 105/105 CERTIFIED,
>   26 Nov 06:13.
>
> Details: "Part 3" below and README.md "Part 3".

## The end theorems (part 3: the budget-69 tree and s35_20 discharged, 26 Nov 2026)

| bound | Lean theorem (module `Combined.ES302Final`) | hypotheses | label |
|---|---|---|---|
| ES(8) ≤ 302 | `Combined.es302_verdicts` | 6: H-N66C, H-N66R, H-ROWS (4) | Lean-checked modulo H-N66C, H-N66R, H-ROWS (2,759 cake_lpr verdicts; trust items E1-E6) |
| ES(8) ≤ 304 | `Combined.es304_verdicts` | the same 6 | the same |
| ResidualBound 118 | `Combined.residual_bound_118_verdicts` | the same 6 | the same |

ES(8) ≤ 303 has no part-3 form: 302 supersedes it, and its tree (H-T68) was deleted on 24 Nov. `src/Audit3.lean`
re-checks the three statements mechanically: 6 hypotheses each, and none mentions `OmissionZRow.N66Bound`,
`ExcludesHoleBudgetZZsN` or `Res118.ResSliceExcludes` (`logs/Audit3.log`, STMT lines). The part-2 tables below stay
valid for the part-2 forms.

> **Update 25 Nov 2026 ~20:45 (main session): H-T69 has a Lean proof.** FV302 was accepted: `E302ZZ.Final.excludes_69`
> proves the budget-69 tree statement with standard axioms. The next step, part 3 (PART3.md), plugs it and `RS.s35_20`
> into `es302_l15_s3519`; s35_20's Root join aborted twice on 25 Nov (stack overflow) and is being rebuilt as sub-roots.

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
| ResidualBound 118 | `Combined.residual_bound_118_l15_s3519` (`Combined.Switch3519L15`) | Lean-checked modulo H-N66C, H-N66R, H-ROWS (cake_lpr verdicts; trust items E1-E6), H-S3520 |
| ES(8) ≤ 304 | `Combined.es304_l15_s3519` (`Combined.Switch3519L15`) | Lean-checked modulo H-N66C, H-N66R, H-ROWS (E1-E6), H-S3520 |
| ES(8) ≤ 303 | `Combined.es303_l15_s3519` (`Combined.Switch3519L15`) | Lean-checked modulo H-T68, H-N66C, H-N66R, H-ROWS (E1-E6), H-S3520 |
| ES(8) ≤ 302 | `Combined.es302_l15_s3519` (`Combined.Switch3519L15`) | Lean-checked modulo H-T69, H-N66C, H-N66R, H-ROWS (E1-E6), H-S3520 |

(Switch of 24 Nov 2026, recipe §2.9 steps 1-6: `RS.s35_19` is in Lean, so H-S3519 is no longer a hypothesis. The
part-2 forms `Combined.residual_bound_118_l15`, `es304_l15`, `es303_l15`, `es302_l15` remain valid with H-S3519 as an
extra hypothesis. The state before this step: `part2/REMAINS.before-switch-step6.md`.)

The hypotheses of these four theorems are exactly the rows below: named cake_lpr verdict props (H-N66C, H-N66R,
H-ROWS), the slice exclusion not yet in Lean (H-S3520) and the trees not in Lean (H-T68, H-T69). No
`N66Bound`, `ResidualBound`, `BlockValid` or other intermediate statement is a hypothesis; the compile checks this
mechanically (hypothesis counts 7 / 7 / 8 / 8 for the `_s3519` forms, and no binder mentioning `OmissionZRow.N66Bound`,
`logs/Switch3519L15.log`; the part-2 forms: 8 / 8 / 9 / 9, `logs/N66L15.log`, `logs/ES304L15.log`).

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
| H-N66C | `cubes : N66R15Enc.CubesUnsat105R`, i.e. `∀ c ∈ N66E15.leaves105, ¬ EncB.DimacsSatisfiable (N66E15.fullCnf N66R15Enc.R1_15 c)` | all four | **CERTIFIED**: 105 level-15 cube leaves, exact cover, one cake_lpr `s VERIFIED UNSAT` per certified `trim.cnf`; second acceptance vfy15 (copies of VB's tools, not independent code): fresh cake_lpr 105/105. The 105 proofs deleted on 24 Nov (receipts N66N20261113/receipts) were **re-solved on 25-26 Nov with the proofs kept** (`n66-resolve-20261125`: each `trim.cnf` = its receipt hash; the 105 texts, 98 distinct, = the multiset M9 binds; CaDiCaL 2.1.3, cake_lpr `s VERIFIED UNSAT` 105/105 at 06:13 on 26 Nov; 121 GB zstd) | N66N20261113/cubes20261120 §8; hash binding of the printed trims to the certified files 105/105 (n66-l15-rows M9; re-printed by its reviewer, 105/105 byte-identical) | a named cake_lpr verdict prop. Its meaning in terms of the certified bytes is the Lean theorem `N66R15.cubesUnsat105R_of_texts` (each leaf's printed `render nvHeader L` refuted ⇒ `CubesUnsat105R`); trust items E1-E6 |
| H-N66R | `certs : N66R15Geo.RowCertsUnsat`, i.e. `(∀ t ∈ N66R15Enc.templates, ¬ DimacsSatisfiable (certCnf t)) ∧ ∀ k ∈ N66R15Enc.cores, ¬ DimacsSatisfiable (certCnf k)` (421 templates, 208 cores) | all four | **CERTIFIED**: 629 row-certificate verdicts, namely **628 full CNFs plus the trimmed sub-CNF of template T208** (`T_849f8a5e23a1fc77`, `349b6c6c…`) | VB's records (exact line 628/628 and T208's `.trimmed.cake.out`); n66-rowsvalid's fresh cake_lpr 629/629; n66-l15-rows' fresh run on the 161 certificates the 595 new rows use, 161/161; its reviewer's fresh sample 13/13; printed texts = VB's CNFs 629/629 (m9rows; reviewer 628/628 + T208) | a named cake_lpr verdict prop; meaning via `N66R15.rowCertsUnsat_of_texts` (T208 through `subUnsat_of_text`, any index list); trust items E1-E6 |
| H-ROWS | `hP : RowGeo.RowsTextUnsat Res118.rowsP`, `hQ : … rowsQ`, `hU : … rowsU`, `hA : … rowsA` (812 + 208 + 35 + 970 = 2,025 rows, 2,021 distinct supports) | all four | **CERTIFIED** per row (one cake_lpr verdict each) | as in part 1: T4 re-check jobs ES307 v169 (1,994 accepted, `f80a720e…`) and VERIFY307 b35s19-v16 (1,057 accepted, `7b8d9eca…`); printed text = certified CNF 2,025/2,025 (res118-rowblocks M9, re-run by its reviewer); cake outputs in `FORMAL20261122/evidence/res118-rowblocks-e2/`. The cut-row LRATs named in the T4 TSVs are now stored as `.lrat.zst` (same content hash; part 1 review nit 2) | a named cake_lpr verdict prop on the bytes `rowprint row B I` writes (`rowprint` `eabe3791…`); trust items E1-E6 |
| H-S3519 | `s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19` | none since the switch (was: all four) | **EXACT TREE** (fresh_replay_v3: 15,533,581 nodes, 7,763,207 leaves, minimum margin 1; tcheck_b35 + pycheck_b35, VB CONFIRMED) | tree `es308-20261114/runs/b35s19/bb` (master `249497e8…`), rows `inputs/b35s19-v16/extra.json` (`1257c4a1…`) | **in Lean**: `RS.s35_19` (res-slices-fv, accepted by its finish recipe 23 Nov 16:30), used by `Combined.Switch3519L15` (compiled 24 Nov 03:22, audit 03:28) |
| H-S3520 | `s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20` | all four | **EXACT TREE by three implementations** (ES307 T5-T7: 238,116,145 nodes, 119,054,034 leaves, minimum margin 1; VR CONFIRMED) | tree `es308-20261114/runs/b35s20/bb-s1` (master `71993a47…`), rows `inputs/b35s20-v169/extra.json` (`de4bcceb…`) | **Lean-checked** since 26 Nov: `RS.s35_20` (res-slices-fv, finish recipe ok 01:14:41); discharged in `Combined.ES302Final` (part 3) |
| H-T68 | `tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68` | 303 | **EXACT TREE by two in-project checks** (check_tree via v5 and balcheck2: 32,765 files, 246,300,833 nodes, 123,166,799 leaves, minimum margin 1, cover complete); the tree b68zs was deleted on 24 Nov, so it cannot be re-checked or put into Lean (corrected 25 Nov) | ES303N20261120 §5 | not started |
| H-T69 | `tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69` | 302 | **EXACT TREE by two in-project checks** (check A v5n54 + check B balcheck2: 32,618 files, 87,902,270 nodes, 43,967,444 leaves, minimum margin 1, cover complete; ACCEPT302 24 Nov 01:43) | ES302N20261124 §4 | **Lean-checked** since 25 Nov: `E302ZZ.Final.excludes_69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69` (FV302 ACCEPTED ~20:40 by its pre-registered items 1-4; FORMAL20261122/fv302). Discharged in `Combined.ES302Final` (part 3, 26 Nov) |

**Trust items** (ENCBLEAN wording) for H-N66C, H-N66R and H-ROWS:
- **E1**: the printers' output equals the certified bytes. Checked: rows 2,025/2,025 (`rowprint`); N66 cube trims
  105/105 (`n66r15print` `65865b1e…`); N66 certificates 629/629 (`r15rowprint` `6b9af2c6…`).
- **E2**: the cake_lpr verdicts (exact line `s VERIFIED UNSAT`). Second check (25 Nov 2026,
  [LEANLRAT20261125](../../LEANLRAT20261125/README.md)): all 2,025 H-ROWS and all 629 H-N66R kept proofs are also
  accepted by Lean core's verified checker `Std.Tactic.BVDecide.LRAT.check` (run natively, on the texts of the frozen
  printers, hash-checked); H-N66C (105) is not covered: its proofs were re-solved on 25-26 Nov and are kept, but at up to about 10 GB raw each they
  exceed that checker's memory (it loads a whole proof).
- **E3**: cake_lpr parses each file as `EncB.parseDimacs` / `parseDimacsBytes` does. Tested, **not proved**.
- **E4**: the Lean compiler and runtime of the three printers.
- **E5**: the kernel, Mathlib `f897ebcf` and the definitions.
- **E6**: SHA-256.

## Per bound, the exact remaining list (part 3 forms)

- **ES(8) ≤ 302, ES(8) ≤ 304, ResidualBound 118** (`Combined.es302_verdicts`, `es304_verdicts`,
  `residual_bound_118_verdicts`): H-N66C, H-N66R, H-ROWS. Nothing else.

## Per bound, the exact remaining list (part 2 forms)

- **ResidualBound 118** (`Combined.residual_bound_118_l15_s3519`): H-N66C, H-N66R, H-ROWS, H-S3520.
- **ES(8) ≤ 304** (`Combined.es304_l15_s3519`): H-N66C, H-N66R, H-ROWS, H-S3520.
  Label: **Lean-checked modulo the cake_lpr verdict hypotheses `CubesUnsat105R` (105 level-15 cube verdicts),
  `RowCertsUnsat` (629 row-certificate verdicts: 628 full CNFs plus the trimmed sub-CNF of T208) and
  `RowsTextUnsat rowsP/Q/U/A` (2,025 row verdicts), trust items E1-E6 (E3 not proved), and the slice exclusion
  `s35_20` (EXACT TREE, not in Lean; its Lean campaign runs since 24 Nov 01:28).**
- **ES(8) ≤ 303** (`Combined.es303_l15_s3519`): H-T68 and the same four. Label: the 304 label plus **`ExcludesHoleBudgetZZsF 68`
  (EXACT TREE by two checks, not in Lean)**. The budget-67 tree is not used.
- **ES(8) ≤ 302** (`Combined.es302_l15_s3519`): H-T69 and the same four. Label: the 304 label plus
  **`ExcludesHoleBudgetZZsN 16 69` (EXACT TREE by two in-project checks, ES302N20261124, 24 Nov; not in Lean: FV302,
  the Lean check of the tree, runs since 24 Nov 04:47, `~/research/data/fv302-20261124`)**.

H-S3519 was dropped from all four by the s35_19 switch (24 Nov 2026; theorems `Combined.*_l15_s3519`).

## Part 1 forms (still valid, unchanged)

`Combined.residual_bound_118`, `Combined.es304`, `Combined.es303`, `Combined.es302` keep `N66Bound 55` (or 54) as a
hypothesis, with the lists of `part1/REMAINS.md` (H-N55 / H-N54 there). They remain useful for an N66 proof that is
not the level-15 one; the part 2 theorems are these four with the N66 slot filled.

## Corrections to part 1's wording (part 1 review nits)

- `RS.Lib`'s olean (`952b115c…`) was called "first recorded here". An earlier record of the same hash exists:
  res-slices-fv `verify/tools/overlay_targets.sha256` line 18 (18:14:58, 22 Nov).
- The T4 TSVs name cut-row LRATs as `system.lrat`; they are now stored as `system.lrat.zst` with the same content
  hash. Anyone re-running E2 must read the `.zst` name (affects the keep-set wording, not the evidence).
