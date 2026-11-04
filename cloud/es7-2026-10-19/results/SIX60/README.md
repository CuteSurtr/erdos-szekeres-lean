# SIX60: the sixfold octagon-free maximum is exactly 60 (5 November 2026)

**Theorem.** The largest 6-fold rotationally symmetric set of points in general position in the plane with no
8 points in convex position has exactly **60** points.

| Part | Statement | Status |
|---|---|---|
| Lower bound | The four sets A, B, C and D in `sets/` have 60 points, are invariant under rotation by 60 degrees, are in general position, and contain no 8 points in convex position. | Exact computation, three independent implementations per set (below). |
| Upper bound | Every 6-fold symmetric set of at least 61 points in general position contains a convex octagon. | `C6UPPER` (3 November): a certificate accepted by both checkers for two separately implemented encoders. The reduction is Lean-checked (`LAYERLEAN`). The encoder steps are a written proof, reviewed but not Lean-checked. |

Sizes of 6-fold sets without a centre are multiples of 6, and a general-position 6-fold set cannot contain the
centre. Together the two parts settle the question that `C6UPPER`, `SIX10REFINE`, `SIX10CEGAR` and
`STATUS20261104` left open as "54 or 60". The k = 8 table of `ES8SYM` and the note therefore change in the 6-fold row
from "54 or 60" to **60**. The 7-fold value was already exactly 64.

**Credit and priority.** The literature check of 4 November (`C6C7REVIEW/LITERATURE.md`) found no prior result on
octagon-free rotational sets; the symmetric literature it inspected stops at k = 7. That check was not repeated on
5 November. No priority claim is made beyond it.

## The sets

All coordinates are exact: one point per line, integers w_0..w_5 for the point sum_j w_j zeta^j, zeta = e^{2 pi i/6}.
Layer o is rows 6o..6o+5, outermost first.

| File | Order type | Scale | SHA-256 |
|---|---|---|---|
| `sets/c6_60pts_A.pts` | A | 2^28 | `614469e9…` |
| `sets/c6_60pts_A_scale2p40.pts` | A (the first certified file) | 2^40 | `7d67447e…` |
| `sets/c6_60pts_B.pts` | B | 2^28 | `2a0c981e…` |
| `sets/c6_60pts_C.pts` | C | 10^12 | `61ed920d…` |
| `sets/c6_60pts_C2.pts` | C' (rounding of C at 10^9; its own exact check) | 10^9 | `8ba0b2e9…` |
| `sets/c6_60pts_D.pts` | D (A robustified; **smallest coordinates, recommended for presentation**) | 2^19 | `e2eaceb9…` |

`sets/SHA256SUMS.txt` has the full hashes. Layer radii (outer layer = 1) and phases theta_i, from the float sources:
- **A.** A twin-layer spiral. The outer hexagon is followed by four pairs of near-twin layers: radius 0.290 / 0.256 at
  4.2 / 4.5 deg, 0.224 / 0.222 at 8.8 / 8.9 deg, 0.197 / 0.195 at 14.9 / 15.0 deg, and 0.146 / 0.146 at 19.47 /
  19.47 deg. A tiny innermost hexagon (radius 0.0096) sits at 0.07 deg, almost aligned with the outer one.
- **B.** A needle cluster. The outer hexagon is followed by eight layers at radii (5.2 to 4.0) x 10^-4 with phases
  28.1 to 36.0 deg, again roughly in twin pairs. The innermost hexagon has radius 1.0 x 10^-5 and phase 55.8 deg.

- **C.** Needles at the outer edge midpoints. Layers 1–8 are at radii 7.3 x 10^-3 to 3.7 x 10^-3 with phases 30.2 to
  34.9 deg. The innermost hexagon has radius 5.4 x 10^-6 and phase 35.1 deg.

- **D.** Set A after a constrained local optimisation that keeps the octagon count at 0 (`construction/tools/robustify.py`).
  All coefficients are at most 2^19 = 524,288, and the minimum normalized sine rises from 2.2e-5 to 1.3e-3.

A, B, C and D have 296,544, 301,674, 221,976 and 316,182 convex 7-subsets, so they are pairwise different order types. None of them
contains a certified 54-point order type of `ES8SYM` as nine of its layers. The realization workstream reports that
neither 54-point order type extends by one hexagon at any nesting position: 36 SAT cases, all UNSAT, with LRAT proofs
accepted by lrat-check (`construction/REALIZE_README.md`; not re-checked by the coordinator).

## Verification (exact computation)

1. **The finder's run of the ES8SYM pipeline** (`ES8SYM/tools`). It ran `verify_cfg.py --pts` (exact algebraic and
   interval methods), `cvx2` (two dynamic programs), `cvxcheck` (depth-first search), `crosscheck_decimal.py` and
   `enum_convex` on an affine image. All report 0 convex 8-subsets and largest convex subset 7, for A at scales 2^40
   and 2^28 and for B. The direct-search workstream ran the same pipeline, plus its own independent checker
   `indep_check.py`, on C and C' (`construction/SEARCH_README.md` §0).
2. **`verify/verify60.py`**, written independently by the coordinator (standard library only).
   - It works in the oblique integer coordinates z = a + b zeta: a = w0 - w2 - w3 + w5, b = w1 + w2 - w4 - w5. This is
     an affine image with positive determinant, so orientations and convex position are preserved.
   - It checks 60 distinct points, the origin absent, and closure under (a, b) -> (-b, a + b).
   - It checks all 34,220 triples for collinearity.
   - It computes the largest subset in convex position by two independently anchored O(n^4) dynamic programs.
   - `verify/selftest.py` validates the DP against brute force on 150 random small sets (0 mismatches) and on planted
     convex 9-gons. `logs/controls_54.log` reproduces 7 for both certified 54-point sets.
3. **`verify/dfs_convex.c`**, an exhaustive depth-first enumeration of all subsets in convex position with exact
   `__int128` orientations and no dynamic programming. It gives these counts (`logs/`):

| set | convex 4 | convex 5 | convex 6 | convex 7 | convex 8 |
|---|---:|---:|---:|---:|---:|
| A | 292,353 | 1,058,232 | 1,454,781 | 296,544 | 0 |
| B | 291,927 | 1,057,422 | 1,462,500 | 301,674 | 0 |
| C | 284,577 | 954,066 | 1,110,345 | 221,976 | 0 |
| C' | 284,607 | 954,234 | 1,111,230 | 223,416 | 0 |
| D | 297,279 | 1,128,000 | 1,651,268 | 316,182 | 0 |

Reproduce, from this directory:

```sh
python3 verify/selftest.py
python3 verify/verify60.py sets/c6_60pts_A.pts
gcc -O2 -o dfs_convex verify/dfs_convex.c
python3 -c "import sys
for l in open('sets/c6_60pts_A.pts'):
    l=l.split('#')[0].split()
    if l: w=list(map(int,l)); print(w[0]-w[2]-w[3]+w[5], w[1]+w[2]-w[4]-w[5])" > A_ab.txt
./dfs_convex A_ab.txt
```

## Consistency with the encodings and cuts (exact computation)

- Set A, labelled by the convention of `C7UPPER/gen.py` (theta_0 = 0, vertex (i,k) at angle theta_i + 60k), gives
  all 5,710 orbit signs and the phase-order variables exactly.
- Encoder A (`gen.py 6 8 10`) is satisfiable under these 5,746 values as assumptions. Its phase order of layers 1..4
  is 1 < 2 < 3 < 4, so A lies in cube c11111.
- The assignment satisfies every one of 2,157,010 clauses in 74 clause files: every cut family produced in the
  5 November campaign (chord lemma, GP, linear, facial, local, final-polynomial), `SIX10CEGAR/cuts_verified.clauses`
  and `SIX10REFINE/cut_model0090_sparse.clauses`.
- Set B (phase order 1 < 2 < ... < 9) was labelled and checked the same way. It satisfies all 2,195,980 clauses of
  the 84 clause files present at 01:25 KST.
- A real configuration satisfies every sound clause, so this is a strong consistency check that none of these cut
  families is unsound.
- It also shows that cube c11111 could never have become UNSAT: the "54 or 60" question could not be settled by
  the 10-layer CEGAR, only by a construction.

## How the sets were found (evidence; the claim rests only on the exact checks above)

Two different methods found octagon-free 60-point sets independently, within the same hour.

**Alternating projections (sets A and B, realization workstream).** The method alternates between real
configurations and abstract models:
1. Start from a real 10-layer configuration with few convex octagons (direct annealing; best start had 90 convex
   octagons).
2. Steer a SAT solver over the lane formula (encoder A plus all certified cuts) toward that configuration's
   orientation signs by setting its phases.
3. Fit seeds to the resulting abstract model.
4. Anneal locally on the exact number of convex octagons until it reaches 0.

Then make the coordinates exact in Z[zeta_6]. This gave A and B, found by the realization workstream. Its full record,
with parameters, seeds, file hashes and a reproduction recipe, is `construction/REALIZE_README.md` §4, with tools in
`construction/tools/`.

**Phase-fixed LP-CEGAR (set C, direct-search workstream).** With the phases fixed, every orientation is the sign of a
linear form in the inverse radii u_i = 1/r_i (`ES8SYM` Lemma 1). Existence of radii for a fixed phase vector is then
decided by SAT (encoder A with the phase units) plus an LP for the radii, adding a Farkas clause for each infeasible
sign vector. The run alternated phase scans around annealing optima with this check. Pure annealing of the octagon
count never got below 90. One perturbed phase vector produced, after 2,284 SAT/LP rounds, a realizable octagon-free
sign vector with LP margin 9.3 x 10^-4. Of 400 random phase vectors all were infeasible, and 293 of 300
perturbations: the realizable phase region is thin. Record: `construction/SEARCH_README.md`.
