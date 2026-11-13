# Bounded 2,598-row residual search — 2026-10-10

This bundle freezes 2,598 necessary Boolean omission inequalities on 154 states.
The bounded searches did **not** find a satisfying 32-hole assignment and did
**not** prove that none exists. This bundle does not improve the maintained
planar bound `ES(8) ≤ 314`.

The best saved 32-hole candidate satisfies 2,597 rows. Its sole violation is old
row 205, with support `[24,31,34,40,61,68,73,100]` and demand one: none of those
eight states is missing. It is a near-model, **not a witness**. An independent
integer checker replays every row and rejects the candidate as a model.

## Frozen catalog and proved row bindings

All row numbers are zero-based. Every row means
`sum(hole[i] for i in support) >= rhs`, with Boolean `hole[i]`.

| Global rows | Source | Lean theorem establishing geometric necessity |
| --- | --- | --- |
| 0–2468 | Unchanged frozen 2,469-row catalog | Existing transfer in the [research bundle](../omission-residual32-research-2026-10-10/) and [remaining-row bundle](../omission-residual32-remaining-lean-2026-10-10/) |
| 2469 | New 13-state Sixth core | `ErdosSzekeres.Omission.CoupledCoreSixth.hole_bound` in [Geometry.lean](../omission-residual32-witness-coupled-2026-10-10/Geometry.lean) |
| 2470 + k, 0 ≤ k < 128 | Fourth template family, in saved local row order | `ErdosSzekeres.Omission.CoupledFourthGlobalVariants.all_rows` in [FourthGlobalProof/Root.lean](../omission-residual32-fourth-global-variants-2026-10-10/FourthGlobalProof/Root.lean) |

The geometric theorems apply to residual configurations with their stated
no-cap, no-octagon, and no-junction hypotheses. They are necessary conditions;
satisfying the Boolean rows alone would not construct a real point set.
The Sixth and Fourth theorem audit records are complete and report only
`Classical.choice`, `Quot.sound`, and `propext`. The Python checker binds those
records and source files by hash; a fresh Lean run uses their sibling checkers.

The [ordered-additions bridge](../omission-residual32-added-rows-2026-10-10/AddedRows.lean)
also passed a fresh Lean check. Its
`ErdosSzekeres.Omission.Residual32AddedRows.literal_binding` and `.all_rows`
theorems identify and validate the exact ordered 129-row tail of this source.

`family-source-manifest.json` records the complete global/local row correspondence
and ordered template injections. `fourth-row-bindings.json` is an exact snapshot
of the Lean family's row data. The unchanged source files retain historical
"prospective" metadata from when their proofs were being checked; the separate
`manifest.json` records the completed theorem bindings.

Decompressed SHA-256 identities:

| Catalog | SHA-256 |
| --- | --- |
| Frozen 2,469-row prefix | `f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909` |
| Intermediate 2,471 rows | `09756e694e643ebcb36bf5c6e763c890e986802c6adb803f99367aca7e81347b` |
| Final 2,598 rows | `01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b` |

The original 32-hole witness satisfies every frozen-prefix row but violates
exactly final rows 2469–2472. `candidates.json` also preserves this witness and
the earlier tabu candidate with two deficient rows.
The compact progress records are retained in `tabu-trace.json`.

## Completed bounded runs

| Run | Budget / work | Outcome |
| --- | --- | --- |
| 2,471-row SCIP search | 300 seconds; 62,201 nodes | Time limit, no witness |
| 2,598-row SCIP search | 300 seconds; 53,005 nodes; state 0 occupied | Time limit, no witness |
| 2,598-row tabu repair | 180 seconds; 476,917 iterations; 115 restarts | Best total integer deficit one |
| Exact local repairs | 3,968 two-exchange trials for each of two candidates | No repair in these neighborhoods |

Every solver used one thread. Tabu kept states 0 and 43 occupied and forced state
65 missing for its first 90 seconds, then released that last restriction. Its
results therefore do not exhaust all assignments. Exact local replay considers
two removed holes and two new holes while keeping states 0 and 43 occupied; it
does not rule out larger changes.

The ordinary LP minima were approximately 27 at the root, 27.301719 in original
context 2, 27.570630 in context 4, and 28.234272 in context 7. Fixing state 0
occupied did not materially change these values. These are numerical diagnostics,
not exact rational bounds or infeasibility certificates. No positive exact dual
contradiction was exported.

## Reproduce the exact checks

From the repository root, using Python 3.10 or newer and no third-party packages:

```sh
python3 experiments/omission-residual32-2598-primal-2026-10-10/check.py
PYTHONDONTWRITEBYTECODE=1 python3 experiments/omission-residual32-2598-primal-2026-10-10/test_check.py
```

The checker verifies compressed and decompressed identities, exact source
prefixes, all 129 appended rows and their ordered Lean bindings, saved script
hashes, set-based and independent bitset row counts, and the two saved local
repair neighborhoods. It confirms the failed searches are recorded as
inconclusive. Eight corruption controls test rejection of altered rows,
bindings, candidates, and repair counts. `exact-check.json` is the saved result.

`research-sources.json.gz` preserves the exact discovery scripts and imported
project helpers as UTF-8 text with individual hashes. These are historical scripts
with their original `.cache/` paths; replaying the numerical discovery requires
extracting them and the source inputs at those paths in a fresh checkout, plus
PySCIPOpt/SCIP, NumPy, and highspy as indicated by their imports. None of those
dependencies is needed for the exact checker. Scripts and project helper code are
this repository's research code; no solver implementation is vendored here.
Large logs, solver state, and build outputs remain in ignored `.cache/` storage.

All requested bounded runs have ended. Further search is deliberately paused;
there is no complete 32-hole exclusion certificate in this bundle.
