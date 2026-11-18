# A second cut reduction: every mixed triple is a cup

**PROVED (written).** Fix n>=5. Let U=L disjoint-union R be nonempty
x-separated blocks of a real general-position set with no five-cap and
no n-gon. Suppose **every mixed triple is a cup**. If both blocks have
at least two points, U has a terminal-safe weak Delta. If one block is
a singleton, the only remaining case reduces to a protected Delta in
the other block. This is separate from the frozen high-split packet and
requires no cup-length hypothesis or novelty claim.

Write c_L=maxcup(L), c_R=maxcup(R). A mixed convex subset must have a cup
in each block. Indeed a cap triple within either block would have its
middle point inside the triangle of its outer vertices and any point
of the other block; all three triangle-side signs follow from the mixed
cup condition. Conversely two cup parts have all their internal and
mixed triples positive, so their union is a cup. Consequently

    maxcup(U)=c_L+c_R<=n-1,
    mixed convex subsets are exactly the mixed cups.

If c_L,c_R<=n-3, choose the union of the two local top cup-rank levels:

    A={v in L: beta_L(v)=c_L} union {v in R: beta_R(v)=c_R}.

Each level is terminal-safe within its own block; a rank-one level is a
singleton and needs no predecessor argument. No selected mixed triple
is a cap, so the union creates no selected cap or four-cap across blocks.
Existing ambient terminal certificates survive in U.

An internal (n-1)-gon has lower cup length at least n-3. Thus, in either
block with cup maximum at most n-3, such a target either does not exist
or has its right endpoint in that block's top rank level. A mixed target
requires c_L+c_R=n-1 and uses a maximum cup in each block, so it meets
both levels at their last points. Therefore A hits every target.

If both blocks have at least two points, both cup maxima are at least
two, so the bound c_L+c_R<=n-1 gives c_L,c_R<=n-3 as required. Otherwise
the only uncovered possibility is that one maximum is n-2 and the other
is one; the latter block is a singleton. Any protected Delta of the
larger block extends by adding that singleton: all new selected triples
are cups and every new target contains the singleton. This works at
either end, for terminal, cup, closure, orientation-forced and uniform-
envelope protection. For a left singleton the old rightward domain is
unchanged; for a right singleton it only shrinks.

For an m-point real counterexample, cuts 2<=k<=m-2 of this type can thus
be excluded unconditionally. The two end cuts require the same property
at size m-1, unless their noncritical case is established separately.
The negated-cut clause is simply

    OR over all triples meeting both sides of cut k: NOT Cup(a,b,c).

As with the high-split reduction, this is a geometric soundness statement,
not an unconditional equivalence of abstract SAT formulas. The right
singleton cut coincides with the corresponding high-split condition;
the left singleton cut coincides with the corresponding low-split one.
No encoder or solver was run by this track for these clauses.

It follows by cardinality induction that sets recursively decomposed
using high splits or these all-mixed-cup splits admit terminal-safe
Deltas under the same no-five-cap/no-n-gon hypotheses. Proper-block
inheritance is used only in the singleton critical case. Selecting
subsets can enforce the usual |A|<=m-n+2 bound, as proved in the frozen
high-split note.

## Exact controls

An interior n5 control consists of two four-caps with all mixed triples
positive. Their local rank-two levels each contain a selected cap triple,
protected by the corresponding four-cap. This checks the smallest n and
nonvacuous terminal certificates. Additional n6/n8 interior controls and
left/right singleton n7 lifts are in `data/cup_join_controls.json`.
These exact checks are not exhaustion or a finite universal theorem.
