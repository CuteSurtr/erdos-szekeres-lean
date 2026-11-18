# A geometric T_n lemma when the rightmost point meets every long cup

**PROVED (written).** This extends the earlier absent-long-cup partial to
sets that may contain an (n-1)-cup. It does not prove unrestricted T_n and
makes no novelty claim. The endpoint part uses the prior a4 argument;
the cap-end condition below is checked explicitly rather than assumed.

Let n>=5, put k=n-1, and let L be a finite real set in general position
with distinct x coordinates and no four-cap. Let r be its rightmost point
and P=L minus {r}. Suppose **P contains no k-cup**. Then there is a cup B
meeting every convex k-gon in L such that every point of B after its
first ends a three-cap in L. In particular, for admissible L this is
Option 1 of T_n(L). No no-n-gon hypothesis is needed for this construction.

Equivalently, the hypothesis says that r belongs to every k-cup in L;
it permits such cups to exist. A potential geometric counterexample to
T_n therefore retains a k-cup after deleting its rightmost point.

## Two elementary facts

If x<y<z is a cap in a four-cap-free set, every cup ending at x extends
by y: otherwise the penultimate p would make p,x,y a cap, and then
p,x,y,z a forbidden four-cap. One-point cups extend trivially.

Let E be the right endpoints of convex k-gons in P. Since P has no
four-cap and no k-cup, each such polygon has upper chain length three
and lower chain length k-1. Thus every e in E ends both a three-cap and
a (k-1)-cup in P. If e1<e2<e3 in E were a cap, the preceding extension
fact would make a k-cup in P. Hence E is a cup. This is the terminal
polygon lemma from [the prior a4 proof](../../../../../a4/theory.md), with
no external root.

## Case 1: r ends a three-cap in L

Take B=E union {r}. This is a cup. Indeed, any cap x<y<z in that union
has x,y in E and hence in P, because r is rightmost. Append y to a
(k-1)-cup in P ending at x using the extension fact. That would be a
forbidden k-cup in P. Thus no such cap exists.

Every k-gon contained in P meets E at its right endpoint. Every other
k-gon contains r. Every point of E already ends a three-cap in P, and
r ends one by this case assumption. Therefore every point of B, including
its first, has the required cap-end witness. Option 1 follows.

## Case 2: r ends no three-cap in L

Every triple a<b<r is then a cup. Let beta_P be longest cup-ending rank
in P and take

    B={v in P: beta_P(v)=k-1}.

If P is empty this means B empty. A cap x<y<z in B would again extend a
(k-1)-cup ending at x by y, giving a k-cup in P. Hence B is a cup.

Every internal P target has a lower (k-1)-cup and its right endpoint in
B, since the maximum cup length in P is at most k-1. A k-gon containing
r must itself be a k-cup: a longer upper chain would contain a cap
a<b<r, which is excluded. Deleting r from that k-cup leaves a (k-1)-cup
in P, whose right endpoint has rank k-1 and belongs to B. This proves
coverage also for targets containing r, even though r is not selected.

Finally, let b be any nonfirst point of B and choose a in B with a<b.
A longest cup ending at a has a penultimate p, because k-1>=3. If
p,a,b were a cup, appending b would give rank at least k at b in P.
Therefore p,a,b is a cap. It witnesses End3_L(b). No condition on the
first B point is required, exactly matching T_n's definition.

Both cases prove the claim. QED.

## A directly checkable boundary condition

If the rightmost r ends no three-cap, the hypothesis P has no k-cup
already follows from no n-gon in L: every cup in P appends r, so a k-cup
there would make an n-cup in L. Thus every admissible L whose rightmost
point ends no three-cap satisfies T_n by Case 2.

The first-point exception in Option 1 matters. For a pure k-cup L there
are no three-caps at all, but B may be the penultimate point alone; this
hits the only k-gon and meets the endpoint condition vacuously. Requiring
End3 at the first point would incorrectly reject this valid construction.

Consequently, any counterexample to T_n must both retain a k-cup after
deleting its rightmost point and have a three-cap ending at that rightmost
point. These are necessary conditions only. No reflection to an analogous
left-end statement is asserted: T_n's endpoint protection is directed.
Under the no-n-gon premise, the retained k-cup already forces that End3
condition at r, so these are not two independent structural restrictions.

For a small nonvacuous example with n=5, take the ordered coordinates

    (0,0), (4,4), (6,15), (8,16), (12,36).

They have no four-cap or five-gon, but {0,1,3,4} is a four-cup.
The prefix has no four-cup; its four-point target ends at index3.
The rightmost point ends the cap (1,2,4), so Case 1 selects B={3,4}.
Both selected vertices end three-caps. The exact control also checks
the analogous interior-point construction for n=6,7,8.

The [exact controls](CONTROLS.md) are separate from this written proof. The unrestricted
case, in which long cups remain in P, is still open in this geometric
argument. A cap among candidate endpoint vertices can then merely create
an allowed k-cup, so the extension contradiction no longer closes.
