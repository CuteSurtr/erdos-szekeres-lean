# Exact quadratic negativity separators for sixfold rotation

4 November 2026 (KST). This extends the necessary linear lift in `math.md`.

## A concrete boundary of the linear and product-cycle tests

**Exact computation.** The retained `model0033`, SHA-256 `8b98f35bf949205a9270d94460b02a8e420e1607c5280db84c6f5588a621a9a8`, has a rational assignment to all 100 dot/cross lift variables satisfying all 5,710 strict orientation inequalities and positive decreasing diagonal entries. `math_primal.py` checks every inequality with rational arithmetic. A separate seed-polynomial reconstruction in `tests/check_linear_primal.py` confirms this. Thus no positive zero dependency among these signed linear orientation forms can exclude this model. This is an exact statement about this lift, not a realization.

The particular rational lift is not positive semidefinite: the exact two-orbit Hermitian principal minor for orbits 0,1 is `-590506859853708478/20892261048855742161`. The separate full product graph check also reports no directed cycle in its complete reduced-GP graph; its coverage and validation belong to the main sixfold campaign. Weighted exponent dependencies beyond directed cycles have not been excluded by that graph result.

## Necessary Gram condition and exact certificate

**Written proof (reviewed, not refereed).** For actual Euclidean seeds, the Hermitian matrix `H=D+i*sqrt(3)*E` is a positive-semidefinite complex Gram matrix (indeed rank one). A congruent real matrix is

```
M = [[D, -E], [E, D/3]].
```

Requiring `M >= 0` is therefore necessary. Numerical SDP search maximizes a common strict orientation margin with `trace(D)=1`. The normalization is valid for a nonzero set of seeds. No numerical infeasibility status or eigenvalue is accepted as proof.

The retained certificate is simpler to check than an SDP dual: it gives positive integer weights `lambda_r` and required signs `sigma_r` such that the polynomial

```
P(z) = sum_r lambda_r * sigma_r * [a_r b_r c_r]
```

is negative definite in the seed coordinates. Here the physical seed corresponding to stored `(u_i,v_i)` is `(u_i,sqrt(3)*v_i)`, and the determinant in the checker is the determinant in the stored coordinate plane. Physical determinants differ by the same positive factor `sqrt(3)`.

`quadratic_matrix_twice` is an integer symmetric matrix `Q` satisfying `z^T Q z = 4 P(z)`. The checker expands the affine determinants directly under `R(u,v)=((u-3v)/2,(u+v)/2)` and compares every coefficient with `Q`. It then proves `-Q` positive definite by exact rational Schur complements, with every pivot strictly positive. If all required signs held, every term of `P` would be positive, contradicting `P<0`. Negating the conjunction therefore gives a universal clause for the prescribed counterclockwise Euclidean sixfold action. No nesting, radius order or convex-polygon restriction is used.

`tests/check_sdp_symbolic.py` independently expands the same determinants in the oblique basis `R(u,v)=(-v,u+v)`, verifies the rational basis congruence to `Q`, and checks definiteness by rational elimination.

## Lifting requires coupled reflection and sign reversal

**Written proof (reviewed, not refereed).** For an injective orbit map and offsets, substitute rotated seeds into `P`. This is an invertible coordinate substitution, so negativity is preserved. Reversing all sector directions corresponds to conjugating all seeds and negating every determinant. Consequently a direction reversal is sound only when coupled with a reversal of every required sign. The permitted transformations are `(direction, sign factor)=(+1,+1)` and `(-1,-1)`.

Unlike a zero identity, this proof does not allow an independent global sign flip. That would change `Q` to `-Q`, which is positive definite. The exact checker retains this negative control and verifies the coupled reflection by direct polynomial congruence.

## First compact certificate and regression checks

**Written proof + exact computation.** A full ten-orbit 75-row negative-definite certificate excludes `model0033`. Greedy orbit deletion reduces it to 16 rows on source orbits `1,3,4,7,8`, witness SHA-256 `85ff269f59fd263be8e11a37c015f94dccb88a2354888eb14b09bd5d26e2fe8d`. Its source clause is

```
1635 -2026 2107 2162 -2320 2675 2737 3852
3888 -3911 -4039 4381 -4431 4564 4895 4977
```

`tests/verify_sdp.py` checks 100 deterministic injective embeddings into the exact certified 54-point set, with offsets, both coupled directions/signs, and original/mirrored geometry. The mirror's sector indexing is reversed as well, so its labeled rotation remains counterclockwise. Every weighted sum is strictly negative and every clause is satisfied. These are finite regression tests; universal soundness follows from the polynomial/definiteness proof, not the sample.

`math_embed_sdp.py` emits a bounded family using increasing target orbit injections and 128 deterministic relative-shift patterns. The first family has 64,512 clauses, SHA-256 `763bdd9da2e160230c006bea3c3659701f1b187c3a60bf37e32bfd79483cec05`. Each emitted canonical clause is checked on original and mirrored injective certified-set embeddings, totaling 129,024 further exact tests. The checks also verify the encoder's rotation/parity canonicalization on actual determinants. This is explicitly a partial family, not all injections or all shifts.

## Scope and limits

**Evidence only.** Numerical search uses one-thread Clarabel and the isolated research environment. The five-orbit source solve took about 1.3 seconds and 154 MB; family generation and exact testing took about 4.7 seconds and 103 MB. Numerical statuses labeled `optimal_inaccurate` are retained as search provenance only; all accepted contradictions are exact integer/rational certificates.

**Open.** Positive-semidefinite feasibility would still not prove realization: the Gram rank-one condition remains. These finite exclusions do not settle the 60-point case or change the bound `54 <= maximum <= 60`.

## Final unresolved candidate

**Exact computation.** The final retained `model0090`, SHA-256 `62b5c1d0ba4c9fb6d9b19a65c86d87f427853af388cf65d470dd73cae1f19f21`, has an independently checked rational linear lift satisfying all 5,710 strict orientation inequalities with minimum margin `2/3491` and positive decreasing radii. Its particular lift is not PSD: the exact principal minor for orbits 0,1 is `-940801/12187081`. This proves that zero-identity separation cannot exclude this model and that this particular lift is indefinite; it does not exclude every PSD lift or every geometric realization.

**Evidence only.** The full numerical SDP reported a near-zero negative margin and an inaccurate status. None of the ten nine-orbit deletion probes yielded an exact negative-definite certificate. A bounded diagnostic tested 1,218 distinct rounded integer dual combinations using exact rational nonnegative-pivot elimination, allowing a zero pivot only when its remaining row and column vanish; none was certified negative semidefinite. The observed kernel pattern was not proved and no kernel-constrained follow-up search was run. These failed extractions establish neither PSD feasibility nor infeasibility. No clause was queued for this candidate, and its prescribed geometric realizability remains unresolved at the research cutoff.
