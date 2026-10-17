# Affine rainbow-four-cycle colorings

Research notes on restricted cases of Erdős problem #810 and an
oscillatory affine-operator estimate over prime fields.

## Main results

Let \(p\) tend to infinity through odd primes. A color \(a\) is a partial
affine map \(x\mapsto ax+\beta(a)\), with one color per nonzero slope.
Assume that the resulting bipartite graph is simple, properly colored,
and every four-cycle is rainbow. Write \(D_a\) for the actual row domain
of color \(a\), and \(m=\sum_a|D_a|\).

1. **Bounded-VC supports.** If the family \(\{D_a\}\) has uniformly
   bounded VC dimension, then \(m=o(p^2)\), with arbitrary intercepts
   \(\beta(a)\). The same conclusion holds when the color–row incidence
   bigraph omits a fixed induced bipartite pattern.
2. **Nearly common supports.** If \(D_a\subseteq X\) and
   \(\sum_a|X\setminus D_a|=o(p^2)\), then \(m=o(p^2)\).
   For polynomial intercepts of fixed degree \(D\ge2\),
   \[
   m\le C_Dp^{19/10}+\sqrt2\,p\sqrt{\sum_a|X\setminus D_a|}.
   \]
3. **Oscillatory affine operators.** For \(s\ne0\) and arbitrary complex
   weights \(|w(a)|\le1\), the operator
   \[
   C_{s,w}f(x)=\sum_{a\ne0}w(a)e_p(s(a^2x+a^3))f(ax+a^2)
   \]
   satisfies \(\|C_{s,w}\|_{2\to2}=O(p^{7/8})\). An exact decomposition
   gives the same bound for the corresponding two-dimensional crossed
   operator.

## Proofs

| Note | Contents |
|---|---|
| [Bounded-VC supports](bounded-vc-supports.md) | Thin limits, finite bracketing, and extraction of nearly complete support rectangles |
| [Common affine supports](common-affine-supports.txt) | Arbitrary intercepts, the affine-energy estimate, group-table reduction, and an explicit common-support rate |
| [Polynomial affine supports](polynomial-affine-supports.txt) | Crossed involutions, Fourier fourth moments, and a power saving |
| [Oscillatory affine operators](oscillatory-affine-operator.txt) | Uniform weighted norm estimate and exact Fourier–character decomposition |

The bounded-VC result uses the common-support theorem. Its spectral
calculation is expanded in the polynomial-support note. The oscillatory
operator proof is self-contained and uses elementary quadratic Gauss
sums. Published inputs and their precise roles are cited in the notes.

## Status

These are analytic research proofs, not Lean-certified results.
Historical novelty has not been established, and external review is
pending. No solution of unrestricted Erdős #810, universal \(o(N^2)\)
bound, or new record is claimed.

The remaining obstacle is controlling arbitrary actual support sets.
A bound for each nonzero Fourier slice does not by itself justify
summing all slices without additional control of their coefficients.
