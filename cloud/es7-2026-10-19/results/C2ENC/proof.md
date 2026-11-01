# Soundness of the central encoder `zcnf.py rot` (m = 2, `--hull`)

Written 1 November 2026 (UTC) for the audit of the symmetric ES(7) theorem (`AUDIT3`). Refereed the same day
(`referee/NOTES.md`: sound, with minor documentation gaps, no blocking or major finding) and then revised to apply the
referee's findings R1–R4 and R6; `README.md` lists each change. **Status of this document:** a complete written proof,
refereed, plus computational evidence (Section 8). It is **not Lean-checked**. Every code reference below is to
`SYMZ/zcnf.py` as committed at 9cf4949a5 (unchanged since). Paths are relative to `cloud/es7-2026-10-19/results`,
except `tests/…` and `referee/…`, which are relative to this directory.

## 0. What is proved

**The object.**

| item | value |
|---|---|
| encoder | `SYMZ/zcnf.py`, SHA-256 `13d6c162a617cff6f4c164d6c921efef18ee58df0e913f6fe98f63b5213a0989` (last changed in commit 40eec333, 2026-10-29) |
| command | `python3 zcnf.py rot 17 7 --m 2 --hull -o base.cnf --map base.json` |
| base CNF | `p cnf 838032 16653336`, SHA-256 `b0061e908bff80e6a597f31a6fec1d91e8504aebc09b0bcf41c2ff21604d8ff1` |
| map | SHA-256 `2476fafff493a763fd7f2883380d359629191912a15a69bcbdfbf49bbf472b48` |

Both files were regenerated from a hash-checked copy of the encoder (33 s, 175 MB RSS). They are byte-identical to the
reference copies used by the tests of Section 8 (`tests/logs/regen_base.log`, where `REF/` stands for the directory of
those copies), and the CNF hash is the one recorded in `C2FINAL` §3 and `WRITEUP/CERTIFICATES.md` (central34-hull). The
base CNF is the formula that every central-34 unit CNF extends (`C2C34`, `C2P`, `C2FINAL`).

**Theorem 1 (soundness of the base).** Let S be a set of 34 points in the plane such that:

- S is in general position;
- S is invariant under the half-turn h(x) = 2c − x about some point c;
- no 7 points of S are in convex position.

Let p₀ be any vertex of conv(S). Then the normal-form labelling λ(S, p₀) of Section 3 exists and is unique. The
assignment α(S, p₀) of Section 4 satisfies **every** clause of the base CNF.

**Corollary 2 (cubes).** Let Q be a set of literals over the base variables (a *cube*). Let F_Q be the base CNF plus one
unit clause for each literal of Q. Define the *class* of Q as the set of pairs (S, p₀) as in Theorem 1 such that
α(S, p₀) makes every literal of Q true. If F_Q is unsatisfiable, the class of Q is empty.

Every hull and second-layer cube of the central-34 work uses only triple variables (1..2856). All 4,616 cubes in
`C2C34/cubes.txt` and `C2P/cubes/P*_cubes.txt` were checked: 613,496 literals, largest |literal| 2,856 (the referee
repeated this check). For such a cube, "α(S, p₀) satisfies Q" is a purely geometric statement about the labelled set,
by Lemma 6: every literal of Q prescribes the orientation of one triple of labelled points (or of points and c).

**Corollary 3 (covers).** Let Q₁, …, Q_n be cubes such that the base CNF plus the clauses ¬Q₁, …, ¬Q_n is
unsatisfiable (as certified for the 136 hull cubes: `central34-cover` in `WRITEUP/CERTIFICATES.md`). Here ¬Q is the
clause made of the negations of the literals of Q. Then for every (S, p₀) as in Theorem 1, α(S, p₀) satisfies at least
one Q_i. If moreover every F_{Q_i} is unsatisfiable, no such S exists.

**Corollary 3′ (covers inside a cube).** Let Q, L₁, …, L_n be cubes such that the base CNF plus one unit clause for each
literal of Q plus the clauses ¬(L₁ ∖ Q), …, ¬(L_n ∖ Q) is unsatisfiable. Then for every (S, p₀) in the class of Q,
α(S, p₀) satisfies at least one L_i; that is, (S, p₀) lies in the class of Q ∪ L_i. Under the units of Q the clauses
¬L_i and ¬(L_i ∖ Q) are equivalent, since ¬L_i has in addition only negations of literals of Q, which are false there.
So the statement also holds with ¬L_i in place of ¬(L_i ∖ Q). This is the form of the second-layer covers of the
parallelogram cases: Q is the hull cube of P_a, every subcase cube L_i contains Q, and the cover CNF is the base, the
units of Q and one clause ¬(L_i ∖ Q) per subcase (`C2C34/p8/mkunits.py`, `C2P/tools/lane.py`). (Stated after referee
finding R1.)

**Not claimed here.**

- That a satisfying assignment is realizable by points. The model is a relaxation; only UNSAT answers carry
  information.
- The geometric meaning of particular cubes (for example "the hull is the parallelogram P_a"), the hull and
  second-layer covers, reductions A and B, and the bookkeeping in `C2FINAL`. These were audited separately (`AUDIT3` A5,
  `C2FINAL`). Corollary 3 shows that the hull cover needs no geometric argument: the certificate alone places every real
  configuration in some hull cube's class. Corollary 3′ does the same for each second-layer cover inside its hull
  cube.
- Anything about the threefold, fivefold or mirror encoders (see `class_table.md` and `perturbation.md`).

## 1. Notation

- A point x = (x₁, x₂) ∈ ℝ² has the homogeneous vector v_x = (1, x₁, x₂).
- D(x, y, z) = det(v_x, v_y, v_z) is the 3×3 determinant with these vectors as rows. It equals
  (y₁−x₁)(z₂−x₂) − (y₂−x₂)(z₁−x₁), which is `ErdosSzekeres.orient x y z` (Lean indexes the coordinates x 0, x 1).
  This is a polynomial identity, checked in `tests/identities.py` (ORIENT).
- χ(x, y, z) = sign D(x, y, z) ∈ {+1, 0, −1}. A value of + means counter-clockwise.
- *Barycentric coordinates* (used in Lemma 8, Proposition 11 and `perturbation.md`). Let a, b, d be points with
  D(a, b, d) ≠ 0, and q any point. By Cramer's rule v_q = λ_a·v_a + λ_b·v_b + λ_d·v_d with λ_a = D(b, d, q)/D(a, b, d),
  λ_b = D(d, a, q)/D(a, b, d) and λ_d = D(a, b, q)/D(a, b, d), and the first coordinates give λ_a + λ_b + λ_d = 1. That
  sum is the identity D(a, b, d) = D(a, b, q) + D(b, d, q) + D(d, a, q) (`tests/identities.py`, HULL). The point q lies
  strictly inside the triangle abd iff λ_a, λ_b, λ_d > 0, that is, iff D(a, b, q), D(b, d, q) and D(d, a, q) are
  nonzero and have the sign of D(a, b, d). Equivalently, the three are nonzero with one common sign, since their sum
  D(a, b, d) then has that sign too. The equal signs come from the positivity of the coordinates; the identity alone
  gives only their sum.
- *General position*: no three distinct points of S are collinear. Equivalently, D(x, y, z) ≠ 0 for distinct
  x, y, z ∈ S. This is the Lean `GeneralPosition`.
- *Convex position*: every point of the set is a vertex of its convex hull, that is, no point lies in the convex hull of
  the others. This is the Lean `ConvexPosition` (`ConvexIndependent`). "S has no 7 points in convex position" is
  ¬`HasConvexNGon 7 S`.
- The 35 *elements* of the encoding are the indices 0..33 for the points and Z = 34 for the centre c.
  - The encoder's `pt(o, r)` is 2o + r.
  - Pair o is {2o, 2o+1}, for o = 0..16.
  - The labelling of Section 3 assigns a point X_i to each index i, with X_Z = c.
- The CNF has 838,032 variables:
  - *triple variables* 1..2856, one per class of nonzero triples (Section 4);
  - *conv variables* 2857..838032, one per canonical r-subset of the 34 points, r = 4, 5, 6 (Section 5.3).
- `lit(a, b, d)` (code lines 202–207) is the literal of the ordered triple (a, b, d). It is 0 for a zero triple.
  Lemma 6 proves that under α it is true exactly when χ(X_a, X_b, X_d) = +.

## 2. Geometry of a centrally symmetric set

Let S, c and h be as in Theorem 1.

**Lemma 1 (the centre).** c ∉ S, h restricted to S is a fixed-point-free involution, and S is the disjoint union of 17
pairs {p, h(p)}.

*Proof.*
- h is an involution of the plane, and its only fixed point is c.
- Suppose c ∈ S. Pick p ∈ S with p ≠ c. Then p, c, h(p) are three distinct points of S on one line, since
  c = (p + h(p))/2. This contradicts general position.
- So h has no fixed point in S. It maps S into S, injectively, hence onto S because S is finite. So S splits into
  2-element orbits; there are 34/2 = 17 of them. ∎

(Lean: `center_not_mem_of_halfTurn`, `halfTurn_facts`. The Lean class `HalfTurn34` assumes c ∉ S explicitly anyway.)

**Lemma 2 (vectors).** For all points x, y, z of the plane:

- (a) v_{h(x)} = A·v_x, where A has rows (1, 0, 0), (2c₁, −1, 0) and (2c₂, 0, −1). Also det A = +1 and A·v_c = v_c.
  Hence D(h(x), h(y), h(z)) = D(x, y, z), and this includes triples containing c, since h(c) = c.
  After translating c to the origin, A = diag(1, −1, −1).
- (b) v_p + v_{h(p)} = 2·v_c. Hence D(c, p, q) = ½·D(h(p), p, q), and D(c, p, h(p)) = 0.
- (c) D(c, p, h(q)) = −D(c, p, q). The two points of a pair lie on opposite sides of every line through c that
  contains neither of them.

*Proof.*
- (a) A·(1, x₁, x₂) = (1, 2c₁ − x₁, 2c₂ − x₂) = v_{h(x)}. A is lower triangular with diagonal (1, −1, −1), so
  det A = 1. A·v_c = (1, c₁, c₂) = v_c. Then det(A·[v_x v_y v_z]) = det A · D(x, y, z) = D(x, y, z).
- (b) The first part is coordinatewise. The determinant is multilinear and alternating, so
  D(c, p, q) = ½·D(p, p, q) + ½·D(h(p), p, q) = ½·D(h(p), p, q). Taking q = h(p) gives D(c, p, h(p)) = 0.
- (c) v_{h(q)} = 2v_c − v_q, so D(c, p, h(q)) = 2·D(c, p, c) − D(c, p, q) = −D(c, p, q). ∎

All of these are polynomial identities. `tests/identities.py` expands each one symbolically to the zero polynomial
(GROUP, CENTRE, ZERO, ANTI). It also checks negative controls: a reflection (det −1) and the centre identity with the
wrong sign both leave nonzero residuals (`tests/logs/identities.log`).

**Lemma 3 (zero triples).** For distinct x, y, z ∈ S ∪ {c}: D(x, y, z) = 0 if and only if
{x, y, z} = {c, p, h(p)} for some p ∈ S.

*Proof.* Reordering a triple changes only the sign of D, so assume x = c whenever c is in the triple.
- If c ∉ {x, y, z}, then D ≠ 0 by general position.
- If x = c and z = h(y), then D = 0 by Lemma 2(b).
- Let x = c and z ∉ {y, h(y)}, and suppose D(c, y, z) = 0. Then c, y, z lie on one line ℓ, and c ≠ y by Lemma 1.
  The point h(y) = c − (y − c) also lies on ℓ. So y, z, h(y) are three points of S on ℓ, and they are distinct:
  y ≠ h(y) by Lemma 1, and z ≠ y, h(y) by assumption. This contradicts general position. ∎

So the real zero triples are exactly the 17 triples {Z, 2o, 2o+1}. These are exactly the triples that the encoder's
`is_zero` (lines 126–130) declares zero: for m = 2, `tau(a) = a XOR 1`, and `is_zero(T)` holds iff Z ∈ T and the other
two elements form a pair. (`tau` is never applied to Z: `is_zero` passes to it only an element of T other than Z,
and `_uf` calls it only for p < NP.)

No perturbation or genericity assumption on c is needed for m = 2. Lemma 3 shows that general position of S already
makes c "as generic as possible": the only collinear triples through c are the forced ones {c, p, h(p)}. Compare
`perturbation.md`, which treats the odd orders, where a uniform model needs a generic centre.

## 3. The normal form (`add_sb`, `add_hull_sb`)

**Definition (normal form NF(p₀)).** A labelling i ↦ X_i of S, with X_Z = c, is in normal form with first point p₀
if:

- (N1) X₀ = p₀ is a vertex of conv(S);
- (N2) χ(c, X₀, X_{2o}) = + for o = 1..16, that is, X_{2o} lies in the open half-plane to the left of the directed
  line c → X₀;
- (N3) χ(c, X_{2o}, X_{2o'}) = + for 1 ≤ o < o' ≤ 16, that is, the representatives X₂, X₄, …, X₃₂ are sorted by angle;
- (N4) X_{2o+1} = h(X_{2o}) for o = 0..16.

**Lemma 4 (existence and uniqueness).** conv(S) has at least one vertex. For every vertex p₀ of conv(S) there is
exactly one labelling in NF(p₀).

*Proof.*
- **Vertices exist.** conv(S) is a polygon. For example, the lexicographically smallest point of S is a vertex.
  Since S is in general position with 34 points, conv(S) has at least 3 vertices. Their number is even: h is an
  isometry with h(S) = S, so it permutes the vertices, without fixed points by Lemma 1. So conv(S) has at least 4
  vertices.
- **The first pair.** Fix p₀ and set X₀ = p₀ and X₁ = h(p₀).
- **One representative per pair.** Let {q, h(q)} be one of the other 16 pairs. By Lemma 3, χ(c, p₀, q) ≠ 0, since
  q ∉ {p₀, h(p₀)}. By Lemma 2(c), χ(c, p₀, h(q)) = −χ(c, p₀, q). So exactly one point of the pair satisfies (N2).
  Call it the representative r_q.
- **Angles.** Measure angles at c counter-clockwise from the ray c → p₀. Every representative has an angle θ in
  (0, π). For two representatives r, r′:
  D(c, r, r′) = |r − c|·|r′ − c|·sin(θ(r′) − θ(r)), and θ(r′) − θ(r) ∈ (−π, π).
  So χ(c, r, r′) = + iff θ(r) < θ(r′). Two different representatives never have the same angle, since then c, r, r′
  would be collinear, which Lemma 3 excludes. So "χ(c, r, r′) = +" is a strict total order on the 16 representatives.
- **The labelling.** Label the representatives X₂, X₄, …, X₃₂ in increasing angle, and set X_{2o+1} = h(X_{2o}). This
  satisfies (N1)–(N4).
- **Uniqueness.** (N1)–(N4) determine X₀ and X₁, the choice of representative in each pair, and their order. ∎

Lemma 4 is the statement "every real centrally symmetric 34-point set in general position admits a labelling in the
normal form". It holds for every vertex of conv(S), so a configuration has exactly as many normal-form labellings as
conv(S) has vertices. The `--hull` option is valid because any point can be the first point (N2–N4 make no demand on
X₀), and conv(S) has vertices. The labelling is defined for every S as in Lemma 1. The hypothesis "no convex 7-gon" is
not used here.

## 4. Variables and the real assignment

### 4.1 The triple variables (`_uf`, lines 159–200)

The encoder builds a union-find with signs over the 6,528 nonzero sorted triples: C(35,3) = 6,545 minus 17 zero
triples. It records two kinds of relations, each of the form "χ(A) = s·χ(B)" for sorted triples A and B and a sign s.

- **(G) Group relations** (lines 166–172). For every nonzero sorted T, the encoder forms its image under
  `gen` = h (on labels, i ↦ i XOR 1 on points and Z ↦ Z; lines 91–93 and 110–114). It records
  χ(sort(hT)) = π·mult·χ(T). Here π is the parity of the sorting permutation (`parity_sort`, lines 44–47:
  the number of inversions mod 2), and `mult` = 1, because `gsign` = (1, 1) for `rot`.
  - *Valid:* χ(hT) = χ(T) as ordered triples by Lemma 2(a) and (N4), and sorting multiplies by π.
  - hT is again nonzero, since h maps the zero triples to themselves. Otherwise `_find` would raise `KeyError`; it
    did not.
- **(C) Centre relations** (lines 174–190). For every point index p and every point index q ∉ {p, h(p)}, the encoder
  records χ(sort(Z, p, q)) = s₁·s₂·χ(sort(h(p), p, q)). Here s₁ and s₂ are the parities of the two sortings, and
  `sp` = +1 (line 177).
  - *Valid:* χ(c, p, q) = χ(h(p), p, q) by Lemma 2(b), and both triples are nonzero by Lemma 3.

**Lemma 5 (the union-find is sound).** Suppose every recorded relation holds for the real labelled configuration (as an
equation between real signs). Then at the end, for every nonzero sorted triple T with `_find(T)` = (r, s), we have
χ(T) = s·χ(r).

*Proof.* Let I be the invariant "for every x with `par[x]` = (y, σ), χ(x) = σ·χ(y)".

- Initially `par[x]` = (x, 1), so I holds.
- `_find` (lines 133–146) multiplies signs along the path to the root. By I, the product s satisfies χ(x) = s·χ(root).
  Path compression sets `par[y]` = (root, s_y), where s_y is the product from y to the root (the update `sy *= sg`
  advances it one step). So I is preserved.
- `_union(a, b, s)` (lines 148–157) is called only for a recorded relation χ(a) = s·χ(b). It finds χ(a) = s_a·χ(r_a)
  and χ(b) = s_b·χ(r_b). If r_a ≠ r_b, it sets `par[r_a]` = (r_b, s_a·s·s_b), and indeed
  χ(r_a) = s_a·χ(a) = s_a·s·χ(b) = s_a·s·s_b·χ(r_b).
- If r_a = r_b and s_a ≠ s·s_b, the relations would force χ(r_a) = −χ(r_a), impossible for a nonzero real value. The
  code raises `ValueError` in that case; it did not raise when generating the base. ∎

Each class receives the number of its root, numbered in order of first appearance (lines 191–200); `tv[T]` = (v, s)
with s = the sign from T to its root. Independently of the code, the classes can be listed by hand from (G) and (C). For
t = 17 there are two types.

- **Type A** (2,720 classes): the orbits {T, h(T)} of triples of three points from three different pairs.
- **Type B** (136 classes): one class for each unordered pair of pairs P = {p, h(p)}, Q = {q, h(q)}, with 8 triples.
  With p, q the even members and s = χ(c, p, q), the signs are:

  | (c,p,q) | (c,p,hq) | (c,hp,q) | (c,hp,hq) | (hp,p,q) | (hp,p,hq) | (hq,q,p) | (hq,q,hp) |
  |---|---|---|---|---|---|---|---|
  | +s | −s | −s | +s | +s | −s | −s | +s |

There are 2,720 + 136 = 2,856 classes, exactly the encoder's `X_vars`. `tests/classes.py` checks that the encoder's map
(`base.json`, a dump of the same `tv` the clauses use, line 391) has exactly this partition and these relative signs
(`tests/logs/mapcheck_base.log`). This is a second, code-independent confirmation that no unintended identification
occurred.

Note what type B means. The 136 type-B variables are exactly the signs χ(c, X_{2o}, X_{2o'}) of the angular order
around c. The 136 SB units (Section 5.4) fix all of them.

### 4.2 The real assignment α(S, p₀)

Fix S, p₀ and the labelling X = λ(S, p₀) of Lemma 4.

- **Triple variable v:** α(v) = true iff χ(r_v) = +, where r_v is the root of class v. Equivalently, by Lemma 5,
  α(v) = true iff s_T·χ(T) = + for any (hence every) triple T in the class with `tv[T]` = (v, s_T).
- **Conv variable** of the canonical point set Q (Section 5.3): α = true iff {X_i : i ∈ Q} is in convex position.

**Lemma 6 (literal semantics).** For every ordered triple (a, b, d) of distinct elements that is not a zero triple,
the literal `lit(a, b, d)` is true under α if and only if χ(X_a, X_b, X_d) = +.

*Proof.*
- `lit(a, b, d)` = π·s·v, where (sort(a, b, d), π) = `parity_sort((a, b, d))` and `tv[sort]` = (v, s).
- The literal is true iff π·s·α(v)^± = +, where α(v)^± = +1 if α(v) is true and −1 otherwise.
- By the definition of α, α(v)^± = χ(r_v) = s·χ(sort(a, b, d)) (s² = 1).
- So the literal is true iff π·χ(sort(a, b, d)) = +, that is, iff χ(a, b, d) = +, since sorting multiplies χ by π. ∎

## 5. The clause families

`build` (lines 367–376) with `sb = True` and `hull = True` calls, in this order:
`add_gp`, `add_a4`, `add_centre_facts`, `add_kgon`, `add_sb`, `add_hull_sb`. `write` (lines 378–394) prints the
comment line, the header and the clause body, and nothing else. For each family, every clause below is satisfied by α.
A clause is satisfied unless all its literals are false; a clause "forbids" exactly the assignments that make all its
literals false.

### 5.1 Grassmann–Plücker (`add_gp`, lines 226–258): 12,588,160 clauses

**The code.**
- For every 5-set F of the 35 elements that is canonical under {id, h} (`canon`, lines 213–219: F is
  lexicographically ≤ sort(hF)), and every x ∈ F, let y₀ < y₁ < y₂ < y₃ be the other four. The encoder forms three
  terms:

  (+1, [x y₀ y₁], [x y₂ y₃]),   (−1, [x y₀ y₂], [x y₁ y₃]),   (+1, [x y₀ y₃], [x y₁ y₂]).

  A term is *zero* if one of its triples is a zero triple (`lit` = 0).
- **Fast path** (lines 239–244). If all three terms are nonzero and their six literals have six distinct variables, the
  encoder writes 16 clauses. Each 6-literal clause forbids one full assignment of the six variables. For each of the 8
  sign choices (s₁, s₂, s₃), the two clauses forbid exactly the assignments in which all three products k·χ·χ equal +1,
  and all equal −1, respectively.
  - Writing σ(l) = +1 if l is true, −1 otherwise: the first clause is false iff σ(l₁₂) = σ(l₃₄) = s₁,
    σ(l₁₃) = −σ(l₂₄) = s₂ and σ(l₁₄) = σ(l₂₃) = s₃. Then the products are +1, −(s₂·(−s₂)) = +1 and +1.
  - The second clause is false iff the products are −1, −1, −1.
  - Over the 8 choices this lists all 16 assignments with three equal products.
- **Generic path** (lines 245–257). Otherwise, let nz be the nonzero terms and V the distinct variables in them. If nz is
  empty, there are no clauses. If not, for every assignment of V under which the products of the nonzero terms do not
  contain both signs, the encoder writes the clause forbidding that assignment of V (`forbid`, lines 222–224).

**Proposition 7.** α satisfies every GP clause.

*Proof.*
- For any five vectors x, a, b, d, e of ℝ³:
  [xab][xde] − [xad][xbe] + [xae][xbd] = 0.
  This is the three-term Grassmann–Plücker relation. Project along x to ℝ³/⟨x⟩ ≅ ℝ². Each bracket [x u w] becomes a
  fixed nonzero multiple of the 2×2 determinant of the projected u and w, and for 2×2 determinants the identity is
  [AB][DE] − [AD][BE] + [AE][BD] = 0. (For x = 0 all terms vanish.) `tests/identities.py` (GP) expands it
  symbolically in 15 indeterminates to the zero polynomial; with the middle sign changed it does not vanish.
- Apply it with x and (a, b, d, e) = (y₀, y₁, y₂, y₃): the three real terms D·D sum to 0.
- By Lemma 3, a term is zero in the encoder iff it is zero in reality. So the real nonzero terms sum to 0. Hence they
  contain both signs, or there are none.
- By Lemma 6, the real signs are what α gives the literals. So α is never one of the forbidden assignments, on either
  path. ∎

Restricting to canonical 5-sets only omits clauses; it cannot affect soundness. The zero triples are handled exactly,
with no approximation, because the encoder's zero triples coincide with the real ones (Lemma 3).

### 5.2 Interiority / acyclicity (`add_a4`, lines 260–273): 413,440 clauses

**The code.** For every 4-set of the 35 elements that contains no zero triple (51,816 sets, all of them, not only
canonical ones), every t in it, with p < q < r the other three, and s ∈ {+1, −1}, the encoder writes the clause

[−s·lit(t,q,r), −s·lit(p,t,r), −s·lit(p,q,t), s·lit(p,q,r)].

It skips the clause if it contains a complementary pair, and removes repeated literals. The clause forbids
χ(t,q,r) = χ(p,t,r) = χ(p,q,t) = s together with χ(p,q,r) = −s.

**Proposition 8.** α satisfies every A4 clause.

*Proof.*
- Every vector of the encoding has first coordinate 1, including v_c = (1, c₁, c₂). For four such vectors:
  D(p,q,r) = D(t,q,r) + D(p,t,r) + D(p,q,t).
  Both sides are affine functions of (t₁, t₂) that agree at t = p, q, r, which forces equality when p, q, r are not
  collinear. In general it is a polynomial identity: `tests/identities.py` (A4) expands it symbolically.
  Without the condition "first coordinate 1" the identity is false (negative control), and the weighted form
  w_t·D(p,q,r) = w_p·D(t,q,r) + w_q·D(p,t,r) + w_r·D(p,q,t) holds in general.
- If the three right-hand terms all have sign s, then D(p,q,r) has sign s, not −s. So the forbidden pattern never occurs
  in reality.
- By Lemma 6, α gives the literals the real signs. Skipping tautologies and merging repeated literals does not change
  which assignments the clause forbids. ∎

This is where the central branch differs from the mirror branch. The mirror encoding's element Z is a point at
infinity, (0, 1, 0), and needs the weighted identity with a form w + εx that is positive on all vectors. Here no ε is
needed, because c is an affine point.

*Remark (evidence, not needed for soundness).* At t = 4, 5, 6 with no K-gon clauses and no normal form, the A4 family is
implied by the GP family together with the identifications. Forcing each of the 8,128 positive-circuit patterns that A4
forbids gives UNSAT without the A4 clauses (`tests/a4redundancy.py`, `tests/logs/a4redundancy.log`). So in this model
the A4 family appears to be logically redundant, and its absence could not be detected by any test on models
(Section 8.4).

### 5.3 No convex 7-gon (`add_kgon`, lines 275–311): 3,640,720 clauses

**The code.** Only the 34 points take part, not c.

- **Conv variables.** One for every point set Q with |Q| = r, r = 4, 5, 6, that is canonical (Q ≤ sort(hQ)
  lexicographically). They are numbered consecutively from 2857 in the order: r = 4, 5, 6, then the lexicographic
  order of `itertools.combinations` (23,256 + 139,128 + 672,792 = 835,176 variables).
- **CONV4** (138,992 clauses). For each canonical 4-set {a < b < d < e}, with literals
  L = (lit(a,b,d), lit(a,b,e), lit(a,d,e), lit(b,d,e)), and each of the six patterns returned by
  `convex4_patterns` (lines 50–63), the encoder writes [−pat₁L₁, −pat₂L₂, −pat₃L₃, −pat₄L₄, conv(Q)]. It skips
  tautologies and merges repeats. The meaning is "if Q has this sign pattern, then conv(Q)".
- **CONV5, CONV6** (139,128 + 672,792 clauses). For each canonical Q with |Q| = 5, 6, the clause is
  [¬conv(canon(Q∖x)) for x ∈ Q] ∨ conv(Q). For 680 h-invariant 6-sets (three whole pairs), the clause contains repeated
  literals, which is harmless.
- **KGON** (2,689,808 clauses). For each canonical 7-set Q, the clause is the set {¬conv(canon(Q∖x)) : x ∈ Q}.

**Lemma 7 (four-point criterion).** Let Q be a finite set in general position with |Q| ≥ 5. Then Q is in convex
position iff every (|Q| − 1)-subset is, iff every 4-subset is.

*Proof.*
- Subsets of a set in convex position are in convex position.
- Conversely, suppose Q is not in convex position. Then some p ∈ Q lies in conv(Q∖{p}). By Carathéodory's theorem in
  the plane, p ∈ conv{a, b, d} for some a, b, d ∈ Q∖{p}.
  - p is not one of a, b, d, since the points are distinct.
  - p is not on a side of the triangle, by general position.
  - So p lies strictly inside the triangle abd, and the 4-set {p, a, b, d} is not in convex position.
- Since |Q| ≥ 5, this 4-set misses some x ∈ Q, so it lies in Q∖{x}, which is then not in convex position either. ∎

**Lemma 8 (the patterns).** Let a 4-set of points in general position have a sign pattern (on its sorted triples) that
is among the six patterns of `convex4_patterns`. Then it is in convex position.

*Proof.*
- `convex4_patterns` keeps a pattern iff `n_in` = 0, where `n_in` counts the d such that O(a,b,d) = O(b,c,d) = O(c,a,d)
  for the other three a < b < c, with O the alternating extension of the pattern.
- If a real 4-set is not in convex position, one point d lies strictly inside the triangle abc of the others (proof of
  Lemma 7). Its barycentric coordinates D(b,c,d)/D(a,b,c), D(c,a,d)/D(a,b,c) and D(a,b,d)/D(a,b,c) are then positive
  (Section 1), so D(a,b,d), D(b,c,d) and D(c,a,d) all have the sign of D(a,b,c).
- So `n_in` ≥ 1 for its pattern, and the pattern is not kept. ∎

The assertion `len(convex) == 6` holds. Of the 16 sign patterns:
- the 6 patterns of 4 points in convex position (one for each cyclic order) have `n_in` = 0;
- the 8 patterns with one point inside have `n_in` = 1;
- the 2 totally cyclic, non-realizable patterns have `n_in` = 4.

So the kept patterns are exactly the six convex ones. `tests/spec.py` derives them independently, from real
quadrilaterals, and the family comparison in Section 8.2 confirms that the CNF uses exactly these.

**Proposition 9.** α satisfies every CONV4, CONV5 and CONV6 clause. If no 7 points of S are in convex position, α also
satisfies every KGON clause.

*Proof.*
- Convex position is invariant under h, an isometry. So α(conv(canon(Q′))) = [Q′ is in convex position] for every point
  set Q′. Choosing one variable per orbit is therefore consistent with α.
- **CONV4.** If the literals match a kept pattern, then by Lemma 6 the real 4-set has that pattern, by Lemma 8 it is in
  convex position, and so α(conv(Q)) is true.
- **CONV5, CONV6.** If every (r−1)-subset is in convex position, then Q is, by Lemma 7.
- **KGON.** If every 6-subset of a 7-set Q were in convex position, Q would be in convex position by Lemma 7,
  contradicting the hypothesis. So some literal ¬conv(canon(Q∖x)) is true. ∎

The CONV clauses only say "convex ⇒ conv(…) true". Given the real triple values, they force true every conv variable
that α sets true: a real convex 4-set has a kept pattern, and Lemma 7 handles larger sets. So α is the least assignment
satisfying them. Conversely, if S does have 7 points in convex position, no assignment that extends the real triple
values satisfies the CNF, since the KGON clause of that 7-set fails. This is the completeness direction, not needed for
soundness; it is what the tests in Section 8.3 observe.

### 5.4 The angular normal form (`add_sb`, lines 330–351): 136 unit clauses

For `rot` with m = 2 the units are:

- lit(Z, pt(0,0), pt(o,0)) for o = 1..16: χ(c, X₀, X_{2o}) = +.
- lit(Z, pt(o,0), pt(o′,0)) for 1 ≤ o < o′ ≤ 16: χ(c, X_{2o}, X_{2o′}) = +.

The second sector unit `−lit(Z, pt(0,1), pt(o,0))` of the docstring is emitted only for m ≥ 4 (line 336). It would be
redundant for m = 2 anyway, by Lemma 2(c). None of these triples is a zero triple (pt(0,0) = 0 and pt(o,0) = 2o are in
different pairs), so no literal is 0. The units are de-duplicated and checked for contradiction (line 348).

**Proposition 10.** α satisfies the 136 units. This is (N2) and (N3) through Lemma 6. ∎

### 5.5 The first point is a hull vertex (`add_hull_sb`, lines 353–365): 10,880 clauses

**The code.** With q = pt(0,0) = 0, for every 3-set {a < b < d} of the other 33 points and s ∈ {+1, −1}, the encoder
writes [−s·lit(a,b,q), −s·lit(b,d,q), −s·lit(d,a,q)], skipping tautologies. The clause forbids
χ(a,b,X₀) = χ(b,d,X₀) = χ(d,a,X₀) = s, that is, "X₀ lies strictly inside the triangle abd".

**Proposition 11.** α satisfies every HULL clause.

*Proof.*
- If the three signs are all s, then their sum D(a,b,d) = D(a,b,X₀) + D(b,d,X₀) + D(d,a,X₀) has sign s, so the
  barycentric coordinates D(b,d,X₀)/D(a,b,d), D(d,a,X₀)/D(a,b,d) and D(a,b,X₀)/D(a,b,d) of X₀ with respect to a, b, d
  are all positive (Section 1), and X₀ lies strictly inside the triangle abd.
- So X₀ ∈ conv(S∖{X₀}), and X₀ is not a vertex of conv(S). This contradicts (N1). ∎

32 of the 10,912 candidate clauses are tautologies and are skipped. They are the 16 triangles {X₁, X_{2o}, X_{2o+1}}
times two signs. Geometrically, X₀ can never lie inside the triangle h(X₀), p, h(p), because c lies on its side p–h(p)
and X₀ is the reflection of a vertex through c. The encoder's literals for these clauses are complementary by the
type-B identifications, consistent with this.

### 5.6 Nothing else

- `add_centre_facts` (lines 313–328) emits no clause for m = 2 (its condition is m ≥ 4; `stats.centre_units` = 0).
- `--hull` asserts `rot` and `sb` (line 375).
- So the base CNF consists exactly of the families of 5.1–5.5:
  12,588,160 + 413,440 + 138,992 + 139,128 + 672,792 + 2,689,808 + 136 + 10,880 = 16,653,336 clauses, which is the
  header count.
- No clause contains a 0 literal. Each family's construction excludes zero triples, and the streamed count equals the
  header count with every literal in range.
- `tests/spec.py` regenerates each family from the statements above and compares it with the CNF as a multiset, block
  by block in the order written: count, sum and XOR of 128-bit hashes, and length histogram. All eight families match
  exactly (Section 8.2). This shows coverage: the descriptions of 5.1–5.5 account for every clause of the CNF, with
  nothing missing or extra. It is not an independent derivation of every family: for the GP generic path and for A4,
  `spec.py` enumerates the clauses the way the encoder does. The correctness of the clauses rests on Propositions 7–11
  and on the semantic tests of Sections 8.3–8.4.

## 6. Proof of Theorem 1 and the corollaries

*Theorem 1.*
- By Lemma 4 the labelling λ(S, p₀) exists and is unique.
- By Lemma 5 and the validity of (G) and (C) (Lemma 2), α(S, p₀) is well defined.
- By Lemma 6 its literals have the real meaning.
- Propositions 7–11 cover every clause of the base CNF (Section 5.6). The hypotheses are used only where noted:
  - general position in Lemmas 1, 3, 4, 7 and 8;
  - "no convex 7-gon" only for KGON;
  - "p₀ is a hull vertex" only for HULL;
  - the normal form only for SB. ∎

*Corollary 2.* α(S, p₀) satisfies the base (Theorem 1). If it also satisfies Q, it satisfies F_Q. So if F_Q is
unsatisfiable, no (S, p₀) with α(S, p₀) ⊨ Q exists. ∎

*Corollary 3.* α(S, p₀) satisfies the base. If it satisfied no Q_i, it would satisfy every clause ¬Q_i, and so the
unsatisfiable formula. The second sentence follows from Corollary 2. ∎

*Corollary 3′.* α(S, p₀) satisfies the base (Theorem 1) and, since (S, p₀) is in the class of Q, every literal of Q.
Suppose it satisfied no L_i. Then each L_i has a literal that α makes false; that literal is not in Q, so α satisfies
¬(L_i ∖ Q). Hence α would satisfy the unsatisfiable formula. ∎

**In words:** every real configuration yields a satisfying assignment of the base, one for each hull vertex chosen as
first point. Hence UNSAT of the base plus a cube excludes every real configuration whose normal-form labelling, from
some hull vertex, satisfies the cube. A theorem about all centrally symmetric 34-point sets then needs, in addition:

- covers that place every (S, p₀) in some cube's class: Corollary 3 for the hull cubes, Corollary 3′ for the
  second-layer cubes inside a hull cube;
- for the classes not refuted directly, relabelling reductions that map a configuration from such a class to a refuted
  class. These are reductions A and B (`C2P/review`, `AUDIT3` A5, `C2FINAL`), outside this document.

Lemma 1 also gives the passage from "at least 33 points" to 34 points (delete pairs). That is `case_halfTurn` in
`SYMLEAN/SymmetricReduction.lean`, which consumes exactly the hypotheses of Theorem 1 through the class `HalfTurn34`.

## 7. Adversarial checklist: code-level traps examined

| trap | finding |
|---|---|
| `lit` returns 0 for a zero triple; a 0 inside a DIMACS clause would end the clause early | never emitted: every family excludes zero triples explicitly (GP: zero terms; A4: 4-sets with a zero triple skipped; K, SB, HULL use no zero triple). Confirmed: clause count = header count, evalcnf range checks, spec comparison |
| `tau(Z)` = 35 is out of range | never evaluated (`is_zero` applies `tau` only to elements other than Z; `_uf` loops p < NP) |
| sign of `parity_sort` | inversion count mod 2 = permutation parity; correct |
| union-find path compression | sign product updated in the right order (Lemma 5) |
| group multiplier | `gsign` = (1, 1): det A = +1 on point triples and on triples with c (h fixes c). A mutant with (−1, 1) is rejected by the encoder itself (Section 8.4) |
| centre identity sign | `sp` = +1 for `rot`: χ(c,p,q) = +χ(−p,p,q) (Lemma 2(b)). The mutant with −1 is caught by every test |
| orbit reduction (GP 5-sets, conv variables, KGON 7-sets) | dropping clauses is always sound; sharing a conv variable across an h-orbit is sound since h preserves convex position |
| `convex4_patterns` | only the direction "kept ⇒ convex" is needed (Lemma 8); the six patterns agree with an independent derivation from real quadrilaterals |
| repeated literals (680 CONV6 clauses) | harmless; evalcnf reports exactly 680 clauses with a repeated literal and 0 tautologies |
| docstring centre facts (m ≥ 4) | not emitted for m = 2 |
| map vs clauses | `write` dumps the same `tv` the clauses use, so cube files built from the map share the literal semantics; all cube literals are triple variables |
| real vs abstract centre | the model has no metric condition on c (e.g. midpoint distances); this only weakens the model (relaxation), never soundness |
| normal form existence for degenerate angular data | angles of representatives are pairwise distinct by Lemma 3, so the order is strict without any perturbation |

## 8. Computational evidence (not part of the proof)

All scripts are in `tests/`; logs are in `tests/logs/`. Geometry is exact: Python integers; `evalcnf.c` only evaluates
Boolean clauses under assignments computed exactly in Python; `count7.c` uses 64-bit integers with an input bound
2³⁰ that makes every orientation exact.

### 8.1 Identities and classes
- `identities.py`: Lemma 2, Lemma 3 (zero), Proposition 7 (GP), Proposition 8 (A4, also weighted), the barycentric
  identity and orient = det are expanded symbolically to 0. Four false variants (GP sign, A4 without first coordinate 1,
  centre identity sign, reflection) leave residuals (`identities.log`).
- `classes.py`: the base map has exactly the hand-derived partition (2,720 type A + 136 type B) with the stated relative
  signs, the triples missing from the map are exactly the 17 zero triples, and the conv numbering gives
  2,856 + 835,176 = 838,032 variables (`mapcheck_base.log`).

### 8.2 The CNF equals the specification
`spec.py` regenerates the eight families from Sections 5.1–5.5, using the map only for variable names (after
`classes.py` has validated it) and its own conv numbering and convex patterns. The full base CNF matches family by
family (`spec_base.log`). As said in 5.6, this establishes coverage; for the GP generic path and A4 the enumeration
follows the encoder's (referee note R4).

| family | clauses | lengths (after removing repeated literals) |
|---|---:|---|
| GP | 12,588,160 | 4: 65,280; 6: 12,522,880 |
| A4 | 413,440 | 4 |
| CONV4 | 138,992 | 2: 272; 5: 138,720 |
| CONV5 | 139,128 | 6 |
| CONV6 | 672,792 | 4: 680; 7: 672,112 |
| KGON | 2,689,808 | 7 |
| SB | 136 | 1 |
| HULL | 10,880 | 3 |

The CNF has no tautological clause. The same comparison passes for 16 small instances (t = 4..8, K = 5..7, with and
without `--hull`; `spec_small.log`). It detects every mutant that changes a family (Section 8.4).

### 8.3 Real configurations on the full base
`run_base.py` labels real centrally symmetric 34-point sets in the normal form from **every** hull vertex, computes α
exactly, and streams the 621 MB CNF through `evalcnf` (`base_full.log`, `work_full/results.json`). For each labelling it
requires:

- the zero pattern equals the map's;
- every class gives one value (the identities hold);
- conv values by the four-point rule agree with hull-size checks on random subsets;
- **the violated clauses are exactly the KGON clauses of the canonical 7-sets in convex position, matched by clause
  index, and nothing else.**

Negative controls label from a non-hull point. Then, besides the same KGON clauses, only HULL clauses are violated, and
their number equals the number of triangles of other points that contain the point, counted independently.
`run_base.py` compares this number, not the identity of the HULL clauses. Clause identity for non-hull controls was
checked by the referee's independent evaluator on three controls of the full base (136, 141 and 130,292 violated
clauses, each exactly the predicted multiset: `referee/logs/refbase.log`).

**Result: all 147 labellings pass** (`BASE EVALUATION PASSED`, 720 s, peak RSS 1.41 GB). 25 configurations,
labelled from every hull vertex (122 labellings) plus one non-hull control each (25 labellings):

| configurations | hull | canonical convex 7-sets = violated clauses |
|---|---|---|
| 12 × the 7-gon-free 32-point set `SYM2/sym7_32points.txt` plus a random antipodal pair | parallelogram | 2,491 or 2,988 |
| 9 × the same set plus a pair placed next to one of its points (found with `count7.c`) | parallelogram | 1, 1, 1, 1, 1, 6, 15, 60, 180 |
| random box, centre (0,0) | 10 vertices | 150,983 |
| random multi-scale ("radial"), centre (−30,−8) | parallelogram | 8,685 |
| pairs almost collinear with the centre (angular gaps about 10⁻⁴ rad) | parallelogram | 3,739 |
| random ring, centre (45,−2) | 20 vertices | 1,375,883 |

In every hull-vertex labelling:
- the zero pattern equals the map's;
- all 2,856 classes are consistent;
- the four-point convexity values agree with hull-size checks on 800 random subsets;
- the set of violated clauses is exactly the set of KGON clauses (identified by clause index) of the canonical 7-sets in
  convex position, from a single clause (near-extremal sets) to 1,375,883, and no clause of any other family.

So the five near-extremal sets whose only convex 7-sets are one antipodal pair of 7-sets violate exactly one clause of
the 16,653,336.

In each control, the number of violated HULL clauses (216 to 1,198) equals the predicted number, and no clause outside
KGON and HULL is violated.

A quick run with 22 labellings preceded it (`base_quick.log`), with the same outcome.

### 8.4 Mutation tests at small sizes
`mutate.py` applies 12 deliberate defects to a copy of the encoder (exact text replacements; the original is the
control). Each defect is generated at t = 4 (8 points plus c, K = 5), t = 5 (10 points plus c, K = 6), t = 6 (K = 6),
t = 5 without normal form, and t = 8 (K = 7, subsets of the 32-point 7-gon-free set). Each is tested against:

- real configurations with no convex K-gon (6 per instance, 4 at t = 8), labelled from every hull vertex: 114 labellings
  per mutant when all five instances generate;
- the two-way SAT test (CNF plus the real point-triple values as units; SAT is required for a sound encoder);
- the map check and the spec comparison;
- for weakening defects, the known-UNSAT instance t = 9, K = 6 (18 points; ES(6) = 17), with an independent axiom check
  of any model.

Full output: `tests/logs/mutation.log`, `tests/mut/summary.json`. Attribution of violated clauses to families for
t = 5, K = 6: `tests/logs/famviol.log` (`tests/famviol.py`; its last line, with an empty name, is the unmodified encoder
copy `zcnf_orig.py`).

| mutant | how it is caught |
|---|---|
| original (control) | 0 violated clauses in all 114 labellings; all two-way tests SAT; map and spec pass; t9k6 UNSAT |
| identity with the wrong sign, χ(c,p,q) = −χ(−p,p,q) | map check fails (type-B signs); every labelling violates A4 clauses (and the SB units when present), never GP clauses: the defect amounts to reorienting the element c, which keeps every GP relation but destroys acyclicity; all two-way tests UNSAT |
| no zero triples | the encoder's own contradiction check: χ(c,p,−p) = −χ(c,p,−p) |
| extra zero triples {c,X₀,X₂}, {c,X₁,X₃} | with normal form: encoder assertion "contradictory SB units"; without: map check fails, every labelling violates GP clauses (attribution by family: `famviol.log`), all two-way tests UNSAT |
| cyclic angular order (χ(c,X₂,X₆) = −) | every labelling violates an SB unit; two-way UNSAT; spec flags SB (no effect without normal form, as expected) |
| hull clauses anchored at X₂ instead of X₀ | labellings whose X₂ is not a hull vertex violate HULL clauses (62 of 90); two-way UNSAT for most configurations; spec flags HULL |
| A4 family missing | **not unsound**: 0 violations, two-way SAT; caught only by the spec comparison; t9k6 stays UNSAT, consistent with the redundancy remark in 5.2 |
| A4 with the wrong sign (forbids t inside pqr) | every labelling violates A4 clauses; two-way UNSAT |
| GP middle coefficient +1 | every labelling violates GP-derived clauses; two-way UNSAT |
| GP family missing | **not unsound**: 0 violations, two-way SAT; caught by the spec comparison and by t9k6 becoming SAT with a model violating GP in 9,164 (5-set, x) instances |
| half-turn with det −1 on point triples | the encoder's own contradiction check |
| forbids convex (K−1)-gons | every labelling violates KGON-type clauses; two-way UNSAT; at K = 5 the encoder crashes |
| a non-convex 4-point pattern counted as convex | most labellings violate CONV4 clauses; two-way UNSAT for some configurations in every instance |

So every unsound defect is caught: by the real-configuration evaluator, by a two-way SAT test proving that the defective
CNF excludes a real configuration, or by the encoder's own consistency checks. The two weakening defects cannot make the
encoding unsound. They are caught by the specification comparison (and GP also semantically).

### 8.5 Reproduction

From `C2ENC/tests`, with `B` and `M` the base CNF and map written by
`python3 SYMZ/zcnf.py rot 17 7 --m 2 --hull -o base.cnf --map base.json` (hashes in Section 0), CaDiCaL 3.0.1 named by
the environment variable `CADICAL` (default: `cadical` on the PATH), and the two C programs built with
`cc -O2 -o evalcnf evalcnf.c` and `cc -O2 -o count7 count7.c` (on the machine used, `cc` also needed `-isysroot` with the
macOS 26 SDK):

```sh
python3 -I identities.py                     # 8.1, about 1 s
python3 -I classes.py $M                     # 8.1
./run_spec_small.sh                          # 8.2, small instances
python3 -I spec.py $B $M --hull              # 8.2, full base: about 100 s, peak RSS 227 MB
python3 -I run_base.py $B $M work_full       # 8.3: 720 s, peak RSS 1.41 GB (the ring set dominates)
python3 -I mutate.py                         # 8.4: 44 s
python3 -I famviol.py mut/<mutant>/zcnf_mut.py 5 6 --no-sb
python3 -I a4redundancy.py <cnf> <map> --all # remark in 5.2 (the CNFs: README.md, Reproduction)
python3 -I perturb3.py 30                    # perturbation.md
```

The instances t = 4 and t = 5 have 8 and 10 points; the centre is the 9th or 11th element (the `rot` m = 2 branch needs
N = 2t points). The referee's scripts and their commands are in `referee/` (`referee/NOTES.md` §6).

## 9. Scope and remaining trust

- **This document establishes** the soundness of the base CNF `b0061e90…` as a complete written proof, refereed
  (`referee/NOTES.md`). It is supported by exact symbolic identity checks, a clause-by-clause specification match
  (coverage; see 5.6), and exact real-configuration tests.
- **It does not establish:**
  - any UNSAT verdict, which rests on the certificates and their checkers;
  - the geometric content of the cubes, the covers, reductions A and B, or the orbit bookkeeping;
  - the threefold, fivefold or mirror cases.
- **Lean.** The step from "HalfTurn34 holds" to the heptagon statement for every half-turn-symmetric set of at least 33
  points is Lean-checked (`case_halfTurn`). The step from the certificates to `HalfTurn34` is not: it is Theorem 1
  together with the case split and the certificates.
