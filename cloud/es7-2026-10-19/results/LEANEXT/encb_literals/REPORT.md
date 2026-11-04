# encb_literals: encoder B's orbit literals against real orientations (evidence only)

The target is `C6UPPER/encb/gen_b2.py`.
- **Method.** The script reads `main()` with `ast` and runs B's own `canon`, `orb` construction, `perm_sign` and `olit`
  unchanged; nothing is reimplemented.
- **Arithmetic.** float64, with a guard that rejects configurations where min |orient| < 1e-9. No configuration was
  rejected.

## Results

- **Literal test (evidence only).**
  - 164 configurations: 82 nested and 82 free, m = 4–7, t = 2–11.
  - **5,947,032 ordered triples, 0 mismatches.** The minimum |orient| was 2.7e-8.
  - Every `olit` call site (angular, nesting and chain clauses) uses distinct-point ordered triples, which this test
    covers.
- **Orbit check (exact computation).** `canon` is orbit-invariant, and the number of orbit variables equals the
  independently counted number of Z_m-orbits for every (m, t) tested.
- **Clause test (evidence only).** 360,621 instances of the transitivity, angular and nesting clauses on nested
  configurations, 0 violated. Chain clauses were not evaluated here.

## Mutants (`make_mutants.py`)

Seven single-edit copies of `gen_b2.py` were tested.
- **Caught.** Constant `perm_sign`, a flipped `olit` sign, and sorting the unrotated triple are detected by the literal
  test. A wrong rotation direction makes `olit` raise. A flipped angular sign and a reversed layer condition are caught
  by the clause test or by the encoder's own conflict check.
- **Expected pass.** Taking the maximum instead of the minimum in `canon` passes, as it should: the literal rule holds
  for any representative (`orbit/sign_eq_of_two_reps`, Lean-checked).

## Open issues

The test is float64, not exact. The chain recurrence is not tested here (see `C6UPPER` §3b for the brute-force chain
tests).
