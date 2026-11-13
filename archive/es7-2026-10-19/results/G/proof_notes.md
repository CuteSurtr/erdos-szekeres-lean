# Hull-size split: soundness and exhaustiveness

Notation. `F = gen_cnf.py N K --hull` (unchanged encoder, `tools/trackB/gen_cnf.py`). Variables
X(i,j,k), i<j<k, are 1..C(N,3) in lexicographic order; X true = counterclockwise ("cup triple").
F contains the signotope axioms, the one-directional cap/cup flags with the K-cap, K-cup and
K-gon (cap + cup with common endpoints) prohibitions, and the hull-frame units X(1,i,j) for all
1<i<j. `hull_split.py` adds, after all clauses of F and in this order:

* D: H_v <-> AND_{2<=a<v<b<=N} X(a,v,b) for v = 3..N-1 (both directions).
* C: a sequential counter over (H_3, ..., H_{N-1}) with full equivalence
  S(i,c) <-> S(i-1,c) | (S(i-1,c-1) & H_{v_i}), S(0,c) = false, S(i,0) = true, c <= C.
* the case units: case m (m = 0..M-1): S(L,m) (if m >= 1) and -S(L,m+1); case ge:M: S(L,M).
  Here L = N-3 and M = K-3. For K = 7 the cases are m = 0,1,2,3 (hull size h = m+3 = 3,4,5,6)
  and ge:4 (h >= 7).

## 1. Each case only adds constraints to F

G_m = F & D & C & units_m contains every clause of F, so any model of G_m restricted to the
X/cap/cup variables is a model of F. (Base-clause order and ids are unchanged, so an LRAT proof
for G_m is checked against a file whose first |F| clauses are exactly F.)

## 2. The cases are exhaustive (and disjoint)

Let alpha be any total assignment to the variables of F that satisfies F. Extend it by
beta(H_v) = AND alpha(X(a,v,b)) and beta(S(i,c)) = [#{j <= i : beta(H_{v_j})} >= c]. Both D and
C are definitions of the form "new variable <-> Boolean function of earlier variables", so
alpha+beta satisfies D and C, and these values are the only ones that do. Let
m* = #{v : beta(H_v)}. Then S(L,c) is true exactly for c <= m*, so alpha+beta satisfies the
units of case m* if m* <= M-1 and of case ge:M otherwise; it violates the units of every other
case. Hence: F satisfiable  =>  some G_m (or G_ge:M) satisfiable. Contrapositive: if every case
is UNSAT, F is UNSAT. This uses nothing about geometry; it is a statement about CNFs only.

## 3. What H means: extreme points in the hull frame

Extend the signotope to all ordered triples by parity (chi(a,b,c) = sign of the sorting
permutation times X(sorted)). Call v extreme if it is not inside any triangle (a,b,c) of other
points, i.e. there is no triangle with chi(a,b,v) = chi(b,c,v) = chi(c,a,v). Claim: under the
signotope axioms and the frame units, the extreme points are exactly {1, 2, N} and the v with H_v.

* v in triangle (1,a,b) with a<b: needs chi(1,a,v) = + (so a<v), chi(b,1,v) = chi(1,v,b) = +
  (so v<b) and chi(a,b,v) = -X(a,v,b) = +. So v is in some triangle through 1 iff
  X(a,v,b) is false for some 2 <= a < v < b <= N, i.e. iff not H_v.
* v in triangle (p,q,r) with 2 <= p<q<r: write s = chi(p,q,r).
  - v < p: the quadruple (v,p,q,r) has sign sequence (s, -s, s, s): two sign changes,
    impossible. v > r: (p,q,r,v) gives (s, s, -s, s), impossible.
  - p < v < q: requires chi(p,v,q) = -s and chi(p,v,r) = s, so X(p,v,q) and X(p,v,r) differ:
    one of them is false, so not H_v. q < v < r: chi(p,v,r) = s and chi(q,v,r) = -s, so
    X(p,v,r) or X(q,v,r) is false: not H_v.
  So if H_v then v is in no triangle; with the first bullet, H_v <=> v extreme, for 3 <= v <= N-1.
* 1 is extreme: in any triangle (a,b,c) with 2 <= a<b<c, chi(a,b,1) = +, chi(c,a,1) = -X(1,a,c) = -.
  2 and N are extreme: 2 < every other non-1 point, so only triangles (1,b,c) could contain it, and
  those need b < 2; symmetrically for N; triangles without 1 are excluded by the v<p / v>r cases.

So in any model, h := 3 + #{v : H_v} is the number of extreme points (the hull size), and the
case m is exactly "hull size m+3". This is checked independently by `verify_sig.c`, which
recomputes extreme points from triangles on every model and control.

## 4. Every configuration has a hull-frame labelling (what the split is a split of)

* Realizable point sets in general position: choose an extreme point p, apply the projective map
  documented in gen_cnf.py (order type preserved), label p as 1 and the others by angle. The
  chirotope is unchanged, so the extreme points (and the hull size) are unchanged.
* Abstract signotopes (uniform acyclic rank-3 chirotopes): take an extreme element p and order the
  rest by chi(p,.,.) (a total order because p is extreme). The 3-term Grassmann-Plucker relations
  with p as a common element give, for i<j<k<l in that order, exactly the four forbidden patterns
  of the signotope axiom: GP on (i | p, j,k,l), (l | p, i,j,k), (j | p, i,k,l), (k | p, i,j,l)
  exclude the patterns +-+ / -+- on positions {1,2,3}, {2,3,4}, {1,2,4}, {1,3,4}. Quadruples
  through p have sequence (+,+,+,*), always fine. So the relabelled chirotope is a signotope
  satisfying the frame units. (This step, and the identification of "K points in convex
  position" with "cap + cup with common endpoints" that gen_cnf.py uses, are the standard facts
  the --hull encoding already relies on; neither is machine-verified here.)
* h >= K is impossible: the K-1 lower-chain vertices 2 = c_1 < ... < c_{K-1} together with point 1
  form a K-cup (consecutive lower-hull triples are counterclockwise, and every (1,a,b) is), which F
  forbids. The case ge:M is nevertheless solved (and LRAT-checked) rather than assumed.

Consequence: "every case G_m UNSAT" gives "F UNSAT", and "G_m UNSAT" alone means: no signotope in
the hull-frame normal form of F has N points, no K-gon in the cap/cup sense, and hull size m+3.
It is a statement about encoding X = (gen_cnf.py --hull + hull_split.py), not a theorem: the
encoding is not verified (critique item 4), and LRAT certifies only the CNF.

## 5. Cup/cap convention (critique item 11)

X(1,i,j) = true is a cup triple (p_i below line p_1 p_j). In the frame, point 1 prepends to every
cup, so P' = {2..N} has no (K-1)-cup and no K-cap, and the hull vertices other than 1 form a cup
(the lower chain). Bounds are computed in code from (a, u) with f(a,u) = C(a+u-4, a-2) for "no
a-cap and no u-cup" (`lemma_cnf.py`): for K = 7, N = 33 (32 points in P'):
  - points ending no 4-cup: no 4-cup and no 7-cap, at most f(7,4) = C(7,2) = 21, so at least 11
    end a 4-cup (not 16 as in the plan);
  - points ending no 4-cap: no 4-cap and no 6-cup, at most f(4,6) = C(6,2) = 15, so at least 17
    end a 4-cap (matches the plan);
  - 3-cups: at least 32 - f(7,3) = 26; 3-caps: at least 32 - f(3,6) = 27.
