# Erdős–Szekeres bounds: a mathematical companion to the Lean proofs

**Status: 10 October 2026.** The closed results are Suk's asymptotic upper
bound, the ordinary real-point specialization of HMPT's improved asymptotic
bound, and $`\mathrm{ES}(8)\le314`$. The assertion $`\mathrm{ES}(8)\le313`$
and an improvement of HMPT's asymptotic coefficient remain unproved here.

This manuscript translates the principal checked declarations into ordinary
mathematics, with their hypotheses and quantifiers retained. Each mathematical
step identifies its Lean declaration or finite certificate schema. Literal
catalogs and long derivations are specified by their archived data and the
soundness theorems explained below; listing every generated proof term is not
necessary to specify their mathematical meaning. The exposition itself is
human-readable documentation, not a separately kernel-checked translation.
The Lean statements and the exact certificate inputs are authoritative.

The intended reader is a mathematician familiar with finite combinatorics and
planar convexity. No rational-coordinate or bounded-grid assumption is made.
The arguments concern convex polygons whose interiors may contain other points.
The [paper correspondence](docs/PAPER_MAP.md) records the differences between
these implementations and the published intermediate lemmas.

- [Definitions and conventions](#a-definitions-and-conventions).
- [Suk and HMPT, with finite bounds and limiting parameters](#s-the-formalized-suk-and-hmpt-bounds).
- [The closed finite octagon theorem](#f-the-finite-octagon-theorem).
- [The residual relaxation and the precise open proposition for 313](#r-the-residual-relaxation-and-the-unresolved-bound-313).
- [Validation and references](#v-validation-and-references).

## A. Definitions and conventions

The ambient plane is $`\mathbb R^2`$, represented by `Point := Fin 2 → ℝ`.
All configurations in the final statements are finite sets, so repeated points
are excluded. A finite set $`P\subset\mathbb R^2`$ is in general position if
no three distinct members are collinear. A finite set $`Q`$ is in convex
position if

```math
  q\notin\mathrm{conv}(Q\setminus\{q\})\qquad(q\in Q).
```

The Lean definition uses Mathlib's `ConvexIndependent`; the displayed
characterization is `ErdosSzekeres.convexPosition_iff` in
[Basic.lean](ErdosSzekeres/Basic.lean).

Write $`\mathsf F(N,n)`$ for the assertion that every finite general-position
set $`P\subset\mathbb R^2`$ with $`\vert P\vert \ge N`$ contains a subset $`Q`$ of
cardinality exactly $`n`$ in convex position. This is precisely
`ErdosSzekeres.ForcesConvexNGon N n` in
[Definitions.lean](ErdosSzekeres/Definitions.lean). There is no requirement
that $`\mathrm{conv}(Q)`$ contain no other points of $`P`$.
The exact-cardinality formulation $`\vert P\vert =N`$ is equivalent, by
`forcesConvexNGon_iff_exact`. Also, $`\mathsf F(N,n)`$ implies
$`\mathsf F(M,n)`$ whenever $`N\le M`$, by `ForcesConvexNGon.mono`.

The usual notation $`\mathrm{ES}(n)\le N`$ abbreviates $`\mathsf F(N,n)`$.
The code formulates the problem through $`\mathsf F`$, rather than a separately
defined minimum $`\mathrm{ES}(n)`$. In particular, its proposition
`ErdosSzekeresConjecture` is

```math
  \forall n\in\mathbb N,\quad n\ge3\Longrightarrow
  \mathsf F(2^{n-2}+1,n).
```

The customary equality $`\mathrm{ES}(n)=2^{n-2}+1`$ additionally uses the
classical lower-bound construction, which is not part of that Lean definition
or a lower-bound formalization claimed here. For $`n=8`$, the conjectured
threshold is $`65`$.

Throughout the following statements, $`\log`$ denotes $`\log_2`$. For a
nonnegative real number $`x`$, $`\lfloor x\rfloor_{\mathbb N}`$ denotes its
natural-number floor. Integer divisions are floor divisions, and a subtraction
in a natural-number expression is truncated at zero. For positive integers
$`u`$, `Nat.clog 2 u` is $`\lceil\log u\rceil`$ and `Nat.log 2 u` is
$`\lfloor\log u\rfloor`$.

## S. The formalized Suk and HMPT bounds

**Theorem S.1 (Suk bound).** There is an integer $`n_0\ge3`$ such that, for every integer
$`n\ge n_0`$,

```math
 \mathsf F\!\left(
   \left\lfloor 2^{\,n+6n^{2/3}\log n}\right\rfloor_{\mathbb N},n
 \right).
 \tag{S}
```

This is `ErdosSzekeres.Suk.theorem2016` in
[Suk/Asymptotic.lean](ErdosSzekeres/Suk/Asymptotic.lean), with the exact
predicate and threshold defined in
[Suk/Statement.lean](ErdosSzekeres/Suk/Statement.lean).
The theorem has no extraction, coloring, or arithmetic-certificate hypothesis.

**Theorem S.2 (HMPT bound for ordinary real point sets).** For every real $`\varepsilon>0`$
there is an integer $`n_0\ge3`$ such that, for every integer $`n\ge n_0`$,

```math
 \mathsf F\!\left(
  \left\lfloor
   2^{\,n+(8\sqrt2/3+\varepsilon)\sqrt{n\log n}}
  \right\rfloor_{\mathbb N},n
 \right).
 \tag{H}
```

This is `ErdosSzekeres.HMPT.theorem2020` in
[HMPT/Asymptotic.lean](ErdosSzekeres/HMPT/Asymptotic.lean);
[HMPT/Statement.lean](ErdosSzekeres/HMPT/Statement.lean) defines
`publishedCoefficient := 8 * Real.sqrt 2 / 3` and makes the quantifier order
$`\forall\varepsilon>0\,\exists n_0\,\forall n\ge n_0`$ explicit.
In particular, the statement does not set $`\varepsilon=0`$.

Both are eventual upper bounds. Neither declaration provides the finite
claim obtained by substituting $`n=8`$ without verifying its eventual
hypotheses. The separately formalized octagon bound does not change the
coefficient in (H). The scope is ordinary finite subsets of $`\mathbb R^2`$;
HMPT's pseudo-configurations and convex-body extensions are not formalized
by these declarations.

### S.1. Finite geometric and arithmetic steps for (S)

The implementation uses finite horizontal support paths. For
$`\omega(a,b,c)=\det(b-a,c-a)`$, a cap frame $`(a,b,c,d)`$ has negative
orientation on each of its four increasing triples. Its open support region
is

```math
 \{p:\ \omega(a,b,p)<0,\quad \omega(b,c,p)>0,\quad
             \omega(c,d,p)<0\}.
```

These are `Suk.CapFrame` and `Suk.CapFrame.spike` in
[SpikeGeometry.lean](ErdosSzekeres/Suk/SpikeGeometry.lean).
`Suk.ClockwiseAnchors (k+3)` consists of a sequence with negative orientation
on every increasing triple; its consecutive four-point windows determine
$`k`$ frames. Horizontal order is an explicit strict-monotonicity hypothesis
at the intermediate support-path theorems, not a hypothesis of (S) or (H).

The finite support theorem supplies the following implication. Let
$`P`$ be in general position, let all $`k+3`$ horizontally ordered anchors
belong to $`P`$, and let $`Q_i\subseteq P`$ lie in the $`i`$-th support
region. If

```math
 n\ge4,\quad K,b\ge3,\quad n\le rK,\quad n\le tb,\quad
 t(r+1)\le k
```

and every region satisfies

```math
 |Q_i|>2^{n+K-4}\binom{n+b-4}{n-2},
```

then $`P`$ contains a convex $`n`$-gon. This is
`Suk.ClockwiseAnchors.finite_support_bound` in
[FiniteSupport.lean](ErdosSzekeres/Suk/FiniteSupport.lean).
The proof constructs the triangle order in each region and uses its
chain/antichain dichotomy. Consecutive large chains are treated by supported
cap growth and adjacent gluing; separated large antichains supply compatible
supported caps whose union is convex. The support sequence itself provides
the adjacency and separation hypotheses used by those gluing results.

The extraction/counting argument and a change of coordinates discharge the
support-path hypotheses for arbitrary $`P`$. Their finite consequence is
`Suk.finite_logarithmic_bound` in
[IntegerParameters.lean](ErdosSzekeres/Suk/IntegerParameters.lean): under the
same integer conditions and $`n+b\le2^H`$,

```math
 \mathsf F\bigl(2^{\,n+K+Hb+64(k+5)},n\bigr).
 \tag{S1}
```

The extraction loss here is $`64(k+5)`$. It is a proved replacement estimate;
the paper's literal intermediate extraction constant is not being asserted.
The closed finite parameter choice $`K=b=a^2`$, $`r=t=a`$,
$`k=a(a+1)`$ gives, for $`n\ge4`$, $`a\ge2`$, $`n\le a^3`$,

```math
 \mathsf F\bigl(2^{D_S(n,a)},n\bigr),\qquad
 D_S(n,a)=n+a^2+a^2\lceil\log(n+a^2)\rceil+64\bigl(a(a+1)+5\bigr).
 \tag{S2}
```

This is `Suk.cubic_log_bound`.

For completeness, the final comparison in (S) retains explicit sufficient
conditions:

```math
 n\ge4,\qquad n^{1/3}\ge4,\qquad \log n\ge100.
 \tag{S3}
```

Put $`x=n^{1/3}`$, $`a=\lceil x\rceil`$, and
$`H=\lceil\log(n+a^2)\rceil`$. The proof establishes
$`n\le a^3`$, $`a^2\le2x^2`$, $`a^2\le n`$,
$`H\le\log n+2`$, and $`a(a+1)+5\le3a^2`$. Consequently

```math
 D_S(n,a)-n
 \le (H+193)a^2
 \le2(\log n+195)x^2
 \le6n^{2/3}\log n.
```

The integer power $`2^{D_S(n,a)}`$ is therefore at most the natural floor in
(S). `Suk.integer_parameters_fit_exponent` proves the parameter comparison;
`Suk.coefficient_six_bound` proves (S) under (S3). Divergence of
$`n^{1/3}`$ and $`\log n`$ then yields `Suk.theorem2016`.

The dependency sequence is
`finite_support_bound` → `finite_density_bound` →
`finite_exponential_bound` → `finite_logarithmic_bound` →
`cubic_parameter_bound` → `coefficient_six_bound` → `theorem2016`.
The full finite density theorem is in
[Suk/FiniteBound.lean](ErdosSzekeres/Suk/FiniteBound.lean), and the power
estimate is in
[Suk/ExponentialBound.lean](ErdosSzekeres/Suk/ExponentialBound.lean).
The intermediate arrows suppress proved counting and coordinate lemmas;
they do not represent additional assumptions.

### S.2. The finite counting interface for (H)

Let $`P`$ be a finite set in general position, let $`c_j(P)`$ count its convex
$`j`$-element subsets, and let
$`N=\vert P\vert `$. This is the cardinality of `Suk.convexSubsets P j` in
[ExtractionCounting.lean](ErdosSzekeres/Suk/ExtractionCounting.lean).
If $`j\le M\le N`$ and $`\mathsf F(M,j)`$, double counting yields

```math
 \binom Nj\le c_j(P)\binom Mj.
 \tag{D}
```

The declaration is `Suk.convex_subsets_density`; the inequality uses integer
multiplication, without division or an implicit rounding convention.

Define

```math
 B(r,n)=2^{(r+1)(n-1)+2r}
       \binom{2(n-1)+r+r(n-2)}{2(n-1)+r},
 \qquad
 \Pi(m,n)=B(m-3,n)B(2m-3,n).
 \tag{P}
```

These are `HMPT.supportProductBound` in
[RegionProduct.lean](ErdosSzekeres/HMPT/RegionProduct.lean) and
`HMPT.twoScaleProduct` in
[TwoScale.lean](ErdosSzekeres/HMPT/TwoScale.lean).
The geometric product bound applies to actual support regions. Attained
chain and antichain maxima give their size-product estimates; adjacent-cap
and even/odd separated-cap budgets control the vertical and horizontal
parameters. In particular, both path endpoints and the padding of small
capacities appear in $`B`$, rather than being discarded as implicit losses.

The convex-fan construction and projective coordinate change give

```math
 c_{2(r+3)+1}(P)\le
 c_{r+4}(P)\,N^3 B(r,n)
 \tag{R}
```

whenever $`n\ge4`$, $`P`$ is in general position with distinct first
coordinates, and $`P`$ avoids a convex $`n`$-gon. This is
`HMPT.convex_family_ratio_bound` in
[FanCounting.lean](ErdosSzekeres/HMPT/FanCounting.lean).
The counting uses actual smaller convex subsets. Projective preservation and
transfer back to the original real configuration are proved in
[Projective.lean](ErdosSzekeres/HMPT/Projective.lean),
[ProjectedCaps.lean](ErdosSzekeres/HMPT/ProjectedCaps.lean), and
[ConvexFan.lean](ErdosSzekeres/HMPT/ConvexFan.lean).

Apply (R) at $`r=m-3`$ and $`r=2m-3`$, with $`m\ge3`$. Direct multiplication
of the two inequalities gives

```math
 c_{4m+1}(P)\le c_{m+1}(P)N^6\Pi(m,n).
 \tag{T}
```

This is `HMPT.convex_two_scale_ratio_bound`. Bounding
$`c_{m+1}(P)\le N^{m+1}`$ and combining (T) with (D) proves
`HMPT.two_scale_bound`: for integers $`m\ge3`$, $`n\ge4`$, and
$`4m+1\le M\le N`$,

```math
 \mathsf F(M,4m+1),\qquad
 N^{m+7}\Pi(m,n)\binom M{4m+1}<\binom N{4m+1}
 \quad\Longrightarrow\quad\mathsf F(N,n).
 \tag{T1}
```

This last statement no longer assumes distinct first coordinates: a proved
linear change of coordinates supplies them. The linear-path ratio argument
is the implementation's replacement for the paper's cyclic alternative; it
is not a claim that the original intermediate proposition has been
formalized verbatim.

### S.3. Entropy budget and the coefficient $`8\sqrt2/3`$

[Entropy.lean](ErdosSzekeres/HMPT/Entropy.lean) proves

```math
 \Pi(m,n)\le
 2^{\,3mn+6m+(4n+3m)\lceil\log(8m)\rceil},\qquad m\ge3,
 \tag{E1}
```

using the elementary binomial estimate
$`\binom NA\le(4R)^A`$ when $`N\le RA`$.
The theorem `HMPT.real_entropy_two_scale_bound` supplies the exact rounding
interface. Let $`m,n,d\in\mathbb N`$, $`X\in\mathbb R`$, and assume

```math
 m\ge3,\quad n\ge4,\quad
 \mathsf F(2^d,4m+1),\quad 4m+1\le2^d,
```

```math
 d+1\le X,\qquad 2(4m+1)+1\le X,
```

and

```math
 (d+1)(4m+1)+3mn+6m+(4n+3m)(\log m+4)
   <(3m-6)(X-1).
 \tag{E2}
```

Then $`\mathsf F(\lfloor2^X\rfloor_{\mathbb N},n)`$.
The proof uses $`E=\lfloor X\rfloor_{\mathbb N}`$ and
$`X-1\le E`$; thus the unit loss in (E2) accounts explicitly for rounding.

Set

```math
 L_n=\log n,\qquad S_n=\sqrt{nL_n},\qquad
 m_n=\lceil cS_n\rceil_{\mathbb N},\qquad
 d_n=\left\lceil
  (4m_n+1)+6(4m_n+1)^{2/3}\log(4m_n+1)
 \right\rceil_{\mathbb N}
```

for a fixed real $`c>0`$. The definitions are `HMPT.asymptoticScale`,
`roundedScale`, and `scaleInputExponent`. Suk's theorem implies
$`\mathsf F(2^{d_n},4m_n+1)`$ eventually.
[AsymptoticInput.lean](ErdosSzekeres/HMPT/AsymptoticInput.lean) and
[ScaleLimits.lean](ErdosSzekeres/HMPT/ScaleLimits.lean) prove

```math
 \frac{m_n}{S_n}\longrightarrow c,\qquad
 \frac{d_n}{S_n}\longrightarrow4c,\qquad
 \frac{\log m_n}{L_n}\longrightarrow\frac12,\qquad
 \frac{m_n}{n},\frac{d_n}{n}\longrightarrow0.
```

For $`X_n=n+CS_n`$, define the exact slack in (E2) by

```math
\begin{aligned}
 \Delta_n(c,C)={}&(3m_n-6)(n+CS_n-1)\\
 &-\bigl((d_n+1)(4m_n+1)+3m_nn+6m_n
             +(4n+3m_n)(\log m_n+4)\bigr).
\end{aligned}
```

`HMPT.budgetRatio_identity` identifies the implemented normalized budget with
$`\Delta_n(c,C)/(nL_n)`$, once $`n\ge2`$, and
`HMPT.normalizedBudget_tendsto` proves

```math
 \frac{\Delta_n(c,C)}{n\log n}\longrightarrow
 3cC-16c^2-2.
 \tag{E3}
```

Consequently every choice with $`c>0`$ and positive limiting slack yields
$`\mathsf F(\lfloor2^{n+C\sqrt{n\log n}}\rfloor_{\mathbb N},n)`$
eventually. This is `HMPT.eventual_bound_of_positive_slack`.
Taking $`c=1/(2\sqrt2)`$ and $`C=8\sqrt2/3+\varepsilon`$ makes the limit
$`3c\varepsilon>0`$, which proves (H).

The exact algebraic identity

```math
 3cC-16c^2-2
  =3c(C-8\sqrt2/3)-(4c-\sqrt2)^2
```

is separately proved as `HMPT.leading_slack_identity` in
[ParameterBarrier.lean](ErdosSzekeres/HMPT/ParameterBarrier.lean).
It shows that a positive limiting slack at some fixed $`c>0`$ is possible
if and only if $`C>8\sqrt2/3`$. This concerns the explicit budget (E2),
not a lower bound for $`\mathrm{ES}(n)`$ or an obstruction to other arguments.

### S.4. Exact binomial and factorial refinements

The following are supplementary finite improvements of the implemented
counting criterion; they do not improve (H)'s asymptotic coefficient.
Retain $`c_{m+1}(P)\le\binom N{m+1}`$ in (T), and put

```math
 T_{\rm bin}(N,m,n)=\binom N{m+1}N^6\Pi(m,n).
```

Then, for $`m\ge3`$, $`n\ge4`$, $`4m+1\le M\le N`$,

```math
 \mathsf F(M,4m+1),\qquad
 T_{\rm bin}(N,m,n)\binom M{4m+1}<\binom N{4m+1}
 \quad\Longrightarrow\quad\mathsf F(N,n).
 \tag{B1}
```

This is `HMPT.two_scale_binomial_bound` in
[BinomialRefinement.lean](ErdosSzekeres/HMPT/BinomialRefinement.lean).
The same file proves
$`T_{\rm bin}(N,m,n)\le N^{m+7}\Pi(m,n)`$, with strict inequality for
$`N>0`$ and $`m\ge1`$. This is a strict improvement of the counting
expression, not by itself a statement of a new best numerical Erdős–Szekeres
bound.

For a closed integer criterion, let

```math
 K=4m+1,\quad D=3m-6,\quad
 V=\lceil\log\Pi(m,n)\rceil,\quad
 A=(d+1)K+V,\quad F=\lfloor\log((m+1)!)\rfloor,
```

and define

```math
 E_0=\max\left\{d,2K,\left\lfloor\frac A D\right\rfloor+1\right\},
\qquad
 E_!=\max\left\{d,2K,
  \left\lfloor\frac{\max(A-F,0)}D\right\rfloor+1\right\}.
 \tag{B2}
```

Here $`m\ge3`$, so $`D>0`$. The definitions are
`HMPT.twoScaleExponent` and `HMPT.twoScaleFactorialExponent`.
If $`n\ge4`$, $`K\le2^d`$, and $`\mathsf F(2^d,K)`$, then

```math
 \mathsf F(2^{E_!},n),\qquad E_!\le E_0.
 \tag{B3}
```

The declarations are `HMPT.integer_two_scale_factorial_bound` and
`HMPT.twoScaleFactorialExponent_le`.

The factorial credit follows from the exact inequality
$`(m+1)!\binom N{m+1}\le N^{m+1}`$. More generally, if
$`\Pi(m,n)\le2^V`$, $`d\le E`$, $`2K\le E`$, and

```math
 (d+1)K+V<DE+\lfloor\log((m+1)!)\rfloor,
 \tag{B4}
```

then $`\mathsf F(2^E,n)`$, under the same $`m,n,K`$ and input-bound
hypotheses. This is `HMPT.two_scale_factorial_exponential_bound`.
One multiplies the binomial count by $`(m+1)!`$, compares the resulting
powers of two, uses $`2^{\lfloor\log((m+1)!)\rfloor}\le(m+1)!`$, and cancels
the positive factorial. Applying the integer division identity to
$`\max(A-F,0)`$ establishes (B4) at $`E=E_!`$.

There is also a uniform strict comparison under one explicit condition.
[FactorialSaving.lean](ErdosSzekeres/HMPT/FactorialSaving.lean) proves

```math
 2^{3m-6}\le(m+1)!\quad(m\ge3),
```

so $`F\ge D`$. It also proves $`d<E_0`$. If $`2K<E_0`$, the counting term
in (B2) is therefore strictly larger than both auxiliary terms, and subtracting
at least $`D`$ from its numerator gives $`E_!<E_0`$. Thus
`HMPT.integer_two_scale_bound_one_bit_smaller` establishes

```math
 \mathsf F(2^{E_0-1},n)
 \tag{B5}
```

whenever $`m\ge3`$, $`n\ge4`$, $`K\le2^d`$,
$`\mathsf F(2^d,K)`$, and $`2K<E_0`$. This halves the previous sufficient
power-of-two threshold in the stated parameter range. It is a comparison
between two finite interfaces in this repository, with no priority claim.

The auxiliary input in (B3) can be discharged by (S2). Specifically,
`HMPT.suk_two_scale_factorial_bound` takes only the integer hypotheses
$`m\ge3`$, $`n\ge4`$, $`a\ge2`$, $`4m+1\le a^3`$, and substitutes
$`d=D_S(4m+1,a)`$. No unproved geometric input remains in that specialization.

### S.5. Declaration correspondence

This table identifies the statements used above. Names in the last column
are fully qualified after prefixing `ErdosSzekeres.`.

| Mathematical content | Lean file | Declaration |
| --- | --- | --- |
| General position, convex position, $`\mathsf F(N,n)`$ | [Definitions](ErdosSzekeres/Definitions.lean) | `GeneralPosition`, `ConvexPosition`, `ForcesConvexNGon` |
| Convex-hull characterization; exact cardinality | [Basic](ErdosSzekeres/Basic.lean) | `convexPosition_iff`, `forcesConvexNGon_iff_exact` |
| (S), with exact coefficient and floor | [Suk/Asymptotic](ErdosSzekeres/Suk/Asymptotic.lean) | `Suk.theorem2016` |
| Support-region finite implication | [Suk/FiniteSupport](ErdosSzekeres/Suk/FiniteSupport.lean) | `Suk.ClockwiseAnchors.finite_support_bound` |
| (S1), (S2) | [Suk/IntegerParameters](ErdosSzekeres/Suk/IntegerParameters.lean) | `Suk.finite_logarithmic_bound`, `Suk.cubic_log_bound` |
| (S3) and exponent comparison | [Suk/Asymptotic](ErdosSzekeres/Suk/Asymptotic.lean) | `Suk.integer_parameters_fit_exponent`, `Suk.coefficient_six_bound` |
| (H), including every positive epsilon | [HMPT/Asymptotic](ErdosSzekeres/HMPT/Asymptotic.lean) | `HMPT.theorem2020` |
| (D) | [Suk/ExtractionCounting](ErdosSzekeres/Suk/ExtractionCounting.lean) | `Suk.convex_subsets_density` |
| Geometric product bound $`B`$ | [HMPT/RegionProduct](ErdosSzekeres/HMPT/RegionProduct.lean) | `HMPT.support_product_bound` |
| (R) | [HMPT/FanCounting](ErdosSzekeres/HMPT/FanCounting.lean) | `HMPT.convex_family_ratio_bound` |
| (T), (T1) | [HMPT/TwoScale](ErdosSzekeres/HMPT/TwoScale.lean) | `HMPT.convex_two_scale_ratio_bound`, `HMPT.two_scale_bound` |
| (E1), exact floor bridge (E2) | [HMPT/Entropy](ErdosSzekeres/HMPT/Entropy.lean) | `HMPT.twoScaleProduct_le_common_entropy`, `HMPT.real_entropy_two_scale_bound` |
| (E3), positive-slack consequence | [HMPT/Asymptotic](ErdosSzekeres/HMPT/Asymptotic.lean) | `HMPT.budgetRatio_identity`, `HMPT.normalizedBudget_tendsto`, `HMPT.eventual_bound_of_positive_slack` |
| Fixed-scale optimization identity | [HMPT/ParameterBarrier](ErdosSzekeres/HMPT/ParameterBarrier.lean) | `HMPT.leading_slack_identity`, `HMPT.positive_leading_slack_iff` |
| (B1), (B3), (B4) | [HMPT/BinomialRefinement](ErdosSzekeres/HMPT/BinomialRefinement.lean) | `HMPT.two_scale_binomial_bound`, `HMPT.integer_two_scale_factorial_bound`, `HMPT.two_scale_factorial_exponential_bound` |
| (B5) | [HMPT/FactorialSaving](ErdosSzekeres/HMPT/FactorialSaving.lean) | `HMPT.integer_two_scale_bound_one_bit_smaller` |

The proof architecture is faithful to these Lean declarations, not a claim of
verbatim coverage of every intermediate result in the papers. Suk's extraction
is replaced by a finite counting argument with the explicit loss above. HMPT's
cyclic statements are replaced where needed by finite support paths, retained
endpoint terms, and the two-step convex-subset count. The final real-point
bounds (S) and (H) are closed theorems. The
[paper correspondence](docs/PAPER_MAP.md) records which original statements are
replaced or outside the formalized scope. These asymptotic proofs do not
import the omission-search experiments or the separate octagon certificates.

## F. The finite octagon theorem

**Theorem F.1 (closed real-plane statement).** Let $`S\subset\mathbb R^2`$ be
finite, with no three distinct points collinear. If $`\vert S\vert \ge314`$, there is a
subset $`T\subseteq S`$ such that $`\vert T\vert =8`$ and every point of $`T`$ is a vertex
of $`\mathrm{conv}(T)`$. Thus $`ES(8)\le314`$.

In Lean this is
`ErdosSzekeres.Omission.forces_convex_octagon_314 : ForcesConvexNGon 314 8`.
The declaration `ErdosSzekeres.Omission.convex_octagon_of_card_ge_314` expands
the conclusion into an eight-element subset with Mathlib's
`ConvexIndependent ℝ` predicate. Both are in
[FinalCover314B61FusedR31Fused.lean](experiments/omission-global-assembly-2026-10-10/FinalCover314B61FusedR31Fused.lean).
The theorem has no hypothesis concerning coordinates being rational, a solver
certificate being valid, or a combinatorial assignment being realizable.
It concerns ordinary convex octagons; other points of $`S`$ may lie inside
their convex hulls. No assertion of optimality or priority is made.

The proof below separates the real-geometric reduction, finite geometric
inequalities, exact arithmetic exclusion, and final composition. The ranks
used in each induced configuration are computed within that configuration;
their witnesses are not taken from a larger set.

### F.1. Configurations, paths, and actual rank states

**Definition F.2 (ordered configuration and chains).** Put

```math
 [a,b,c]=(b_x-a_x)(c_y-a_y)-(b_y-a_y)(c_x-a_x).
```

An ordered configuration of size $`n`$ is a map
$`p:\{0,\ldots,n-1\}\to\mathbb R^2`$ such that $`p_i^x<p_j^x`$ whenever
$`i<j`$, and $`[p_i,p_j,p_k]\ne0`$ whenever $`i<j<k`$.
A $`k`$-cup is a strictly increasing sequence of $`k`$ indices on whose
increasing triples this determinant is positive; a $`k`$-cap has negative
determinants instead. These are the precise predicates
`Configuration`, `Configuration.HasCup`, and `Configuration.HasCap` in
[Realization.lean](ErdosSzekeres/Omission/Realization.lean).
The ambient real-set predicates are defined in
[Definitions.lean](ErdosSzekeres/Definitions.lean).

For an increasing list it is equivalent to require the appropriate sign on
consecutive triples. The implication from consecutive to all triples uses
real geometry. For $`a_x<b_x<c_x<d_x`$, the identities

```math
\begin{aligned}
(c_x-b_x)[a,b,d]
  &=(d_x-b_x)[a,b,c]+(b_x-a_x)[b,c,d],\\
(c_x-b_x)[a,c,d]
  &=(d_x-c_x)[a,b,c]+(c_x-a_x)[b,c,d]
\end{aligned}
```

preserve either common strict sign. Induction gives closure under taking
subsequences. The declarations `PlanarChains.positive_four`, `negative_four`,
and `cup_all` prove this step in
[PlanarChains.lean](ErdosSzekeres/Omission/PlanarChains.lean).
The actual-path conversions `Configuration.endingPath_hasCup` and
`endingPath_hasCap` use the same geometric transitivity. In particular, an
eight-cup gives a convex octagon by `ListGeometry.hasNCup_octagon` in
[ListGeometry.lean](ErdosSzekeres/Omission/ListGeometry.lean).

**Definition F.3 (attained ranks).** For $`u<v`$, write
$`E_-(u,v)`$ and $`E_+(u,v)`$ for the maximum lengths of actual caps and cups
ending with the exact pair $`(u,v)`$. Write $`F_-(u,v)`$ for the maximum length
of an actual cap starting with that pair and remaining in the same finite
configuration. The pair itself is a path of length two, so these maxima
exist. The inductive predicates are `ActualRanks.EndingPath` and
`ResidualRanks.StartingPath`; their maxima and attainment theorems are
`ActualRanks.rank`, `ActualRanks.rank_attained`, `ResidualRanks.rank`, and
`ResidualRanks.rank_attained` in
[ActualRanks.lean](ErdosSzekeres/Omission/ActualRanks.lean) and
[ResidualRanks.lean](ErdosSzekeres/Omission/ResidualRanks.lean).

For $`u<v<w`$, appending or prepending the third point gives

```math
[p_u,p_v,p_w]\lt0
 \Longrightarrow E_-(u,v)\lt E_-(v,w),\quad F_-(v,w)\lt F_-(u,v).
\tag{F.1a}
```

```math
[p_u,p_v,p_w]\gt0
 \Longrightarrow E_+(u,v)\lt E_+(v,w).
\tag{F.1b}
```

These are `ActualRanks.rank_growth` and `ResidualRanks.rank_growth`.
They concern attained lengths, rather than freely assigned numerical ranks.

**Definition F.4 (balanced and residual hypotheses).** A balanced
configuration has no seven-cap, no seven-cup, and no convex octagon. A
residual configuration has no six-cap, no convex octagon, and no junction.
A junction is an actual six-cup ending at a vertex $`u`$, together with an
actual five-cap starting at $`u`$, both wholly inside the configuration.
This is `Subsets.JunctionOn` and its negation `NoJunctionOn` in
[Subsets.lean](ErdosSzekeres/Omission/Subsets.lean). In particular, the
no-junction condition does not merely prohibit a chosen numerical pair of
rank values.

For balanced configurations define

```math
d_B(u,v)=\bigl(E_-(u,v)-1,E_+(u,v)-1\bigr)\in\{1,\ldots,5\}^2.
\tag{F.2}
```

For residual configurations define instead

```math
d_R(u,v)=\bigl(6-F_-(u,v),E_+(u,v)-1\bigr)
 \in\{1,\ldots,4\}\times\{1,\ldots,6\}.
\tag{F.3}
```

The bounds follow by shortening an attained forbidden chain if a rank were
too large. For the residual cup coordinate, octagon avoidance excludes an
eight-cup. Formulas (F.1a–b) imply, for either label system $`d`$,

```math
[p_u,p_v,p_w]\lt0\Longrightarrow d_1(u,v)\lt d_1(v,w).
\tag{F.4a}
```

```math
[p_u,p_v,p_w]\gt0\Longrightarrow d_2(u,v)\lt d_2(v,w).
\tag{F.4b}
```

The corresponding declarations are `ActualRanks.labels`,
`ActualRanks.balanced_label_bounds`, `ActualRanks.labels_increasing`,
`ResidualRanks.labels`, `ResidualRanks.label_bounds`, and
`ResidualRanks.labels_increasing`.

**Lemma F.5 (incoming state separation).** In the appropriate positive label
grid, define the incoming down-set of vertex $`v`$ by

```math
I(v)=\{z:\exists u<v,\ z_1\le d_1(u,v),\ z_2\le d_2(u,v)\}.
```

For every $`u<v`$,

```math
d(u,v)\in I(v)\setminus I(u).
\tag{F.5}
```

Consequently distinct vertices have distinct incoming states.

*Proof.* Membership in $`I(v)`$ is witnessed by $`u`$. If the same label
belonged to $`I(u)`$, some $`t<u`$ would have both coordinates of $`d(t,u)`$
at least those of $`d(u,v)`$. The triple $`(t,u,v)`$ is either a cap or a
cup; either possibility contradicts the appropriate strict inequality in
(F.4a–b). Thus (F.5) holds, and it separates the two states. This is
`StateInterface.incoming_admissible` and `StateInterface.states_distinct` in
[StateInterface.lean](ErdosSzekeres/Omission/StateInterface.lean). The
specialized injectivity results are `ActualRanks.balancedState_injective`
and `ResidualStates.state_injective`. ∎

**Proposition F.6 (the two literal state universes).** A balanced incoming
state is represented by its nonincreasing column heights

```math
5\ge f_1\ge f_2\ge\cdots\ge f_5\ge0.
```

There are $`\binom{10}{5}=252`$ such profiles. A residual state is represented
by

```math
6\ge f_1\ge f_2\ge f_3\ge f_4\ge0,
\qquad f_1<6\ \text{or}\ f_2=6.
\tag{F.6}
```

There are $`\binom{10}{4}-\binom83=210-56=154`$ such profiles. The residual
literal catalog appends a fifth, zero coordinate to each four-column profile.
Both configurations therefore have injective maps into their respective
ordered catalogs.

*Proof.* The height at column $`a`$ is the maximum second coordinate of an
incoming pair whose first coordinate is at least $`a`$, taking zero when
there is no such pair. Heights are nonincreasing, and positive cell membership
is exactly the corresponding height inequality. In the residual case the
label $`(1,6)`$ is impossible: it would give an attained outgoing five-cap
from $`(u,v)`$ and an attained incoming seven-cup ending with $`(u,v)`$.
Removing the last vertex of the cup leaves a six-cup ending at $`u`$, hence a
forbidden junction. If $`f_1=6`$, attainment of that height must therefore
come from a label with first coordinate at least two, giving $`f_2=6`$.
The excluded profiles have first height six and three remaining heights
between zero and five, explaining the subtraction of $`\binom83`$.
Injectivity follows from Lemma F.5. ∎

The height construction and its characterization are
`ActualRanks.column`, `incoming_iff_column`, and `balancedState` in
[BalancedStates.lean](ErdosSzekeres/Omission/BalancedStates.lean), and
`ResidualStates.column`, `incoming_iff_column`, `top_cell_constraint`, and
`state` in [ResidualStates.lean](ErdosSzekeres/Omission/ResidualStates.lean).
The crucial attained-rank argument is `ResidualRanks.forbidden_label`.
The Lean implementation checks completeness and the precise order of the
literal catalogs, rather than relying on the informal binomial count:
`BalancedCatalog.catalog_length`, `profiles_covered`, `ownerIndex_profile`,
and `ownerIndex_injective` in
[BalancedCatalog.lean](ErdosSzekeres/Omission/BalancedCatalog.lean), with
the analogous declarations in
[ResidualCatalog.lean](ErdosSzekeres/Omission/ResidualCatalog.lean).
The real-point maps are `Configuration.balancedOwner` and
`Configuration.residualOwner`; the latter and its injectivity theorem are in
[ResidualRealization.lean](ErdosSzekeres/Omission/ResidualRealization.lean).

### F.2. Geometric omission inequalities

**Definition F.7 (holes and a row system).** For a configuration whose owner
map takes values in a catalog $`V`$, let $`O\subseteq V`$ be its image and put
$`h_i=1`$ for $`i\notin O`$, $`h_i=0`$ for $`i\in O`$. By injectivity,

```math
\sum_{i\in V}h_i+n=|V|.
\tag{F.7}
```

An omission row is a pair $`(S_r,d_r)`$, with $`S_r\subseteq V`$ and
$`d_r\in\mathbb N`$, asserting

```math
h(S_r):=\sum_{i\in S_r}h_i=|S_r\setminus O|\ge d_r.
\tag{F.8}
```

Every actual configuration satisfies the rows proved below. The converse,
that every Boolean solution is realized by points in the plane, is not used
or asserted.

**Lemma F.8 (cycle rows).** Suppose a list of distinct catalog states
$`s_0,\ldots,s_{k-1}`$ has the following checked property: for each
$`i<j<\ell`$, any actual owners of $`s_i,s_j,s_\ell`$, in that order, have
positive orientation. In a configuration with no convex octagon, at most
seven listed states are occupied. Thus the support of the list has demand
$`k-7`$, with natural subtraction understood when $`k<7`$.

*Proof.* If eight listed states were occupied, take them in list order and
select their distinct actual owners. Every increasing triple in this order
has positive orientation. `hasConvexNGon_of_positive_cycle` then supplies an
actual convex octagon. Subtract the resulting bound of seven occupied states
from the support cardinality. ∎

The checked property is finite and stronger than an unsupported assertion
about a polygon order. For catalog states $`A,B`$, every actual pair label
lies in the directed difference $`I(B)\setminus I(A)`$ by (F.5). The computed
rectangle bounding this difference either is empty, ruling out that
chronological order, or contains every allowable pair label. For each of the
six possible chronological orders of three owners, the checker verifies
either an empty required difference or a coordinate separation forcing the
desired sign via (F.4a–b). To force a chronological cup it checks that the
second pair's maximum first coordinate is at most the first pair's minimum
first coordinate; to force a cap it checks the analogous second-coordinate
inequality. Orientation changes sign under an odd permutation, so all six
checks together prove positive orientation in the specified list order.
Catalog index order, list order, and chronological owner order are distinct.

This is exactly `CycleSigns.Safe`, `CheckTriple`, and
`checked_triple_positive` in
[CycleSigns.lean](ErdosSzekeres/Omission/CycleSigns.lean), using
`BoundingBoxes.computedTable_valid` and the corresponding residual table.
The geometric conclusions are `Configuration.checked_cycle_capacity`,
`checked_cycle_hole_bound`, and `list_cycle_hole_bound` in
[CycleGeometry.lean](ErdosSzekeres/Omission/CycleGeometry.lean), and
`Configuration.residual_checked_cycle_capacity`,
`residual_checked_cycle_hole_bound`, and `residual_list_cycle_hole_bound` in
[ResidualCycleGeometry.lean](ErdosSzekeres/Omission/ResidualCycleGeometry.lean).

**Lemma F.9 (residual block rows).** Let $`S`$ be a checked residual support
with a compression $`\kappa`$ of all admissible pair labels on that support
into $`\{1,2\}`$. Suppose every actual cap triple in the support satisfies
$`\kappa(d(u,v))<\kappa(d(v,w))`$. Then at most 22 states of $`S`$ can be
occupied in an octagon-free residual configuration. Consequently
$`h(S)\ge \vert S\vert -22`$.

*Proof.* A four-cap would give three consecutive pair values strictly
increasing in $`\{1,2\}`$, which is impossible. Baek's finite theorem says
that any 23 points of the resulting ordered combinatorial configuration
contain a four-cap or an eight-vertex cap/cup boundary. The geometric
boundary theorem converts the latter alternative to a convex octagon on
the same real points. Thus the occupied owner set has size at most 22. ∎

The finite certificate consists of active label cells and a threshold at
each cup coordinate. Its compression is one or two according as the cap
coordinate is at most that threshold or exceeds it. `BlockCompression.pairsOK`
checks that every possible directed-difference label is active;
`growthOK` checks the strict increase at the shared middle state. The
declarations `no_four_cap_of_rank2` in
[BlockCompression.lean](ErdosSzekeres/Omission/BlockCompression.lean),
`Baek.four_cap_or_eight_gon` in
[Baek.lean](ErdosSzekeres/Omission/Baek.lean),
`BaekGeometry.geometric_capacity22` in
[BaekGeometry.lean](ErdosSzekeres/Omission/BaekGeometry.lean), and
`BlockGeometry.block_hole_bound` in
[BlockGeometry.lean](ErdosSzekeres/Omission/BlockGeometry.lean) carry out
these steps. The boundary's convexity is proved by supporting affine
functionals in `BoundaryGeometry.boundary_polygon` in
[BoundaryGeometry.lean](ErdosSzekeres/Omission/BoundaryGeometry.lean).

**Proposition F.10 (the complete original geometric row systems).** Every
balanced configuration satisfies the 2,685 literal balanced rows, comprising
1,584 cycle supports of size eight and demand one, 780 of size nine and
demand two, and 321 of size ten and demand three. Every residual
configuration satisfies the 1,187 literal residual rows: 974 cycles of size
eight and demand one, 190 of size nine and demand two, and 23 blocks of size
28 and demand six.

*Proof.* Each cycle list is checked against Lemma F.8, including injectivity,
every triple, support equality, and demand equality. Each block is checked
against Lemma F.9, including its compression conditions and support equality.
Finite row-index case splits cover the entire catalogs. ∎

The exact universal conclusions are `OmissionBalanced.all_geometric_rows`
in `BalancedRows.lean`, preserved in
[balanced-rows-sources.tar.gz](experiments/omission-global-assembly-2026-10-10/balanced-rows-sources.tar.gz),
and `OmissionResidual.all_geometric_rows` in `ResidualAllGeometry.lean`,
preserved in
[blocks-sources.tar.gz](experiments/omission-residual-geometry-2026-10-09/blocks-sources.tar.gz).
For example, the residual conclusion is

```math
\forall r\in\{0,\ldots,1186\},\quad
d_r\le |S_r\setminus O_R(c)|
```

for every real `Configuration` satisfying exactly the residual hypotheses
of Definition F.4. Equation (F.7), Booleanity, and all rows are combined in
`OmissionBalanced.feasible_holes` in
[BalancedBudgets.lean](experiments/omission-global-assembly-2026-10-10/BalancedBudgets.lean)
and `OmissionResidual.feasible_holes` in
[ResidualReduction.lean](experiments/omission-residual-geometry-2026-10-09/ResidualReduction.lean).

### F.3. Exact arithmetic certificates and rounded cuts

All quantities in this subsection are integers. Write $`x_+=\max(x,0)`$;
Lean's subtraction on natural numbers implements this truncation.

**Lemma F.11 (weighted capacity inequality).** Suppose
$`h:V\to\{0,1\}`$ satisfies $`h(S_r)\ge d_r`$ for every row. Choose
nonnegative integer weights $`w_r`$, and define

```math
L_i=\sum_{r:i\in S_r}w_r,
\qquad D=\sum_r w_rd_r.
```

For every nonnegative integer capacity $`C`$,

```math
D\le\sum_i L_ih_i
 \le C\sum_i h_i+\sum_i(L_i-C)_+.
\tag{F.9}
```

*Proof.* Multiply each row by its weight and transpose the finite sum.
For each Boolean $`h_i`$,
$`L_ih_i\le Ch_i+(L_i-C)_+`$; summing proves the second inequality. ∎

This is `OmissionCertificates.weighted_capacity_bound` in
[OmissionCertificates.lean](ErdosSzekeres/OmissionCertificates.lean).
In particular, a strict inequality
$`Cb+\sum_i(L_i-C)_+<D`$ excludes a hole vector of total at most $`b`$.
The corresponding theorem is `OmissionCertificates.excludes_budget`.

**Proposition F.12 (rounded cover cut).** Fix a prospective support
$`T\subseteq V`$, a target $`q\ge1`$, and weights on already valid rows.
Set

```math
E_T=\sum_{i\in T}(L_i-C)_++\sum_{i\notin T}L_i.
```

If

```math
C(q-1)+E_T<D,
\tag{F.10}
```

then every Boolean vector satisfying the old rows satisfies $`h(T)\ge q`$.

*Proof.* The same pointwise bound inside $`T`$, and $`L_ih_i\le L_i`$
outside it, yield $`D\le Ch(T)+E_T`$. If the integer $`h(T)`$ were less
than $`q`$, it would be at most $`q-1`$, contradicting (F.10). ∎

For $`C>0`$, this is the integer rounding step behind
$`h(T)\ge\lceil(D-E_T)/C\rceil`$. The proof never rounds a floating-point
objective. It checks the exact strict inequality (F.10), using
`OmissionCertificates.weighted_subset_capacity_bound` and
`rounded_cover_cut` in
[CoverCuts.lean](ErdosSzekeres/Omission/CoverCuts.lean).

For a concrete certificate, the first balanced added row, row 2685, has
support

```math
T=\{136,154,174,178,188,189,194,203,208,209,216,218,220,228\}.
```

It adds original rows 150, 112, and 111, each with weight one and demand one.
Their union is $`T`$; every column load is at most two. Thus $`D=3`$,
$`C=2`$, and $`E_T=0`$. The exact inequality $`2(2-1)<3`$ gives demand two
on $`T`$. The literal inputs and integer margin are in
[balanced-v2-cuts.json](experiments/omission-cover-certificates-2026-10-10/balanced-v2-cuts.json).

There are 446 balanced and 1,108 residual added cuts. Each recorded parent row
precedes the derived row, so induction along the finite dependency order
justifies the entire augmentation. The source modules
[BalancedCoverCutsV2.lean](experiments/omission-cover-certificates-2026-10-10/BalancedCoverCutsV2.lean)
and [ResidualCoverCutsV2.lean](experiments/omission-cover-certificates-2026-10-10/ResidualCoverCutsV2.lean)
prove `BalancedCoverCutsV2.all_rows` and `ResidualCoverCutsV2.all_rows`.
Their premises are Booleanity and the original row system; the cuts add no
geometric hypothesis. The augmented systems contain 3,131 balanced and 2,295
residual rows.

**Proposition F.13 (conditioned leaf certificate).** At a branch, let
$`M`$ be the indices fixed missing, $`Z`$ the indices fixed occupied, and
$`F=V\setminus(M\cup Z)`$. A feasible vector has $`h_i=1`$ on $`M`$,
$`h_i=0`$ on $`Z`$, and total at most $`b`$. If $`\vert M\vert >b`$, no such vector
exists. Otherwise, any weighted rows satisfying

```math
C(b-|M|)+\sum_{i\in F}(L_i-C)_++\sum_{i\in M}L_i<D
\tag{F.11}
```

exclude the branch.

*Proof.* Fixed missing indices already use $`\vert M\vert `$ holes. After transposing
the weighted rows,

```math
D\le\sum_{i\in M}L_i+\sum_{i\in F}L_ih_i
 \le\sum_{i\in M}L_i+C(b-|M|)+\sum_{i\in F}(L_i-C)_+,
```

contradicting (F.11). If both values were fixed at one index, the branch
would already be inconsistent. ∎

The general implementation first replaces a row by support
$`S_r\setminus(M\cup Z)`$ and residual demand
$`(d_r-\vert S_r\cap M\vert )_+`$. `sum_after_fixing` proves the exact decomposition
of its row sum. `conditioned_excludes_budget` and
`conditioned_excludes_of_full_load` prove the clipped-demand and original-load sufficient
tests for this argument in
[OmissionCertificates.lean](ErdosSzekeres/OmissionCertificates.lean).
The production fused leaves use the original-load test, written without
subtracting whole sums:

```math
C(b-|M|)+\sum_{i\in V}(L_i-C)_++\sum_{i\in M}L_i
 <D+\sum_{i\in M\cup Z}(L_i-C)_+.
\tag{F.12}
```

**Definition F.14 (exclusion tree).** A node contains either an over-budget
check, a weighted leaf as above, or a split on an index $`i`$. Its zero child
adds $`i`$ to $`Z`$, and its one child adds $`i`$ to $`M`$. Both children
must be excluded. Since a natural number bounded above by one is zero or
one, induction on the tree proves exclusion at its root. An empty root
context therefore excludes every Boolean solution of the row system with
at most $`b`$ holes. There is no pending or oracle case in this proof rule.

The general statements are `CertificateTree.check_sound`,
`CertificateTree.excludes_of_check`, and `split_excludes` in
[OmissionCertificates.lean](ErdosSzekeres/OmissionCertificates.lean).
The large production proofs instantiate the same leaf and split lemmas in
separate modules, rather than evaluating one enormous recursive Boolean
term. Their archived JSON has a `root`, a `hole_budget`, and a `nodes` array;
a branch records `vertex`, `zero`, and `one`, while a weighted leaf records
its integer `capacity` and sparse `[row, weight]` entries. Every descendant
theorem retains its inherited missing and occupied context.

**Lemma F.15 (packed column verification).** For a base $`B>1`$, encode a row
by $`R_r=\sum_{i\in S_r}B^i`$. Suppose $`\sum_r w_r<B`$, every proposed
column coefficient $`c_i<B`$, and

```math
\sum_i c_iB^i=\sum_r w_rR_r.
\tag{F.13}
```

Then $`c_i=L_i`$ for every $`i`$.

*Proof.* The right side equals $`\sum_iL_iB^i`$ by rearrangement, and
$`L_i\le\sum_rw_r<B`$. Uniqueness of base-$`B`$ digits gives the result.
The formal induction first takes both sides modulo $`B`$, then cancels the
equal lowest digit and a positive factor $`B`$. ∎

This is `pack_injective_of_lt`, `load_eq_of_packed`, and
`load_eq_of_sparse_packed` in
[OmissionPacking.lean](ErdosSzekeres/OmissionPacking.lean).
The generated helper `fused_sparse_packed_excludes` checks in one conjunction
the base bound, total weight bound, digit bounds, packed equality, and strict
margin (F.12). It then applies `sparse_list_conditioned_excludes`. Sparse
storage and Horner evaluation change the representation of the calculation,
not its mathematical premise. The helper is embedded in each archived
`Catalog.lean`; its generator is
[omission_fused_export.py](scripts/omission_fused_export.py).

**Theorem F.16 (the two certified arithmetic exclusions).** For the literal
augmented balanced system, no Boolean vector satisfies every row and
$`\sum_i h_i\le61`$. For the literal augmented residual system, no Boolean
vector satisfies every row and $`\sum_i h_i\le31`$.

*Proof.* The complete balanced tree contains 22,318 weighted leaves and
22,317 splits, with packing base 524,288. The residual tree contains 50,945
weighted leaves and 50,944 splits, with packing base 262,144. Both roots have
empty missing and occupied contexts. Every finite leaf computation is
checked using the Lean kernel, and the split lemmas compose them to the
empty-context exclusions. ∎

The declarations are `OmissionBalancedCover61Fused.excludes_budget` in
`BalancedCover61FusedProof/Root.lean` and
`OmissionResidualCover31Fused.excludes_budget` in
`ResidualCover31FusedProof/Root.lean`. The sources and trees are preserved as
[balanced proof sources](experiments/omission-cover-certificates-2026-10-10/balanced-61-fused-lean-sources.tar.gz),
[balanced tree](experiments/omission-cover-certificates-2026-10-10/balanced-61-fused-tree.json.gz),
[residual proof sources](experiments/omission-cover-certificates-2026-10-10/residual-31-fused-lean-sources.tar.gz),
and [residual tree](experiments/omission-cover-certificates-2026-10-10/residual-31-fused-tree.json.gz).
The exact augmented source hashes are
`acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72`
and `c5bc49d588791a6a43e9deba3c4f01af59cf12b781037e69cffb5c2f7735ac61`,
respectively. Numerical discovery records and an export-time `lean_checked`
flag do not establish Theorem F.16; the separate complete kernel records do.

**Proposition F.17 (population bounds).** Every balanced real configuration
has at most 190 points. Every residual real configuration has at most 122
points.

*Proof.* The finite bridges check equality of both supports and demands:
the first 2,685 balanced rows are exactly the original geometric rows, and
the remaining 446 are exactly the proved balanced cuts; the first 1,187
residual rows and remaining 1,108 cuts satisfy the analogous identities.
Hence a hole vector supplied by Proposition F.10 satisfies the augmented
system. Theorem F.16 and integrality give at least 62 balanced holes or
32 residual holes. Using (F.7),

```math
n_B\le252-62=190,\qquad n_R\le154-32=122.
\tag{F.14}
```

∎

The literal identities are `base_catalog_matches` and `cut_catalog_matches`
in [BalancedCover61FusedBridge.lean](experiments/omission-global-assembly-2026-10-10/BalancedCover61FusedBridge.lean)
and [ResidualCover31FusedBridge.lean](experiments/omission-global-assembly-2026-10-10/ResidualCover31FusedBridge.lean).
Their `all_cover_rows` and `exclusion_transfer` theorems discharge the
arithmetic-to-geometric catalog connection. The general population maps are
`OmissionBalanced.balanced_bound_of_hole_budget` and
`OmissionResidual.residual_bound_of_hole_budget`; a rejected budget $`b`$
gives bounds $`251-b`$ and $`153-b`$, respectively, using natural subtraction.
The final closed declarations are
`ErdosSzekeres.Omission.balanced_population_190` and
`ErdosSzekeres.Omission.residual_population_122` in the same file as
Theorem F.1. Their types are exactly `Partition.BalancedBound 190` and
`Partition.ResidualBound 122`, whose universally quantified geometric
hypotheses are those of Definition F.4.

### F.4. Projective reduction, partition, and final composition

**Proposition F.18 (one-point projective reduction).** Every nonempty finite
general-position set $`S\subset\mathbb R^2`$ with no convex octagon gives an
actual ordered configuration $`c`$ of size $`\vert S\vert -1`$, with no seven-cap and
no convex octagon.

*Proof.* First apply an invertible linear map making all abscissae distinct.
Let $`a`$ be the unique leftmost transformed point. All remaining points lie
in $`x>a_x`$. On this half-plane apply

```math
\Phi_a(x,y)=\left(\frac{y-a_y}{x-a_x},-\frac1{x-a_x}\right).
\tag{F.15}
```

The map is injective there. Its first coordinates are distinct because equal
ray slopes from $`a`$ would make three original points collinear. Thus its
image can be ordered as a `Configuration`. General position is preserved;
the determinant identity is

```math
[\Phi_a(p),\Phi_a(q),\Phi_a(r)]
=-\frac{[p,q,r]}{(p_x-a_x)(q_x-a_x)(r_x-a_x)}.
\tag{F.16}
```

An octagon in the chart transfers to an octagon among the original non-root
points. A seven-cap in increasing chart order, together with $`a`$, also
gives a convex octagon: triples not containing the root acquire positive
orientation by (F.16), and triples containing the root acquire positive
orientation from the strictly increasing ray slopes. Both alternatives
contradict avoidance. Exactly one original point was deleted. ∎

The precise conclusion `exists_cap_free_chart` retains
`IsRootDeletionChart S c`, an explicit relation through the invertible linear
map, root deletion, and (F.15), in addition to the cardinality and avoidance
claims. See `root_cap_polygon`, `exists_projective_chart`, and
`exists_cap_free_chart` in
[ProjectiveTransfer.lean](ErdosSzekeres/Omission/ProjectiveTransfer.lean).
Formula (F.15) is `HMPT.projectFrom` and (F.16) is
`HMPT.orient_projectFrom` in
[HMPT/Projective.lean](ErdosSzekeres/HMPT/Projective.lean).

**Proposition F.19 (minimum-slope partition).** Let $`c`$ be an ordered
configuration with $`n\ge2`$, no seven-cap, and no convex octagon. Its index
set partitions into $`H\sqcup R`$, where the induced configuration on $`H`$
is balanced and the induced configuration on $`R`$ is residual. In
particular $`n=\vert H\vert +\vert R\vert `$.

*Proof.* For each vertex $`u`$, choose a distinct vertex $`m(u)`$ attaining
the minimum slope among all segments from $`u`$. Such a vertex exists by
finiteness. Put

```math
U=\{u:u<m(u)\},\qquad L=\{u:m(u)<u\}.
```

These sets are disjoint and cover the indices. Minimum slope and nonzero
orientation give two extension rules: a cap whose last point is in $`U`$
extends to its right-hand minimum-slope neighbor; a cup whose first point
is in $`L`$ extends to its left-hand minimum-slope neighbor. Consequently
$`U`$ has no six-cap and $`L`$ has no seven-cup.

Let $`G\subseteq U`$ be the junction vertices witnessed wholly inside $`U`$,
and set

```math
H=L\cup G,\qquad R=U\setminus G.
\tag{F.17}
```

The residual part has no six-cap, being a subset of $`U`$, and no junction:
a junction in $`R`$ would also be one in $`U`$, placing its vertex in
$`G`$. Both parts inherit octagon avoidance, and $`H`$ inherits seven-cap
avoidance.

It remains to exclude a seven-cup in $`H`$. Its first vertex $`s`$ cannot
belong to $`L`$, since the left extension would give an eight-cup. Its last
vertex $`t`$ cannot belong to $`G`$: extend the outgoing five-cap at that
junction to a six-cap; the sign at the join either extends the given
seven-cup to an eight-cup or prepends its penultimate point to that six-cap,
giving a seven-cap. Hence $`s\in G`$ and $`t\in L`$. At $`s`$ there is an
incoming six-cup and an outgoing six-cap, the latter obtained by extending
the outgoing five-cap in $`U`$. Its second point $`q`$ lies in $`U`$, so
$`q\ne t`$. The geometric three-chain lemma forbids precisely these three
chains: an incoming six-cup ending at $`s`$, an outgoing six-cap beginning
$`(s,q)`$, and an outgoing seven-cup from $`s`$ to $`t\ne q`$, in a
configuration with no seven-cap and no octagon. Its proof uses the
four-point sign identities and cup/cap boundary geometry to produce one of
those forbidden configurations. This eliminates the remaining seven-cup.
Equation (F.17) is a disjoint partition, proving the cardinality identity. ∎

The minimum-slope choice and extension rules are `MinimumSlope.MinNeighbors`,
`exists_min_neighbors`, `cap_to_right`, and `cup_from_left` in
[MinimumSlope.lean](ErdosSzekeres/Omission/MinimumSlope.lean).
The sets in (F.17) are `SlopePartition.junctions`, `balancedPart`, and
`residualPart` in
[SlopePartition.lean](ErdosSzekeres/Omission/SlopePartition.lean).
The precise three-chain statement is `ThreeChain.three_chain` in
[ThreeChain.lean](ErdosSzekeres/Omission/ThreeChain.lean); it imposes only
the specified endpoint exception, without assuming unrelated chains are
disjoint. `Partition.balanced_no_seven_cup` and `Partition.exists_partition`
in [Partition.lean](ErdosSzekeres/Omission/Partition.lean) prove the
remaining avoidance and the full partition statement. All restrictions use
`Subsets.restrict`, which enumerates exactly the chosen real-point subset.

**Proof of Theorem F.1.** Suppose $`S`$ avoids convex octagons. The empty
case is immediate. Otherwise Proposition F.18 gives a cap-free chart with
$`\vert S\vert =n+1`$. If $`n\le1`$, the desired avoiding-set bound is immediate.
If $`n\ge2`$, apply Proposition F.19 and then Proposition F.17:

```math
|S|=|H|+|R|+1\le190+122+1=313.
```

Therefore $`\vert S\vert \ge314`$ forces a convex octagon. ∎

The general composition theorem is
`Partition.forces_of_population_bounds`: for natural numbers $`B,R`$ with
$`1\le B+R`$, a proved `BalancedBound B` and `ResidualBound R` imply
`ForcesConvexNGon (B + R + 2) 8`. Its avoiding-set form is
`Partition.avoiding_card_le_of_population_bounds`, giving
$`\vert S\vert \le B+R+1`$. Both are in
[PopulationBounds.lean](ErdosSzekeres/Omission/PopulationBounds.lean).
One added point accounts for the deleted root, and the other for the strict
forcing threshold. Instantiating $`B=190`$ and $`R=122`$ gives the exact
closed declaration in Theorem F.1.

### F.5. Recorded kernel validation and correspondence

The table reports preserved successful Lean 4.24.0 checks; it is not a claim
that the entire large proof was recompiled while writing this note. Source
archives contain Lean text and mathematical data, not compiled objects.
Every cited final audit uses only `propext`, `Classical.choice`, and
`Quot.sound`. The mathematical dependencies are the checked declarations;
solver outputs and Python replay are supplementary discovery and provenance
records.

| Mathematical statement | Lean declaration or family | Recorded validation |
| --- | --- | --- |
| Original balanced geometric rows, Proposition F.10 | `OmissionBalanced.all_geometric_rows`; 84 row blocks and aggregate | [85-module complete record](experiments/omission-global-assembly-2026-10-10/balanced-rows-kernel-check.json) |
| Original residual cycles and blocks, Proposition F.10 | `OmissionResidual.all_nonblock_rows`, `all_geometric_rows` | [39 cycle modules](experiments/omission-residual-geometry-2026-10-09/cycles-kernel-check.json) and [24 block/composition modules](experiments/omission-residual-geometry-2026-10-09/blocks-kernel-check.json), both complete |
| All 446 rounded balanced cuts, Proposition F.12 | `BalancedCoverCutsV2.all_rows` | [Complete cut check](experiments/omission-cover-certificates-2026-10-10/balanced-v2-cuts-kernel-check.json) |
| All 1,108 rounded residual cuts, Proposition F.12 | `ResidualCoverCutsV2.all_rows` | [Complete cut check](experiments/omission-cover-certificates-2026-10-10/residual-v2-cuts-kernel-check.json) |
| Balanced exclusion of at most 61 holes, Theorem F.16 | `OmissionBalancedCover61Fused.excludes_budget`; 22,318 weighted leaves | [504 modules: catalog, 502 parts, root](experiments/omission-cover-certificates-2026-10-10/balanced-61-fused-kernel-check.json), complete |
| Residual exclusion of at most 31 holes, Theorem F.16 | `OmissionResidualCover31Fused.excludes_budget`; 50,945 weighted leaves | [1,218 modules: catalog, 1,216 parts, root](experiments/omission-cover-certificates-2026-10-10/residual-31-fused-kernel-check.json), complete |
| Literal support/demand transfer and population bounds, Proposition F.17 | Both fused bridges; `balanced_population_190`, `residual_population_122` | Included in the [complete eight-module final assembly record](experiments/omission-global-assembly-2026-10-10/global-cover-314-check.json) |
| Closed real-point octagon theorem, Theorem F.1 | `forces_convex_octagon_314`, `convex_octagon_of_card_ge_314` | Same final record; [explicit axiom output](experiments/omission-global-assembly-2026-10-10/global-cover-314-axioms.txt) |

The final profile pins the arithmetic exports, cut transfers, row counts,
and budgets in
[profile-balanced61-fused-v2-residual31-fused-v2.json](experiments/omission-global-assembly-2026-10-10/profile-balanced61-fused-v2-residual31-fused-v2.json).
The exact profile matters: the completed 314 proof uses the 2,295-row residual
system and rejects budget 31. Later 2,469-row and 2,598-row investigations
targeting budget 32 are separate research artifacts and are not premises of
Theorem F.1.

The finite catalogs, initial row families, geometric architecture, and adapted
proof code derive in part from Michael Schroeder's pinned version-1 archive;
the 23-point combinatorial theorem uses Baek's formal development. Their
attribution and separate code/data licenses are documented in
[THIRD_PARTY.md](docs/THIRD_PARTY.md). The present theorem is the result of the
closed formal composition above, not a claim of independent discovery of
every constituent argument.

## R. The residual relaxation and the unresolved bound 313

This section separates proved consequences of real geometry from the unresolved
integer optimization problem. The state indices are those of the fixed residual
catalog in Section F; they are not coordinates of points. Every assertion about
an actual residual configuration assumes all three residual restrictions from
Section F: no six-cap, no convex octagon and no six-cup/five-cap junction.

### R.1. The frozen 2,469-row system

Let $`U=\{0,\ldots,153\}`$. For $`r\in\{0,\ldots,2468\}`$ let $`(S_r,d_r)`$ be
the exact support and demand given by `OmissionResidual32Contexts.support`
and `demand` in
[Catalog.lean](experiments/omission-residual32-context-certificates-2026-10-10/Residual32ContextsProof/Catalog.lean).
For $`h:U\to\{0,1\}`$ define

```math
 \mathcal A_{2469}(h)\quad\Longleftrightarrow\quad
 \forall r<2469,\qquad d_r\le\sum_{i\in S_r}h_i.
 \tag{R1}
```

In Lean, $`h`$ is a natural-valued function together with the explicit premises
$`h_i\le1`$; this is equivalent to the displayed Boolean-valued convention.
The first 1,187 rows are the original residual geometric rows. They are followed
by 1,108 rounded consequences, 162 additional geometric rows and 12 further
rounded consequences. All row indices in this section are zero-based.

**Proposition R.1 (geometric necessity).** For every residual configuration
$`c`$ on $`n`$ points, let $`O(c)\subseteq U`$ be its occupied states and set
$`h_i=1`$ if $`i\notin O(c)`$, and $`h_i=0`$ otherwise. Then

```math
 \mathcal A_{2469}(h),\qquad \sum_{i\in U}h_i+n=154.
 \tag{R2}
```

This is `OmissionResidual32Transfer.all_rows` and `feasible_holes` in
[Transfer.lean](experiments/omission-residual32-transfer-2026-10-10/Transfer.lean).
The proof uses one common $`O(c)`$ for every family. Literal equalities identify
the row supports and demands with the geometric and rounded-cut theorems;
injectivity of the state assignment gives $`\vert O(c)\vert =n`$, hence the second equality.
The converse to (R2) is not a theorem: a feasible $`h`$ need not be realized by
points in the plane.

### R.2. A proved obstruction to this relaxation

Define

```math
\begin{aligned}
 M_{\ast} = \{&7,12,33,39,44,47,50,51,52,54,55,56,69,71,73,75,\\
          &76,77,78,90,97,99,101,109,115,117,118,119,124,127,132,133\}.
\end{aligned}
```

Let $`h_i^{\ast}=\mathbf1_{M_{\ast}}(i)`$.

**Proposition R.2 (exact finite witness).** The function $`h^{\ast}`$ satisfies

```math
 \mathcal A_{2469}(h^{\ast}),\qquad \sum_i h_i^{\ast}=32,\qquad
 h_{54}^{\ast}=1,\quad h_{43}^{\ast}=h_{67}^{\ast}=h_0^{\ast}=0.
 \tag{R3}
```

In particular the universally quantified implication from (R1) and the four
displayed branch conditions to $`\sum_i h_i\ge33`$ is false.

**Proof.** The literal set has 32 distinct members. For each of the 2,469
literal rows, finite computation proves $`d_r\le\vert S_r\cap M_{\ast}\vert `$.
For every $`S\subseteq U`$, $`\sum_{i\in S}\mathbf1_{M_{\ast}}(i)=\vert S\cap M_{\ast}\vert `$;
this converts the cardinality checks into (R3). Substitution of $`h^{\ast}`$ in
the proposed universal implication would give $`33\le32`$. These are ordinary
kernel-checked proofs (`decide +kernel` for the finite computations).
The declarations `missing_card`, `all_rows`, `sum_holes`,
`allows_thirty_two_holes` and `no_universal_thirty_three_hole_bound`, all in
namespace `OmissionResidual32Case4`, appear in
[Witness.lean](experiments/omission-residual32-case4-2026-10-10/Witness.lean).
This is a counterexample to a finite implication, not a planar counterexample.

### R.3. A further necessary geometric inequality

Let

```math
 S_{\ast} = \{25,43,53,65,74,85,89,91,96,107,110,111,125\}.
```

**Theorem R.3 (the Sixth obstruction).** Every actual residual configuration
$`c`$ satisfies

```math
 |S_{\ast}\setminus O(c)|\ge1.
 \tag{R4}
```

This is `ErdosSzekeres.Omission.CoupledCoreSixth.hole_bound` in
[Geometry.lean](experiments/omission-residual32-witness-coupled-2026-10-10/Geometry.lean).

**Proof and exact certificate semantics.** Suppose all 13 states are occupied.
Enumerate them in the displayed increasing order by $`s:\{0,\ldots,12\}\to U`$.
Choose owners $`v_j\in\{0,\ldots,n-1\}`$ with residual state $`s(j)`$.
The $`v_j`$ are distinct because the $`s(j)`$ are distinct. Write $`p_j=c(v_j)`$.
All owners belong to the same configuration; neither their relative order nor
their pair ranks may be chosen independently in different clauses.

The structure `Coupled.Context 13 n s` records exactly these owners, their
states, the residual restrictions and the nonzero orientations of distinct
triples. For a pair of distinct owners, let $`(a_{ij},b_{ij})`$ be its actual
residual label with the earlier owner placed first. The proved bounds are
$`1\le a_{ij}\le4`$ and $`1\le b_{ij}\le6`$.
The atom interpretation in
[CoupledSemantics.lean](ErdosSzekeres/Omission/CoupledSemantics.lean) is:

| Lean atom | Mathematical proposition |
| --- | --- |
| `falsum` | $`\bot`$ |
| `before i j` | $`v_i<v_j`$ |
| `capGe i j t` | $`t\le a_{ij}`$ |
| `cupGe i j t` | $`t\le b_{ij}`$ |
| `positive i j k` | $`\det(p_j-p_i,p_k-p_i)>0`$ |
| `convex i j k l` | $`\{p_i,p_j,p_k,p_l\}`$ is in convex position |

Positive literals assert the corresponding proposition; negative literals
assert its negation. A clause is their disjunction, and the formula is the
conjunction of its clauses. The ordered list `CoupledCoreSixth.atoms` fixes
the correspondence between numerical variable identifiers and these
propositions. Thus the numerical formula is completely specified by that list
and [core13.cnf](experiments/omission-residual32-witness-coupled-2026-10-10/core13.cnf).

For every such context, the private lemmas `sound000` through `sound375` in
[LeanCore.lean](experiments/omission-residual32-witness-coupled-2026-10-10/LeanCore.lean)
prove all 376 clauses, using actual order, rank growth, domain restrictions,
orientation implications and convex-octagon exclusion. `formula_eq` identifies
these clauses with the refuted formula. The retained formula has 337 variables;
[core13.lrat](experiments/omission-residual32-witness-coupled-2026-10-10/core13.lrat)
contains 258 clause additions. Each retained RUP step is justified by unit
propagation after negating its proposed clause, using the indicated earlier
clauses. The checked derivation ends in the empty clause. Mathlib's LRAT
proof-term generator supplies a proof checked by the Lean kernel; the solver
output is not an additional axiom.

`CoupledCoreSixth.context_impossible` applies that refutation to the valuation
defined above. This contradicts the supposed simultaneous occupation and
proves `exists_missing_state`; its cardinality form is (R4). This proof is
finite but does not enumerate real coordinates. Its validity depends on the
proved geometric interpretation of every clause.

**Corollary R.4 (strict strengthening and nonrealizability).** The row (R4)
does not follow from (R1), even after restricting to the 32-hole witness with
state zero occupied. Moreover no actual residual configuration has occupied
set $`U\setminus M_{\ast}`$.

**Proof.** Direct finite checking gives $`S_{\ast}\cap M_{\ast}=\varnothing`$. Hence
$`h^{\ast}`$ satisfies every old inequality and violates (R4). If
$`O(c)=U\setminus M_{\ast}`$, then
$`S_{\ast}\setminus O(c)=S_{\ast}\cap M_{\ast} =\varnothing`$, contradicting Theorem R.3.
These are `CoupledCoreSixth.strict_strengthening` and
`countermodel_not_realizable` in the same geometry module. The last statement
excludes this exact occupied set; it does not exclude all 32-hole assignments.

### R.4. Template transport and the 2,598-row system

The Fourth obstruction has a state-parametric form. A map
$`\sigma:\{0,\ldots,12\}\to U`$ is called compatible here precisely when it
satisfies `CoupledTemplateFourth.Compatible` in
[CoupledTemplateFourth.lean](ErdosSzekeres/Omission/CoupledTemplateFourth.lean).
This is a finite conjunction: the ordered pairs in `emptyTests` have the
specified empty directed domains, the labels listed in `domainTests` are
disallowed, and the ordered triples in `positiveTests` pass the proved
orientation test. These three literal lists are part of the definition;
compatibility does not mean merely that the support has 13 elements.
More explicitly, within $`\{1,\ldots,4\}\times\{1,\ldots,6\}`$, the directed
domain is

```math
 D_\sigma(i,j)=\bigl(I(\sigma(j))\setminus I(\sigma(i))\bigr)
                 \setminus\{(1,6)\}.
```

Here $`I(s)`$ denotes the positive cells of the catalog profile $`s`$.
`emptyTests` requires the indicated domain to be empty, and `domainTests`
requires the indicated label to lie outside it. Removing $`(1,6)`$ uses the
proved forbidden-label statement from Section F.1; this is exactly
`Coupled.Allowed`, not the unmodified Ferrers difference.

**Proposition R.5 (template transport).** If $`\sigma`$ is injective and
compatible, then every actual residual configuration satisfies

```math
 |\sigma(\{0,\ldots,12\})\setminus O(c)|\ge1.
 \tag{R5}
```

This is `CoupledTemplateFourth.hole_bound` in
[CoupledTemplateFourthGeometry.lean](ErdosSzekeres/Omission/CoupledTemplateFourthGeometry.lean).
The proof again selects distinct owners. Compatibility justifies the
state-dependent premises in the frozen Fourth refutation; its other clauses
are valid for every actual context. That refutation contradicts occupation
of all owners.

The literal family `CoupledFourthGlobalVariants.maps` contains 128 maps.
`checked` proves injectivity and compatibility for each, and `all_rows` applies
(R5) to each support; see
[Data.lean](experiments/omission-residual32-fourth-global-variants-2026-10-10/FourthGlobalProof/Data.lean)
and [Root.lean](experiments/omission-residual32-fourth-global-variants-2026-10-10/FourthGlobalProof/Root.lean).
This finite family is not asserted to enumerate all compatible maps.

Define 129 added supports $`T_0,\ldots,T_{128}`$ by taking $`T_0=S_{\ast}`$ and
$`T_{j+1}`$ equal to the support of the $`j`$-th Fourth map. The theorem
`Residual32AddedRows.literal_binding` identifies that family with the exact
ordered literal array used in the search. Its `all_rows` theorem proves

```math
 \forall j<129,\qquad \sum_{i\in T_j}h_i\ge1
 \quad\text{for }h_i=\mathbf1_{U\setminus O(c)}(i).
 \tag{R6}
```

Both are in namespace `ErdosSzekeres.Omission`, in
[AddedRows.lean](experiments/omission-residual32-added-rows-2026-10-10/AddedRows.lean).
Together, (R1) and (R6) define $`\mathcal A_{2598}`$: the unchanged old 2,469
rows followed by these 129 rows. The archived JSON's ordered correspondence
is separately checked against these Lean literals; it is not silently assumed
from matching family names.

### R.5. The precise remaining proposition

The sufficient arithmetic statement for the present residual route is

```math
 \forall h:U\to\{0,1\},\qquad
 \mathcal A_{2598}(h)\Longrightarrow\sum_{i\in U}h_i\ge33.
 \tag{OPEN}
```

**(OPEN) is not proved in this repository.** If proved and bound to these
exact literal rows, it would give $`n\le121`$ by (R2). The proved balanced
bound $`190`$ and the proved projective/partition composition would then give
$`\mathsf F(313,8)`$, because $`190+121+2=313`$. A statement restricted to
$`h_0=0`$ would also suffice for nonempty residual configurations, using the
separate proved occupation-of-zero lemma and treating the empty case directly.

The bounded searches recorded in the
[2,598-row bundle](experiments/omission-residual32-2598-primal-2026-10-10/README.md)
provide neither a feasible 32-hole assignment nor a complete exclusion. The
best saved candidate violates old row 205, whose support is
$`\{24,31,34,40,61,68,73,100\}`$ and whose demand is one. Timeouts and failed
local repairs do not establish (OPEN). Cases 2 and 7 of the earlier search
remain partial; Proposition R.2 shows why closing those cases alone could
not prove the old relaxation sufficient.

There is no remaining unproved geometric premise in the completed 314 theorem.
For the current 2,598-row route, the existing row families already have
geometric necessity proofs. A successful continuation would still require a
complete arithmetic certificate, kernel checking of it, literal catalog
identification and final composition. A new feasible 32-hole assignment would
instead require stronger geometry or another argument. No completion-time or
certificate-size estimate is justified by the partial searches.

## V. Validation and references

All finished results discussed above are proved without `sorry`, `admit`,
custom mathematical axioms, or `native_decide`. The audited declarations depend
only on the standard Lean axioms `propext`, `Classical.choice` and `Quot.sound`
(or a subset). The maintained-library audit covers 571 named declarations;
the latest standalone residual continuation has a separate gate checking 20
modules and 43 audit roots. The large arithmetic trees for 314 have their own
complete kernel records, linked in Section F.5. They are distinct from the
maintained-library CI build. A passing discovery script is not substituted
for any of these proofs. The [validation ledger](docs/VALIDATION.md) supplies
commands, scopes and recorded outputs.

The source-to-mathematics correspondences in Sections S, F and R preserve
strict inequalities, natural-number subtraction, the order of asymptotic
quantifiers and all geometric restrictions. In particular, a conditional
finite arithmetic implication is not identified with an unconditional planar
bound, and an abstract feasible state assignment is not identified with a
realizable point set. These distinctions explain both the completed theorem
and the present boundary of the research.

The principal external references are:

1. Andrew Suk, *On the Erdős–Szekeres convex polygon problem*,
   [arXiv:1604.08657v2](https://arxiv.org/abs/1604.08657v2), 2016.
2. Andreas F. Holmsen, Hossein Nassajian Mojarrad, János Pach and Gábor Tardos,
   *Two extensions of the Erdős–Szekeres problem*,
   [arXiv:1710.11415v3](https://arxiv.org/abs/1710.11415v3),
   *Journal of the European Mathematical Society* **22** (2020), 3981–3995,
   [doi:10.4171/JEMS/1000](https://doi.org/10.4171/JEMS/1000).
3. Michael Schroeder, *Erdős–Szekeres: Upper Bounds for Convex Heptagons and
   Octagons*, supplied version-1 archive dated 19 September 2026. The supplied
   identifier is DOI `10.5281/zenodo.22842891`; its README describes a reserved
   Zenodo draft, so public resolution or peer review is not asserted here.
   Pinned source identities, local changes and attribution are in the
   [third-party ledger](docs/THIRD_PARTY.md).
4. Jineon Baek, [erdos-tuza-valtr](https://github.com/jcpaik/erdos-tuza-valtr),
   the attributed formal combinatorial prerequisites and finite block theorem;
   the exact imported revisions and adaptations are in the same ledger.

Original project exposition is Apache-2.0. Third-party code and derived data
retain the exceptions listed in [the license scope](docs/LICENSING.md).
The theorem $`\mathrm{ES}(8)\le314`$ is the proved bound of this repository;
no literature-priority or best-known-bound claim is made.
