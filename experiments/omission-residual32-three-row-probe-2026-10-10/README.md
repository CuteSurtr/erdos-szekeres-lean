# Three-row probe of the residual checkpoint

The three newly proved nine-state inequalities were tested at the 24 pending
contexts of the frozen residual 32-hole checkpoint. They closed no additional
context in this probe. Five contexts already admit exact weighted contradictions
using the original 2,469 rows alone. The remaining 19 are unresolved.

`diagnostic.json` preserves all five cuts, their contexts, exact input hashes,
the geometric provenance of the tested additions and the numerical LP results.
The positive integer margins are 11, 1, 159, 13 and 21. They were replayed by two
separate integer calculations. They are **not Lean-checked certificates**, and
the complete literal research catalog has no finished Lean transfer. No new
planar bound follows. The frozen large tree was not edited and still records
24 pending leaves.

For independent replay, let `M` and `O` be the prescribed missing and occupied
states, let `U` be the remaining states, and let `c` be the stored capacity.
Each nonnegative row weight contributes its weighted demand to `D` and its
weight to each incident state load `L_i`. Under the 32-hole budget, the weighted
left side is at most

`sum(i in M, L_i) + c * (32 - |M|) + sum(i in U, max(L_i - c, 0))`.

The stored margin is `D` minus that expression, and is strictly positive for
each cut. Every referenced row is below index 2,469, so none of the three
appended rows is used. The other 19 contexts have reported numerical LP optima
below 32; those floating-point values are neither integer witnesses nor exact
feasibility proofs. No search or solver remains running.

The source catalog and attribution are preserved in the
[parent research checkpoint](../omission-residual32-research-2026-10-10/README.md).
