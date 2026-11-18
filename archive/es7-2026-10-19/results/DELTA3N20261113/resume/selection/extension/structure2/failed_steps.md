# Two exact failed steps on terminal18

**PROVED finite obstructions, using the frozen real coordinates.** These
refute the stated restricted selection rules, not weak Delta or uniform
selection. Indices are those of `../../terminal/data/witness.json`.
The full set is (5,7)-valid and has maximum cup five.

Its cup-ending ranks are

    1,2,3,4,5,3,3,4,5,3,4,5,4,4,5,5,5,5.

Thus L5={4,8,11,14,15,16,17}, L4={3,7,10,12,13}, and T=L4 union L5.
The data files retain the full frozen coordinates and exact profiles;
verification uses the points afresh.

## 1. One rank-four representative is insufficient

L5 misses exactly the two hexagons

    H0=(0,1,5,6,9,10), H1=(0,1,5,7,9,10).

Their common vertices are {0,1,5,9,10}; the sole common rank-four vertex
is p=10. Thus the nonvacuous hypothesis of `CANDIDATE.md` holds.

But every weak Delta contained in L5 union {10} would have to include
10,11,14,16, forced by these hexagons:

| Hexagon | Intersection with L5 union {10} |
|---|---|
| (0,1,5,6,9,10) | {10} |
| (0,1,2,6,7,11) | {11} |
| (2,3,5,6,13,14) | {14} |
| (2,3,5,6,13,16) | {16} |

The forced set (10,11,14,16) is a four-cap. Hence no ordinary weak Delta
exists in that region, a fortiori no uniform one. Enumeration of its 128
subsets agrees: 126 fail coverage, the remaining two have four-caps.
No solver verdict is needed for this four-target contradiction.

## 2. Replacing every mixed blocker by its first pair is too strong

For subsets of T, every exposed cap triple and every old four-cap has
first two cup ranks 4,5. For triples this follows from the prior rank
lemma: beta(a)>=beta(b) would supply an identical ambient terminal pair.
For a four-cap, its first triple must have terminal cap rank three, since
rank four would extend to a five-cap. Thus the same strict rank inequality
applies. The first two vertices give a bipartite graph G between the levels.

An independent set of G avoids every original blocker and is therefore
cap-free and envelope-safe. But G need not have an independent set hitting
all hexagons. This stronger pair replacement fails on terminal18.

Five of its graph edges, with actual blocker witnesses, are

| Edge | Witness giving that first pair |
|---|---|
| 3--4 | four-cap (3,4,11,12) |
| 7--8 | four-cap (7,8,11,12) |
| 10--11 | four-cap (10,11,14,16) |
| 10--14 | four-cap (10,14,15,16) |
| 12--16 | exposed cap triple (12,16,17) |

The final triple's terminal line is exposed at t=1, with X=max_x(U)+t;
verification compares it exactly against every ambient four-cap line.
The following hexagons have these traces on T:

| Hexagon | Trace on T |
|---|---|
| (0,1,5,6,9,10) | {10} |
| (0,1,2,6,7,11) | {7,11} |
| (0,1,8,9,14,16) | {8,14,16} |
| (2,3,5,9,11,12) | {3,11,12} |
| (2,4,5,9,11,12) | {4,11,12} |

Any independent transversal selects 10. Edges 10--11 and 10--14 exclude
11 and 14. The second trace forces 7, so edge 7--8 excludes 8. The third
trace forces 16, so edge 12--16 excludes 12. The last two traces force
both 3 and 4, contradicting edge 3--4. This is an explicit ten-row
contradiction, not an uncertified solver UNSAT claim.

## 3. The original constraints still have solutions inside T

A={3,4,7,10,14,16} is an exactly checked uniform-envelope Delta in T.
It may contain 3,4 because it omits the remaining vertices of that pair's
forbidden quadruple. It also contains 10,14 without the third vertex 15
of their exposed triple.

Enumeration over 4,096 subsets of T finds 28 ordinary weak Deltas, 16
uniform-envelope Deltas, no terminal-safe Delta, and no G-independent
transversal. These are fixed-instance COMPUTED counts. The written
contradictions above do not depend on exhaustion. Separate verification
rechecks one positive uniform witness and every row in both negative proofs.

More rank-four vertices may be essential for coverage. Also, the third
and fourth vertices of a blocker matter: forbidding just its first pair
can remove all favorable selections. It remains open here whether some
uniform selector always lies in T for the full maximum-cup-five subclass.
