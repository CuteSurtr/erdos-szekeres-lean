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

1. Connect general convex-subset counts at successive sizes to compatible support
   configurations. The current density theorem counts horizontal cups and caps;
   a bound forcing a convex polygon cannot simply be substituted into that theorem.
   Cyclic support geometry, or an equivalent construction preserving the required
   density and cap budgets, still needs a proof.
2. Prove the two-scale count-ratio argument and its bootstrapped density estimate
   using the same geometric family throughout.
3. Formalize the sharpened entropy estimates, integer rounding, and eventual
   optimization giving the coefficient 8√2/3.
4. A strict improvement needs additional mathematical input beyond this known
   argument. `DyadicModel.two_scales_optimal` already excludes an improvement
   from merely adding more doublings in its explicitly restricted model.

No finite parameter search here proves the final asymptotic coefficient. These
modules establish the product-method infrastructure needed to investigate it.
