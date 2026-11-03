# LAYERLEAN: the layer lemma in Lean (steps 1–3)

4 November 2026 (KST). **Lean-checked**: Lean 4.24.0, Mathlib `f897ebcf`, the repository's pins. The file is
`LayerLemma.lean`.
- **Build.** `lake env lean LayerLemma.lean` from the repository root exits 0 with no messages (`logs/build.log`).
- **Axioms.** Every theorem below depends only on `[propext, Classical.choice, Quot.sound]` (`logs/axioms.log`).
- **No gaps.** There is no `sorry`, `admit` or `axiom`.
- **Sanity check.** A copy with one proof step broken fails to compile.

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

**Hypotheses.** Only m > 0 and K ≤ 2m are needed, with no general position. The written version (`SYM5/README.md` §2,
the note's Lemma `lem:layer`) assumes m ≥ 3 or 4.

The hypothesis is stated exactly as in the repository's case classes, as `Invariant (rotAbout c (2 * Real.pi / m)) S`.
The definitions `orbitFS`, `Invariant`, `toC`, `ofC`, `crot` and `rotAbout`, and their basic lemmas, are copied verbatim
from `SYMLEAN/SymmetricReduction.lean`.

## What is not in Lean

- **Step 4 of the written proof, strict nesting.** The written proof uses general position to put each later point
  *strictly* inside every earlier hull, not on an edge. Lean proves only non-strict containment. The encoders' nesting
  clauses (`C7UPPER/gen.py`, `SYM5/symcnf_layers.py`) use the strict form.
- **The centre for even m.** That the centre is not in S for even m, because O, p and −p would be collinear, is not
  formalized.
- **The step from layers to CNF clauses.** Labelling the layers outermost first, normalizing θ_0 = 0, and the angular
  and chain families are all part of each encoder's soundness proof, which remains a written proof.

## Where the lemma is used

| Directory | Case | m | K |
|---|---|---|---|
| `SYM5` | fivefold ES(7), Theorem 5 | 5 | 7 |
| `C4CUT` | fourfold 32-point exclusion | 4 | 7 |
| `C7UPPER` | 7-fold octagon bound | 7 | 8 |
| `C6UPPER` | 6-fold octagon bound | 6 | 8 |
| `ROT456` | open 4-, 5- and 6-fold octagon thresholds | 4, 5, 6 | 8 |
| `ES8SYM` | layered constructions | | |

For these, the lemma's status changes from "written proof" to "**Lean-checked, except strict nesting (written
proof)**".
