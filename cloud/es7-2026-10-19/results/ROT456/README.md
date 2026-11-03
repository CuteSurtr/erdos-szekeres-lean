# ROT456: the 6-, 5- and 4-fold cases of ES(8) = 65 — encoder review and status (open)

3 November 2026 (UTC). **Status: the 6-fold case is settled in `C6UPPER`; the 5- and 4-fold cases are open.** This
directory records an independent review of the `C7UPPER` encoder for m = 4, 5, 6, its validation, and computations that
did not finish. The review in §2 is what `C6UPPER` relies on for m = 6.

## 1. Target

By the layer lemma (`SYM5/README.md` §2; K = 8 <= 2m), an m-fold symmetric set in general position with no convex
octagon is t nested regular m-gons, plus possibly the centre (odd m only). A set of at least 65 points needs
t >= 11 (m = 6), t >= 13 (m = 5) or t >= 17 (m = 4). UNSAT of the corresponding CNF would give the m-fold case of
ES(8) = 65, as `C7UPPER` does for m = 7. One layer beyond the best known sets (`ES8SYM`: 54, 56, 52 points), UNSAT
would give the exact maxima 54, 56 and 52.

## 2. Encoder soundness for m = 4, 5, 6

`C7UPPER/gen.py` is written for general (m, K), and its docstring gives the soundness proof. An independent review,
done line by line, found it sound for (4, 8), (5, 8) and (6, 8). This is a review plus tests, not a refereed or
formal proof.
- **Even m.** Antipodes are orbit points, so every direction is psi + 2 pi J/m and no H variables are needed.
  - Same-layer antipodal triples are degenerate and get no clause, which is weaker but sound.
  - General position forces distinct, nonzero phases.
  - A triple stabiliser can only act as a 3-cycle (an even permutation), so one variable per orbit is consistent.
- **Chain family.** K enters only through L = K - 1. A chain is a fan polygon with all turns to the left, hence a
  convex K-gon, for every K. Completeness also holds for K > m + 1 but is not needed.
- **Tests** (`tests/`, logs in `logs/`; exact cyclotomic or 90-digit arithmetic):
  - Fresh `gen.py` runs reproduce the CNFs byte for byte.
  - The certified sets `ES8SYM/sets/c6_54pts_9layers`, `ES8SYM/sets/c4_52pts_13layers` and
    `ES8SYM/sets3/c5_56pts_11layers_centre` (centre removed) satisfy m6K8t9, m4K8t13 and m5K8t11 with 0 violated
    clauses. The assignment takes the true orientations, with chain variables at their least fixpoint.
  - Random configurations with t = 3..6: all 15,451 without a convex octagon satisfy the CNF; all 4,032 with one
    violate a chain clause; 0 violations outside the chain family. Each of about 2,086 violations matched a convex
    octagon checked exactly.
  - All 4,668 layer subsets of the certified sets that were tested satisfy their CNFs.
- **Caveat.** For m = 5, 6 and t >= 5, random configurations without a convex octagon are rare. There, the evidence
  comes mainly from the certified sets and their subsets.

## 3. Computations

All runs used CaDiCaL 3.0.1, one core each.

| CNF | m | t | variables | clauses | SHA-256 | result |
|---|---|---|---|---|---|---|
| m6K8t9 | 6 | 9 | 42,728 | 1,040,348 | `467e7119…` | SAT (a real set exists) |
| m5K8t11 | 5 | 11 | 54,767 | 1,630,243 | `4d9a193e…` | SAT (a real set exists) |
| m4K8t13 | 4 | 13 | 57,701 | 1,517,980 | `c8c3a158…` | SAT (a real set exists) |
| m6K8t10 | 6 | 10 | 58,626 | 1,609,785 | `ff10dafb…` | SAT in 7.4 s |
| m5K8t12 | 5 | 12 | 71,523 | 2,354,156 | `10d36965…` | SAT in 17 s |
| m4K8t14 | 4 | 14 | 72,298 | 2,071,625 | `4ddfc22a…` | SAT (GP loop, below) |
| m6K8t11 | 6 | 11 | 78,059 | 2,387,083 | `542c8a3a…` | unknown after 1,500 s; **UNSAT** with Y(1,2) and 32 cubes (`C6UPPER`) |
| m5K8t13 | 5 | 13 | 91,390 | 3,295,617 | `d7bbb743…` | **unknown** after 1,500 s |
| m4K8t17 | 4 | 17 | 130,439 | 4,658,852 | `4843a9e9…` | **unknown** after 1,500 s |

Full hashes are in `CNF_SHA256.txt`. The GP clause sets and the two GP-consistent models are in the local archive
`es8-rot456-2026-11-03` (outside Git). A SAT answer concerns the abstraction only. It is **not** a claim that a point
set exists.

**Grassmann–Plücker refinement.** This adds the 3-term relations [abc][ade] − [abd][ace] + [abe][acd] = 0 lazily, as
sign clauses in the orbit variables. They hold for every configuration in general position, so adding them is sound.
- m6K8t10: after 26 rounds (1,143,808 clauses) the model satisfies all 27,307,560 relations. It is an abstract 6-fold
  chirotope on 60 points that obeys the angular and nesting rules and has no chain of 7.
  - It has not been realized. A hinge-loss fit of the polar linear forms over radii and phases left at best 249 of
    5,710 orbit signs wrong.
  - Annealing (`scout` nest3) seeded from the plain SAT model reached at best 210 convex octagons.
- m4K8t14: after 41 rounds (1,771,040 clauses) the model satisfies all 19,099,080 relations. It is an abstract
  4-fold chirotope on 56 points of the same kind. Not realized either (best fit: 424 of 6,930 orbit
  signs wrong; `logs/realize.txt`).
- m5K8t12: still SAT after 44 rounds (1,804,128 clauses), with violation counts not converging, when stopped.

## 4. Next steps

- Symmetry breaking: reflection in the x-axis keeps theta_0 = 0. For even m it reverses the psi-order, so the unit
  Y(1,2) loses nothing (written out and tested in `C6UPPER` §2). For odd m the unit is H(1), as in `C7UPPER`.
- m = 6: done (`C6UPPER`: Y(1,2) plus a 32-cube split on the phase order of layers 1–4, all proofs checked by both
  checkers).
- m = 5, 4: the same split. For m5K8t13 the base is H(1) plus 64 patterns of the six Y variables on layers 1–4, of which
  24 are consistent; the 40 impossible ones are refuted, and a first run of the 24 consistent ones did not finish
  (see `C6UPPER` §4 when updated).
- More GP rounds at t = L + 1.

## Reproduction

```sh
python3 C7UPPER/gen.py 6 8 11 m6K8t11.cnf          # likewise (5, 8, 13), (4, 8, 17), (6, 8, 10), ...
cd ROT456/tests && CNFDIR=<dir with m6K8t9.cnf, m4K8t13.cnf, m5K8t11.cnf and their .json> python3 -I test_files.py
```
