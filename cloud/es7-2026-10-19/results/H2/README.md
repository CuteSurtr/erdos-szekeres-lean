# Task H2: checking results/H independently, and a verified D3 encoding

Everything here ran in a cloud VM: Linux x86_64, 4 cores, 15 GB RAM. `env.txt` has the
details. Lean 4.24.0 came from the GitHub release tarball, because the proxy blocks
`release.lean-lang.org` (403). The Mathlib cache is blocked too (`lakecache.blob.core.windows.net`,
403), so `lake exe cache get` downloaded nothing and Mathlib v4.24.0 was **built from source**.

## 1. Independent check of results/H

**Verdict: PASS.** No discrepancies were found.

- **Build.** `lake build` in `results/H` completed with all 1552 jobs and no errors.
  `ETVEncoding.Audit` is part of the default target, so all 24 `#guard_msgs` axiom checks
  passed. The unfinished `ETVEncoding/Packed.lean` is not imported by the library; built on
  its own (`lake build ETVEncoding.Packed`) it also succeeds. Log: `logs/H_lake_build.log`.
- **Parent repository.** The full `lake build` of the parent (all 209 modules) was **not
  completed**. I ran it twice:
  - The first, parallel run built Mathlib from source and most parent modules, but seven
    memory-heavy `ErdosSzekeres.Omission.*` modules (`GeneralResidualBlocks`,
    `CoupledCore13`, `CoupledCoreSecond` … `Fifth`, `CoupledCoreEleven`) were OOM-killed
    (exit 137). Four Lean processes do not fit in 15 GB.
  - Rebuilt one at a time, all seven compiled successfully, each with "Build completed
    successfully".
  - The final parallel `lake build` for the remaining modules took the whole container down
    twice (out of memory, then a restart), so I stopped. Some parent modules outside H's
    import closure were never built here.

  **Every parent module that H imports was built and checked.**
- **Source scan.** `sorry`, `admit`, `native_decide` and `axiom` occur in neither
  `results/H` nor the parent `ErdosSzekeres/` tree, except inside comments.
- **Independent `#print axioms`.** These were run in a separate file (`logs/H_print_axioms.log`)
  for `heptagonConjecture_of_unsat`, `heptagonConjecture_of_unsat_n33k7hm`,
  `forces_quadrilateral_5(_hm)`, `xsbSound`, `dimacsB_eq_spec` and
  `forcesConvexNGon_of_unsat_hull`. Every one reports `[propext, Classical.choice,
  Quot.sound]`. The statement of `heptagonConjecture_of_unsat` is as claimed:
  `¬ETV.DimacsSatisfiable (ETV.dimacs 33 7 7 7) → ErdosSzekeres.HeptagonConjecture`, where
  `HeptagonConjecture := ForcesConvexNGon 33 7`.
- **Byte-for-byte check.** Using `logs/H_compare_dimacs.log` with H's own scripts, these were
  all identical:
  - the `gen_etv.py` grid (2160 files) and the same grid with `--xsb` (1512 files);
  - (33,7,7,7), (17,4,7,7), (26,7,5,7), (31,7,6,6), (32,7,7,7), and `--xsb` on (33,7,7,7)
    and (17,4,7,7);
  - the `gen_cnf.py` grid of 280 files over 7 option sets;
  - (33,7), (33,7) `--hull --mirror` and (17,6) `--hull`.

  `trackb_dimacs 33 7 --hull --mirror` has sha256 prefix `86a1a1f68d18f2a3`, as H's README
  says. The emitters in the package build are byte-identical binaries to the standalone
  build used for the grid, and spot checks were repeated with them.
- **Not rechecked.** The 38 cached `.cache/es7/trackB-sat/cnf/*.cnf` files are local to the
  original machine and not in the repository.

## 2. The D3 class: what is proved

Package `D3Encoding` (this directory, Lean 4.24.0 + Mathlib v4.24.0; it depends on `../H`
by path). There is no `sorry`, `admit`, `native_decide` or new axiom.
`D3Encoding/Audit.lean` checks with `#guard_msgs` that the main theorems use only `propext`,
`Classical.choice` and `Quot.sound`.

### 2a. The CNF is the one the solver saw

`D3Encoding/Clauses.lean` is a Lean generator `D3.d3Cnf N K` that follows
`results/E/tools/d3cnf.py` (default `--kgon layered`, on top of `tools/symmetric/symcnf.py`)
loop for loop. `lake exe d3_dimacs N K OUT` prints it in Python's layout, and
`scripts/compare_d3.sh` compares it with Python. The outputs are **byte-identical** for
(N,K) = (3,5), (9,5), (9,6), (15,5), (15,6), (21,6), (21,7), (27,7) and **(33,7)**.
The 33-point file has sha256 `72ebbae027ac5e9264bfe00da8003774049875e1fecc94f60d4baf97af13fa01`,
the same as in `results/E/logs/cnf_sha256.txt`. It has 232,406 variables and 4,760,236 clauses.
(`d3cnf.py N 4` crashes in Python with a KeyError, so K ≥ 5.)

Only the `IO` string formatting in `Emit.lean` is unverified. Two changes were made for
the proofs: the `conv` table uses `insertIfNew`, and the conv keys are processed in one fold
over all levels. Neither changes the output, and the byte checks above were rerun after
each change.

### 2b. Soundness, chirotope level (`D3/Main.lean`)

    theorem D3.d3Cnf_sat {t K} {χ : ℕ → ℕ → ℕ → ℤ} (M : Model t K χ)
        (hA4 : A4 (3*t+1) χ) (hGP : GP3 (3*t+1) χ) (hC : CenterFacts t χ)
        (hSB : SectorOrder t χ) :
        ∃ ν, ∀ c ∈ (d3Cnf (3*t) K).2.2, ClauseSat ν c

`Model t K χ` bundles the following:
- `χ` is alternating, takes values `±1` on distinct points below `3t+1`, and is equivariant
  under the six maps of `group t`: `χ(ga,gb,gc) = ±χ(a,b,c)`, with sign `-1` for reflections.
- `5 ≤ K`.
- `GroupClosed t`, a decidable side condition, discharged for `t = 11` by `decide` in
  `groupClosed_11`.
- No `K` set points are in convex position. Convex position here is `ConvAll`: no point
  lies inside a triangle of three others.

The proof covers every clause family:
- the triple table (variable numbering and signs: consistent and complete);
- A4 and Grassmann–Plücker;
- the centre facts;
- the sector and order normal form;
- the conv₄ pattern clauses, the layered conv_r clauses and the K-set clauses.

For the conv_r and K-set clauses, the proof shows that `canon` is idempotent, so every lookup
`canon(S∖Sᵢ)` hits an allocated key.

### 2c. Soundness, point-set level (`D3/Geometry.lean`)

`LabelledD3 t` is a configuration in the convention of `results/E`:
- points `P i`, where orbit `o` is `P(3o), P(3o+1), P(3o+2)`;
- the centre `P(3t) = c`;
- the exact rotation by 120° about `c`, acting as `rot`;
- a reflection in a line through `c`, acting as `sigma` (the convention
  `S(j,r) = (t−j, −r−1)`);
- all `3t+1` points (the centre included) in general position;
- the sector and angular-order facts as orientation inequalities.

From such a configuration the proof gets a `χ` that satisfies all the hypotheses of 2b.
The GP and A4 hypotheses come from polynomial identities, the centre facts from
`orient(c, a, Ra) = (√3/2)|a−c|²`, and convexity through
`convexPosition_four_iff_signs` and `Suk.convexPosition_of_four_subsets`. The theorems are:

    theorem D3.dimacsSatisfiable_of_labelled (L : LabelledD3 t) (hG : GroupClosed t) (hK : 5 ≤ K)
        (hno : ¬HasConvexNGon K L.pts) : ETV.DimacsSatisfiable (d3Cnf (3*t) K).2.2
    theorem D3.hasConvexNGon_of_unsat_d3 (h : ¬ETV.DimacsSatisfiable (d3Cnf 33 7).2.2)
        (L : LabelledD3 11) : HasConvexNGon 7 L.pts

`ETV.DimacsSatisfiable` is the DIMACS semantics from `results/H`.

### 2d. The UNSAT certificate, checked by cake_lpr

- **CNF:** `d3cnf.py 33 7`, which is byte-identical to `lake exe d3_dimacs 33 7` (sha256 72ebbae0…).
- **Solver:** CaDiCaL 3.0.1 (git c607304, built here) with `--elim=0 --lrat --binary=false`.
  It answered UNSAT (exit 20) in 33 s wall and wrote a 170,827,636-byte LRAT proof
  (sha256 be9261f9…).
- **Checker:** cake_lpr, built from https://github.com/tanyongkiam/cake_lpr at a36874a8
  (`cake_lpr.S` sha256 2f3af32d…, the same as the repo's `cake_lpr.sha256`; HOL4 0ae70303,
  CakeML fb377b4b), compiled with gcc 13.3 -O2. It printed **`s VERIFIED UNSAT`** after 35 s.

Logs: `logs/d3_python_cnf_cadical_cakelpr.log`, `logs/cadical_n33k7d3_summary.log`,
`logs/tool_versions.txt` and `logs/d3_lean_cnf_cakelpr.log`. The last is a cake_lpr rerun directly on
the file from the package's own `lake exe d3_dimacs 33 7`; it gave `s VERIFIED UNSAT` in 42 s. The CNF and the proof are not committed. To regenerate:
`lake exe d3_dimacs 33 7 x.cnf`, then `cadical --elim=0 --lrat --binary=false x.cnf x.lrat`,
then `cake_lpr x.cnf x.lrat`.

**Trust base for "no heptagon-free labelled D3 configuration with 33 points":**
1. The Lean 4.24.0 kernel and the Mathlib/repository definitions (`Point`, `orient`,
   `HasConvexNGon`, `ConvexPosition`). The Lean proofs use only `propext`,
   `Classical.choice` and `Quot.sound`.
2. The unverified `IO` formatting in `Emit.lean`. It is cross-checked byte for byte against
   Python and against E's sha256.
3. cake_lpr, which is verified in HOL4/CakeML down to machine code. The trust here is the
   HOL4 logic, CakeML's compiler correctness theorem, the x64 assembly `cake_lpr.S` as
   shipped, the C FFI shim `basis_ffi.c`, gcc/ld for linking that shim, and the OS. Its
   DIMACS parser is part of the verified code.
4. The step "cake_lpr said UNSAT, therefore `¬ETV.DimacsSatisfiable (d3Cnf 33 7).2.2`".
   This step is not imported into Lean, so no axiom is added. It rests on cake_lpr's DIMACS
   semantics matching `ETV.DimacsSatisfiable`. Both are the standard CNF semantics.

CaDiCaL and the Python encoder are **not** trusted.

### Build

    cd cloud/es7-2026-10-19/results/H2
    mkdir -p .lake && ln -s ../../../../../.lake/packages .lake/packages   # share the parent's Mathlib
    lake build                 # D3Encoding (all modules, Audit included) and d3_dimacs
    scripts/compare_d3.sh      # byte comparison with d3cnf.py

Modules:
- `Clauses` (the generator) and `Emit` (the exe);
- `Triples` and `TripleTable` (the numbering and signs of triple variables);
- `Families` (A4, GP, centre, sector);
- `Canon` (the orbit minimum and idempotence);
- `Conv` (convexity, and its invariance under the group);
- `Sound` and `Main` (conv keys, the fold, and `d3Cnf_sat`);
- `Instance` (`groupClosed_11`);
- `Geometry` (`LabelledD3` and the point-set theorems);
- `Targets` (`D3LabellingTarget`, `D3Exclusion` and `d3Exclusion_of_unsat`);
- `Audit`.

`lake build` printed `Build completed successfully (1754 jobs)` (`logs/H2_lake_build.log`).

### 3. Remaining gap

1. **The labelling target** (`D3Encoding/Targets.lean`: `D3LabellingTarget : Prop`, not
   proved). It says that every D3-symmetric (`D3Symmetric`), heptagon-free 33-point set in
   general position yields a heptagon-free `LabelledD3 11`. Proving it needs:
   - the orbit classification (five 6-orbits and one 3-orbit is the only type in general
     position);
   - the choice of the reflection axis through the 3-orbit point;
   - sorting the 6-orbit representatives by angle and checking `sigma`'s label permutation;
   - the perturbation that puts the centre in general position without changing any
     orientation among the 33 points.

   `D3.d3Exclusion_of_unsat` (proved) turns the target plus the UNSAT fact into
   `D3Exclusion`.
2. **The UNSAT fact inside Lean.** The package's own kernel checker (`results/H/Rup.lean`,
   list-based, quadratic) cannot handle a 4.76-million-clause CNF with a 170 MB proof. The
   fact therefore stays external (cake_lpr), as in EmptyHexagonLean.
3. Non-vacuity: no explicit `LabelledD3 11` is constructed in Lean. That only matters for
   reading the theorem, not for soundness.
