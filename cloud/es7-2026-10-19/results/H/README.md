# Task H: a verified encoding for the ETV signotope CNF (first part)

This directory is a Lean 4 package (`ETVEncoding`, Lean 4.24.0, Mathlib v4.24.0) that
formalises two encoders and proves them sound:

- `tools/etv/gen_etv.py N A U K`, without options and with `--xsb`;
- `tools/trackB/gen_cnf.py N K` with every option combination it accepts: none,
  `--no-mono`, `--flip`, `--hull` and `--hull --mirror`.

For `gen_etv.py` the statement is: if the CNF is unsatisfiable, every point set of the given size, in general
position and with distinct x-coordinates, has an `A`-cap, a `U`-cup or a convex `K`-gon.
For `A = U = K` no distinct-x hypothesis is needed. For example,

    theorem ETV.heptagonConjecture_of_unsat :
        ¬DimacsSatisfiable (dimacs 33 7 7 7) → ErdosSzekeres.HeptagonConjecture

where `dimacs 33 7 7 7` is the clause list of `gen_etv.py 33 7 7 7`. For the file of the
ES(7) SAT runs:

    theorem ETV.heptagonConjecture_of_unsat_n33k7hm :
        ¬DimacsSatisfiable (dimacsB 33 7 true true false true) → ErdosSzekeres.HeptagonConjecture

Here `dimacsB 33 7 true true false true` is `gen_cnf.py 33 7 --hull --mirror`, and
`lake exe trackb_dimacs 33 7 OUT --hull --mirror` reproduces the cached
`.cache/es7/trackB-sat/cnf/n33k7hm.cnf` byte for byte.

There is no `sorry`, `admit`, `native_decide` or new axiom. Every theorem listed below
depends only on `propext`, `Classical.choice` and `Quot.sound`. `ETVEncoding/Audit.lean`
checks this with `#guard_msgs`, so `lake build` fails if it changes.

No ES(7) UNSAT result is proved here. That needs an UNSAT certificate for the actual instance
(see "Remaining gap" below). The pipeline has been run end to end, with no trust in the SAT
solver, on a small instance: `ETV.forces_quadrilateral_5 : ForcesConvexNGon 5 4` and
`ETV.forces_quadrilateral_5_hm` (the `--hull --mirror` route). Each goes from the Lean-generated
CNF, through a CaDiCaL LRAT proof, to a kernel check by a small verified checker.

## Build

The package needs the parent repository at `../../../..` (path dependency) for `Point`,
`orient`, `ConvexPosition`, `GeneralPosition` and some geometric lemmas.

    cd cloud/es7-2026-10-19/results/H
    lake exe cache get      # Mathlib oleans for this workspace
    lake build              # library, axiom audit, `etv_dimacs` and `trackb_dimacs`

A fresh build compiles 14 modules of the parent repository and the 19 modules here, a few
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
| `ClausesB.lean` | The `gen_cnf.py` generator: `trackBClauses N K hull mirror flip mono` (same loops and order as Python) and `dimacsB` (numbering of `gen_etv.py N K K K`). |
| `EmitB.lean` | `lake exe trackb_dimacs N K OUT [--hull] [--mirror] [--flip] [--no-mono]`, which also prints the two `c` comment lines. |
| `TrackB.lean` | Soundness of `gen_cnf.py` at the signotope level (all options), `--flip` (complemented signotope), and the point-set theorem without `--hull`. |
| `Kernel.lean` | `dimacsBSpec`, the `dimacsB` numbering written with `List.idxOf` so that the kernel can evaluate it, and `dimacsB_eq_spec`. |
| `Rup.lean` | A small LRAT (RUP-only) checker over lists, with soundness theorem `Rup.not_dimacsSatisfiable_of_run`. It runs in the kernel. |
| `EndToEnd.lean` | Kernel-checked UNSAT of `gen_cnf.py 5 4` and `gen_cnf.py 5 4 --hull --mirror`, giving `ForcesConvexNGon 5 4` both ways. |
| `Hull.lean` | The projective normal form behind `--hull` (`HullFrame`, `exists_hullFrame`), the x-axis reflection behind `--mirror`, and `forcesConvexNGon_of_unsat_hull`. |
| `Audit.lean` | `#guard_msgs` axiom checks. |
| `scripts/compare_dimacs.sh` | Byte-for-byte comparison with `gen_etv.py`. |
| `scripts/compare_trackb.sh`, `scripts/compare_trackb_dir.sh` | The same for `gen_cnf.py`, on a grid or on a directory of existing `nNkK[h][m].cnf` files. |
| `scripts/lrat_to_lean.py` | Turns a DIMACS file and its textual LRAT proof into the Lean definitions used in `EndToEnd.lean`. |

## Proved

All in namespace `ETV`. None uses an axiom beyond `propext`, `Classical.choice` and
`Quot.sound`.

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

Track B (`gen_cnf.py`):
- `mem_trackBClauses`: apart from the symmetry-breaking clauses, every clause of
  `gen_cnf.py N K` is a clause of `gen_etv.py N K K K`. The two files differ only in the
  order of the end-flag and monotonicity clauses, and `--no-mono` drops some.
- `dimacsB_satisfiable_of_signotope`: a signotope on `N ≥ 3` points with no `K`-gon, in
  the normal forms that the options ask for (`HullForm`, `MirrorForm`, `σ 0 1 2 = true` for
  `--flip`), satisfies `dimacsB N K hull mirror flip mono`.
- `dimacsB_noHull_satisfiable` (`--flip` is sound): `σ` or its complement `!σ` satisfies the
  flip unit, and complementing swaps caps and cups, so gons survive (`hasGon_of_compl`).
- `forcesConvexNGon_of_unsat_trackB`: UNSAT of `gen_cnf.py N K [--flip] [--no-mono]`
  (`N ≥ 3`, `K ≥ 4`) implies `ForcesConvexNGon N K`.
- `hasConvexNGon_of_hasGon'`: a gon of the orientation signotope of any injective
  family in general position (not necessarily x-sorted) is a convex gon.
- `HullFrame`, `HullFrame.isSignotope` and `HullFrame.hullForm`. In a hull frame, `Q 0` is
  left of all the other points and they are sorted by slope seen from `Q 0`. The orientation
  signs then form a signotope in `--hull` normal form. For triples avoiding `Q 0`, the
  projective map `q ↦ (slope, 1/(q.x - p.x))` multiplies orientations by a positive factor
  (`orient_proj`) and sorts the images by x; for triples through `Q 0`, `orient_from`
  applies.
- `exists_hullFrame`: every finite set in general position with distinct x-coordinates has
  a hull frame. Its leftmost point is `Q 0`.
- `HullFrame.mirror`, `sigOf_mirrorFrame` and `ptSet_mirrorFrame`: reflecting in the x-axis
  gives another hull frame of the reflected set, with `σ'(i,j,k) = σ(N-k, N-j, N-i)` away
  from `Q 0`. This swaps the two sides of the `--mirror` clause.
- `forcesConvexNGon_of_unsat_hull`: UNSAT of `gen_cnf.py N K --hull [--mirror] [--no-mono]`
  (`N ≥ 3`, `K ≥ 4`) implies `ForcesConvexNGon N K`.
- `heptagonConjecture_of_unsat_n33k7hm`: the `N = 33`, `K = 7`, `--hull --mirror` case.

End to end (`Kernel.lean`, `Rup.lean`, `EndToEnd.lean`):
- `dimacsB_eq_spec`: `dimacsB = dimacsBSpec` when `N ≥ 3`. This is needed because the
  `HashMap` numbering uses the opaque `mixHash`, which the kernel cannot evaluate.
- `Rup.not_dimacsSatisfiable_of_run`: if the RUP checker accepts a proof that starts from
  clauses of `cnf`, then `¬DimacsSatisfiable cnf`. Deletions are ignored, which is sound.
- `n5k4_unsat` and `n5k4hm_unsat`: three `decide +kernel` facts each (the generator output
  equals the literal CNF, the start clauses are in it, the checker accepts the CaDiCaL proof).
- `forces_quadrilateral_5` and `forces_quadrilateral_5_hm`: `ForcesConvexNGon 5 4`.

Lean's own LRAT checker (`Std.Tactic.BVDecide.LRAT.check`, used by `bv_decide`) has a
soundness proof, but `decide +kernel` gets stuck on it, so without `native_decide` it is not
usable here. That is why `Rup.lean` exists.

Only the needed direction is proved: a gon in the signotope gives a convex set of points.
The converse (a convex `K`-subset gives a gon) is not needed for soundness and is not
proved.

## The Lean CNF is the Python CNF

The proofs are about `ETV.dimacs` and `ETV.dimacsB`. `lake exe etv_dimacs` and
`lake exe trackb_dimacs` print exactly those lists, after plain string formatting in
`Emit.lean` and `EmitB.lean`, which is not verified. To check that it is the file
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

Track B (`scripts/compare_trackb.sh`), also byte-identical:
- the grid N ∈ {3,…,9,12}, K ∈ {4,…,8}, each with the seven option sets none,
  `--no-mono`, `--hull`, `--hull --mirror`, `--hull --mirror --no-mono`, `--flip`,
  `--flip --no-mono` (280 files);
- (33,7), (33,7) `--hull --mirror`, (17,6) `--hull`;
- all 38 cached files `.cache/es7/trackB-sat/cnf/n*k*[h][m].cnf` used in the earlier ES(7)
  runs, including `n33k7hm.cnf` (sha256 prefix `86a1a1f68d18f2a3`), `n33k7h.cnf`,
  `n33k7.cnf`, `n32k7hm.cnf` and `n17k6hm.cnf`. These files are local, not in the
  repository; `scripts/compare_trackb_dir.sh DIR` reruns the check on any such directory.

For a run that is meant to become a theorem, it is simpler to generate the CNF with
`lake exe etv_dimacs` or `lake exe trackb_dimacs` and give that file to the solver and the proof checker, as
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
   - Check the proof inside Lean. This works for tiny instances: `EndToEnd.lean` (`N = 5`,
     97 clauses) compiles in under a minute. It does not scale. For the ES(5) instance
     `gen_cnf.py 9 5 --hull --mirror` (2,073 clauses, 276 proof steps), elaborating and
     checking the literal clause list did not finish within about 20 minutes, so it is not
     included. ES(7) certificates are many orders of magnitude larger. Lean core's LRAT
     checker needs `Lean.ofReduceBool` (`native_decide`) to run, and that is forbidden here.

   For the external route, `DimacsSatisfiable` is the usual DIMACS semantics of the printed
   file, so the imported fact is exactly "this file is UNSAT".
2. **Cube-and-conquer.** If the UNSAT comes from cubes (`tools/cnc`), you also need a
   checked proof that the cubes cover the space (a tautology/LRAT check of the cube
   disjunction) and one certificate per cube, as in EmptyHexagonLean.
3. **Symmetry breaking and other encodings.** Covered: `gen_etv.py` without options and
   with `--xsb`, and `gen_cnf.py` with all its options. Not covered:
   - `gen_etv.py --hull`. The projective map used here preserves orientations, convex
     position and gons, but not caps and cups, because it changes the x-order. So the hull
     normal form is justified only when caps and cups are subsumed by gons, i.e. for
     `A = U = K`, where the clauses are those of `gen_cnf.py N K --hull` up to order. For
     `A ≠ U` I do not know a justification, and the argument here does not give one.
   - `gen_etv.py --mirror`. It identifies `X(i,j,k)` with `X(m-k,m-j,m-i)`, so it restricts
     to mirror-symmetric configurations. UNSAT then says only that no symmetric
     configuration exists; it is not symmetry breaking.
   - The symmetric encodings (`tools/symmetric`), one-point extensions (`ext_cnf.py`), and
     any injected lemma clauses (critique item 4).
4. **The emitter.** The `IO` code that prints `dimacs` is unverified (only string
   formatting). Its output has been compared with Python but not proved equal.

Completeness is not needed for soundness, but note: the CNF forbids `K`-gons only through
caps and cups with at least 3 points each (`3 ≤ r ≤ A-1`, `3 ≤ s ≤ U-1`). If `U > K`, a pure
`K`-cup is not excluded, so SAT models of such instances can contain one. This does not
affect any UNSAT conclusion.

## Effort estimate for the rest

- An UNSAT import via an external verified checker and a disclosed hypothesis: about 1 day
  of plumbing, plus the solver and checker time for the instance.
- A faster in-kernel checker (balanced trees instead of lists, clause deletion) for
  ES(5)/ES(6)-sized test instances: 1–2 days. ES(7) certificates stay out of reach in the
  kernel; they need an external verified checker.
- `gen_etv.py --hull` with `A = U = K`: under a day (reuse `Hull.lean`; only the clause
  order differs).
- Cube-and-conquer certification: 2–4 days of tooling, plus the compute.
