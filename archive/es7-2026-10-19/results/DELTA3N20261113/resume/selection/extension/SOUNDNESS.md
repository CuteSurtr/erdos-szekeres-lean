# General terminal-safe formula: written projection proof

**PROVED logical reductions; implementation review and result checks are
separate.** A terminal-safe weak Delta A hits every whole convex (n-1)-gon,
has no four-cap, and every cap triple in A ends in an ambient rank-four
pair. The model has no five-cap and no convex n-gon on m points.

The compact geometric base is unchanged: ordered signotope packets,
no-five-cap clauses, exact four-set convexity, exact five-child convexity
recursion, and no-n-gon rows. Real general-position points have a canonical
assignment satisfying this base. No boundary localization is imposed here.

Four-cap flags are equivalent to all their negative triple signs. A bad
triple a<b<c is equivalent to its negative triple sign together with the
absence of every four-cap u<v<b<c. Under no-five-cap this is precisely a
cap triple of terminal rank three. Absence of bad triples excludes four-
caps too: a four-cap a,b,c,d has a bad prefix, since any ambient four-cap
ending b,c would extend by d to a forbidden five-cap.

The new bad-containment lattice aliases these exact flags at size three.
At each larger set it implies the disjunction of four one-point-deletion
children. Any three-element witness avoids one of those four deleted
vertices. Hence a true flag descends to an actual bad triple, and assigning
every flag its actual containment value satisfies all clauses together.
The recursion strictly decreases cardinality. The target lattice similarly
aliases exact Q at size n-1, and uses n deletion children above that size.
These one-way witnesses therefore have exact existential projection even
though arbitrary auxiliaries need not be their canonical values.

For every A of size 0<=|A|<=m-n+2 the failure row requires a bad triple in A
or a target in its complement. Missing flags below minimum witness size
mean false. All sizes zero, one and two are included: a terminal-safe set
cannot in general be grown to three safely. Larger working sets can be
shrunk to size m-n+2, preserving safety and leaving n-2 complement points.
Thus the full formula projects exactly onto failure of terminal-safe Delta
existence in its stated abstract model. Validated certified UNSAT implies
the real-point finite statement. SAT is not a real counterexample without
exact realization and independent geometry/selection checks.

`--stats` emits no CNF. The optional fixed-sign file explicitly restricts
the formula and is only a control/candidate tool. Accepted unrestricted
theorems must use `fixed_signs=false`. No symmetry or minimum-counterexample
assumption is used. Counts at a single m do not by themselves imply every
smaller size, because terminal ranks change when points are deleted.
