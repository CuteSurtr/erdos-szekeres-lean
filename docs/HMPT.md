# HMPT product-method formalization

Checkpoint: 2026-10-05. The finite product argument below is proved for ordinary
real point sets. **The final HMPT 2020 asymptotic coefficient and a strict
improvement remain unproved.**

The reference is [Holmsen–Mojarrad–Pach–Tardos, final v3, Section 3](https://arxiv.org/pdf/1710.11415).
The implementation reuses the horizontal support paths from the Suk proof.
It accounts explicitly for their endpoints and for small or empty regions.
It does not assert the cyclic pseudo-configuration theorem from the paper.

## Proved dependencies

| Module | Checked result |
| --- | --- |
| `HMPT/Maxima.lean` | Attained longest chain and largest triangle-order antichain; region size is at most their size product |
| `HMPT/ChainCapacity.lean` | Attained facing-cap maxima, binomial chain bound, and adjacent-cap sum strictly less than n under n-gon avoidance |
| `HMPT/AntichainCapacity.lean` | Attained supported-cap maximum, binomial antichain bound, and total inner-cap size at most 2(n−1) by even/odd gluing |
| `HMPT/RegionProduct.lean` | Product bound with all geometric cap budgets derived internally |
| `HMPT/FiniteBound.lean` | Alternating-anchor counting, density, reflection, and rotation turn the product bound into an arbitrary-real-plane theorem |
| `HMPT/ExponentialBound.lean` | Factorial cancellation in the density comparison and a closed integer exponent valid for every positive region count |
| `HMPT/Projective.lean` | Exact projective chart, inverse, general-position preservation, and polygon pullback by four-point convexity |
| `HMPT/ProjectedCaps.lean` | A convex polygon minus its leftmost vertex projects to a horizontal cap, retaining every remaining vertex |
| `HMPT/ConvexCounting.lean` | Count-preserving projection of anchored families and a bound for all convex subsets |
| `HMPT/BootstrapBound.lean` | Bootstrap any checked ES bound through the product method; a closed corollary uses the proved finite Suk bound |

The actual cap witnesses retain their unpadded sizes. Only the binomial
parameters are padded to at least two. Thus adjacent and parity budgets are
proved about real configurations, and padding costs are added afterward.

## Exact finite formula

For integers n ≥ 4 and r ≥ 1, set

    L = 2(r+3)
    M = 2(n−1)+r
    B = 2^((r+1)(n−1)+2r) choose(M+r(n−2), M)
    E = max(4(r+3), floor((2L²+L+1+clog₂ B)/r)+1).

Here clog₂ B is the least integer v such that B ≤ 2^v. The definitions are
`supportProductBound r n` and `productExponent r n`.

`HMPT.integer_product_bound` proves

    ForcesConvexNGon (2 ^ productExponent r n) n.

All geometric assumptions have been discharged: only n ≥ 4 and r ≥ 1 remain.
The statement holds for every such r, so a finite search may choose an efficient
parameter without changing the mathematical theorem.

The more precise `HMPT.finite_product_bound` uses the exact binomial density
inequality rather than the sufficient power estimate. The factorial cancellation
lemma removes the extra L² loss of the earlier coarse Suk extraction estimate;
this is an improvement to the repository's estimates, not to the published bound.

`scripts/product_bound_search.py` searches r = 1,...,128 with exact Python integers
and independently checks the original binomial density inequality for each chosen
parameter. Results for n = 64,128,256,512,1024,2048 are recorded in
`experiments/hmpt-product-2026-10-05.json`. These numerical evaluations are not
separate Lean kernel certificates, and the search does not assert optimality
outside its stated range. The symbolic theorem covering every r is audited.

## Remaining route to the published coefficient

The one-scale general convex-subset bridge is now proved. For the leftmost
vertex a, the chart is

    (x,y) ↦ ((y−a_y)/(x−a_x), −1/(x−a_x)),  x > a_x.

Its denominator is positive on the retained halfplane. The proof verifies the
inverse and orientation formula explicitly, then uses the four-point criterion
to pull a found polygon back to the original real point set. A convex polygon
with anchor a projects to a clockwise cap after removing a. This reuses the
support-path argument without requiring cyclic support geometry.

Writing f_j for the number of convex j-subsets, `convex_family_bound` proves

    f_(2r+7) ≤ N^(r+7) B(r,n)

under n-gon avoidance. `bootstrap_product_bound` combines this with convex-subset
density from **any proved** `ForcesConvexNGon M (2r+7)`. In power form, let
K = 2r+7, suppose K ≤ 2^d and that 2^d points force a convex K-gon, and set

    E_boot = max(d, 2K, floor(((d+1)K+clog₂ B(r,n))/r)+1).

Then `integer_bootstrap_bound` proves that 2^E_boot points force a convex n-gon.
`suk_bootstrap_bound` instantiates the input exponent d with `Suk.cubic_log_bound`,
so it has only integer parameter hypotheses and no assumed ES theorem.

What remains:

1. Retain the actual number of smaller convex subsets when counting alternating
   anchor choices. The target is

       f_(2r+7) ≤ f_(r+4) N³ B(r,n).

   This requires proving that the original projection anchor together with the
   alternating retained vertices determines the relevant fiber. The current
   proof counts these choices more coarsely by N^(r+4).
2. Apply that ratio estimate at sizes m+1, 2m+1, and 4m+1, and combine the
   resulting inequalities with the bootstrapped convex-subset density.
3. Formalize the sharpened entropy estimates, integer rounding, and eventual
   optimization giving the coefficient 8√2/3.
4. A strict improvement needs additional mathematical input beyond this known
   argument. `DyadicModel.two_scales_optimal` already excludes an improvement
   from merely adding more doublings in its explicitly restricted model.

No finite parameter search here proves the final asymptotic coefficient. The
projective construction closes the earlier one-scale counting obstacle; the
two-scale ratio and asymptotic coefficient still require checked proofs.
