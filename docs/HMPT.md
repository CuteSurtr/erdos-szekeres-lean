# HMPT 2020 upper bound in Lean

Checkpoint: 2026-10-05. **The final HMPT 2020 asymptotic coefficient is proved
for ordinary real point sets** by `ErdosSzekeres.HMPT.theorem2020`. For every
ε > 0, all sufficiently large n satisfy

    ForcesConvexNGon floor(2^(n + (8√2/3 + ε)√(n log₂ n))) n.

This reproduces the published bound. A strict improvement remains unproved.

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
| `HMPT/ConvexFan.lean` | Canonical projection anchor and ray ordering; uniqueness from the vertex set and count-preserving fan representations |
| `HMPT/FanCounting.lean` | Genuine convex-subset ratio with only the three support-path endpoint choices free |
| `HMPT/TwoScale.lean` | Telescope the ratios at m+1, 2m+1, 4m+1 and combine with convex-subset density; closed finite bound using Suk |
| `HMPT/Entropy.lean` | Factorial-sensitive binomial estimate, common logarithmic budget, closed exponent, and exact natural-floor transfer |
| `HMPT/AsymptoticInput.lean` | Suk's rounded natural input exponent eventually forces the required polygon and has ratio tending to one |
| `HMPT/ScaleLimits.lean` | Rounded square-root parameter, logarithmic ratios, and the induced Suk input exponent limits |
| `HMPT/Asymptotic.lean` | Exact normalized budget identity, positive eventual slack, and the final coefficient 8√2/3 with arbitrary ε > 0 |

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

## General convex subsets and two scales

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

The sharper ratio is now proved as `convex_family_ratio_bound`:

    f_(2r+7) ≤ f_(r+4) N³ B(r,n).

`ConvexFan.vertices_injective` proves that the original projection anchor and
alternating retained vertices uniquely determine their ray-slope ordering.
Counting these choices by actual smaller convex subsets removes the earlier
tuple-count loss. The three powers of N account for the support-path endpoints.

For m ≥ 3, applying the ratio twice gives

    f_(4m+1) ≤ f_(m+1) N⁶ B(m−3,n) B(2m−3,n)
             ≤ N^(m+7) B(m−3,n) B(2m−3,n).

Let K = 4m+1, and let 2^d ≥ K be a verified bound forcing a convex K-gon.
Define P = B(m−3,n) B(2m−3,n). Then `integer_two_scale_bound` proves that
2^E points force a convex n-gon, where

    E = max(d, 2K, floor(((d+1)K + clog₂ P)/(3m−6))+1).

`suk_two_scale_bound` supplies d from the already proved finite Suk theorem.
The ratio estimates concern the actual convex-subset counts of arbitrary real
point sets; coordinate rotation discharges the temporary distinct-x assumption.

## Checked entropy estimate and rounding

`choose_le_four_mul_pow` proves

    choose(N,A) ≤ (4R)^A  whenever N ≤ RA.

The proof uses the exponential-series inequality A^A/A! ≤ exp(A), preserving
the factorial saving. Consequently, each B(r,n) is at most 2 raised to

    (r+1)(n−1) + 2r + (2(n−1)+r) clog₂(4(r+1)).

Both scales together have the simpler checked budget

    P ≤ 2^[3mn + 6m + (4n+3m) H],   H = clog₂(8m) ≤ log₂ m + 4.

This yields the closed exponent `twoScaleEntropyExponent`:

    E_entropy = max(d, 2K,
      n + floor(((d+1)K + 6n + 6m + (4n+3m)H)/(3m−6)) + 1).

`suk_entropy_two_scale_bound` proves the corresponding geometric theorem using
only n ≥ 4, m ≥ 3, a ≥ 2, and K ≤ a³, with

    d = K + a² + clog₂(K+a²)a² + 64(a(a+1)+5).

`real_entropy_two_scale_bound` transfers a sufficient real exponent budget to
the exact threshold floor(2^X), with a unit of slack for exponent rounding.
There are no numerical experiments or unproved geometric assumptions inside
these theorems.

## Checked asymptotic optimization

Let S = sqrt(n log₂ n), fix c > 0, and choose m = ceil(cS). The input exponent
d is ceil(Suk.exponent 6 (4m+1)). Its polygon-forcing property follows from the
fully proved Suk theorem; it is not an assumed asymptotic estimate.
The new limit lemmas establish

    m/S → c,       m/n → 0,
    d/S → 4c,      d/n → 0,
    log₂ m / log₂ n → 1/2.

`budgetRatio_identity` relates the normalized expression exactly to the finite
entropy criterion. After division by n log₂ n, its slack tends to

    3cC − 16c² − 2.

For c = 1/(2 sqrt(2)) and C = 8 sqrt(2)/3 + ε, this limit is positive for
every ε > 0. The proof simultaneously supplies all eventual positivity, size,
and input-bound hypotheses, and uses `real_entropy_two_scale_bound` to retain
the exact floor threshold. Thus `theorem2020 : Theorem2020` has no hypotheses.

The result covers arbitrary finite real point sets in general position. It
does not formalize the paper's pseudo-configuration or convex-body extensions.
The theorem and its dependencies are included in the standard-axiom audit.

## Research beyond the published coefficient

A strict improvement needs additional mathematical input beyond this known
argument. `DyadicModel.two_scales_optimal` excludes an improvement from merely
adding more doublings in its explicitly restricted model. It is not a general
obstruction to other proof strategies.

`MixedCap.mixed_cap_budget_counterexample` also rejects an unconditional mixed
vertical/inner-cap budget: two nonadjacent eight-point caps, with all support
anchors included in a 22-point general-position configuration, can avoid a
convex 16-gon. The largest convex subset has size 15, proved in Lean from exact
triangle and supporting-edge certificates. See [`MIXED_CAPS.md`](MIXED_CAPS.md).
This is a counterexample to a proposed lemma, not an improvement of the bound.
