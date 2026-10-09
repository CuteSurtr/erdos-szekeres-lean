# Linking the two finite certificate families

The global target remains **unproved**. This page describes the production
module layout and the remaining checks, not a completed `ES(8) ≤ 317` theorem.
The historical balanced bound 192 and all residual geometric rows have
completed check records in their separate artifact directories.

## Module layout

Historical balanced and residual arithmetic exports both used `Catalog`,
`PartNNNNN`, and `Root`. Lean cannot load two different modules with the same
name into one proof. The balanced family is smaller, so it is being rebuilt as
`BalancedProof.Catalog`, `BalancedProof.PartNNNNN`, and `BalancedProof.Root`.
Residual arithmetic keeps its existing names and accumulated partial checks.
Declaration namespaces remain `OmissionBalanced` and `OmissionResidual`.

The balanced geometry exporter accepts `--arithmetic-prefix BalancedProof`.
It emits a `BalancedOccupancy.lean` bridge with the new root import, makes each
cycle block import `BalancedProof.Catalog`, and makes `BalancedGeometry` import
the prefixed root and occupancy bridge. The checker rejects a disagreement
between the geometry and arithmetic manifests' prefixes.

Regeneration on 9 October reproduced all **900 arithmetic sources** and all
**86 geometry/occupancy sources** exactly after reversing these import-name
changes. This comparison does not replace fresh compilation. The old compiled
objects are not renamed or reused as proofs of the new modules.

## Reproduce the linked balanced family

Use the pinned toolchain and an extracted copy of Schroeder's version-1
archive, as attributed in [THIRD_PARTY.md](THIRD_PARTY.md). From the repository
root, choose fresh output directories:

```sh
python3 scripts/omission_lean_export.py \
  /path/to/es7_es8_bounds_81_319_v1/certificates/balanced.json \
  experiments/omission-balanced-59-2026-10-05.json.gz \
  --output .cache/omission-balanced-linked \
  --namespace OmissionBalanced --leaf-limit 16 --module-prefix BalancedProof

python3 scripts/omission_geometry_export.py \
  /path/to/es7_es8_bounds_81_319_v1 \
  --output .cache/omission-balanced-geometry-linked \
  --arithmetic-prefix BalancedProof

lake env python3 scripts/check_omission_lean.py \
  .cache/omission-balanced-linked --resume --workers 2 --memory 3000

lake env python3 scripts/check_omission_geometry.py \
  .cache/omission-balanced-geometry-linked \
  --arithmetic .cache/omission-balanced-linked --resume
```

The arithmetic command without `--module` attempts the **whole** family, not
a short sample. `--module Part00000` selects a single part and its catalog;
part-only checks report `complete: false`. Selecting `Root` requests the whole
family, including every part. On this Mac, substitute
`ELAN_HOME="$PWD/.elan" .elan/bin/lake` for `lake`.

`--workers` controls independent Lean processes, not additional agents. The
catalog finishes before any part starts; the root starts only after every part
has succeeded. Each process has its own `--memory` limit, so total memory can
increase with the worker count. One coordinator writes progress atomically.
Do not run multiple checker invocations against the same output directory at
once. Failed checks cancel queued work and prevent root checking; already
running checks are allowed to finish. Resume requires matching inputs and
compiled-output hashes, not just the presence of an object file.

## Final composition still required

After the residual arithmetic root and renamed balanced family both pass,
recheck the existing `BalancedPartition.lean` and `ResidualReduction.lean`
bridges with the new import search paths. The final module must load:

| Module | Role |
| --- | --- |
| `BalancedGeometry`, through `BalancedProof.Root` | Unconditional balanced population bound 192 |
| `ResidualAllGeometry`, through the residual `Catalog` | All 1,187 geometric row implications |
| Residual `Root` | Exclusion of Boolean hole vectors with total at most 30 |
| `ResidualReduction` | Actual residual bound 123 and geometric/projective composition |

The intended final application is
`OmissionResidual.forces_317_of_arithmetic` with
`OmissionBalanced.balanced_bound_192` and
`OmissionResidual.excludes_budget`. This application has **not** been checked
as a closed theorem. Its last argument is not available until the full residual
root succeeds. Final validation must inspect the resulting statement, audit
its axioms, and bind the generated sources and prerequisites to their check
records before any numerical result is reported as proved.

Integration controls compile complete small prefixed and unprefixed trees
together, including the real occupancy bridge with its 252-state / 59-hole
types. They also check partial parallel runs, resume into a complete root,
missing occupancy sources, mismatched prefixes, and a deliberately corrupted
arithmetic part. These controls test the integration machinery; they do not
stand in for the large certificates.
