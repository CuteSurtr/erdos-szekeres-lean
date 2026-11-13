# Four omission rows found with rank-aware coupled search

This frozen discovery batch produced four new omission rows, of sizes 13, 13,
13 and 12. Their literal certificates and real-point geometric transfer live
in the adjacent
[rank certificate bundle](../omission-residual32-rank-certificates-2026-10-10/README.md).
Its current kernel audit is the authority for completed Lean results. The
search reports themselves are not proofs. This work does not establish
ES(8) ≤ 313, exclude all 32-hole Boolean assignments, or produce a geometric
realization of a Boolean assignment.

Each added row says that at least one state in its support is missing from an
actual residual configuration. The geometric hypotheses are real planar points
in general position with strict x-order, no six-cap, no convex octagon, and no
six-cup/five-cap junction. These are the residual hypotheses used by the
existing planar-bound transfer.

| Row | Support | Retained source-cup clauses |
|---|---|---:|
| One | 33, 43, 53, 65, 74, 77, 85, 89, 91, 96, 107, 110, 125 | 0 |
| Two | 1, 2, 7, 12, 18, 20, 27, 30, 33, 34, 39, 43, 53 | 16 |
| Three | 33, 43, 53, 65, 75, 77, 87, 89, 91, 99, 110, 111, 118 | 0 |
| Four | 1, 11, 23, 24, 30, 33, 34, 39, 50, 56, 67, 77 | 3 |

`rows-and-countermodels.json` preserves the ordered supports and four exact
33-hole Boolean countermodels. The countermodel for each new row satisfies
all 2,646 previous rows and every preceding row in this table, while occupying
the entire new support. Thus the additions successively strengthen the
Boolean catalog. These countermodels are not point configurations.

## What the new rank bound does

The search adds the chronological restriction

```text
cup(label(u,v)) ≤ firstColumn(state(u)) + 1, when u precedes v.
```

Rows Two and Four retain this restriction in their final refutations.
However, its use in a proof does not make it logically essential to the full
coupled model. The separately formalized
[clipping normalization](../omission-residual-rank-normalization-2026-10-10/README.md)
preserves satisfiability when each chronological cup coordinate is replaced by
its minimum with that bound. The new rank lemma therefore does not, by itself,
make this complete abstract model stronger. It supplied an additional proof
rule and a different search encoding. An old 11-state model with 15 rank-bound
violations was independently clipped and replayed; that sample is retained in
the normalization bundle.

## Exact local progress

Row One excludes 290 of the 306 previously saved feasible 33-hole assignments.
Row Four excludes all 16 remaining assignments. Together they exclude the
**entire saved component**, and Row One also excludes all 26 of its saved
32-hole near-models. This is a finite local result about the recorded component;
it is not an exclusion of all possible 33-hole assignments.

`check.py` independently replays source hashes, certificate support bindings,
all four successive strictness witnesses, and these finite coverage counts
using set counts and integer bit counts. It includes controls rejecting a
duplicate hole, a circular strictness witness, a premature claim that Row One
excludes the whole component, and modified source bytes.

```sh
python3 experiments/omission-residual32-rank-search-2026-10-10/check.py
```

This command uses only the Python standard library. It complements the
certificate bundle's independent RUP replay and Lean kernel checks; it does
not replace them. `check.json` records the successful replay.

## Discovery records and limits

The three bounded primary campaigns recorded:

| Campaign | Attempts | Necessary-model SAT | Solver UNSAT | Unknown |
|---|---:|---:|---:|---:|
| Initial near-model face unions | 9 | 8 | 1 | 0 |
| Further face unions | 64 | 54 | 6 | 4 |
| Common occupied states of the 16 survivors | 20 | 18 | 1 | 1 |

SAT here means only that the necessary abstract conditions have a model. The
four selected solver-UNSAT discoveries are superseded by the exact certificates
in the certificate bundle. Other unexported UNSAT reports are retained as
research diagnostics, not claimed theorems. Unknown probes remain unresolved.
The survivor campaign's first 15-state obstruction was reduced to 12 states;
all twelve one-state deletions produced checked abstract assignments. No Lean
minimality theorem is claimed.

`model.py` derives from the frozen witness-coupled model and adds the source-cup
bound to each allowed chronological direction, with a matching assignment
replay check. `probe.py`, `cnf_export.py`, `trim_core.py`, and `search/` preserve
discovery and export programs. Their cache paths are research reproduction
inputs, not portable CI dependencies. Z3, NumPy and CaDiCaL are needed only for
those discovery programs, not for the standard-library replay above. Large
formulas, full solver model collections and compiled objects remain ignored
under `.cache/rank313/`.

`model-provenance.json` pins the parent model and derivative. The parent
model's attribution to Schroeder's state data (CC BY 4.0) is retained; see
[THIRD_PARTY.md](../../docs/THIRD_PARTY.md). No third-party solver source or
binary is vendored in this bundle.
