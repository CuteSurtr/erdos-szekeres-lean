# LAYERLEAN: the layer lemma, the chain family and the angular rules in Lean

4 November 2026 (KST). **Lean-checked**: Lean 4.24.0, Mathlib `f897ebcf`, the repository's pins. The file is
`LayerLemma.lean`.
- **Build.** `lake env lean LayerLemma.lean` from the repository root exits 0 with no messages (`logs/build.log`).
- **Axioms.** Every theorem below depends only on `[propext, Classical.choice, Quot.sound]` (`logs/axioms.log`).
- **No gaps.** There is no `sorry`, `admit` or `axiom`.
- **Sanity check.** Copies with one proof step broken (in the core lemma, and in strict nesting) fail to compile.

## What is proved

Throughout, `S : Finset Point` and `Point = Fin 2 → ℝ` (`ErdosSzekeres.Definitions`). The convex-position notions are
the repository's `ConvexPosition` and `HasConvexNGon`.

**Hull vertices.** `hullVerts S` is the set of x ∈ S with x ∉ conv(S \ {x}).
- They are in convex position (`convexPosition_hullVerts`).
- They are nonempty when S is (`hullVerts_nonempty`, by Krein–Milman).
- Every extreme point of conv S is a hull vertex (`extreme_mem_hullVerts`).
- S ⊆ conv(hullVerts S) (`subset_convexHull_hullVerts`).

**Core lemma, abstract** (`hullVerts_eq_orbitFS`). Suppose:
- f is an injective affine map with f(S) ⊆ S;
- every point of S has minimal period m > 0;
- S has no K points in convex position, for some K ≤ 2m.

Then, for every hull vertex x, hullVerts S = {x, f x, …, f^[m-1] x}.

**Rotations** (`hullVerts_eq_orbitFS_rotAbout`).
- The statement is the same, for f = `rotAbout c (2π/m)` with c ∉ S.
- The rotation is affine (`rotAff`) and injective.
- Every point other than c has minimal period exactly m (`minimalPeriod_rotAbout`, via primitive roots of unity).
- If c ∈ S, apply the lemma to `S.erase c` (`invariant_erase_centre`).

**Layers.** `peel S n` is S with its n outermost layers removed. Under the same hypotheses (`layers_are_orbits`), every
nonempty `peel S n` satisfies:
- its hull vertices form one orbit, i.e. a regular m-gon about c;
- that orbit has exactly m points;
- `peel S (n+1)` lies in the convex hull of that orbit.

The layers exhaust S: every point of S is a hull vertex of some `peel S n` (`exists_layer`).

**Strict nesting** (`strict_nesting`, step 4). Suppose further that S is in general position and m ≥ 2. Then for n < n',
every vertex x of layer n and every y ∈ `peel S n'` satisfy `orient x (ρ x) y > 0`: y is strictly to the left of the
edge x → ρx. This is exactly the form of the layered encoders' nesting clauses. The proof has three steps:
- **Weak side.** The vertices of a regular m-gon lie weakly left of each edge (`orient_regular_nonneg`), via
  `orient(x, ρx, ρ^j x) = |x − c|² · 4 sin t · sin jt · sin (j−1)t` with t = π/m (`orient_rotAbout`, `trig_layer`).
- **Convexity.** Half-planes are convex (`convex_orient_nonneg`), so the hull of the layer is weakly left too.
- **Strictness.** Equality would make three points of S collinear.

**The centre for even m** (`centre_not_mem_of_even`). If m is even, S is invariant and in general position, and S has a
point p ≠ c, then c ∉ S. The rotation by π, a power of the given rotation, maps p to 2c − p, and the three points
p, c, 2c − p would be collinear.

**Chain clauses** (`chain_clauses_sound`). The encoders forbid a convex K-gon by forbidding K − 1 points q₀, …, q_{K−2}
of the layers ≥ i, all other than a pivot p of layer i, that satisfy `orient p qₛ qₛ₊₁ > 0` and
`orient qₛ qₛ₊₁ qₛ₊₂ > 0`. Under the layer lemma's hypotheses, general position, no convex K-gon, 4 ≤ K ≤ 2m and m ≥ 3,
no such chain exists. In other words, the true orientations satisfy the encoders' chain family. The proof has two
parts.
- **Fan lemma** (`hasConvexNGon_of_fan`, general position not needed). A pivot plus n ≥ 3 chain points inside an open
  half-plane through the pivot form a convex (n+1)-gon. Every ordered triple is positive, by two polynomial identities
  (`orient_trans_halfplane`, `fan_step`) and the repository's `Suk.convexPosition_of_positive_triples`.
- **Half-plane** (`lin_pos_of_peel`). Every other point of layers ≥ i lies strictly on the inner side of the tangent at
  p.
  - For vertices ρʲp, the value is |p − c|²(1 − cos jα).
  - For later layers, it follows from strict nesting at the two edges through p.

**Angular rules, polar form** (`orient_polar`, `orient_polar_centre_inside`, `orient_polar_halfplane`).
- For points c + r(cos θ, sin θ):
  `orient = r_a r_b sin(β−α) + r_b r_d sin(δ−β) + r_d r_a sin(α−δ)`.
- **Rule A.** If the three angular gaps lie in (0, π), so that the centre is inside the triangle, the triple is
  positive.
- **Rule B.** If the directions increase by x, y > 0 with x + y < π, and the angularly middle point has the largest
  radius, the triple turns left. This uses sin x + sin y > sin(x + y) (`sin_add_lt`).
- **Radius order** (`dist2_le_of_later`). Points of later layers are no farther from c than those of earlier layers, by
  convexity of the disk (`convex_disk`) and the layer lemma. This is the radius fact that rule B needs.

**Hypotheses.** Steps 1–3 need only m > 0 and K ≤ 2m, with no general position. Strict nesting also needs general
position and m ≥ 2. The written version (`SYM5/README.md` §2,
the note's Lemma `lem:layer`) assumes m ≥ 3 or 4.

The hypothesis is stated exactly as in the repository's case classes, as `Invariant (rotAbout c (2 * Real.pi / m)) S`.
The definitions `orbitFS`, `Invariant`, `toC`, `ofC`, `crot` and `rotAbout`, and their basic lemmas, are copied verbatim
from `SYMLEAN/SymmetricReduction.lean`.

## What is not in Lean

- **From phase patterns to the rules.** Each encoder computes which of rule A or rule B applies, and to which ordered
  triple, from the discrete phase pattern: the circular order of points and antipodes. That classification is part of
  the code: it is exact integer comparisons in encoder B and reviewed float sampling in encoder A. Also outside Lean:
  the perturbation to generic phases, and the consistency of one variable per triple orbit.
- **Code to clauses.** That the Python generators emit exactly these families is checked by review and tests, not by
  Lean.

## Where the lemma is used

| Directory | Case | m | K |
|---|---|---|---|
| `SYM5` | fivefold ES(7), Theorem 5 | 5 | 7 |
| `C4CUT` | fourfold 32-point exclusion | 4 | 7 |
| `C7UPPER` | 7-fold octagon bound | 7 | 8 |
| `C6UPPER` | 6-fold octagon bound | 6 | 8 |
| `ROT456` | open 4-, 5- and 6-fold octagon thresholds | 4, 5, 6 | 8 |
| `ES8SYM` | layered constructions | | |

For these, the status changes as follows:
- the layer lemma, from "written proof" to "**Lean-checked**";
- the mathematical soundness of the chain family, now **Lean-checked**;
- the angular rules in polar form, now **Lean-checked**;
- the classification of phase patterns, the perturbation lemma and the code-to-clause correspondence, unchanged
  (written proof, review and tests).
