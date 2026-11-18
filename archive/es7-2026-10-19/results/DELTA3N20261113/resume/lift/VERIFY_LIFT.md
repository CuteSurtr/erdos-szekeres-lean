# Verification scope for the fixed-old extension sidecar

**CONFIRMED at the stated local scopes.** The all-gap one-insertion n7 CNF
has an accepted LRAT proof. Source coordinates and real controls use exact
integers. The weak-n8 five-insertion obstruction is a written proof. No
n7/n8 counterexample or general conjecture is confirmed.

Selectors choose an increasing injection because d_i is nondecreasing.
Every old triple is fixed at that injection; conversely every increasing
source copy supplies selectors. Conditional triple clauses are vacuous
unless all their selectors are active. The parent reported reading this
argument and the weak-n8 proof and finding both sound. No Lean check exists.

`audit_extension.py` and `controls.py` import neither the old universal
encoder, its checker, coordinator geometry code nor generic-cluster code.
They compute arbitrary-precision determinants; real convexity uses hulls,
abstract convexity uses all four-subsets. The Delta scan uses a full subset
transform, not the encoder's bounded-deletion witness DAG. Actual clauses
are evaluated literally. These two programs share their own geometry
module and are not independent of each other.

The positive real16 extension is nonvacuous: all 203,832 validity/embedding
clauses hold, it has 30 hexagons and many cup-side Deltas. Full-formula
positive controls reproduce the existing real15 cup-side failure and its
actual clause values. Tiny exhaustive embedding controls cover 10,240
orientation/embedding combinations, including nonrealizable sign assignments.
The secant-sign control lies outside the generic pair model but fails
geometric validity; those failures are explicitly retained. Early collinear
and vacuous controls are retained, corrected and not counted as evidence.

The first certificate pairs CNF SHA-256
`9138cb5807ca6d208e2cb3f1519b0060026d495e295e9388c1f45bc35284d233`
with LRAT SHA-256
`41978f2d53df04787a34aba49a119675079d95b63bb5f5350cef7541289467f1`.
The actual cake_lpr output contains exactly the whole line `s VERIFIED UNSAT`.
Its exit status alone was not evidence. The parent's fresh solver/checker
rerun subsequently passed (0.364s / 0.564s), with the same CNF and LRAT
hashes. Its result and exact checker line were read, and its small evidence
is copied into `data/parent-add1/`. The copied compressed proof was checked
by decompression against the uncompressed SHA-256.

The two-insertion result is UNKNOWN. Its partial LRAT and the SAT traces
are not certificates. Optional preprocessing has separate complete tiny
truth-table controls and a full-original-CNF SAT audit. It was not used
in the one-insertion exclusion. Existing universal-encoder soundness remains
an explicit dependency: this is not an independent implementation of that
component. Identical CNF regeneration is a reproducibility check, not an
independent encoding proof. No new result is Lean-checked or refereed.
