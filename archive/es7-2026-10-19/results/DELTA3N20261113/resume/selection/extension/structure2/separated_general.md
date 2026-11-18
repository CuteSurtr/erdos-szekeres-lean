# Favorable selection for separated sets, every n>=5

**PROVED (written).** The parent pointed out this generalization of the
n=7 proof in `separated_theorem.md`. Both blocks below are explicitly
nonempty. No novelty, Lean formalization, global weak-Delta theorem or
numerical ES bound is claimed.

## Statement

Let n>=5 and let U be a finite real point set in general position with
distinct x coordinates. Assume U has no five-cap, no (n-1)-cup and no
convex n-gon. Suppose U=L union R, with **L and R both nonempty**, every
point of L to the left of every point of R, every LLR triple a cup, and
every LRR triple a cap.

Let c=maxcup(L) and beta_U(v) be longest cup length ending at v. Then
1<=c<=n-3, and the following single global rank level is a terminal-safe
weak Delta, hence a uniform-envelope Delta:

    A={v: beta_U(v)=n-3}   if c=n-3 or c=n-4;
    A={v: beta_U(v)=n-2}   if c<=n-5.

A weak Delta here has no four-cap and meets every whole convex (n-1)-gon.
For every general-position rightmost insertion r for which U+r remains
five-cap-free, A+r is a weak Delta. No cup or n-gon restriction on the
extension is needed. The theorem covers, in particular, maximum cup
exactly n-2, while allowing shorter cups too.

## Proof

The split-polygon lemma from the n=7 proof is independent of n: a mixed
convex subset consists exactly of a cup from L and a cap from R. Also

    maxcup(U)=max(c+1,maxcup(R)),
    maxcap(U)=max(maxcap(L),maxcap(R)+1),
    beta_U(v)=max(c+1,beta_R(v))  for v in R.

The nonempty-block assumptions justify the +1 terms. Therefore c<=n-3
and R has no four-cap. R has maximum cap at most three, L has maximum cap
at most four, and both blocks have maximum cup at most n-2.

**Case c=n-3.** A three-cap in R together with a maximum cup in L would
form a mixed convex n-gon. Thus R is a cup of size at most n-2, so it has
no target. Every mixed target has n-3 cup vertices in L and two cap
vertices in R. Its last L vertex has rank n-3 in L and U. Every internal
L target has upper chain at most four, hence lower cup at least n-3;
its right endpoint likewise has rank exactly n-3. The stated level hits
every target.

**Case c=n-4.** Every R vertex has global rank n-3 or n-2. Let
Q={v in R: beta_R(v)=n-2}, the latter global level in R. Q is a cup:
if a<b<d in Q were a cap, take a longest cup ending ...p,a. If p,a,b were
a cup, appending b would give an (n-1)-cup. Otherwise p,a,b,d is a four-cap
in R, also impossible. The penultimate p exists because n-2>=3.

There is no internal L target: its upper cap and lower cup lengths give
polygon bound 4+c-2=n-2. A mixed target has exactly n-4 cup vertices in L
and three cap vertices in R. Its R cap cannot lie wholly in the cup Q,
so it contains a global rank-(n-3) vertex. An internal R target also cannot
lie wholly in Q, because Q is a cup of size at most n-2. Thus the global
rank-(n-3) level hits all targets.

**Case c<=n-5.** No internal L target exists, since its polygon bound is
c+2<=n-3. No mixed target exists either, since its size is at most
c+maxcap(R)<=n-2. An internal R target has upper chain at most three and
therefore lower cup at least n-2. Its right endpoint has beta_R=n-2 and
beta_U=n-2. The indicated level hits every target.

Finally, a single global beta level is terminal-safe by the prior rank
lemma. A cap triple a,b,d at one level extends on the left to an ambient
four-cap with last pair b,d. A four-cap in the level would then extend
such an ambient four-cap to a forbidden five-cap. Thus A is four-cap-free
and all its triple lines occur in the ambient envelope. This proves the
uniform assertion and the claimed extension at every admissible r. QED.

## The n=5 boundary

Nonempty L gives c>=1 and the first rank bound gives c<=2. If c=2, this
is the first case and selects level two. If c=1, this is the second case
and again selects level two; L is a singleton, and R's global ranks are
two or three. Its rank-three part is a cup of at most three points, so
every four-point target meets level two. The third case c<=0 is empty.
No hidden requirement n>=6 enters the proof.

The nonempty condition cannot be dropped from this rule. For example at
n=5, take L empty and U=R a four-cap. With the convention maxcup(empty)=0,
the displayed low-c rule would select global level three, which is empty
and misses U itself. The hypotheses on cap/cup/n-gon alone hold. This
example explains the role of the explicitly nonempty blocks; it is not
a counterexample to the theorem as stated.

## Controls and scope

Keep the original n=7 proof and 19/25-point controls as instances. The
new finite controls exercise c=1 and c=2 at n=5, including vacuous small
sets; and each of the three cases at n=6 and n=8. They are separate exact
checks of this written proof, not an exhaustion over configurations.
The full unseparated maximum-cup-(n-2) class is not settled.
