# Erdős–Szekeres bounds and their formal proofs

## 1. Statements and conventions

This article describes three completed Lean proofs: Suk's asymptotic bound,
the ordinary real-point specialization of the Holmsen–Mojarrad–Pach–Tardos
(HMPT) bound, and the finite bound $`\mathrm{ES}(8)\le314`$. It also explains
the proved refinements and the precise remaining problem in the investigation
of $`\mathrm{ES}(8)\le313`$.

The [finite octagon proof](#2-geometric-configurations-and-finite-state-spaces)
occupies §§2–3. Section 4 treats the [asymptotic bounds](#4-the-asymptotic-arguments),
and §§5–6 develop the [residual inequalities and the open bound 313](#5-stronger-residual-inequalities).

A finite set $`P\subset\mathbb R^2`$ is in **general position** if no three
distinct points are collinear. It is in **convex position** if

```math
p\notin\mathrm{conv}(P\setminus\{p\})\qquad(p\in P).
```

Write $`\mathsf F(N,n)`$ when every finite general-position set of at least
$`N`$ points contains a subset of cardinality $`n`$ in convex position. Thus
$`\mathrm{ES}(n)\le N`$ means $`\mathsf F(N,n)`$. These are ordinary convex
polygons: other points may lie inside their hulls. Coordinates are arbitrary
real numbers.

**Theorem 1.1 (completed bounds).** The following statements hold.

**(1) Suk.** There exists $`n_0\ge3`$ such that, for every integer $`n\ge n_0`$,

```math
\mathsf F\!\left(\left\lfloor2^{n+6n^{2/3}\log n}\right\rfloor_{\mathbb N},n\right).
```

**(2) HMPT.** For every real $`\varepsilon>0`$ there exists $`n_0\ge3`$ such that,
for every integer $`n\ge n_0`$,

```math
\mathsf F\!\left(
\left\lfloor2^{n+(8\sqrt2/3+\varepsilon)\sqrt{n\log n}}\right\rfloor_{\mathbb N},n
\right).
```

**(3) Finite octagon bound.** $`\mathsf F(314,8)`$.

The first two statements are eventual bounds; their quantifiers do not permit
an unverified substitution of $`n=8`$. The HMPT statement retains every
positive $`\varepsilon`$ and concerns ordinary point sets, not the paper's
pseudo-configuration or convex-body extensions.

All logarithms are to base two. Finite counting parameters are natural numbers
unless specified otherwise. Natural-number subtraction is truncated at
zero; natural-number division is floor division. We write
$`\lfloor x\rfloor_{\mathbb N}`$ for the natural floor, and use
$`\lceil\log u\rceil`$, $`\lfloor\log u\rfloor`$ for Lean's
`Nat.clog 2 u`, `Nat.log 2 u` when $`u>0`$.

| Statement | Lean declaration and source |
| --- | --- |
| General position, convex position, $`\mathsf F`$ | `ErdosSzekeres.GeneralPosition`, `ConvexPosition`, `ForcesConvexNGon` in [Definitions](ErdosSzekeres/Definitions.lean) |
| Convex-hull characterization; equivalence with sets of exactly $`N`$ points; monotonicity in $`N`$ | `convexPosition_iff`, `forcesConvexNGon_iff_exact`, `ForcesConvexNGon.mono` in [Basic](ErdosSzekeres/Basic.lean), with prefix `ErdosSzekeres` |
| Suk bound | `ErdosSzekeres.Suk.theorem2016` in [Suk/Asymptotic](ErdosSzekeres/Suk/Asymptotic.lean) |
| HMPT bound | `ErdosSzekeres.HMPT.theorem2020` in [HMPT/Asymptotic](ErdosSzekeres/HMPT/Asymptotic.lean) |
| Finite octagon bound | `ErdosSzekeres.Omission.forces_convex_octagon_314`, `convex_octagon_of_card_ge_314` in [FinalCover314B61FusedR31Fused](experiments/omission-global-assembly-2026-10-10/FinalCover314B61FusedR31Fused.lean) |

The formalized conjecture is
$`\forall n\ge3,\ \mathsf F(2^{n-2}+1,n)`$; for octagons its threshold is
$`65`$. This definition does not include a formalization of the classical
lower-bound construction. Neither the conjecture nor the bound $`313`$ is
proved here.

## 2. Geometric configurations and finite state spaces

### 2.1. Cups, caps and attained ranks

Put $`[a,b,c]=\det(b-a,c-a)`$. An **ordered configuration** of size $`n`$ is a
map $`p:\{0,\ldots,n-1\}\to\mathbb R^2`$ with strictly increasing first
coordinates and nonzero determinants on increasing triples. A cup, respectively
cap, is an increasing sequence whose increasing triples have positive,
respectively negative, determinant.

Consecutive-triple signs suffice. Indeed, when
$`a_x\lt b_x\lt c_x\lt d_x`$,

```math
\begin{aligned}
(c_x-b_x)[a,b,d]&=(d_x-b_x)[a,b,c]+(b_x-a_x)[b,c,d],\\
(c_x-b_x)[a,c,d]&=(d_x-c_x)[a,b,c]+(c_x-a_x)[b,c,d].
\end{aligned}
```

Both identities preserve a common strict sign. Induction gives the
all-triples condition and closure under subsequences. An eight-cup is
therefore a convex octagon.

For $`u\lt v`$, let $`E_-(u,v)`$ and $`E_+(u,v)`$ be the greatest lengths of
caps and cups ending with the exact pair $`(u,v)`$. Let $`F_-(u,v)`$ be the
greatest length of a cap starting with that pair. All paths lie inside the
configuration under consideration. The pair itself has length two, so these
finite maxima exist and are attained. Extension of an attaining path gives

```math
\begin{aligned}
{}[p_u,p_v,p_w]\lt0&\Longrightarrow
 E_-(u,v)\lt E_-(v,w),\quad F_-(v,w)\lt F_-(u,v),\\
{}[p_u,p_v,p_w]>0&\Longrightarrow E_+(u,v)\lt E_+(v,w)
\qquad(u\lt v\lt w).
\end{aligned}
```

A configuration is **balanced** if it has no seven-cap, seven-cup or convex
octagon. It is **residual** if it has no six-cap, convex octagon or junction.
A **junction** consists of an actual six-cup ending at a vertex and an actual
five-cap starting there, both inside the configuration.

Define pair labels by

```math
d_B(u,v)=(E_-(u,v)-1,E_+(u,v)-1)\in\{1,\ldots,5\}^2
```

in the balanced case, and by

```math
d_R(u,v)=(6-F_-(u,v),E_+(u,v)-1)
 \in\{1,\ldots,4\}\times\{1,\ldots,6\}
```

in the residual case. These bounds follow by shortening an attained forbidden
chain; octagon avoidance rules out an eight-cup. In both cases a cap triple
strictly increases the first label coordinate, and a cup triple strictly
increases the second.

### 2.2. Incoming states

For either label system, define the incoming down-set

```math
I(v)=\{z:\exists u\lt v,\ z_1\le d_1(u,v),\ z_2\le d_2(u,v)\}
```

inside the corresponding positive label grid.

**Lemma 2.1 (state separation).** If $`u\lt v`$, then
$`d(u,v)\in I(v)\setminus I(u)`$. Consequently different vertices have
different incoming states.

*Proof.* The first membership is immediate. Membership in $`I(u)`$ would
supply $`t\lt u`$ with both coordinates of $`d(t,u)`$ at least those of
$`d(u,v)`$. The triple $`(t,u,v)`$ is a cup or a cap; either sign contradicts
the corresponding strict growth inequality. ∎

A balanced state has nonincreasing column heights
$`5\ge f_1\ge\cdots\ge f_5\ge0`$. There are $`\binom{10}{5}=252`$ profiles.
A residual state satisfies

```math
6\ge f_1\ge f_2\ge f_3\ge f_4\ge0,
\qquad f_1\lt6\ \text{or}\ f_2=6.                       \qquad\text{(2.1)}
```

To prove the extra restriction, observe that label $`(1,6)`$ would give a
five-cap starting with $`(u,v)`$ and a seven-cup ending with $`(u,v)`$.
Deleting the cup's last vertex creates a junction at $`u`$. Thus a height
six in the first column must be attained by a label whose first coordinate
is at least two. The residual catalog consequently has
$`\binom{10}{4}-\binom83=154`$ profiles; its literal representation appends a
fifth zero coordinate.

Lean checks completeness and ordering of both literal catalogs. Lemma 2.1
then gives injective owner maps into these catalogs. If $`O`$ is the image
of a configuration of size $`n`$, define its **holes** by
$`h_i=\mathbf1_{V\setminus O}(i)`$. Injectivity gives

```math
\sum_{i\in V}h_i+n=\vert V\vert.                         \qquad\text{(2.2)}
```

| Construction | Declarations (prefix `ErdosSzekeres.Omission`) |
| --- | --- |
| Ordered real configurations; cups and caps | `Configuration`, `Configuration.HasCup`, `Configuration.HasCap` in [Realization](ErdosSzekeres/Omission/Realization.lean) |
| Sign propagation and convexity | `PlanarChains.positive_four`, `negative_four`, `cup_all` in [PlanarChains](ErdosSzekeres/Omission/PlanarChains.lean); `ListGeometry.hasNCup_octagon` in [ListGeometry](ErdosSzekeres/Omission/ListGeometry.lean) |
| Ending and starting paths, maxima, attainment, growth | `ActualRanks.EndingPath`, `rank`, `rank_attained`, `rank_growth`, `labels` in [ActualRanks](ErdosSzekeres/Omission/ActualRanks.lean); corresponding `ResidualRanks` declarations and `forbidden_label` in [ResidualRanks](ErdosSzekeres/Omission/ResidualRanks.lean) |
| Junction and restriction to subsets | `Subsets.JunctionOn`, `NoJunctionOn`, `restrict` in [Subsets](ErdosSzekeres/Omission/Subsets.lean) |
| State separation | `StateInterface.incoming_admissible`, `states_distinct` in [StateInterface](ErdosSzekeres/Omission/StateInterface.lean) |
| Heights and state injectivity | `ActualRanks.column`, `incoming_iff_column`, `balancedState_injective` in [BalancedStates](ErdosSzekeres/Omission/BalancedStates.lean); `ResidualStates.column`, `top_cell_constraint`, `state_injective` in [ResidualStates](ErdosSzekeres/Omission/ResidualStates.lean) |
| Literal catalogs and owner maps | `BalancedCatalog.profiles_covered`, `ownerIndex_profile`, `ownerIndex_injective` in [BalancedCatalog](ErdosSzekeres/Omission/BalancedCatalog.lean); analogous [ResidualCatalog](ErdosSzekeres/Omission/ResidualCatalog.lean) results and `Configuration.residualOwner` in [ResidualRealization](ErdosSzekeres/Omission/ResidualRealization.lean) |

### 2.3. Geometric omission inequalities

An **omission row** is a support $`S_r\subseteq V`$ and demand $`d_r\in\mathbb N`$
asserting

```math
h(S_r):=\sum_{i\in S_r}h_i=\vert S_r\setminus O\vert\ge d_r. \qquad\text{(2.3)}
```

These are necessary conditions on actual configurations; their Boolean
solutions need not be realizable by points.

**Lemma 2.2 (cycle rows).** Suppose a list of distinct states has this checked
property: owners of every three states, in list order, have positive
orientation. At most seven listed states occur in an octagon-free
configuration. A list of length $`k`$ therefore gives demand $`k-7`$.

*Proof.* Eight occupied states would have distinct owners, positive orientation
on every increasing triple in list order, and hence form a convex octagon. ∎

The check uses rectangles bounding directed differences
$`I(B)\setminus I(A)`$. By Lemma 2.1 every actual pair label lies in the
appropriate rectangle. For each of the six chronological orders of three
owners, the check finds either an empty required difference or a coordinate
separation forcing the desired sign. For example, a second pair's maximum
first coordinate at most the first pair's minimum excludes cap growth and
forces a cup. Permutation parity converts chronological signs to list-order
signs. Catalog order, list order and chronological order are distinct.

**Lemma 2.3 (block rows).** Suppose all admissible pair labels on a residual
support $`S`$ have a checked compression into $`\{1,2\}`$ that strictly
increases along every cap triple. Then at most 22 states of $`S`$ are
occupied, giving demand $`\vert S\vert-22`$.

*Proof.* A four-cap would require three strictly increasing compressed values.
Baek's finite theorem gives a four-cap or an eight-vertex cup/cap boundary
among any 23 points. The boundary is a convex octagon by supporting affine
functionals. Both alternatives are impossible. ∎

The compression is specified by active cells and a threshold at each cup
coordinate. Finite checks establish coverage of all directed-difference labels
and growth at every shared middle state. The resulting original catalogs
contain 2,685 balanced cycle rows and 1,187 residual cycle or block rows.
Every row is proved for the same occupied set $`O`$.

| Step | Lean correspondence |
| --- | --- |
| Six-order sign check | `CycleSigns.Safe`, `CheckTriple`, `checked_triple_positive` in [CycleSigns](ErdosSzekeres/Omission/CycleSigns.lean), using the proved [BoundingBoxes](ErdosSzekeres/Omission/BoundingBoxes.lean) and residual tables |
| Cycle capacities and hole bounds | `Configuration.checked_cycle_capacity`, `checked_cycle_hole_bound`, `list_cycle_hole_bound` in [CycleGeometry](ErdosSzekeres/Omission/CycleGeometry.lean), with residual versions in [ResidualCycleGeometry](ErdosSzekeres/Omission/ResidualCycleGeometry.lean) |
| Block compression and geometry | `BlockCompression.pairsOK`, `growthOK`, `no_four_cap_of_rank2` in [BlockCompression](ErdosSzekeres/Omission/BlockCompression.lean); `Baek.four_cap_or_eight_gon`, `BaekGeometry.geometric_capacity22`, `BlockGeometry.block_hole_bound` in [Baek](ErdosSzekeres/Omission/Baek.lean), [BaekGeometry](ErdosSzekeres/Omission/BaekGeometry.lean), [BlockGeometry](ErdosSzekeres/Omission/BlockGeometry.lean) |
| All original rows and Boolean hole vectors | `OmissionBalanced.all_geometric_rows`, `feasible_holes` in the [balanced source bundle](experiments/omission-global-assembly-2026-10-10/README.md); `OmissionResidual.all_geometric_rows`, `feasible_holes` in the [residual source bundle](experiments/omission-residual-geometry-2026-10-09/README.md) |

The first three rows use namespace prefix `ErdosSzekeres.Omission`.

## 3. Exact certificates and the proof of the octagon bound

### 3.1. Weighted inequalities and integer rounding

**Lemma 3.1 (weighted capacity bound).** Let $`h:V\to\{0,1\}`$ satisfy the
rows (2.3). For nonnegative integer weights $`w_r`$, put

```math
L_i=\sum_{r:i\in S_r}w_r,\qquad D=\sum_rw_rd_r.
```

For every integer $`C\ge0`$,

```math
D\le\sum_iL_ih_i\le C\sum_ih_i+\sum_i(L_i-C)_+,           \qquad\text{(3.1)}
```

where $`x_+=\max(x,0)`$.

*Proof.* Multiply and sum the rows, then use
$`L_ih_i\le Ch_i+(L_i-C)_+`$ for each Boolean coordinate. ∎

In particular, $`Cb+\sum_i(L_i-C)_+\lt D`$ excludes at most $`b`$ holes.
For a proposed support $`T`$, put

```math
E_T=\sum_{i\in T}(L_i-C)_++\sum_{i\notin T}L_i.
```

The same proof gives $`D\le Ch(T)+E_T`$. Hence, for $`q\ge1`$,

```math
C(q-1)+E_T\lt D\quad\Longrightarrow\quad h(T)\ge q.       \qquad\text{(3.2)}
```

This is an exact **rounded cover cut**: if the integer $`h(T)`$ were less
than $`q`$, it would be at most $`q-1`$. For $`C>0`$ it expresses the ceiling
bound $`h(T)\ge\lceil(D-E_T)/C\rceil`$. No floating-point objective is rounded.
For example, three demand-one rows whose union is $`T`$ and whose column loads
are at most two yield $`2(2-1)\lt3`$, and thus demand two on $`T`$.

The formal augmentations add 446 balanced cuts and 1,108 residual cuts.
Every cut uses only earlier rows, so induction proves all 3,131 balanced
and 2,295 residual inequalities without additional geometric assumptions.

At a tree node, let $`M`$ be indices fixed missing, $`Z`$ indices fixed occupied,
and $`F=V\setminus(M\cup Z)`$. Assume $`M,Z`$ disjoint. A budget $`b`$ is
impossible if $`\vert M\vert>b`$. Otherwise a sufficient leaf test is

```math
C(b-\vert M\vert)+\sum_{i\in F}(L_i-C)_++\sum_{i\in M}L_i\lt D. \qquad\text{(3.3)}
```

Indeed, fixed missing indices consume $`\vert M\vert`$ holes, and the weighted
sum is at most the left side. The implementation can instead remove fixed
indices from each support and replace its demand by
$`(d_r-\vert S_r\cap M\vert)_+`$. The production proofs use the equivalent
full-load form

```math
C(b-\vert M\vert)+\sum_{i\in V}(L_i-C)_++\sum_{i\in M}L_i
\lt D+\sum_{i\in M\cup Z}(L_i-C)_+.                       \qquad\text{(3.4)}
```

A split on $`i`$ has a zero child fixing it occupied and a one child fixing it
missing. Both children must be excluded. Induction, using Booleanity,
therefore excludes the root context; an empty root excludes every solution
within budget. No incomplete leaf is a proof case.

Large column sums are checked by positional encoding. Put
$`R_r=\sum_{i\in S_r}B^i`$ for $`B>1`$. If
$`\sum_rw_r\lt B`$, every proposed digit $`c_i\lt B`$, and

```math
\sum_i c_iB^i=\sum_rw_rR_r,
```

then $`c_i=L_i`$. Indeed, every actual load is below $`B`$; equality follows
from uniqueness of base-$`B`$ digits, proved by reduction modulo $`B`$ and
induction. Sparse storage and Horner evaluation change only representation.

| Argument | Lean declaration and source |
| --- | --- |
| Weighted bounds and conditioned leaves | `OmissionCertificates.weighted_capacity_bound`, `excludes_budget`, `sum_after_fixing`, `conditioned_excludes_budget`, `conditioned_excludes_of_full_load` in [OmissionCertificates](ErdosSzekeres/OmissionCertificates.lean) |
| Rounded cuts | `OmissionCertificates.weighted_subset_capacity_bound`, `rounded_cover_cut` in [CoverCuts](ErdosSzekeres/Omission/CoverCuts.lean); `BalancedCoverCutsV2.all_rows`, `ResidualCoverCutsV2.all_rows` in the [cut bundle](experiments/omission-cover-certificates-2026-10-10/README.md) |
| Tree induction | `CertificateTree.check_sound`, `excludes_of_check`, `split_excludes` in [OmissionCertificates](ErdosSzekeres/OmissionCertificates.lean) |
| Packed loads | `pack_injective_of_lt`, `load_eq_of_packed`, `load_eq_of_sparse_packed` in [OmissionPacking](ErdosSzekeres/OmissionPacking.lean); `fused_sparse_packed_excludes` generated by [omission_fused_export.py](scripts/omission_fused_export.py) |

The certificate and packing declarations have namespace prefix
`ErdosSzekeres.OmissionCertificates`; in particular, the tree declarations are
`CertificateTree.check_sound`, `CertificateTree.excludes_of_check`, while
`split_excludes` belongs directly to that namespace.

### 3.2. Population bounds

**Theorem 3.2.** Every balanced configuration has at most 190 points; every
residual configuration has at most 122 points.

*Proof.* Complete kernel-checked exclusion trees show that the augmented
balanced system has no solution with at most 61 holes, and the augmented
residual system has none with at most 31 holes. Literal support and demand
identities identify their rows with the geometric rows and proved cuts.
Thus (2.2) gives

```math
n_B\le252-62=190,\qquad n_R\le154-32=122.                 \qquad\text{(3.5)}
```

∎

The arithmetic roots are `OmissionBalancedCover61Fused.excludes_budget` and
`OmissionResidualCover31Fused.excludes_budget`, preserved with their complete
trees in the [certificate bundle](experiments/omission-cover-certificates-2026-10-10/README.md).
The [balanced bridge](experiments/omission-global-assembly-2026-10-10/BalancedCover61FusedBridge.lean)
and [residual bridge](experiments/omission-global-assembly-2026-10-10/ResidualCover31FusedBridge.lean)
prove `base_catalog_matches`, `cut_catalog_matches`, `all_cover_rows` and
`exclusion_transfer`. The resulting closed declarations are
`ErdosSzekeres.Omission.balanced_population_190` and `residual_population_122`
in the final theorem file from §1. Their types are `Partition.BalancedBound 190`
and `Partition.ResidualBound 122`, with exactly the geometric hypotheses of §2.
More generally, excluding budget $`b`$ yields populations $`251-b`$ and $`153-b`$.

### 3.3. Projective reduction and minimum-slope partition

**Lemma 3.3 (root deletion).** A nonempty finite general-position set $`S`$
without a convex octagon gives an ordered configuration of size
$`\vert S\vert-1`$ with no seven-cap and no convex octagon.

*Proof.* An invertible linear change makes all abscissae distinct. Let $`a`$
be the leftmost point. On the half-plane $`x>a_x`$ use

```math
\begin{aligned}
\Phi_a(x,y)&=\left(\frac{y-a_y}{x-a_x},-\frac1{x-a_x}\right),\\
{}[\Phi_a(p),\Phi_a(q),\Phi_a(r)]
&=-\frac{[p,q,r]}{(p_x-a_x)(q_x-a_x)(r_x-a_x)}.
\end{aligned}                                           \qquad\text{(3.6)}
```

This map is injective; equal first coordinates would mean equal ray slopes
from $`a`$, contradicting general position. Its image is therefore an ordered
configuration. Convex polygons transfer back through this chart. A seven-cap,
together with $`a`$, also transfers to a convex octagon: non-root triples
acquire positive orientation by (3.6), and root triples do so by increasing
ray slopes. Both alternatives contradict avoidance. ∎

**Lemma 3.4 (partition).** An ordered configuration of size $`n\ge2`$ with no
seven-cap or convex octagon partitions into a balanced part $`H`$ and a
residual part $`R`$.

*Proof.* At each vertex $`u`$, choose a distinct minimum-slope neighbor $`m(u)`$.
Set $`U=\{u:u\lt m(u)\}`$, $`L=\{u:m(u)\lt u\}`$. Minimum slope and
nonzero orientation show that a cap ending in $`U`$ extends rightwards to its
minimum-slope neighbor; a cup starting in $`L`$ extends leftwards. Hence
$`U`$ has no six-cap and $`L`$ no seven-cup.

Let $`G`$ be the junction vertices witnessed within $`U`$, and put
$`H=L\cup G`$, $`R=U\setminus G`$. The residual restrictions on $`R`$ follow
by restriction; a junction there would place its vertex in $`G`$. Both parts
inherit octagon avoidance, and $`H`$ inherits seven-cap avoidance.

Suppose $`H`$ contains a seven-cup from $`s`$ to $`t`$. Its first vertex cannot
lie in $`L`$, since left extension gives an eight-cup. Its last vertex cannot
lie in $`G`$: extend that junction's outgoing five-cap to a six-cap; the join
sign either extends the seven-cup or prepends its penultimate vertex to the
six-cap, contradicting one of the avoidance assumptions. Thus $`s\in G`$
and $`t\in L`$. At $`s`$ there is an incoming six-cup and an outgoing six-cap
whose second vertex $`q`$ lies in $`U`$, so $`q\ne t`$. The geometric
three-chain lemma excludes these chains together with the seven-cup from
$`s`$ to $`t`$. It follows from the four-point sign identities and cup/cap
boundary geometry, without requiring unrelated chains to be disjoint.
Thus $`H`$ is balanced. ∎

**Proof of Theorem 1.1(3).** If $`S`$ avoids convex octagons, the empty and
small cases are immediate. Otherwise Lemmas 3.3–3.4 and Theorem 3.2 give

```math
\vert S\vert=\vert H\vert+\vert R\vert+1\le190+122+1=313.
```

Therefore 314 points force a convex octagon. ∎

| Geometric step | Declarations (prefix `ErdosSzekeres.Omission` except where specified) |
| --- | --- |
| Actual root-deletion chart | `IsRootDeletionChart`, `root_cap_polygon`, `exists_projective_chart`, `exists_cap_free_chart` in [ProjectiveTransfer](ErdosSzekeres/Omission/ProjectiveTransfer.lean); `ErdosSzekeres.HMPT.projectFrom`, `orient_projectFrom` in [Projective](ErdosSzekeres/HMPT/Projective.lean) |
| Minimum-slope extension | `MinimumSlope.MinNeighbors`, `exists_min_neighbors`, `cap_to_right`, `cup_from_left` in [MinimumSlope](ErdosSzekeres/Omission/MinimumSlope.lean) |
| Partition and three-chain argument | `SlopePartition.junctions`, `balancedPart`, `residualPart` in [SlopePartition](ErdosSzekeres/Omission/SlopePartition.lean); `ThreeChain.three_chain` in [ThreeChain](ErdosSzekeres/Omission/ThreeChain.lean); `Partition.balanced_no_seven_cup`, `exists_partition` in [Partition](ErdosSzekeres/Omission/Partition.lean) |
| Final composition | `Partition.avoiding_card_le_of_population_bounds`, `forces_of_population_bounds` in [PopulationBounds](ErdosSzekeres/Omission/PopulationBounds.lean) |

The general composition gives $`\mathsf F(B+R+2,8)`$ from balanced and residual
population bounds $`B,R`$, provided $`1\le B+R`$. One added point is the
deleted root; the other converts an avoiding-set bound into a forcing threshold.

## 4. The asymptotic arguments

### 4.1. Suk's finite support bound

A **cap frame** $`(a,b,c,d)`$ has negative orientation on all four increasing
triples. Its support region is

```math
\{p:[a,b,p]\lt0,\ [b,c,p]>0,\ [c,d,p]\lt0\}.
```

A clockwise sequence of $`k+3`$ horizontally ordered anchors determines
$`k`$ consecutive frames. Suppose the anchors belong to a general-position set
$`P`$, and $`Q_i\subseteq P`$ lies in the $`i`$th region. The finite support
theorem gives a convex $`n`$-gon whenever

```math
\begin{gathered}
n\ge4,\quad K,b\ge3,\quad n\le rK,\quad n\le tb,\quad t(r+1)\le k,\\
\vert Q_i\vert>2^{n+K-4}\binom{n+b-4}{n-2}\quad\text{for every }i.
\end{gathered}                                           \qquad\text{(4.1)}
```

The proof uses the triangle order's chain/antichain dichotomy within each
region. Consecutive large chains yield supported cap growth and adjacent
gluing; separated large antichains yield compatible caps with convex union.
Extraction by finite counting, followed by a coordinate change, proves

```math
\mathsf F\bigl(2^{n+K+Hb+64(k+5)},n\bigr)                 \qquad\text{(4.2)}
```

under the integer hypotheses of (4.1) and $`n+b\le2^H`$. The extraction loss
$`64(k+5)`$ is a proved replacement estimate, not the paper's literal
intermediate constant.

Taking $`K=b=a^2`$, $`r=t=a`$, $`k=a(a+1)`$ gives

```math
\begin{aligned}
D_S(n,a)&=n+a^2+a^2\lceil\log(n+a^2)\rceil+64(a(a+1)+5),\\
n\ge4,\ a\ge2,\ n\le a^3&\quad\Longrightarrow\quad
\mathsf F(2^{D_S(n,a)},n).                               \qquad\text{(4.3)}
\end{aligned}
```

For $`n\ge4`$, $`x=n^{1/3}\ge4`$ and $`\log n\ge100`$, set
$`a=\lceil x\rceil`$, $`H=\lceil\log(n+a^2)\rceil`$. Then
$`n\le a^3`$, $`a^2\le2x^2`$, $`a^2\le n`$, $`H\le\log n+2`$ and
$`a(a+1)+5\le3a^2`$. Consequently

```math
D_S(n,a)-n\le(H+193)a^2
 \le2(\log n+195)x^2\le6n^{2/3}\log n.
```

The integer $`2^{D_S(n,a)}`$ lies below the natural floor in Theorem 1.1(1).
The sufficient hypotheses hold eventually, proving Suk's bound.

| Step | Declarations (prefix `ErdosSzekeres.Suk`) |
| --- | --- |
| Frames and support theorem | `CapFrame`, `CapFrame.spike` in [SpikeGeometry](ErdosSzekeres/Suk/SpikeGeometry.lean); `ClockwiseAnchors.finite_support_bound` in [FiniteSupport](ErdosSzekeres/Suk/FiniteSupport.lean) |
| Extraction and integer parameters | `finite_density_bound` in [FiniteBound](ErdosSzekeres/Suk/FiniteBound.lean), `finite_exponential_bound` in [ExponentialBound](ErdosSzekeres/Suk/ExponentialBound.lean), `finite_logarithmic_bound`, `cubic_log_bound` in [IntegerParameters](ErdosSzekeres/Suk/IntegerParameters.lean) |
| Exponent comparison and eventual conclusion | `integer_parameters_fit_exponent`, `coefficient_six_bound`, `theorem2016` in [Asymptotic](ErdosSzekeres/Suk/Asymptotic.lean) |

### 4.2. HMPT's two-scale count

Let $`P`$ be a finite set in general position, let $`c_j(P)`$ count its convex
$`j`$-subsets, and let $`N=\vert P\vert`$.
If $`j\le M\le N`$ and $`\mathsf F(M,j)`$, double counting gives

```math
\binom Nj\le c_j(P)\binom Mj.                            \qquad\text{(4.4)}
```

Define

```math
\begin{aligned}
B(r,n)&=2^{(r+1)(n-1)+2r}
 \binom{2(n-1)+r+r(n-2)}{2(n-1)+r},\\
\Pi(m,n)&=B(m-3,n)B(2m-3,n).
\end{aligned}
```

Attained chain and antichain maxima bound products of support-region sizes;
adjacent-cap and separated even/odd-cap budgets control their parameters.
The expression $`B`$ retains endpoint and small-capacity padding terms.
For $`n\ge4`$, an $`n`$-gon-free general-position set with distinct abscissae
satisfies the convex-fan ratio

```math
c_{2(r+3)+1}(P)\le c_{r+4}(P)N^3B(r,n).
```

The fan construction uses a projective chart and proved transfer back to the
original points. Applying the ratio at $`r=m-3`$ and $`r=2m-3`$ gives, for
$`m\ge3`$,

```math
c_{4m+1}(P)\le c_{m+1}(P)N^6\Pi(m,n).                    \qquad\text{(4.5)}
```

Combine $`c_{m+1}(P)\le N^{m+1}`$ with (4.4). For
$`m\ge3`$, $`n\ge4`$, $`4m+1\le M\le N`$,

```math
\mathsf F(M,4m+1),\qquad
N^{m+7}\Pi(m,n)\binom M{4m+1}\lt\binom N{4m+1}
\quad\Longrightarrow\quad\mathsf F(N,n).                 \qquad\text{(4.6)}
```

A linear coordinate change removes the distinct-abscissa hypothesis from
this conclusion. The support-path and two-step counting arguments replace
some cyclic intermediates in the paper; the [paper map](docs/PAPER_MAP.md)
records the correspondence.

### 4.3. Entropy, rounding and the leading coefficient

The elementary estimate $`\binom NA\le(4R)^A`$ for $`N\le RA`$ yields

```math
\Pi(m,n)\le2^{3mn+6m+(4n+3m)\lceil\log(8m)\rceil}
\qquad(m\ge3).
```

The exact real-exponent interface assumes $`m,n,d\in\mathbb N`$,
$`X\in\mathbb R`$, and

```math
\begin{gathered}
m\ge3,\quad n\ge4,\quad \mathsf F(2^d,4m+1),\quad 4m+1\le2^d,\\
d+1\le X,\qquad 2(4m+1)+1\le X,\\
(d+1)(4m+1)+3mn+6m+(4n+3m)(\log m+4)
 \lt(3m-6)(X-1).                                        \qquad\text{(4.7)}
\end{gathered}
```

It concludes $`\mathsf F(\lfloor2^X\rfloor_{\mathbb N},n)`$. The unit loss
comes from $`E=\lfloor X\rfloor_{\mathbb N}\ge X-1`$, so rounding is explicit.

For a fixed $`c>0`$, put

```math
\begin{gathered}
L_n=\log n,\quad S_n=\sqrt{nL_n},\quad m_n=\lceil cS_n\rceil_{\mathbb N},\\
d_n=\left\lceil(4m_n+1)+6(4m_n+1)^{2/3}\log(4m_n+1)\right\rceil_{\mathbb N}.
\end{gathered}
```

Suk's theorem supplies $`\mathsf F(2^{d_n},4m_n+1)`$ eventually. The proved
limits are

```math
\frac{m_n}{S_n}\to c,\qquad \frac{d_n}{S_n}\to4c,\qquad
\frac{\log m_n}{L_n}\to\frac12,\qquad \frac{m_n}{n},\frac{d_n}{n}\to0.
```

At $`X_n=n+CS_n`$, define the exact slack

```math
\begin{aligned}
\Delta_n={}&(3m_n-6)(n+CS_n-1)\\
&-\bigl((d_n+1)(4m_n+1)+3m_nn+6m_n
 +(4n+3m_n)(\log m_n+4)\bigr).
\end{aligned}
```

Then

```math
\frac{\Delta_n}{n\log n}\longrightarrow3cC-16c^2-2.       \qquad\text{(4.8)}
```

A positive limit makes (4.7) hold eventually. Taking
$`c=1/(2\sqrt2)`$ and $`C=8\sqrt2/3+\varepsilon`$ makes it
$`3c\varepsilon>0`$, proving Theorem 1.1(2). The identity

```math
3cC-16c^2-2=3c(C-8\sqrt2/3)-(4c-\sqrt2)^2
```

shows that positive limiting slack for some $`c>0`$ is possible exactly when
$`C>8\sqrt2/3`$. This is a barrier for this particular budget, not a lower
bound on Erdős–Szekeres numbers.

| Step | Lean correspondence |
| --- | --- |
| Convex-subset density | `ErdosSzekeres.Suk.convex_subsets_density` in [ExtractionCounting](ErdosSzekeres/Suk/ExtractionCounting.lean) |
| Product and fan estimates | `support_product_bound` in [RegionProduct](ErdosSzekeres/HMPT/RegionProduct.lean), `convex_family_ratio_bound` in [FanCounting](ErdosSzekeres/HMPT/FanCounting.lean); geometry in [ProjectedCaps](ErdosSzekeres/HMPT/ProjectedCaps.lean) and [ConvexFan](ErdosSzekeres/HMPT/ConvexFan.lean) |
| Two scales | `convex_two_scale_ratio_bound`, `two_scale_bound` in [TwoScale](ErdosSzekeres/HMPT/TwoScale.lean) |
| Entropy and floor interface | `twoScaleProduct_le_common_entropy`, `real_entropy_two_scale_bound` in [Entropy](ErdosSzekeres/HMPT/Entropy.lean) |
| Rounded input and limits | `asymptoticScale`, `roundedScale`, `scaleInputExponent` and their limits in [AsymptoticInput](ErdosSzekeres/HMPT/AsymptoticInput.lean), [ScaleLimits](ErdosSzekeres/HMPT/ScaleLimits.lean) |
| Slack and conclusion | `budgetRatio_identity`, `normalizedBudget_tendsto`, `eventual_bound_of_positive_slack`, `theorem2020` in [Asymptotic](ErdosSzekeres/HMPT/Asymptotic.lean) |
| Fixed-scale barrier | `leading_slack_identity`, `positive_leading_slack_iff` in [ParameterBarrier](ErdosSzekeres/HMPT/ParameterBarrier.lean) |

Except in the first row, declaration names have prefix `ErdosSzekeres.HMPT`.

### 4.4. Finite binomial and factorial refinements

Retaining $`c_{m+1}(P)\le\binom N{m+1}`$ improves (4.6) by replacing
$`N^{m+7}\Pi`$ with $`T_{\mathrm{bin}}=\binom N{m+1}N^6\Pi`$, under the same
hypotheses. This expression is no larger, and strictly smaller for $`N>0`$,
$`m\ge1`$.

For a closed integer bound, set

```math
\begin{gathered}
K=4m+1,\quad D=3m-6,\quad V=\lceil\log\Pi(m,n)\rceil,\\
A=(d+1)K+V,\quad F=\lfloor\log((m+1)!)\rfloor.
\end{gathered}
```

```math
\begin{aligned}
E_0&=\max\left\{d,2K,\left\lfloor A/D\right\rfloor+1\right\},\\
E_!&=\max\left\{d,2K,\left\lfloor\max(A-F,0)/D\right\rfloor+1\right\}.
\end{aligned}
```

For $`m\ge3`$, $`n\ge4`$, $`K\le2^d`$ and $`\mathsf F(2^d,K)`$,

```math
\mathsf F(2^{E_!},n),\qquad E_!\le E_0.                  \qquad\text{(4.9)}
```

The credit comes from $`(m+1)!\binom N{m+1}\le N^{m+1}`$. More generally,
for nonnegative integers $`E,V`$ with $`\Pi(m,n)\le2^V`$, the same input hypotheses and

```math
d\le E,\quad 2K\le E,\quad (d+1)K+V\lt DE+\lfloor\log((m+1)!)\rfloor
```

imply $`\mathsf F(2^E,n)`$. Multiply the counting inequality by the factorial,
compare powers using $`2^F\le(m+1)!`$, and cancel that positive factor.
Integer division applied to $`\max(A-F,0)`$ proves (4.9).

Moreover, $`2^{3m-6}\le(m+1)!`$ for $`m\ge3`$, so $`F\ge D`$; also
$`d\lt E_0`$. If $`2K\lt E_0`$, the counting term determines $`E_0`$, giving
$`E_!\lt E_0`$ and hence $`\mathsf F(2^{E_0-1},n)`$. Finally the input
$`d=D_S(4m+1,a)`$ is discharged by (4.3) whenever $`a\ge2`$ and
$`4m+1\le a^3`$.

These results are `two_scale_binomial_bound`,
`integer_two_scale_factorial_bound`, `twoScaleFactorialExponent_le`,
`two_scale_factorial_exponential_bound`, `suk_two_scale_factorial_bound` in
[BinomialRefinement](ErdosSzekeres/HMPT/BinomialRefinement.lean), and
`integer_two_scale_bound_one_bit_smaller` in
[FactorialSaving](ErdosSzekeres/HMPT/FactorialSaving.lean), all under prefix
`ErdosSzekeres.HMPT`. They improve finite interfaces in this development; they do
not improve HMPT's asymptotic coefficient or establish literature priority.

## 5. Stronger residual inequalities

### 5.1. The Boolean relaxation and an exact countermodel

Fix the residual universe $`U=\{0,\ldots,153\}`$. For a literal catalog of
$`q`$ rows, write

```math
\mathcal A_q(h)\quad\Longleftrightarrow\quad
\forall r\lt q,\quad d_r\le\sum_{i\in S_r}h_i,
\qquad h:U\to\{0,1\}.                                  \qquad\text{(5.1)}
```

The 2,469-row catalog extends the residual system of §3 by additional
geometric rows and rounded cuts. Its exact supports and demands are
`OmissionResidual32Contexts.support` and `demand` in
[Catalog](experiments/omission-residual32-context-certificates-2026-10-10/Residual32ContextsProof/Catalog.lean).
`OmissionResidual32Transfer.all_rows` and `feasible_holes` in
[Transfer](experiments/omission-residual32-transfer-2026-10-10/Transfer.lean)
prove, for every actual residual configuration,

```math
\mathcal A_{2469}(h),\qquad \sum_i h_i+n=154,
\qquad h=\mathbf1_{U\setminus O(c)}.                     \qquad\text{(5.2)}
```

The implication $`\mathcal A_{2469}(h)\Rightarrow\sum h_i\ge33`$ is false.
An exact countermodel has missing set

```math
\begin{aligned}
M_* =\{&7,12,33,39,44,47,50,51,52,54,55,56,69,71,73,75,\\
       &76,77,78,90,97,99,101,109,115,117,118,119,124,127,132,133\}.
\end{aligned}
```

It has 32 elements, satisfies every old row, and has
$`h_{54}=1`$, $`h_{43}=h_{67}=h_0=0`$. The kernel checks each integer
intersection count; indicator sums equal those counts. These are
`OmissionResidual32Case4.missing_card`, `all_rows`, `sum_holes`,
`allows_thirty_two_holes`, `no_universal_thirty_three_hole_bound` in
[Witness](experiments/omission-residual32-case4-2026-10-10/Witness.lean).
This is a countermodel to a finite relaxation, not a configuration of points.

### 5.2. Coupled geometric obstructions

For occupied distinct states $`s_i`$, choose their distinct actual owners $`v_i`$
in one residual configuration. A `Coupled.Context` retains these owners,
their states and geometric hypotheses. The semantics uses the following atoms:

| Atom | Interpretation |
| --- | --- |
| `falsum` | $`\bot`$ |
| `before i j` | $`v_i\lt v_j`$ |
| `capGe i j t`, `cupGe i j t` | $`t\le a_{ij}`$, $`t\le b_{ij}`$ for the actual pair label, with its earlier owner first |
| `positive i j k` | $`[p_{v_i},p_{v_j},p_{v_k}]>0`$ |
| `convex i j k l` | The four owners are in convex position |

Positive and negative literals assert these propositions and their negations.
Each initial clause is proved from order, admissible domains, rank growth,
orientation or octagon avoidance. A checked RUP derivation proves the clauses
inconsistent: each added clause follows by unit propagation after negating
it, and the derivation ends with the empty clause. The interpretation in
[CoupledSemantics](ErdosSzekeres/Omission/CoupledSemantics.lean) ensures that
owners and pair labels cannot vary independently between clauses. Lean checks
the resulting proof terms.

For example, let

```math
S_* =\{25,43,53,65,74,85,89,91,96,107,110,111,125\}.
```

**Proposition 5.1 (Sixth obstruction).** Every residual configuration satisfies
$`\vert S_*\setminus O(c)\vert\ge1`$.

*Proof.* Simultaneous occupation would supply a context satisfying the refuted
formula. Thus some state is missing. ∎

The declarations are `CoupledCoreSixth.context_impossible` in
[LeanCore](experiments/omission-residual32-witness-coupled-2026-10-10/LeanCore.lean)
and `exists_missing_state`, `hole_bound` in
[Geometry](experiments/omission-residual32-witness-coupled-2026-10-10/Geometry.lean),
with prefix `ErdosSzekeres.Omission`. Since $`S_*\cap M_*=\varnothing`$, this
row strictly strengthens the old conjunction and proves that the exact
occupied set $`U\setminus M_*`$ is not realizable (`strict_strengthening`,
`countermodel_not_realizable`).

### 5.3. Transporting obstructions

For an injection $`\sigma:\{0,\ldots,12\}\to U`$, define

```math
D_\sigma(i,j)=\bigl(I(\sigma(j))\setminus I(\sigma(i))\bigr)
 \setminus\{(1,6)\}.
```

Here $`I(s)`$ means the positive cells of profile $`s`$. A template's
**compatibility** predicate consists of specified empty-domain tests,
excluded-label tests and positive-orientation tests. These are exact finite
lists, not merely a condition on the cardinality of the image.

The Fourth template uses the lists `emptyTests`, `domainTests`, `positiveTests`
in [CoupledTemplateFourth](ErdosSzekeres/Omission/CoupledTemplateFourth.lean).
The relaxed Sixth template uses

```math
\begin{aligned}
E&=\{(1,0),(10,6),(12,10),(12,11)\},\\
D&=\{(10,11,a,b):a\in\{2,3\},\ b\in\{4,5,6\}\}.
\end{aligned}
```

and the exact 31-triple list `positiveTests` in
[SixthRelaxedTemplate](experiments/omission-residual32-sixth-relaxed-2026-10-10/SixthRelaxedTemplate.lean).
Writing that list as $`Q`$ and the six-order sign check of §2.3 as $`P`$,
compatibility means

```math
\begin{aligned}
(i,j)\in E&\Rightarrow D_\sigma(i,j)=\varnothing,\\
(i,j,a,b)\in D&\Rightarrow(a,b)\notin D_\sigma(i,j),\\
(i,j,k)\in Q&\Rightarrow P(\sigma(i),\sigma(j),\sigma(k)).
\end{aligned}
```

**Proposition 5.2 (transport).** For either template, every injective compatible
map satisfies $`\vert\mathrm{image}(\sigma)\setminus O(c)\vert\ge1`$.

*Proof.* Choose distinct owners if the image is occupied. Compatibility
justifies every state-dependent clause of the template refutation; the
remaining clauses hold for all actual contexts. The refutation contradicts
simultaneous occupation. ∎

This is `CoupledTemplateFourth.hole_bound` in
[CoupledTemplateFourthGeometry](ErdosSzekeres/Omission/CoupledTemplateFourthGeometry.lean),
and `CoupledTemplateSixthRelaxed.context_impossible`, `hole_bound` in the
[relaxed template](experiments/omission-residual32-sixth-relaxed-2026-10-10/SixthRelaxedTemplate.lean)
and its [geometry module](experiments/omission-residual32-sixth-relaxed-2026-10-10/SixthRelaxedTemplateGeometry.lean),
all under `ErdosSzekeres.Omission`.

The checked catalogs append the Sixth support and 128 Fourth images to obtain
$`\mathcal A_{2598}`$, then 48 relaxed Sixth images to obtain
$`\mathcal A_{2646}`$. Their `checked` theorems establish injectivity and
compatibility, and `all_rows` proves necessity for the same $`O(c)`$:

| Family | Literal maps and geometric correspondence |
| --- | --- |
| Fourth images | `CoupledFourthGlobalVariants.maps`, `checked`, `all_rows` in [FourthGlobalProof](experiments/omission-residual32-fourth-global-variants-2026-10-10/README.md) |
| Ordered first 129 additions | `Residual32AddedRows.literal_binding`, `all_rows` in [AddedRows](experiments/omission-residual32-added-rows-2026-10-10/AddedRows.lean) |
| Relaxed Sixth images | `CoupledSixthRelaxedVariants.maps`, `checked`, `all_rows` in [SixthRelaxedProof](experiments/omission-residual32-sixth-relaxed-2026-10-10/README.md) |

The Fourth family is not claimed exhaustive. Each of the 48 later supports
passes a finite test for nonimplication by any single previous row; this
observation alone is not used as a budget-constrained independence result.

## 6. Rank attainment, further rows and the remaining problem

### 6.1. A bound from the source profile

Let
$`H_u=\max(\{0\}\cup\{d_R(t,u)_2:t\lt u\})`$.
If there is no six-cap, the first label coordinate is positive, so this
is exactly the first column height of the incoming state.

**Lemma 6.1 (source cup bound).** For $`u\lt v\lt n`$,

```math
d_R(u,v)_2\le H_u+1.                                    \qquad\text{(6.1)}
```

*Proof.* Let $`r=E_+(u,v)`$, attained by an ending cup. A two-point path gives
$`d_R(u,v)_2=1`$. Otherwise its prefix ends with some $`(t,u)`$ and has length
$`r-1`$. Hence $`H_u\ge E_+(t,u)-1\ge r-2`$, proving the inequality. ∎

This raw result needs neither eight-cup nor junction avoidance; it also holds
for arbitrary Boolean triple colorings when paths check consecutive triples.
Geometric transitivity is only needed to identify those paths with cups.
For an actual residual owner state $`s_u`$, its first height equals $`H_u`$.
Thus an ordered pair of owners $`i,j`$ satisfies the clause

```math
\neg\mathrm{before}(i,j)\ \lor\
\neg\mathrm{cupGe}(i,j,s_i(0)+2).
```

The order is chronological, not catalog order. The exact declarations are
`ResidualRankAttainment.cup_label_le_source_height_succ`,
`cup_label_le_source_shape_succ` and
`Configuration.residual_cup_label_le_source_shape_succ` in
[RankAttainment](experiments/omission-residual-rank-attainment-2026-10-10/RankAttainment.lean),
and `Coupled.Context.edge_cup_le_source_shape_succ`, `source_cup_clause`,
`source_cup_domain_clause` in
[CoupledDomain](experiments/omission-residual-rank-attainment-2026-10-10/CoupledDomain.lean),
all under prefix `ErdosSzekeres.Omission`. The last theorem excludes any label
$`(a,b)`$ with $`s_i(0)+1\lt b`$ in that direction.

### 6.2. Four additional omission rows

Define

```math
\begin{aligned}
W_1&=\{33,43,53,65,74,77,85,89,91,96,107,110,125\},\\
W_2&=\{1,2,7,12,18,20,27,30,33,34,39,43,53\},\\
W_3&=\{33,43,53,65,75,77,87,89,91,99,110,111,118\},\\
W_4&=\{1,11,23,24,30,33,34,39,50,56,67,77\}.
\end{aligned}
```

**Proposition 6.2.** Every actual residual configuration satisfies
$`\vert W_t\setminus O(c)\vert\ge1`$ for $`1\le t\le4`$.

*Proof.* The owner interpretation of §5.2 satisfies each initial clause of
the corresponding checked refutation. The second and fourth proofs also
use source-cup clauses from Lemma 6.1. Simultaneous occupation is impossible. ∎

For each suffix `One`, `Two`, `Three`, `Four`, the namespace
`ErdosSzekeres.Omission.CoupledCoreRankSearch` followed by that suffix contains
`context_impossible` in `RankCore*.lean`, and `states_injective`,
`exists_missing_state`, `hole_bound` in `RankGeometry*.lean`. These sources
and complete refutations are in the [four-core bundle](experiments/omission-residual32-rank-certificates-2026-10-10/README.md).

Append $`W_1,W_2,W_3,W_4`$ in this order to define $`\mathcal A_{2650}`$.
The [finite catalog replay](experiments/omission-residual32-rank-global-2026-10-10/README.md)
checks the unchanged prefix and four additions. Exact Boolean assignments
with 33 holes and $`h_0=0`$ satisfy each preceding conjunction but violate the
next row. Thus these are strict strengthenings at budget 33. These arithmetic
countermodel checks use exact Python integers and are distinct from the Lean
geometric proofs. The rows also eliminate a saved component of 306
single-swap-connected 33-hole assignments, not all such assignments.

### 6.3. Normalization of abstract cup labels

Lemma 6.1 narrows label domains, but the following theorem limits what that
restriction alone can achieve. On a finite index set $`\{0,\ldots,k-1\}`$,
fix profiles $`s_i`$, first heights $`H_i=s_i(0)`$,
and assume $`s_i(a-1)\le H_i`$ for $`1\le a\le4`$. Fix an injective order
$`p(i)`$, symmetric cap coordinates $`a_{ij}`$, triple signs and four-point
convexity data; denote this collection by $`F`$.

A symmetric cup labeling $`b_{ij}`$ is **valid**, written $`V(s,F,b)`$, if
$`1\le a_{ij}\le4`$, $`1\le b_{ij}\le6`$ for distinct indices, and:

- For $`p(i)\lt p(j)`$, the label belongs to
  $`I(s_j)\setminus I(s_i)`$ and differs from $`(1,6)`$.
- On $`p(i)\lt p(j)\lt p(\ell)`$, positive sign requires
  $`b_{ij}\lt b_{j\ell}`$; negative sign requires
  $`a_{ij}\lt a_{j\ell}`$.

Let $`P(F)`$ be any further condition independent of cup coordinates, including
fixed-sign, orientation-packet, four-point convexity and no-octagon constraints.

**Proposition 6.3 (clipping).** Set, for increasing pairs,

```math
\widehat b_{ij}=\min\{b_{ij},H_i+1\},\qquad
\widehat b_{ji}=\widehat b_{ij},\qquad \widehat b_{ii}=b_{ii}.
```

Validity is preserved, and therefore

```math
\begin{aligned}
&\exists F,b\,[P(F)\land V(s,F,b)]\\
&\quad\Longleftrightarrow\quad
 \exists F,b\,[P(F)\land V(s,F,b)\land\\
&\qquad\qquad \forall i,j\,(p(i)\lt p(j)\Rightarrow b_{ij}\le H_i+1)].
\end{aligned}                                            \qquad\text{(6.2)}
```

*Proof.* Decreasing a positive cup coordinate preserves target membership.
A changed value is $`H_i+1`$, above every source column, so source exclusion
persists. Clipping cannot create $`(1,6)`$: a clipped value six was already
six because the old coordinate is at most six. Bounds and symmetry persist.
For a positive increasing triple, target membership gives $`b_{ij}\le H_j`$,
so

```math
\min\{b_{ij},H_i+1\}\le b_{ij}\lt\min\{b_{j\ell},H_j+1\}.
```

Cap growth and $`P(F)`$ are unchanged. Clipping proves one implication in
(6.2); forgetting the extra bound proves the other. ∎

`ErdosSzekeres.Omission.RankNormalization` defines `Frame`, `HeightDominates`,
`Allowed`, `Valid`, `SourceBound`, `clip` and proves `allowed_clip`,
`clipped_growth`, `clip_valid`, `clip_sourceBound`, `exists_frame_iff_sourceBound`
in [Normalization](experiments/omission-residual-rank-normalization-2026-10-10/Normalization.lean).
`catalog_exists_frame_iff_sourceBound` in
[CatalogNormalization](experiments/omission-residual-rank-normalization-2026-10-10/CatalogNormalization.lean)
checks the exact catalog's height hypothesis.

This equivalence neither realizes points nor preserves equations requiring
labels to equal attained maxima. It shows that the source bound alone cannot
change satisfiability on a fixed support in this abstract model, although it
can shorten certificates. Independently, finite domain replay finds no new
empty directed domain, incompatible pair or changed bounding-box forced sign;
its data are in the [rank-attainment bundle](experiments/omission-residual-rank-attainment-2026-10-10/README.md).

### 6.4. The open implication for 313

The present sufficient arithmetic statement is

```math
\forall h:U\to\{0,1\},\qquad
\mathcal A_{2650}(h)\Longrightarrow\sum_i h_i\ge33.        \qquad\text{(OPEN)}
```

**This implication remains unproved.** If established for the exact catalog,
(5.2) would give residual population at most 121, and the proved composition
would yield $`\mathsf F(313,8)`$, since $`190+121+2=313`$. Restricting (OPEN) to
$`h_0=0`$ would also suffice: the first vertex of a nonempty actual residual
configuration occupies state zero, by `OmissionResidualZeroState.zero_mem_residualOccupied`
in [ZeroState](experiments/omission-residual32-context-certificates-2026-10-10/ZeroState.lean);
the empty case is immediate.

All current rows already have geometric necessity proofs. What remains is a
complete arithmetic exclusion, its kernel-checked certificate, literal catalog
identification and final composition. Bounded searches provide neither that
exclusion nor a current 32-hole model. A feasible model would instead require
stronger geometric information. Partial trees, unsuccessful local searches
and the elimination of one finite component do not settle (OPEN). The
[remaining-work account](docs/ES8_REMAINING.md) records the computational
status; the partial searches do not justify a completion-time estimate.

## 7. Validation and attribution

The completed results use no `sorry`, `admit`, custom mathematical axioms or
`native_decide`. Their audited dependencies are contained in the standard
Lean axioms `propext`, `Classical.choice`, `Quot.sound`. The mathematical
statements and certificate literals are authoritative; this article is an
exposition, not a separately checked translation.

| Proof scope | Validation record |
| --- | --- |
| Maintained geometric and asymptotic library | [Validation ledger](docs/VALIDATION.md), including commands and axiom audit |
| Original balanced and residual geometric rows | [Balanced record](experiments/omission-global-assembly-2026-10-10/balanced-rows-kernel-check.json); residual [cycle](experiments/omission-residual-geometry-2026-10-09/cycles-kernel-check.json) and [block](experiments/omission-residual-geometry-2026-10-09/blocks-kernel-check.json) records |
| Rounded cuts and complete arithmetic exclusions | [Certificate ledger](experiments/omission-cover-certificates-2026-10-10/README.md), with source archives and full kernel records |
| Closed real-point theorem $`\mathsf F(314,8)`$ | [Final assembly record](experiments/omission-global-assembly-2026-10-10/global-cover-314-check.json) and [axiom output](experiments/omission-global-assembly-2026-10-10/global-cover-314-axioms.txt) |
| Later residual rows and normalization | Standalone continuation checks in the [validation ledger](docs/VALIDATION.md) and source bundles linked in §§5–6 |

The large arithmetic proofs have complete preserved kernel records distinct
from the maintained-library build. The completed 314 theorem uses the
2,295-row residual catalog and excludes budget 31. Later budget-32 research
is not a premise of that theorem. The asymptotic proofs are likewise
independent of the omission-search experiments.

References and attribution:

1. Andrew Suk, *On the Erdős–Szekeres convex polygon problem*,
   [arXiv:1604.08657v2](https://arxiv.org/abs/1604.08657v2), 2016.
2. Andreas F. Holmsen, Hossein Nassajian Mojarrad, János Pach and Gábor Tardos,
   *Two extensions of the Erdős–Szekeres problem*, JEMS **22** (2020),
   3981–3995, [arXiv:1710.11415v3](https://arxiv.org/abs/1710.11415v3),
   [doi:10.4171/JEMS/1000](https://doi.org/10.4171/JEMS/1000).
3. Michael Schroeder, *Erdős–Szekeres: Upper Bounds for Convex Heptagons and
   Octagons*, supplied version-1 archive, 19 September 2026. The supplied
   DOI `10.5281/zenodo.22842891` is described as a reserved Zenodo draft;
   public resolution or peer review is not asserted. The finite catalogs,
   geometric architecture and adapted proof code are attributed in the
   [third-party ledger](docs/THIRD_PARTY.md).
4. Jineon Baek, [erdos-tuza-valtr](https://github.com/jcpaik/erdos-tuza-valtr),
   the formal combinatorial prerequisites and block theorem; imported
   revisions and adaptations are recorded in the same ledger.

The [paper correspondence](docs/PAPER_MAP.md) distinguishes direct statements
from replacement arguments. Original exposition is Apache-2.0; third-party
code and derived data retain the [documented license exceptions](docs/LICENSING.md).
No literature-priority or best-known-bound claim is made.
