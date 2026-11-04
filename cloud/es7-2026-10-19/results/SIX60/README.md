# SIX60: the sixfold octagon-free maximum is exactly 60 (5 November 2026)

**Theorem.** The largest 6-fold rotationally symmetric set of points in general position in the plane with no
8 points in convex position has exactly **60** points.

| Part | Statement | Status |
|---|---|---|
| Lower bound | The two sets in `sets/` have 60 points, are invariant under rotation by 60 degrees, are in general position, and contain no 8 points in convex position. | Exact computation, three independent implementations (below). |
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

`sets/SHA256SUMS.txt` has the full hashes. Layer radii (outer layer = 1) and phases theta_i, from the float sources:
- **A.** A twin-layer spiral. The outer hexagon is followed by four pairs of near-twin layers: radius 0.290 / 0.256 at
  4.2 / 4.5 deg, 0.224 / 0.222 at 8.8 / 8.9 deg, 0.197 / 0.195 at 14.9 / 15.0 deg, and 0.146 / 0.146 at 19.47 /
  19.47 deg. A tiny innermost hexagon (radius 0.0096) sits at 0.07 deg, almost aligned with the outer one.
- **B.** A needle cluster. The outer hexagon is followed by eight layers at radii (5.2 to 4.0) x 10^-4 with phases
  28.1 to 36.0 deg, again roughly in twin pairs. The innermost hexagon has radius 1.0 x 10^-5 and phase 55.8 deg.

A and B have different numbers of convex 7-subsets (296,544 and 301,674), so they are different order types. Neither
contains a certified 54-point order type: by an exact computation with LRAT proofs checked by lrat-check (realization
workstream, `six10-linux` campaign), neither 54-point set of `ES8SYM` extends by one hexagon.

## Verification (exact computation)

1. **The finder's run of the ES8SYM pipeline** (`ES8SYM/tools`). It ran `verify_cfg.py --pts` (exact algebraic and
   interval methods), `cvx2` (two dynamic programs), `cvxcheck` (depth-first search), `crosscheck_decimal.py` and
   `enum_convex` on an affine image. All report 0 convex 8-subsets and largest convex subset 7, for A at scales 2^40
   and 2^28 and for B.
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
- A real configuration satisfies every sound clause, so this is a strong consistency check that none of these cut
  families is unsound.
- It also shows that cube c11111 could never have become UNSAT: the "54 or 60" question could not be settled by
  the 10-layer CEGAR, only by a construction.

## How the set was found (evidence; details in `construction/` when added)

The set came from alternating projections between real configurations and abstract models:
1. Start from a real 10-layer configuration with few convex octagons (direct annealing; best start had 90 convex
   octagons).
2. Steer a SAT solver over the lane formula (encoder A plus all certified cuts) toward that configuration's
   orientation signs by setting its phases.
3. Fit seeds to the resulting abstract model.
4. Anneal locally on the exact number of convex octagons until it reaches 0.

Then make the coordinates exact in Z[zeta_6]. The search was done by the realization workstream of the 5 November
campaign. The working record is outside git (`six10-linux-20261105/realize/`).
