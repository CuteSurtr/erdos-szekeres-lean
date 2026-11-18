# The cup/complement lemma is false for every n>=6

**PROVED by the explicit construction below.** This is a written real-point
proof, not a Lean proof or SAT certificate. It refutes only the proposed
cup/complement sufficient condition. In fact every member of the family
has a two-point terminal-safe weak Delta. Numerical controls are separate.

## 1. An integer family

Put k=n-2>=4 and q=100k. Define three blocks, in this x-order:

```
A_i = (4qi,          qi + 4i^2)       (0<=i<=k-2),
B_j = (4q^2 + 4qj,   4q^2 + 4j^2)    (0<=j<=2),
D_i = (8q^2 + 4qi,  -qi + 4i^2)       (0<=i<=k-2).
```

Let U=A union B union D. It has 2k+1=2n-3 points. Each block is a cup.
For the slope estimates, divide both coordinates by 4q^2. The blocks are

```
A(t)=(t, t/4+t^2), B(t)=(1+t, 1+t^2), D(t)=(2+t, -t/4+t^2),
```

where every parameter belongs to [0,1/100). Slopes within A, B, D belong
respectively to (1/4,27/100), (0,2/100), (-1/4,-23/100); these open bounds
apply to distinct parameters. Slopes between the blocks obey

```
9/10 < slope(A,B) < 11/10,
-11/10 < slope(B,D) < -9/10,
-1/100 < slope(A,D) <= 0.
```

For example, A-heights lie in [0,26/10000), B-heights in [1,10001/10000),
and D-heights in (-1/400,0]. The AB and BD horizontal separations lie in
(99/100,101/100), and the AD separations in (199/100,201/100). These bounds
give the displayed cross-slope bounds directly. Consequently all triples
are noncollinear and their signs are exactly the following table. A plus
means cup and a minus means cap; repeated letters denote ordered distinct
points from that block.

| Pattern | AAA | BBB | DDD | AAB | ABB | AAD | ADD | BBD | BDD | ABD |
|---|---|---|---|---|---|---|---|---|---|---|
| Sign | + | + | + | + | - | - | - | - | + | - |

The table, together with block sizes, is all the remaining proof uses.

## 2. Maximum cups: exactly six

A cup with at least three vertices cannot meet both A and D: any third
vertex produces one of AAD, ADD, ABD, all negative. If a cup meets A and B,
it contains at most one B vertex (ABB is negative). Likewise a cup meeting
B and D contains at most one B vertex (BBD is negative).

Since |A|=|D|=k-1 and |B|=3<k, the maximum cup length is exactly k. Its
six maximum cups are precisely

```
A union {B_j},  {B_j} union D     (j=0,1,2).
```

The complement of A union {B_j} is (B minus {B_j}) union D. If the two
remaining B points are b<b', its lower chain is b followed by every D
point; its upper chain is b,b',last(D). The BDD and BBD signs verify these
chains. Thus all k+1 points are vertices, with upper/lower sizes (3,k).
Similarly A union (B minus {B_j}) is convex, with lower chain every A
point followed by b', and upper chain first(A),b,b'. Every maximum cup
therefore has a convex (k+1)-point complement.

## 3. No five-cap

A cap uses at most two vertices from each block, because each block is a
cup. If it meets all three blocks, AAB excludes two A vertices and BDD
excludes two D vertices, so its size is at most 1+2+1=4. If it uses at most
two blocks its size is at most 2+2=4. Thus U has no five-cap. Two A and two
D points do form a four-cap; this hypothesis is attained, not vacuous.

## 4. No convex (k+2)-gon; classification of the targets

Here are the strict-interior consequences of the sign table. For a cup
x<y<z and a point w to its right with every pair from the cup followed by
w a cap, y lies strictly inside triangle x,z,w. The left-hand version is
the same assertion with the outside point before the cup. In either case
the three edge determinants of the containing triangle have its orientation.

In particular a convex subset meeting both A and D can contain at most
two A and two D vertices if it avoids B. If it also meets B, the quadruple
a<a'<b<d has a' strictly inside triangle a,b,d, and the quadruple
a<b<d<d' has d strictly inside triangle a,b,d'. Hence such a convex subset
contains at most one A and one D vertex.

Any convex subset meeting B and another block contains at most two B
vertices: for b<b'<b'', the point b' is strictly inside triangle a,b,b''
if a is in A, or inside triangle b,b'',d if d is in D. Thus convex subsets
meeting both A and D have size at most four, whether or not they meet B.

A convex subset supported on A union B has at most (k-1)+2=k+1 vertices;
the same holds for B union D. A subset in one block has at most k-1 or
three vertices. There is therefore no convex (k+2)=n-gon. Moreover, since
k+1>=5, the only convex (k+1)=(n-1)-gons are precisely

```
A union {B_i,B_j},  {B_i,B_j} union D     (0<=i<j<=2).
```

This proves all premises and the failure of the requested conclusion for
every n>=6, without relying on any solver or finite audit.

## 5. Why cup exchange fails, while Delta selection succeeds

The graph of maximum cups joined by one-point exchanges is two disjoint
triangles: one consists of A union {B_j}, and the other of {B_j} union D.
Across the two families, intersections have size at most one, whereas a
one-point exchange requires k-1>=3 common vertices. Every vertex of this
exchange graph has a convex complement. Even restricting all complementary
polygons to upper-chain size three does not repair the proposed lemma.

Any two B points meet every target in Section 4, since two two-subsets of
a three-set intersect. The chosen pair has no cap triple and is therefore
terminal-safe. It is a weak Delta of size two. No singleton works: an A
point misses every target supported on B union D, a D point misses those
supported on A union B, and a B point misses targets using the other two
B points. Thus the minimum weak-Delta size is exactly two.

For any additional point r, this pair together with r still has at most
three points and hence no four-cap. It meets every old target by the pair
and every new target by r. This family therefore gives rooted Deltas even
with an arbitrary root position. It is not a Delta counterexample.

## 6. Stronger localization for a prescribed root

**Lemma (cup plus root).** Let |S|=m>=n and let r be any prescribed point.
If S contains a cup C of size at least m-n+1, it has a rooted weak Delta.
If r is outside C use C union {r}. If r belongs to C and |C|>=m-n+2 use C.
In the remaining case, |C|=m-n+1 and r belongs to C; add any point outside
C, which exists since n>=6.

**Proof.** A cup with at most one extra point has no four-cap, because any
four-set contains three cup vertices. The selected set contains r and has
at least m-n+2 vertices, so its complement has at most n-2 vertices and
cannot contain a target of size n-1. QED.

At m=2n-2, the existence of an (n-1)-cup anywhere in S therefore suffices
for any prescribed root. A rooted counterexample at this boundary must
exclude (n-1)-cups in the full S, not only in U=S minus {r}. This elementary
strengthening was pointed out by the parent; no finite SAT claim is made
here. The refutation in Sections 1–5 concerns U and needs no extension r.

## 7. Conditional one-point augmentation

Put |U|=2n-3 and let C be an (n-2)-cup. For each q in U minus C, the set
C union {q} is an old weak Delta: it has no four-cap by the same three-cup-
vertices argument, and its complement has n-2 points.

For a prescribed root r outside U, C union {q,r} is cap-free if and only
if no pair a,b in C forms a four-cap with q,r. Indeed any four-cap would
have to contain both extra points, since three C vertices form a cup.
This is an exact obstruction characterization, not an existence theorem
for q. Cardinality then makes every cap-free such choice a rooted Delta.

For rightmost r there is also a sufficient condition independent of r:
require every cap triple in C union {q} to end in a pair of ambient cap
rank at least four in U. Such triples necessarily use q and two C points.
If S remains five-cap-free, a new four-cap ending at r would extend the
ambient four-cap on its last old pair to a five-cap. Thus this condition
makes C union {q} terminal-safe and its extension rooted-safe. Existence
of q under general boundary premises remains unresolved by this argument.

## 8. Exact scope of the parent's conditional finite reduction

Fix n>=6. Suppose a separate argument proves that every U satisfying

```
|U|=2n-3; no five-cap; no convex n-gon; maximum cup length n-2;
every (n-2)-cup has a convex complement
```

has a terminal-safe weak Delta. Then **every** no-five-cap, no-convex-n-gon
U with |U|<=2n-3 has a terminal-safe weak Delta. Here is the full reduction,
including smaller sizes.

* If U has no (n-2)-cup, the right endpoints of its target polygons all
  have cup-ending rank n-3. That one rank level is terminal-safe by the
  prior proved rank lemma, and the endpoints hit all targets. If there
  are no targets the empty set works.
* If |U|<=2n-4 and U has an (n-2)-cup, select such a cup. Its complement
  has at most n-2 points, so the cup is a terminal-safe weak Delta.
* At |U|=2n-3, an (n-1)-cup likewise leaves at most n-2 points.
* In the remaining case the maximum cup length is n-2. If some such cup
  has nonconvex complement, it is a terminal-safe weak Delta: its only
  possible disjoint target is its whole (n-1)-point complement.
* Otherwise U satisfies precisely the displayed boundary premises.

For any rightmost r such that S=U union {r} is still five-cap-free, add r
to the selected terminal-safe Delta. A new four-cap a,b,c,r would append
r to an ambient four-cap ending b,c, contradicting five-cap-freeness.
All new targets contain r. The no-n-gon premise is needed only for U in
this reduction, not for S; |S|<=2n-2.

This is a **PROVED conditional reduction** using the prior written rank
lemma. It neither checks the parent's terminal-safe CNF nor asserts any
SAT/UNSAT outcome. A successful finite result for n=6,7,8 would concern
only those n, not all n>=6. The family in Sections 1–5 shows the boundary
class is nonempty for every n and so cannot be discharged by disproving
its geometric premises.
