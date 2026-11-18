# Envelope proof roadmap

This is the written algebraic derivation behind the completed Lean translation in
`WeightedEnvelope.lean`, `TwoSupport.lean`, and `NumericalExample.lean`. See `README.md`
and `data/` for the exact checked source scope and axiom audits. All arguments work in
any linearly ordered field; completeness and the Archimedean property are unnecessary.

## 1. Sufficient certificate

Write the target as `q(t)=s*t+z` and the supports as `L_i(t)=u_i*t+w_i`.
Let `a_i >= 0`, `sum_i a_i=1`, `s <= sum_i a_i*u_i`, and
`z <= sum_i a_i*w_i`. For `t>=0` and any common upper bound `M` for the
support values at `t`,

```
q(t) <= (sum_i a_i*u_i)*t + sum_i a_i*w_i
     = sum_i a_i*(u_i*t+w_i)
     <= sum_i a_i*M
     = M.
```

The first inequality uses nonnegativity of `t`; the second uses nonnegativity
of each weight. The last equality uses exactly the unit-sum hypothesis.
Taking `M` to be the finite maximum proves the requested envelope theorem.
The common-upper-bound version does not need a nonempty-set hypothesis;
the weight hypotheses already rule out an empty support set.

Local Mathlib declarations identified:

- `Finset.sum_le_sum`, from `Algebra.Order.BigOperators.Group.Finset`;
- `Finset.sum_mul`, `Finset.sum_add_distrib`, `mul_add`, and `mul_assoc`;
- `mul_le_mul_of_nonneg_left`, `mul_le_mul_of_nonneg_right`, `add_le_add`;
- `Finset.le_sup'` and `Finset.le_sup'_iff`, from `Data.Finset.Lattice.Fold`.

The primary proof needs no arithmetic tactic import. The completed proof establishes the
weighted-evaluation identity, the common-upper-bound theorem, and the maximum corollary
in that order. Finite lists and local recursive sums/maxima avoid the Finset imports,
which exceeded the resource guard. Every finished declaration has an axiom audit.

## 2. Necessity of at most two supports

Assume a finite nonempty family dominates `q` at every `t>=0`. Subtract the
target coefficients: `d_i=u_i-s`, `e_i=w_i-z`. Thus for each `t>=0` some
`i` has `d_i*t+e_i>=0`.

If some `i` has both `d_i>=0` and `e_i>=0`, a single support suffices.
Otherwise `d_i>=0` implies `e_i<0`.

At `t=0`, some `i0` has `e_i0>=0`, hence `d_i0<0`. Therefore the finite set
`N={i : d_i<0}` is nonempty. Choose `i` maximizing

```
alpha_i = e_i/(-d_i),   alpha = alpha_i.
```

Since `alpha_i0>=0`, also `alpha>=0`. For every `k` with `d_k<0`, the
residual `d_k*t+e_k` is strictly negative whenever `t>alpha`. Every zero-slope
residual is also strictly negative. Apply domination at `alpha+1`: its witness
must have positive slope. Thus `P={j : d_j>0}` is nonempty.

Choose `j` minimizing

```
beta_j = -e_j/d_j,   beta = beta_j.
```

Every positive-slope line has negative height in the no-single-support case,
so `beta>0`. If `alpha<beta`, then `t=(alpha+beta)/2>0` makes every residual
strictly negative: lower-slope lines because `t>alpha`, higher-slope lines
because `t<beta`, and zero-slope lines because their heights are negative.
This contradicts universal domination. Hence `beta<=alpha`.

For the selected lines put `a=-d_i>0`, `b=d_j>0` and
`lambda=b/(a+b)`. Then `0<lambda<1`, and

```
lambda*d_i + (1-lambda)*d_j = 0,
lambda*e_i + (1-lambda)*e_j = a*b/(a+b)*(alpha-beta) >= 0.
```

Adding back the target coefficients gives exact equality of weighted slope
and domination of weighted height. The supports straddle the target slope,
and their original-coordinate weight is
`lambda=(u_j-s)/(u_j-u_i)`.

The completed implementation uses `exists_max_on` and `exists_min_on` for finite lists,
and `exists_mem_of_le_maxFrom` to extract pointwise witnesses. The sign of an affine
function and crossing-time arithmetic are isolated as small helpers. Ordinary checked
proof terms establish the result; no numerical solver verdict is evidence.
`le_envelope_iff_two_supports` combines necessity and sufficiency. Its repeated support
indices and endpoint weights include the single-support case, while
`two_supports_of_no_single` gives the stronger strict-pair conclusion.

## 3. Numerical example

Use `q=(-2,-4)`, `L24=(-3/2,-15/2)`, `L56=(-12,-14)` and
`L57(h)=((h-10)/2,h)`. Define the explicit three-line maximum `F(h,t)`.

At `h=5`, the average of `L24(t)` and `L57(5,t)` is `q(t)+11/4`.
An average of two values is at most their maximum, which is at most `F(5,t)`.
The margin statement is in fact valid for all `t`, although the draft only
requires the requested ray `t>=0`.

Positive witnesses against each single support:

| Support | t | Support value | Target value |
|---|---:|---:|---:|
| L24 | 1 | -9 | -6 |
| L56 | 1 | -26 | -6 |
| L57(5) | 20 | -45 | -44 |

At `h=3`, subtracting each support from the target gives `(7-t)/2`,
`10*t+10`, and `3*t/2-7`. Their simultaneous strict positivity is equivalent
to `14/3<t<7`; on this interval the middle inequality is automatic.
At `t=6`, `F(3,6)=-33/2` and `q(6)=-16`.

No statement here identifies these formal line definitions with terminal
lines of a point configuration. Determinant invariance, five-cap-freeness,
and all Delta-selection claims remain outside this algebra result.
