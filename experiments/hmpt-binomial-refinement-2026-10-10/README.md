# A finite HMPT counting refinement

The Lean module [`HMPT/BinomialRefinement.lean`](../../ErdosSzekeres/HMPT/BinomialRefinement.lean)
proves a stricter finite counting criterion for **ordinary finite real planar point
sets in general position**. It retains the number of subsets at the initial scale
instead of replacing it by the number of ordered point tuples. The coefficient
`8√2/3` in the HMPT asymptotic theorem is unchanged.

Let `K = 4m+1`, `k = m+1`, `D = 3m−6`, and
`P = supportProductBound (m−3) n * supportProductBound (2m−3) n`.
For an n-gon-free set of N points, after an invertible linear normalization
making x-coordinates distinct, the existing geometric ratio theorem gives

```text
f_K ≤ choose(N,k) N⁶ P
```

where `f_K` counts convex `K`-subsets. For `N > 0` and `m ≥ 1`, this displayed
upper bound is strictly smaller than the previous `N^(m+7) P`.

For `m ≥ 3`, `n ≥ 4`, and an already proved input `ES(K) ≤ M ≤ N`,
`two_scale_binomial_bound` proves `ES(n) ≤ N` whenever

```text
choose(N,k) N⁶ P choose(M,K) < choose(N,K).
```

For powers `M = 2^d` and `N = 2^E`, put `F = floor(log₂(k!))`. If `P ≤ 2^V`,
then `two_scale_factorial_exponential_bound` proves the sufficient criterion

```text
(d+1)K + V < DE + F,       d ≤ E,       2K ≤ E.
```

Consequently the closed exponent is

```text
E_new = max(d, 2K, floor(max(0,(d+1)K + ceil(log₂P) − F)/D) + 1).
```

`twoScaleFactorialExponent_le` proves that this exponent never exceeds the
existing `twoScaleExponent`. `suk_two_scale_factorial_bound` supplies the input
bound using the already formalized finite Suk theorem, leaving only the integer
constraints `m ≥ 3`, `n ≥ 4`, `a ≥ 2`, and `4m+1 ≤ a³`. Thus the final theorem
has no unproved geometric input. All names are in `ErdosSzekeres.HMPT`.

The small [kernel-checked arithmetic example](StrictExponentExample.lean) proves
`twoScaleExponent 3 4 26 = 129` and `twoScaleFactorialExponent 3 4 26 = 128`.
This demonstrates strictness of the formula; it is not a competitive bound for
`ES(4)`. Larger exact Python comparisons in `validation.json` are explicitly
marked as numerical diagnostics, not additional Lean certificates.

## Verification and provenance

The maintained module builds with Lean; its nine theorem roots and the standalone
example depend only on `propext`, `Classical.choice`, and `Quot.sound`. The complete
local output is in [axiom-audit.txt](axiom-audit.txt). The source scan finds no
`sorry`, `admit`, `sorryAx`, or `native_decide` in either new Lean source. Source
hashes and exact commands are recorded in [validation.json](validation.json).

This is a refinement of the repository's finite interface, **not a claim of a new
literature result**. In [HMPT v3, Proposition 3.8](https://arxiv.org/html/1710.11415v3),
the initial-scale estimate is `f_k ≤ N^k`; the earlier Theorem 2.4 already counts
supports by a binomial coefficient. Retaining that factorial information is a
standard counting refinement. [The complete paper](https://arxiv.org/abs/1710.11415)
provides the underlying geometric argument. No improvement to its leading
asymptotic coefficient, extension to pseudo-configurations, or best-known finite
bound is claimed by this artifact.
