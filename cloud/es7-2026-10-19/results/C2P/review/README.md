# Review of the reductions (A) and (B) used by C2P

(A) The 16 parallelogram hull cases reduce to the canonical cases P1..P8. (B) The reflection pairs the second-layer
subcases (P_a, V) and (P_a, {(a − i) mod 17 : i ∈ V}). The scripts are independent of the code under test, except
where they say they call it; the geometry helpers use exact integers.

- `litcheck.py`: literal-level check of the relabelling maps on the actual cube files (no geometry, no solver).
- `geom.py`: exact-integer helpers (orientation, convex layers, the angular normal form) used by the scripts below.
- `small_full.py`: small analogues of the central formula (t classes, K) generated with the code under test. Every
  clause of base.cnf is evaluated on designed and random real sets, original and reflected, with every hull vertex as
  the first point. Logs: `small/run_t*k*.log`.
- `big17.py`: real 34-point sets with a parallelogram hull designed to hit every (a, V). The script checks the map
  identities, the symmetry-breaking and hull clauses from the tail of the real base.cnf, and that exactly one hull
  cube and one second-layer cube hold, the geometric ones. Logs: `big17/run_a*.log`.
- `mut17.py`: mutation tests. Wrong class maps for (B) and wrong normal forms must be detected.
- `coverage.py`: every reflection orbit of the 560 subcases of each case has a member in `lists/C2P.tsv` or certified in
  the P8 pilot, and `orbits/P<a>.tsv` agrees with an independent orbit computation.
- `smoke17.py`: timing smoke test of the 34-point labelling.

Results (all with 0 failures):
- `litcheck.py`: 3 × 17,920 literal checks on the t = 17 cube files. The (B) map sends each full cube of (P_a, V),
  hull literals included, onto the cube of (P_a, V′) and preserves the symmetry-breaking units. The (A) maps send P_a
  cubes onto P_(17−a) cubes.
- `big17.py`: 8,960 real sets and 71,680 labellings. (B) gave the predicted subcase in 17,920 of 17,920 checks, and
  (A) the predicted case in 17,920 of 17,920. Convex 7-gon clauses are not evaluated here; random sets contain 7-gons.
- `small_full.py`: t/K = 7/7, 7/8, 8/7, 9/7, 9/8 and 11/8. That is 1,628 sets and 26,048 labellings, with 9,768 checks
  of (B) and 3,256 of (A). The 542 sets with no K points in convex position satisfy every clause and their own cubes;
  in the other sets, the only false clauses are genuine K-gon clauses. The 7/7 run printed to the terminal only.
- `mut17.py`: on 300 reflected sets the claimed map never mismatched, and each wrong map mismatched 291–300 times. A
  clockwise labelling was rejected by the symmetry-breaking units in 50 of 50 sets, and a non-hull first point by the
  hull clauses in 50 of 50.
- `coverage.py`: the orbit files agree, and `lists/C2P.tsv` covers every orbit of P1..P7 and their covers. Three P8
  orbits were left out of the list because their representatives timed out in the pilot: P8_1-9, P8_2-11 and P8_3-11.

(B) is a statement about real configurations, not a symmetry of the CNF: the map turns the hull clauses into "(a, 1)
is a hull vertex". So a partner subcase is excluded by this argument, not by a solver.
