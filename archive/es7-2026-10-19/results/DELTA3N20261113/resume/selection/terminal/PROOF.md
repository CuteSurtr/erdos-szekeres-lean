# The exact obstruction and the surviving envelope witness

The coordinate predicates and finite counts below were computed exactly
and independently checked by the parent. The terminal-selection CNF has
a fresh parent cake_lpr certificate. The deductions from those predicates
are written proofs; none is Lean-checked.

## 1. Frozen coordinates and terminal obstruction

The points are listed in strictly increasing x order:

```
 0=(-877024,-728732)   1=(-848175,-806081)
 2=(-315477, 411721)   3=(-313031, 607898)
 4=(-312174, 772879)   5=(-275463,-257726)
 6=(-247748,-312490)   7=(-229906,-280298)
 8=(-224691,  37110)   9=(-219347,-771737)
10=(-147229,-623666)  11=( -42059,  77725)
12=(   3816,-817775)  13=(  75450,-921685)
14=( 153870, 234592)  15=( 182298, 276392)
16=( 458162, 265990)  17=( 758070, 903438)
```

Exact checks give no collinear triple, no five-cap and no heptagon. There
are 402 hexagons and 219 cap triples whose terminal pair has ambient rank
three. Any terminal-safe weak Delta would satisfy the negative clauses
for all these triples and the positive clauses for every hexagon. The
108-clause retained subformula is CERTIFIED UNSAT, and every row is one
of these actual clauses. Therefore no such Delta exists for this U.

This does not rule out ordinary weak Deltas: A={0,5,6,7,8} contains no
four-cap and meets every one of the 402 hexagons. Its only cap triples
are (0,5,6) and (0,5,7), both with ambient terminal rank three.

## 2. Explicit all-X envelope witness (PROVED from exact checks)

The ambient quadruple C=(6,7,14,17) is a four-cap. Let L be the line
through points 14 and 17, and let L56 and L57 be the lines through the
terminal pairs of the two cap triples in A. Exact rational subtraction
gives, writing T=X-758070,

    L(X)-L56(X) = 88782061472/27715
                   + (5162547569/1674540300) T,

    L(X)-L57(X) = 76228055224/45557
                   + (22054309811/13762769700) T.

All four coefficients are strictly positive. Thus for every X>=758070,

    F3(A;X) = max(L56(X),L57(X)) < L(X) <= F4(U;X).

The last inequality holds because C is an ambient four-cap whose terminal
line is L. This proof does not depend on the envelope-building algorithm.
It is checked directly in `data/all_X_direct_proof.json` and separately
by the parent.

## 3. Consequence for rightmost insertion (PROVED)

Let r=(X,Y) be rightmost, with U+r in general position and still five-cap-free.
Every ambient four-cap terminal line must lie strictly below r, so
Y>F4(U;X). Section 2 gives Y>F3(A;X), preventing a four-cap formed by
adjoining r to a cap triple in A. No old four-cap lies in A. Hence A+r
is four-cap-free. Every old hexagon is hit by A and every new hexagon
contains r. Therefore A+r is a weak Delta.

This applies to every such r, with or without the no-heptagon condition.
In particular, this terminal-selection obstruction cannot produce a
counterexample to selecting the newly inserted rightmost point.

## 4. Relation between the two criteria

Ambient terminal rank four implies line-envelope domination, but the
converse fails on this explicit real fixture: every weak Delta violates
the rank condition, while 4,057 weak Deltas pass the weaker envelope
condition for all rightward X. The latter count is a finite computation;
Section 2 proves the stronger useful assertion that one explicit fixed A
works on the whole half-line. No universal envelope-selection theorem or
counterexample follows from this example.
