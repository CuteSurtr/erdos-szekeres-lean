# Complete residual geometric row proof

**All 1,187 residual row implications are checked for actual real points.**
There are 1,164 cycle rows and 23 block rows. The assumptions are strict
x-order and general position (the `Configuration` structure), no 6-cap, no
convex octagon, and no incoming-six-cup/outgoing-five-cap junction.

The main theorem is `OmissionResidual.all_geometric_rows` in
`ResidualAllGeometry.lean`, included in `blocks-sources.tar.gz`. It states
that each literal row has its required number of missing states. It has no
unproved geometric or row-validity premise. `ResidualGeometry.lean`, in the
cycle archive, proves the 1,164 cycle rows; row 973 and rows 1165–1186 are
handled by the 23 block modules. Their coverage and support/demand equality
are checked inside Lean.

[ResidualReduction.lean](ResidualReduction.lean) then proves:

- `feasible_holes`: every such actual configuration supplies a Boolean hole
  vector satisfying all 1,187 rows, with `sum holes + n = 154`.
- `residual_bound_of_arithmetic`: the explicit proposition
  `ExcludesThirtyHoles` implies `Partition.ResidualBound 123`.
- `forces_317_of_arithmetic`: the separately completed `BalancedBound 192`
  and `ExcludesThirtyHoles` imply `ForcesConvexNGon 317 8`.

**`ExcludesThirtyHoles` has not yet been proved in Lean. This artifact does
not prove the residual population bound 123 or ES(8) ≤ 317.** The residual
arithmetic tree is checked only in part. The [remaining-work estimate](../../docs/ES8_REMAINING.md)
also records the module-name isolation needed for final certificate linking.

## Checks and contents

The default maintained library proves all geometric prerequisites, including
the 154-state catalog, actual owner injection, restricted-domain signs,
compression to two cap-rank values, Baek's combinatorial bound, and its
supporting-line transfer to real convex polygons. Its fresh audit contains
444 roots. This artifact separately records **39 cycle-module checks**,
**24 block/composition checks**, and the three reduction theorems. Only
`propext`, `Classical.choice`, and `Quot.sound` occur. No placeholders or native
evaluation proofs are used. See [the proof map](../../docs/OMISSION_RESIDUAL.md).

- `cycles-sources.tar.gz`, `blocks-sources.tar.gz`: generated Lean sources only.
- `cycles-export.json`, `blocks-export.json`: source hashes and exact scope.
- `cycles-kernel-check.json`, `blocks-kernel-check.json`: successful invocations,
  complete expected axiom reports, prerequisite bindings and output hashes.
- `Catalog.lean.gz`, `arithmetic-export.json`, `catalog-validation.json`: the
  separately checked arithmetic catalog prerequisite. The full arithmetic
  manifest is retained for provenance; this bundle does not include or claim
  to have checked its full tree.
- `row-source.json.gz`: exact upstream residual JSON, including its original
  weaker tree; only the literal state order and rows are used by the geometry.
- `block-data.json`: the 23 source compression records as strict JSON.
- `axioms.txt`, `validation.json`: reduction audit and checkpoint bindings.

Compiled objects and cache directories are not committed. The default CI
checks the maintained library, audits, and small positive/negative controls;
it does not silently count these 63 generated module builds as CI checks.

## Reproduce the geometry without building the full arithmetic tree

After building the pinned library, extract only the checked catalog and row
proofs. From the repository root:

```sh
mkdir -p .cache/residual-replay/arithmetic .cache/residual-replay/cycles .cache/residual-replay/blocks
gzip -dc experiments/omission-residual-geometry-2026-10-09/Catalog.lean.gz > .cache/residual-replay/arithmetic/Catalog.lean
cp experiments/omission-residual-geometry-2026-10-09/arithmetic-export.json .cache/residual-replay/arithmetic/export.json
tar -xzf experiments/omission-residual-geometry-2026-10-09/cycles-sources.tar.gz -C .cache/residual-replay/cycles
tar -xzf experiments/omission-residual-geometry-2026-10-09/blocks-sources.tar.gz -C .cache/residual-replay/blocks
cp experiments/omission-residual-geometry-2026-10-09/cycles-export.json .cache/residual-replay/cycles/export.json
cp experiments/omission-residual-geometry-2026-10-09/blocks-export.json .cache/residual-replay/blocks/export.json
lake env sh -c 'LEAN_PATH="$PWD/.cache/residual-replay/arithmetic:$LEAN_PATH" lean -j 1 -s 32768 -M 6000 .cache/residual-replay/arithmetic/Catalog.lean -o .cache/residual-replay/arithmetic/Catalog.olean'
lake env python3 scripts/check_omission_residual_geometry.py .cache/residual-replay/cycles --arithmetic .cache/residual-replay/arithmetic
lake env python3 scripts/check_omission_residual_blocks.py .cache/residual-replay/blocks --arithmetic .cache/residual-replay/arithmetic --cycles .cache/residual-replay/cycles
lake env sh -c 'LEAN_PATH="$PWD/.cache/residual-replay/blocks:$PWD/.cache/residual-replay/cycles:$PWD/.cache/residual-replay/arithmetic:$LEAN_PATH" lean -j 1 -s 32768 -M 6000 experiments/omission-residual-geometry-2026-10-09/ResidualReduction.lean'
```

On the original Mac use `ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place of
`lake`. The checker verifies every source hash, expected axiom report and
successful output. Resume records are bound to toolchain and prerequisite
hashes. Independent build directories keep these historical generic module
names separate from the balanced certificate. Use the new `--module-prefix`
export option and corresponding `--catalog-module` option for a future jointly
linked residual tree; renamed imports require fresh checks, not copied objects.

To regenerate the geometry, obtain the attributed source archive below and
run `omission_residual_geometry_export.py` and `omission_residual_block_export.py`
with its extracted directory and fresh output paths. The current scripts
reproduce these Lean sources byte for byte. Export metadata may differ because
module-prefix support was added after the recorded checks. The saved manifests
and successful check records are preserved unchanged.

## Attribution

The residual catalog, cycles and compression records are adapted from Michael
Schroeder, *Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*,
version 1, 19 September 2026,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891), under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Row indices, supports,
demands and orders are retained; checks are regenerated for this project's
actual real-point definitions and Lean kernel. Source proof code adapted in
the main library is MIT; the embedded Baek proof is Apache-2.0. Full notices
and file mappings are in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
No endorsement or independent-discovery claim is implied.
