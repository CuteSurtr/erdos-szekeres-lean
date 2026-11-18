# Uniform cuts inside the four-cap-free left set

**PROVED (written), n>=5.** This concerns T_n(S) for a set S with no
four-cap and no n-gon. It is stronger than terminal selection on S and
must not be confused with the separate cut reductions for five-cap-free
full ambient sets.

If S has any nonempty x-separated cut P,Q on which each of the two types
P P Q and P Q Q has a constant sign, then Option1 of T_n(S) holds.
Thus the four possible sign patterns all suffice in this domain. No
finite T_n result or capacity theorem is used in this proposition.

## Two elementary tools

In a four-cap-free set, a single cup-ending rank level is a cup. Indeed,
a cap a<b<c in rank t would extend a t-cup ending at a by b, raising
b's rank. For t>=2, every vertex after the first in this level ends a
three-cap: if a<b share rank t, take the penultimate p of a longest cup
ending at a. The triple p,a,b must be a cap, otherwise b has rank>t.
Rank1 consists of just the first point.

There is also a left-end version with an extra hypothesis. If the
leftmost l starts no three-cap, then T_n(S) holds. Put k=n-1 and
V=S minus {l}. Every cup in V can be prepended by l, so V has no k-cup
(otherwise S has an n-cup). Let E be the right endpoints of k-gons in V.
The terminal polygon lemma makes E a cup, all of whose vertices end
three-caps in V. Then B={l} union E is a cup because every l,E,E triple
is a cup. It hits targets inside V at E and all other targets at l.
Only l is exempt from End3, exactly as required. Empty E is harmless.
This proves the stated left-end case; an unrestricted reflection of
the rightmost-point T_n lemma is not asserted.

## High split: P P Q cups, P Q Q caps

If Q is a singleton, it is the rightmost point and ends no three-cap.
The rightmost-point lemma applies directly.

Suppose |Q|>=2. Q is a cup: any Q three-cap preceded by any P point
would be a four-cap. Let c=maxcup(P). If c>=n-2, an (n-2)-cup in P and
any Q pair make an n-gon. Hence c<=n-3. A cup meeting both blocks uses
only one Q point, since a P Q Q triple is a cap; its size is at most
c+1<=n-2. A pure P cup also has size<n-1. Since Q is a cup of size at
most n-1, any (n-1)-cup in S is all of Q. It contains the rightmost point
of S. Deleting that point therefore removes every (n-1)-cup, and
[ROOTED_LEMMA.md](ROOTED_LEMMA.md) proves Option1.

## Low split: P P Q caps, P Q Q cups

If P is a singleton, it starts no three-cap, so the preceding left-end
lemma applies. Suppose |P|>=2. P is a cup: any P three-cap followed by
any Q point would be a four-cap. With d=maxcup(Q), an arbitrary P pair
and a maximum Q cup form a polygon, so d<=n-3.

Choose any p in P and set

    B={p} union {q in Q: beta_Q(q)=d}.

The rank level is a cup, and crossing p,Q,Q triples are cups, so B is a
cup. Every selected Q point ends an ambient three-cap formed with any
P pair. Consequently every B vertex after p has End3, even the first
point of the Q rank level.

An internal Q polygon has size at most d+1<=n-2, since Q has no four-cap;
there are no internal Q targets. An internal P target, if present, is
all of the cup P and meets p. A mixed target is a P cap joined to a Q
cup. Since P is a cup its P part has at most two vertices. A target can
therefore occur only with d=n-3 and a maximum Q cup, whose endpoint hits
the selected Q rank level. This proves Option1, including d=1 and n=5.

## All crossing triples are cups

For a singleton block use the corresponding left-end or rightmost-point
lemma. Otherwise both blocks have at least two points. Let c=maxcup(P),
d=maxcup(Q). The union of any P cup and Q cup is a cup, so c+d<=n-1 and
both c,d<=n-3. Neither block has an internal target, since its maximum
polygon is at most its cup maximum plus one.

Every mixed convex subset is a cup. A cap triple in either block together
with any point of the other block would have one point inside the
triangle on the remaining three, by the internal cap sign and the three
crossing cup signs. Thus each block's part of a mixed convex set must
be a cup, and all crossing triples are cups as well.

Take B to be the beta_P=c level. It is a cup, and all its nonfirst points
have End3 in P by the rank fact. A mixed target must concatenate maximum
cups from both blocks, because c+d<=n-1. It therefore meets B at the
endpoint of its P cup. This proves Option1.

## All crossing triples are caps

Two points on each side would form a four-cap, forbidden in S. Hence at
least one block is a singleton, and the pattern is already a high or
low split with its other crossing condition vacuous. The preceding
proofs apply. This internal argument is distinct from the full-ambient
five-cap-free [all-cap theorem](all_cap.md).

## Critical-size consequence and limits

A geometric T7 failure of size16 cannot have any of these four internal
cut patterns. It must also retain a six-cup after deleting its rightmost
point, have a three-cap ending there, and have a three-cap starting at
its leftmost point. These are necessary restrictions, not an existence
or classification theorem for the remaining configurations.

No new encoder or search was run for this reduction. The argument is a
written deduction from exact split geometry, the rank fact, and the
proved endpoint lemma. Its three nontrivial constructions are specified
above; numerical equality in a capacity theorem is not used to assume
that a cut exists.
