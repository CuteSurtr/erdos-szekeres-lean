# A bounded human result for a = 4

13 November 2026. **PROVED** below means a written argument, not a Lean proof.
The unrestricted strong and cup-side statements for arbitrary n remain **OPEN**.
No implication from Baek's numerical theorem to the stronger decomposition is used.

## 1. Main result: an extreme point meeting all target-sized cups

**Theorem (PROVED).** Fix k >= 3. Let S be a finite real point set in general
position, with distinct x-coordinates and no 4-cap. Let r be its rightmost point,
and suppose U = S minus {r} contains no k-cup. Define

    E = {right endpoints of convex k-gons contained in U},
    Delta = E union {r}.

Then Delta is a cup, |Delta| <= k-1, and Delta meets the lower cup chain,
including endpoints, of every convex k-gon of S.

Thus, with k = n-1, the **strong cup-side version of D(4,n)** holds whenever the
rightmost point belongs to every (n-1)-cup. The reflected statement holds for
the leftmost point. The condition is vacuous if there are no (n-1)-cups.
The theorem itself does not even need the additional assumption that S has no
convex n-gon.

This is a restricted theorem for every n >= 4, not a proof of the unrestricted
conjecture. In particular it supplies no result for D(5,7) or D(5,8).

### 1.1 The two extension facts

All chains are listed in increasing x-order. In a 4-cap-free set:

* If (p,q,z) is a 3-cap, every cup ending at p extends to the right by q.
  Indeed, if a is the penultimate point of such a cup and (a,p,q) were a cap,
  then (a,p,q,z) would be a 4-cap. A one-point cup extends trivially.
* If (a,b,p) is a 3-cap, every cup starting at p extends to the left by b.
  Otherwise its next point q would make (a,b,p,q) a 4-cap. Again the
  one-point case is immediate.

Consecutive cup turns suffice for a geometric cup, and consecutive cap turns
suffice for a geometric cap: their successive slopes are respectively strictly
increasing and strictly decreasing. Thus both concatenations above are valid
chains, not just assertions about one triple.

These are the a=4 specializations of DELTA2N20261113, Section 6, Lemma 1.

### 1.2 A smaller transversal when the longest cups are absent

**Terminal polygon lemma (PROVED).** Suppose U has no 4-cap and no k-cup,
k >= 3. The set E of right endpoints of its convex k-gons is a cup of at most
k-2 points. It meets every such polygon on its lower chain.

**Proof.** A convex k-gon has an upper cap of c points and a lower cup of d
points, with c+d-2=k. Here c <= 3. The case c=2 would give a k-cup, so necessarily
c=3 and d=k-1. Consequently every e in E ends both a 3-cap and a (k-1)-cup
contained in U.

If e1 < e2 < e3 in E formed a cap, the first extension fact would extend a
(k-1)-cup ending at e1 by e2. This is a k-cup entirely in U, a contradiction.
Thus E contains no 3-cap and is a cup.

If |E| >= k-1, take its first k-1 points as a cup C, starting at e. Some 3-cap
(a,b,e) ends at e inside U. The second extension fact makes bC a k-cup in U,
again a contradiction. Therefore |E| <= k-2. Each polygon's right endpoint is
on its lower chain and in E. This proves the lemma. QED.

The additional saving of one point is useful: for n=k+1, this gives a lower-chain
transversal of size at most n-3 when S itself has no (n-1)-cup.

### 1.3 Proof of the main theorem

The terminal polygon lemma gives |E| <= k-2. To show E union {r} is a cup,
suppose x < y < z in that union formed a cap. Since r is rightmost, both x and y
belong to E and hence U. A (k-1)-cup in U ends at x. The first extension fact,
applied in S to the cap (x,y,z), appends y to that cup. Every point of the
resulting k-cup belongs to U, which is forbidden. Thus Delta is a cup and
|Delta| <= k-1.

Let H be any convex k-gon in S. If r is in H, then r is the right endpoint of H
and belongs to its lower chain. If r is not in H, then H is contained in U and
its right endpoint belongs to E. In either case Delta meets the lower chain.
Finally, a cup with at most k-1 points has no 3-cap and no convex k-gon. These
are exactly the two restrictions required of a strong Delta for a=4. QED.

The leftmost version follows by reflecting the horizontal coordinate. That
reflection reverses the order but preserves cups, caps, and lower chains.

### 1.4 Explicit scope and an obstruction to an unrestricted proof

A counterexample to the strong cup-side statement for a=4 must retain an
(n-1)-cup after deleting its rightmost point, and must also retain one after
deleting its leftmost point. These two cups need not be distinct.

The proof uses the absent-cup hypothesis at a precise step: a cap among proposed
transversal vertices produces a k-cup in U. When U already has such cups, this
is not a contradiction. It also uses it to ensure every k-gon in U has a 3-cap
upper chain; pure k-cups would not supply the incoming 3-cap used in the
cardinality bound. Neither use can simply be omitted.

This result is compatible with the failed online rules: recognizing that r
belongs to every k-cup requires knowledge of the whole set. E is likewise
defined using all polygons of U. It is not a pointwise rule in ranks.

In fact, in this special class Delta is contained in Q_S, the set of points
starting no 3-cap in S. For e in E, a cap (e,x,z) in S would have x in U, since
r is rightmost; extending the (k-1)-cup ending at e by x would give a k-cup in
U. Also r starts no 3-cap. This conditional Q_S localization is consistent
with the failures of unconditional Q and Q union Q' rules: those failures
cannot satisfy the rightmost-point hypothesis used here.

## 2. A localization for the general case

Here S has no 4-cap and no convex n-gon, and k=n-1 >= 3. Label an edge xy by

    s(xy) = 2 if (x,y,z) is a cap for some z>y, and 1 otherwise.

Every cap (x,y,z) has s(xy)=2 and s(yz)=1: label 2 on yz would extend it to a
4-cap. An edge of label 1 prepends its first endpoint to every cup starting at
its second endpoint. An edge of label 2 appends its second endpoint to every
cup ending at its first endpoint. Both assertions follow from the extension
facts, or directly from the label definition.

More generally, call ANY assignment of labels in {1,2} valid if every cap
triple has successive labels (2,1). The same prepend/append rules hold for
every valid assignment: a triple starting with a label-1 edge, or ending with
a label-2 edge, cannot be a cap. The reflected-label argument below uses this
larger class, not just the canonical "exists a future cap" assignment.

Let beta(v) be the maximum length of a cup ending at v, and alpha(v) the maximum
length of such a cup whose last edge has label 1, with alpha(v)=1 if no such
edge exists. Put R={v: beta(v)=k}.

**Boundary localization (PROVED).** R is a cup, has at most k-1 points, and hits
every k-cup. If a target lower chain C=(c1,...,cL) misses R, then

    L=k-1, beta(cL)=k-1, alpha(c1)=1,
    and alpha(ci) <= i for 1 <= i <= L.

**Proof of the chain statements.** A k-cup ends in R. Since target polygons
have upper cap length 2 or 3, a missed target lower chain must have length
k-1. Its endpoint has beta at least k-1, at most k, and is not in R; hence its
beta is k-1. If alpha(ci) >= i+1, a cup ending at ci with a last edge of label 1
can be concatenated with the suffix (ci,...,cL). This makes a cup of length at
least (i+1)+(L-i+1)-1 = k ending at cL, forcing cL into R. This proves all the
alpha inequalities, including alpha(c1)=1.

**Proof that R is a cup.** A cap (p,q,z) with p in R would extend a k-cup
ending at p by q to an n-cup, impossible. In particular no 3-cap lies in R.

For completeness, the size bound follows from the following local form of
Baek's shared-endpoint argument; no numerical theorem is invoked.

**Shared-endpoint fact (PROVED).** Two k-cups meeting with the end of one equal
to the start of the other force a 4-cap, a (k+1)-cup, or a convex (k+1)-gon.
To prove this in a 4-cap-free set, write the cups as Pz and zQ, with a the last
point of P and b the first point of Q. Fix ANY valid two-label assignment; the
canonical one proves that such an assignment exists. We can assume s(ab)=1:
otherwise reflect the horizontal coordinate, reverse the order, and assign
the reversed edge yx the label 3-s(xy). A cap with old labels (2,1) has reversed
labels (3-1,3-2)=(2,1), so this assignment is valid. It need not be the canonical
assignment of the reflected set. The two cups exchange roles, and their new
connecting edge has label 1. Both prepend/append rules still hold by the
validity condition alone. The edge ab then prepends a to Q, giving a k-cup aQ.
Let c be the last point of Q. If (a,z,c) is a cup, Pzc is a (k+1)-cup. If it is a cap, that cap
and aQ form a convex (k+1)-gon: they have the same endpoints a,c, and z is above
their chord whereas the internal points of aQ are below it.

If R had k points, its first k points would form a k-cup starting at a point
that also ends a k-cup. The shared-endpoint fact contradicts the hypotheses.
Thus |R| <= k-1. QED.

The remaining task is to repair R to hit the missed (k-1)-cups without losing
the cup condition or the size bound. The boundary description localizes those
misses; it does not perform that repair. Taking the entire alpha=1 boundary
together with R is not justified.

## 3. A trimming argument that fails even on seven real points

The assertion "an existing cup-side transversal of size n-1 can always be
shrunk by deleting one of its points" is false. This is not a counterexample
to the existence of another, smaller transversal.

Use the following points, indexed in increasing x-order:

    0=(-500,-530), 1=(10,0), 2=(20,10), 3=(30,40),
    4=(40,90), 5=(100,162), 6=(110,405).

Their negative triples are exactly

    012, 135, 145, 235, 245, 345, 346.

All remaining triples are positive, and none is collinear. These signs imply
that there is no 4-cap. Direct exact checks of all subsets also give no convex
5-gon. The cup C={1,2,3,4} meets the lower chain of every convex quadrilateral.
Indeed a lower chain missing C would have to be {0,5,6}; its upper vertex i
would require (0,i,6) to be a cap, whereas all four of these triples are cups.

For each i in C, {0,i,5,6} is a 4-cup meeting C only at i. Thus deleting any
point of C destroys its transversal property. This is an explicit obstruction
to trimming a previously chosen transversal, not to exchanging its vertices.
For comparison, {0,1,3} is a smaller cup-side transversal, verified by the
independent exhaustive check. Inclusion-minimal and minimum-cardinality are
distinct requirements in this example.

Labels for this example: the sign evaluation and finite configuration checks
are **COMPUTED** with exact integers; the private-cup and lower-chain arguments
above are written proofs conditional only on those displayed signs. No UNSAT
certification is claimed.

## 4. Local sources and verification

Read before deriving these statements:

* `../../DELTA2N20261113/README.md`, especially Sections 4.2b, 6, and 7;
* `../../DELTA2N20261113/VERIFY_D1.md`, including its warning about the written
  signotope-to-convexity converse;
* `../../ETVTHY20261113/README.md`, Sections 1, 2, 3, and 5;
* the existing local text `/home/jay/research/data/session-scratch-20261113/baek/baek.txt`,
  Sections 3-5. Baek's row deletion removes long cups; it is not assumed to
  hit all target polygons.

The proofs above are stated for real point sets, so they do not rely on the
unproved arbitrary-size signotope converse noted by VERIFY_D1. No literature
search or network request was made.

### 4.1 Independent bounded controls (COMPUTED)

`check_theory.py` is a fresh standard-library checker; it imports no old
research code and calls no solver. It enumerates subsets directly. For real
points it computes exact integer determinants and a monotone-chain hull, then
cross-checks hull convexity against the independent four-subset sign test.
The theorem's Delta is built from the actual enumerated polygons, without
using a formula that presupposes the theorem.

Inputs are the 662 recorded (4,5)-valid signotopes on 5, 6, and 7 points; ten
old real a=4 counterexample fixtures; the new seven-point example; a convex
pentagon checking that the main theorem does not require n-gon-freeness; and
five explicit nonvacuous examples with k=3,...,7. Each input is also reflected.
The last family is

    {(2i, (2i)^2): 0 <= i <= k-1} union {(1, 2k-3)}.

Here deleting the rightmost point leaves a convex k-gon whose upper chain has
three points; the full set has no convex (k+1)-gon and does have a k-cup.
These facts are checked from coordinates, not assumed by the script.

Final run: **PASS**, 0.157743 seconds of script wall time; one Python thread,
256 MiB address-space cap, external 20-second timeout. The script also stops
before starting another input if its elapsed time exceeds 17 seconds.

| control | instances checked |
|---|---:|
| input configurations, counting reflected inputs separately | 1,358 |
| terminal polygon lemma | 528 |
| extreme-point theorem, including its conditional Q_S localization | 456 |
| those extreme-point instances with a k-cup present | 384 |
| boundary localization under its additional no-(k+1)-gon hypothesis | 1,356 |
| missed target lower chains localized, counting polygon multiplicity | 5,572 |

All 16,914 target polygon occurrences were enumerated with their lower chains. The
seven-point example has 17 convex quadrilaterals, no convex pentagon, and no
4-cap. Its four private 4-cups prevent every one-point deletion from C; the
alternative {0,1,3} passes the same lower-chain check. These are bounded
**COMPUTED** controls, not proofs of the unrestricted conjecture or claims of
UNSAT certification. Reflections and repeated chain occurrences are not
claimed to be distinct configurations or chains.

The recorded source-file hashes, detailed counts, coordinates, and witnesses
are in `controls.json`. `SHA256SUMS` hashes the final note, checker, and result.
Reproduce from the repository root (no output file is written unless the
caller redirects stdout):

```bash
ulimit -v 262144
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
timeout 20s /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python \
  cloud/es7-2026-10-19/results/DELTA3N20261113/a4/check_theory.py
```

All work stayed in `DELTA3N20261113/a4/` and the assigned `a4/` scratch
directory. No old record, main README, or math.md was edited. No commit, push,
branch change, email, long computation, or systemd unit was performed. No
heavy follow-up command is proposed or waiting for scheduling.
