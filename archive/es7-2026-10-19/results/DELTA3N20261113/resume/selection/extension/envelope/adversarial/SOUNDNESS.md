# Exact score and bounded-search scope

All search decisions use exact integers. The search strategy is HEURISTIC;
the reported survivor counts for retained coordinates are COMPUTED exact
finite enumerations. No absence of a counterexample establishes a theorem
for this orientation cell or for uniform selection in general.

## The invariant ordinary family

The retained18-point n7 fixture is freshly checked by the parent envelope
geometry/model code. Its full no-five-cap/no-seven-gon premises, all four-caps
and all convex six-gons are exact. For each of the2^18 membership assignments
A, the ordinary weak Delta formula forbids a selected four-cap and requires
a hit in every whole six-gon. The initial family is therefore precisely all
ordinary weak Deltas, not a previously selected subfamily.

`ordinary_family` represents the formula's truth table in one large integer.
Bit A corresponds to assignment A. The truth table for membership of vertex
v consists of alternating zero/one blocks of length2^v; repeated doubling
constructs it exactly. Bitwise conjunction/disjunction/complement implements
the clauses. The separate control explicitly loops through all262,144
assignments and directly evaluates every required clause, agreeing on the
same8,149 masks. At the baseline, direct checks of all8,149 masks against
the exposed triples agree with the bitset score4,057.

Every accepted coordinate state preserves every sorted triple's strict
orientation. Cups/caps and convex subsets depend only on these orientations,
so the ordinary family and geometric premises remain unchanged. Hence an
ordinary weak Delta failure is impossible in this cell; only uniform
envelope failure is being sought.

## Pair coverage and exact envelope score

For each candidate terminal pair(b,c), the earlier-vertex mask lists all
a<b for which(a,b,c) is a cap triple. A Delta A contains a cap triple ending
in(b,c) iff it contains b,c and at least one vertex in this mask. The stored
bitset therefore marks exactly the Deltas that would be removed if this
terminal line were exposed. A pair already ending an ambient four-cap can
never be exposed, since its own line belongs to the ambient maximum.

For each remaining pair, subtract each ambient line using positive integer
denominators. The exact strict inequalities are ds*t+dz>0, t>0. Intersect
their strict rational bounds using integer cross-products. A single ambient
line dominating both slope and height, or an empty bound intersection,
establishes safety. No approximation or tolerance is used. The score is

    8149 - popcount(union of pair-coverage bitsets for all exposed pairs).

This is exactly the number of uniform Deltas by the prior forbidden-triple
theorem. It is not the number of exposed pairs or triples. Every accepted
state and every new sampled exposure family is checked against the full
Fraction/certificate implementation. Each strict best is additionally
checked by looping over all8,149 ordinary masks and all its exposed triples,
and receives a complete coordinate CNF and geometric positive model check.

The fast line predicate agrees with an independently written Fraction
intersection test on1,000 deterministic algebra controls, including empty
families and equal slopes. These are implementation controls, not a general
formal verification.

## Exact one-coordinate bounds and bounded search

The initial x and y coordinates are multiplied once by4096. All subsequent
x coordinates remain fixed. y lies on the integer grid in the box
[-B,B], B=16*max_i|initial y_i|, well inside the geometry encoder's coordinate
bound. Positive scaling preserves the initial orientations and exposures.

When only y_v moves, each affected determinant is affine, d=c*y_v+k, with
nonzero integer c determined by the fixed x coordinates. Its required strict
sign gives a strict lower or upper rational bound. For root N/D, D>0, the
integer lower endpoint is floor(N/D)+1 and upper endpoint is
ceil(N/D)-1=(N-1)//D. Intersect all such bounds with the box. Current y_v
must remain inside. Testing all triple signs after every accepted move
provides a separate guard against a bound implementation error.

The controls check both endpoints for all18 vertices. Each endpoint preserves
every orientation; stepping beyond a non-box endpoint violates at least one
strict sign. This checks the rounding and open-boundary behavior.

The deterministic heuristic visits integer endpoints, near-boundary fractions,
the midpoint and four random integers for one randomly chosen vertex. It
usually selects the lowest survivor count, allows neutral movement, and uses
warmup/rare escape moves plus restarts. These choices are not exhaustive.
All accepted moves and restart coordinates are retained in a replayable
trajectory; strict bests retain full proof inputs. The declared proposal,
restart, step and wall-clock limits bound the run independently.

If the exact score reaches zero, the driver freezes a full coordinate CNF,
all coordinates and exposure data, then stops. Any UNSAT solver result remains
uncertified until the parent independently audits the encoding and retains
a proof accepted by cake_lpr with exactly `s VERIFIED UNSAT`.
