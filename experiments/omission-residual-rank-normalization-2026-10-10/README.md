# Cup-coordinate normalization in the abstract coupled model

Status: two Lean modules prove that adding the source-cup upper bound does not
change satisfiability of the complete abstract coupled labeling model defined
here. This is a limitation on that search model, not a new numerical
Erdős–Szekeres bound. The attained-rank theorem in the preceding
[rank-attainment bundle](../omission-residual-rank-attainment-2026-10-10/README.md)
remains valid and informative about actual ranks.

Fix catalog states, an injective chronological order, symmetric cap labels,
orientation signs and convexity data. Write `H_i` for the source state's first
column. For each unordered pair, let `i` be its earlier endpoint and replace
only its cup coordinate by

```math
b'(i,j)=\min\{b(i,j),H_i+1\}.
```

The old domain is exactly the target state's Ferrers cells minus the source's
cells and the forbidden cell `(1,6)`, with cap coordinates in `1..4` and cup
coordinates in `1..6`. Clipping preserves this domain: it decreases the cup
coordinate within the target, while remaining above the source's column at
the unchanged cap coordinate. A clipped value of six must already have been
six, so clipping cannot introduce the forbidden cell.

For consecutive edges in chronological order `i < j < l`, old positive growth
is `b(i,j) < b(j,l)`. Target membership gives `b(i,j) ≤ H_j`, so

```math
\min\{b(i,j),H_i+1\}<\min\{b(j,l),H_j+1\}.
```

Negative growth uses cap coordinates, which are unchanged. All other model
conditions can be arbitrary predicates on the unchanged `Frame`: chronological
position range, orientations, fixed signs, orientation packets, convexity
equations and convex-octagon exclusion. Thus the existence equivalence retains
these conditions verbatim. The model's symmetric labels and bounds are also
part of `Valid`; no assumed geometric realizability is used.

The equivalence does **not** include existential equations asserting that every
state column or label is an attained rank, nor any additional constraint that
depends on cup labels beyond the stated domains, bounds and growth clauses.
Clipped labels need not be the longest ranks of a real point configuration.
Neither abstract satisfiability nor this theorem supplies a real-point
realization. Stronger attainment constraints require separate analysis.

## Lean declarations

All names below have prefix `ErdosSzekeres.Omission.RankNormalization.`.

| Declaration | File | Content |
| --- | --- | --- |
| `clip_ordered`, `clip_symm` | [Normalization.lean](Normalization.lean) | Earlier-endpoint formula and symmetry |
| `allowed_clip` | [Normalization.lean](Normalization.lean) | State difference and forbidden-cell safety |
| `clipped_growth` | [Normalization.lean](Normalization.lean) | Exact arithmetic growth preservation |
| `clip_valid`, `clip_sourceBound` | [Normalization.lean](Normalization.lean) | Full label constraints and added bound |
| `exists_iff_sourceBound` | [Normalization.lean](Normalization.lean) | Existence equivalence for a fixed frame |
| `exists_frame_iff_sourceBound` | [Normalization.lean](Normalization.lean) | Equivalence with arbitrary frame-only constraints |
| `catalog_heightDominates` | [CatalogNormalization.lean](CatalogNormalization.lean) | Kernel-checked first-column maximum for all 154 catalog states |
| `catalog_allowed_iff` | [CatalogNormalization.lean](CatalogNormalization.lean) | Definitionally exact agreement with `Coupled.Allowed` |
| `catalog_exists_iff_sourceBound` | [CatalogNormalization.lean](CatalogNormalization.lean) | Exact-catalog fixed-frame equivalence |
| `catalog_exists_frame_iff_sourceBound` | [CatalogNormalization.lean](CatalogNormalization.lean) | Exact-catalog equivalence retaining arbitrary frame constraints |

## Replay and audit

With the maintained library already built and the pinned Lean toolchain:

```sh
lake env python3 experiments/omission-residual-rank-normalization-2026-10-10/check.py
```

For source checks and the independent finite example without Lean or a solver:

```sh
python3 experiments/omission-residual-rank-normalization-2026-10-10/check.py --preflight-only
python3 experiments/omission-residual-rank-normalization-2026-10-10/test_check.py
```

[manifest.json](manifest.json) pins bundle sources, the full maintained local
import closure, toolchain/package locks, the example's source catalog, and the
axiom checker. The serial checker places compiler outputs only in `.cache/`,
audits all twelve exported theorems, and writes [kernel-check.json](kernel-check.json)
and the complete [axioms.txt](axioms.txt). The proof sources contain no unchecked
placeholders and use only standard Lean axioms. The CI entry point `check()`
checks source identities and replays the finite example without compiling.

[clipping-example.json](clipping-example.json) is an 11-state old-model
assignment with 15 source-cup violations, and its clipped assignment. Its
positions, cap coordinates and orientations are identical. [replay.py](replay.py)
uses Python's standard library to recompute every directed domain, signed
growth, orientation packet and forced sign. It checks all 165 eight-element
subsets in each assignment for the absence of an abstract convex octagon,
and verifies every changed coordinate equals the clipping formula. This
finite illustration is separate from the general Lean proof. Neither
assignment is claimed to be a geometric realization or a global hole witness.

The imported catalog and residual infrastructure retain their attribution in
source headers and [THIRD_PARTY.md](../../docs/THIRD_PARTY.md). The example's
catalog originates from Schroeder's cited archive; no third-party solver
binary or solver proof is included.
