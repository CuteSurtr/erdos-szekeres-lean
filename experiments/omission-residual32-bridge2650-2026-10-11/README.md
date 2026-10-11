# Conditional bridge: the 2,650-row residual catalog and ES(8) ≤ 313

**This bundle is CONDITIONAL. ES(8) ≤ 313 is NOT proved.** The completed planar
bound remains 314. What is checked here is that ES(8) ≤ 313 follows from one
purely arithmetic statement about a finite catalog, `Excludes2650Zero 32`.
That statement is a Lean definition; it is an explicit hypothesis of the final
theorems and is not proved, assumed as an axiom, or asserted anywhere.

**Completed fresh Lean check (2026-10-11):** one `check.py` invocation compiled
all 46 modules of the chain into an empty overlay in 2,463 seconds of wall time
(2,447 s of Lean compilation; this bundle's own four modules took 321 s) and
audited 115 theorem reports, all using only `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, `admit`, `native_decide` or custom axiom occurs. See
[kernel-check.json](kernel-check.json) (`"complete": true`, `"fresh_build": true`)
and [axioms.txt](axioms.txt).

## The arithmetic statement

`Residual32Bridge2650/Catalog.lean` is the literal catalog generated from
[`source-2650.json.gz`](../omission-residual32-rank-global-2026-10-10/source-2650.json.gz)
(154 states, 2,650 rows; decompressed SHA-256
`e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6`).
Row `r` is the zero-based entry `constraints[r]`. The namespace is
`OmissionResidual32Bridge2650`:

```lean
def support2650 (r : Fin 2650) : Finset (Fin 154)   -- constraints[r].support
def demand2650  (r : Fin 2650) : ℕ                  -- constraints[r].rhs

def Excludes2650Zero (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
    (∀ r, demand2650 r ≤ ∑ i ∈ support2650 r, holes i) ∧ (∑ i, holes i) ≤ budget
```

In words: there is no 0/1 hole vector with state 0 occupied that satisfies all
2,650 rows and has at most `budget` holes.

The catalog uses the repository's packed format, emitted by `catalog_source`
of `scripts/omission_lean_export.py` with base 2^17, the same base as the
frozen 2,469-row catalog: 128-row chunks of `(support, demand, code)`, with
every `code = rowCode base support` checked by `decide +kernel`
(`OmissionResidual32Bridge2650.code_correct`). `support2650`/`demand2650` are
the exporter's `support`/`demand` under public names.

### Plugging in an exported certificate

The context exporter (`scripts/omission_context_export.py`) emits, for its own
generated catalog `support`/`demand` in the same row order, a root theorem of
exactly this shape:

```lean
theorem node1 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ (∅ : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 0 ∅) : Finset (Fin 154)), holes i = 0)
```

The adapters are

```lean
theorem excludes2650Zero_of_node {budget : ℕ} {support' : Fin 2650 → Finset (Fin 154)}
    {demand' : Fin 2650 → ℕ} (hs : ∀ r, support' r = support2650 r)
    (hd : ∀ r, demand' r = demand2650 r) (h : <node shape for support'/demand'/budget>) :
    Excludes2650Zero budget

theorem forces_convex_octagon_313_of_node ... (hs) (hd) (h : <node shape, budget 32>) :
    ForcesConvexNGon 313 8
```

so `forces_convex_octagon_313_of_node hs hd Cert.node1` closes the argument
once `hs` and `hd` are proved. Ways to obtain them:

- `∀ r, support' r = support2650 r ∧ demand' r = demand2650 r` by
  `decide +kernel` over the two literal catalogs, the method of
  `BalancedCover61FusedBridge.lean`. Decide it per 128-row chunk and combine,
  exactly as `prefix_chunk0`–`prefix_chunk19` and `prefix_matches` do: one
  declaration over all 2,469 prefix rows peaked at 20.6 GB, while the chunked
  version made the whole `Matches` module take 107 s and 6.5 GB.
- If the exporter chose base 2^17 (the base here), `support2650_eq_of_codes`
  needs only `hcode'` (the exporter's `code_correct`) and `∀ r, code' r = code r`,
  a `decide +kernel` comparison of big integers without any `Finset`
  normalization. For another base `b`, `support2650_eq_of_rowCode` needs
  `∀ r, code' r = rowCode b (support2650 r)`. Both rest on
  `rowCode_injective : 1 < b → rowCode b s = rowCode b t → s = t`.
- Demands: `∀ r, demand' r = demand2650 r` by `decide +kernel`.

## Final theorems

```lean
theorem OmissionResidual32Bridge2650.all_rows_2650 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 2650, demand2650 r ≤
      ∑ i ∈ support2650 r, holesOf (c.residualOccupied noCap noOctagon noJunction) i

theorem OmissionResidual32Bridge2650.residual_bound_121_of_excludes
    (h : Excludes2650Zero 32) : Partition.ResidualBound 121

theorem OmissionResidual32Bridge2650.forces_convex_octagon_313_of_excludes
    (h : Excludes2650Zero 32) : ForcesConvexNGon 313 8

theorem OmissionResidual32Bridge2650.convex_octagon_of_card_ge_313_of_excludes
    (h : Excludes2650Zero 32) (S : Finset (Fin 2 → ℝ)) (gp : GeneralPosition S)
    (size : 313 ≤ S.card) :
    ∃ T : Finset (Fin 2 → ℝ), T ⊆ S ∧ T.card = 8 ∧
      ConvexIndependent ℝ (fun p : (T : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ))
```

`holesOf` is `OmissionResidual32Transfer.holesOf` (0 on occupied states, 1 on
holes). `Partition.ResidualBound 121` says every actual residual configuration
has at most 121 points. `residual_bound_of_excludes2650` is the general form:
`Excludes2650Zero b` gives `Partition.ResidualBound (153 - b)`.

## How the pieces fit

| Rows (zero based) | Count | Literal match (`Matches.lean`, `decide +kernel`) | Geometric validity used in `all_rows_2650` |
| --- | ---: | --- | --- |
| 0–2468 | 2,469 | `prefix_matches`: `OmissionResidual32Contexts.support`/`demand` | `OmissionResidual32Transfer.all_rows` |
| 2469–2597 | 129 | `added_matches`: `Residual32AddedRows.support`, demand 1 | `Residual32AddedRows.all_rows` |
| 2598–2645 | 48 | `relaxed_matches`: `CoupledSixthRelaxedVariants.support`, demand 1 | `CoupledSixthRelaxedVariants.all_rows` |
| 2646–2649 | 4 | `rank_{one,two,three,four}_matches`: `CoupledCoreRankSearch*.support.toFinset`, demand 1 | `CoupledCoreRankSearch*.hole_bound` |

`suffix_demand` separately checks that every row from 2469 on has demand 1.
The demand-one families are stated as `1 ≤ (S \ occupied).card`; they are
converted with `OmissionResidual32Transfer.holesOf_sum`.

`residual_bound_of_excludes2650` follows the template of
`OmissionResidual32Transfer.residual_bound_of_hole_budget`: for `n` points the
actual hole vector satisfies `∑ holes + n = 154`, so more than `153 - b` points
would give a Boolean model with at most `b` holes. State 0 is occupied by
`OmissionResidualZeroState.zero_mem_residualOccupied`, which needs `0 < n`;
`n = 0` is below every bound and is excluded automatically by the contradiction
hypothesis. With `b = 32` this is the bound 121.

`Final.lean` adds the balanced side exactly as the completed 314-point assembly
does: `balanced_population_190` is
`OmissionBalanced.balanced_bound_of_hole_budget (budget := 61)` applied to
`OmissionBalancedCover61Fused.exclusion_transfer OmissionBalancedCover61Fused.excludes_budget`,
and `Partition.forces_of_population_bounds` gives 190 + 121 + 2 = 313. It
imports `BalancedCover61FusedProof.Root` and `BalancedCover61FusedBridge`
directly, not the 314 assembly module, so the residual 31-hole certificate is
not loaded and no declaration names collide.

## Checking

From the repository root, with the maintained library built:

```sh
python3 experiments/omission-residual32-bridge2650-2026-10-11/generate.py
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
  experiments/omission-residual32-bridge2650-2026-10-11/check.py
```

`generate.py` verifies the source identity, cross-checks the four row blocks
against the Lean literal families in Python (untrusted, for early failure
only), writes `Catalog.lean`, and pins the source, generator, exporter and
every Lean file of the bundle in `manifest.json`.

`check.py --preflight-only` validates those identities, regenerates the catalog
in memory and compares it byte for byte, scans every compiled source for
`sorry`, `admit`, `native_decide` and `axiom`, and computes the import closure.
The full check then:

1. requires Lean 4.24.0 and `lake build --no-build ErdosSzekeres` up to date;
2. creates a fresh overlay directory under ignored `.cache/` and links into it
   only the older prerequisite objects whose `.olean` **and** `.lean` SHA-256 both
   match the committed complete 314-point gate record
   [`global-cover-314-check.json`](../omission-global-assembly-2026-10-10/global-cover-314-check.json):
   the original residual catalog, the residual cycle and block geometry, the
   residual and balanced cut transfers, the balanced catalog and rows-only
   geometry, and the 61-hole balanced cover certificate (656 objects);
3. compiles every other module of the chain from tracked sources, one Lean
   process at a time with `-j1`, `LEAN_NUM_THREADS=1` and `-M 8000`
   (46 modules: the frozen 2,469-row catalog, its transfer, the Witness,
   coupled Sixth and Fourth-family modules, the added rows, the relaxed Sixth
   modules, the rank-attainment and rank-core modules, the zero-state lemma,
   `BalancedBudgets`, `BalancedCover61FusedBridge`, and the four modules here);
4. rejects any error or warning, parses every `#print axioms` report, requires
   the audits listed in `check.py`, and accepts only `propext`,
   `Classical.choice` and `Quot.sound`;
5. checks the printed final signatures and writes
   [kernel-check.json](kernel-check.json) and [axioms.txt](axioms.txt).

The overlay contains only the linked pinned objects and fresh outputs, so no
other cached copy of a module can shadow an import. Reused objects never import
freshly compiled ones (checked). `--resume` exists for development only and
marks the record `"fresh_build": false`.

## What was checked

In the recorded run (`kernel-check.json`, Lean 4.24.0, arm64 macOS):

| Module | Seconds | Max RSS | Main results |
| --- | ---: | ---: | --- |
| `Residual32Bridge2650.Catalog` | 143.8 | 5.2 GB | 2,650 literal rows, `code_correct` |
| `Residual32Bridge2650.Matches` | 106.8 | 6.5 GB | the literal matches above, `rowCode_injective`, `support2650_eq_of_codes` |
| `Residual32Bridge2650.Rows` | 9.5 | 2.9 GB | `all_rows_2650`, `residual_bound_121_of_excludes`, `excludes2650Zero_of_node` |
| `Residual32Bridge2650.Final` | 60.3 | 6.4 GB | `balanced_population_190`, `forces_convex_octagon_313_of_excludes`, `convex_octagon_of_card_ge_313_of_excludes`, `forces_convex_octagon_313_of_node` |

Final axiom reports (each `[propext, Classical.choice, Quot.sound]`):
`balanced_population_190`, `all_rows_2650`, `residual_bound_121_of_excludes`,
`forces_convex_octagon_313_of_excludes`,
`convex_octagon_of_card_ge_313_of_excludes`,
`forces_convex_octagon_313_of_node`. The pinned fully qualified statements are

```text
OmissionResidual32Bridge2650.Excludes2650Zero : ℕ → Prop
OmissionResidual32Bridge2650.residual_bound_121_of_excludes :
  OmissionResidual32Bridge2650.Excludes2650Zero 32 → ErdosSzekeres.Omission.Partition.ResidualBound 121
OmissionResidual32Bridge2650.forces_convex_octagon_313_of_excludes :
  OmissionResidual32Bridge2650.Excludes2650Zero 32 → ErdosSzekeres.ForcesConvexNGon 313 8
```

The record also lists the SHA-256 of every reused object and source, every
freshly compiled source and object, and all 209 maintained-library objects.
`prefix_matches` is decided in twenty 128-row chunks: as one declaration over
all 2,469 rows it peaked at 20.6 GB, chunked at 6.5 GB.

## Scope and caveats

- Nothing here proves `Excludes2650Zero 32`. A separate exact search is trying
  to produce that arithmetic certificate. Solver timeouts and partial runs in
  [omission-residual32-rank-global-2026-10-10](../omission-residual32-rank-global-2026-10-10/README.md)
  establish neither feasibility nor infeasibility.
- The catalog rows are necessary conditions. A 32-hole Boolean model, if one
  exists, need not correspond to a real point configuration; it would only show
  that this catalog is insufficient.
- The balanced 61-hole certificate and the other reused objects were not
  recompiled here. They are bound by hash to the complete 314-point gate record,
  which compiled them against the same maintained library objects.
- Memory: `-M 8000` bounds Lean's elaborator heap but not kernel checking. This
  bundle's modules stay below 6.5 GB RSS, and the final module maps the 15 GB
  balanced certificate objects with a 6.4 GB peak. Several existing
  prerequisites, compiled unchanged, peak higher: RankCoreFour 19.7 GB,
  BalancedCover61FusedBridge 18.6 GB, SixthRelaxedTemplate 17.6 GB,
  RankCoreTwo 17.6 GB, RankCoreThree 14.6 GB, RankCoreOne 12.0 GB, Witness
  11.4 GB, OldcutsBinding 10.8 GB, LeanCore 10.1 GB.

The inherited catalog and geometric framework derive in part from Michael
Schroeder's companion archive,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
Attribution and licensing are in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
