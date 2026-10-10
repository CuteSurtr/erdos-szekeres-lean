# A 32-hole model of the frozen residual catalog

`Witness.lean` proves that one explicit set of 32 holes satisfies all **2,469**
rows of the frozen catalog, with state 54 missing and states 43, 67 and 0
occupied. The witness leaves 122 abstract states occupied. Consequently, this
catalog alone cannot establish a universal lower bound of 33 holes, even with
these fixed states. This is **not a point configuration**, and does not refute
ES(8) ≤ 313 or change the completed 314-point theorem.

The standalone kernel check passes both modules and audits 15 conclusions,
using only `propext`, `Classical.choice`, and `Quot.sound`. There are no proof
placeholders or custom axioms. The modules import the same literal
`Residual32ContextsProof.Catalog` used by the completed geometric transfer.

| File | Main theorems (namespace `OmissionResidual32Case4`) | Meaning |
| --- | --- | --- |
| `Witness.lean` | `missing_card`, `all_rows`, `fixed_context`, `zero_occupied` | Exact cardinality, every literal row, and the fixed context |
| `Witness.lean` | `allows_thirty_two_holes`, `no_universal_thirty_three_hole_bound` | Boolean model and explicit refutation of the corresponding arithmetic exclusion |
| `ExistingFamilies.lean` | `all_first_variants` through `all_fifth_variants` | All 132 stored maps in these five template families also hold |
| `ExistingFamilies.lean` | `later_nine_rows` | The three later nine-state rows have four, three and three holes, respectively |

The source hash is
`f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909`.
`witness.json` contains the 32 indices; `check_witness.py` verifies all rows
using plain integer arithmetic. Exactly 588 rows are tight. The witness also
satisfies the three known rows omitted from the frozen catalog, so appending
those rows does not remove this obstruction.

The covering inequalities do not supply a common assignment of owner order,
pair-rank labels and triple orientations for the 122 occupied states. Those
geometric compatibility conditions remain the relevant missing information.
An arbitrary substitution into an existing template, or a new coupled
geometric obstruction, could supply a row that this witness violates. The
stored-variant checks do not exhaust all compatible substitutions.

## Reproduction

Run the independent finite check and its 22 regression/rejection tests:

```sh
python3 experiments/omission-residual32-case4-2026-10-10/check_witness.py
python3 experiments/omission-residual32-case4-2026-10-10/test_check.py
```

Build the maintained library and the catalog according to the
[context certificate bundle](../omission-residual32-context-certificates-2026-10-10/README.md)
first. Then run:

```sh
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
  experiments/omission-residual32-case4-2026-10-10/check_lean.py
```

The checker validates the frozen catalog's source and object hashes, matches
the Lean hole literal with `witness.json`, checks the source archive, and
records the imported project sources and objects. `--preflight-only` checks
inputs without compilation. `--catalog PATH` selects the catalog cache and
`--output PATH` selects a fresh build directory. All build products stay in
ignored cache. The complete proof record is `kernel-check.json`; the verbatim
axiom audit is `axioms.txt`.

The one-thread HiGHS search stopped on this witness after 138.53 seconds of a
600-second allocation. It processed 20,240 LP solves and generated 20,487 tree
nodes. Independent integer replay verifies 10,234 weighted leaves and reports
10 pending leaves; that partial tree is not an exclusion proof. The full
checkpoint is retained only in ignored cache at
`.cache/residual32-case4-2026-10-10/chunk1.json.gz`. Reproduce the search with the
project's solver environment:

```sh
.cache/solver-venv/bin/python -u \
  experiments/omission-residual32-case4-2026-10-10/search.py \
  .cache/residual32-resume-2026-10-10-b/source.json \
  experiments/omission-residual32-case4-2026-10-10/seed.json \
  .cache/residual32-case4-2026-10-10/reproduced.json.gz \
  --budget 32 --seconds 600 --strategy pseudocost
```

`search.py` and `conditional_check.py` adapt the archived resume bundle. The
fixed missing/occupied context is included in every search and replay leaf;
every binary split keeps both children. Numerical LP output can select a
branch but cannot close a leaf without a strict exact integer margin.

Original residual row data and attribution are preserved in the
[parent research checkpoint](../omission-residual32-research-2026-10-10/README.md).
Those data originate in Schroeder's attributed release,
DOI [10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891), under
CC BY 4.0. No additional third-party implementation is distributed here.
