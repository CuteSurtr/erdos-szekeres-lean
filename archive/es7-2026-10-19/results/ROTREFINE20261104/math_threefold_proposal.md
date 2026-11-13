# Proposed threefold encoding by radius order

4 November 2026 (KST).

**Status: proposed encoding; evidence only.** No implementation, CNF generation, solver run, or complete soundness validation has been performed for this proposal. The observations below identify a possible adaptation and the exact assumptions that need review. They do not certify the threefold octagon case.

## Replace convex-layer order with orbit-radius order

**Written argument to review (not refereed).** A threefold configuration is a union of regular triangular rotation orbits, but its convex layers need not be single orbits. Remove a possible centre point. Perturb the orbit radii and phases slightly while preserving every nonzero point-triple orientation. The candidate normalization orders the resulting distinct orbit radii strictly decreasingly, then labels one representative in each 120-degree sector convention. Preserving all point-triple signs preserves general position and convex-octagon-freeness. The small-perturbation argument, including tied radii and generic phase conditions, needs to be written fully for the adapted encoder.

For the threshold case, threefold cardinalities are 0 or 1 modulo 3. Thus a set of at least 65 points has at least 22 noncentral orbits after its centre is removed; the proposed instance is `m=3, K=8, t=22`. The index `i` would mean decreasing **radius rank**, not convex-layer rank.

## Which existing clause families may survive

Locations below refer to the unchanged `C7UPPER/gen.py` source.

- **Phase order and orbit variables:** lines 4–12 and 35–41 describe orbit labeling, orientation orbits, and generic phase order. Their possible reuse concerns regular rotation orbits, not convex-layer nesting. The perturbation and normalization require fresh review for radius ordering.
- **Origin-inside angular rule:** `fam_angle`, lines 233–234. Its geometric rationale is the angular order around the rotation centre, independently of nesting; see docstring lines 38–42.
- **Radial angular rule:** `fam_angle`, lines 235–239, tests `lb<=la` and `lb<=lc`. The proof at lines 43–45 only uses the corresponding inequality `u_b<=u_a,u_c`, where `u=1/r`. Radius-rank labels appear sufficient for this rule. This is different from an inner-polygon condition: the angularly middle point must have at least the other two radii, but the triangles need not be nested.
- **Nesting:** `fam_nest`, lines 254–263, inserts orientation units placing every later orbit inside every earlier polygon. This family is not justified by radius ordering and must be omitted.
- **Chains:** `fam_chain`, lines 272–329, chooses `p=i*m` and all points of ranks at least `i` (lines 276–278). The proposed substitute for the docstring's nesting justification at lines 47–48 is the radius inequality: every other point `q` satisfies `p dot q < |p|^2`. For a smaller-radius orbit this follows from Cauchy–Schwarz; for another point on the same circle it follows from `q!=p`. Hence all such `q` lie in the open tangent half-plane at `p`. The remaining simple-polygon/convex-chain argument at lines 49–53 must be reviewed unchanged in that setting.
- **Capturing octagons:** lines 55–57 choose an outermost layer. The proposed replacement chooses a vertex in a maximum-radius orbit occurring in the octagon and rotates it to `(i,0)`. All other vertices then have radius ranks at least `i`.

**Critical implementation condition.** Do not generate the current CNF and merely delete its nesting units afterward. `fam_nest` writes entries into `forced` at line 263, and chain construction uses `val` at lines 294 and 315 to simplify literals and omit cases. Once the units are removed, those simplifications would no longer have their stated justification. A separate adapter must omit `fam_nest` **before** `fam_chain` is built, retaining only sound angular units in `forced`. The current build sequence calls nesting at line 347 immediately before chains at line 348. Certified source directories must remain unchanged.

## Why nesting really cannot be retained

**Exact computation.** In transformed coordinates `(x,y)` representing the Euclidean point `(x,sqrt(3)*y)`, consider

```
outer: (1,0), (-1/2,1/2), (-1/2,-1/2)
inner-radius orbit: (3/8,3/8), (-3/4,0), (3/8,-3/8).
```

These are two regular triangles of radii 1 and 3/4. All 20 point-triple determinants are nonzero; the minimum absolute transformed determinant is `1/4`. Nevertheless, for the first outer edge and the first inner-radius point, the transformed determinant is `-1/4`, contradicting the corresponding nesting unit `orient(0,1,3)>0`. The point set has only six points and is automatically octagon-free. A sufficiently small phase perturbation preserves the failed nesting inequality and general position while avoiding the phase boundary in this example.

This counterexample rejects retaining the nesting family. It does not validate the rest of the proposed encoding.

## Linear determinant cuts without a layer lemma

**Written identity (not an encoder soundness claim).** For a 120-degree rotation, keep `D_ij=dot(z_i,z_j)` and `E_ij=det(z_i,z_j)/sqrt(3)`. The coefficients of `(2/sqrt(3))*det(z_i,R^k z_j)` are

| `k` | `D_ij` | `E_ij` |
|---:|---:|---:|
| 0 | 0 | 2 |
| 1 | 1 | -1 |
| 2 | -1 | -1 |

This gives integer linear determinant forms in `22^2=484` lift variables for 22 orbits. The positive-dependency certificate argument of `math.md` does not use convex layers or nesting, so it is a candidate source of sound additional constraints once signs are correctly mapped. A feasible lift would still not be a realization.

## Required next checks

Before any solve, write and adversarially review the adapted normalization and chain proof, audit all uses of the old layer index, and check the formula exactly on the certified threefold 61-point configuration after removing its centre and sorting its orbits by radius. Small randomly generated and deliberately nonnested threefold configurations should be compared with a separate brute-force octagon oracle. The known counterexample above must satisfy every retained non-chain clause in the adapter. This work remains open; no threefold theorem is claimed here.
