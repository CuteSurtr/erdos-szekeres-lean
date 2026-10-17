# Packed catalog lookups for omission leaves — 17 October 2026

This record measures a faster proof style for the weighted leaves of omission
certificates. It proves no new bound. The ES(8) ≤ 312 certificate is used only as
a benchmark; its accepted kernel check is unchanged.

## Where the time went

A fused leaf (`fused_sparse_packed_excludes`) decides one conjunction: packed
loads equal the weighted sum of row codes, and an integer margin is positive.
Each component of one leaf of the 312 export (node 8647 in `Part00098`) was timed
separately:

| Component | Kernel seconds |
| --- | --- |
| whole leaf | 1.44 |
| `code r` for the leaf's 194 rows (`row r` through nested `Array` lookups) | 1.12 |
| `packList`, coefficient bounds, `Finset` sums and cardinalities | < 0.05 |

So about 6 ms per catalog lookup, and nearly all the leaf time, went into reading
the catalog rather than into arithmetic. (`demand r` reuses the same `row r`
reductions.)

## The new style

[scripts/omission_fast_export.py](../../scripts/omission_fast_export.py) wraps the
fused exporter and adds to the end of the Catalog:

- `fastDemand r`, read from one packed natural number by a shift and a mask;
- `fastCode r`, read from 32-code chunks the same way (slots of
  `log₂(base) · states` bits);
- `fastDemand_eq` and `fastCode_eq`, proved for every row by one exhaustive
  `decide +kernel`;
- `fused_fast_excludes`, which rewrites the fused check through these equalities.

Each leaf keeps its statement word for word. Only its proof changes to
`fused_fast_excludes ... code_correct fastCode_eq fastDemand_eq`. The Root, the
branch theorems, and the checker contract (`Catalog`, `Part*`, `Root`, source
hashes in `export.json`) are unchanged.

## Measurements

Same host, Lean 4.24.0. The ES(8) ≤ 311 search was using 10 of 15 cores
throughout. Full numbers are in [benchmark.json](benchmark.json).

| Object | Fused | Packed lookups |
| --- | --- | --- |
| one leaf (node 8647) | 1.47 s | 0.56 s |
| `Part00098` (58 weighted leaves) | 108.4 s | 51.5 s |
| `Part00500` (46) | 83.1 s | 42.3 s |
| `Part01500` (41) | 71.7 s | 38.4 s |
| Catalog (once per export) | — | 220 s, 12.5 GB peak |

Parts are about twice as fast. What remains per part is mostly elaborating the
statements and the branch theorems. Turning off linters and code generation saved
another 6% on `Part01500`; that change was not adopted.

## Controls

- Raising the first weight of the first leaf of the fast `Part01500` by one makes
  Lean fail with exactly one error, for that leaf (the decided proposition is
  false).
- [scripts/test_omission_fast_export.py](../../scripts/test_omission_fast_export.py)
  checks that statements, the Root and the report fields match the fused export.
  It also checks that unexpected leaf shapes are refused. With
  `ERDOS_LEAN_FAST_TEST=1` it compiles a complete control tree and confirms that a
  corrupted coefficient is rejected.

## Use

```sh
cd scripts && python3 omission_fast_export.py SOURCE TREE --output OUT \
  --namespace NS --module-prefix PREFIX --leaf-limit 64
lake env python3 scripts/check_omission_lean.py OUT --resume --workers 8 --memory 6000
```

The pending budget-63 (ES(8) ≤ 311) pipeline uses this exporter.
