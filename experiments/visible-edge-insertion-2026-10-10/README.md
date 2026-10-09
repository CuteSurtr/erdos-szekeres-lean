# Convex insertion through one visible edge

[`VisibleEdgeInsertion.lean`](../../ErdosSzekeres/VisibleEdgeInsertion.lean)
proves two generic real-plane results, with no catalog, rank, avoidance, or
hidden general-position hypothesis:

- `ErdosSzekeres.VisibleEdgeInsertion.convexPosition_insert_of_retained_pair_supports`:
  an exterior point preserves convex independence when every old vertex retains
  a supporting pair-line that strictly separates the new point and the other vertices.
- `ErdosSzekeres.VisibleEdgeInsertion.convexPosition_insert_of_one_visible_edge`:
  a directed supporting-edge family permits insertion of a point outside one
  edge and inside all the others, provided the retained edges cover every old vertex.

All supporting-side and coverage conditions are explicit in the theorem types.
The second statement uses a finite edge family; no cyclic polygon representation
is assumed implicitly. Both checked roots use only `propext`, `Classical.choice`,
and `Quot.sound`; see [the audit](axiom-audit.txt) and [validation record](validation.json).

The [nine-state interpretation](nine-core-interpretation.md) explains why this
lemma arose: two possible eighth points extend the same edge of a common
heptagon. The complete reconstruction is now also
[kernel-checked through a structural proof](../omission-coupled-nine-structural-2026-10-10/README.md).
The original nine-state CNF/LRAT proof remains unchanged.
This artifact does not claim a further numerical Erdős–Szekeres improvement or
literature priority for the insertion lemma.
