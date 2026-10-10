# Exact geometric validity of the 129 added rows

This bundle connects the ordered suffix of the frozen 2,598-row source to the
already checked Sixth core and 128 Fourth-template substitutions. It adds no
new search and proves no global 32-hole exclusion or improved planar bound.
**The bridge passed fresh compilation in 13.979 seconds.** `kernel-check.json`
records both theorem audits, using only `propext`, `Classical.choice`, and
`Quot.sound`.

`AddedRows.lean` defines the 129 literal supports and kernel-checks their equality
to the geometric families in
`ErdosSzekeres.Omission.Residual32AddedRows.literal_binding`. The theorem
`ErdosSzekeres.Omission.Residual32AddedRows.all_rows` proves demand one on each
support for every actual residual configuration satisfying the no-six-cap,
no-octagon, and no-junction hypotheses. It uses the ordinary geometric theorems
from the two checked families, with no additional row-validity assumptions.

The exact order is local row 0 / global row 2469 = Sixth core, followed by local
row `k+1` / global row `2470+k` = Fourth family row `k` for `0 ≤ k < 128`.
`manifest.json` records each literal support and source index. The source's first
2,469 rows and state catalog are checked equal to the frozen original. Their
geometric validity remains in the separate existing transfer bundle; this
module does not recompile or replace that transfer.

The source archive is
`../omission-residual32-2598-primal-2026-10-10/source-2598.json.gz`, with
decompressed SHA-256
`01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b`.

After building the maintained library and the two imported experimental proof
families, reproduce with:

```sh
python3 experiments/omission-residual32-added-rows-2026-10-10/generate.py
python3 experiments/omission-residual32-added-rows-2026-10-10/check.py --preflight-only
python3 experiments/omission-residual32-added-rows-2026-10-10/test_preflight.py
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
  experiments/omission-residual32-added-rows-2026-10-10/check.py
```

The read-only preflight verifies all recorded source hashes, both decompressed
catalog identities, the unchanged prefix, the ordered literal suffix, and its
equality to the checked families. The negative control changes one source-row
index in memory and must be rejected before compilation. The local compiler
check also verifies imported object hashes against their successful kernel
records, then freshly compiles this bridge. Portable CI instead compiles all
dependencies from source into its own isolated cache. All build products remain
under `.cache/`.

The inherited catalog and geometric framework derive in part from Michael
Schroeder's companion archive,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
Attribution and licensing are in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
