# Real eleven-point lower bound — independently checked

**COMPUTED by exact integer enumeration:** the following eleven real points
have no five-cap or convex seven-gon, have no weak Delta of size at most
two, and have a terminal-safe weak Delta of size three. **PROVED written
implication:** the finite geometric facts and pair-cover certificate below
establish minimum weak and terminal-safe Delta size exactly three for this
set. A one-parameter extension follows by affine interpolation of exact
orientation determinants. No LRAT/CERTIFIED, Lean, novelty or ambient-size
minimality claim is made.

## Coordinates and the positive selection

Labels are zero based, in increasing x order.

| i | x | y |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 2 | -1 |
| 2 | 9 | 2 |
| 3 | 24 | 9 |
| 4 | 25 | -13 |
| 5 | 48 | 1 |
| 6 | 71 | -29 |
| 7 | 85 | -11 |
| 8 | 86 | -11 |
| 9 | 140 | 59 |
| 10 | 141 | 0 |

Take **A={0,1,3}**. Its determinant is **42>0**, so A is a cup. It has no
four-cap and no cap triple at all, hence is terminal-safe. Every convex
six-subset of U meets A, as checked by the complete hull enumeration.
Thus A is a weak Delta as well.

The exact geometric facts are:

- All 165 triple determinants are nonzero; the smallest absolute value is 1.
- There are twelve four-caps and **no five-cap** among the 462 five-subsets.
- There are exactly **22 convex six-subsets** and **no convex seven-subset**
  among the 330 seven-subsets. The maximum cap/cup/convex sizes are (4,5,6).
- Every one of the 22 six-targets meets A.

The complete target/four-cap lists and every pair's explicit disjoint
six-target are in [simple11.verify.json](data/simple11.verify.json).
The coordinates are in [witness.json](data/witness.json), also available
as [plain point data](data/witness.points).

## A short certificate excluding all pairs

For each five-subset B in this table, its six-point complement U\\B is
convex. The twelve B rows together contain **every one of the 55 pairs**.

| B, whose complement is a convex six-subset |
|---|
| {3,4,8,9,10} |
| {0,2,5,7,10} |
| {0,1,5,6,8} |
| {2,4,5,6,9} |
| {1,3,7,9,10} |
| {2,3,4,5,6} |
| {0,1,2,4,6} |
| {0,3,8,9,10} |
| {0,2,5,7,8} |
| {3,4,7,9,10} |
| {3,4,6,9,10} |
| {0,2,5,6,7} |

Given a pair D, choose a row B containing it. The convex six-set U\\B is
disjoint from D, so D is not a weak Delta. Every singleton and the empty
set can be extended to a pair, so they fail too. Together with the cup A
above, this proves the claimed exact minimum size three. No minimality of
this twelve-row certificate or of the eleven-point ambient size is claimed.

As a redundant finite check, all 2,048 subsets were inspected. Counts by
selection size are:

| Size | Weak Deltas | Terminal-safe weak Deltas |
|---:|---:|---:|
| 0,1,2 | 0 | 0 |
| 3 | 65 | 46 |
| 4 | 246 | 96 |
| 5 | 379 | 62 |
| 6 | 297 | 9 |
| 7 | 126 | 0 |
| 8 | 26 | 0 |
| 9 | 2 | 0 |
| 10,11 | 0 | 0 |

## A non-affine one-parameter family on eleven points

Keep ten points fixed and replace only p5 by

    p5(t)=(48,1+t),       -1<t<8/61.

Every triple retains its original orientation throughout this open interval,
so all premises, target sets, pair obstructions and the same cup Delta A
remain unchanged. Equivalently, p5's height can be any real
number strictly between **0 and 69/61**.

Here is the written interval proof. For each original triple, multiply its
determinant by its original sign. The result is affine in t. At t=-1 all
165 such values are nonnegative, and exactly triple (0,5,10) is zero. At
t=8/61 they are again all nonnegative, and exactly triple (3,5,7) is zero.
These zero sets are disjoint. An affine function nonnegative at both ends
and not zero at both is positive at every interior point. Thus all signs
are strictly preserved. Distinct increasing x coordinates do not change.

The two active determinants are

    det(p0,p5(t),p10) = -141(1+t),
    det(p3,p5(t),p7)  = 8-61t.

Consequently the strict interval cannot be enlarged while preserving this
entire orientation vector; either endpoint is collinear. This is a family
of eleven-point examples, not an all-n or increasing-size construction.
The independent [endpoint certificate](data/family-endpoints.verify.json)
uses integer-scaled coordinates and the geometry replay's determinant
routine, importing no family finder. Full independent hull replays at
t=-1/2 and t=4/61 also pass.

## Discovery, independence and unsuccessful attempts

The finder first exhausted eleven-subsets of three retained real sources:

| Source | Eleven-subsets checked | Outcome |
|---|---:|---|
| terminal18 | 31,824 | Every one has a pair hitting all six-targets |
| compact16 | 4,368 | Every one has a pair hitting all six-targets |
| star12 | 12 | Every one has a pair hitting all six-targets |

Every attempted subset and its first hitting pair is retained in the TSV
traces. These are bounded finder outcomes on those three sources, not an
exhaustive statement about other coordinate pools or all real sets.

Next, `realize.py` used the existing n7/m11/k2 abstract SAT model only as
an orientation target. Eight deterministic fixed-x numerical proposals
were tried. The first seven produced no candidate; their statuses are
retained without interpreting a HiGHS status as mathematical evidence.
The eighth produced rationally reconstructed integer coordinates, and
**all 165 signs were checked exactly** before accepting them. The initial
realization remains in `sat11.candidate.json`.

`simplify.py` then preserved all signs using exact integer rounding and
single-coordinate admissible intervals. The first 109 rounding amplitudes
failed; amplitude 110 succeeded. Subsequent coordinate moves yielded the
small table above. Every failed rounding has its first incorrect triple
recorded. This is not an optimal coordinate-size claim.

The coordinate-subset finder uses the four-subset convexity criterion.
The independent `verify.py` imports no finder, optimizer, audit script or
parent checker. It uses the expanded shoelace determinant, monotone convex
hulls, direct all-triple cap tests, every pair, and all 2,048 subsets. It
separately checks the initial realization, simplified realization and two
family samples. The independent endpoint check proves the entire parameter
interval from nonnegative endpoint signs. Seven deliberately invalid
controls are rejected: a convex eleven-cup, a duplicate point, both family
endpoints, a triple missing a target, an ordinary Delta triple that is not
terminal-safe, and a valid boundary set admitting a pair.

## Resources and limits

Every invocation used one CPU, AS400 MiB, at most 18 CPU seconds and an
external 20-second deadline. The longest measured search was under one
second, and largest observed RSS was 75,572 KiB during numerical discovery.
No long job, solver CNF scan, large replay, OOM, AS failure, timeout,
installation, git mutation, external action or proof deletion occurred.
The parent's uniform-envelope replay and optional terminal-safe CNF scan
were not duplicated. The completed `../audit/` remains unchanged and its
manifest was rechecked. Only `extension/cardinality/` and its own scratch
directory were written; no shared manifests or old records were changed.

There is no unresolved candidate in this bounded task. No new ES bound,
ordinary Delta counterexample, all-n extension, or global ambient-size
minimality follows. All jobs in this subtrack are finished.
