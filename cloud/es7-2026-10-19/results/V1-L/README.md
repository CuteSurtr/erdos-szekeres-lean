# Task V1-L: the Lean side of mirror sub-case (i)

Sub-case (i): 33 points in general position, symmetric in a line, whose point on the line
(the axis point) is a vertex of the convex hull. This directory is a Lean 4 package, `V1L`
(Lean 4.24.0, Mathlib v4.24.0), that depends on `results/H3` (`MirrorEncoding`) by path.
It turns the per-leaf refutations of runs V1-0..V1-3 into a theorem about point sets.

No `sorry`, `admit`, `native_decide` or new axiom. `V1L/Audit.lean` pins the axiom sets
with `#guard_msgs`; `lake build` fails if they change.

The overall verdict, with the leaf-by-leaf status of the sibling runs, is in `SUMMARY.md`.

## Environment

One cloud VM: Linux x86_64, 4 cores, 15 GB RAM, no swap (`env.txt`). Started 04:48 UTC,
20 Oct 2026. Lean 4.24.0 came from the GitHub release zip. The Mathlib cache download is
blocked (proxy 403), so Mathlib was built from source as part of `results/H`.

## 1. Builds of results/H and results/H3

| package | result | wall time | log |
|---|---|---|---|
| `results/H` | `Build completed successfully (1559 jobs)`, including `ETVEncoding.Audit` (24 `#guard_msgs` axiom checks) | 22 min 15 s (with Mathlib from source) | `logs/H_lake_build.log` |
| `results/H3` | `Build completed successfully (1560 jobs)`, including `MirrorEncoding.Audit` (29 `#guard_msgs` axiom checks) | 32 s | `logs/H3_lake_build.log` |

H3 shares H's packages directory (`H3/.lake/packages -> ../../H/.lake/packages`).

## 2. The CNF

`logs/mir_dimacs_hull.log`:

    lake exe mir_dimacs hull 33 7 OUT           1.7 s
    sha256 bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d   p cnf 47002 535454
    results/C/scripts/make_cnfs.sh → hm33k7.sub.cnf
    sha256 bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d
    cmp: identical

The sha256 matches the one given for `hm33k7.sub.cnf` and the one in H3's README.

## 3. The compiled cover check

`logs/cover_check.log`:

    $ lake exe cover_check cloud/es7-2026-10-19/verify/hull_leaves.icnf
    (sha256 cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6)
    c cubes: 1198
    s COVERED
    real 0m0.012s

This is a cross-check only. The Lean theorem does not depend on it, because the cover fact is
proved in the kernel (§4).

## 4. The Lean development

| file | contents |
|---|---|
| `V1L/Leaves.lean` | generated: `V1L.hullLeaves : List (List Int)`, the 1,198 cubes of `hull_leaves.icnf` in file order |
| `V1L/Cover.lean` | `hullLeaves_coverCheck : coverCheck hullLeaves = true`, by `decide +kernel` |
| `V1L/Main.lean` | the statements and the theorems |
| `V1L/Audit.lean` | `#guard_msgs` axiom checks |
| `V1L/LeavesEq.lean` | `lake exe leaves_eq FILE`, an unverified cross-check of the generated data |
| `scripts/gen_leaves.py` | writes `V1L/Leaves.lean` from the cube file |
| `scripts/check_siblings.py` | checks V1-0..3's `leaves_cake.jsonl` against the cube file |

### The leaf data

`scripts/gen_leaves.py ../../verify/hull_leaves.icnf V1L/Leaves.lean` writes the file. The
source sha256 `cc11270a…2478b6` is in its header. `Leaves.lean` itself has sha256
`c028ca5a08c0aa242a862bb49fcf6effc5763eee81b9d7339112c940029e6048`, and rerunning the script
reproduces it byte for byte.

Literals are stored as natural numbers (`z ↦ 2z` for `z > 0`, `z ↦ 2|z|+1` for `z < 0`) in
chunks of 100 cubes, and decoded by `decLit`. Plain `Int` list literals were too slow to
elaborate: more than 200,000 heartbeats for one 1,198-cube literal, and 2 minutes for 100-cube
chunks. With the `Nat` encoding the file elaborates in 10 s. The encoding is part of the
definition of `hullLeaves`, so it is covered by the kernel.

The data can be checked against the file in two ways:
- regenerate and `cmp`;
- `lake exe leaves_eq ../../verify/hull_leaves.icnf`, which compares the evaluated
  `hullLeaves` with the parsed file. It prints `c file cubes: 1198, hullLeaves: 1198` and
  `s EQUAL` (`logs/leaves_eq.log`).

### The cover fact, by kernel evaluation

    theorem V1L.hullLeaves_coverCheck : coverCheck hullLeaves = true := by decide +kernel

`decide +kernel` has the kernel reduce `Decidable.decide (coverCheck hullLeaves = true)` to
`true`. It does not use the compiler, `Lean.ofReduceBool`, or any axiom: `#print axioms`
reports **no axioms**. Building `V1L.Cover` takes 66 s. So the cover fact is a theorem, not a
hypothesis.

### Statements

```lean
/-- The external facts: every leaf cube CNF is unsatisfiable. -/
def LeavesRefuted : Prop :=
  ∀ c ∈ hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)

def HullVertexY : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 33 →
    (∀ q ∈ S, reflX q ∈ S) → c ∈ S → c 0 = 0 →
    c ∉ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S

def HullVertexLine : Prop :=
  ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
    S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
    c ∉ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S
```

`c ∉ conv(S ∖ {c})` is "`c` is a vertex of the convex hull of `S`". `reflLine a u` is H3's
reflection in the line through `a` with unit direction `u`. `reflLine a u c = c` says `c` is on
the line. By general position and odd size, `c` is then the unique such point of `S`.

### Theorems

    theorem V1L.hullCnf_unsat_of_leaves (h : LeavesRefuted) : ¬DimacsSatisfiable (hullCnf 33 7)
    theorem V1L.hullVertexY_of_unsat (h : ¬DimacsSatisfiable (hullCnf 33 7)) : HullVertexY
    theorem V1L.hullVertexLine_of_hullVertexY (h : HullVertexY) : HullVertexLine
    theorem V1L.hullVertexY_of_leaves (h : LeavesRefuted) : HullVertexY

    theorem V1L.hullVertexLine_of_leaves
        (h : ∀ c ∈ hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)) :
        ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
          S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
          c ∉ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S

How they are proved:
- **`hullCnf_unsat_of_leaves`** is `Mir.not_dimacsSatisfiable_of_coverCheck` applied to the
  kernel-proved cover fact.
- **`hullVertexY_of_unsat`** first applies `Mir.exists_mirrorSet` to get the axis point `c'`.
  Then `c = c'`, since `MirrorSet.off` puts every other point off the axis. Then it applies
  `Mir.hasConvexNGon_of_unsat_hull`.
- **`hullVertexLine_of_hullVertexY`** moves the set by H3's rigid motion `toAxis a u`, which
  sends `c` to a point on the y-axis.
  - For hull-vertex-ness it uses `AffineMap.image_convexHull` and injectivity.
  - General position and the pullback of the 7-gon are as in H3's
    `mirrorExclusionLine_of_mirrorExclusionY`. The pullback is factored out here as
    `hasConvexNGon_of_image_affine`.

### Axiom report

From `logs/print_axioms.log`, and enforced by `V1L/Audit.lean`:

| theorem | axioms |
|---|---|
| `hullLeaves_coverCheck`, `hullLeaves_length` | none |
| `hullCnf_unsat_of_leaves`, `hullVertexY_of_unsat`, `hasConvexNGon_of_image_affine`, `hullVertexLine_of_hullVertexY`, `hullVertexY_of_leaves`, `hullVertexLine_of_leaves` | `propext`, `Classical.choice`, `Quot.sound` |

Build: `logs/V1L_lake_build.log`, from a clean `.lake/build`:
`Build completed successfully (1561 jobs)`, 1 min 26 s wall time.

## Build

    cd cloud/es7-2026-10-19/results/H && lake build                  # Mathlib from source, ~22 min
    cd ../H3 && mkdir -p .lake && ln -s ../../H/.lake/packages .lake/packages && lake build
    cd ../V1-L && mkdir -p .lake && ln -s ../../H/.lake/packages .lake/packages && lake build
    lake exe leaves_eq ../../verify/hull_leaves.icnf

`lake-manifest.json` is committed. Without it, lake re-resolves the dependencies and runs
Mathlib's `cache get` post-update hook. Here that hook spent 10 minutes on 403s before failing.
