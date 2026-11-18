# Testing maximality as a sufficient condition

**REFUTED by exact real coordinates:** the proposed strengthening that every inclusion-maximal four-cap-free
subset R of a (5,n)-valid configuration meets every convex (n−1)-gon fails
already at n=7. A different R can work; this does not refute weak Delta.

The independent audit `../audit/VERIFY_MAXIMAL.md` confirms a real 12-point
example, retained at `../audit/results/real-star-input.json`. It has no
five-cap or heptagon, 25 four-caps and 54 convex hexagons. The red set
{0,1,4,5,6,10} is four-cap-free and inclusion-maximal, but its complementary
six points form a hexagon. Every attempted addition has an explicit cap
blocker. Among all 65 maximal red sets, four fail; there are 1,526 working
weak Deltas. In particular the singleton {8} meets every hexagon.

The coordinates were found by the bounded C++ `real_star.cpp` sampling on
the existing real fixture pool, then reduced by `minimize_real_star.py`.
The independent audit uses its own integer determinants, hulls and all
4,096 subsets. It also checks a canonical assignment against every clause
of the new encoder on this real witness. These are COMPUTED exact checks,
not an LRAT certificate or a global minimum-size claim.

An earlier 16-point abstract SAT witness reduced to ten points; 300
numerical realization starts found no exact realization. That unresolved
search is retained and is not evidence of nonrealizability. The real
12-point result does not depend on it.

The saved real 16-point fixture from `coordinator/data/minimum16/witness.json`
has 144 inclusion-maximal four-cap-free sets; a direct exact-integer hull
probe found that all of them hit its 279 hexagons. This is only one positive
control and motivates a deliberately adversarial search.

`maximal_cnf.cpp` includes the already audited C++ geometric base verbatim.
The new red variables encode membership in R. For every four-subset K,
the clause consisting of its two positive consecutive orientation literals
and four negative red literals forbids an all-red four-cap. A cap witness
variable implies both negative consecutive orientations. For each point p,
either p is red, or a positive witness selects a cap containing p whose
other three points are red. This is precisely maximality; the witnesses
are one-way, with their actual geometric meanings giving a canonical
assignment in every genuine example. Finally, some (n−1)-subset is forced
to be blue and convex using one-way four-subset convexity witnesses.

Thus a SAT model represents a counterexample to this proposed strengthening
in the abstract model, subject to independent sign checks. A real claim
additionally needs exact coordinates. UNSAT, if freshly LRAT-certified,
proves the strengthening at the stated finite size and would imply weak
Delta there. Neither a timeout nor an unverified solver result does so.

Only the existing model's orientation convention is used; no symmetry,
fixed vertex positions, or assumed order of the red and blue points is added.
