# Searching for 33 points without a convex heptagon — 11–13 October 2026

ES(7) ≥ 33 is the classical lower bound; the Erdős–Szekeres conjecture says
ES(7) = 33. A set of 33 points in general position with no convex heptagon
would disprove it. **No such set was found, and nothing about ES(7) is
established.** All results here are exploratory computations, not Lean proofs.

## SAT encoding (`encoding/`)

`gen_cnf.py` encodes N points as a signotope (one variable per triple; the
four-point monotonicity axiom) with cup/cap chain variables forbidding K points
in convex position. Symmetry breaking (`hm`): point 1 is extreme and the other
points are sorted around it, and an x-reflection rule; both are justified for
real point sets. Validation:

| Check | Result |
| --- | --- |
| Every signotope with N ≤ 7 against brute force (K = 4, 5) | 0 mismatches |
| K = 5: N = 8 SAT, N = 9 UNSAT | as required by ES(5) = 9 |
| K = 6: N = 16 SAT, N = 17 UNSAT | as required by ES(6) = 17; the N = 17 refutation was checked with an LRAT proof |
| K = 7: N = 32 SAT | model checked by brute force over all 7-subsets |

A SAT model is an abstract configuration; it is a counterexample only after a
realization by real coordinates. `realize.c` attempts this and `brute_kgon.c`
re-checks models by brute force.

## Cube-and-conquer (`cnc/`)

`worker.cpp` (linked against CaDiCaL 3.0.1) keeps the formula loaded and
solves cubes under a conflict budget; an unresolved cube is split on the
solver's lookahead literal into two disjoint children, so open cubes always
partition the unrefuted part of the space. `cnc.py` schedules cubes on
persistent workers with per-worker lineages. The same code re-proved the
refutation for K = 6, N = 17 in 100 s with 473 cubes whose weights sum to 1.

For K = 7, N = 33 (`n33k7hm`), the run on 12 workers (later 4) ruled out
about 2,200 cubes in roughly 17 hours of wall time without finding a model.
The unrefuted part is concentrated in about 100 deep cubes (depth up to about
190), and the frontier did not shrink steadily, so no completion estimate is
possible. `run33-state.json` holds the open cubes, from which the run resumes;
cube refutations are solver answers without proof logs. An earlier portfolio
of eight randomized CaDiCaL runs on the same formula
(`portfolio-manifest.json`, about 2.9 CPU-hours each) also ended `UNKNOWN`.

## Extremal 32-point sets (`saturation/`)

The generator anneals and random-walks through heptagon-free 32-point sets,
deduplicates them by order type, and tests each with the exact one-point
extension program of the [ES(8) search record](../es8-lower-bound-search-2026-10-11/README.md).
All 8,537 distinct order types tested were saturated: no 33rd point avoids a
convex heptagon. The pipeline was first validated on 18,617 hexagon-free
16-point order types, all saturated as ES(6) = 17 requires. A separate SAT test
showed that 267 of these and related sets have no one-point extension even in
the abstract model. These samples come from annealing and local walks and are a
tiny, biased part of all heptagon-free 32-point configurations.

The direction of this search follows a suggestion by Andrew Suk that the
conjecture might fail for small n. No literature-priority claim is made.

## Rotationally symmetric SAT models (`symmetric/`, added 14 October 2026)

`symcnf.py` encodes N points with an m-fold rotational symmetry as a CC system
(Knuth interiority and Grassmann–Plücker clauses on orbit representatives of
triples, with an auxiliary or included centre and a labelling normal form); the
"no convex K-gon" constraint uses the 4-point criterion. The encoding was checked
against brute force on all models of small instances and against 3,040 random
realizable symmetric sets (`symcheck.py`, `axiom5_check.py`, `symvalidate.py`),
and it reproduces the controls: 16 points, no hexagon: 3-fold UNSAT, 4- and
5-fold SAT; 18 points, no hexagon: UNSAT for m = 2, 3, 6, 9 (DRAT-checked).

| Instance | Outcome |
| --- | --- |
| 33 points, no heptagon, 11-fold | UNSAT in 0.75 s, trivially: an 11-point orbit is a regular 11-gon, so every symmetry order ≥ 7 is excluded |
| 33 points, no heptagon, 3-fold (2,002 orientation orbits; 464k variables, 9.5M clauses) | undecided after two 2-hour CaDiCaL runs and a short cube-and-conquer start (`cnc/`, 5 cubes refuted, 3 open at the checkpoint) |
| 32 points, no heptagon, 2-fold | SAT in 51 s; 45 distinct abstract models (`enum_models.cpp`), none realized by the two realizers here (`symrealize.c`, `lp_realize.py`), which also fail on known-realizable symmetric 32-point chirotopes, so no realizability conclusion follows |

`runs-summary.txt` records the runs. A realizable 2-fold model would be a new
symmetric extremal 32-point set, not a counterexample; the 3-fold 33-point
question is the open symmetric target. Nothing about ES(7) is established.
