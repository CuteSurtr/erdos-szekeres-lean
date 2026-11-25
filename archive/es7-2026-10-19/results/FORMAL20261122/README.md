# FORMAL20261122: Lean formalizations of 22 November 2026 (sources, reviews, hash bindings)

> **Proof deletion (24 Nov 2026, owner OK):** the 4,405 kept proofs of the 182-vertex campaign (31.8 GB; the 4,404
> piece verdicts behind `V182Geo.chiRainbow_eq_six`, plus the k7 proof) are deleted after
> `evidence/v182-proof-receipts-20261124.tsv` was committed and pushed: per proof, the file hash and size, the
> decompressed LRAT hash recomputed on 24 Nov, and the independent re-check that had accepted exactly that proof
> (wave 1's verifier 1,624, v182-recheck 2,781). The N66 cube proofs behind `CubesUnsat132`/`CubesUnsat105R` go the same
> way (receipts in N66N20261113/receipts). Bindings this breaks: re-running cake_lpr on those proofs (trust item E2
> becomes "two recorded acceptances" instead of "re-runnable"). The Lean statements are unchanged.


**Status (23 Nov 2026, 00:50 KST): RECORD OF LEAN WORK; formalization waves 3 and 5 finished and reviewed.** The work was done in waves (owner: "formalize
everything", "lean verify everything"; end state for SAT-certificate parts: **Lean + cake_lpr**). Every item below
compiles with only `propext`, `Classical.choice` and `Quot.sound`, and had an independent statement-fidelity review
unless marked otherwise.

Nothing here is refereed. "Lean-checked modulo X" means that the Lean theorem takes X as a hypothesis. Verdicts of
cake_lpr enter only as named hypotheses on Lean-defined CNFs. The CNF bytes are bound by hash to the certified files
(trust items E1-E6 of ENCBLEAN).

## 1. What is Lean-checked

| result | Lean statement (main theorem) | what remains outside Lean | review |
|---|---|---|---|
| ES(8) ≤ 304 | `E304Z.Final.forces_304_of_n66_res : N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 304 8`; the tree hypothesis is discharged by `E304Z.Final.excludes_67` (FV304) | N66Bound 55, ResidualBound 118 | `fv304-audit` (closing audit: 13,199-module closure, one provider each) |
| ES(8) ≤ 304, refined | `FV4A.forces_304_of_slices_rows_n66` | N66Bound 55, BlockValid rowsP/Q/U/A, the six ResSliceExcludes | `fv304-audit` |
| ResidualBound 118 | `Res118.residual_bound_118_of_slices` | N66Bound 55, the four row blocks, six slices | `res118/review` |
| residual slices | `RS.s33_18`, `RS.s34_18`, `RS.s35_18` (reviewed); `RS.s34_19` (compiled, rc 0, standard axioms; review pending); compact checker on the existing slice trees | s35_19 (running), s35_20 | `res-slices-fv` (in the work dir; copied when finished) |
| Res118 row blocks | `RowGeo.blockValid_P/Q/U/A : RowsUnsat rowsX → BlockValid rowsX`; `RowGeo.residual_bound_118_of_texts` (ResidualBound 118 from N66Bound 55, the four blocks' printed texts and the six slices). Hash binding: 2,025 of 2,025 block rows (2,021 distinct supports) | the 2,025 per-row cake_lpr verdicts | `res118-rowblocks/review`: 5 of 5 confirmed. E2 evidence copied to `evidence/res118-rowblocks-e2/` (reviewer fix 1; 3,051 of 3,051 cake_lpr outputs carry the exact line); printer `rowprint` sha256 `eabe3791…` (fix 2) |
| N66 ≤ 55 | `N66Geo.n66_bound_55_of_cubes : CubesUnsat132 → RowsValid R0 → N66Bound 55`; byte identity re-run on the frozen exe: all MATCH (`n66enc-recheck`) | the 132 cube verdicts, RowsValid R0 | `n66enc/review`, `n66enc-recheck/verify` |
| N66 rows (level 14) | `RowGeo.rowsValid_R1 : RowCertsUnsat → RowsValid R1` (11,884 rows, 119 kernel-checked chunks) and `RowGeo.n66_bound_55_of_cubes_rows : CubesUnsat132 → RowCertsUnsat → R0Parse → N66Bound 55` | 629 row-CNF verdicts (`RowCertsUnsat`), and **`R0Parse`** (`N66Enc.R0 = R1`), a named hypothesis whose evidence is COMPUTED (`#eval`, E4-class): the kernel cannot evaluate n66enc's `include_str`/`String.splitOn` row list | `n66-rowsvalid/review`: 11 confirmed, 2 not confirmed: the target without R0Parse was not reached, and the T208 sub-list print was not independently reproduced (it needs about 3 GB). Quote the label with R0Parse named. Since wave 5 the end theorems take N66 from the level-15 row below, which has no R0Parse; T208 was reproduced on 22 Nov (`n66-rowsvalid/review/t208own`) and again by n66-l15-rows. |
| N66 ≤ 54 (level 15) | `N66G15.n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 → N66Bound 54` | the 105 cube verdicts, RowsValid R0_15 (not formalized); the plug into `composition_302_n54` is not compiled yet | `n66-level15/review`: 11 confirmed, 2 not claimed by the worker (RowsValid R0_15, the 302 plug). Both are closed by the next two rows. |
| N66 ≤ 54 and ≤ 55 without R0Parse (level 15) | `N66R15.n66_bound_54 : CubesUnsat105R → RowCertsUnsat → N66Bound 54` and `N66R15.n66_bound_55`. The 10,859 level-15 rows are Std-only chunk constants (109 chunks) that the kernel checks with `decide +kernel`; the cube printer reads the same constants (105 of 105 trims byte-identical to the certified files); no new certificate CNF was needed | the 105 level-15 cube verdicts and the 629 row-certificate verdicts (628 full CNFs plus the trimmed sub-CNF of template 208), under E1-E6 | `n66-l15-rows/review`: 13 confirmed, 1 not confirmed (the reviewer did not re-run the co-import compile; it is off the label's path); no fixes. The reviewer's own prints: 105/105 trims, 628/628 certificates and T208 byte-identical; own fresh cake_lpr 17/17 accepted, 2/2 negative controls rejected |
| end theorems for 304 / 303 / 302 | `Combined.es304 : N66Bound 55 → RowsTextUnsat rowsP/Q/U/A → s35_19 → s35_20 → ForcesConvexNGon 304 8` (the budget-67 tree is discharged by `E304Z.Final.excludes_67`); `Combined.es303` (adds `ExcludesHoleBudgetZZsF 68`); `Combined.es302` (adds `ExcludesHoleBudgetZZsN 16 69` and uses N66Bound 54; a conditional theorem until 24 Nov; since 24 Nov its tree hypothesis has evidence: the budget-69 tree is an EXACT TREE by two in-project checks, ES302N20261124, not in Lean); `Combined.residual_bound_118`; `Combined.n66Bound_mono` | as listed in each statement | `combined/review`: 8 confirmed (the five statements, each re-derived by an independent route; the CNF binding of the row texts, a sample of 20 with fresh cake_lpr; the import audit, 13,638 modules with one provider each; REMAINS.md), 2 not confirmed (H-T69 has no evidence; the s35_19 switch template is not compiled) |
| the same with the level-15 N66 | `Combined.es304_l15`, `es303_l15`, `es302_l15`, `residual_bound_118_l15`: one-line instances with `N66R15.n66_bound_55` (`_54` for 302) | 304: the 105 + 629 + 2,025 cake_lpr verdicts (E1-E6; E3 tested, not proved) and the slices s35_19 and s35_20 (EXACT TREE, not in Lean). 303: also the budget-68 tree (EXACT TREE by two checks, not in Lean; superseded by 302 and its tree deleted on 24 Nov, digest in ES303N). 302: also the budget-69 tree (EXACT TREE by two in-project checks since 24 Nov, ES302N20261124; not in Lean) | `combined/review/VERIFY_combined-2.md`: 8 confirmed, 2 not confirmed (the same two as part 1: H-T69 has no evidence, and `Switch3519L15.lean` is not compiled); no fixes. The reviewer's own sample: 14 of 14 printed items byte-identical to the certified files; fresh cake_lpr 5 of 5 accepted |
| s35_20 launch gate | `RS3520.U2080.root`: the context-level fact for ctx-4274, the largest context (320,422 leaves, 57 chunk modules), with no hypotheses; units 161 and 1793 also compile. That is 3 of 3,212 units (387,322 of 119,054,033 leaves); it is not `RS.s35_20`. The new exporter v3 writes the same bytes as the reference; the streamed pre-pass equals the T7 record on all 8,080 contexts | – (context-level fact only) | `s3520-gate/review`: 12 confirmed, 2 not confirmed: pre-registered acceptance item 3 was met only through re-prints (C208014, C208053); LAUNCH_PLAN §5's `FVR_JOBS=4` gives 4 compiles once the export ends, against its own §6.5. The 4 required fixes to LAUNCH_PLAN are not applied yet: apply them before any launch |
| 7-fold octagon case (64) | `EncB.Geo7.sevenfold_es8_of_text` (and `_order7_of_text`) | one cake_lpr verdict (the 7-8-10 CNF text) | `sevenfold/review` |
| 5-fold heptagon case (32; RESULTS C4; added 25 Nov 2026) | `EncB.Geo5.fivefold_heptagon_of_text` (and `_order5_of_text`, `_of_centre_not_mem_of_text`, `fivefold35_of_text`): the sevenfold's generic lemmas at (5,7,7) | one cake_lpr verdict (the 5-7-7 CNF text, CaDiCaL 2.1.3 on Linux, proof kept) | none beyond a negative control (`fivefold/README.md` §2); not reviewed |
| 182-vertex graph (#810) | `V182Geo.chiRainbow_eq_six : PieceVerdicts → chiRainbow = 6`; `rainbowColorable_six` has no hypothesis (kernel walk check) | the 4,404 piece verdicts | `v182-lean/review`: 5 of 5 confirmed |
| AE33 radius 1 | `AE33Geo.ae33_pair`, `AE33Geo.ae33_radius1` (and `ae33_radius0`) | `TextsUnsat203` (203 verdicts; the record has 194 distinct CNFs) | `ae33-lean/review`: 5 of 5 confirmed |
| 30x compositions | all 31 theorems of the nine composition files, rebuilt in one olean directory with an import audit | as stated per theorem | `comp-audit/review` |

## 2. Findings worth knowing

- **FV304 axiom check (`fv304-audit` §1).** FV304's own per-module check passed four chunk logs whose axiom line had
  been split by profiler output (C260801, C325201, C311801, C634501). All four were re-printed from their oleans with
  the standard axioms. Slice checks therefore read their acceptance from the Final module's axiom print.
- **Two docstrings are wrong** (no effect on proofs):
  - `ES306N20261119/Composition306.lean` attributes BalancedBound 186 to a stopped campaign;
  - "ExcludesHoleBudgetZZsF b is the statement a zero-side-only tree certifies" should read "follows from what the
    tree certifies" (`comp-audit/review`).

## 3. Files

- One folder per project, as in `/home/jay/research/data/formalize-20261122/<project>`. Each holds the Lean sources,
  tools, README/DESIGN, logs with axiom prints, and reviews.
- `SHA256SUMS` lists every file. Bulk runtime data was not copied: the printers' descriptor files and the large
  closure tables. Lean does not trust the descriptors, which are regenerable. These files are marked `NOT COPIED`
  with their hashes; the originals stay in the work directories.
- Not copied: oleans, builds, exported chunk sources (e.g. FV304's 20.7 GB export). They are regenerable from the
  sources here and the pinned toolchain. Since wave 5, any `.lean` or `.json` file over 1 MB is hash-only as well
  (generated chunk modules and skeletons, e.g. the s35_20 gate's negative-control copy).
- `evidence/sync_record.py` rebuilds a project folder from its work directory (`python3 -I sync_record.py <record>
  <project> ...`) and keeps the other folders and their SHA256SUMS entries.

## 4. Rebuild

Use each project's README ("Resume" or "rebuild" section). In short, compile the sources here with the pinned
`leanprover/lean4:v4.24.0` and Mathlib `f897ebcf` (the repo's `.lake`), using a read-only `LEAN_PATH` as described in
`comp-audit/README.md`. Never run `lake update`.

## 5. What remains (for "Lean + cake_lpr" end to end)

Done in wave 5: N66 without R0Parse (level 15), the T208 print (reproduced twice), the 302 plug (`Combined.es302_l15`,
conditional). What remains:

- **s35_19:** its Lean check runs unattended (`esr-fvr-drv`, 3 compiles; 626 of about 1,412 modules at 00:28 on 23 Nov,
  no root or final yet). When res-slices-fv accepts `RS.s35_19` (its README §9), compile
  `combined/src/Combined/Switch3519L15.lean` (recipe in `combined/README.md` §2.9; both switch templates are untested).
- **s35_20:** the gate passed, with pre-registered acceptance item 3 met only through re-prints; the campaign has
  not been launched. About 383-417 CPU-h, and 228-239 GB of disk with the
  chunk sources kept or about 140 GB without them (HEURISTIC, `s3520-gate/LAUNCH_PLAN.md`). Before launching: apply the
  review's 4 LAUNCH_PLAN fixes, and set `FVR_JOINMEM` from the s35_19 Root measurement. Owner decisions: more than 3
  compiles, and deleting chunk sources once their oleans exist.
- **Trees not in Lean:** budget 68 (for 303; EXACT TREE by two checks) and budget 69 (for 302; EXACT TREE by two
  in-project checks since 24 Nov, ES302N20261124).
- `RS.s34_19`: its own review is still pending.
- R0Parse remains in the level-14 theorem only. Plan M10 is no longer needed by the end theorems.
- E3 (cake_lpr parses each file as `EncB.parseDimacs` does) is tested, not proved, as in ENCBLEAN.

> **25 Nov 2026:** the 8,198 generated FV304 chunk sources were deleted on the owner's word (receipts and the
> regeneration test in ES304N20261119); FV304's compiled proof (`fv304-20261120/olean/E304Z`), its non-chunk sources and
> the 304 tree stay, so the sources can be regenerated byte for byte.
