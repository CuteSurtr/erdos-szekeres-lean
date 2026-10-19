# Task H: a verified encoding for the ETV signotope CNF (first part)

This directory is a Lean 4 package (`ETVEncoding`, Lean 4.24.0, Mathlib v4.24.0) that
formalises the encoding of `tools/etv/gen_etv.py` (without options, and with `--xsb`) and
proves it sound: if the CNF is unsatisfiable, every point set of the given size, in general
position and with distinct x-coordinates, has an `A`-cap, a `U`-cup or a convex `K`-gon.
For `A = U = K` no distinct-x hypothesis is needed. For example,

    theorem ETV.heptagonConjecture_of_unsat :
        ¬DimacsSatisfiable (dimacs 33 7 7 7) → ErdosSzekeres.HeptagonConjecture

where `dimacs 33 7 7 7` is the clause list of `gen_etv.py 33 7 7 7`.

There is no `sorry`, `admit`, `native_decide` or new axiom. Every theorem listed below
depends only on `propext`, `Classical.choice` and `Quot.sound`. `ETVEncoding/Audit.lean`
checks this with `#guard_msgs`, so `lake build` fails if it changes.

Nothing here proves an UNSAT result. That still needs an UNSAT certificate for a concrete
instance; see "Remaining gap" below.

## Build

The package needs the parent repository at `../../../..` (path dependency) for `Point`,
`orient`, `ConvexPosition`, `GeneralPosition` and some geometric lemmas.

    cd cloud/es7-2026-10-19/results/H
    lake exe cache get      # Mathlib oleans for this workspace
    lake build              # library, axiom audit and the `etv_dimacs` executable

A fresh build compiles 14 modules of the parent repository and the 11 modules here, a few
minutes on top of the Mathlib cache. Lake creates `.lake/packages/mathlib` inside this
directory. To avoid a second Mathlib checkout, copy or clone the parent's
`.lake/packages` there first (on macOS, `cp -cR ../../../../.lake/packages .lake/`).

## Conventions

These follow the Python encoder.

- Points are `0, …, N-1` in x-order. Python uses `1, …, N`; because the numbering only
  depends on the variable order, the DIMACS output is identical.
- `X(i,j,k)` (`i<j<k`) is true iff the triple is counterclockwise, i.e. `j` lies below `ik`
  (a *cup triple*). A false triple is a *cap triple*. A chain of sign `t` is a cap for
  `t = false` and a cup for `t = true`.
- A `K`-gon is a cap and a cup with the same first and last point and `K + 2` points in
  total. This is Baek's `Config.NGon`, the "weak" gon. `HasGon.vertices` shows that in a
  signotope the two chains share only their ends, so it is also the strong gon.

## Files and definitions

| File | Contents |
|---|---|
| `Clauses.lean` | The clause generator. `Var` (`x i j k`, `v t x a b r` = Python `V`, `e t x b r` = Python `E`), `Lit`, and `signotopeClauses`, `baseClauses`, `extClauses`, `vClauses`, `eClauses`, `gonClauses`, which follow the Python loops in the same order. `etvClauses N A U K` is the whole clause list. `allVars` lists variables in the order of Python's `new()` calls. `numberMap` (a `HashMap` built by `insertIfNew`) numbers them, `dimacs N A U K : List (List ℤ)` gives the DIMACS clauses, and `dimacsXsb` adds the `--xsb` clause. |
| `Emit.lean` | `lake exe etv_dimacs N A U K OUT [--xsb]` prints `dimacs`/`dimacsXsb` in the Python layout. |
| `Signotope.lean` | `Sig`, `IsSignotope N σ` (the 4-point axiom = the repository's `PacketValid`), `Chain σ t l`, `HasChain`/`HasCap`/`HasCup`, `HasGon`, and the semantics of the auxiliary variables: `ChainEnd σ t x a b r` (`V`) and `ChainE σ t x b r` (`E`). |
| `Soundness.lean` | `assn σ : Var → Prop`, the induced assignment, and the soundness of each clause family. |
| `Dimacs.lean` | `DimacsSatisfiable`, the numbering lemmas, the transfer from structured to DIMACS models, and the signotope-level theorems. |
| `Gon.lean` | The middle-vertex rule and the vertex set of a gon. |
| `Points.lean` | `XSorted P N`, `ptSet`, `sigOf P` (the chirotope), `HasChainPts s m S` (an `m`-cap for `s = -1`, an `m`-cup for `s = 1`, via `LowerBound.IsChain`), and the geometric links. |
| `Main.lean` | Sorting a finite set by x and the final theorems. |
| `Targets.lean` | `DistinctXReduction` and `XsbSound` stated as `def … : Prop`, both proved in the files below. |
| `Xsb.lean` | `mirror N σ`, and the soundness of the `--xsb` clause. |
| `Shear.lean` | The shear `(x, y) ↦ (x + εy, y)`, `DistinctXReduction`, and the `ForcesConvexNGon` corollaries. |
| `Audit.lean` | `#guard_msgs` axiom checks. |
| `scripts/compare_dimacs.sh` | Byte-for-byte comparison with `gen_etv.py`. |

## Proved

All in namespace `ETV`, all with axioms `[propext, Classical.choice, Quot.sound]`.

Signotope combinatorics:
- `Chain.allTriples`: in a signotope, every triple of a chain (not only consecutive ones)
  has the chain's sign.
- `ChainEnd.pred`: deleting the second point of an `(r+1)`-chain leaves an `r`-chain with
  the same ends. This is what makes the monotonicity clauses `V(r) → V(r-1)` and
  `E(r) → E(r-1)` sound.
- `ChainEnd.toList`, `ChainEnd.hasChain` and `hasGon_of_chainE`: the auxiliary variables
  describe real lists.
- `gon_middle` and `HasGon.vertices`: for vertices `p < q < r` of a gon, `σ(pqr)` is the sign
  of the chain containing `q`. A `K`-gon therefore has exactly `K` vertices, and every
  increasing quadruple `a<b<c<d` of them has `σabc = σabd` and `σacd = σbcd`.
- `hasGon_of_hasCap` and `hasGon_of_hasCup`: a `K`-cap or a `K`-cup is a `K`-gon.

CNF soundness:
- `etvClauses_sound`: if `IsSignotope N σ`, `¬HasCap σ N A`, `¬HasCup σ N U` and
  `¬HasGon σ N K`, then every clause of `etvClauses N A U K` holds under `assn σ`.
- `etvClauses_vars`: every variable that occurs in a clause is in `allVars`.
- `numberMap_getD` and `decode_numberMap`: the number of `v` is `1 + ` its position in
  `allVars`, so the numbering is injective on allocated variables.
- `dimacsSatisfiable_of_signotope`: under the same hypotheses, `dimacs N A U K` is
  satisfiable.
- `signotope_of_unsat`: if `dimacs N A U K` is unsatisfiable, every signotope on `N` points
  has an `A`-cap, a `U`-cup or a `K`-gon.

Point sets:
- `isSignotope_sigOf`: x-sorted points give a signotope, by `packetValid_of_xordered`.
- `hasChainPts_of_hasChain`: a signotope cap or cup is a geometric cap or cup (all
  x-increasing triples have the same orientation).
- `hasConvexNGon_of_hasGon` (`K ≥ 4`): a signotope `K`-gon is a convex `K`-gon of the
  points. The proof uses the 4-point sign criterion `convexPosition_four_iff_signs` and
  `Suk.convexPosition_of_four_subsets` (Carathéodory).
- `exists_xsorted`: any finite set with distinct x-coordinates is an x-sorted sequence.
- `dimacsSatisfiable_of_pointSet`: a point set in general position with distinct
  x-coordinates and no `A`-cap, `U`-cup or convex `K`-gon (`K ≥ 4`) makes
  `dimacs |S| A U K` satisfiable.
- `cap_cup_or_gon_of_unsat`: if `¬DimacsSatisfiable (dimacs N A U K)` and `K ≥ 4`, then
  every `N`-point set in general position with distinct x-coordinates has an `A`-cap, a
  `U`-cup or a convex `K`-gon.
- `xsbSound : XsbSound`: for a signotope with no `A`-cap, `U`-cup or `K`-gon (`N ≥ 3`),
  `dimacsXsb N A U K` (the `--xsb` file) is satisfiable. Either `σ` or its x-mirror
  `σ(N-1-k, N-1-j, N-1-i)` satisfies the lex-leader clause, and the mirror is again a
  signotope with no `A`-cap, `U`-cup or `K`-gon (`isSignotope_mirror`,
  `hasChain_of_mirror`, `hasGon_of_mirror`).
- `cap_cup_or_gon_of_unsat_xsb`: the point-set conclusion of `cap_cup_or_gon_of_unsat`
  from UNSAT of the `--xsb` file (`N ≥ 3`, `K ≥ 4`).
- `hasConvexNGon_of_unsat`, the diagonal case: if `dimacs N K K K` is unsatisfiable, every
  such `N`-point set has a convex `K`-gon.
- `distinctXReduction : DistinctXReduction`: some shear `(x, y) ↦ (x + εy, y)` makes the
  x-coordinates of a finite set distinct (`exists_shear_distinctX`). The shear preserves
  `orient` (`orient_shear`) and general position, and convex position pulls back along it
  (`convexPosition_of_image_linear`, via `LinearMap.image_convexHull`).
- `forcesConvexNGon_of_unsat`: `¬DimacsSatisfiable (dimacs N K K K)` and `K ≥ 4` imply
  `ForcesConvexNGon N K`, the repository's own statement, with no extra hypotheses.
- `heptagonConjecture_of_unsat`: `¬DimacsSatisfiable (dimacs 33 7 7 7)` implies
  `HeptagonConjecture`.

Only the needed direction is proved: a gon in the signotope gives a convex set of points.
The converse (a convex `K`-subset gives a gon) is not needed for soundness and is not
proved.

## The Lean CNF is the Python CNF

The proofs are about `ETV.dimacs`. `lake exe etv_dimacs` prints exactly that list, after
plain string formatting in `Emit.lean`, which is not verified. To check that it is the file
the SAT solver saw:

    lake build
    scripts/compare_dimacs.sh                # 2,160-instance grid, N ≤ 12
    XSB=1 scripts/compare_dimacs.sh          # the same with --xsb (N ≥ 3)
    scripts/compare_dimacs.sh 33 7 7 7       # any list of N A U K quadruples

Results on 19 Oct 2026, all byte-identical (`cmp`) to `gen_etv.py`:
- the full grid N ∈ {0,…,7,9,12}, A, U ∈ {2,…,7}, K ∈ {3,…,8} (2,160 files);
- the same grid with `--xsb` for N ≥ 3 (1,512 files);
- (17,4,7,7), (26,7,5,7), (27,7,5,7), (31,7,6,6), (32,7,7,7) and (33,7,7,7);
- `--xsb` on (17,4,7,7), (26,7,5,7) and (33,7,7,7).

For a run that is meant to become a theorem, it is simpler to generate the CNF with
`lake exe etv_dimacs` and give that file to the solver and the proof checker, as
EmptyHexagonLean does with `lake exe encode`. The Python encoder is then only a
cross-check.

## Targets

`Targets.lean` states `DistinctXReduction` and `XsbSound` as propositions. Both are now
proved (`distinctXReduction`, `xsbSound`). The remaining open items are listed below.

## Remaining gap to a verified UNSAT pipeline

1. **The UNSAT fact.** The theorems take `¬DimacsSatisfiable (dimacs N A U K)` as a
   hypothesis. Two routes:
   - Check an LRAT/LPR proof of the file from `lake exe etv_dimacs` with a verified checker
     (cake_lpr) and record it in Lean as a disclosed hypothesis or axiom about
     `ETV.dimacs N A U K`. This is what EmptyHexagonLean does (`axiom unsat_6hole_cnf`).
     It breaks the "standard axioms only" rule, so it has to be stated openly.
   - Check the proof inside Lean. Lean core's LRAT checker (used by `bv_decide`) has a
     soundness proof but needs `Lean.ofReduceBool` to run at useful speed, and that is
     forbidden here. Kernel evaluation of a certificate for an ES(7) instance is not
     realistic. It could work for a tiny instance such as (7,4,7)@17 (UNSAT in 0.79 s);
     that would be a useful end-to-end test.

   Either route also needs a small bridge from `DimacsSatisfiable` to the checker's CNF
   semantics.
2. **Cube-and-conquer.** If the UNSAT comes from cubes (`tools/cnc`), you also need a
   checked proof that the cubes cover the space (a tautology/LRAT check of the cube
   disjunction) and one certificate per cube, as in EmptyHexagonLean.
3. **Symmetry breaking and other encodings.** `--xsb` is covered. `--hull` and `--mirror`
   (projective normal form, which needs a projective-transformation argument),
   `gen_cnf.py` options (`--flip`, `--hull`, `--mirror`), the symmetric encodings
   (`tools/symmetric`), and any injected lemma clauses (critique item 4) are not covered.
   Only the option-free and `--xsb` `gen_etv.py` CNFs are.
4. **The emitter.** The `IO` code that prints `dimacs` is unverified (only string
   formatting). Its output has been compared with Python but not proved equal.

Completeness is not needed for soundness, but note: the CNF forbids `K`-gons only through
caps and cups with at least 3 points each (`3 ≤ r ≤ A-1`, `3 ≤ s ≤ U-1`). If `U > K`, a pure
`K`-cup is not excluded, so SAT models of such instances can contain one. This does not
affect any UNSAT conclusion.

## Effort estimate for the rest

- An UNSAT import via an external verified checker and a disclosed hypothesis: about 1 day
  of plumbing, plus the solver and checker time for the instance.
- An axiom-free in-kernel check of a small instance: 1–3 days, if feasible at all.
- `--hull` / `--mirror` soundness (projective normal form): about 1 week.
- Cube-and-conquer certification: 2–4 days of tooling, plus the compute.
