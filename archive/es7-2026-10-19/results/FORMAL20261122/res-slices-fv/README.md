# FORMAL20261122/res-slices-fv: record copy for the residual-slice Lean campaign (started 26 Nov 2026)

The campaign's work directory is `~/research/data/formalize-20261122/res-slices-fv` (README there). Status 26 Nov 01:14
KST: all six slice exclusions are Lean-checked (`RS.s33_18`, `RS.s34_18`, `RS.s34_19`, `RS.s35_18`, `RS.s35_19`,
`RS.s35_20`; standard axioms); s35_20 accepted by its finish recipe (audit 3520: only profiler-split axiom lines,
settled by the 671-line reprint; axlines 23,485 / 23,485; leaf sum 119,054,033; minimum margin 1; no leaf-test
failure); the six-slice specialisation `RS.residual_bound_118_fv` (no slice hypothesis) compiled, snapshot in
`data/spec-snapshots/`.

This folder (so far): `receipts/` for the guarded deletion of the generated chunk sources `export/<TAG>/src/RS<TAG>/C*.lean`
of s35_20 (21,495 files, 100.24 GB) and of s34_18, s35_18, s34_19, s35_19 (4 + 40 + 148 + 1,411 files, 7.86 GB),
built by `receipts/mkrcpt3520.py` from each slice's audit (which re-hashed every source against its unit manifest) and
cross-checked against the manifests; `regen-test/`: the regeneration tests that allow it (s35_20: 25 units in 5 ranges,
327 modules, 1.56 GB; earlier slices: every unit of 3418, 3518, 3419 and 24 of 3519's 307, 299 modules, 1.53 GB; all
byte-identical to the campaign's files and to their manifest hashes; manifests equal except `seconds`). Kept: the
joins (Root, Sub*), `root-flat/`, `export/*/ctx` manifests and skeletons, `reprint/`, all oleans, and the es308 run and
input directories, which are now the only source to regenerate the chunk sources.
