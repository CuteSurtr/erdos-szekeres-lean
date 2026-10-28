# SYMMAX: the largest symmetric point sets without a convex 7-gon

For a symmetry type, N(type) is the largest number of points in general position with that symmetry and no 7 points in
convex position. All point files here have been checked exactly (see Verification).

| symmetry | possible sizes | example here | upper bound | N |
|---|---|---|---|---|
| 3-fold rotation | 3m, 3m+1 (centre allowed) | `c3_31points.txt` (31, with centre) | 32 is not a possible size; every set with at least 33 points contains a 33-point 3-fold set, excluded by `results/C3FINAL` | **31** |
| 6-fold rotation | 6m (no centre) | `c6_30points.txt` (30) | a 36-point 6-fold set contains a 33-point 3-fold set | **30** |
| 4-fold rotation | 4m (no centre) | `c4_28points.txt` (28) | no 32-point 4-fold set exists (Subercaseaux, Mackey, Qian, Heule, arXiv 2506.00224, §6.2); larger sets contain one | **28** (with their result) |
| 2-fold rotation (central symmetry) | 2m (no centre) | `results/SYM2/sym7_32points.txt` (32) | a 34-point set would refute ES(7) = 33; not excluded | at least 32 |
| 5-fold rotation | 5m, 5m+1 | not searched | 35 or 36 points would refute ES(7) = 33 | open |
| mirror | 2m + b, b <= 2 points on the axis | `mirror_32points.txt` (32, no point on the axis) | 33 points with one point on the axis: excluded (`results/FINAL`, `results/WRITEUP/MIRROR.md`); 34 points with no point on the axis would refute ES(7) = 33, not excluded | at least 32 |
| rotation of order 7 or more | | | every orbit is a convex polygon with at least 7 vertices | none |

An even-order rotation contains the half-turn, so a centre point would be collinear with every pair p, -p. That is why
those sizes are multiples of the order.

The 2-fold and mirror rows both reach 32, the largest size any 7-gon-free set can have if ES(7) = 33. The 2-fold example
is the explicit construction of `results/SYM2`; the mirror example was found by search. The paper above treats only
rotations.

Also here: two further 3-fold sets, `c3_30points.txt` (30, no centre) and `c3_27points.txt` (27).

## What the 33-point theorem covers, and what it does not

`results/C3FINAL` with the mirror class gives: every set of 33 points in general position with a nontrivial symmetry
contains 7 points in convex position. So a 33-point counterexample to ES(7) = 33 has no symmetry.

A symmetric set with more than 33 points and no convex 7-gon would refute ES(7) = 33 too. Such sets are excluded here in
three cases: when they have a 3-fold rotation (they contain a 33-point 3-fold set); when they have a mirror with at
least one point on the axis (they contain a 33-point mirror set with one axis point); and, by the result above, when
they have a 4-fold rotation. Not excluded: centrally symmetric sets of 34 or more points, mirror-symmetric sets with no
point on the axis (even size, 34 or more), and 5-fold sets of 35 or more points.

## Coordinates

`c3_27points.txt` 27 points, |coordinate| <= 287; `c3_30points.txt` 30 points, |coordinate| <= 306; `c3_31points.txt` 31 points, |coordinate| <= 1017; `c4_28points.txt` 28 points, |coordinate| <= 147; `c6_30points.txt` 30 points, |coordinate| <= 456; `mirror_32points.txt` 32 points, |coordinate| <= 614.

- 4-fold and mirror files: ordinary integer coordinates, rotation (x, y) -> (-y, x), mirror (x, y) -> (-x, y).
- 3-fold and 6-fold files: Eisenstein coordinates. A line (a, b) is the point a + b·w, w = e^(2πi/3), that is the plane
  point (a - b/2, b·√3/2). This map is linear and invertible, so collinearity and convex position are decided exactly on
  the integer pairs. In these coordinates the rotation by 120° is (a, b) -> (-b, a - b), and the rotation by 60° is
  (a, b) -> (a - b, a).

## Verification

- `python3 verifyg.py G FILE 7`, with G in {3, 4, 6, 2, M}. It checks, with exact integer arithmetic: distinct points,
  invariance under the symmetry, no three collinear, and the largest subset in convex position (dynamic program in
  `convex.py`). It also writes `FILE.orient`.
- `brute.c` (`cc -O2 -o brute brute.c; ./brute 7 < FILE.orient`): an independent brute force over every 7-point subset
  (a subset is in convex position iff no point lies in a triangle of three others).
  - c3_31points: 2,629,575 subsets, 0 convex.
  - c3_30points: 2,035,800, 0.
  - c3_27points: 888,030, 0.
  - c4_28points: 1,184,040, 0.
  - c6_30points: 2,035,800, 0.
  - mirror_32points: 3,365,856, 0.

## How they were found

`annealg.c`: simulated annealing on the orbit representatives (integer coordinates, the orbit rebuilt exactly by the
symmetry map). The cost is the exact number of convex 7-gons, by a dynamic program. Runs: 2026-10-28 on one machine.
Time to the first zero-cost set:
- 3-fold 27: under 1 minute.
- 3-fold 30: 1 to 3 minutes.
- 3-fold 31: about 3 minutes.
- 4-fold 28: 1 second.
- 6-fold 30: about 10 seconds.
- mirror 32: 22 seconds.

`shrink.py` then scaled the representatives down while all checks still passed.
