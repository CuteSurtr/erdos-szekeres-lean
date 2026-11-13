# Sixfold refinement campaign, 2026-11-04

Status: stopped; final assessment margin reached. All task children were reaped.
The hard computation deadline was 2026-11-03 19:00 UTC
(2026-11-04 04:00 KST).

## Final retained status

The campaign retained 90 SAT models and 92 verified cut blocks.
The final formula has 58,626 variables and 9,198,581 clauses.
There were 40 fully GP-consistent candidate models; their exact
separations and any pending cases are listed in `survivor_outcomes.json`.

| Separation method | Candidates |
| --- | ---: |
| linear identity | 36 |
| product cycle | 2 |
| negative-definite quadratic obstruction | 1 |
| Pending separation | 1 |

Final formula SHA-256: `4281bf37057401b54a912b40d3466e83406debc38918712b3c7fffe29d08d041`.
Last retained model: `models/model0090.json`, SHA-256 `62b5c1d0ba4c9fb6d9b19a65c86d87f427853af388cf65d470dd73cae1f19f21`.
Its full-GP scan found 0 violations; its verified
input formula SHA-256 is `4281bf37057401b54a912b40d3466e83406debc38918712b3c7fffe29d08d041`.

Observed total-memory peak in this lane's samples was 28.115 decimal GB.
The corrected worker measured peak lane RSS of 2.002 decimal GB.
Initial GiB/GB guard correction is disclosed below.

Recorded UNSAT events: 0. All SAT, UNKNOWN or partial
LRAT traces are noncertificates. Any complete UNSAT trace still requires the
separately coordinated checker replays before a certified bound is claimed.
The final input was reconstructed from the durable base and exact cut prefix,
and compressed final input/proof artifacts passed decompression hash checks.

These experiments leave the sixfold maximum unresolved between 54 and 60.

This campaign refines the open 60-point sixfold-symmetric octagon-free case.
Its starting assignment satisfies the previous formula but violates 2,640 of
the 27,307,560 Grassmann–Plücker sign relations. The first refinement and a
verified family of six-literal linear determinant cuts produced a successor
that satisfies all 3,492,341 current clauses and all GP sign relations. This
remains a combinatorial candidate, not an established real configuration.

The first successor has no directed product cycle on any two- or three-orbit
restriction or in their complete union of 1,300,220 product-comparison edges.
The independent linear separation lane subsequently supplied additional
exact determinant identities. Final progress is recorded below at completion.

## Complete directed-product test on model 0033

Model 0033 satisfies its 5,139,093-clause input and every GP sign relation.
It survives all 375 two-, three- and four-orbit linear searches and product
cycle restrictions. The independent lane also retained an exact feasible
rational solution of the full linear lift; this is not a point realization.

The compact integer checker `m6_full_products.c` then enumerated all
4,551,260 rotation-reduced GP identities, representing all 27,307,560 anchored
identities. It retained both strict comparisons from each identity, giving
9,102,520 directed edges with multiplicity and 9,848,610 used product vertices.
Exact indegree pruning removed every vertex: the complete directed
product-vertex graph is acyclic. Three small-case comparisons matched all
29,880 edges against direct Python enumeration, and an independent Python DFS
agreed, including recovery of the archived five-comparison cycle. The full
check used approximately 412 MB child RSS; its complete evidence and compiler
provenance are under `full_product_model0033/` in the archive.

A retrospective complete check also found model 0001's entire product graph
acyclic, with the same coverage counts. Its six-row linear identity therefore
excludes a candidate that survives this complete directed-cycle class, not
merely the initial bounded searches. See `full_product_model0001/`.

This exhausts only directed cycles whose vertices are products of two bracket
magnitudes. It does **not** exhaust positive weighted combinations of bracket
exponent inequalities, general multiplicative final polynomials, or other
nonrealizability methods. Indeed, the independent lane subsequently obtained
an exact negative-definite quadratic obstruction for this same model; its
cut integration and real-configuration tests are recorded separately.

The reduced quadratic certificate uses 16 required-sign determinant rows on
five orbits. Their positive integer combination is a negative-definite
quadratic form in the seed coordinates, checked by exact rational LDL and an
independent direct-polynomial calculation. Its bounded family has 64,512
clauses: order-preserving orbit injections, 128 sampled relative-shift
patterns, and the valid coupled reversal of orbit direction and global sign.
Independent sign reversal is **not** a valid symmetry for this nonzero
quadratic inequality. The source passed 100 specified exact54 embeddings;
every emitted clause additionally passed two direct exact54 embeddings, for
129,024 family tests. This is finite corroboration alongside the universal
exact algebraic proof, not exhaustive testing of all embeddings. The family
is retained as `incoming/psd1006/` and was added before resuming the solver.

Later zero identities involving more orbits also use bounded lift families
and finite exact54 corroboration where full embedding enumeration would be
too large. Each `family_verified.json` records its actual coverage and test
count. Universal soundness rests on the exact identity and literal mapping;
the retained families are not claimed to exhaust all such identities.

## Evidence and scope

Model 0090 has an independently checked exact rational solution of all 5,710
strict linear orientation inequalities, with minimum margin `2/3491`; see
`logs/m6_primal0090_independent.json`. A two-by-two Gram minor of that
particular lift is negative, so the lift itself is not a real point
realization. This does not refute the model: another lift could behave
differently. A near-zero numerical SDP margin is likewise not an exact
nonrealizability certificate. Its final separation status is recorded in the
table and `survivor_outcomes.json`, separately from the exact linear-feasibility
result and complete directed-product acyclicity.

The archived base is the previous campaign's `family_run3/instance.cnf`, with
58,626 variables and 3,381,621 clauses. SHA-256:
`7889860ea9c629e9a00d8f1523ecfaaa6e02d615d88853b7695c6ab1985c50d6`.
Its initial model SHA-256 is
`437144235bdaf2045f30767432d7453a2199bb608fee49257dfb51554db9789d`.

GP clauses follow directly from the three-term determinant identity. The
rotational product and linear determinant cuts additionally use the specified
geometric sixfold action. They are sound for actual rotation-invariant point
sets; their argument does not assert a restriction on arbitrary realizations
of an abstract chirotope with merely combinatorial cyclic symmetry. Every cut
has exact verification and tests against the certified 54-point configuration.
These tests corroborate the literal implementation; the universal argument is
the accompanying exact determinant identity. Evidence here is exact computation
plus written algebraic proof, unless a separate dual replay is explicitly
recorded. No realizability or nonrealizability claim follows merely from a
solver timeout or failed separation search.

## Reproduction and archive layout

The archive root is `proof-archives/es8-rot-refine-2026-11-04/m6/`.
`base.cnf`, all `cuts/blockNNNN.clauses`, and all numbered models are immutable.
Each solver input has an `iterations/stepNNNN/input.json` record with its
complete ordered cut prefix, clause count, and SHA-256. The mutable
`current.cnf` is a convenience copy; historical formulas can be reconstructed
exactly without retaining repeated copies of the large base.

An iteration folder first assesses the **preceding** model, may append cuts,
and then records the **next** solve. Thus `assignment.json` and `gp/` in a
folder do not generally refer to that same folder's `input.json`. The `SAT`
event in `events.jsonl` explicitly binds an output model to its solver
`input.json`; use that binding when reconstructing and checking a model.
`survivor_outcomes.json` binds each full-GP assessment to its model SHA and
the exact identity that subsequently excluded it. An independent audit
reconstructed the inputs for models 0014, 0021 and 0024 and verified all
their clauses; see `logs/m6_reconstruction_audit.json` and its three check logs.

Run these verification commands from this results directory:

```sh
python3 -I m6_reconstruct.py --archive "$M6_ARCHIVE" \
  --input "$M6_ARCHIVE/iterations/step0000/input.json" \
  --output "$SCRATCH/reconstructed.cnf"
python3 -I m6_verify_assignment.py --cnf "$SCRATCH/reconstructed.cnf" \
  --model "$M6_ARCHIVE/models/model0001.json" --out "$SCRATCH/assignment.json"
python3 -I m6_full_gp.py --model "$M6_ARCHIVE/models/model0001.json" \
  --checker "$GP_CHECKER" --out "$SCRATCH/gp" --max-output 100000
```

The continuation uses `m6_worker.py`; command paths are runtime parameters.
The GP checker is built from the retained `m6_gpcheck.c` source. On a system
with the appropriate C SDK:

```sh
clang -O2 -isysroot "$MAC_SDK" m6_gpcheck.c -o "$GP_CHECKER"
python3 -I m6_worker.py --previous-archive "$PREVIOUS_M6_ARCHIVE" \
  --archive "$M6_ARCHIVE" --cadical "$CADICAL" --checker "$GP_CHECKER" \
  --deadline 2026-11-03T19:00:00+00:00
```

The worker runs one computational child at a time and initially caps each SAT
solve at 300 seconds. Its first version mistakenly expressed the total-memory
guard as 29 GiB rather than the intended 29 decimal GB. Its observed peak was
26.184 GiB = 28.115 decimal GB, below the intended ceiling. At 17:33 UTC it was
interrupted cleanly and resumed with a 29 decimal GB total-memory guard and a
separate 2.5 decimal GB guard for the worker plus its direct child RSS. The
interrupted formula remains reconstructible. `resource_guard_correction.json`
records this change; initial event-log `peak_total_gb` values are GiB, while
values after the `resumed` event are decimal GB. The initial worker and resumed
sources are both retained.

Child peak RSS and observed total memory are retained in the event log. The
worker never launches a proof checker; any UNSAT result requires a retained
LRAT and the separately coordinated checker replays before being called a
certificate.
