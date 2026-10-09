# Interpreting the checked nine-state obstruction

Read-only mathematical review of the frozen `core9.json`, CNF/LRAT, catalog
profiles, and `CoupledSemantics`. No new solver run was used. The complete
short geometric argument below is now kernel-checked in
`ErdosSzekeres/Omission/CoupledNineStructural.lean`. The generic insertion
lemmas are maintained in `ErdosSzekeres/VisibleEdgeInsertion.lean`.

## Names and exact scope

Write the nine owners as follows. The four entries are their Ferrers-column
profiles (the catalog's trailing zero is omitted).

| Name | Core index | State | Profile |
|---|---:|---:|---|
| A | 0 | 33 | (5,1,1,0) |
| B | 1 | 43 | (5,1,1,1) |
| C | 2 | 64 | (5,2,2,1) |
| D | 3 | 68 | (5,5,0,0) |
| E | 4 | 75 | (5,3,2,1) |
| F | 5 | 87 | (5,4,2,1) |
| G | 6 | 91 | (6,6,0,0) |
| H | 7 | 99 | (5,5,2,1) |
| I | 8 | 118 | (6,6,2,1) |

The letters are NOT chronological indices. Write `X < Y` for actual increasing
x-order, and `[XYZ]` for the determinant `orient X Y Z`.

All ownership and label statements below are under the existing residual
configuration assumptions: no 6-cap, no convex octagon, and no incoming
6-cup/outgoing 5-cap junction. In particular, `Context` already assumes
`noOctagon`, and the owner states depend on its proof. This is not a claim
that arbitrary nine real points contain a convex octagon.

## The certificate has exactly two alternative octagons

Its only two `no_octagon` clauses, original CNF clauses 279 and 280, concern

- `Q + A = {A,B,C,E,F,G,H,I}`;
- `Q + D = {B,C,D,E,F,G,H,I}`;

where `Q = (B,C,E,F,H,I,G)` is the common cyclic seven-point polygon.

Precisely, the checked propositional refutation implies that the first 278
clauses entail “all 70 four-subsets of Q+A are convex, OR all 70 four-subsets
of Q+D are convex.” The existing four-point convexity transfer turns either
alternative into a convex octagon when those atoms have their real semantics.
Removing the last two clauses does not remove the local rank/ownership
premises needed to make the other clauses true.

## A short structural explanation

The fixed-sign clauses give **every cyclic triple of Q positive**. I checked
all 35 triples against the literal fixed-sign data, including the parity of
the permutation from the displayed cyclic order to the canonical atom order.
Thus the common seven-point polygon is strictly convex in that cyclic order.
They also give every triple of `(A,B,C,E,F,H,I)` positive: this is a seven-cup
in its forced x-order. The latter full 35-sign fact is more than the short
argument needs.

The exact pair differences force

```text
A < B < C < E < F < H < I,        D < G < I.
label(A,B) = (4,1).
A < G  ==> label(A,G) ∈ {(2,2),(2,3),(2,4),(2,5),(2,6)}.
label(G,I) ∈ {(3,1),(3,2),(4,1)}.
```

The pair label is shared across all these uses. Its first coordinate is
`6 − maximum future-cap length`; its second is `maximum past-cup length − 1`.
Both coordinates lie in `[1,4] × [1,6]`. A chronological negative triple
strictly increases the first coordinate along its two pairs, and a positive
triple strictly increases the second. These are the existing `edge_allowed`,
`edge_bounds`, and `growth_clause` semantics. The forbidden junction cell
`(1,6)` is excluded when computing the pair differences.

Now split on the actual order of G and B.

### Case 1: B < G

Because the first coordinate of `label(A,B)` is already 4, the triple A,B,G
cannot be negative: it would require the first coordinate of `label(B,G)`
to exceed 4. General position therefore gives `[ABG] > 0`.

Also A<G<I. The second coordinate of `label(A,G)` is at least 2, while that
of `label(G,I)` is at most 2. Hence A,G,I cannot be positive, and `[AGI] < 0`.

Together with the five fixed signs

```text
[ABC], [ACE], [AEF], [AFH], [AHI] > 0,
```

these put A strictly to the left of every directed edge of Q except G→B,
and strictly to the right of G→B. For the closing two edges, use
`[IGA] = −[AGI] > 0` and `[GBA] = −[ABG] < 0`.

Thus A sees exactly the edge G→B. Inserting A at that edge gives a convex
octagon with cyclic order `(B,C,E,F,H,I,G,A)`.

### Case 2: G < B

Now D<G<B<H. The fixed signs say

```text
[DGH] < 0,       [DBH] > 0,       [GBH] > 0.
```

For the x-ordered quadruple `(D,G,B,H)`, the four-sign packet is therefore
`(sign[DGB], −, +, +)`. The packet condition allows at most one sign change,
so `[DGB] < 0`. By cyclic symmetry, `[GBD] < 0`.

The six other required side signs are fixed already:

```text
[BCD], [CED], [EFD], [FHD], [HID], [IGD] > 0.
```

Thus D also sees exactly G→B, so inserting D gives the other convex octagon,
with cyclic order `(B,C,E,F,H,I,G,D)`.

The two cases contradict the residual no-octagon assumption. The mechanism
is a choice between two points extending the same exposed edge of a common
heptagon. Chronological rank growth handles the first case; a single
four-point packet handles the second.

## The reusable lemma suggested by this explanation

**One visible edge insertion.** Let a strictly convex finite polygon have
at least three vertices in counterclockwise order. If a new point lies
strictly to the right of exactly one directed boundary edge and strictly to
the left of every other boundary edge, adjoining it preserves every old
vertex and adds the new point as a vertex.

An elementary proof avoids choosing a new cyclic order algebraically. Every
old vertex belongs to at least one unchanged incident edge; that edge is
still exposed because the new point lies strictly on its inner side.
Consequently its endpoints remain extreme. The new point is outside the
old hull, as certified by the violated edge, and is therefore also extreme.

This lemma is independent of the 154-state catalog and works for every
polygon size. Two generic roots are now separately kernel-checked in
`ErdosSzekeres/VisibleEdgeInsertion.lean`: retained supporting-pair
insertion, and its one-visible-edge corollary. The latter uses an explicit
finite edge family and requires the retained edges to cover every old vertex;
it has no hidden cyclic-order assumption. Their axioms are exactly the usual
`propext`, `Classical.choice`, and `Quot.sound`.

The complete combination is now separately formalized in
`ErdosSzekeres/Omission/CoupledNineStructural.lean`, under the distinct
`ErdosSzekeres.Omission.StructuralNine` namespace. Its roots
`context_impossible_structural`, `states_injective`, `exists_missing_state`,
and `hole_bound` all pass with only the same three standard axioms. The
maintained module imports `CoupledSemantics` and `VisibleEdgeInsertion`, and
never invokes or imports the literal nine-state CNF/LRAT theorem. The old
certificate remains unchanged as an alternative proof of the same omission
row. This reconstruction adds no numerical ES improvement.

## Checks and cautions

- All listed fixed signs were read from the 63 fixed-sign clauses. Both
  seven-point cyclic/cup patterns were checked by a small exact comparison.
- All three displayed label domains were calculated directly from the two
  Ferrers profiles, with `(1,6)` removed; no optimization or SAT search was
  involved.
- The trace has 243 atoms, 280 original clauses and 215 RUP additions. Only
  its final two original clauses express absence of an octagon.
- Independently tracing the existing RUP dependencies also shows that
  failure of Q+A entails `G<E` (RUP clause 484 uses clause 279 but not 280).
  The new checked first case obtains an octagon whenever `B<G`, using
  the full actual pair domains and the insertion lemma. This is stronger
  local geometric reasoning than that intermediate minimized-CNF deduction;
  no new global threshold is inferred from it.
- The smaller pair-label premises in this note use the FULL exact domains,
  not merely the selected domain exclusions retained by the minimized CNF.
  Therefore the short argument is a semantic reconstruction, not a claim
  that those stronger intermediate facts follow by unit propagation from
  the minimized clause list.
