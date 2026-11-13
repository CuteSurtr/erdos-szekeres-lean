# Coupled-template union and finite irredundancy

The two checked template families contain 42 and 35 rows. After removing
20 repeated unordered supports, their union has 57 distinct demand-one rows,
each on 13 distinct states. All twelve Lean modules have passed the complete sequential check and
standard-axiom audit. The [complete record](kernel-check.json) binds the exact
source and object dependencies; the [audit output](axiom-audit.txt) reports only
`propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, custom axiom or
native evaluation proof is used.

The [exact finite audit](exact-check.json) checks all 70,224 pairs consisting of
one union support and one original or prior geometric row. It finds **nine
independent additions and 48 rows already implied by original inequalities**.
Calling all 57 independent additions would therefore be incorrect.

This classification concerns the frozen 57-row union; adding later geometric
constraints may change which of its rows are independent.

The nine are first-family indices 6, 7, 10, 24, 25, 28, 38 and second-family
indices 8, 23 (all indices are zero based). For each selected support S, take
all states outside S as holes. This assignment satisfies all 1,187 original
rows, all 45 prior added rows, and every other distinct union row, while it
violates S's demand-one row. Each witness has 141 holes; these are finite
logical independence witnesses with no total-hole budget or claim of geometric
realizability. They are different from the earlier 32-hole strictness witnesses.

For each of the remaining 48 supports S, the audit identifies an original row
R whose demand exceeds the number of states in R outside S. Boolean holes
satisfying that original row must therefore include a hole in S. The generic
Lean theorem states this implication explicitly, with the Boolean condition.

The checked interfaces are all in
`ErdosSzekeres.Omission.CoupledUnion`:

| File | Main declarations | Scope |
| --- | --- | --- |
| `UnionCatalog.lean` | `support`, `all_rows`, `first_covered`, `second_covered`, `distinct_support`, `classification` | The exact deduplicated geometric family and its nine/48 classification |
| `Redundancy.lean` | `forced_hole_of_deficit`, `redundant_deficits`, `redundant_rows_implied` | All 48 redundant inequalities follow from individual original rows |
| `Independent00.lean`–`Independent08.lean` | `original_rows_00`–`original_rows_08` | Original-row checks for each selected complement witness |
| `Independence.lean` | `independent_each_selected_row` | Each of the nine is independent of the original rows, prior 45 rows, and other 56 union rows |

`support` is defined through a reference into one of the two checked geometric
families, and `all_rows` applies the corresponding existing theorem. A literal
support equality also binds the exact data checked by the finite controls.
No new geometric compatibility assumption is introduced.

Reproduce the exact controls with:

```sh
python3 scripts/check_coupled_union_exact.py \
  --output .cache/coupled-union-exact.json
```

Once the original catalog and library dependencies are built, run the
sequential Lean checks with:

```sh
ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 scripts/check_coupled_union_lean.py \
  --catalog .cache/omission-lean-full/residual \
  --output .cache/coupled-union-checked --memory 1500
```

Build products remain in ignored cache. The checker binds every local imported
source and object, the preserved original catalog record, the toolchain and
Lake manifest. A complete record requires all modules, unchanged inputs, and
standard-axiom audits. This artifact establishes no improved ES(8) bound.

The original residual row data are from Schroeder's attributed release,
DOI [10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891), under
CC BY 4.0, preserved in the earlier residual-geometry artifact. The two coupled
families and their geometric proofs are linked through the project modules;
this artifact does not redistribute additional third-party implementation.
