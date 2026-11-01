# The centre-perturbation lemma (odd rotation orders; used for m = 3 and m = 5)

Written 1 November 2026 (UTC) for the audit of the symmetric ES(7) theorem (`AUDIT3`), and refereed with `proof.md` the
same day (`referee/NOTES.md` §4: correct). Revised for referee note R3: the reason given in (P2) for the triangle
criterion. **Status:** complete written proof, refereed, with an exact computational illustration for m = 3
(`tests/perturb3.py`). **Not Lean-checked.** Paths are relative to `cloud/es7-2026-10-19/results`, except `proof.md`,
`class_table.md`, `tests/…` and `referee/…`, which are in this directory.

## Why it is needed

The threefold and fivefold exclusions use encoders that need a **generic centre**: no line through the centre c
contains two points of S.

- **Fivefold** (`SYM5`). Both `symcnf.py 35 7 5` (certificate c5-angle, proof P1) and `symcnf_layers.py 35 7 5`
  (c5-layer, proof L1) use a *uniform* CC-system on 36 elements: the 35 points plus c as an auxiliary point. "Uniform"
  means every triple, including those with c, has a nonzero sign. The angle normal form also sorts the orbit
  representatives strictly by angle about c.
- **Threefold** (`C3a`, `C3b`, `C3-S`). The labelling sorts the points by the slope y/x in a frame whose y-axis is a
  line l through c. This needs pairwise distinct slopes, that is, no two points on a line through c.

A real symmetric set need not have a generic centre. The repository asserts in one sentence each that a symmetric
perturbation fixes this (`SYM5/README.md` §1; `C3a/README.md`, "The encoding"; `C3-S/soundness.md`, first paragraph).
The completeness review of the audit (`AUDIT3`, A8 §6) asked for an explicit statement and proof. Here it is.

For the half-turn (m = 2) no such lemma is needed or possible. The two points of a pair are always collinear with c.
The central encoder therefore models c non-uniformly, with exactly the zero triples {c, p, −p}, which general position
of S already forces (`proof.md`, Lemma 3).

## Setting

- m ≥ 3 is odd and c is a point of the plane.
- R = ρ_{2π/m} is the counter-clockwise rotation about c by 2π/m, where ρ_α denotes the rotation about c by angle α.
  This is the Lean `rotAbout c (2π/m)`.
- S is a finite set in general position with R(S) ⊆ S and c ∉ S. (R is injective, so R(S) = S.)

**Orbits.** For p ≠ c and 0 < k < m, R^k(p) ≠ p, because ρ_{2πk/m} fixes only c. So S is a disjoint union of orbits
O_j = {R^i(p_j) : 0 ≤ i < m}, j = 1..n, each with exactly m points.

**The perturbation.** For θ = (θ₁, …, θ_n) ∈ ℝⁿ define φ_θ : S → ℝ² by φ_θ(R^i(p_j)) = ρ_{θ_j}(R^i(p_j)). That is,
rotate each orbit as a whole about c by its own angle. Let S_θ = φ_θ(S).

## Lemma P (centre perturbation)

There is ε > 0 such that for every θ with max_j |θ_j| < ε:

- **(P1) Symmetry is kept.** φ_θ is injective, c ∉ S_θ, and φ_θ ∘ R = R ∘ φ_θ on S. Hence R(S_θ) = S_θ and
  |S_θ| = |S|.
- **(P2) The order type is kept.** sign orient(φ_θx, φ_θy, φ_θz) = sign orient(x, y, z) for all x, y, z ∈ S. Hence
  S_θ is in general position, and for every T ⊆ S, T is in convex position iff φ_θ(T) is. In particular S has 7 points
  in convex position iff S_θ does.
- **(P3) The centre becomes generic.** Within the cube max_j |θ_j| < ε, the set of θ for which some two distinct points
  of S_θ are collinear with c is contained in finitely many hyperplanes {θ_l − θ_j = const}, j ≠ l. So for all other θ
  in the cube (an open dense set of full measure), no line through c contains two points of S_θ, and S_θ ∪ {c} is in
  general position.

### Proof

**(P1).**
- Rotations about the same centre commute. For x = R^i(p_j): φ_θ(R(x)) = ρ_{θ_j}(R^{i+1}(p_j)) = R(ρ_{θ_j}(R^i(p_j)))
  = R(φ_θ(x)), since R(x) lies in the same orbit O_j.
- So φ_θ maps each orbit O_j onto the R-orbit of ρ_{θ_j}(p_j), and R(S_θ) = S_θ.
- ρ_α(x) = c only for x = c, so c ∉ S_θ.
- Let δ > 0 be the least distance between two points of S, and M = max_{x∈S} |x − c|. Then
  |φ_θ(x) − x| ≤ |θ_j|·|x − c| ≤ εM (a chord is at most the arc). If 2εM < δ, distinct points have distinct images.

**(P2).**
- For fixed distinct x, y, z ∈ S, the function θ ↦ orient(φ_θx, φ_θy, φ_θz) is continuous. Each coordinate of
  φ_θ(x) is a trigonometric polynomial in θ.
- At θ = 0 it equals orient(x, y, z) ≠ 0, by general position. So it keeps its sign on a neighbourhood of 0.
- There are finitely many triples, so one ε works for all of them (and for (P1)).
- With (P1), S_θ consists of |S| distinct points with all orientations nonzero, that is, it is in general position.
- Convex position of a set in general position depends only on the orientation signs. A finite set T in general
  position is in convex position iff no point of T is strictly inside a triangle of three other points of T (Carathéodory;
  `proof.md`, Lemma 7). Also, q is strictly inside the triangle abd iff orient(a,b,q), orient(b,d,q) and orient(d,a,q)
  are nonzero with one common sign. Indeed, by Cramer's rule the barycentric coordinates of q with respect to a, b, d
  are orient(b,d,q)/orient(a,b,d), orient(d,a,q)/orient(a,b,d) and orient(a,b,q)/orient(a,b,d); q is strictly inside
  iff all three are positive; and if the three numerators have one sign, so does their sum orient(a,b,d) (`proof.md`,
  Section 1, barycentric coordinates). Both conditions are preserved by φ_θ, in both directions.

**(P3).** Use complex coordinates with c = 0 and ω = e^{2πi/m}. Take two distinct points of S_θ,
x′ = φ_θ(ω^a·p_j) = e^{iθ_j}·ω^a·p_j and y′ = φ_θ(ω^b·p_l) = e^{iθ_l}·ω^b·p_l, with β_j = arg p_j. Then

orient(c, x′, y′) = Im(conj(x′)·y′) = |p_j|·|p_l|·sin(θ_l − θ_j + 2π(b − a)/m + β_l − β_j).

- **Same orbit (j = l, a ≢ b mod m).** The θ's cancel and the value is |p_j|²·sin(2π(b − a)/m). This vanishes iff
  2(b − a)/m ∈ ℤ, iff m | 2(b − a), iff m | (b − a), since m is **odd**. That means x′ = y′, which is excluded. So two
  points of one orbit are never collinear with c, for every θ. (For even m the pair a, a + m/2 always is; this is the
  half-turn's zero triple.)
- **Different orbits (j ≠ l).** The value vanishes iff θ_l − θ_j ∈ β_j − β_l − 2π(b − a)/m + πℤ. For each of the
  finitely many choices of (j, l, a, b) this is a family of parallel hyperplanes spaced π apart. Only finitely many of
  them meet the cube, where |θ_l − θ_j| < 2ε. Their union is closed and nowhere dense, with measure zero.
- An explicit choice: θ_j = j·η with small η > 0. The bad conditions say (l − j)·η lies in a finite set of values in
  (−2ε, 2ε), and they exclude only finitely many η. ∎

**Variant.** The proof uses only two facts: each φ restricted to an orbit commutes with R, and it is close to the
identity. So "rotate orbit j by θ_j" can be replaced by "multiply orbit j (about c) by a complex number λ_j close to 1",
a rotation-scaling. The exact illustration below uses λ_j = 1 + η_j·ω, which keeps the coordinates rational in the
Eisenstein basis.

## Corollary (reduction to a generic centre)

Let (m, N) = (3, 33) or (5, 35). Suppose every set S′ with all of the following properties contains 7 points in convex
position:

- |S′| = N and S′ is in general position;
- R(S′) = S′ and c ∉ S′;
- no line through c contains two points of S′.

Then every set S with |S| = N, in general position, with R(S) = S and c ∉ S, contains 7 points in convex position.
That is, the Lean class `Threefold33` (for m = 3) and `Fivefold35` (for m = 5) holds.

*Proof.* Given S, choose θ as in (P3), inside the cube of (P1) and (P2). By (P1), (P2) and (P3), S′ = S_θ satisfies the
hypothesis, so it has a convex 7-subset φ_θ(T). By (P2), T ⊆ S is in convex position. ∎

The labellings and normal forms of the encoders are then applied to S′, not to S. Every fact that the normal forms
derive from the order type of the points, such as hull vertices, convex layers and the C3-S hull cases, is the same for
S and S′ by (P2). The signs of triples **through c** may change. That is the point of the lemma: zero values become
nonzero.

## What else the encoders' frames need (no perturbation required)

**Threefold.** Besides a generic centre, the C3a/C3b frame needs a line l through c with two properties:

- (i) l contains no point of S (all x-coordinates nonzero, as required for φ(x, y) = (y/x, 1/x));
- (ii) l is parallel to no segment of S (pairwise distinct x-coordinates, as used by the x-order and inversion
  variables).

C3-S Lemma 2(a) also turns l to a direction "just before" the line through a chosen point. Each of (i), (ii) excludes
finitely many directions: the directions of the lines through c and a point of S, and of the segments of S. So
admissible directions are dense, and l can be placed in any open interval of directions. `AUDIT3` (A2) noted that (ii)
is used but not stated as a WLOG step (finding A2-F3). This paragraph supplies it.

**Fivefold.** Nothing beyond a generic centre is needed:

- The sector representatives of the angle normal form lie strictly inside the open 72° sector after the ray c → X₀. A
  point on a boundary ray would be collinear with c and X₀ or with c and R(X₀).
- Two representatives have distinct angles. Equal angles would put them on one ray from c.
- The centre facts χ(c, a, R^k a) = + for k = 1, 2 and − for k = 3, 4 hold for every R-invariant set, by the same-orbit
  computation above: the angle at c is 2πk/5.

**Mirror classes.** No perturbation is needed. The mirror encoder's zero triples {Z, L_i, R_i} (Z = the point at
infinity perpendicular to the axis) are exactly the forced ones. Two points of different pairs at the same height would
give three collinear points of S (`SYMZ/README.md` §1, fact 1). This concerns the SAT confirmation of the mirror
classes; the classes themselves are proved in Lean from Baek's theorem (`SYMLEAN/mirror`, `class_table.md` §2).

## Exact illustration (`tests/perturb3.py`, `tests/logs/perturb3.log`)

This is not part of the proof. For m = 3 in Eisenstein coordinates (rational, exact; the orientation sign equals the
Euclidean one because the coordinate map has determinant √3/2 > 0):

- **Test sets.** Random R-invariant sets in general position. Each contains one or two pairs of orbits whose
  representatives lie on a common line through c (the second representative is k times the first, k ∈ {±2, ±3}), so
  that 3 or 6 pairs of points are collinear with c before the perturbation.
- **Perturbation.** Orbit j is multiplied by 1 + j·η·ω, with η halved from 1/50 until all checks hold.
- **Checks, all exact:**
  - the result is R-invariant;
  - every orientation sign of the points is unchanged;
  - no pair is collinear with c afterwards;
  - the number of convex k-subsets (k = 5 or 6) is unchanged.

**Result:** `PERTURBATION CHECK PASSED on 30 sets`, with 9 to 18 points, 3 or 6 pairs collinear with c before and 0
after. The final η ranged from 1/50 to 1/1600. All orientation signs and convex-subset counts were unchanged.

## Remaining gap

Lemma P is a written proof only. A Lean formalization (estimated in `AUDIT3`, A8 §6, at 1–3 days) would connect the Lean
classes `Threefold33` and `Fivefold35` to statements with a generic centre. The encoders' CNF soundness for those
statements remains a written argument in their own documents (`class_table.md`).
