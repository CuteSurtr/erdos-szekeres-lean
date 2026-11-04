# Fourfold and threefold routes

**Proposals, not completed computations or upper bounds.** The algebraic
separation methods use rotation orbits and can be adapted independently of
whether the convex layers are individual orbits. An adapted encoder still
needs its own soundness review and exact tests.

For fourfold rotation, let `D_ij=dot(z_i,z_j)` and `E_ij=det(z_i,z_j)`.
The coefficients of `det(z_i,R^k z_j)` are

| `k` | `D_ij` | `E_ij` |
|---:|---:|---:|
| 0 | 0 | 1 |
| 1 | 1 | 0 |
| 2 | 0 | -1 |
| 3 | -1 | 0 |

Thus the seventeen-orbit threshold has 289 rational linear lift variables.
Positive zero dependencies give area-identity cuts; negative quadratic
combinations can be checked exactly in the actual 34 seed coordinates.
The Hermitian matrix `D+iE` must also be positive semidefinite and rank one.
This suggests adding the linear/Gram approach alongside the existing
fourfold final-polynomial work. The current sixfold implementations hardcode
their rotation and variable map; they must not be reused unchanged.

For threefold rotation, the analogous lift has 484 variables at 22 orbits.
The more consequential prerequisite is the encoder: radius order can supply
the tangent half-plane used by the chain argument, while nesting must be
removed before any chain simplification. The detailed, explicitly unverified
adaptation and a counterexample to retaining nesting are in
[math_threefold_proposal.md](math_threefold_proposal.md).

In either case, a feasible Gram relaxation is not a point construction.
Rank-one feasibility or a separately verified coordinate set remains
necessary. A local numerical search that fails to find such coordinates is
only search evidence. No fourfold or threefold solver was launched in this
continuation.
