# Exact coordinate clauses and their scope

## Fixed-instance model

Let U=(p_0,...,p_{m-1}) have strictly increasing x coordinates and no three
collinear points. A cap has strictly decreasing consecutive slopes. A convex
k-gon means any k points in convex position, not necessarily an empty polygon.
The premise is no five-cap and no convex n-gon, with k=n-1.

For each point, Boolean x_i means p_i is selected in A. The full coloring
formula consists of:

1. For each four-cap C, the clause OR_{i in C} not x_i.
2. For each three-cap (a,b,c) whose terminal pair (b,c) has maximum ambient
   cap length exactly three, the clause not x_a OR not x_b OR not x_c.
3. For each complete convex k-gon H, the clause OR_{i in H} x_i.

The first and third families say exactly that A is a weak Delta. Under the
five-cap-free premise, the terminal pair of a three-cap has rank either
three or four. Thus the second family says exactly that all selected cap
triples have ambient terminal rank four. There are no orientation variables,
realization assumptions, or lower-chain-only hit clauses.

UNSAT of a subformula consisting of actual clauses of these families excludes
a terminal-safe weak Delta for these coordinates. A finder verdict is only
COMPUTED. CERTIFIED additionally requires a fresh retained LRAT accepted by
cake_lpr with its literal `s VERIFIED UNSAT` and recorded CNF/proof hashes.
The geometric premises and clause interpretation require independent exact
checking even when a propositional certificate is available.

## Redundancy lemma (PROVED, written)

In a five-cap-free U, every four-cap a,b,c,d has h_U(b,c)=3. The rank is at
least three, because a,b,c is a cap. If it were four, a four-cap ending b,c
could be extended by d, giving a five-cap. This is impossible. Therefore the
initial triple of every four-cap is in family 2; its negative triple clause
implies the negative four-cap clause. Family 1 is redundant, although the
full frozen CNF retains it. The reduced core uses only families 2 and 3.

## Geometry implementation and independent controls

`encode.cpp` computes determinants in signed 128-bit integers, with an input
coordinate bound of 10^15. Coordinate differences are at most 2*10^15,
so the determinant magnitude is at most 8*10^30, below 2^127.
It computes terminal ranks by the recurrence

    h(b,c) = max(2, 1+h(a,b) over a<b with orientation(a,b,c)<0).

For each fixed first endpoint it computes maximum cup and cap lengths by
the analogous recurrence. A cap and a cup with the same endpoints have
disjoint interiors, lying strictly above and below the endpoint line.
Their union is convex, with size cap_length+cup_length-2. Conversely the
upper and lower hull chains of a convex polygon are exactly such a cap
and cup. This justifies the convexity maximum and enumerated target sets.

`check.py` does not import the encoder or finder: it uses unbounded Python
integers, enumerates caps directly, obtains rank-three terminals by excluding
the endpoints of enumerated four-caps, and enumerates each candidate polygon
with a monotone-chain convex hull. It compares complete clause sets and
checks saved SAT models. Its exhaustive coloring count is a separate finite
COMPUTED calculation, not an LRAT certificate or an EXACT TREE in the
repository's omission-tree sense. It is independent code by the same agent,
not a separate person's audit.

## All-X envelope calculation

For each cap terminal pair, its line is represented by rational slope and
intercept. `envelope.py` builds the upper envelope F4 of ambient four-cap
terminal lines. For any line L, L<=F4 on X>xmax iff it holds at xmax and
at each envelope breakpoint strictly to its right, and the final envelope
slope is at least the slope of L. This follows because F4-L is affine on
each interval, and the final interval is a ray. Boundary tests at xmax are
valid for the open half-line by continuity.

For a fixed selection A, every triple line must pass this test. For each
representative X, only its value is tested. The program enumerates all weak
Deltas and reports both counts. This is a finite-instance result: neither
failure of the rank condition nor survival of the envelope condition proves
or refutes the universal envelope-selection statement.
