# The parent's orientation-only cup-domination certificate

**PROVED sound sufficient rule; supplied by the parent.** Keep the four-
cap exclusion condition separate. This note checks the line implication
and its relation to the rank arguments; it is not a universal selection
existence claim or an audit of the parent's new CNF.

For a cap triple a<b<c, suppose an ambient four-cap ends in u<v, with
b<=u and c<=v in the common x order, and every triple of the distinct
vertices in {b,c,u,v} is a cup. Identical pairs are allowed separately.
Then ell_uv(X)>=ell_bc(X) for every X>=x_v, hence on the whole rightward
half-line X>max_x(U).

In a cup, secant slopes are nondecreasing when either endpoint moves to
the right. In this case the assertion follows explicitly by first moving
c to v and then b to u:

    slope(b,c) <= slope(b,v) <= slope(u,v).

Omit the first comparison if c=v and the second if b=u; these inequalities
also cover overlapping pairs and shared endpoints. If u=c the same
increasing-slope property applies. If v>c, the cup b,c,v gives

    ell_bc(x_v) < y_v = ell_uv(x_v);

if v=c the values are equal. Therefore

    ell_uv(X)-ell_bc(X)
      = y_v-ell_bc(x_v) + (slope(u,v)-slope(b,c))*(X-x_v) >= 0.

If b=u and c=v the two lines are identical. This proves the rule for all
componentwise right shifts, not just disjoint four-cups b<c<u<v.

The rule is definable by point order, triple orientations and actual
ambient four-cap flags. It is sufficient, not necessary for domination:
the frozen eight-point two-support example in `../theory/` has a safe
terminal line that is not dominated by any single ambient line.

For a selection A, excluding its old four-caps and requiring this rule
(or an identical ambient terminal pair) for each selected cap triple
suffices for uniform extension. Excluding only the unrescued triples does
not ensure A is an old weak Delta. The prior seven-point example has an
old four-cap whose triples pass an envelope test, so four-cap clauses must
remain unless a separate theorem makes them redundant in a restricted model.

**Withdrawn fixture claim, preserved.** The parent initially proposed that
the terminal18 witness A={0,5,6,7,8}, whose only cap triples are 056 and 057,
was certified by ambient four-cap (6,7,14,17) via four-cups (5,6,14,17)
and (5,7,14,17). The parent then reported an independent correction: both
quadruples have signs ++--, so neither is a four-cup. A one-off determinant
bug caused that false claim; no result here relies on it. The specific
certificate is withdrawn. The parent retains the failed quick-check
receipt. The parent subsequently reported an independently checked count
of 1,639 cup-protected Deltas on terminal18, with a different minimum
selection {0,2,3,14,15}. This track does not reproduce that whole-set count.

The parent owns the generic nonexistence CNF and another worker owns
pool-wide probes; neither is duplicated here. The proposed specific
quadruples were independently checked here as negative controls: both
indeed have signs ++--. The exact determinants are retained in
`data/independent_replay.json`.

For the separated theorem, the selected set is a single rank level and
every selected cap triple already has an identical ambient terminal pair.
Thus the separated proof supplies an existence subclass for the new rule.
The later restricted top-two-level tests in this track also give explicit
positive cup-protected selections on terminal18. Neither observation is a
general selection theorem.

## A real positive control for the line implication

The exact general-position, five-cap-free seven-point set

    (0,-8),(1,1),(2,4),(3,-10),(4,11),(5,25),(6,36)

has ambient four-cap (3,4,5,6). It certifies cap triples 012, 015 and 016
via terminal pair (5,6): their cup unions are respectively {1,2,5,6},
{1,5,6}, {1,5,6}. This exercises a strict four-cup, a shared intermediate
endpoint, and a shared final endpoint. At X=6+t the three target lines
are 3t+16, 6t+31 and 7t+36, while the ambient line is 11t+36.
The independent replay checks all stated turns and the line inequalities.
This is a certificate control, not a full selection theorem for that set.
