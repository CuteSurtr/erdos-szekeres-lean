# A structural proof of the nine-state omission row

[`CoupledNineStructural.lean`](../../ErdosSzekeres/Omission/CoupledNineStructural.lean)
proves the existing nine-state obstruction by a short geometric construction.
The selected states are `{33,43,64,68,75,87,91,99,118}`. Every actual residual
configuration omits at least one: the explicit assumptions are no 6-cap,
no convex octagon, and no incoming 6-cup/outgoing 5-cap junction.

The four public roots, in `ErdosSzekeres.Omission.StructuralNine`, are:

- `context_impossible_structural`: the nine actual owners cannot coexist;
- `states_injective`: the nine state identifiers are distinct;
- `exists_missing_state`: some selected state is absent from the actual occupied set;
- `hole_bound`: the selected support has at least one hole.

The [complete explanation](interpretation.md) identifies a common convex
heptagon and two possible eighth points. If one owner lies to the right of
another, shared pair-rank growth makes the first candidate extend a single
visible edge. In the opposite order, one four-point orientation packet
makes the second candidate extend that edge. The generic
[visible-edge insertion theorem](../visible-edge-insertion-2026-10-10/README.md)
then supplies the convex octagon.

The proof directly imports `CoupledSemantics` and `VisibleEdgeInsertion`.
It does not import or invoke `CoupledCoreNine`, its literal CNF, or its LRAT
refutation. Small finite sign and domain tests still use ordinary kernel
reduction. This is an alternative proof of the same row, not an additional
independent constraint or a further numerical Erdős–Szekeres improvement.
It does not assert that arbitrary nine real points contain an octagon.

The maintained module builds successfully. The [saved audit](axiom-audit.txt)
prints all four roots and exposes the final geometric wrapper types. Every
root depends only on `propext`, `Classical.choice`, and `Quot.sound`; no
`sorry`, `admit`, `sorryAx`, or `native_decide` occurs in the new source.
The [validation record](validation.json) gives exact commands and source hashes.
The underlying residual-state catalog and rank geometry retain their existing
attribution in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md). No literature-priority
claim is made for this reconstruction or the insertion lemma.

## Two further structural instances

[`CoupledNineStructuralVariants.lean`](../../ErdosSzekeres/Omission/CoupledNineStructuralVariants.lean)
checks two more supports by the same geometric argument:

| Namespace under `ErdosSzekeres.Omission` | Support |
|---|---|
| `StructuralNine111` | `{33,43,64,68,75,87,91,99,111}` |
| `StructuralNineShifted111` | `{44,53,64,68,75,87,91,99,111}` |

Each namespace exports `context_impossible_structural`, `states_injective`,
`exists_missing_state`, and `hole_bound`, with the same explicit residual
hypotheses. These are two checked geometric rows. The implementation uses two
explicit instances of the structural proof, changing their state identifiers
and rechecking every finite domain/sign premise. The original structural
module and old literal certificate are unchanged.

The [variant audit](variants-axiom-audit.txt) and
[variant validation](variants-validation.json) cover all eight new roots.
The [candidate filtering diagnostic](candidate-filter-diagnostic.json) is an
exact finite search record that motivated these instances; its filtering and
compatibility classifications are not asserted as Lean theorems here. Neither
these rows nor that diagnostic alone establishes a smaller global octagon threshold.
