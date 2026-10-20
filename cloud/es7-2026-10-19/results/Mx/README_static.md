## Encoding (scripts/mxgen.py, written without reading gen_etv.py, mirgen.py or mirlib.py)

Points 0..n−1 are sorted by x. chi(i,j,k) for i<j<k is true iff the triple is counter-clockwise,
i.e. j lies below the chord ik (a "cup triple"). The axis is vertical, so the mirror sends point
i to point m−i with m = n−1; for n = 33 the axis point is a = 16.

**Mirror sign rule.** The task statement gives chi(m−k, m−j, m−i) = −chi(i,j,k). That is
wrong for an x-sorted signotope: the correct rule is **chi(m−k, m−j, m−i) = +chi(i,j,k)**.
The reflection reverses orientation, giving one minus sign:
orient(σi, σj, σk) = −orient(i,j,k). It also reverses the x-order, so re-sorting
(m−i, m−j, m−k) into (m−k, m−j, m−i) is an odd permutation and gives a second minus sign.
The two cancel. Geometrically, a reflected cup is still a cup. With the minus rule, the 16
self-mirror triples (i, a, m−i) would be forced to be zero, so every CNF would be trivially
UNSAT. The + rule was checked on every triple of all 10,000 validation sets (0 violations).
It agrees with the rule stated in results/C/README.md.

**Variables.** There is one variable per mirror orbit of triples: 2,736 orientation variables
for n = 33 (16 orbits of size 1 and 2,720 of size 2). This substitution is sound because it
is equivalent to adding the equality clauses.

**Signotope axioms.** For each a<b<c<d, the sign sequence (abc, abd, acd, bcd) may change sign
at most once. This is encoded by forbidding +−+ and −+− on every 3 of the 4 positions (8
clauses per 4-set; after deduplication across orbits, 163,440 remain for n = 33).

**No convex k-gon: the "anchored chain" encoding.** gen_etv.py has no-cap and no-cup
counters; this encoding is built differently. Take a convex k-gon with leftmost vertex p and
rightmost vertex q. Its lower chain is a cup p…q with s vertices, and its upper chain is a
cap p…q with t vertices, where s + t = k + 2 and s, t ≥ 2. The auxiliary variables are:

- U[p,j,q,ℓ]: "some cup of exactly ℓ vertices starts at p and ends with the pair j,q". It is
  defined one-directionally: chi(p,j,q) → U[p,j,q,3], and U[p,i,j,ℓ] ∧ chi(i,j,q) →
  U[p,j,q,ℓ+1].
- EU[p,q,ℓ]: the OR over j of U[p,j,q,ℓ], also one-directional.
- C and EC: the same for caps, with ¬chi in place of chi.

The forbidding clauses are ¬EU[p,q,s] ∨ ¬EC[p,q,t] for s + t = k + 2 with s, t ≥ 3, plus
¬U[p,j,q,k] and ¬C[p,j,q,k] (a k-cup or k-cap is itself a k-gon). Every auxiliary clause is
Horn with exactly one positive auxiliary literal. So for fixed orientations, the least model
is reached by forward chaining. The CNF is satisfiable iff that least model satisfies the
purely negative gon clauses.

*Soundness for point sets.* Take any real k-gon-free set and set every auxiliary variable to
"the chain exists". Every definition clause then holds. A violated gon clause would give a cup
p…q and a cap p…q with s + t − 2 = k vertices in total. The cup's inner points lie below the
line pq and the cap's lie above it, so together they form a convex k-gon, a contradiction.
Hence UNSAT implies that no such point set exists.

*Completeness.* A convex k-gon decomposes into a cup and a cap with the same endpoints, and
the propagation forces the corresponding variables to true. Both directions were tested
against an exhaustive brute force (see Validation).

**Case split and symmetry breaking (my own choice; soundness argument).**

- *Distinct x.* The projective map used in results/C is not needed. General position and "no
  convex 7-gon" depend only on the strict orientation signs, and those signs survive small
  perturbations. A mirror-symmetric perturbation (x, y) → (x + ε_P, y) applied to each pair,
  with ±ε on the two partners, therefore makes all x distinct while keeping the symmetry and
  every sign. The axis point stays at x = 0 and is the median point a = (n−1)/2.
- *y-reflection.* The map (x,y) ↦ (x,−y) keeps the mirror, the x-order, general position and
  convex position. It negates every chi and swaps cups with caps. Each CNF below, before its
  symmetry-breaking literal, is invariant under "negate all orientation variables, swap U↔C
  and EU↔EC".
- **Sub-case "top"** (the analogue of (i)): the axis point is a vertex of the upper hull. With
  a strictly between the leftmost and rightmost points, this holds iff a lies above every
  chord ik with i < a < k, which is the 136 unit clauses ¬chi(i,a,k) after orbit
  substitution. "Lower-hull vertex" is the y-reflection of "upper-hull vertex", so the
  y-reflection is spent here.
- **Sub-case "interior"** (the analogue of (ii)): the axis point is on neither hull. This is
  two clauses: OR chi(i,a,k) and OR ¬chi(i,a,k) over i < a < k. The interior class is closed
  under y-reflection, so one unit chi(0,1,2) = true is added without loss of generality.
- *Coverage.* In general position the axis point is an upper-hull vertex, a lower-hull vertex
  or interior. It cannot be both an upper and a lower vertex, because chord (a−1, a+1) has it
  on one side. So top ∪ y-flip(bottom) ∪ interior covers every 33-point mirror-symmetric set
  in general position.
- No other symmetry breaking is used. The x-reflection is the mirror itself.

Sizes for n = 33, k = 7 (all with 2,736 orientation variables):

| CNF | vars | clauses | sig | aux | gon | case/sym |
|---|---|---|---|---|---|---|
| top33 | 51,590 | 492,920 | 163,440 | 320,354 | 8,990 | 136 |
| int33 | 51,590 | 492,787 | 163,440 | 320,354 | 8,990 | 2 + 1 |
