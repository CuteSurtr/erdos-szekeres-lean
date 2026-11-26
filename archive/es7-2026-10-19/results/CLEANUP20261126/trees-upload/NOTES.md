Inputs that regenerate the generated Lean chunk sources of the ES(8) <= 302 end theorem (`Combined.es302_verdicts`,
repository erdos-szekeres-lean, record `archive/es7-2026-10-19/results/FORMAL20261122/combined`). Uploaded 26 Nov 2026.

| archive | source directory | what it is |
|---|---|---|
| `b69zs54.tar` | `~/research/data/bal186-20261119/zrow/b69zs54` | the budget-69 tree (EXACT TREE by two checks; Lean-checked as `E302ZZ.Final.excludes_69`); `files/` is read by `fv302-20261124/tools/export302.py` |
| `b67.tar` | `~/research/data/bal186-20261119/zrow/b67` | the budget-67 tree (FV304, `E304Z.Final.excludes_67`); `files/` is read by `export_es304z.py` |
| `es308-runs-inputs.tar` | `~/research/data/es308-20261114/{runs,inputs}` | the residual-slice trees and inputs read by `res-slices-fv/tools/slice_export_v3.py` (slices s33_18 to s35_20) |
| `ctx-manifests.tar` | `~/research/data/fv302-20261124/export/ctx`, `formalize-20261122/res-slices-fv/export` | the per-context export manifests |

Each archive is a POSIX tar (sorted names), split into parts of 1900 MiB. `SHA256SUMS` lists every part and every whole
tar; `<name>.list` is the tar's verbose file list. To restore one: download its parts, run
`cat <name>.tar.part* > <name>.tar`, check `sha256sum -c` against `SHA256SUMS`, and `tar -xf <name>.tar` in the source
directory's parent. The regeneration tests showing that these inputs reproduce the deleted chunk sources byte for byte
are in the repository: `FORMAL20261122/fv302/regen-test`, `FORMAL20261122/res-slices-fv/regen-test`, ES304N20261119.
