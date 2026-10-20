# Task H3: a verified mirror-class exclusion, prepared

This directory is a Lean 4 package, `MirrorEncoding` (Lean 4.24.0, Mathlib v4.24.0). It
depends on `results/H` (`ETVEncoding`) by path. It contains:

- a Lean generator for the two CNFs of the mirror-symmetric 33-point class;
- proofs that both CNFs are sound;
- a verified cube-cover check and the theorem that composes per-cube results.

Together these reduce the statement

> every 33-point set in general position that is symmetric in a line has a convex 7-gon

to two UNSAT facts about files that the Lean generator writes byte for byte. **Those UNSAT
facts are not established here.** The parallel shard runs did not close either instance. C2's final
state (commit 3a34639) has open weight 0.002722 in sub-case (i) (1,048 open cubes) and
0.3640 in sub-case (ii) (1,340 open cubes).
This run then took on C2's 1,048 open cubes of sub-case (i) with plain CaDiCaL (no conflict
limit, 600 s cap) and cake_lpr.
- 1,047 were refuted with cake_lpr-verified proofs.
- The last cube timed out once. It was split on two more variables (2538, 2687), and all four
  sub-cubes were refuted and verified.

**Result for sub-case (i), certified as a claim about one CNF.** The Lean-generated
`hm33k7.sub.cnf` (sha256 `bfbc2d60…`) is UNSAT:
- each of its 5,589 leaves `c` (`logs/leaves_i_hull_verified.txt`) has a
  `s VERIFIED UNSAT` from cake_lpr on `cubeCnf F c`;
- the Lean-proved `coverCheck` (compiled `cover_check`) accepts the leaf list
  (`logs/cover_check_i_hull_final.log`).

The leaves were checked with cake_lpr, a verified LRAT checker, and not with `lrat-check`.
This UNSAT is **not imported into Lean**, so it is not a Lean theorem. Through the Lean
theorem `Mir.hasConvexNGon_of_unsat_hull`, it would give: every 33-point mirror-symmetric set
in general position whose axis point is a hull vertex has a convex 7-gon. That conclusion
rests on the cake_lpr runs and the trust base in §4. **Sub-case (ii) is open** (open weight
0.364), so there is no claim about the whole mirror class and none about ES(7).

There is no `sorry`, `admit`, `native_decide` or new axiom. `MirrorEncoding/Audit.lean`
checks with `#guard_msgs` that the 29 main theorems use at most `propext`,
`Classical.choice` and `Quot.sound`. `lake build` fails if this changes.

## What ran where

Everything ran in one cloud VM: Linux x86_64, 4 cores, 15 GB RAM, no swap (`env.txt`). The
VM started at 02:35 UTC on 20 Oct 2026.

- **Lean.** Lean 4.24.0 came from the GitHub release zip. `lake exe cache get` could not
  download anything: the proxy answered 403 for `lakecache.blob.core.windows.net`. So the
  Mathlib modules that `results/H` needs were built from source. `lake build` in `results/H`
  took 26 min wall time (`logs/H_lake_build.log`).
- **Solver.** CaDiCaL 3.0.1 (git c6073042), built here.
- **Checker.** cake_lpr from https://github.com/tanyongkiam/cake_lpr at a36874a8, built
  here with gcc 13.3 `-O2` (`make cake_lpr`). `cake_lpr.S` has sha256
  `2f3af32d…72b7d4a`, which matches the repository's `cake_lpr.sha256`. `basis_ffi.c` has
  sha256 `8e30d84f…` (the file listed in `cake_lpr.sha256` has a different hash; results/H2
  saw the same). The bundled `example.cnf`/`example.lpr` check prints `s VERIFIED UNSAT`.
- **Python references.** `results/C/scripts/make_cnfs.sh` (on top of
  `tools/etv/gen_etv.py` and `results/C/scripts/mirgen.py`, both at commit 3a04d94) ran in
  the scratch directory. The CNF and LRAT files are not committed.

## 1. Builds and audits of results/H and results/H2

- `results/H`: `lake build` completed (`Build completed successfully (1557 jobs)`). This
  includes `ETVEncoding.Audit`, whose 24 `#guard_msgs` axiom checks all passed. Log:
  `logs/H_lake_build.log`.
- `results/H2`: `lake build` completed (`Build completed successfully (1754 jobs)`,
  the same count as in H2's README), after building the additional Mathlib modules it needs.
  `D3Encoding.Audit` (11 `#guard_msgs` axiom checks) is part of the default target and
  passed. Logs: `logs/H2_lake_build.log` (first run; the log file is cut off, the job exited
  0) and `logs/H2_lake_build_rerun.log` (incremental rerun showing the completion line and
  the linter warnings).
- The byte comparisons of H/H2 were not rerun here; H2 already checked them.

## 2. Formalisation of the mirror class

All definitions are in namespace `Mir`. Points use the parent repository's `Point`,
`orient`, `GeneralPosition` and `HasConvexNGon`.

- `reflX : (x, y) ↦ (-x, y)` is the mirror.
- `MirrorSet S c` means `c ∈ S`, `c` is on the axis, `S` is `reflX`-symmetric, and every
  other point is off the axis. For `|S| = 33` this is "one axis point and 16 mirror pairs",
  the convention of `results/C`. `exists_mirrorSet` proves that every `reflX`-symmetric set
  of odd size in general position is a `MirrorSet` for exactly one axis point: the off-axis
  points pair up, and three axis points would be collinear.
- Sub-case (i) is `c ∉ convexHull ℝ (S ∖ {c})`, i.e. `c` is a hull vertex. Sub-case (ii) is
  the complement, `c ∈ convexHull ℝ (S ∖ {c})`.
- **Sub-case (i), projective normal form** (`Frame.lean`).
  - `extreme_axis_split`: if `c` is extreme, all other points are strictly below it or all
    are strictly above it. Otherwise `c` lies between the midpoints of two mirror pairs.
  - A rotation (`rotA` for the top case, `rotB` for the bottom case) makes `c` strictly
    leftmost, on the new mirror axis.
  - Sorting the others by slope from `c` (`exists_hullFrame_at`) gives `ETV.HullFrame`.
    This is C's map `(x, y) ↦ (x/d, 1/d)` with `d = y₀ − y`: `c` goes to vertical
    infinity, and the slope from `c` is C's sort key `x/(y₀ − y)`.
  - Hull frames of a set with a given first point are unique (`HullFrame.eq_of_ptSet`).
    The mirrored frame is therefore the frame itself, which gives the pairing
    `i ↔ N − i` (C's `i ↔ 35 − i` in 1-based indexing) as `MirSym N true σ`.
- **Sub-case (ii), "the axis point is not extreme"** (`Interior.lean`, `TieBreak.lean`).
  - Sort the points by x. Then `P (N−1−i) = reflX (P i)`, and the axis point is
    `P ((N−1)/2)` (point 17 in 1-based indexing).
  - `axis_above_below`: some point is strictly above `c` and some strictly below. Otherwise
    `conv(S ∖ {c})` lies in an open half-plane.
  - For a mirror pair `a, reflX a` with `a` left of the axis,
    `orient a c (reflX a) = 2·a.x·(c.y − a.y)`. So one chord through `c` is a cup triple and
    one is a cap triple, which is exactly what the two `--interior` clauses say
    (`AxisInterior`).
  - Mirror pairs can share x-coordinates with other pairs, so the x-sort can have ties.
    `TieBreak.lean` handles them with the projective map
    `(x, y) ↦ (x, y)/(1 + εy)`. It commutes with `reflX` and multiplies orientations by
    `1/(w_a w_b w_c) > 0`. For all but finitely many small `ε` it separates all
    x-coordinates (`exists_eps`). Sorting by the image's x-coordinate and pulling back
    gives the enumeration (`interiorTieBreak`).
- **Any mirror line** reduces to the y-axis by a rigid motion (`Line.lean`, see §3).
- **The y-flip unit `X(1,2,3)`** is handled at the signotope level. Complementing `σ` keeps
  the signotope axioms, the mirror symmetry and gon-freeness, and it swaps the two interior
  clauses.

## 3. Soundness of the two CNFs

### The generator

`MirrorEncoding/Gen.lean` follows `gen_etv.py --mirror [--hull]` and `mirgen.py` loop for
loop.

- `mirClauses N A U K hull` is `ETV.etvClauses` (the option-free `gen_etv.py`, whose
  soundness is proved in `results/H`), then the hull units, then the identification clauses.
- `subVar` and `subLit` do the orbit substitution, mapping each triple to the
  lexicographically smaller one of its pair.
- `normClause`, `isTaut` and `mirgen` do Python's sort/dedupe/tautology filter, keeping the
  first occurrence.
- `interiorClauses` and `yflipUnit` are the extra clauses.
- `hullCnf N K` and `interiorCnf N K` are the two files.

`lake exe mir_dimacs (hull|interior) N K OUT` prints them. Only the string formatting in
`Emit.lean` is unverified.

**Byte-for-byte comparison** (`scripts/compare_mir.sh`; logs `logs/compare_mir.log` and
`logs/compare_mir_package.log`):

| file | Lean command | result | sha256 | header |
|---|---|---|---|---|
| `hm33k7.sub.cnf` | `mir_dimacs hull 33 7` | identical (`cmp`) | `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d` | `p cnf 47002 535454` |
| `m33k7int.sub.cnf` | `mir_dimacs interior 33 7` | identical | `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d` | `p cnf 47002 515121` |
| `hm17k6.sub.cnf` | `mir_dimacs hull 17 6` | identical | `703b2364…` | `p cnf 4702 30413` |
| grid: hull for N ∈ {3..13, 15, 17}, interior for odd N, K ∈ {4..7} | | 84/84 identical | | |

The clause counts agree with `results/C/README.md`. Neither C nor C2 recorded hashes of
these files, so the table is the reference.

### Proved theorems

Signotope level, in `Sound.lean`:

    theorem Mir.dimacsSat_mirgen : DimacsSat cls ν → DimacsSat (mirgen cls) ν
    theorem Mir.hullCnf_satisfiable (hK2 : 2 ≤ K) (hσ : IsSignotope N σ) (hK : ¬HasGon σ N K)
        (hH : HullForm N σ) (hS : MirSym N true σ) : DimacsSatisfiable (hullCnf N K)
    theorem Mir.interiorCnf_satisfiable (hN : 3 ≤ N) (hK2 : 2 ≤ K) (hσ : IsSignotope N σ)
        (hK : ¬HasGon σ N K) (hS : MirSym N false σ) (hI : AxisInterior N σ) :
        DimacsSatisfiable (interiorCnf N K)

The model is `results/H`'s `nuOf N K K (assn σ)`. Orbit substitution is sound because this
model gives `X(i,j,k)` and its mirror the same value (`assn_subVar`).

Point-set level:

    theorem Mir.hasConvexNGon_of_unsat_hull (hunsat : ¬DimacsSatisfiable (hullCnf 33 7))
        (hgp : GeneralPosition S) (hcard : S.card = 33) (hM : MirrorSet S c)
        (hext : c ∉ convexHull ℝ ↑(S.erase c)) : HasConvexNGon 7 S
    theorem Mir.interiorTieBreak_holds : InteriorTieBreak
    theorem Mir.mirrorExclusion_of_unsat (h1 : ¬DimacsSatisfiable (hullCnf 33 7))
        (h2 : ¬DimacsSatisfiable (interiorCnf 33 7)) : MirrorExclusion
    theorem Mir.mirrorExclusionY_of_mirrorExclusion : MirrorExclusion → MirrorExclusionY
    theorem Mir.mirrorExclusionLine_of_unsat (h1 : ¬DimacsSatisfiable (hullCnf 33 7))
        (h2 : ¬DimacsSatisfiable (interiorCnf 33 7)) : MirrorExclusionLine
    theorem Mir.mirrorExclusionLine_of_cubes (hc1 : coverCheck C1 = true) (hc2 : coverCheck C2 = true)
        (h1 : ∀ c ∈ C1, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
        (h2 : ∀ c ∈ C2, ¬DimacsSatisfiable (cubeCnf (interiorCnf 33 7) c)) : MirrorExclusionLine

The targets are stated in `Targets.lean`:

    def Mir.MirrorExclusion : Prop := ∀ S c, GeneralPosition S → S.card = 33 → MirrorSet S c →
        HasConvexNGon 7 S
    def Mir.MirrorExclusionY : Prop := ∀ S, GeneralPosition S → S.card = 33 →
        (∀ q ∈ S, reflX q ∈ S) → HasConvexNGon 7 S
    def Mir.MirrorExclusionLine : Prop := ∀ S a u, u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
        S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → HasConvexNGon 7 S

`MirrorExclusionLine` is the statement for an arbitrary mirror line, the line through `a`
with unit direction `u`. `Line.lean` reduces it to the y-axis. The rigid motion
`p ↦ M (p − a)`, with `M = [[u₁, −u₀], [u₀, u₁]]`, conjugates `reflLine a u` to `reflX`,
preserves orientations (`det M = 1`), and convex position pulls back along it
(`convexPosition_of_image_affine`).

`DimacsSatisfiable` is the plain DIMACS semantics from `results/H`.

Axiom report (`logs/print_axioms.log`, enforced by `Audit.lean`):
- `dimacsSat_mirgen` and `not_dimacsSatisfiable_of_cover` use `[propext, Quot.sound]`.
- The other 27 theorems, including `hullCnf_satisfiable`, `interiorCnf_satisfiable`,
  `interiorTieBreak`, `mirrorExclusion_of_unsat`, `mirrorExclusion_of_cubes`,
  `exists_mirrorSet` and `covers_of_coverCheck`, use `[propext, Classical.choice, Quot.sound]`.

## 4. The checker side

### Per-cube certificates

`scripts/check_cubes.sh CNF CUBES OUT.jsonl [--timed]` works through a cube file. For each
cube `c` it:
1. writes `cubeCnf F c = F ++ [[l] | l ∈ c]`;
2. runs `cadical --elim=0 --lrat --binary=false`;
3. checks the textual LRAT proof with cake_lpr;
4. deletes both files.

It ran on the Lean-generated `hm33k7.sub.cnf` and `m33k7int.sub.cnf`, over **every closed
cube of the C2 runs**. That is `results/C2/logs/cnc_*/closed.txt` at C2's final commit
3a34639; earlier checkpoints were processed first, and then the cubes they lacked. Up to 4
streams ran at nice 10 from 02:59 to 04:46 UTC.

| sub-case | distinct closed cubes | cake_lpr `s VERIFIED UNSAT` | not verified | sum of `2^-len` | CaDiCaL s | cake_lpr s | largest proof | total proof bytes |
|---|---|---|---|---|---|---|---|---|
| (i) `hm33k7.sub` | 4,535 | **4,535** | 0 | 0.99743 | 6,920 | 7,297 | 22.2 MB | 16.5 GB |
| (ii) `m33k7int.sub` | 749 | **749** | 0 | 0.63687 | 325 | 1,467 | 17.9 MB | 0.65 GB |

Formerly open cubes of sub-case (i), from C2's final `state.json` (03:46 to 06:19 UTC, 4
streams, `SOLVE_TIMEOUT=600`):

| cubes | cake_lpr `s VERIFIED UNSAT` | timed out | weight verified | weight left | CaDiCaL s | cake_lpr s | largest proof |
|---|---|---|---|---|---|---|---|
| 1,048 | **1,047** | 1 (19 literals) | 0.0027197 | 2^-19 ≈ 1.9e-6 | 17,132 | 3,052 | 301 MB |

Logs: `logs/cube_lrat_i_hull_open.jsonl` and `logs/cube_lrat_i_hull_open.summary.json`. The
remaining cube is `logs/open_cubes_i_hull_remaining.txt`.
`logs/cover_check_i_hull_after_open.log` shows `coverCheck` accepting the 5,585 verified
cubes plus that one cube; without it, the check says `NOT COVERED`.

The weight column is a plain sum over distinct cubes. Some of C2's closed entries are stale
duplicates of re-split cubes, so the sum can exceed C2's exact closed weight (0.99728 and
0.63601).

Logs:
- `logs/cube_lrat_*.jsonl`: one line per cube, with the cube, solver exit, times, proof size
  and cake_lpr verdict;
- `logs/cube_lrat_*.summary.json`, produced by `scripts/summarize_cubes.py`.

No proof file is committed. Each one was deleted right after its check.

C2's own spot checks used `lrat-check`, which is not verified. Here every leaf C2 closed has a
certificate checked by a verified checker, against the CNF that the Lean generator emits.

### The cover argument, verified

`Cover.lean` and `CoverCore.lean` provide the following.

- `coverCheck cubes` is a decision-tree tautology check. It splits on the first literal of
  the first cube, restricts all cubes, recurses, and rejects the literal `0`. Its fuel is
  total length + 1, which always suffices, because each branch removes at least one literal
  occurrence.
- `covers_of_coverCheck : coverCheck cubes = true → ∀ ν, ∃ c ∈ cubes, CubeSat ν c`.
- `not_dimacsSatisfiable_of_cover`: if the cubes cover, and `¬DimacsSatisfiable (cubeCnf F c)`
  holds for every cube, then `¬DimacsSatisfiable F`.
- `mirrorExclusion_of_cubes`: the mirror exclusion from two accepted cube lists and a
  refutation of every cube CNF.

`lake exe cover_check [--timed] FILE…` runs the compiled `coverCheck`. It accepts march_cu
`a … 0` lines and C's `time … 0` lines. The run on the cube logs (`logs/cover_check_C_C2.log`)
gave:

| run | closed cubes only | closed + open (from `state.json`) |
|---|---|---|
| C, sub-case (i) | NOT COVERED (277) | COVERED (746) |
| C, sub-case (ii) | NOT COVERED (47) | COVERED (366) |
| C2, sub-case (i) | NOT COVERED (2,824) | COVERED (3,686) |
| C2, sub-case (ii) | NOT COVERED (587) | COVERED (1,624) |

| C2 final (3a34639), sub-case (i) | NOT COVERED (4,538) | COVERED (5,586) |
| C2 final (3a34639), sub-case (ii) | NOT COVERED (749) | COVERED (2,089) |

The C2 rows above the last two are from commit eb75ac3. For the final state,
`logs/cover_check_C2_final.log` agrees with C2's own `check_tree2.py`. `coverCheck` accepts
any branching variable, so the stale closed entries that C2 reports after its resume do no
harm.

So the schedulers' bookkeeping is a complete partition, and the open cubes are exactly what
remains.

### How the pieces compose into one verified UNSAT

For each sub-case `F ∈ {hullCnf 33 7, interiorCnf 33 7}`:

1. Generate `F` with `lake exe mir_dimacs`. The file has the sha256 in the table above.
2. Run the cube-and-conquer to completion. The leaf list `C` is a march_cu cube file, or the
   final `closed.txt`.
3. Run `lake exe cover_check C`. It must print `s COVERED`.
4. For every `c ∈ C`, cake_lpr must print `s VERIFIED UNSAT` on `cubeCnf F c` with that
   cube's proof (`scripts/check_cubes.sh`).
5. Then `Mir.mirrorExclusionLine_of_cubes` gives `MirrorExclusionLine`, from the two cube
   lists and the two families of per-cube facts.

Steps 3 and 4 run outside the Lean kernel. Bringing them into Lean takes either:
- a disclosed hypothesis or axiom per instance (EmptyHexagonLean style), or
- an in-kernel checker. Per results/H and H2 this is out of reach at this size.

cake_lpr's own two-level mode (`cake_lpr F summary i-j proof` and `-check`) is an
alternative to steps 3 and 4. It would also move the cover argument into verified code. I
have not set it up here, and its exact use for cube lists is not checked.

**Trust base of the composed statement:**
- the Lean kernel and the definitions of `Point`, `orient`, `GeneralPosition` and
  `HasConvexNGon`;
- the unverified string formatting in `Emit.lean` (cross-checked byte for byte against
  Python);
- cake_lpr (HOL4/CakeML verified down to x64; plus `basis_ffi.c`, gcc/ld and the OS);
- the compiled `cover_check` (the Lean compiler and its unverified parser) and
  `check_cubes.sh`'s unit-clause appending;
- the step "cake_lpr said UNSAT ⇒ `¬DimacsSatisfiable`", which uses the same standard
  DIMACS semantics on both sides.

CaDiCaL, `cnc2.py` and the Python encoders are not trusted.

## 5. Remaining targets, precisely

1. **`¬ETV.DimacsSatisfiable (Mir.hullCnf 33 7)`.** Certified outside Lean in this run,
   with 5,589 cake_lpr-verified leaves and the cover check passing. What is left is only
   the import into Lean (item 3). The four sub-cubes of the last open cube are in
   `logs/cube_lrat_i_hull_last.jsonl`.
2. **`¬ETV.DimacsSatisfiable (Mir.interiorCnf 33 7)`.** Open and far from closure: 1,340 open
   cubes, open weight 0.3640 (`logs/open_cubes_ii_interior.txt`). The same procedure
   applies, and the 749 verified closed cubes are already done.
3. **Importing 1 and 2 into Lean.** cake_lpr runs outside Lean, so the final statement is
   "Lean theorem + cake_lpr runs + cover check run", or an explicitly disclosed axiom.
4. **Not needed, but open:** completeness (the CNFs could be stronger than the geometry),
   and non-vacuity (no explicit `MirrorSet` is built in Lean).

## Build

    cd cloud/es7-2026-10-19/results/H3
    mkdir -p .lake && ln -s ../../../../../.lake/packages .lake/packages   # share Mathlib
    lake build      # library, Audit, mir_dimacs, cover_check
    scripts/compare_mir.sh .lake/build/bin/mir_dimacs /tmp/cmp            # grid
    scripts/compare_mir.sh .lake/build/bin/mir_dimacs /tmp/cmp 33:7       # real instances

`lake build` of this package took about 33 s, after `results/H` was built.

| File | Contents |
|---|---|
| `Gen.lean`, `Emit.lean` | generator and `mir_dimacs` |
| `Sound.lean` | `MirSym`, `AxisInterior`, `mirgen` soundness, both signotope-level theorems |
| `Frame.lean` | `MirrorSet`, `reflX`, sub-case (i) geometry |
| `Interior.lean` | sub-case (ii) geometry for an enumeration and for distinct x |
| `TieBreak.lean` | the projective tie-break (`interiorTieBreak`) |
| `CoverCore.lean`, `Cover.lean`, `CoverMain.lean` | cover check, its soundness, composition, `cover_check` |
| `Targets.lean` | `MirrorExclusion(Y)`, `InteriorTieBreak`, the reductions, `exists_mirrorSet` |
| `Line.lean` | `reflLine`, the rigid motion to the y-axis, `MirrorExclusionLine` |
| `Audit.lean` | `#guard_msgs` axiom checks |
