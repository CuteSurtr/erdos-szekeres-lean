# Mathematical findings and their exact scope

This is a synthesis of the linked records, not a replacement certificate.
The active checkpoint and later outcomes are in [README.md](README.md).
Throughout, point sets are finite, in general position, with distinct
horizontal coordinates and their induced left-to-right order.

## Definitions

For a set U with no five-cap and no convex n-gon, a **weak Delta** is
A contained in U such that A has no four-cap and meets every convex
(n-1)-subset of U. A **terminal-safe** Delta additionally requires every
cap triple a<b<c in A to have an ambient four-cap ending in the exact
pair (b,c). This is a sufficient condition for extending A by admissible
rightmost points. Its failure need not be weak-Delta failure.

The weaker uniform-envelope condition allows domination by other ambient
four-cap terminal lines. The cup-support and endpoint-sign criteria are
orientation-based sufficient tests for that domination. Fixed-coordinate
uniform safety can depend on more than the orientation signs.

## Terminal selection has a sharp small obstruction

**PROVED minimum deduction, with CERTIFIED finite lower-bound inputs:**
at n=6 the smallest admissible U without a terminal-safe Delta has
exactly12 points. The explicit coordinates and192-clause membership
formula are in [terminal12](terminal12/README.md). An independent audit
checks its full geometry, all4096 selections and the lower-bound proofs
at sizes10 and11. Smaller sizes use an explicit separate theorem; no
ambient-size monotonicity is assumed.

**PROVED, Lean:** existence of that exact twelve-point real obstruction
is checked with the repository's actual convex-position definition. The
proof includes cardinality12, distinct x, general position, absence of
five-caps and hexagons, and the universal failure of terminal selection.
Its14 finite and5 real modules passed fresh parent builds. This Lean
statement proves the upper bound12 for the minimum; the lower bound is
still supplied by the audited finite-certificate chain.

The same set has945 ordinary weak Deltas. Its simplest displayed uniform
witness is {0,2,3,6}; a single exact rational line inequality protects its
only cap triple over the whole rightward ray. The parent enumerates848
uniform selections in these coordinates. See
[the explicit uniform certificate](terminal12/uniform/README.md).

**CERTIFIED and independently audited:** all admissible n=5 sets have a
terminal-safe Delta, by explicit coverage through6, separate certificates
at7 and8, and the size9 geometric exclusion. See
[terminal5_audit](terminal5_audit/README.md).

At n=7, the corresponding minimum is **14 or15**. The lower coverage
through13 has independent proof replay. A real15 obstruction has a
complete Lean real-geometry proof and a fresh parent replay. Every proper
restriction of that particular example has a terminal selector, but this
does not prove that every other14-point set does. See
[terminal15](terminal15/README.md) and [lean_real_parent](lean_real_parent/README.md).

## A stronger sufficient rule also fails on real points

**CERTIFIED and independently audited:** a different real15-point set
admits no cup-support Delta. Nevertheless it has7078 ordinary weak
Deltas and742 endpoint-sign-protected Deltas. Its two exact realizations
have3562 and3588 uniform selections, respectively, although all455
orientation signs agree. Both have uniform selections of minimum size4.
The membership difference is established by exact rational envelopes and
independent exhaustive replay, not floating-point optimization.

Thus the cup-support rule is not universally sufficient as a search
restriction, and uniform-membership families are not determined solely
by the orientation signs. Neither statement disproves uniform existence.
See [protection_models](protection_models/README.md) and
[the metric audit](protection_models/cup15_uniform/README.md).

## An abstract obstruction is excluded geometrically

**PROVED, written with independent exact replay:** the forced16 Boolean
model cannot be realized by real planar coordinates. A certificate has
387 strict bracket-product inequalities and positive integer weights.
Every bracket exponent cancels in their weighted product, contradicting
strict inequality. Both an independent worker and a separate parent
checker reconstruct the arithmetic; the parent also checks the symbolic
Grassmann--Pluecker identity. This does not rely on failed realization
searches or on a linear-programming solver's status.

This excludes only the fixed560-sign model. Other sixteen-point models,
real configurations and the general endpoint-sign conjecture remain
outside the result. See [the proof](protection_models/forced16_realization/VERIFY_FORCED16.md)
and [parent replay](protection_models/forced16_parent/README.md).

**PROVED, Lean, conditional algebra:** the fixed387 product inequalities
in560 positive variables are infeasible. The finite transcription,
sign/parity metadata and weighted cancellations are kernel-checked.
A fresh parent replay passed all338 modules and matched all354 exact
axiom reports. The coordinate-to-product bridge and Mathlib real adapter
are still outside this formal packet, so the real nonrealizability theorem
itself remains the written proof above. See
[the fresh certificate replay](protection_models/forced16_instance_parent/README.md).

## Smaller positive lemmas

**PROVED, written:** a cardinality-minimal terminal counterexample has
neither a high split nor a cut whose every crossing triple is a cup.
For a low split, its hard case reduces exactly to a predicate T_n(L) on
the left block alone. It asks for either a cup transversal of its internal
(n-1)-gons with the specified three-cap endpoint support, or a partition
into two cups with one part of size at most n-2. This equivalence transfers
any verified T_n(L) statement to arbitrary admissible right-block shapes.
See [structure2](structure2/README.md) and [low_split](low_split/README.md).

**PROVED, written composition using CERTIFIED finite inputs and Lean
capacity bounds:** T6(L) and T7(L) hold for every admissible left set.
Explicit small-size coverage and separate certificates cover all sizes
through11 and16, respectively; the geometric capacity theorems exclude
larger left sets. Every used finite formula has an independent soundness
audit and fresh accepted proof replay. The last original left16 proof
passed the clean independent retry at08:17:29 KST. See the complete
[universal closure and hashes](low_split/CLOSURE.md).

Consequently every admissible n6/n7 low join with at least two left
points has a terminal-safe selector. The singleton-left critical branch
still uses a selector on the right block. Therefore a cardinality-minimal
n6/n7 terminal counterexample has no low cut; an unconditional statement
about every low join is not inferred.

**PROVED, written:** for n>=5, if every crossing triple is a cap and both
blocks have at least two points, any one left point together with the
whole right block is a terminal-safe selector. No-five-cap forces both
blocks to be cups. The singleton-left case is also directly positive;
the singleton-right case follows from T_n. Thus all admissible all-cap
joins at n6/n7 are positive, without minimality. Two independent exact
control packets supplement this proof. See
[the all-cap lemma](low_split/consequences/all_cap.md) and
[independent review](fourcuts14_audit/VERIFY_FOURCUTS14.md).

**PROVED, written:** for every n>=5, a nonempty no-four-cap left set satisfies
Option1 of T_n if deleting its rightmost point leaves no(n-1)-cup.
This construction does not need the no-n-gon premise. Thus a potential
T_n counterexample retains a long cup after that deletion. The general
case is still open in this purely geometric argument; the finite T6/T7
closure above is separate. See
[the rooted geometric lemma](low_split/consequences/ROOTED_LEMMA.md).
A separate [parent integer check](low_split/rooted_parent/README.md)
passes3360 eligible cases, including400 containing an n-gon and50 where
the first selected vertex has no cap-end witness. These are controls,
not a finite exhaustion or an additional universal proof.
Combining that lemma with the audited transfers gives a
[size-free structured corollary](low_split/rooted_parent/COROLLARY.md):
the corresponding low joins with maxcup(R)<=n-4, and all-cap joins with
singleton R, are positive for any n>=5 under the rooted cup hypothesis.
This is a written composition; it does not close universal T8.

**PROVED, Lean:** weighted-envelope sufficiency and the at-most-two-support
principle supply a small exact witness format for metric protection;
the open and closed rightward-ray tests are equivalent. The Lean packet
records the precise hypotheses and standard-only axiom audits. See
[lean/FINAL.md](lean/FINAL.md).

## What remains open

The general weak D(5,7), weak D(5,8), and universal uniform-selection
questions remain open. The n7 terminal minimum still needs its14-point
case settled. The generic, three-cut, four-cut and no-six-cup14-point
searches all ended UNKNOWN; no failed search is evidence of either
existence or nonexistence. No result here improves an ES bound. These records have
not been refereed, published or committed; no novelty-priority claim is
made. Certificate-backed computations and handwritten reductions are
not described as a fully Lean-formalized theorem chain.
