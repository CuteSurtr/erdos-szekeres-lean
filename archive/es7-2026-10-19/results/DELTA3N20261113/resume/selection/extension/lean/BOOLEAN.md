# PROVED: fixed 15-variable, 313-clause Boolean refutation

Completed and freshly replayed by the parent at 06:17 KST, 14 November 2026.
The source is `Terminal15Boolean.lean`; it has no explicit imports beyond Lean's
implicit core `Init` environment.

## Statement

`Delta3.Terminal15Boolean.terminalFormula` is the conjunction of all 313 original
DIMACS clauses, in their original order. Its fifteen arguments are propositions.
Positive literal `i` denotes `p_i`; negative literal `-i` denotes `¬p_i`.

The three checked theorems are:

- `core_unsat`: the specified 98 original clauses imply `False`;
- `terminal_unsat_prop`: the full 313-clause formula implies `False`;
- `terminal_unsat_bool`: no assignment of fifteen Boolean values satisfies the
  formula when `p_i` means `b_i = true`.

## Model and soundness

This is a Boolean refutation of one fixed formula. Coordinate validity, geometric
encoding, convexity, and the connection to Delta-selection remain external.
It is not a Lean proof of the entire geometric 15-point counterexample.
The source has no `sorry`, custom axiom, `native_decide`, or `Lean.ofReduceBool`.
All three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`.
Irredundancy and minimum core size are not claimed as Lean-checked results.

## Method

The parent's supplied tree has 85 nodes, 43 conflict leaves, and 197 unit steps.
`generate_boolean.py` translates each unit and conflict into ordinary elimination
of the original clause's disjunction. Branches use `Classical.em`; their two proof
branches cover both truth values. No SAT verdict or executable Boolean reduction
is admitted as an axiom.

The full-formula theorem extracts the 98 selected clauses through conjunction
projections, then applies `core_unsat`. The Boolean theorem instantiates the
propositional theorem with the fifteen equalities `b_i = true`.

A separate syntax roundtrip parsed the generated formula back to integer literals
and matched all 313 rows and 1,548 literal occurrences exactly to the DIMACS file.
It also checked all 98 core hypothesis rows and the fifteen-Boolean interpretation.
The generator checks all supplied unit reasons, conflicts, and branch variables;
the resulting proof terms are then checked by Lean. This source correspondence
audit is recorded separately from the kernel theorem.

## Results

| Check | Seconds | Kernel maximum RSS (KiB) | Axiom reports |
|---|---:|---:|---:|
| Core environment probe | 0.093 | 346,804 | 2 probe declarations |
| Finished Boolean source | 12.003 | 560,420 | 3 |
| Fresh parent replay | 11.818 | 583,912 | 3 |

Both finished-source checks exit zero with no warnings or guard stop. The first
check sampled anonymous memory at 249,808 KiB, virtual address at 805,660 KiB, and
swap at zero. The checked scratch source and repository source are byte-identical.
The final generator, using the copied input artifacts, reproduces the same hash.

## Controls

The existing bounded CLI wrapper uses one CPU, `-j1 -M1000`, AS 4 GiB, RSS guard
1300 MiB, a 27-second inner deadline, and a 30-second outer timeout. All checks were
short probes; no long Lean unit was required. The Lean slot was released before
the parent replay, so no two Lean checks overlapped. All original algebra sources
and their manifests remained unchanged.

## Files and hashes

| Artifact | SHA-256 |
|---|---|
| `Terminal15Boolean.lean` | `cd50fd74384bea5a17d93ba9f15ce52762df8bf8c872e30fbe8c4780687d9463` |
| Original CNF | `7d18c713d190d893a4d3d7873e8caa7d45061326c403ee8133888382040cc22a` |
| Core CNF | `d04ad6b75aeec577d766842207040ad174ad2562fba3b96a0748da1dbc4f12f0` |
| DPLL tree | `5d91e4eb69b074ba20a9915b1c4d707347a749ca0d352671106e99c0a6675e77` |

Inputs are copied as `data/terminal15-{original.cnf,core.cnf,tree.json,core-DONE.json}`.
The producer log and JSON are `data/boolean-v1.*` (the original scratch run tag was
`boolean-step-1`). Source correspondence is in `data/boolean-input-audit.json`;
generation metadata is in `data/boolean-generation.json`.
`data/boolean-manifest.json` hashes the source, runner, generator, inputs, and evidence.
Parent replay logs are under `data/parent-replay/`, indexed by
`data/parent-replay-manifest.json`.

## What remains

This fixed Boolean refutation is complete. The geometry connection and any
irredundancy or minimum-size claims are outside this packet. Any subsequent
geometry formalization must use a separate record and must not alter these files.

## Resume commands

Under an explicitly available Lean slot, from the repository root:

```bash
/usr/bin/timeout --signal=TERM --kill-after=2 30s \
  /usr/bin/prlimit --as=4294967296 --core=0 /usr/bin/taskset -c 4 \
  python3 -B cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/lean/check.py \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/lean/Terminal15Boolean.lean \
  boolean-replay
```

The generator is optional for replay; the checked source is already present.
Running `python3 -B .../lean/generate_boolean.py` regenerates the source only in
the authorized scratch directory, using the copied input files in this record.
