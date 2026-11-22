# REMAINS: what each bound still rests on after `combined` part 1 (22 Nov 2026)

Labels follow es-research §2 (PROVED / CERTIFIED / EXACT TREE / COMPUTED / HEURISTIC). "Lean-checked" means
kernel-checked, axioms exactly `propext`, `Classical.choice`, `Quot.sound` (`#guard_msgs` in each module). Lean's
kernel does not re-check imported oleans against their sources; the oleans imported here are pinned by sha256
(`data/closure.tsv`, `data/audit.json`). Nothing here is refereed, and no bound or record label changes.

## The four end theorems (this directory, `src/Combined/*.lean`)

| bound | Lean theorem | label |
|---|---|---|
| ResidualBound 118 | `Combined.residual_bound_118` (module `Combined.Residual`) | Lean-checked modulo H-N55, H-ROWS (with trust items E1-E6), H-S3519, H-S3520 |
| ES(8) ≤ 304 | `Combined.es304` (module `Combined.ES304`) | Lean-checked modulo H-N55, H-ROWS (E1-E6), H-S3519, H-S3520 |
| ES(8) ≤ 303 | `Combined.es303` (module `Combined.ES303`) | Lean-checked modulo H-T68, H-N55, H-ROWS (E1-E6), H-S3519, H-S3520 |
| ES(8) ≤ 302 | `Combined.es302` (module `Combined.ES302`) | Lean-checked modulo H-T69, H-N54, H-ROWS (E1-E6), H-S3519, H-S3520. **Not a bound claim**: H-T69 has no evidence yet |

What is no longer a hypothesis (each already Lean-checked by its own project, plugged in here):
- the budget-67 tree `ExcludesHoleBudgetZ 67` (304 only): `E304Z.Final.excludes_67`, inside
  `E304Z.Final.forces_304_of_n66_res` (FV304; closing import audit `fv304-audit`);
- the four `BlockValid` row blocks: from their per-row CNF verdicts by `RowGeo.blockValid_*` and
  `RowGeo.rowsUnsat_of_texts` (res118-rowblocks; the encoder soundness that was written before is now Lean);
- Lemma A (Lo half), h(F) ≥ 18 and the gluing of the six splits (Res118);
- the slices `s33_18`, `s34_18`, `s35_18`, `s34_19`: `RS.s33_18`, `RS.s34_18`, `RS.s35_18`, `RS.s34_19`
  (res-slices-fv, compact checker). The first three are reviewed (`res-slices-fv/verify/VERIFY_res-slices-fv.md`).
  **`RS.s34_19` is plugged in with its own review pending**: its statement match is checked here by Lean (it is
  accepted as Res118's argument `s34_19`), and `verify/VERIFY_s35_19.md` check 4a confirmed the live four-slice
  specialisation that uses it; its chunk logs were audited by the worker only (`tools/axlines.py`: 4 split axiom
  lines re-printed standard);
- the Z-row / Z*-row and the balanced half of 303/302 (`composition_303_zzsf`, `composition_302_n54`, comp-audit);
- `N66Bound 54 → N66Bound 55` (`Combined.n66Bound_mono`, here).

## The remaining hypotheses

| id | Lean hypothesis (exact type) | used by | label today | evidence | Lean status |
|---|---|---|---|---|---|
| H-N55 | `n66 : OmissionZRow.N66Bound 55` | 304, 303, ResidualBound 118 | **CERTIFIED** (132 cube leaves, cake_lpr, cover complete) + **PROVED** (written model) | N66N20261113 (and cubes20261115); claim `n66-le55-cubes-1118` CONFIRMED by VS and VN (LEAN_STATUS §4.4) | `N66Geo.n66_bound_55_of_cubes : CubesUnsat132 → RowsValid R0 → N66Bound 55` (n66enc) and `RowGeo.n66_bound_55_of_cubes_rows : CubesUnsat132 → RowCertsUnsat → R0Parse → N66Bound 55` (n66-rowsvalid; R0Parse is COMPUTED, E4-class). Not plugged in: part 2 will use the level-15 theorem of `n66-l15-rows` (target without R0Parse). n66-rowsvalid's `RowEnc.*`/`RowGeo.*` share module names and namespaces with res118-rowblocks', so the two cannot be on one LEAN_PATH |
| H-N54 | `n54 : OmissionZRow.N66Bound 54` | 302 | **CERTIFIED** (105 leaves, exact cover; independent verifier vfy15: fresh cake_lpr 105/105) + **PROVED** (written model, L = 15) | N66N20261113/cubes20261120 §8 (F_c `2f78368f…`) | `N66G15.n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 → N66Bound 54` (n66-level15; RowsValid R0_15 not formalised); `n66-l15-rows` in progress |
| H-ROWS | `hP : RowGeo.RowsTextUnsat Res118.rowsP`, `hQ : … rowsQ`, `hU : … rowsU`, `hA : … rowsA` (812 + 208 + 35 + 970 = 2,025 rows, 2,021 distinct supports) | all four | **CERTIFIED** per row (one cake_lpr verdict each) | T4 re-check jobs: ES307 v169 (1,994 jobs ACCEPTED, summary `f80a720e…`) and VERIFY307 b35s19-v16 (1,057 jobs ACCEPTED, summary `7b8d9eca…`); hash binding of the printed text to the certified CNF 2,025/2,025 (res118-rowblocks M9, re-run by its reviewer); cake outputs copied to `FORMAL20261122/evidence/res118-rowblocks-e2/` (3,051 of 3,051 with the exact line) | the meaning of each verdict is a Lean statement about the bytes `rowprint row B I` writes; trust items **E1** (printer output = certified bytes: checked for all 2,025), **E2** (cake_lpr verdicts), **E3** (cake_lpr parses each file as `EncB.parseDimacsBytes` does: **not verified**, as in ENCBLEAN), **E4** (Lean compiler/runtime of the printer), **E5** (kernel, Mathlib `f897ebcf`, the definitions), **E6** (SHA-256) |
| H-S3519 | `s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19` | all four | **EXACT TREE** (fresh_replay_v3: 15,533,581 nodes, 7,763,207 leaves, minimum margin 1; tcheck_b35 + pycheck_b35, VB CONFIRMED) | tree `es308-20261114/runs/b35s19/bb` (master `249497e8…`), rows `inputs/b35s19-v16/extra.json` (`1257c4a1…`); res118 README §4 | **Lean check running** in res-slices-fv (`RS.s35_19`, pre-registered 19:50; driver `esr-fvr-drv`; HEURISTIC end 23 Nov 05:00-08:30 KST). Switch: `src/Combined/Switch3519.lean` (README "s35_19 switch") |
| H-S3520 | `s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20` | all four | **EXACT TREE by three implementations** (ES307 T5-T7: 238,116,145 nodes, 119,054,034 leaves, minimum margin 1; VR CONFIRMED) | tree `es308-20261114/runs/b35s20/bb-s1` (master `71993a47…`), rows `inputs/b35s20-v169/extra.json` (`de4bcceb…`) | **not started.** Catalog and bridge `RS.cat3520_ok` (4,642 rows) built; 13-bit exporter built and controlled; six break points listed in res-slices-fv §8; cost about 360-440 CPU-h and 140-297 GB (HEURISTIC) |
| H-T68 | `tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68` | 303 | **EXACT TREE by two independent checks** (check_tree via v5 and balcheck2: 32,765 files, 246,300,833 nodes, 123,166,799 leaves, minimum margin 1, cover complete) | ES303N20261120 §5 | not started ("FV303 skipped because 302 supersedes it", STATUS20261121_1930) |
| H-T69 | `tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69` | 302 | **none yet** (no label: the tree does not exist) | STATUS20261121_1930: the b69 finder runs as `esr-bal-zbs69` since 22 Nov 16:25 (still active at 21:22); checks prepared in `bal186-20261119/b69prep` (review 6/6). Not read here: the run directory is being written | not started (FV302 after b69's checks) |

## Per bound, the exact remaining list

- **ResidualBound 118** (`Combined.residual_bound_118`): H-N55, H-ROWS (2,025 verdicts; E1-E6, E3 unverified),
  H-S3519, H-S3520.
- **ES(8) ≤ 304** (`Combined.es304`): H-N55, H-ROWS, H-S3519, H-S3520. Compared with `FV4A.forces_304_of_slices_rows_n66`,
  the four `BlockValid` became H-ROWS and four of the six slices are gone.
- **ES(8) ≤ 303** (`Combined.es303`): H-T68, H-N55, H-ROWS, H-S3519, H-S3520. The budget-67 tree is not used.
- **ES(8) ≤ 302** (`Combined.es302`): H-T69, H-N54, H-ROWS, H-S3519, H-S3520. A conditional theorem only, until the
  budget-69 tree exists and passes its checks.

After the s35_19 switch, H-S3519 disappears from all four (theorems `Combined.*_s3519`).
