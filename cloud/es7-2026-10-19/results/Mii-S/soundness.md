# Soundness of the hull-pair split and of the layer split

`F` is `m33k7int.sub.cnf` (sha256 `69c1dc8f…ffff932d`): points 1..33 sorted by x, pairs
i ↔ 34−i, axis point 17, `X(i,j,k)` true = counter-clockwise, orientation orbits identified,
the two "17 is not extreme" clauses, and the unit `X(1,2,3)`.

There are two independent soundness arguments. Either one is enough.

1. **Certificate-based (no geometry needed).** Every added clause comes with a SAT
   certificate that the cases cover `F`. The cover lemmas below are themselves UNSAT claims about
   explicit CNFs, checked with cake_lpr. This argument is about the CNF's models
   (signotopes), so it composes directly with `Mir.interiorCnf_satisfiable`.
2. **Geometric.** Every real configuration of sub-case (ii) satisfies `F` and the cube of
   exactly one case. This is the argument the random tests exercise.

## Notation

`orient(p,q,r) > 0` means counter-clockwise (ccw). In `F` it is the literal `ccw_lit(p,q,r)`:
`±X(sorted triple)`, with the sign given by the parity of the sorting permutation, then mapped
to its orbit representative (`hullsplit.ccw_lit`).

## The split (layer 1 = hull)

A case is `(U, L)`. Here U and L are disjoint sets of pair labels in 2..16 with
1 ≤ |U| + |L| ≤ 2: 30 cases with one extra pair and 420 with two, 450 in all.
The hull in ccw order is
`1, l1, l2, …, 34−l2, 34−l1, 33, 34−u_k, …, 34−u1, u1, …, u_k`, with `l1 < l2` and
`u1 < u2`. The lower chain runs left to right and then the upper chain right to left
(`hullsplit.hull_ccw`). The cube `cube(U,L)` consists of:

- (a) for every hull edge `(h_t, h_{t+1})` and every other point `r`: `orient(h_t,h_{t+1},r) > 0`;
- (b) for every ccw-ordered triple of hull vertices: ccw;
- (c) for every upper vertex v and every i < v < k: `X(i,v,k)` false, i.e. v is above the
  chord ik. For a lower vertex, `X(i,v,k)` is true.

Each case CNF is `F` plus the cube's units (`hullsplit.py case`, or `layers.py case`). The
X(1,2,3) unit is kept, and both above/below placements are enumerated, so the y-flip is
used exactly once (by `F` itself, as in results/C and H3).

### Geometric argument

Let S be 33 points in general position, symmetric in a line, with no convex 7-gon, and with
the axis point c in the interior of conv(S∖{c}).

1. H3 gives the normal form (`Mir.interiorTieBreak`, `Line.lean`): a rigid motion makes the
   axis the y-axis. Then a projective map `(x,y) ↦ (x,y)/(1+εy)` commutes with the reflection,
   keeps all orientation signs, and separates the x-coordinates. Sorting by x gives P_1..P_33
   with P_{34−i} = reflX(P_i) and c = P_17, and `F`'s model is this enumeration's orientation
   assignment. If X(1,2,3) is false, apply (x,y) ↦ (x,−y) first. It commutes with the
   reflection, keeps x-order, general position, interiority and convex position, and makes
   X(1,2,3) true. So WLOG the assignment satisfies `F`.
2. P_1 and P_33 have the smallest and largest x, so they are hull vertices. They have equal y, so the
   chord P_1P_33 is horizontal.
3. The vertex set V of conv(S) is reflection-invariant, and c ∉ V. So V∖{P_1,P_33} is a union of
   mirror pairs. A pair at the height of the chord would put 4 points on a line, so each pair is
   strictly above the chord (upper chain) or strictly below it (lower chain).
4. V is in convex position, so |V| ≤ 6. |V| is even and at least 3, so |V| ∈ {4, 6}. This gives
   exactly the (U, L) list. Along each chain the vertices are in x-order, which gives the ccw
   order stated above.
5. (a) S ⊂ conv(V), and no 3 points of S are collinear, so every point other than p,q is strictly
   left of each ccw edge (p,q). (b) This is convex position in ccw order. (c) An upper
   vertex v ≠ P_1,P_33 has a non-vertical supporting line ℓ through it, with S∖{v} strictly
   below ℓ. Any chord P_iP_k with x_i < x_v < x_k is then strictly below ℓ at x_v, so v is above
   it, which gives orient(P_i,v,P_k) < 0. Lower vertices are symmetric.
6. Every cube literal is on orbit representatives. That is valid because X(i,j,k) =
   X(34−k,34−j,34−i) holds for the enumeration (H3 `assn_subVar`).

So the assignment satisfies `F ∧ cube(U,L)` for the (U,L) read off from conv(S). If every
case CNF is UNSAT, sub-case (ii) has no realisation.

### Certificate argument (`cover.py`, checked with cake_lpr)

`UP(U)`: for each edge v→q of the left half of the upper chain 1, u1, …, u_k, 34−u_k (the
crossing edge included), `orient(v,q,r) < 0` for every other r. The right half is the mirror
image and has the same orbit literals.

- `root`: `F + {¬UP(U) : U ⊆ 2..16, |U| ≤ 2}` (121 blocking clauses) is UNSAT.
  So every model of F satisfies some UP(U).
- `up:U` for each of the 121 U: `F + UP(U) + {¬cube(U,L) : (U,L) a case}` is UNSAT. So every
  model of F ∧ UP(U) satisfies some cube(U,L).
- Each case `F + cube(U,L)` is UNSAT.

Then F is UNSAT. Take a model ν. By `root` it satisfies some UP(U), by `up:U` some cube(U,L),
and that contradicts the case. Nothing geometric is used. The lemma that is needed is a
"clause cover" version of H3's `not_dimacsSatisfiable_of_cover` (see `shard_plan.md`).

A single flat cover CNF (`F` + all 450 blocking clauses) did not finish in 1,480 s of
CaDiCaL. The 2-level form is what makes it cheap: root took 130 s (proof 199 MB, cake_lpr 25 s).

## Layer split (layer 2 and deeper, `layers.py`)

Remove layer 1's vertices. The remaining points R are still reflection-symmetric with the
axis point in R, and they still have no convex 7-gon. Their hull (layer 2) has ≤ 6 vertices:

- its leftmost/rightmost points are p = min R and 34−p, at equal height;
- the other vertices are pairs strictly above or below chord p(34−p), and possibly the axis point
  17. This time 17 can be a vertex: the top one (`T`, above the chord) or the bottom one (`B`),
  never both, since there is only one axis point;
- 3 ≤ 2 + 2(|U2|+|L2|) + [17 ∈ V2] ≤ 6, which gives the `next_cases` list (392 options below a
  4-gon layer 1, 338 below a 6-gon layer 1).

The cube adds (a)–(c) for layer 2, with r and the chords restricted to R. The proofs of
(a)–(c) are the same as for layer 1, applied to the point set R, which is itself in general
position. For 17 as a top vertex, the supporting-line argument of (c) applies to 17 itself.
Deeper layers repeat this with the remaining points, and the axis option is dropped once 17
has been used.

The certificate version (`cover2.py`) is the same 2-level scheme relative to the parent cube:
- `P|up`: F + cube(P) + {¬UPR(U,T)} UNSAT;
- `P|up:U:T`: F + cube(P) + UPR(U,T) + {¬cube(P+child)} UNSAT.

Tested for P = `8/`: `8/|up` UNSAT in 67 s, `8/|up:3:-` 13 s, `8/|up::T` 11 s (no proof
written for these three).

## Random tests

- `test_split.py` (`test_split_report.json`): 2,000 sets with a random 4- or 6-gon mirror hull
  and 1,000 uniform mirror sets with an interior axis point. In every one:
  - the set's assignment, y-flipped where needed, satisfies all 163,443 orientation-only clauses of F;
  - exactly its own case cube is satisfied, among all 450. A uniform set whose hull has more than
    6 vertices satisfies none; 148 of the 1,000 uniform sets had a hull of at most 6 vertices.
  - Failures: 0. Distinct cases hit: 279.
- `test_layers.py` (`test_layers_report.json`): 2,000 sets with a random layer 1 and a random
  symmetric layer 2 of 3–6 vertices (axis on it for 979 of them). Both layers are recomputed by
  monotone chain. In every set:
  - the orientation-only clauses of F hold;
  - exactly the right layer-1 cube holds among 450;
  - exactly the right layer-2 cube holds among the next-layer options.
  - Failures: 0. Distinct specs: 1,207.
