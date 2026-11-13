# Exact linear determinant separation for regular hexagons

4 November 2026 (KST). This is a continuation of the sixfold realizability review.

## Necessary linear conditions

**Written proof (reviewed, not refereed).** Let `z_i` be the chosen representative of rotation orbit `i`, and let `R` be counterclockwise rotation by 60 degrees. Introduce real lift variables

```
D_ij = dot(z_i,z_j),                 D_ji = D_ij,
E_ij = det(z_i,z_j)/sqrt(3),         E_ji = -E_ij, E_ii = 0.
```

There are `t(t+1)/2 + t(t-1)/2 = t^2` variables. Elementary rotation formulas give

| `k` | Coefficient of `D_ij` | Coefficient of `E_ij` |
|---:|---:|---:|
| 0 | 0 | 2 |
| 1 | 1 | 1 |
| 2 | 1 | -1 |
| 3 | 0 | -2 |
| 4 | -1 | -1 |
| 5 | -1 | 1 |

The table represents `(2/sqrt(3))*det(z_i,R^k z_j)`. For points `a=R^ka z_i` and `b=R^kb z_j`, use `k=kb-ka mod 6`. Since

```
[abc] = det(a,b) + det(b,c) + det(c,a),
```

every triangle orientation is the sign of an integer linear form in these `t^2` lift variables. The common factor `2/sqrt(3)` is positive. These formulas require only the prescribed Euclidean rotation; they do not require nesting, a phase-order unit, or a bound on the number of convex polygons.

For a proposed orientation sign `sigma_v`, write the corresponding signed linear row as `a_v`. Every real general-position realization must satisfy `a_v dot x > 0` for every row. If positive integers `lambda_v` satisfy

```
sum_v lambda_v * a_v = 0,
```

then the proposed sign pattern is impossible: its weighted sum would be strictly positive and identically zero. The clause negating those finitely many signs is therefore sound. This implication uses the displayed integer certificate directly; it does not depend on an LP solver's infeasibility verdict.

**Limit.** The lift variables are treated as free real numbers during search. Actual dot and cross products satisfy additional quadratic and rank constraints. A feasible lift or failure to find a positive dependency is not a geometric realization.

## Search and exact verification

**Exact computation.** `math_linear.py` and `math_scan.py` search for nonnegative dependencies by solving the normalized dual system `A^T lambda=0`, `sum(lambda)=1`, `lambda>=0`. Numerical LP values select a support. Rational Gaussian elimination then reconstructs weights, clears denominators, and checks the integer residual exactly. No numerical tolerance is used in the retained certificate check.

`tests/verify_linear.py` uses a separate representation: a stored point `(x,y)` means `(x,sqrt(3)*y)`, and rotation is the rational matrix

```
R(x,y) = ((x-3y)/2,(x+y)/2).
```

It expands each affine determinant directly as a polynomial in the seed coordinates, compares it with the advertised lift row, verifies positive integer weights and exact cancellation, and repeats the identity with the inverse rotation. It also binds the required signs to the retained model and checks the encoder's variable map. The separate `tests/check_linear_symbolic.py` check uses the oblique-coordinate matrix `R(u,v)=(-v,u+v)`; its retained logs provide a further polynomial verification without the dot/cross table.

Every proposed two-/three-orbit clause receives an exact test on `ES8SYM/sets/c6_54pts_9layers.pts`. For a three-orbit clause, the test covers `9*8*7 * 6^2 * 2 * 2 * 2 = 145,152` cases: ordered orbit choices, relative index shifts, common direction, global sign reversal, and the original/mirror coordinates. The omitted common index shift is a rotation and preserves every orientation. Each case checks the actual weighted determinant identity as well as satisfaction of the exclusion clause.

## Embedding families

**Written proof (reviewed, not refereed).** An injective orbit map with independent offsets and a common direction,

```
(i,k) -> (f(i), epsilon*k+s_i mod 6),       epsilon in {+1,-1},
```

preserves the class of configurations to which the identity applies. For `epsilon=+1`, absorb each offset into its seed vector. For `epsilon=-1`, use the same identity for the inverse rotation, which is independently checked symbolically. A global reversal of all required signs multiplies the identity by `-1`, so its impossibility is preserved. The orbit injection need not preserve radial order. Arbitrary unrelated sign changes or different direction choices on individual orbits are not justified by this argument.

**Exact computation.** `math_embed_linear.py` checks coefficient cancellation separately for every mapped identity, translates each required sign through the encoder's canonical orientation map, and emits the negated sign pattern. A three-orbit source has `10*9*8 * 6^2 * 2 * 2 = 103,680` checked embeddings before deduplication. The full families and their per-clause embedding records are retained outside Git in the review archive's `math/` directory.

A bounded four-orbit family uses only increasing orbit injections: `binomial(10,4) * 6^3 * 2 * 2 = 181,440` embeddings. This is a sound subset of the full family, with its restriction stated explicitly. Generation streams clause and embedding records. Its source identity is tested on all `9*8*7*6 * 6^3 * 2 * 2 * 2 = 5,225,472` ordered certified-set embeddings.

For sources on five through nine orbits, exhaustive certified-set testing would be unnecessarily large. The same universal polynomial proof applies, but the recorded regression policy is explicitly finite: at least 100 deterministic injective source embeddings, then an original and mirrored exact embedding test for every emitted canonical clause. Families use increasing orbit injections and a bounded deterministic sample of relative shifts, including the source's zero offsets. Both direction and independent global sign choices remain sound for zero identities. The source also passes the separate `tests/check_linear_symbolic.py` checker before it enters the queue, with that output and its hash retained.

**Exact computation.** `model0046`, SHA-256 `03e51ab03e64b7b2c39dece6423ba60851a9647e5ea9c4c62ab2060d721dbf35`, survives every two-, three- and four-orbit linear restriction. A full lift search finds a 56-row integer dependency. Greedy orbit deletion reduces this to a 39-row identity on orbits `3,4,5,6,7,8,9`, maximum weight 34, witness SHA-256 `8c17edc308a483e58202c809833c9abb69242489c348b2682d31fd208798716d`. Its bounded family has 61,440 clauses, with 100 source tests and 122,880 per-clause exact tests; all pass. This shows why full linear search follows the small restrictions before attempting the quadratic method in `math_sdp.md`. A near-zero numerical SDP margin is not an infeasibility or feasibility certificate.

## First retained separators

**Written proof + exact computation.** The following source clauses all have exact positive integer certificates and passed the symbolic and certified-set checks. The variable numbers are for encoder A at sixfold/ten layers.

| Source model | Source orbits | Clause | Largest weight | Distinct family clauses |
|---|---|---|---:|---:|
| Prior `gp_run08` | 1,8,9 | `-2757 -2782 -2793 2795 5697 -5707` | 1 | 103,680 |
| Prior `family_run3` | 0,3,4 | `-795 868 -873 -3838` | 1 | 103,680 |
| Continuation `model0001` | 1,4,7 | `-1587 1654 -2197 -2210 2215 -4564` | 2 | 51,840 |
| Continuation `model0003` | 1,5,9 | `1641 -1642 1692 -2467 -2497` | 2 | 51,840 |

For the first source, the exact identity has six unit-weight terms:

```
+[6,48,49] +[6,50,55] +[6,51,58]
-[6,52,53] -[48,55,56] +[54,55,56] = 0.
```

The forbidden assignment makes all six displayed signed terms strictly positive. The final term has the positive orientation of three consecutive vertices of one regular hexagon; it is kept explicitly in the clause rather than silently using another unit.

**Exact computation, restricted method comparison.** Continuation `model0001`, SHA-256 `72f8c875af61243ab5fba34ab9cd927efd8881ef26992c0bb623cc10b9c4e353`, satisfies all GP sign relations and the formulas checked in the main lane. The retained product-cycle search found no directed cycle in its two-/three-orbit restrictions or their 1,300,220-edge union. The six-row linear certificate nevertheless excludes this same model under the prescribed rotation. This is a concrete case where the linear method succeeds after that bounded graph search fails; no completeness or general dominance claim is made.

The complete growing list of verified templates, injection scopes, exact-test counts, and hashes is in `math_cases.md` and `math_catalog.json`; compact proof records are in `math_witnesses/`.

## Reproduction and operational limits

Run numerical search with the isolated research environment and one-thread settings:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 "$PYTHON" -I -B \
  ROTREFINE20261104/math_scan.py --model "$MODEL" --out "$OUT" --limit 1
python3 -I -B ROTREFINE20261104/tests/verify_linear.py \
  --model "$MODEL" --witness "$WITNESS" --out "$VERIFIED"
python3 -I -B ROTREFINE20261104/math_embed_linear.py \
  --witness "$WITNESS" --verified "$VERIFIED" --out "$FAMILY"
```

HiGHS also receives `threads=1` explicitly. All proof checks use stdlib exact arithmetic. Each retained witness directory contains its model hash, exact weights, coefficient rows, clause, verification result, family hash, and resources. The search over the first full model found a 62-row dependency touching all ten orbits; that exploratory witness is retained, but it was not submitted as a clause family because the compact restrictions provide tested, reusable families.

**Evidence only (observed resources).** The recorded small-restriction searches took about one second each with roughly 100 MB peak RSS. Full family generation stayed below 180 MB peak RSS. The ten-orbit exploratory LP took about nine seconds and about 110 MB. These are observations, not worst-case guarantees.

**Open.** These cuts exclude particular abstract sign patterns. They do not by themselves settle the existence of a real 60-point set or change the bound `54 <= maximum <= 60`. Any stronger conclusion requires the main campaign's remaining solve and certificate checks.
