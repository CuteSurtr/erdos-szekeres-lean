# closure-src: the remaining sources of the ES(8) <= 302 import closure (mirrored 26 Nov 2026)

`Combined.es302_verdicts` imports 69,731 modules (`data/closure3.tsv` in the work directory; `data/audit3.json`). As
of 26 Nov their sources are accounted for as follows (`MANIFEST.tsv` lists the 198 files of this folder):

| modules | where the source is |
|---|---|
| 4,811 | public: the Lean toolchain v4.24.0 and Mathlib `f897ebcf` with its packages (`lake-manifest.json`) |
| 427 | already in git, found by content (the repository's `ErdosSzekeres/`, `FORMAL20261122/*` mirrors such as `fv302/joins/`, ENCBLEAN and other records) |
| 198 | **this folder**: 149 generated sources of the 311 compact chain (`experiments/omission-compact-checker-2026-11-05/build/chain311/src`, written by `build_chain311.py`), the 40 files of the residual-slice library `RS/` (`res-slices-fv/lean/RS`) and the 9 assembly files of FV304 `E304Z/` (`fv304-20261120/export/src/E304Z`) |
| 64,295 | generated chunk modules, not mirrored (about 190 GB of text): `E302ZZ.C*` 32,953, `RS35xx/RS34xx/RS3318.*` 23,135, `E304Z.C*` 8,207. Their generators are in git, and byte-identical regeneration was tested (`FORMAL20261122/fv302/regen-test`, `res-slices-fv/regen-test`, ES304N20261119 "Regenerable") from the kept inputs (`bal186-20261119/zrow/b69zs54`, `zrow/b67/files`, `es308-20261114` runs) |

The files are copied byte for byte; each `sha256` in `MANIFEST.tsv` is that of the source on disk. Where two
byte-identical copies existed, the build directory's copy is named. Only this folder was added; no compile reads it.
