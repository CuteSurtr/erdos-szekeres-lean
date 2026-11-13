# ES(8) ≤ 313 — 12 October 2026

**`ErdosSzekeres.Omission.forces_convex_octagon_313 : ForcesConvexNGon 313 8`**:
every set of at least 313 points in general position in the real plane contains
eight points in convex position. The Lean kernel checked the complete chain on
12 October 2026 (Lean 4.24.0, Mathlib v4.24.0). Its axiom report is
`[propext, Classical.choice, Quot.sound]`; see [final-audit.out](final-audit.out)
and [final-report.json](final-report.json). The check ran on one local machine;
the certificate is too large for the hosted CI workflow.

## Structure of the proof

The [conditional bridge](../omission-residual32-bridge2650-2026-10-11/README.md)
proves `ForcesConvexNGon 313 8` from one finite statement: no 0/1 hole vector with
state 0 occupied satisfies all 2,650 residual rows with at most 32 holes. Every
row is bound to its geometric theorem; the balanced side is the existing bound 190.
This record supplies that statement and closes the chain.

| Piece | Lean declaration | Source |
| --- | --- | --- |
| Arithmetic exclusion | `OmissionResidual2650Zero.node1` | 10,325 generated parts, `Catalog` and `Root`, regenerated from [the certificate](certificate/) |
| Catalog identity | `OmissionResidual2650ZeroMatch.support_eq`, `demand_eq` | [Final313/Match.lean](Final313/Match.lean): 21 kernel-decided chunks of 128 rows |
| Assembly | `forces_convex_octagon_313`, `convex_octagon_of_card_ge_313`, `residual_excludes_2650_zero` | [Final313/Final.lean](Final313/Final.lean) |

## The certificate

An exact parallel branch-and-bound ([search/](search/)) answered the 32-hole
question over the [2,650-row catalog](../omission-residual32-rank-global-2026-10-10/README.md)
with state 0 occupied. Branching used LP strong branching (40 candidates in the
top twelve levels, 12 below) over 512 contexts. It found no assignment with at
most 32 holes. The assembled tree has 875,159 nodes and 437,580 leaves; its root
branches on state 0, and only the zero branch (state 0 occupied) is exported,
since the bridge uses the proved occupancy of state 0. Every leaf is a weighted
row combination with a positive exact integer margin (minimum 1). Numerical LP
values only proposed the weights; `scripts/omission_tree.check_tree` replayed
every leaf with unbounded integers before export.

`certificate/` contains the tree as two parts of one xz stream, the exporter
manifest `export.json` (SHA-256 of every generated Lean file), and the complete
per-module kernel record `kernel-check.json.xz`.

| Object | SHA-256 |
| --- | --- |
| Source catalog (decompressed `source-2650.json.gz`) | `e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6` |
| Tree JSON (decompressed) | `6b61f0ff91c7b1e4a66a2f360d414117f0ce2172193ea0076d9679a579061fdb` |
| Tree as exported (gzip, recorded in `export.json`) | `f983432a71016307d69721ba37ef4f08c2bccd012205ce56e3205c3a78a98eee` |
| Concatenated xz parts | `0e171397f13f679d7234cc3bea329313b3adb8173bce12e02178c1884df6a7a1` |

## Kernel check

[scripts/omission_context_export.py](../../scripts/omission_context_export.py)
exported the state-0 subtree with fused leaves (namespace
`OmissionResidual2650Zero`, module prefix `Residual2650ZeroProof`, 64 leaves per
part, packing base 2^21). `scripts/check_omission_lean.py` compiled the catalog,
all 10,325 parts and the root; each record has exit 0, a passing axiom audit and
the SHA-256 of its object file. Parts took 30–90 s; the root took 365 s. The
run was interrupted and resumed several times; resumed modules were accepted only
when their object hash still matched. Before assembly, all 10,327 object files
were hashed again, the inputs were compared with the checkpoint, and the final
chain and generated sources were scanned for `sorry`, `admit`, `native_decide`,
`axiom` and `unsafe` (none). `Match.lean` and `Final.lean` were then compiled
afresh and audited.

## Reproduction

From the repository root, with the bridge chain built by its
[check.py](../omission-residual32-bridge2650-2026-10-11/check.py):

```sh
cat experiments/omission-final313-2026-10-11/certificate/tree-2650-32.json.xz.part-* \
  | xz -dc > .cache/final313/tree.json
python3 -c "import gzip,shutil;shutil.copyfileobj(gzip.open('experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'),open('.cache/final313/source-2650.json','wb'))"
cd scripts && python3 omission_context_export.py ../.cache/final313/source-2650.json \
  ../.cache/final313/tree.json --output ../.cache/final313/export \
  --namespace OmissionResidual2650Zero --subtree 1 --module-prefix Residual2650ZeroProof --leaf-limit 64 && cd ..
lake env python3 scripts/check_omission_lean.py .cache/final313/export --resume --workers 8 --memory 6000
```

The export replays the whole tree before writing. Its generated Lean files must
have the hashes listed under `files` in `certificate/export.json`; only the tree
hash differs, because the input is uncompressed. The kernel check needs about
120 CPU-hours and 3–6 GB per worker. Finally compile `Final313/Match.lean` and
`Final313/Final.lean` with the export and the bridge overlay on `LEAN_PATH`.

The catalog and omission method derive from Michael Schroeder's version-1
archive; see [THIRD_PARTY.md](../../docs/THIRD_PARTY.md). No literature-priority
or best-known-bound claim is made.
