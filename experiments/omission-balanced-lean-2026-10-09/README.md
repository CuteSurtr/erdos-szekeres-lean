# Complete balanced omission certificate

The **entire balanced tree** is checked in Lean 4.24.0: 19,723 nodes,
9,862 leaves, 898 proof parts, and the final root. The literal system has
252 states and 2,685 rows. These are finite combinatorial results; their
geometric necessity for real point sets has not been proved here.

The full part/root build completed locally on 7 October 2026. On 9 October,
we recovered the unpushed results, verified every generated source against its
manifest, reproduced all generated sources byte for byte, rechecked the catalog
and root, and proved the explicit occupancy corollary. This was not a second
full-tree rebuild. See `validation.json` and the original per-module output in
`build-results-2026-10-07.jsonl`.

## Exact conclusions

- `OmissionBalanced.code_correct` proves every packed row encoding matches its
  literal support.
- `OmissionBalanced.excludes_budget`, in the generated `Root.lean`, proves that
  no function `holes : Fin 252 → ℕ` with values at most one satisfies every
  catalog demand and has total at most 59.
- [`OmissionBalanced.occupied_card_le`](Occupancy.lean) proves that any
  `occupied : Finset (Fin 252)` satisfying
  `∀ r, demand r ≤ (support r \ occupied).card` has `occupied.card ≤ 192`.

All three have only `propext`, `Classical.choice`, and `Quot.sound` as transitive
axioms. There are no placeholders, custom axioms or native evaluation proofs in
the generated sources or the corollary. **This is not `ForcesConvexNGon 317 8`.**
The residual tree and all required geometric transfer remain separate work.

## Reproduce the kernel check

Build the repository's pinned library first. The archive contains exactly 900
Lean source files, with no compiled objects. Build outputs stay in the ignored
cache. From the repository root:

```sh
mkdir -p .cache/omission-balanced-lean
tar -xzf experiments/omission-balanced-lean-2026-10-09/sources.tar.gz \
  -C .cache/omission-balanced-lean
cp experiments/omission-balanced-lean-2026-10-09/export.json \
  .cache/omission-balanced-lean/export.json
lake env python3 scripts/check_omission_lean.py \
  .cache/omission-balanced-lean --resume
lake env sh -c 'LEAN_PATH="$PWD/.cache/omission-balanced-lean:$LEAN_PATH" lean -j 1 -s 32768 -M 6000 experiments/omission-balanced-lean-2026-10-09/Occupancy.lean'
```

The checker verifies source hashes, compiles sequentially with one Lean worker,
requires the expected axiom report after every module, and records successful
outputs in `kernel-check.json`. Resume records bind sources, toolchain, library
objects and compiled output hashes. A full run may take hours. A partial block
run is explicitly recorded as incomplete. The default GitHub build checks the
main library and small positive/negative exporter controls, not this large tree.

On the original Mac, replace `lake` with
`ELAN_HOME="$PWD/.elan" .elan/bin/lake`.

## Reproduce the export

`row-source.json.gz` preserves the exact upstream balanced JSON, including its
original weaker certificate. Only its states, supports and demands are used by
the exporter. Our stronger certificate is the separately committed
`../omission-balanced-59-2026-10-05.json.gz`.

```sh
gzip -dc experiments/omission-balanced-lean-2026-10-09/row-source.json.gz \
  > .cache/omission-balanced-original.json
python3 scripts/omission_lean_export.py .cache/omission-balanced-original.json \
  experiments/omission-balanced-59-2026-10-05.json.gz \
  --output .cache/omission-balanced-regenerated \
  --namespace OmissionBalanced --leaf-limit 16
```

The output directory must not already exist. `export.json` records generation
only; its `lean_checked: false` field is intentional. Successful checking is
recorded separately rather than inferred from generation or Python replay.

## Attribution

The catalog and original row-source data are adapted from Michael Schroeder,
[*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*, version 1,
19 September 2026](https://doi.org/10.5281/zenodo.22842891), under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). We preserve the row
indices, supports and demands, add integer encodings and a stronger certificate,
and generate new Lean arithmetic proofs. No source Lean module is imported and
no endorsement is implied. See [third-party provenance](../../docs/THIRD_PARTY.md).
