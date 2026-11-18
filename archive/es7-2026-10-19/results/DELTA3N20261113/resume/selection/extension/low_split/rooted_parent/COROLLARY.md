# A size-free structured consequence of the rooted lemma

**PROVED, written composition.** Fix n>=5. Let U=L disjoint-union R be
a finite real x-separated general-position set, both blocks nonempty,
with no five-cap and no convex n-gon. Write l for the rightmost point
of L. Suppose L minus {l} contains no(n-1)-cup.

1. If the cut is low (every LLR triple a cap, every LRR triple a cup)
   and the longest R cup has length at most n-4, then U has a
   terminal-safe weak Delta.
2. If every crossing triple is a cap and R is a singleton, then U has
   a terminal-safe weak Delta.

For either cut, an L four-cap together with any R point would be a
five-cap, so L has no four-cap. The
[rooted lemma](../consequences/ROOTED_LEMMA.md) therefore gives Option1
of T_n(L): a cup B hitting every internal(n-1)-gon, with every nonfirst
selected point ending an L three-cap.

For (1), apply the independently reviewed arbitrary-right-block
[low-split transfer](../../structure2/low_split.md). Its hypotheses are
exactly Option1, the stated low-cut signs, ambient exclusions and
maxcup(R)<=n-4. Explicitly, take B together with the top cup-ending-rank
level in R; that transfer supplies the internal and mixed target coverage
and terminal witnesses. No finite-cardinality certificate is used here.

For (2), write R={r} and take B union {r}. The independent
[all-cap argument](../../fourcuts14_audit/VERIFY_FOURCUTS14.md) applies:
the cup B hits internal targets and r hits every crossing target. Every
selected cap a<b<r has b nonfirst in B. An L cap u<v<b gives the ambient
four-cap u<v<b<r with its exact terminal pair. A selected four-cap is
impossible because B is a cup.

These conclusions have no separate bound on |L|, |R| or |U|. Their
geometric cup-length hypothesis is substantive; removing it would require
the unresolved general T_n argument or additional finite evidence. In
particular, this does not assert universal T8 or the general Delta
conjecture. This is a written deduction, not a new Lean theorem or SAT
certificate, and no novelty claim is made.
