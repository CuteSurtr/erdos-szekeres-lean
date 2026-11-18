# The remaining purely geometric size16 step

**PROVED necessary reductions; the proposed compatibility step remains
UNPROVED.** The finite left16 proof-verification work belongs to the
parent and independent replay worker. This page does not claim a second,
purely geometric proof of universal T7.

Let S have16 points, no four-cap and no seven-gon. T7 is already
independently established through15, and capacity16 excludes larger S.
Any remaining geometric failure has maximum cup6; the absent-six-cup
case was proved in the frozen rank/endpoint work.

## Selector sizes are forced to five or six

Option2 is impossible: its two cups have sizes at most6 and5, totaling
at most11. For Option1, a cup B has size at most6. Its complement has no
six-gon and no four-cap, so checked Capacity11 gives |S minus B|<=11.
Therefore every possible Option1 selector has **size5 or6**.

If |B|=5, its complement is an11-point capacity-extremal set. Every
b in B has a private six-gon: deleting the other four selected points
leaves12 four-cap-free points, so Capacity11 forces a six-gon. Because
B hits every six-gon, that polygon intersects B exactly at b. This
does not imply such a B exists.

For any six-cup in S, its first point cannot end a three-cap and its
last point cannot start one. Either witness would extend the six-cup
to a seven-cup by the no-four-cap extension facts. Thus a size6 Option1
selector uses its first-vertex exception necessarily; the required
End3 witnesses at its other five points are still additional conditions.

## A precise extension candidate

Let r be rightmost and P=S minus {r}. A possible T7 failure must retain
a six-cup in P by [the rightmost lemma](ROOTED_LEMMA.md). It follows that
r ends a three-cap, since otherwise that six-cup would append r.
The through15 theorem supplies at least one Option1 selector B in P;
Option2 is impossible there too.

Call such B compatible with r if every triple a<b<r with a,b in B is
a cup. If a compatible B exists, then B union {r} proves Option1 in S:
it is a cup, old End3 witnesses persist, r has End3, old targets meet B,
and every new target contains r. A compatible B automatically has at
most5 points, since adjoining r to a six-cup would make a seven-cup.
Capacity11 applied to the15-point P gives |B|>=4.

**Unproved stronger candidate:** every such S admits an Option1 selector
B of P of size4 or5 compatible with r. This would solve the remaining
right-root case, but it is stronger than T7: a successful selector on S
could avoid r. A failure of this candidate would therefore not refute T7.

The exact missing inference is the passage from existence of an arbitrary
P selector to existence of a compatible one. If all P selectors fail
compatibility, each has a pair a<b with a,b,r a cap. The through15
certificate does not control these pairs. Replacing a selected vertex
using an End3 witness can repair a cap while losing a private target;
no simultaneous exchange argument has been proved.

## Structural reductions that do hold

[internal_cuts.md](internal_cuts.md) proves Option1 whenever S admits any
high, low, all-cup or all-cap cut. Therefore any critical failure is
indecomposable under all four patterns. The first point must start a
three-cap, the last must end one, and a six-cup survives deletion of the
last point. No claim that capacity equality forces a cut is made.

The existing Baek size proof does not by itself close the gap. Its
17-point induction removes five points and leaves12, where the next
capacity threshold forces a polygon. At16 the same count leaves11,
which is an allowed extremal size. The row deletion is not automatically
a cup transversal of all targets. The earlier a4 work also supplies a
real counterexample to indiscriminately trimming an already chosen cup
transversal; it does not refute the possibility of choosing a different
one. The known16-point controls already defeat either single top rank
as a general choice.

No additional computation, solver call, or tentative theorem promotion
is used for this page. Its conclusion is the proved restrictions plus
the explicitly unproved compatibility candidate.
