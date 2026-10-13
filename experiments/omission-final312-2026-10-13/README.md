# Toward ES(8) ≤ 312 — 13–14 October 2026

**Status: the arithmetic certificate is complete and replayed exactly; its Lean
kernel check is in progress. ES(8) ≤ 312 is NOT yet proved.** The completed
planar bound is 313. This file will be updated when the check finishes.

## The route

The 313 proof bounds the balanced population by 190 (at least 62 of the 252
balanced states missing) and the residual population by 121. Lowering the
balanced bound to 189 gives octagon-free sets at most `189 + 121 + 1 = 311`
points, so `ForcesConvexNGon 312 8`. This needs: no 0/1 hole vector satisfies
the 3,131 rows of the [balanced V2 catalog](../omission-cover-certificates-2026-10-10/balanced-v2-source.json)
(2,685 geometric rows and 446 checked rounding cuts) with at most 62 holes.
The transfer to actual configurations already exists: `Final312/Bridge62.lean`
is the budget-61 bridge of the 314 assembly with the catalog name changed, and
`Final312/Final.lean` combines `balanced_population_189` with the residual
bound 121 of the [313 proof](../omission-final313-2026-10-11/README.md).

## The certificate

`search/pbb_strong.py` (the 313 search, made generic in the catalog) ran with
budget 62 over 512 contexts on 8 workers: 187,464 nodes in 6.2 hours, no
assignment with at most 62 holes. The assembled tree
(`search/assemble.py`) has 187,975 nodes and 93,988 leaves; every leaf is a
nonnegative integer row combination with capacity margin at least 1, replayed
with unbounded integers by `scripts/omission_tree.check_tree` before export.

| Object | SHA-256 |
| --- | --- |
| Tree JSON (decompressed) | `e1c37b55fdf039a95da36d856800f2fb86808f4fb72fe89d3327e245c3fed7e2` |
| `certificate/tree-62.json.xz` | `91c0fa1be1c98221b4bb01d62337f7372df56530c563f52cbdf41e1ed93d45df` |
| Tree as exported (gzip, recorded in `export.json`) | `974ee0cd50c77bd49598aa9f56cd35dda52431c0d21c5ffb7b4ed1acd6ed0cad` |

`certificate/export.json` is the manifest of the fused Lean export (namespace
`OmissionBalancedCover62`, prefix `BalancedCover62Proof`, 2,167 parts, 64
leaves per part, packing base 2^22) with the SHA-256 of every generated file.

## Kernel check

`search/pipeline.sh` runs the unattended completion: assembly and replay,
export, `scripts/check_omission_lean.py` with resumable per-module records,
compilation of `Final312/Bridge62.lean` and `Final312/Final.lean`, and the
statement and axiom audit of `forces_convex_octagon_312`. Parts take about
95 s each; the full check needs roughly 60 CPU-hours.

The catalog and omission method derive from Michael Schroeder's version-1
archive; see [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
