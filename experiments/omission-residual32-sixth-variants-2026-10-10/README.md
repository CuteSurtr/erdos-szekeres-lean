# Reusable sixth coupled template

Three standalone Lean modules generalize the new sixth coupled obstruction to
any injective map of its thirteen owners that satisfies the frozen finite
compatibility tests. The shared LRAT refutation and all geometric clause
semantics are retained. All three modules passed kernel checking; four audited
conclusions use only `propext`, `Classical.choice`, and `Quot.sound`.

| Module | Declaration in `ErdosSzekeres.Omission.CoupledTemplateSixth` | Meaning |
| --- | --- | --- |
| `SixthTemplate.lean` | `Compatible`, `context_impossible` | The 159 state-dependent tests suffice for the shared 376-clause obstruction |
| `SixthTemplateCheck.lean` | `check`, `check_sound` | A Boolean compatibility test implies the stated prerequisites |
| `SixthTemplateGeometry.lean` | `exists_missing_index`, `hole_bound` | An injective compatible support omits at least one state in every actual residual configuration |

The concrete clause refutation is imported from the separate
[new-core bundle](../omission-residual32-witness-coupled-2026-10-10/LeanCore.lean).
No maintained module or earlier experiment was changed. The resulting row is
conditional on explicitly supplied injectivity and compatibility, with the
usual real-configuration hypotheses: no six-cap, no convex octagon and no
junction. This bundle proves no new global ES(8) bound.

A complete finite CSP traversal over all 154 candidate states found 30 distinct
compatible maps in 1.96 seconds: the new core itself and 29 additional supports.
It searched all available assignments rather than a coordinate neighborhood.
**All 29 additions are already implied by individual rows of the frozen
2,469-row catalog.** Only the previously proved base core adds strength to
that catalog. No further Lean compilation was spent on the redundant literal
instances.

`variants.json`, `row-bindings.json`, and `diagnostic-check.json` are explicitly
Python-only results. The last file independently rechecks injectivity, every
state-dependent test, and the strict row deficit establishing redundancy. It
does not certify search exhaustiveness in Lean. The claimed exhaustion is a
property of the recorded CSP run, not a formal theorem.

To replay the finite diagnostics:

```sh
python3 experiments/omission-residual32-sixth-variants-2026-10-10/check.py
```

To rebuild the generic proofs, first build the maintained library and the new
core's `LeanCore.olean` as documented in its bundle, then run:

```sh
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
  experiments/omission-residual32-sixth-variants-2026-10-10/check_lean.py
```

`--core PATH` and `--output PATH` select the prerequisite and output caches.
Only ignored cache receives compiled objects. `kernel-check.json` records
source/object identities and the complete standard-axiom audit;
`axioms.txt` preserves its output. The portable fresh-source order is
`LeanCore`, then `SixthTemplate`, then `SixthTemplateCheck` and
`SixthTemplateGeometry`.

`generate.py` adapts the repository's sized template exporter and the existing
Fifth-template check and owner-extraction proofs. `discover.py` adapts the
case-4 global CSP search. Original residual-state data and their CC BY 4.0
attribution remain in the [frozen research checkpoint](../omission-residual32-research-2026-10-10/README.md).
