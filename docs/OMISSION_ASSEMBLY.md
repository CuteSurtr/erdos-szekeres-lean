# Closed real-point octagon assembly

**`ES(8) ≤ 317` is proved in Lean.** The theorem
`ErdosSzekeres.Omission.forces_convex_octagon_317 : ForcesConvexNGon 317 8`
is in
[`FinalCover317.lean`](../experiments/omission-global-assembly-2026-10-10/FinalCover317.lean).
Its explicit companion, `convex_octagon_of_card_ge_317`, states that every
finite set of at least 317 points in `ℝ²` in general position contains an
eight-element subset in convex position. No certificate, population bound,
or additional coordinate restriction remains as a hypothesis.

The [complete assembly record](../experiments/omission-global-assembly-2026-10-10/global-cover-317-check.json)
reports `complete: true`; the
[axiom output](../experiments/omission-global-assembly-2026-10-10/global-cover-317-axioms.txt)
contains only `propext`, `Classical.choice`, and `Quot.sound` for all four final
roots. The finished source chain contains no `sorry`, custom axioms, or native
evaluation proofs. This is an ordinary convex octagon result, not an
empty-octagon result or an asymptotic strengthening of Suk or HMPT. No priority
claim for the numerical bound is made here.

## Completed proof chain

| Layer | Checked modules / declarations | Exact role |
| --- | --- | --- |
| Original balanced rows | `BalancedRows`; `OmissionBalanced.all_geometric_rows` | All 2,685 row inequalities follow for actual balanced configurations. The 84 row blocks and aggregator are checked. |
| Original residual rows | `ResidualGeometry`, `ResidualAllGeometry`; `OmissionResidual.all_geometric_rows` | All 1,187 rows follow for actual residual configurations: 1,164 cycle rows and 23 block rows. |
| Arithmetic consequences | `BalancedCoverCuts.all_rows`, `ResidualCoverCuts.all_rows` | Derive 220 balanced and 402 residual rows from the original rows and Boolean hole bounds. These introduce no new geometric assumptions. |
| Compressed arithmetic | `OmissionBalancedCover.excludes_budget` in `BalancedCoverProof.Root`; `OmissionResidualCover.excludes_budget` in `ResidualCoverProof.Root` | Exclude balanced hole total at most 59 and residual hole total at most 30. All 17 balanced and 149 residual proof parts, both catalogs, and both roots are checked. |
| Catalog identification | `BalancedCoverBridge`, `ResidualCoverBridge`; `base_catalog_matches`, `cut_catalog_matches`, `exclusion_transfer` | Kernel-check equality of every original and added support/demand pair, then transfer each exclusion to the original geometric row system. |
| Actual populations | `BalancedBudgets`, `ResidualBudgets`; `balanced_bound_of_hole_budget`, `residual_bound_of_hole_budget` | The hole identities are `sum holes + n = 252` and `sum holes + n = 154`, yielding populations 192 and 123. |
| Global geometry | `Partition`, `PopulationBounds`; `forces_of_population_bounds` | The minimum-slope partition and projective transfer combine populations `B`, `R` into forcing threshold `B + R + 2`. |
| Closed statement | `FinalCover317` | Proves `balanced_population_192`, `residual_population_123`, `forces_convex_octagon_317`, and `convex_octagon_of_card_ge_317`. |

The extra two points in the last threshold account for the root removed by
the projective chart and the strict inequality needed to force an octagon:
`192 + 123 + 2 = 317`. The [semantic review](../experiments/omission-global-assembly-2026-10-10/SEMANTIC_REVIEW.md)
explains the real-point boundary and cardinality bookkeeping.

## Reproduce the checked route

Use the pinned Lean/Mathlib toolchain, build the maintained library, and obtain
the version-1 archive attributed in [THIRD_PARTY.md](THIRD_PARTY.md). Build
outputs belong in fresh ignored directories. On the original Mac, substitute
`ELAN_HOME="$PWD/.elan" .elan/bin/lake` for `lake` below.

1. Reproduce the residual catalog and all residual geometry using the
   [residual artifact's commands](../experiments/omission-residual-geometry-2026-10-09/README.md#reproduce-the-geometry-without-building-the-full-arithmetic-tree).
   They create `.cache/residual-replay/arithmetic`, `cycles`, and `blocks`.
   Its original large arithmetic root is not needed.
2. Prepare and check the original balanced catalog. This generates the old
   tree's sources for its manifest, but checks only `Catalog`:

```sh
archive_dir=/path/to/es7_es8_bounds_81_319_v1
python3 scripts/omission_lean_export.py "$archive_dir/certificates/balanced.json" \
  experiments/omission-balanced-59-2026-10-05.json.gz \
  --output .cache/317/balanced-catalog --namespace OmissionBalanced \
  --module-prefix BalancedProof --leaf-limit 16
lake env python3 scripts/check_omission_lean.py \
  .cache/317/balanced-catalog --module Catalog --memory 3000
```

3. Extract the exact checked balanced row sources and compile all 85 modules:

```sh
mkdir -p .cache/317/balanced-rows
tar -xzf experiments/omission-global-assembly-2026-10-10/balanced-rows-sources.tar.gz \
  -C .cache/317/balanced-rows
cp experiments/omission-global-assembly-2026-10-10/balanced-rows-export.json \
  .cache/317/balanced-rows/export.json
lake env python3 scripts/omission_balanced_rows.py check \
  .cache/317/balanced-rows --arithmetic .cache/317/balanced-catalog \
  --resume --memory 3000
```

4. Follow the [compressed-certificate reproduction](../experiments/omission-cover-certificates-2026-10-10/README.md#reproduction)
   to generate and check both new complete arithmetic trees. Its directories
   are `.cache/reproduce-cover-residual-tree` and
   `.cache/reproduce-cover-balanced-tree`; its cut-source directories are
   `.cache/reproduce-cover-residual` and `.cache/reproduce-cover-balanced`.
   Then check the two cut transfers against the original catalogs:

```sh
lake env python3 scripts/check_omission_cover_lean.py \
  .cache/reproduce-cover-residual \
  --arithmetic .cache/residual-replay/arithmetic --memory 3000
lake env python3 scripts/check_omission_cover_lean.py \
  .cache/reproduce-cover-balanced \
  --arithmetic .cache/317/balanced-catalog --memory 3000
```

5. Run the closed global gate in a separate output directory:

```sh
lake env python3 scripts/check_omission_global.py \
  --output .cache/317/global \
  --residual-arithmetic .cache/residual-replay/arithmetic \
  --residual-cycles .cache/residual-replay/cycles \
  --residual-blocks .cache/residual-replay/blocks \
  --balanced-arithmetic .cache/317/balanced-catalog \
  --balanced-geometry .cache/317/balanced-rows \
  --residual-cover-arithmetic .cache/reproduce-cover-residual-tree \
  --residual-cover-cuts .cache/reproduce-cover-residual \
  --balanced-cover-arithmetic .cache/reproduce-cover-balanced-tree \
  --balanced-cover-cuts .cache/reproduce-cover-balanced \
  --memory 3000
```

A successful run ends with `complete: true` in `global-check.json`. The gate
refuses partial families, changed source or object hashes, inconsistent
catalog dependencies, unlisted compiled modules that could shadow imports,
wrong arithmetic targets, and nonstandard axiom reports. It checks the final
statement in an isolated overlay and confirms its inputs remained unchanged.
Saved records document actual runs on the original host; a reproduction on a
new path produces new records rather than treating old records as fresh checks.
The archived proof bundles contain sources, not compiled objects.

`--workers` on the arithmetic checker counts Lean processes, not agents. Each
process has its own memory allowance. Use one coordinator per output directory;
resume validates source, dependency, and output hashes. A selected part or
catalog reports `complete: false`, as intended. Only both complete compressed
roots can satisfy the final global gate.

## Stronger candidates and historical routes

The balanced60 certificate would give population 191 and threshold 316. Its
sources are prepared in the [assembly artifact](../experiments/omission-global-assembly-2026-10-10/README.md),
but it needs its own completed arithmetic root and final gate. Further V2
profiles use different cut catalogs and exact manifest identities. None is
promoted to a theorem merely because a search or integer replay succeeds.
See [remaining work](ES8_REMAINING.md) for current status.

The earlier direct route renamed the balanced arithmetic modules to
`BalancedProof.*` to avoid collisions with residual `Catalog`, `PartNNNNN`,
and `Root`. Its 898-part rebuild and the large direct residual tree were left
partial when the shorter cover route succeeded. The
[9 October partial record](../experiments/omission-linked-balanced-2026-10-09.json)
and [production import control](../experiments/omission-linked-control-2026-10-09.json)
remain historical evidence, not prerequisites or substitutes for either new
root. `Final317.lean` and the weaker `Final318.lean` preserve those alternative
assemblies; the checked theorem uses `FinalCover317.lean`.

The original state catalogs, row data, and geometric strategy are attributed
to Michael Schroeder's version-1 archive, DOI
[10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
The new search trees and arithmetic consequences are recorded separately from
that source material; code and data notices are preserved in
[THIRD_PARTY.md](THIRD_PARTY.md).
