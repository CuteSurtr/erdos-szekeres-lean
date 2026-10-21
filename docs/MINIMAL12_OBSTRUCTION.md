# A twelve-point minimal nonrealizability obstruction with threefold symmetry

Technical note — 22 October 2026

We give an explicit uniform acyclic rank-three oriented matroid on twelve
elements that is not realizable over the reals, although every proper minor
is realizable. It has a free threefold symmetry and no abstract convex
heptagon. Four comparisons of determinant orbit products prove
nonrealizability; their expansion uses 24 ordinary Grassmann–Plücker
inequalities. Four small integer coordinate tables prove deletion-minimality.
The data and an offline exact verifier accompany this note.

**Status.** This is a reproducible example and a realizability filter for the
present Erdős–Szekeres search. Minimal nonrealizable oriented matroids and
product certificates are classical. The example is distinct from the two
specific constructions compared below, but historical novelty of its
reorientation class or short certificate is **not established**. No new
general bound for ES(7), completed 33-point exclusion, or Lean formalization
is claimed.

## 1. The order type and its proper deletions

For distinct planar points, write $[abc]$ for the determinant of their
homogeneous coordinates $(1,x,y)$ and $\chi(a,b,c)$ for its sign. An abstract
order type specifies these signs subject to the rank-three chirotope axioms
and acyclicity. A subset is *abstractly convex* if none of its four-element
circuits places one element inside the triangle of the other three.

**Theorem.** There is a uniform acyclic rank-three oriented matroid $M$ on

```math
V=\{0,2,3,4,8,10,11,12,16,18,19,20\}
```

with maximum abstract convex subset size six, a free orientation-preserving
action of $C_3$, and the following properties:

1. $M$ is not realizable over the reals.
2. Every proper minor of $M$ is realizable.
3. The permutation group preserving the reorientation class of $M$ is
   isomorphic to $S_3$.

The following table defines $\chi$ without a separate 220-entry sign list.
Each column is an independent eleven-point coordinate configuration; a dash
marks the omitted label. For any triple, use its determinant sign in any
column containing that triple. There is always such a column, and the
columns agree on every overlap.

| Label | Delete 0 | Delete 2 | Delete 3 | Delete 4 |
| --- | --- | --- | --- | --- |
| 0 | — | (-12, 14) | (-10, 25) | (-20, 5) |
| 2 | (32, 7) | — | (40, -19) | (24, -3) |
| 3 | (-37, 3) | (-29, -4) | — | (-39, -5) |
| 4 | (-17, -27) | (-23, -16) | (-66, -7) | — |
| 8 | (13, 10) | (8, 7) | (25, 11) | (12, 5) |
| 10 | (-16, -30) | (-14, -36) | (-34, -31) | (-20, -26) |
| 11 | (7, 33) | (3, 29) | (29, 46) | (12, 19) |
| 12 | (1, 29) | (-6, 35) | (23, 45) | (6, 19) |
| 16 | (2, -17) | (-4, -17) | (4, -25) | (-8, -20) |
| 18 | (-28, 16) | (-10, 40) | (3, 52) | (-18, 24) |
| 19 | (19, -24) | (13, -25) | (16, -65) | (10, -28) |
| 20 | (26, -6) | (22, -20) | (31, -33) | (20, -9) |

All 660 determinants are nonzero. The minimum absolute determinants in the
four columns are respectively 4, 12, 11 and 6. Direct comparison gives
the orientation-preserving permutation

```math
\tau=(0\;16\;8)(2\;18\;10)(3\;19\;11)(4\;20\;12)
```

and the orientation-reversing permutation

```math
\rho=(2\;19)(3\;18)(4\;12)(8\;16)(10\;11),
\qquad \rho\tau\rho=\tau^{-1}.
```

Relabel a coordinate column by $v\mapsto\tau^k v$, keeping the coordinates
the same. The four omissions represent all four $\tau$-orbits, so these
relabelings realize all twelve single-element deletions. Every proper
restriction lies in one of them. The rank-three exchange axioms involve at
most six labels, and acyclicity here is determined by four-element circuits;
each such check lies in a realizable deletion. Thus the well-defined sign
table is indeed a uniform acyclic rank-three oriented matroid. The verifier
also checks the exchange axioms directly.

The supporting-edge hull cycles are

```math
(2,11,18,3,10,19),\qquad(4,20,12),\qquad(0,16,8).
```

The outer layer is a convex six-set. Of the 495 four-subsets, 111 have an
interior-point circuit. Each of the 792 seven-subsets contains at least one
of these witnesses, so none is abstractly convex. These finite assertions
are checked exactly from the displayed coordinates, with no catalog lookup.

Finally, a proper minor involving a contraction has rank at most two. Every
oriented matroid of rank at most two is realizable, allowing parallel
elements and loops. Together with the deletion realizations, this proves
assertion 2 once nonrealizability is established.

## 2. Four product inequalities

Suppose a realization existed. The Grassmann–Plücker identity is

```math
P_0+P_1+P_2=0,\qquad
P_0=[abc][ade],\quad P_1=-[abd][ace],\quad P_2=[abe][acd].
```

The unique minority-sign term has absolute value equal to the sum of the
other two. General position therefore makes it strictly larger in absolute
value than either other term. The sign table gives:

| Anchor $a$ | Other labels $(b,c,d,e)$ | Signs of $(P_0,P_1,P_2)$ | Comparison |
| --- | --- | --- | --- |
| 0 | (2,3,4,12) | $(+,-,+)$ | $\lvert P_1\rvert>\lvert P_2\rvert$ |
| 2 | (3,18,19,20) | $(+,-,+)$ | $\lvert P_1\rvert>\lvert P_2\rvert$ |
| 2 | (8,12,18,20) | $(-,-,+)$ | $\lvert P_2\rvert>\lvert P_0\rvert$ |
| 4 | (0,2,3,19) | $(+,+,-)$ | $\lvert P_2\rvert>\lvert P_0\rvert$ |

Let $G=\langle\tau,\rho\rangle$, of order six. For an unordered triple $T$,
define the positive orbit product

```math
X_T=\prod_{g\in G}\lvert[gT]\rvert.
```

Reindexing gives $X_{gT}=X_T$. This is an identity between products; no
equality of individual determinant magnitudes or geometric realization of
the symmetry is assumed. Put

```math
\begin{aligned}
A&=X_{\{0,2,4\}}, & B&=X_{\{0,2,12\}}, & C&=X_{\{0,3,4\}},\\
D&=X_{\{0,3,12\}}, & E&=X_{\{2,4,10\}}, & F&=X_{\{2,3,4\}},\\
H&=X_{\{2,10,20\}}.
\end{aligned}
```

Multiply each displayed comparison over its six images under $G$. The
three GP term signs are preserved even by $\rho$, since each term contains
two bracket factors. Orbit identities, with a common positive factor
cancelled in the second row, give

```math
AD>BC,\qquad E>F,\qquad CH>DE,\qquad BF>AH.
```

Their product asserts $ABCDEFH>ABCDEFH$, a contradiction. This proves
assertion 1 for ordinary real realizations, without a metric symmetry
assumption. The expanded certificate has 24 unit-coefficient comparisons
and cancels exactly on 48 distinct ordinary bracket factors.

## 3. A four-orbit realizability filter

The expanded proof uses 84 bracket signs, forming 28 $C_3$-orbits. Split
$G$ into the two cosets of $\langle\tau\rangle$: four original and four
reflected seed comparisons, each translated three times, give the same
24-row contradiction.

The file [c3-cut.json](certificates/minimal12/c3-cut.json) lists the 28
required signs and eight seed comparisons. Its label $3i+t$ means phase
$t$ of orbit $i$, and its generator increments $t$ modulo three. Thus any
realizable general-position order type with four free, orientation-preserving
$C_3$-orbits must
violate at least one listed requirement. The negated conjunction is a sound
28-literal clause; global sign reversal gives another sound clause.

**The target requires only $C_3$ symmetry.** All signs needed by the reflected
rows are explicit requirements, not deductions from a reflection of the
target. No minimum-length or search-speed claim is made. The cut excludes
the source candidate but does not show that every remaining candidate
contains this pattern.

## 4. Comparison with prior work

Product certificates and their symmetry reduction are classical; see
Bokowski–Richter [1]. Bokowski–Sturmfels [2] already constructed infinitely
many minor-minimal nonrealizable rank-three chirotopes. The following exact
invariant distinguishes this example from their twelve-element star member.

A permutation $p$ preserves the reorientation class precisely when signs
$\gamma,\epsilon_i\in\{\pm1\}$ satisfy

```math
\chi(p(i),p(j),p(k))=
\gamma\epsilon_i\epsilon_j\epsilon_k\chi(i,j,k).
```

Contract one anchor. The other eleven projective rays have a cyclic order
invariant under reorientation up to reversal. Any admissible permutation
maps the anchor to one of twelve labels and maps these cycles by one of
eleven shifts and two directions. Hence only $12\cdot11\cdot2=264$
candidates are possible. Solving all 220 sign equations over $\mathbf F_2$
for each candidate gives exactly six permutations, of orders
$1,2,2,2,3,3$. All already preserve or reverse $\chi$ without individual
reorientation. This proves assertion 3; the complete calculation is in
[symmetry.py](certificates/minimal12/symmetry.py).

The cyclic definition of the star family in [2, p. 586] gives its
twelve-element member a faithful order-six permutation. Our group has none,
so the two are not equivalent even after relabeling and reorientation.
The six inner twelve-point patterns in the fourfold-symmetry search of
Subercaseaux–Mackey–Qian–Heule [3, §6.2] inherit an order-four permutation;
our group also has none. Their
[pinned companion encoder](https://github.com/bsubercaseaux/automatic-symmetries/blob/9e72ef6fdf7519b2204824837c2c7b7d28f285f1/encoders/erdos_szekeres.py#L40-L60)
enforces four-cycles on each layer, so the last three layers retain that
action. This comparison uses the cited preprint and encoder, not six
recovered sign tables or the full final publisher version.

The discovery workflow is also established: Scheucher [4, §§4.3.3, 5.2]
uses floating-point GP linear programs followed by exact certificate
verification and extracts smaller nonrealizable restrictions from large
candidates. Neither that workflow nor symmetry reduction is claimed here
as a new method.

The broader priority question remains open in this note. Other classical
constructions, including the Haiman–Kahn construction discussed in
*Oriented Matroids*, §8.3, have not been compared at the level of complete
sign tables. Neither a failed literature search nor a distinction from two
families establishes a new reorientation class. The useful, verified content
here is the explicit example, small deletion realizations, short certificate,
and reusable filter.

## 5. Reproduction and provenance

From the repository root, Python 3.10 or later suffices:

```sh
python3 docs/certificates/minimal12/verify.py --self-test
python3 docs/certificates/minimal12/symmetry.py
python3 docs/certificates/minimal12/verify_cut.py
```

These commands use integer arithmetic and the standard library only. The
main verifier derives all 220 signs from the four coordinate columns,
checks their overlaps, all twelve deletions, the chirotope and acyclicity
axioms, all seven-subsets, and the 24-row contradiction. Its self-test
rejects deliberately corrupted coordinates and a changed GP comparison.
The cut verifier uses only its own 28-sign data. The files can be copied to
an otherwise empty directory and run without Git, network access, Lean,
numerical optimization or a satisfiability solver.

The sign table was extracted from the saved 24-point candidate
[`model_m8_k7.json`](https://github.com/CuteSurtr/erdos-szekeres-lean/blob/c82c74c379ca81218b0eff4dacf552de055114d4/cloud/es7-2026-10-19/results/C3a/models/model_m8_k7.json).
Every reconstructed sign has been compared with that pinned source. Its
SHA-256 is recorded as provenance in
[certificate.json](certificates/minimal12/certificate.json); verification
does not rely on the source file or its surrounding search claims.

## References

1. J. Bokowski and J. Richter, *On the finding of final polynomials*,
   European Journal of Combinatorics 11 (1990), 21–34.
   [Author-hosted full text](https://science-to-touch.com/Articles/jrg/05_BFP.pdf).
2. J. Bokowski and B. Sturmfels, *An Infinite Family of Minor-Minimal
   Nonrealizable 3-Chirotopes*, Mathematische Zeitschrift 200 (1989), 583–589.
   [DOI](https://doi.org/10.1007/BF01160956);
   [institutional full text](https://gdz.sub.uni-goettingen.de/download/pdf/PPN266833020_0200/LOG_0055.pdf).
3. B. Subercaseaux, E. Mackey, L. Qian and M. J. H. Heule,
   *Automated Symmetric Constructions in Discrete Geometry*,
   arXiv:2506.00224v1 (2025), §6.2.
   [Version examined](https://arxiv.org/html/2506.00224v1#S6.SS2).
4. M. Scheucher, *On Order Types, Projective Classes, and Realizations*,
   bachelor's thesis, TU Graz (2014), §§4.3.3 and 5.2.
   [Author-hosted full text](https://scheucher.dev/files/theses/bachelors_thesis_tm_2014.pdf).
5. A. Björner, M. Las Vergnas, B. Sturmfels, N. White and G. M. Ziegler,
   *Oriented Matroids*, second edition, Cambridge University Press (1999),
   Chapter 8, §8.3. [Publisher record](https://doi.org/10.1017/CBO9780511586507.011).
