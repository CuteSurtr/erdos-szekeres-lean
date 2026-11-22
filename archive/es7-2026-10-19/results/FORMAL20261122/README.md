# FORMAL20261122: Lean formalizations of 22 November 2026 (sources, reviews, hash bindings)

**Status (22 Nov 2026, about 20:00 KST): RECORD OF LEAN WORK.** The work was done in waves (owner: "formalize
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
| Res118 row blocks | BlockValid rowsP/Q/U/A from per-row CNF verdicts (`res118-rowblocks`) | the per-row cake_lpr verdicts | `res118-rowblocks/review` |
| N66 ≤ 55 | `N66Geo.n66_bound_55_of_cubes : CubesUnsat132 → RowsValid R0 → N66Bound 55`; byte identity re-run on the frozen exe: all MATCH (`n66enc-recheck`) | the 132 cube verdicts, RowsValid R0 (being formalized) | `n66enc/review`, `n66enc-recheck/verify` |
| N66 ≤ 54 (level 15) | `N66G15.n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 → N66Bound 54` | the 105 cube verdicts, RowsValid R0_15; the plug into `composition_302_n54` is not compiled yet | `n66-level15/review` (11/13; 2 not claimed) |
| 7-fold octagon case (64) | `EncB.Geo7.sevenfold_es8_of_text` (and `_order7_of_text`) | one cake_lpr verdict (the 7-8-10 CNF text) | `sevenfold/review` |
| 182-vertex graph (#810) | χ_rainbow(G) = 6; the 6-colouring is unconditional (`decide`) | the 4,404 piece verdicts | `v182-lean/review` |
| AE33 radius 1 | `AE33Geo.ae33_pair`, `AE33Geo.ae33_radius1` (and `ae33_radius0`) | `TextsUnsat203` (203 verdicts) | review pending |
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
  sources here and the pinned toolchain.

## 4. Rebuild

Use each project's README ("Resume" or "rebuild" section). In short, compile the sources here with the pinned
`leanprover/lean4:v4.24.0` and Mathlib `f897ebcf` (the repo's `.lake`), using a read-only `LEAN_PATH` as described in
`comp-audit/README.md`. Never run `lake update`.

## 5. What remains (for "Lean + cake_lpr" end to end)

- RowsValid R0 / R0_15 (N66 rows): the `n66-rowsvalid` project is running.
- Slices s35_19 (running) and s35_20 (4,642 rows exceed the exporter's 12-bit assert; feasibility under test).
- N66 ≤ 54 plugged into `composition_302_n54`, plus the 302 tree check once the budget-69 tree has passed both checks.
