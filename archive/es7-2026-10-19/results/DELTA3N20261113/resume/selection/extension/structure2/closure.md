# Cup-comparison closure has an exact two-triangle test

**PROVED (written):** on the set of all ordered point pairs, the transitive
closure of componentwise-right cup-union comparisons has a direct test
using at most two triple orientations. The closure is strictly stronger
than the original cup-union relation, even for protection of an actual
cap triple and a specified weak Delta in a real (5,7) set with maximum
cup five. No stronger global selection theorem is asserted.

## 1. Pair universe and the exact closure formula

Use all pairs (b,c), b<c, of a real set with distinct x coordinates and
no collinear triples. Put q -> r for distinct pairs q=(b,c), r=(u,v) when
b<=u, c<=v and every triple of the distinct vertices in their union is
a cup. Identity is allowed in reachability, so End4 pairs protect themselves.

Define D(q,r) by the componentwise inequalities and these two tests:

    c=v OR (b,c,v) is a cup,
    b=u OR (b,u,v) is a cup.                              (D)

**Theorem.** r is reachable from q by zero or more cup-union comparisons
if and only if D(q,r). Every reachable pair has a path of length at most
two, using the intermediate pair (b,v):

    (b,c) -> (b,v) -> (u,v),

with identity steps omitted.

The universe of all ordered pairs matters. If an implementation permits
only cap-triple terminal pairs as intermediate nodes, exact equivalence
to that smaller graph is not asserted. All pairs are legitimate supporting
lines; there is no geometric reason to require an intermediate line itself
to be a cap-triple terminal line.

## 2. Proof of the closure formula

Every cup-union comparison satisfies (D). Conversely (D) supplies the
displayed two-step path: the first union is {b,c,v}, the second is {b,u,v}.
When c=v or b=u, omit the corresponding identity step.

It remains to prove D transitive. Write ell_q, ell_p for the secant lines
of q=(b,c), p=(u,v). The two tests in D(q,p) give

    ell_p(x_b) <= ell_q(x_b)=y_b,
    ell_p(x_v)=y_v >= ell_q(x_v),
    slope(p) >= slope(q).                                (1)

The last inequality follows from the first two, since x_b<x_v. Equalities
at a test point are allowed exactly when the relevant endpoint is shared;
otherwise general position makes the determinant inequality strict.

Suppose also D(p,r) for r=(w,z). Componentwise order gives b<=u and v<=z.
Since slope(r)>=slope(p), the first inequality for p,r implies

    ell_r(x_b) <= ell_p(x_b) <= ell_q(x_b).

Since slope(p)>=slope(q), the second inequality for q,p implies

    ell_r(x_z) >= ell_p(x_z) >= ell_q(x_z).

These are exactly the two orientation tests in D(q,r), again with shared
endpoint tests omitted. Thus D is transitive. Every path is contained in
D, completing the equivalence. No cap, cup-length or polygon restriction
was used in this argument.

## 3. Consequence for ambient four-cap protection

A pair (b,c) is closure-protected precisely when some ambient four-cap
terminal pair (u,v) satisfies (D). Therefore the parent's proposed path
criterion can be encoded without recursive reachability variables:

    Covered(b,c) iff OR over u>=b, v>=c, u<v:
        End4(u,v)
        AND [c=v OR Cup(b,c,v)]
        AND [b=u OR Cup(b,u,v)].                           (2)

The identical pair is included. This is the exact closure of the parent's
cup-union rule, not merely another sufficient approximation. Every such
certificate gives one actual ambient line dominating ell_bc on the whole
rightward half-line. Unprotected pairs are forward-closed under D, hence
under every cup-union step.

For a selection, old four-cap exclusion must still be imposed separately.
The closure is contained in the one-ambient-line domination criterion, so
it cannot protect the safe two-support-only line from the frozen eight-
point example in `../theory/`. Exact envelope safety remains weaker.

## 4. A real nine-point strictness example

Index these integer points in the displayed order:

    0=(-1,-3), 1=(0,0), 2=(10,0), 3=(12,-20), 4=(16,-2),
    5=(20,13), 6=(30,1), 7=(40,40), 8=(50,100).

They are in general position with maximum cap four, maximum cup five and
maximum convex polygon size six. Exact finite checks give the complete
four-cap list

    0123, 0124, 0156, 3456, 3457, 3458,

and the complete hexagon list

    012578, 013678, 014678, 345678.

There is no five-cap and no six-cup. The five-cup 12678 attains the cup
bound. There is no seven-gon; a seven-gon would already supply seven
different convex six-subsets, whereas the list above contains only four.

The cap triple 016 has terminal pair q=(1,6). A two-step cup-union path is

    (1,6) -> (2,7) -> (5,8).

The corresponding four-cups are 1267 and 2578, with consecutive slopes
respectively (0,1/20,39/10) and (13/10,27/20,6). Pair (5,8) ends the
ambient four-cap 3458, whose consecutive slopes are (9/2,15/4,29/10).
The normal-form two-step path is (1,6)->(1,8)->(5,8).

There is no one-step cup-union certificate to any End4 pair. Among the
complete terminal-pair list, only (5,6),(5,7),(5,8) satisfy u>=1,v>=6.
Every relevant union contains the negative triple (1,5,6), whose determinant
is -370, so none is a cup. Pair (1,6) itself is not End4.

At X=50+t, the lines of (1,6),(2,7),(5,8) are

    q(t)=t/30+5/3,
    p(t)=4t/3+160/3,
    r(t)=29t/10+100.

Their slopes and heights directly confirm r>=p>=q for all t>=0.

Moreover A={0,1,6} hits all four hexagons and has no four-cap. Its sole
cap triple is 016. Thus A is a uniform weak Delta proved by closure, but
fails the original one-step cup criterion. This concerns a specified A:
{7} is another weak Delta and satisfies both rules, so no change in global
existence is claimed. The construction disproves collapse of the closure
to one-step protection even under all three geometric restrictions.

## 5. Relation to the rank-five selection task

An unprotected cap triple still forces beta(a)<beta(b), since the prior
rank lemma would otherwise give an identical End4 pair. On L4 union L5,
its first two ranks must therefore be 4,5. Forward closure under (D) adds
constraints on which terminal pairs may remain unprotected, but does not
by itself supply a polygon-hitting choice or justify replacing triples by
their first pairs. The explicit terminal18 obstruction to that replacement
remains relevant. A general structural selection implication remains
unresolved in this bounded track.

## 6. Separate replay and explicit four-cap warning

`tools/verify_closure_examples.py` rechecks the nine-point example using
the separate determinant and triangle-containment implementation, without
importing the closure finder. It exhausts the actual four-caps, hexagons
and seven-subsets, checks both displayed paths and their rational lines,
and verifies both the specified Delta and the alternative singleton.
Output: `data/closure_examples_replay.json`, status PASS.

Four-cap exclusion is necessary even after restricting to the top two
cup-rank levels in terminal18. Its four-cap C={3,4,8,10} has ranks
(4,5,5,4), and every selected triple has a one-step cup certificate:

* 348 uses ambient four-cap (0,9,12,13), via cup union {4,8,12,13}.
* (3,4,10) uses (0,5,6,10), via cup union {4,6,10}.
* (3,8,10) and (4,8,10) use the identical pair (8,10), ending (0,2,8,10).

The separate replay checks all positive determinants and line inequalities.
Thus neither the raw cup rule nor its closure makes the old four-cap
clauses redundant in this rank-restricted setting.
