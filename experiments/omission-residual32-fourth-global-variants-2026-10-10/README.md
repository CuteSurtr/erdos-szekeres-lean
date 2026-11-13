# Additional global substitutions of the Fourth template

**All 128 rows are kernel-checked.** `kernel-check.json` records `complete: true`
for all ten freshly compiled modules. Every audited theorem uses only
`propext`, `Classical.choice`, and `Quot.sound`.

This bundle adds 128 distinct literal support rows obtained from the existing
Fourth coupled-state template. Every support has 13 states and demand one.
The main theorem is
`ErdosSzekeres.Omission.CoupledFourthGlobalVariants.all_rows`, in
`FourthGlobalProof/Root.lean`: each row holds for every actual residual
configuration satisfying the usual no-six-cap, no-octagon, and no-junction
hypotheses. `kernel-check.json` records whether the full local check is complete.

The earlier catalog included a bounded search through one component of
single-coordinate substitutions. This search instead enumerates injective maps
using every explicit empty-direction, forbidden-domain, and positive-triple
condition in the formal Fourth template. A search over the 122 occupied states
of the 32-hole witness found exactly three compatible maps. All three provide
new rows violated by that witness. The full 154-state search stopped at 128 new
support sets; it is not an exhaustive classification of compatible maps.

The selected family contains those three witness maps first, then 125 other
distinct new supports. Every support differs from all positive-demand support
sets in the frozen 2,469-row source. `row-bindings.json` records the precise
ordered map, sorted support, and demand for every row.

`classify.py` checks whether an old row alone implies each new demand-one row:
an old demand `d` suffices when `d > |old support \ new support|`, because
each outside state contributes at most one hole. The exact, source-bound
`direct-implication.json` records **zero of 128** rows certified by this test.
This does not establish that all 128 rows are logically independent of the old
catalog: combinations of old rows may still imply some of them. The first
three are violated by the known assignment satisfying all old rows.

`Data.lean` defines all maps. Eight independent modules, `Part00.lean` through
`Part07.lean`, each kernel-check 16 injective maps against the complete template.
`Root.lean` combines the checks and applies the existing geometric transfer.
All finite checks use `decide +kernel`; no new SAT proof or native oracle is
assumed. These additional rows strengthen the relaxation and exclude the known
32-hole witness. They do not by themselves prove a new global planar bound.

Reproduce from the repository root after building its maintained library:

```sh
.cache/solver-venv/bin/python experiments/omission-residual32-fourth-global-variants-2026-10-10/search.py
.cache/solver-venv/bin/python experiments/omission-residual32-fourth-global-variants-2026-10-10/search.py --all-states
python3 experiments/omission-residual32-fourth-global-variants-2026-10-10/generate.py
python3 experiments/omission-residual32-fourth-global-variants-2026-10-10/classify.py
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
  experiments/omission-residual32-fourth-global-variants-2026-10-10/check.py
```

Search requires NumPy as used by the existing triple-table enumerator. The Lean
check requires no Python solver package. `--preflight-only` validates source
and row identities without compilation or writes; `--output` selects a fresh
object directory for portable checks. `test_preflight.py` rejects a corrupted
row-binding identity. Build outputs and detailed logs stay in `.cache/`.

The inherited catalog and geometric framework derive in part from Michael
Schroeder's companion archive,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
Attribution and licensing are in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
