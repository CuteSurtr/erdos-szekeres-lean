# ES(8) ≤ 311 — 14–18 October 2026

**`ErdosSzekeres.Omission.forces_convex_octagon_311 : ForcesConvexNGon 311 8`**:
every set of at least 311 points in general position in the real plane contains
eight points in convex position. The Lean kernel checked the complete chain on
19 October 2026 (Lean 4.24.0, Mathlib v4.24.0): the catalog, all 18,066
certificate parts and the root, the bridge `Final311/Bridge63.lean`, and the
assembly `Final311/Final.lean`. The axiom report of the final theorems is
`[propext, Classical.choice, Quot.sound]`; see [final-audit.out](final-audit.out)
and [final-report.json](final-report.json). `Final.lean` was compiled verbatim
with one appended `#check @ErdosSzekeres.Omission.forces_convex_octagon_311`;
since the file opens `ErdosSzekeres`, the audit prints the statement as
`Omission.forces_convex_octagon_311 : ForcesConvexNGon 311 8`, and
`ErdosSzekeres.ForcesConvexNGon` is the only declaration of that name. `certificate/kernel-check.json.xz`
is the complete per-module record. The check ran on one local machine and is
not part of the hosted CI workflow.

## The route

The 312 proof bounds the balanced population by 189 (at least 63 of the 252
balanced states missing) and the residual population by 121. Lowering the
balanced bound to 188 gives octagon-free sets at most `188 + 121 + 1 = 310`
points, so `ForcesConvexNGon 311 8`. This needs: no 0/1 hole vector satisfies
the 3,131 rows of the [balanced V2 catalog](../omission-cover-certificates-2026-10-10/balanced-v2-source.json)
(2,685 geometric rows and 446 checked rounding cuts) with at most 63 holes.
`Final311/Bridge63.lean` is the budget-generic bridge of the
[312 proof](../omission-final312-2026-10-13/README.md) with the catalog name
changed, and `Final311/Final.lean` combines `balanced_population_188` with the
residual bound 121 of the [313 proof](../omission-final313-2026-10-11/README.md).
No geometric input is new; the step is arithmetic over proved rows.

## The certificate

`search/pbb_strong.py` ran with budget 63 over 512 contexts (LP strong branching
with 40 candidates in the top twelve levels and 12 below; 10–11 workers, with
several interruptions and resumptions from saved contexts). The searched
contexts contain 1,562,913 logged nodes and took about 147 CPU-hours. No
assignment with at most 63 holes exists. The assembled tree (`search/assemble.py`)
has 1,564,873 nodes and 782,437 leaves; every leaf is a nonnegative integer row
combination with capacity margin at least 1, replayed with unbounded integers by
`scripts/omission_tree.check_tree` before export.

| Object | SHA-256 |
| --- | --- |
| Tree JSON (decompressed) | `d51f0dc2cee764867a0310b10d3981d20009d3d92a38844c03a6fef4e336e545` |
| Concatenated `certificate/tree-63.json.xz.part-*` | `e5380cc6f20c88c970ed9c5801e4b982c15822ba0214554d551a342666fa258c` |
| Tree as exported (gzip, recorded in `export.json`) | `ed32023ec7e6d3edfc42e7a8a61c359c32738bc55e8ca2712b918a11df5408c4` |

`certificate/export.json` is the manifest of the Lean export (namespace
`OmissionBalancedCover63`, prefix `BalancedCover63Proof`, 18,066 parts, 64
leaves per part, packing base 2^22) with the SHA-256 of every generated file.
It was produced by [scripts/omission_fast_export.py](../../scripts/omission_fast_export.py)
(proof style `fast_packed_lookup_v2`): each leaf keeps the statement of the
fused export, and its proof reads the catalog through packed lookups that the
catalog proves equal to `code` and `demand` row by row
([benchmark](../omission-fast-lookup-2026-10-17/README.md)).

## Kernel check

`search/pipeline.sh` runs the unattended completion: assembly and replay,
export, and `scripts/check_omission_lean.py` with resumable per-module records.
`search/finish.sh` then compiles `Final311/Bridge63.lean` and `Final311/Final.lean`
(with the appended `#check`) and audits the statement and axioms of
`forces_convex_octagon_311`. The catalog took 155 s; parts took 10–58 s each
(34 s median); the recorded module times sum to about 175 CPU-hours, including
the root, on 10 workers. Importing the
compiled parts dominates the last steps: the root took 5.5 hours and the
final compilation, which also imports the 313 chain, about 11 hours, because
the compiled parts far exceed main memory. The compiled parts occupy about 500 GB; they are not kept, and the
kernel record holds the SHA-256 of every object file.

## Reproduction

From the repository root, with the 313 chain built as described in its
[record](../omission-final313-2026-10-11/README.md) (the overlay of
[check.py](../omission-residual32-bridge2650-2026-10-11/check.py) and the residual
export):

```sh
cat experiments/omission-final311-2026-10-14/certificate/tree-63.json.xz.part-* \
  | xz -dc > .cache/es311/tree-63.json
cd scripts && python3 omission_fast_export.py \
  ../experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json \
  ../.cache/es311/tree-63.json --output ../.cache/es311/lean-export \
  --namespace OmissionBalancedCover63 --module-prefix BalancedCover63Proof --leaf-limit 64 && cd ..
lake env python3 scripts/check_omission_lean.py .cache/es311/lean-export --resume --workers 8 --memory 6000
```

The generated Lean files must have the hashes listed in `certificate/export.json`
(only the recorded tree hash differs, because the input is uncompressed). Then
compile `Final311/Bridge63.lean` and `Final311/Final.lean` with this export,
that overlay and the 313 chain on `LEAN_PATH`, as `search/pipeline.sh` does.
Plan for about 170 CPU-hours and 500 GB of disk.

The catalog and omission method derive from Michael Schroeder's version-1
archive; see [THIRD_PARTY.md](../../docs/THIRD_PARTY.md). No literature-priority
or best-known-bound claim is made in this record.
