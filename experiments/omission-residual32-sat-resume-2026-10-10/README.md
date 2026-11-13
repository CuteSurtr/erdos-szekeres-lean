# Residual32 SAT comparison, 2026-10-10

This experiment tests the Boolean omission-row relaxation on 154 hole
variables, with at most 32 holes and state 0 occupied. It does not add a
planar theorem or improve the maintained bound. No state-43 restriction is
used in the global runs.

The frozen 2,598-row source is
`../omission-residual32-2598-primal-2026-10-10/source-2598.json.gz`.
Its decompressed SHA-256 is
`01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b`.
The augmented comparison adds the 48 literal rows in
`../omission-residual32-sixth-relaxed-2026-10-10/rows.json`, SHA-256
`6b5693be0d1e1c19f4acd6090b4f25d88204a596a8daba93bbb089e43e7cbb7b`.
The geometric kernel status of those rows is recorded in their own bundle;
the SAT experiment does not establish that transfer.

## Results

| Probe | Rows | Encoding / solver | Wall time | Outcome |
| --- | ---: | --- | ---: | --- |
| Original global system | 2,598 | Z3 sorting CNF / CaDiCaL | 300.04 s | UNKNOWN; 9,296,194 conflicts |
| Augmented global system | 2,646 | Shared-counter CNF / CaDiCaL | 300.03 s | UNKNOWN; 6,492,530 conflicts |
| Augmented global system | 2,646 | Native pseudo-Boolean / RoundingSat | 310.67 s | TIMELIMIT; 1,092,580 conflicts |

All three searches retain the full row list, impose at most 32 holes, and
require only state 0 to be occupied. None returns a budget-32 model or an
UNSAT certificate. Different encodings and row sets make the conflict totals
unsuitable as a speed comparison; this experiment does not show that SAT
outperforms the earlier primal searches.

Two trivial controls exercise the complete CaDiCaL checking pipeline:
budget 26 is UNSAT, independently DRAT-verified (the input already contains
a 27-hole lower-bound row), and budget 154 is SAT with 153 holes, checked
against all 2,598 original rows and all 125,149 CNF clauses. These are
pipeline controls, not new mathematical bounds. The original encoder's four
tests and this bundle's four counter/OPB tests pass.

`results.json` contains the SAT records. `roundingsat-result.json` preserves
the parent experiment's record verbatim, including the historically pending
geometry scope; `roundingsat-provenance.json` records the cached source commit
and build without SoPlex. No LP calls occurred in that native PB run.
`regenerate_opb.py` recreates the 2,646-row OPB file byte-for-byte and
independently replays all integer coefficients, with expected SHA-256
`d46d9fe1ab9f2a76ad6e193880d6debce403a30d5d05f10d211c37581dbb86f6`.

## Methods and checks

`run.py` uses the cached CaDiCaL 3.0.1 executable, a single solver worker,
fixed seeds, explicit wall-clock limits, and binary DRAT output. There are
two encoders:

- The existing Z3 5.1.0 sorting/cardinality encoder in
  `scripts/omission_cnf.py`.
- `shared_counter.py`, an independent deterministic threshold circuit.
  A gate `T(xs,k)` is constrained to be equivalent to
  `T(xs[:-1],k) OR (xs[-1] AND T(xs[:-1],k-1))`. Gates with identical
  prefixes and thresholds are shared. Small row lower bounds use the exact
  direct clauses over complements of `(rhs-1)`-subsets. The global upper
  bound asserts that threshold 33 is false.

The shared-counter controls exhaust all assignments through seven original
variables for each gate truth value, and through six variables for combined
rows, budgets, occupied states, and optional neighborhood restrictions.
These finite controls are not a general Lean correctness proof.

A returned SAT assignment must satisfy the DIMACS clauses and every source
row by exact integer arithmetic, with independent set and bitset counts.
An UNSAT result is checked independently with `drat-trim`. A timeout is
inconclusive, and its unfinished DRAT prefix is not an UNSAT certificate.

The optional `--radius r` restricts holes outside the saved best candidate
to at most `r`. Such a run is explicitly a conditional local exclusion,
not a global residual32 exclusion.

## Formalization boundary

The repository already has Mathlib's `Mathlib.Tactic.Sat.FromLRAT` and the
term-producing `ErdosSzekeres.Omission.CoupledLrat` wrapper. To obtain a
kernel-checked residual theorem from a successful global run, one would
still need an LRAT refutation, a proof that every satisfying hole assignment
extends to the generated CNF auxiliary variables, and all geometric row
transfer and state-0 reduction hypotheses. The threshold recurrence gives
a simple candidate for the encoding proof, but it is not formalized here.
Certificate size is a practical concern: the initial 300-second global
search already generated about 1.48 GB of unfinished binary DRAT output.

No maintained Lean source, axiom audit, README, manuscript, or CI workflow is
changed by this experiment. Large CNF/proof/log artifacts remain under
`.cache/resume313-sat/`; small result records describe their hashes and scope.

## Reproduction

From the repository root, with `z3-solver` available to Python and the cached
solver/checker binaries available:

```sh
python3 -m unittest discover -s experiments/omission-residual32-sat-resume-2026-10-10 -p test_shared_counter.py
python3 experiments/omission-residual32-sat-resume-2026-10-10/run.py --output .cache/resume313-sat/fresh-sorting --seconds 300
python3 experiments/omission-residual32-sat-resume-2026-10-10/run.py --encoder shared-counter --extra-rows experiments/omission-residual32-sixth-relaxed-2026-10-10/rows.json --output .cache/resume313-sat/fresh-2646 --seconds 300
python3 experiments/omission-residual32-sat-resume-2026-10-10/regenerate_opb.py --output .cache/resume313-sat/fresh-2646.opb
```
