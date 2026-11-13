# THREEFOLDRELAX: a radius-ordered relaxation for threefold symmetry (4 November 2026)

**Why a relaxation.** For m = 3 and K = 8 the layer lemma fails (8 > 2·3), because a convex layer may hold two orbits.
`gen_relax.py --nonest` (a copy of `C7UPPER/gen.py` with 5 hunks changed) drops the nesting family and orders the orbits
by decreasing radius.

**Soundness: written proof, not refereed.**
- **Normalisation.** A small perturbation gives distinct radii and generic phases; both properties are open conditions.
- **Rule B.** It needs only radii.
- **Chains.** Every other point of orbits ≥ i lies in the open tangent half-plane at the pivot, since ⟨q,p⟩ < r_i² for
  q ≠ p.
- **Coverage.** Every convex K-gon has a vertex of largest radius.
- **Why the nesting family must go.** It fails on the real 61-point and 31-point sets and on 2730 of 2730 random sets.

**Validation (exact computation).**
- **Known sets.** The certified threefold sets and their mirrors give 0 violations: 61 points (centre and blowup
  versions), 60 points, and the 31-point K = 7 set.
- **Negative controls.** The 63-point and 64-point near misses each give exactly 1 chain violation.
- **Random sets.** 2730 random configurations with two orbits in one convex layer give 0 non-chain violations, and the
  chain verdict equals brute force every time.

**Calibration.** The result is negative: the relaxation is too weak.
- **K = 7.** It is SAT at t = 10, 11, 12 and 13. The models for t = 10 and t = 11 are checked exactly; t = 12 and 13 are
  solver verdicts only. The true maximum is 10 orbits.
- **Why.** The SAT models violate 3-term Grassmann–Plücker relations: 25,650 at t = 10 and 29,370 at t = 11.
- **Lazy GP loop at t = 11.** 23 rounds were all SAT; round 24 timed out.
- **(3,8,22).** It has 170,270 variables and 7,400,332 clauses. No answer came in 800 s, which proves nothing.

**Next step.** Add a sound strengthening and calibrate it at K = 7, t = 11 before (3,8,22). Candidates: GP clauses,
hull-batch constraints, or signotope axioms.

The CNFs (up to 197 MB) are not in Git. They regenerate from `gen_relax.py`, and their hashes are in
`CNF_SHA256SUMS`. The agent's full report is in the coordinator's notes.
