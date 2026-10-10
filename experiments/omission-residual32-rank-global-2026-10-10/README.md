# The 2,650-row residual search checkpoint

The current source contains the unchanged 2,646-row prefix followed by four
new geometric rows. Their [Lean certificates](../omission-residual32-rank-certificates-2026-10-10/README.md)
prove necessity for actual residual configurations. The decompressed SHA-256
of [source-2650.json.gz](source-2650.json.gz) is
`e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6`.
`catalog.py` regenerates the exact prefix and suffix from their frozen inputs;
it does not claim a global exclusion or a complete Lean catalog bridge.

**ES(8) ≤ 313 remains unproved. The completed planar bound is 314.**

## Exact finite progress

All 306 vertices of the previously saved 33-hole single-swap component satisfy
all 2,646 old inequalities and occupy state zero. Appending the new rows in
order leaves the following numbers:

| Catalog | Saved component vertices still feasible |
| --- | ---: |
| 2,646 rows | 306 |
| Add row One | 16 |
| Add row Two | 16 |
| Add row Three | 16 |
| Add row Four | 0 |

[coverage.json](coverage.json) records this replay. It does not enumerate all
33-hole assignments. Four separately checked 33-hole countermodels demonstrate
successive strict strengthening; see the [discovery replay](../omission-residual32-rank-search-2026-10-10/README.md).
Those countermodels do not represent real point configurations.

## Bounded global probes

Each probe asks for at most 32 holes with state zero occupied. The omission
rows are necessary conditions, so a SAT result would still need geometric
analysis. A solver timeout proves neither feasibility nor infeasibility.

The complete diagnostic records and compressed logs are retained in
[runs.json](runs.json). The SAT probes use the frozen shared-counter encoder
and CaDiCaL 3.0.1; the integer probe uses SCIP 10.0.2. Each has a 600-second
limit. The 2,647-row SAT and 2,649-row SCIP probes test intermediate prefixes;
the final SAT probe tests all 2,650 rows. No complete exclusion certificate
or feasible 32-hole assignment was obtained. Partial proof traces remain in
ignored cache storage and are not presented as certificates.

The global SAT encoding is experimental: its local finite controls are
separate from a general Lean soundness proof. An eventual complete global
refutation would require that encoding proof or transfer to the existing
checked arithmetic-certificate pipeline, literal row binding, and final
population composition. The four local coupled refutations already have
their own complete Lean semantic transfer.

## Reproduction

These commands use only the standard library:

```sh
python3 experiments/omission-residual32-rank-global-2026-10-10/catalog.py
python3 experiments/omission-residual32-rank-global-2026-10-10/test_replay.py
python3 experiments/omission-residual32-rank-global-2026-10-10/check_runs.py
```

The last command reproduces both SAT input hashes from the exact catalog
prefixes and binds the retained logs and SCIP source. It does not rerun the
solvers. Three controls reject altered row data and false coverage claims.

To launch another bounded full-catalog probe, with the optional solver
packages and local CaDiCaL executable installed, use a fresh ignored output
directory:

```sh
python3 experiments/omission-residual32-sat-resume-2026-10-10/run.py \
  --output .cache/residual2650-new-probe \
  --extra-rows experiments/omission-residual32-rank-global-2026-10-10/extra-rows.json \
  --encoder shared-counter --seconds 600 --seed 11 --configuration sat
```

`search/scip2649.py` preserves the exact intermediate integer probe. Its
outputs go to `.cache/rank313-root/`, as in the original experiment.
The inherited catalog's attribution remains in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
No solver executable, build object, or full partial proof trace is committed.
