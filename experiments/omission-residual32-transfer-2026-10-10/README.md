# Geometric binding for the 2,469-row residual research catalog

**Completed standalone Lean check:** six modules, 17 audited theorem roots,
only `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, `admit`,
custom axioms or `native_decide` occur in the six modules.
See `kernel-check.json`, `axioms.txt` and `validation.json`.

This bundle connects the exact frozen search input in
`../omission-residual32-research-2026-10-10/source.json.gz` to actual residual
configurations of real points in general position. Its uncompressed SHA-256 is
`f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909`.
The arithmetic catalog is shared with the neighboring
`omission-residual32-context-certificates-2026-10-10` bundle; its namespace is
`OmissionResidual32Contexts`.

The main statements in `Transfer.lean`, namespace `OmissionResidual32Transfer`, are:

- `all_rows`: every literal research inequality holds for the same hole vector
  `holesOf (c.residualOccupied noCap noOctagon noJunction)`.
- `feasible_holes`: that Boolean vector satisfies all 2,469 inequalities and
  the exact population equation `sum holes + n = 154`.
- `residual_bound_of_hole_budget`: an explicitly supplied arithmetic exclusion
  for budget `b` implies the residual population bound `153 - b`.

The assumptions are the existing `Configuration n` (strict x-order and real
planar general position), no 6-cap, no convex octagon, and no incoming-six-cup /
outgoing-five-cap junction. There is no separate unproved row-validity premise.
The polygon is an ordinary convex polygon and need not be empty.

`ContextGeometry.lean` composes the five independently checked arithmetic
context exclusions with `all_rows`. Its `geometric_node492360`,
`geometric_node492359`, `geometric_node485523`, `geometric_node485522`, and
`geometric_node30` rule out those literal missing/occupied patterns for any
actual residual configuration with at least 122 points. Their hypotheses
refer directly to membership in the same `c.residualOccupied` set.
The two `geometric_parent492360` and `geometric_parent485523` results combine
complementary children, removing the assumptions about states 87 and 109,
respectively. Thus the five children also yield three excluded parent regions
(two merged pairs and node 30). These do not exhaust every possible pattern.

This bundle does **not** prove `ExcludesHoleBudget 32`, does not close the
partial search tree, and does not improve the completed global bound 314.
`kernel-check.json` records the actual verification status; a generated source
file or `mapping.json` alone is not a successful Lean check.

| Source rows (zero based) | Count | Existing geometric or arithmetic proof | Literal binding |
|---|---:|---|---|
| 0–1186 | 1187 | `OmissionResidual.all_geometric_rows` | `OriginalBinding.lean`, `original_matches` |
| 1187–2294 | 1108 | `ResidualCoverCutsV2.all_rows` | `OldcutsBinding.lean`, `oldcuts_matches` |
| 2295–2315 | 21 | `AdditionalResidualRows.all_rows` | `GeometricBinding.lean`, `geometric_matches` |
| 2316–2339 | 24 | `GeneralResidualBlocks.all_rows` | same |
| 2340–2456 | 117 | Five coupled variant families and five single-row theorems | same; exact per-row theorem/index in `mapping.json` |
| 2457–2468 | 12 | `NewCuts.lean`, `cut0`–`cut11`, `new_cut_rows` | Direct use of the shared literal catalog |

Every support and demand equality is checked in Lean with `decide +kernel`.
The five singleton rows use `CoupledCoreThird.hole_bound`,
`CoupledDemandTwo.hole_bound`, `CoupledCoreFifth.hole_bound`,
`CoupledCoreEleven.hole_bound`, and `CoupledCoreNine.hole_bound`.
The first coupled core is also a member of the first proved variant family.
Second-family indices are selected by literal equality, not by assuming that
research metadata or row order matches the public theorem order.
The twelve final cuts are ordinary applications of `rounded_cover_cut`;
row 2462 explicitly depends on the previously proved row 2457.

## Reproduction

Build the pinned maintained library first. The standalone checker requires
these separately compiled, existing proof packages:

1. The original residual catalog, all cycle rows and all block rows. Follow
   the [residual geometric reproduction instructions](../omission-residual-geometry-2026-10-09/README.md#reproduce-the-geometry-without-building-the-full-arithmetic-tree).
2. `ResidualCoverCutsV2.lean`, retained in
   `../omission-cover-certificates-2026-10-10/`, compiled against that original
   `Catalog.olean`. The source is already complete and can be compiled in a
   fresh directory; no arithmetic exclusion tree is needed.
3. The shared `Residual32ContextsProof.Catalog` from the neighboring context
   bundle, using its `check.py` instructions.

`generate.py` regenerates the four proposed binding/cut modules and their
mapping from the frozen data and current public Lean definitions. The mapping
manifest deliberately records generation only (`lean_checked: false`); the
separate `kernel-check.json` contains the completed verification result. `Transfer.lean`
and `ContextGeometry.lean` are the handwritten compositions. The check rejects changed frozen data, changed
binding sources, and prerequisite source files that differ from the retained
source manifests. It records the toolchain, all imported experimental objects,
maintained proof objects, generated output objects, source identities and
expected theorem axiom reports. Build artifacts remain in ignored `.cache/`.

With existing local prerequisite paths, from the repository root:

```sh
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
  experiments/omission-residual32-transfer-2026-10-10/check.py
```

For fresh reproduction directories, specify them explicitly:

```sh
lake env python3 experiments/omission-residual32-transfer-2026-10-10/check.py \
  --arithmetic .cache/residual-replay/arithmetic \
  --cycles .cache/residual-replay/cycles \
  --blocks .cache/residual-replay/blocks \
  --old-cuts .cache/residual-replay/cuts-v2 \
  --contexts .cache/residual32-context-certificates-2026-10-10 \
  --output .cache/residual32-transfer-fresh
```

The check is deliberately sequential and caps each Lean process at 14,000 MB.
The six fresh module checks took about 184 seconds in the recorded run.
Afterward all 747 recorded prerequisite objects/configuration files and 72
external Lean sources were rehashed and unchanged. A mutated-catalog negative
control was rejected before compilation (`provenance-negative.json`).
These standalone checks are separate from the maintained-library CI workflow.

## Attribution

The original 154-state catalog and 1,187 source inequalities derive from
Michael Schroeder, *Erdős–Szekeres: Upper Bounds for Convex Heptagons and
Octagons*, version 1, 19 September 2026,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
Original data is CC BY 4.0; adapted proof code is MIT, with the embedded Baek
proof under Apache-2.0. See [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
The later geometric families and arithmetic consequences retain their existing
provenance. This bundle adds literal matching and composition, not a claim of
independent discovery of those source results.
