# ENCBLEAN: encoder B in Lean (M0 design, M1 byte-identical port, M2 functional twin and numbering bridge, M3 combinatorial soundness, M9 hash binding, DIMACS round trip, re-solve script and review fixes; M4–M8 geometric half and end-to-end theorem, package `geo/`)

- **M1.** `EncB.gen m K t` is a Lean definition of the CNF that `C6UPPER/encb/gen_b2.py m K t` writes (gen_b2.py
  SHA-256 `3d47459a9723b5f7344205f3f2d7463e0be00b41c5070155e5da8dbf78fd40ba`). It has the same variable numbering,
  clause order and literal order as Python, for both even and odd m.
- **M2.** `EncB.encB m K t` is a second definition of the same CNF, written with list functions and closed-form
  variable codes (`genCoded`), then renumbered in the order of Python's `new()` calls (`allCodes`, `numberMap`).
  The theorems are about `encB`: model transfer, well-formedness, code decoding, and the cube cover of the 64 cubes.
- **M3.** `EncB.encB_satisfiable`: for even m ≥ 2, every `Model m K t` (the combinatorial interface of `DESIGN.md`
  §2.2, frozen as `EncB/Model.lean`) makes `encB m K t` satisfiable. Proved Std-only; its only hypotheses are
  `m % 2 = 0`, `2 ≤ m` and the `Model` (section "M3" below).
- `lake exe encb_dimacs` prints either one in gen_b2.py's DIMACS layout, and prints cubes in the layout of
  `C6UPPER/tools/mkcubes.py`. With `twin-cubes64` and `twin-cube64` the cubes are taken from the Lean list `cubes64`
  itself.
- **M9.** The text the exe prints for the base `encB 6 8 11` and for each of the 64 cubes of `cubes64` (by index) has
  the recorded SHA-256: for the base the hash of the generated file (`C6UPPER/SHA256SUMS.txt:86`, `encb_gen.log`),
  for each cube that of the file cake_lpr certified; 65/65 (plus 3 other instances, 68/68; compiled code, evidence).
  The printer is `EncB/Render.lean`, with a proved round trip through a reference DIMACS parser
  (`parseDimacs_render`, `cubesUnsat64_of_texts_get`; on the UTF-8 bytes, `parseDimacsBytes_cube64_get` in
  `EncB/Compose.lean`), and `no_model_6811_of_texts` (`EncB/Compose.lean`) composes it with M3: if the 64 printed
  texts parse to unsatisfiable lists, no `Model 6 8 11` exists. `scripts/resolve.sh` re-solves any of the 64 cubes
  with the pinned CaDiCaL and cake_lpr (smoke test 2/2; `all` not run). Section "M9" below.

**Status (2026-11-06, about 20:15 KST; the fixes of the two M9 reviews about 20:55–21:06 KST).**
- **M4–M8 are done (2026-11-07, about 05:35 KST; not committed; section "M4–M8 (geo)" below).** The package `geo/`
  (Mathlib) proves `EncB.Geo.sixfold_es8` (from `CubesUnsat64`) and `EncB.Geo.sixfold_es8_of_texts` (from the
  hypothesis of `no_model_6811_of_texts`, which `texts_iff_cubesUnsat64` shows equivalent to `CubesUnsat64`): every
  set of at least 61 points in general position that is invariant under the counterclockwise rotation by 2π/6 about
  some point has a convex octagon; `sixfold_es8_order6(_of_texts)` extend this to a rotation of order 6 in either
  direction (2π/6 or 2π·5/6). Axioms [propext, Classical.choice, Quot.sound], guarded by `#guard_msgs`;
  `geo/scripts/audit_geo.sh` PASS and its self-test 23/23 (after the review fixes of about 05:40–05:55 KST).
  Statements below that say M4–M8 are not done are superseded.
- **M3 is done (17:20 KST).** `encB_satisfiable` and `encB_satisfiable_6811` are proved, with no `sorry`, no
  unit statement left as a hypothesis, and axioms [propext, Classical.choice, Quot.sound] (section "M3" below).
- **M0, M1 and M2 are done, and the three fixes of the M2 review are applied** (section "M2 review fixes" below).
  The design is in `DESIGN.md` (§3.1 is M2, §3.2 M3; the plan M3 followed is `docs/M3PLAN.md`).
- **Risk R1 is resolved (16:35 KST).** The unit `c6upper-noty12` finished at 15:40:35 KST: cake_lpr accepted all 32
  n-cubes (base + ¬Y(1,2) + pattern), 32/32, each bound to the CNF and proof hashes, and `verify_final64.py` prints
  PASS (record `C6UPPER/noty12-2026-11-06/`). With the 32 encoder-B c-cubes of the replay, every verdict that
  `CubesUnsat64` asks for is certified, so variant A (64 cubes, no reflection) is the primary target with all 64
  verdicts in hand; variant B and M7′ are not needed (`DESIGN.md` D1, R1).
- **M2 in one paragraph.** `encB` is proved well formed (`encB_wf`). A model of the coded clauses transfers to a
  model of `encB` (`dimacsSat_of_holds`); membership of every code in the numbering holds by construction. The codes
  decode back to their variables (`decodeCode_code`). The 64 cubes cover all assignments, so the statement
  `(∀ c ∈ cubes64, ¬ DimacsSatisfiable (cubeCnf (encB 6 8 11) c)) → ¬ DimacsSatisfiable (encB 6 8 11)` is a
  theorem (`encB_unsat_of_cubes64`). `encB` equals `gen` and Python on everything tested: bytes on the 225-instance
  grid and the four recorded instances, Lean values on 229 instances, and kernel evaluation on 4 tiny instances,
  one of them, (4,5,1), with a two-level chain.
- **What the clauses mean is proved for even m (M3), relative to the combinatorial `Model`.** That a geometric
  counterexample yields a `Model` (M4–M6) and the assembly (M8) were not done as of M9; they are done since 2026-11-07
  (section "M4–M8 (geo)", commit ae42e816d).
- **M9 is done (2026-11-06, 17:50–20:15 KST; not committed).** A1: the mode `twin-cube64` and
  `scripts/hash_binding.sh` bind the base and all 64 cubes of `cubes64` (by index) and 3 other instances to the
  records, 68/68 (trust item E1). A2: `EncB/Render.lean`, a Std-only printer for the twin with a proved round trip
  through a reference DIMACS parser, which narrows trust items E3/E4. A3: `scripts/resolve.sh` and
  `scripts/build_cake_lpr.sh` for E2 provenance (risk R7). Each step was checked by an independent verifier or
  reviewer and fixed. P1 (`WRITEUP/P1/p1.tex` and the soundness note in both copies) now states what is Lean-checked
  for encoder B and what is not. Section "M9" below; the trust table after M9 is in "Trust". The findings of two
  reviews of M9 (Lean soundness, 6 minor; claims, 3 medium and 10 lower) were then applied (about 20:55–21:06 KST; not
  committed; section "M9 review fixes" below).
- **The package is Std-only:** no `[[require]]`, no Mathlib, toolchain `leanprover/lean4:v4.24.0` (Lean 4.24.0,
  commit `797c613e`).
- **No forbidden constructs and standard axioms:**
  - no `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `partial`, `axiom`, `opaque`,
    `set_option` or `ofReduceBool` (`scripts/audit.sh`);
  - no `decide`/`rfl`/`simp`/`omega`/`#eval`/`#reduce` anywhere in a declaration that mentions the (6,8,11) instance
    (`encB`, `gen`, `genCoded`, `numVars`, `allCodes`, `allCodesOf`, `encode` or `diagCoded` applied to 6 8 11, or
    `CubesUnsat64`); since the M9 review fixes also no `simpa`, `grind`, `trivial`, `Eq.refl`, `eq_self`,
    `Nat.decEq` or `decide_eq_true`, and a time gate: the files that state such theorems (Cover, Render,
    Satisfiable, Compose) elaborate within 60 s each (0.3–1.8 s as built);
  - every declaration of the package, 425 named ones (180 theorems written in the source; 236 and 47 before M3)
    found by walking the environment, has axioms within {propext, Classical.choice, Quot.sound}
    (`logs/axioms.log`); 26 of them are also guarded at build time by `#guard_msgs` (17 before M3). These counts
    are M3's; the declarations M9 added (Render.lean) are queried one by one in `logs/m9_axioms.log`, and 13 of them
    are guarded at build time. For the write-up 14 theorems were queried again, among them the 7 that P1 cites by
    name: all within the three axioms (`logs/m9_d_recheck.log`). The 7 declarations of `EncB/Compose.lean` (review
    fixes; 6 theorems and the definition `parseDimacsBytes`) are queried in `logs/m9_review_fix.log`, and 5 of them
    are guarded at build time.
- No git commit was made at the time; M9 was committed afterwards as 536800bfe.

## What exists

| file | lines | content |
|---|---|---|
| `DESIGN.md` | 770 | M0: target theorem (variant A: 64 cubes on Y12 Y13 Y14 Y23 Y24 Y34), trust list E1–E6, interfaces (`Model`, `PolarLabelling`), lemma map (with the as-built M3 map in §3.2), milestones M0–M9 (with M9's "done when" against what was built), risks; revision notes for M2, the M2 review fixes, R1, M3, M9 A2, M9 and the M9 review fixes at the top |
| `EncB/Gen.lean` | 382 | M1: the port (`canon`, `olit`, `angOuts`, `patternLit`, `unitOf`, itertools orders, `gen`). Unchanged since M1 (`ec97b335…`) |
| `EncB/Dimacs.lean` | 220 | M2: `DimacsSat`, `DimacsSatisfiable`, `LitSat` (copied from H/H3); `numberMap` (an `Array`), `decode`, `numberMap_getD`, `decode_numberMap`; re-proofs of Mathlib's `List.idxOf_cons_ne` and `List.getElem_idxOf`; `dedupStep` with `mem_dedup_foldl` |
| `EncB/Coded.lean` | 460 | M2: `Var`, the codes and `decodeCode_code`; the twin `genCoded`, `allCodes`, `encB`, `numVars` (via `encode`); `mem_allCodes`, `dimacsSat_of_holds`, `encB_wf`; `diagCoded` (refusal flags for the emitter only) |
| `EncB/Cover.lean` | 121 | M2: `CubeSat`, `Covers`, `cubeCnf`, `not_dimacsSatisfiable_of_cover` (copied from H3); `signPatterns`, `covers_signPatterns`; `cubeVars64`, `cubes64`, `CubesUnsat64`, `encB_unsat_of_cubes64` |
| `EncB/KernelCheckB.lean` | 102 | M2: `decide +kernel` on `encB`/`numVars` at (3,4,1), (3,4,2), (6,4,1), (4,5,1), on `gen` at (4,5,1) and on `codesDecode` at (3,4,2); `#guard_msgs` axiom audit of the M2 theorems |
| `EncB/Emit.lean` | 319 | M1's modes unchanged (with M1's printer `pushClause`/`body`/`header`/`cubeTail`, used only by them); M2's `twin-*` modes; M9 A1's `twin-cube64`. Since M9 A2 every twin mode prints through Render's `cnfText`/`renderCube`; M2's twin printer `bodyL`, `cubeBody`, `cubeBody_eq` was removed (superseded by `renderCube_eq`) |
| `EncB/Render.lean` | 890 | M9 A2: the twin's DIMACS printer (`pushNat`, `pushInt`, `pushClauseR`, `bodyR`, `headerR`, `cubeBodyR`, `render`, `renderCube`, `cnfText`), the reference parser `parseDimacs` with 14 kernel-checked examples, the round trip `parseDimacs_render`, `renderCube_eq`, `cnfText_encode`, the (6,8,11) instances `parseDimacs_base6811`, `parseDimacs_cube64_get`, `cubesUnsat64_of_texts(_get)`, `encB_unsat_of_texts(_get)`, and `cnfText_bytes`; 13 `#guard_msgs` axiom guards (section "Trust") |
| `EncB/KernelCheck.lean` | 35 | M1: `decide +kernel` on `gen` at (3,4,1), (3,4,2), (4,4,2) |
| `EncB/Model.lean` | 196 | M3 (U0, frozen interface): `Model`, `ChainFrom`, `baseVal`, `tauOf`, `Model.τ`, `Model.τc`; the intermediate specs `OlitSpec`, `OrbListSpec`, `RkMono`, `PatternSpec`, `SortSpec`, `ObjLtSpec`, `objImg`, `SortedSix`, `WordSpec`; `Decidable` instances (used only by the early-warning test) |
| `EncB/ModelLemmas.lean` | 162 | M3 (U0): literal semantics (`codeLitHolds_neg`, `holds_y`, `holds_orb`, `holds_f`), `perm012_cases`, `chi_perm3`, membership lemmas |
| `EncB/SortLemmas.lean` | 164 | M3 (U0): `mem_perms`, `insSort_perm`, `insSort_pairwise`, `Obj.lt_iff`, `sortSpec`, position lemmas for `ccwIn` on strictly sorted lists |
| `EncB/SoundOlit.lean` | 94 | M3 (U0): `rotBy`, `chi_rotBy`, `orbVarC_some`, `olitSpec` (an orbit literal holds iff `chi` of its labels) |
| `EncB/SoundOrbit.lean` | 233 | M3 U1: `orbListSpec`, `transCl_sound`, `nestLits_sound` (helpers in `EncB.Orbit`) |
| `EncB/SoundChain.lean` | 218 | M3 U2: `chainCl_sound` (helpers in `EncB.Chain`) |
| `EncB/SoundAng.lean` | 369 | M3 U3: `angCl_sound` (helpers in `EncB.Ang`) |
| `EncB/SoundRules.lean` | 276 | M3 U4: `Rules.sortSix`, `Rules.patternSpec_of_sort`, `patternSpec_of` (helpers in `EncB.Rules`) |
| `EncB/SoundWord.lean` | 229 | M3 U5: `wordSpec` (helpers in `EncB.Word`) |
| `EncB/Satisfiable.lean` | 52 | M3: `genCoded_sound`, **`encB_satisfiable`**, `encB_satisfiable_6811`; `#guard_msgs` on the axioms of the last two |
| `EncB/Compose.lean` | 104 | M9 review fixes: `parseDimacsBytes` (the reference parser on a byte list), `cnfText_ascii`, `parseDimacsBytes_cnfText`, `parseDimacsBytes_cube64_get` (the round trip on the UTF-8 bytes); **`no_model_6811_of_texts`** (M3 composed with `encB_unsat_of_texts_get`) and `no_model_6811_of_bytes`; 5 `#guard_msgs` axiom guards. Imported by `EncB.lean` only, not by the exe's root, so the exe is unchanged |
| `EncB/EarlyWarning.lean` | 436 | M3 U6: the early-warning test (evidence only; run by `lean --run`, not imported by `EncB.lean`, not built) |
| `scripts/ew_test.sh` | 34 | M3 U6: runs the early-warning test under the cap, logs it, exits nonzero unless `EW SUMMARY: PASS` |
| `docs/M3PLAN.md`, `docs/m3start/` | 607 | the M3 plan (judge of two plans) and the unit start files, copied verbatim by U0 |
| `ref/make_ref.py`, `ref/hashes.tsv` | 80 | M1: the reference corpus (225 instances from gen_b2.py) |
| `scripts/compare_b.sh` | 34 | the 225 grid instances by SHA-256; second argument `gen` or `twin` |
| `scripts/twin_check.sh` | 25 | M2: `encB = gen` as Lean values (no printing) on the grid plus extra instances |
| `scripts/check_recorded.sh` | 127 | recorded instances; third argument `gen` or `twin`. Twin `big` = one emission of (6,8,11) with cubes from `cubes64`, the cube-variable check and the emitted-file check |
| `scripts/audit.sh` | 92 | static checks (forbidden tokens, Std-only, toolchain, no kernel evaluation of the (6,8,11) instance, checked per declaration) and, since the M9 review fixes, a time gate (`lake build --no-build` up to date; each file that states (6,8,11) theorems elaborates with `lake env lean` within 60 s); must run in the capped scope after `lake build` |
| `scripts/hash_binding.sh` | 315 | M9 (E1): streams `twin-base 6 8 11`, `twin-cube64 6 8 11 I` (I = 0..63) and 3 other instances into sha256sum and compares each hash with every record of its name, read from the record files; logs the hashes of every source of the exe (the import closure of `EncB/Emit.lean`); since the M9 review fixes it stops unless `lake build --no-build` reports the build up to date, runs only a copy of the exe (hash compared at the end) and requires `twin-cube64 6 8 11 64` to be refused |
| `scripts/resolve.sh` | 611 | M9 (E2 provenance, R7): `resolve.sh CUBES OUTDIR` emits each requested cube with `twin-cube64`, checks its hash against both records, solves it with the pinned CaDiCaL 2.1.3 and checks the proof with the pinned cake_lpr; append-only `results.tsv` (23 columns); section "M9" |
| `scripts/build_cake_lpr.sh` | 91 | M9: the build recipe of cake_lpr commit `033aad53` (source hashes pinned from the local clone, first recorded by M9; clean environment; expected binary `c14ff498…`); **not run** |
| `logs/` | | see "M3", "M2 results", "M2 review fixes" and "M1 results" below; `env.txt` has every source hash (as of M2); `axioms_enum.lean.txt` and `axioms_query.lean.txt` are the two axiom queries; M3: `m3_u0_*` (U0), `m3_build.log`, `m3_mutants.log`, `m3_early_warning.log` (U6's run), `m3_early_warning_integ.log` (Integration's rerun); M9: `m9_*` (A1: `m9_hash_binding.log`, `m9_hash_binding_selftest.log`, `m9_regress_modes.log`; A2: `m9_a2_*`, with sections in `m9_build.log`, `m9_audit.log`, `m9_axioms.log`; the A2 fixes: `m9_a2fix_hash_binding.log` and further sections in those three; A3: `m9_resolve_smoke.log`, `m9_review_resolve.log`, `m9_resolve_fix.log`; write-up: `m9_d_recheck.log`; reviews: `m9_review_lean_soundness.log`; review fixes: `m9_review_fix.log`, `m9_review_fix_hash_binding.log`); table in section "M9" |

Lines of Lean code written in M2, without blank and comment lines: Dimacs 154, Coded 285, Cover 73, KernelCheckB 40
(30 before the review fixes), plus 133 in Emit.lean (from 90 to 223 such lines; 132 to 301 lines in all). Scripts:
`twin_check.sh` is new; the other three gained a mode argument (+8, +48 and +10 lines). The review fixes rewrote
check 4 of `audit.sh` (35 to 64 lines).

## How to build and run

Every compile and every run goes at nice 10, one at a time, inside an 8 GB scope. `lake build` is run only in this
directory.

```
cd cloud/es7-2026-10-19/results/ENCBLEAN
export PATH=$HOME/.elan/bin:$PATH
CAP="systemd-run --user --scope -q -p MemoryMax=8G -p MemorySwapMax=0 nice -n 10"
$CAP lake build                                        # clean (M2): 21 s wall, 2.1 GB peak (KernelCheckB 17-19 s, KernelCheck 11 s); the 10 M3 modules add about 10 s, 0.45 GB
$CAP scripts/audit.sh                                  # after lake build: its time gate runs lake build --no-build and lake env lean
bash scripts/ew_test.sh [LOG]                          # M3 early-warning test, about 6 min; caps itself at 4 GB (default LOG overwrites logs/m3_early_warning.log)
$CAP scripts/compare_b.sh ref/hashes.tsv twin          # 48 s; the 225 grid instances, encB
$CAP scripts/compare_b.sh ref/hashes.tsv gen           # 23 s; the same, gen (M1)
$CAP scripts/twin_check.sh ref/hashes.tsv '6 8 9' '7 8 9' '7 8 10'   # 110 s; encB = gen as values
$CAP scripts/check_recorded.sh SCRATCH small twin      # 33 s; (6,8,9), (7,8,9), (7,8,10)
$CAP scripts/check_recorded.sh SCRATCH big twin        # 16 s; (6,8,11) once, ~470 MB transient in SCRATCH, deleted
$CAP python3 ref/make_ref.py OUT.tsv                   # 59 s; regenerates the corpus from gen_b2.py
```

M9 ran `hash_binding.sh` under the 4 GB cap (`MemoryMax=4G`) instead of `$CAP`; `resolve.sh` caps each step itself (4 GB
for emission and CaDiCaL, 12 GB for cake_lpr):

```
TMPDIR=SCRATCH systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10 scripts/hash_binding.sh   # ~15 min; exit 0 iff 68/68
nice -n 10 scripts/resolve.sh CUBES OUTDIR             # caps each step itself (4G emit/CaDiCaL, 12G cake_lpr); OUTDIR under /path/to/data
```

How to call the exe (the `twin-*` modes print `encB`, the others print `gen`):

```
.lake/build/bin/encb_dimacs twin-base 6 8 11 > B.cnf                    # encB 6 8 11
.lake/build/bin/encb_dimacs twin-cube 6 8 11 1 2 3 -10 11 18 > c.cnf    # cubeCnf (encB 6 8 11) [1, 2, 3, -10, 11, 18]
.lake/build/bin/encb_dimacs twin-cubes64 6 8 11 DIR [NAME ...]         # DIR/base.cnf + the cubes of cubes64 (all 64 if no NAME)
.lake/build/bin/encb_dimacs twin-cube64 6 8 11 I > c.cnf                # cubeCnf (encB 6 8 11) (cubes64.get I), I = 0..63 (M9)
.lake/build/bin/encb_dimacs twin-check 6 8 11                           # encB = gen in memory, nothing written
.lake/build/bin/encb_dimacs twin-stats|twin-ymap|twin-profile M K T     # summary line / Y numbering / phase times
.lake/build/bin/encb_dimacs base|stats M K T, cube M K T U..., files M K T DIR NAME...   # gen, as in M1
```

- **Cube names.** `cBBBBB` is the cube whose first unit is +Y12, followed by the pattern on Y13 Y14 Y23 Y24 Y34,
  where bit 1 means a positive literal; these are mkcubes' 32 cubes. `nBBBBB` is the same pattern with −Y12 first;
  these are the cubes of the c6upper-noty12 run. `twin-cubes64` derives each name from the signs of the cube
  (`cubeName`, Emit.lean:88). It writes only cubes of `cubes64`, in list order.
- **Variable numbers.** At t = 11, Y12 Y13 Y14 Y23 Y24 Y34 are the variables 1, 2, 3, 10, 11 and 18
  (`cubeVars64`).
- **Refusal.** On an instance where gen_b2.py raises, the exe writes nothing and exits with 1. For the twin this is
  decided by `diagCoded`.

## M4–M8 (geo): the geometric half and the end-to-end theorem (2026-11-07, about 05:00–05:35 KST; committed ae42e816d)

**What is proved.** The package `geo/` (Lean package `es8geo`, Lean 4.24.0, Mathlib `f897ebcf72cd16f8…` in
`geo/.lake`, `encblean` required by path `..`) proves that a counterexample yields a `Model`, and composes this
with M3 and M9:

- **M5** `labelling_of_counterexample` (`ES8Geo/Labelling.lean`): an m-fold counterexample (any even m ≥ 2, with
  K ≤ 2m) with `m·t` points has a polar labelling of its `t` layers (`PolarLabelling`, frozen in `ES8Geo/Interface.lean`).
- **M6** `modelOfLabelling` (`ES8Geo/ModelOfLabelling.lean`): the labelling's intended model, `chi := L.chi`
  (`decide (0 < orient (P a) (P b) (P d))`) and `psiLt := L.psiLt` (`decide (ψ i < ψ j)`); `modelOfLabelling_chi`
  and `modelOfLabelling_psiLt` record this by `rfl`. The 13 fields come from `ES8Geo/ModelBasic.lean` (G1–G7:
  the `psiLt` laws, `chi_rot`, `chi_cycle`, `chi_swap`, `nest`, `noChain`) and `ES8Geo/ArcBridge.lean` (G8–G9:
  `objLt` is the real circular order of the directions, `ccwIn` is a real arc, and rules A/B from
  `PhaseClassification.orient_pos_of_alternating` / `orient_pos_of_runMidB`).
- **M8** `ES8Geo/Main.lean`: `sixfold66_of_no_model` (M5 + M6), `sixfold66_of_unsat` (+ M3),
  `sixfold66_of_cubes64` (+ the cover), `sixfold_es8` and `sixfold_es8_of_texts` (+ `sixfold_octagon`, Capstone2),
  and for the clockwise case `sixfold_es8_order6`, `sixfold_es8_order6_of_texts` (invariance under a rotation by
  2π/6 or by 2π·5/6; `invariant_sixth_of_five`: invariance under ρ⁵ gives invariance under ρ²⁵ = ρ;
  `rotAbout_neg_sixth`: the rotation by 2π·5/6 is the rotation by −2π/6). `ES8Geo/Audit.lean` adds
  `texts_iff_cubesUnsat64`: the texts hypothesis ↔ `CubesUnsat64`.

**The final statements, as `#check @…` prints them** (pinned by `#guard_msgs` in `ES8Geo/Audit.lean`):

```
EncB.Geo.sixfold_es8 : EncB.CubesUnsat64 →
  ∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
    ErdosSzekeres.GeneralPosition S →
      ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 6)) S →
        61 ≤ S.card → ErdosSzekeres.HasConvexNGon 8 S
EncB.Geo.sixfold_es8_of_texts : (∀ (i : ℕ) (hi : i < EncB.cubes64.length) (nv : ℕ) (G : List (List ℤ)),
    EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G) →
  ∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
    ErdosSzekeres.GeneralPosition S →
      ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 6)) S →
        61 ≤ S.card → ErdosSzekeres.HasConvexNGon 8 S
EncB.Geo.sixfold_es8_order6 : EncB.CubesUnsat64 →
  ∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
    ErdosSzekeres.GeneralPosition S →
      ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 6)) S ∨
          ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi * 5 / 6)) S →
        61 ≤ S.card → ErdosSzekeres.HasConvexNGon 8 S
EncB.Geo.sixfold_es8_order6_of_texts : (the hypothesis of sixfold_es8_of_texts) → (the conclusion of
  sixfold_es8_order6, from ∀ S c on)
EncB.Geo.rotAbout_neg_sixth : ∀ (c : ErdosSzekeres.Point),
  ErdosSzekeres.LayerLemma.rotAbout c (-(2 * Real.pi / 6)) = ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi * 5 / 6)
EncB.Geo.texts_iff_cubesUnsat64 : (∀ (i : ℕ) (hi : i < EncB.cubes64.length) (nv : ℕ) (G : List (List ℤ)),
    EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G) ↔
  EncB.CubesUnsat64
EncB.Geo.sixfold66_of_unsat : ¬EncB.DimacsSatisfiable (EncB.encB 6 8 11) → ErdosSzekeres.LayerLemma.Sixfold66
EncB.Geo.sixfold66_of_cubes64 : EncB.CubesUnsat64 → ErdosSzekeres.LayerLemma.Sixfold66
EncB.Geo.sixfold66_of_no_model : (∀ (a : EncB.Model 6 8 11), False) → ErdosSzekeres.LayerLemma.Sixfold66
@EncB.Geo.modelOfLabelling : {m K t : ℕ} → 3 ≤ m → Even m → 4 ≤ K → K ≤ 2 * m →
  {T : Finset ErdosSzekeres.Point} → {c : ErdosSzekeres.Point} → ErdosSzekeres.GeneralPosition T → c ∉ T →
  ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / ↑m)) T →
  ¬ErdosSzekeres.HasConvexNGon K T → EncB.Geo.PolarLabelling m t T c → EncB.Model m K t
@EncB.Geo.labelling_of_counterexample : ∀ {m K t : ℕ}, 2 ≤ m → Even m → K ≤ 2 * m →
  ∀ {T : Finset ErdosSzekeres.Point} {c : ErdosSzekeres.Point}, ErdosSzekeres.GeneralPosition T → c ∉ T →
  ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / ↑m)) T →
  ¬ErdosSzekeres.HasConvexNGon K T → T.card = m * t → Nonempty (EncB.Geo.PolarLabelling m t T c)
```

(`modelOfLabelling` and `labelling_of_counterexample` are re-wrapped here, Lean prints one binder per line, and
`sixfold_es8_order6_of_texts` is abbreviated; `Audit.lean` pins every one of them verbatim, and also
`modelOfLabelling_chi` and `modelOfLabelling_psiLt`.)
`Sixfold66` (Capstone2.lean:1110) is `∀ T c, GeneralPosition T → c ∉ T → Invariant (rotAbout c (2 * Real.pi / 6)) T →
T.card = 66 → HasConvexNGon 8 T`. The hypothesis of `sixfold_es8_of_texts` is, token for token, that of
`EncB.no_model_6811_of_texts` (Compose.lean:72; an `example` in Audit.lean applies one to the other): each of the
64 texts the exe prints with `twin-cube64 6 8 11 i` parses, by `parseDimacs`, to an unsatisfiable clause list. That
is what cake_lpr's 64 verdicts are taken to mean (trust item E3). The hypothesis is not vacuous (a failing parse
would make it trivially true): `texts_iff_cubesUnsat64` proves it equivalent to `CubesUnsat64`, by
`cubesUnsat64_of_texts_get` one way and by `parseDimacs_cube64_get` with `Option.some.inj` the other, as a term
(`cases` would try to reduce `encB 6 8 11`).

**Axioms.** Every theorem above, and `modelOfLabelling`, depends on [propext, Classical.choice, Quot.sound];
fourteen `#guard_msgs in #print axioms` and thirteen `#guard_msgs in #check` in `ES8Geo/Audit.lean` make
`lake build` fail if this or a statement changes. Each unit file also ends with `#print axioms` for its own theorems (`logs/m8_build.log`).

**The proof chain of `sixfold_es8_of_texts h S c hgp hinv hcard`.**
`sixfold_octagon (sixfold66_of_no_model (EncB.no_model_6811_of_texts h)) S c hgp hinv hcard`, where
`no_model_6811_of_texts` is M3 + M9 (Std-only) and `sixfold66_of_no_model` takes a 66-point counterexample `T`,
casts the real `6` of `Sixfold66` to `((6 : ℕ) : ℝ)` (`MainAux.invariant_cast_six`), gets `L` from M5 with m = 6,
K = 8, t = 11 and applies `h` to `modelOfLabelling … L`. The side conditions `3 ≤ 6`, `2 ≤ 6`, `Even 6`, `4 ≤ 8`,
`8 ≤ 2 * 6` and `66 = 6 * 11` are one lemma, `MainAux.numerals`, closed by `norm_num`/`decide` on these numerals
alone. Every declaration that mentions the instance (`Model 6 8 11`, `encB 6 8 11`, `CubesUnsat64`, …) is a term
with no tactic block (`sixfold66_of_no_model` is `Classical.byContradiction` with `Nonempty.elim`), so nothing
evaluates `encB 6 8 11`; audit check 5 enforces this.

**Files** (`geo/`; line counts with comments):

| file | lines | content |
|---|---|---|
| `ErdosSzekeres/**` (10 files) | — | verbatim copies of the repository modules at commit `536800bf`, `VENDOR.sha256` (M4) |
| `ES8Geo/Capstone2.lean`, `KeyOrder.lean`, `OrbitConsistency.lean` | 2132, 158, 429 | verbatim copies of `LEANEXT/{capstone,keys,orbit}/…`, `SOURCES.sha256` (M4) |
| `ES8Geo/Orbit.lean` | 21 | `orient_rotAbout_inv` for `LayerLemma.rotAbout` (M4) |
| `ES8Geo/Interface.lean` | 53 | `PolarLabelling`, `L.P`, `L.chi`, `L.psiLt`, frozen before the M5/M6 units (M4) |
| `ES8Geo/Labelling.lean` | 161 | M5 (`EncB.Geo.Lab`) |
| `ES8Geo/ModelBasic.lean` | 231 | M6 fields G1–G7 (`EncB.Geo.Basic`) |
| `ES8Geo/ArcBridge.lean` | 497 | M6 G8–G9 and rules A/B (`EncB.Geo.Arc`) |
| `ES8Geo/ModelOfLabelling.lean` | 52 | M6 assembly |
| `ES8Geo/Main.lean`, `ES8Geo/Audit.lean` | 138, 202 | M8 (with the review fixes) |
| `scripts/audit_geo.sh` | 358 | M8 audit and its `--selftest` (below) |

**How to rebuild.** `lake-manifest.json` pins Mathlib, so `lake update` is **not** needed (and would move the pin).

```
cd cloud/es7-2026-10-19/results/ENCBLEAN/geo
export PATH=$HOME/.elan/bin:$PATH
CAP="systemd-run --user --scope -q -p MemoryMax=8G -p MemorySwapMax=0 nice -n 10"
lake exe cache get          # Mathlib oleans for f897ebcf (7335 files, about 6 GB in geo/.lake; network)
$CAP lake build             # M4: 32 s wall, 2176 jobs, 2.9 GB (logs/m4_build.log); M5–M8 add 6 modules, about 10 s, 2.4 GB (logs/m8_build.log, logs/m8_fix_build.log)
scripts/audit_geo.sh        # read-only; exit 0 iff AUDIT PASS (logs/m8_fix_audit.log); about 47 s
scripts/audit_geo.sh --selftest   # plants 22 violations in a temporary copy; exit 0 iff SELFTEST PASS (logs/m8_fix_selftest.log); about 10 s
```

`scripts/audit_geo.sh` checks (the header of the script states each one exactly):
1. **Pinned files.** `SOURCES.sha256` verifies with exactly 5 OK lines and lists exactly the non-unit ES8Geo files;
   `VENDOR.sha256` exactly 10. A PINNED list inside the script binds by SHA-256 the build configuration
   (`geo/{lakefile.toml, lake-manifest.json, lean-toolchain}`, `../{lakefile.toml, lean-toolchain,
   lake-manifest.json}`), the two manifests themselves, and the Std-only package `../EncB.lean`, `../EncB/*.lean`
   (the definitions `Model`, `encB`, `encode`, `cubes64`, `cubeCnf`, `CubesUnsat64`, `cnfText`, `parseDimacs`,
   `DimacsSatisfiable` that give the final theorems their meaning), with no unlisted file in `../EncB`. Neither
   lakefile sets Lean options (`leanOptions`, `moreLeanArgs`, `weakLeanArgs`, server args, …; such an option could
   turn off kernel checking for the build). The geo manifest pins Mathlib `f897ebcf` and every package of the
   repository's `lake-manifest.json` at the repository's revision, and each checkout in `geo/.lake/packages` is at its
   manifest revision with no tracked change.
2. **Git cross-checks** against the commit recorded in `VENDOR.sha256` (`536800bf`, the M9 commit), not the moving
   HEAD: the 10 vendored modules and every PINNED file under `../` equal that commit (34 files); once `geo/` is
   committed, `SOURCES.sha256` and `VENDOR.sha256` equal their committed versions. Outside a git checkout (or with
   `AUDIT_NO_GIT=1`) these are skipped with a note; the PINNED hashes still bind every file.
3. Capstone2, KeyOrder and OrbitConsistency equal the LEANEXT files byte for byte.
4. No `sorry`, `sorryAx`, `admit`, `native_decide`, `axiom` declaration, `opaque`, `implemented_by`, `extern`,
   `unsafe`, `maxHeartbeats 0`, `skipKernelTC`, `ofReduceBool`, `ofReduceNat`, `reduceBool`, `reduceNat` in the code of
   `ES8Geo/*.lean`, `ES8Geo.lean` and `ErdosSzekeres/**` (22 files; there is no `maxHeartbeats` at all). Comments are
   stripped by a scanner that nests block comments and keeps string and char literals, so `"/-"` in a string cannot
   hide code.
5. In the six M5–M8 files, a *mention* of the instance is `encB`/`gen`/`genCoded`/`numVars`/`allCodes`/`allCodesOf`/
   `encode`/`diagCoded`/`Model` applied to `6 8 11`, a named argument `(m := 6)`/`(K := 8)`/`(t := 11)`,
   `CubesUnsat64`, `cubes64`, `cubeVars64`, `cubeCnf`, `cnfText`, `parseDimacs*`, `encB_unsat*` or any name containing
   `6811`. (a) No `decide`/`rfl`/`norm_num`/`simp`-family/`omega`/`trivial`/`grind`/`aesop`/`#eval`/`#reduce`/… within
   3 lines of a mention; (b) a declaration that mentions the instance contains no `by` at all (it is a term);
   (c) the files define no macro, syntax, elaborator or notation. Today: Main.lean 7 and Audit.lean 3 such
   declarations, all terms. This is a text check (a local abbreviation for 6 would evade it); the time limit of
   check 7 is the real protection.
6. `ES8Geo.lean` imports every module.
7. `lake build --no-build` is up to date (so every `#guard_msgs` of Audit.lean passed), and all six M5–M8 files
   (Labelling, ModelBasic, ArcBridge, ModelOfLabelling, Main, Audit) elaborate again with `lake env lean` within
   300 s each (3.6–12.3 s as built) with no `file:line:col: error` line; the axioms of the main theorems are printed
   and must be the standard three. `lake env lean` uses no package Lean options, and check 1 makes sure there are
   none, so this re-elaboration also re-runs the kernel on every declaration of the six files.

`scripts/audit_geo.sh --selftest` copies `geo/` (without `.lake`), `../EncB*`, the `../` build files and the three
LEANEXT sources to a temporary directory and plants one violation per run: a tactic, `decide`, a named-argument
instance or `#eval` near the instance, a tactic block with no listed tactic, a macro, an `axiom`, `maxHeartbeats 0`,
`sorryAx`, a `sorry` behind a string holding `/-`, a `sorry` after a nested block comment, a missing import, an
edited Interface.lean (also after deleting its line from `SOURCES.sha256`), an edited or an unlisted vendored module,
`leanOptions` in `geo/lakefile.toml`, `moreLeanArgs` in `../lakefile.toml`, an edited `lean-toolchain`, an edited
`../EncB/Model.lean`, an extra file in `../EncB`, a changed LEANEXT source. Each must end AUDIT FAIL (exit 1), and the
clean copy AUDIT INCOMPLETE (exit 3, the build gate is skipped in the copy). Run 2026-11-07 05:52: **23/23, SELFTEST
PASS**; the audit itself: **AUDIT PASS**, exit 0, 47 s (`logs/m8_fix_audit.log`).

**Decisions and deviations.**
- **Vendored modules, not a path require of the repository.** Requiring the repository by path would make lake build
  it inside the repository's own `.lake`, which is frozen and must not be touched. So the ten
  repository modules the geometry imports (the closure of `ErdosSzekeres.{Definitions, Orientation,
  OrientationGeometry, Suk.OrientationClique}`) are copied verbatim into `geo/ErdosSzekeres/`; every constant keeps
  its repository name, `VENDOR.sha256` records the hashes and audit check 2 compares them with the recorded
  commit `536800bf`. Mathlib is
  fetched into `geo/.lake` (R5, option (a), the author's choice of 2026-11-07).
- **Capstone2 kept whole.** The M4 row planned to split Capstone2 into `Layer`/`Phase`/`Link`/`PhaseClass`/`Capstone`
  modules. It is kept as one verbatim file instead, so the statements are checked by a hash (audit check 3), not by a
  diff of a split. DESIGN's "LL line n" is Capstone2 line n + 8 (n ≥ 10).
- **Interface: typed binders in `PolarLabelling`.** In DESIGN §2.1 the `k` of `mem_layer` is untyped and occurs only
  as `(k : ℝ)`, so Lean would read it as a real number and the field would claim membership for every real `k`,
  which is false for every actual configuration. `Interface.lean` types the binders (`i k : ℕ`); nothing else in
  §2.1 changed.
- **Binders of the field theorems.** Each takes only the standing hypotheses it uses, in the standing order and with
  the standing names (`labelling_ruleA hm heven L`, `labelling_nest hm hK hgp hc hinv hno L`, …).
  `labelling_of_counterexample` takes `hm : 2 ≤ m` and `hcard : T.card = m * t`, as in §2.1.
- **Added:** `sixfold66_of_no_model`, the common core of `sixfold66_of_unsat` and `sixfold_es8_of_texts`.
  `sixfold_es8_of_texts` goes through `no_model_6811_of_texts`, not through `CubesUnsat64`.
- **Direction of the rotation.** `sixfold_es8` and `sixfold_es8_of_texts` are the counterclockwise case, as in
  P1 thm:main(a) ("a rotation by 2π/6"). P1's cor:es8 and DESIGN §1.1's optional add-on also allow a rotation of order
  6 by 2π·5/6 (= ρ⁻¹); `sixfold_es8_order6` and `sixfold_es8_order6_of_texts` cover it (invariance under ρ⁵ gives
  invariance under ρ²⁵ = ρ, with no finiteness needed).
- **ArcBridge** handles the three cyclic cases of `ccwIn` by lifting two directions by 2π (`Arc.lift3`) instead of
  the cyclic relabelling through `orient_cycle` planned in DESIGN §3.4; it uses only the fields `r_pos`, `r_anti`,
  `ψ_zero`, `ψ_pos`, `ψ_lt` (and `ψ_inj` in `rdir_eq_iff`).
- **Not re-run in M8:** the mutation tests of the M8 row (a changed `genCoded` family changes the hashes; a deleted
  `Model` field breaks M3). They were done in M3 (13/13 field mutants and the nesting mutant) and M9 (the hash
  self-test); M8 changed neither `genCoded` nor `Model`.

**Process.** M5 and the two M6 units (`ModelBasic`, `ArcBridge`) were written in parallel against the frozen
Interface, each checked by `lake env lean` only and then by an independent verifier (compile, exact statements
by `Expr` comparison or typed `example`, axioms, tokens, frozen hashes); logs `logs/m5m6_{M5,M6basic,G9rules}.log`.
The G9 go/no-go spike (R2) passed on the first attempt. The integrator wrote ModelOfLabelling, Main and Audit, and
ran the only `lake build`s (`logs/m8_build.log`) and the audit (`logs/m8_audit.log`). M4–M8 with the review fixes
were committed afterwards as ae42e816d.

**Review fixes (2026-11-07, about 05:40–05:55 KST).** An independent review of M4–M8 gave 11 findings (2 major,
9 minor); none concerned a proof. Disposition:

| finding | disposition |
|---|---|
| only the counterclockwise rotation by 2π/6 is covered (P1 cor:es8 also allows 2π·5/6) | **fixed:** `sixfold_es8_order6`, `sixfold_es8_order6_of_texts`, `invariant_sixth_of_five`, `rotAbout_neg_sixth` (Main.lean); "Direction of the rotation" above |
| P1 is out of date (Rigor text, line 292 "without Mathlib", line 1057 future work) | **not edited:** P1 is outside this package and was left to the operator; the items for its revision are listed under "Trust after M4–M8" below |
| README's "only hypothesis is the meaning of the verdicts" is imprecise; nothing shows the texts hypothesis is not vacuous | **fixed:** `texts_iff_cubesUnsat64` (Audit.lean, a term, pinned) and the sentence reworded |
| check 5 missed `Model 6 8 11` and named arguments (`sixfold66_of_no_model` used `norm_num`/`decide` unchecked) | **fixed:** wider mention pattern; such declarations must be terms; `sixfold66_of_no_model` rewritten as a term, numerals in `MainAux.numerals` |
| (major) the build configuration is not hash-checked; `leanOptions` could disable the kernel for unit modules that check 7 did not re-elaborate | **fixed:** PINNED hashes of both lakefiles, manifests and toolchains; grep for Lean options; manifest revisions compared with the repository's and with the checkouts; check 7 re-elaborates all six M5–M8 files |
| (major) check 6 compared `EncB/` with the moving HEAD and omitted `EncB.lean`, `../lakefile.toml` | **fixed:** `../EncB.lean`, `../EncB/*.lean` and the `../` build files are in PINNED, and check 2 compares them with commit `536800bf` |
| check 2 used HEAD and needed git; check 1 did not assert the counts 5 and 10 | **fixed:** commit from the `VENDOR.sha256` header; runs without git (cross-checks skipped with a note); counts asserted; `SOURCES.sha256` must list exactly the non-unit files; the manifests themselves are pinned |
| check-5 pattern too narrow; `FORB` lacked `sorryAx`, `ofReduceNat`, `reduceBool`, `reduceNat`; the comment stripper mangled strings | **fixed:** pattern extended (`cubes64`, `cnfText`, `parseDimacs*`, `*6811*`, …), the four tokens added, a stripper that nests block comments and keeps string/char literals |
| only 4 statements pinned; no axiom pins for the two `rfl` lemmas | **fixed:** 13 `#check` and 14 `#print axioms` pins, including `sixfold66_of_no_model`, `modelOfLabelling(_chi/_psiLt)`, `labelling_of_counterexample` |
| `grep -q 'error'` too loose; negative tests not reproducible | **fixed:** `^file:line:col: error`; `audit_geo.sh --selftest` (23 cases) |
| "6-fold-type counterexample" understates M5 | **fixed:** "an m-fold counterexample (any even m ≥ 2, with K ≤ 2m)" |

`lake build` after the fixes: green, 2200 jobs, 13 s, 2.5 GB (`logs/m8_fix_build.log`).

**Trust after M4–M8.** M4–M8 remove the one step that was missing rather than trusted: that a geometric
counterexample yields a `Model 6 8 11` (KS steps S5, S7, S8, the geometric side of S11–S17, and the
composition S22; `DESIGN.md` §1.5). The composition with `sixfold_octagon` is now one Lean term. What stays trusted
is the list E1–E6 (`DESIGN.md` §1.4, the table in "Trust" below), unchanged in content:
- **E1** the hash binding (compiled exe) ties the texts of the hypothesis of `sixfold_es8_of_texts` to the 64 files
  cake_lpr checked; **E2** the 64 verdicts; **E3** that cake_lpr reads those texts as `parseDimacs` does and that its
  `s VERIFIED UNSAT` means `¬ DimacsSatisfiable`; **E4** the compiler and runtime of the exe behind E1 (not of the
  theorems); **E6** SHA-256.
- **E5** the kernel, Mathlib `f897ebcf…`, and that the definitions mean what the paper says: `Point`,
  `GeneralPosition`, `HasConvexNGon` (`geo/ErdosSzekeres/Definitions.lean`), `orient`
  (`geo/ErdosSzekeres/Orientation.lean`), `rotAbout` and `Invariant` (Capstone2). These are now the vendored copies;
  audit checks 1–3 tie them byte for byte to the repository at commit `536800bf` and to LEANEXT, and pin the
  `EncB` definitions and the build configuration.
- `sixfold_es8` instead assumes `CubesUnsat64`, a Lean statement about `cubeCnf (encB 6 8 11) c`; its tie to the
  certificates is the same E1–E3 through `cubesUnsat64_of_texts_get`.

So the sixfold bound (every 6-fold symmetric set of ≥ 61 points in general position has a convex octagon) is now a
Lean theorem whose only hypothesis is equivalent to `CubesUnsat64` (`texts_iff_cubesUnsat64`), i.e. what the 64
cake_lpr verdicts certify given E1–E4, with E5 and E6 as the remaining trust beyond that.

**P1 was updated on 2026-11-07** (`WRITEUP/P1/README.md`, "Revision for the end-to-end Lean check (ENCBLEAN M4–M8),
2026-11-07"). The notes written before that revision, kept for the record:
its Rigor text (about line 131) still calls the soundness of the encodings a written proof with gaps (G1)–(G4);
line 292 says ENCBLEAN is "standard library only, without Mathlib"; line 1057 lists closing (G1)/(G2) as future work.
For encoder B with m = 6 the revision should cite `EncB.Geo.sixfold_es8_of_texts` (and `sixfold_es8_order6_of_texts`
for cor:es8), mention the Mathlib-based package `geo/` (Mathlib `f897ebcf`), and narrow the encoder-B (m = 6) gaps
to E1–E6.

## M9: hash binding, DIMACS round trip and re-solve script (2026-11-06, 17:50–20:15 KST; not committed)

**What M9 had to do** (`DESIGN.md` §4, M9 row): bind the base and the 64 cubes of `cubes64` to the recorded hashes
by printing them from `encB` (trust item E1), write the trust table and P1's rigor text, and ship a re-solve script for
the provenance of the verdicts (E2, risk R7). As built it also proves a DIMACS round trip for the printer, which
narrows E3 and E4. The comparison of the row's "done when" with what was built is in `DESIGN.md` below the
milestone table.

| step | what was built or run | result | logs |
|---|---|---|---|
| A1 | mode `twin-cube64 M K T I` (Emit.lean); `scripts/hash_binding.sh` | 68/68 MATCH, exit 0, 908 s (exe `a0dff6f2…`); self-test with one hex digit changed in a scratch copy of a record: n10100 FAIL, 67/68, exit 1 | `m9_hash_binding.log`, `m9_hash_binding_selftest.log`; regression against the M2 exe `e9454996…` on every mode and 14 instances: 154 same, 0 unexpected (`m9_regress_modes.log`) |
| A2 | `EncB/Render.lean`: the twin's own decimal printer, the reference parser `parseDimacs`, the round trip; every twin mode prints through it | proved (statements below); exe `3d43fa8b…` byte-identical to the A1 exe on 321/321 runs over all modes, 17 instances and edge values; 68/68 again (897 s) | `m9_a2_regress_modes.log`, `m9_a2_hash_binding.log`, `m9_a2_cake_parse.log`; build, audit and axioms in `m9_build.log`, `m9_audit.log`, `m9_axioms.log` |
| A2 check | independent verifier: rebuild, axioms of all 229 constants of `EncB.Render`, 43 hand-written parser cases, 90 random round trips, the code path of each mode, 4 hashes | pass; defects in the log (`m9_a2_verify_rt.log:270`): stale doc passages, and the script's `sources:` line missed Render.lean; also reported by the verifier, not in the log: no theorem in the index form, E3 still trusted (disclosed) | `m9_a2_verify_rt.log` |
| A2 fixes | the 5 fixable findings: docs; `hash_binding.sh` hashes the exe's import closure; `cubesUnsat64_of_texts_get`, `encB_unsat_of_texts_get` | 68/68, 0 FAIL, exit 0, 878 s (script `29d89510…`, exe `3d43fa8b…`) | `m9_a2fix_hash_binding.log`; sections in `m9_build.log`, `m9_audit.log`, `m9_axioms.log` |
| A3 | `scripts/resolve.sh` (re-solve), `scripts/build_cake_lpr.sh` (build recipe, not run) | smoke test on c00100 (I = 27) and n10000 (I = 47): 2/2 ACCEPTED, exit 0, 37.4 s | `m9_resolve_smoke.log` |
| A3 review | independent review with stub tools (no solver run) | 10 defects (D1–D10, listed with their fixes in `m9_resolve_fix.log`; the review log itself records only the fake-tool run in which the summary printed PASS for an unpinned cake_lpr's row; `m9_resolve_fix.log:5` wrongly says D1–D10 are numbered in the review log, see `m9_review_fix.log`) | `m9_review_resolve.log` |
| A3 fixes | all 10 fixed (`resolve.sh` `22e07b3b…`, 611 lines; `build_cake_lpr.sh` `488502ba…`, 87 lines) | 39/39 stub runs with the expected exit code; real smoke test again into a new directory: 2/2 ACCEPTED, exit 0, 36.8 s, same CNF and proof hashes; rerun on it: both skipped, rows re-checked, PASS | `m9_resolve_fix.log` |
| D | this write-up (README, DESIGN, P1's trust and gap text); `lake build`, `scripts/audit.sh` and `#print axioms` on 14 theorems, among them the 7 that P1 cites; P1 rebuilt | build exit 0 (nothing to rebuild, exe `3d43fa8b…`), AUDIT PASS, all 14 within [propext, Classical.choice, Quot.sound]; `p1.pdf` three passes exit 0, 35 pages, 0 errors, 0 undefined references | `m9_d_recheck.log`; `WRITEUP/P1/README.md`, "Revision for the Lean encoder-B package" |
| R | two independent reviews: Lean soundness (rebuild, axioms of all constants of Render and Emit, proof terms, three mutants in a scratch copy) and claims (every name, line, number and sentence of the docs and P1) | Lean: no blocking finding, 6 minor; claims: 3 medium, 10 lower | `m9_review_lean_soundness.log`; the claims review reported to the workflow |
| F | the review fixes (section "M9 review fixes" below) | all 19 findings fixed (none declined); new module `EncB/Compose.lean`; `lake build` exit 0, exe unchanged `3d43fa8b…`; AUDIT PASS with the time gate; hash binding 68/68, exit 0, 906 s; `p1.pdf` rebuilt (36 pages, 0 errors, 0 undefined references) | `m9_review_fix.log`, `m9_review_fix_hash_binding.log` |

### What is proved (M9; Std-only, axioms within [propext, Classical.choice, Quot.sound], `logs/m9_axioms.log`)

| statement | file:line | axioms |
|---|---|---|
| `cnfText_encode : cnfText (encode m K t) cube = renderCube (numVars m K t) (encB m K t) (bodyR (encB m K t)) cube` (by `rfl`; `cnfText e cube` is the string the exe writes) | Render.lean:156 | propext, Quot.sound |
| `renderCube_eq : renderCube nv F (bodyR F) cube = render nv (cubeCnf F cube)` | Render.lean:164 | propext, Quot.sound |
| **`parseDimacs_render : (∀ cl ∈ F, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nv) → parseDimacs (render nv F) = some (nv, F)`** | Render.lean:585 | propext, Quot.sound |
| `parseDimacs_cube64_get i h : parseDimacs (cnfText (encode 6 8 11) (cubes64.get ⟨i, h⟩)) = some (numVars 6 8 11, cubeCnf (encB 6 8 11) (cubes64.get ⟨i, h⟩))` | Render.lean:800 | propext, choice, Quot.sound |
| `parseDimacs_base6811 : parseDimacs (renderCube (numVars 6 8 11) (encB 6 8 11) (bodyR (encB 6 8 11)) []) = some (numVars 6 8 11, encB 6 8 11)` | Render.lean:806 | propext, choice, Quot.sound |
| **`cubesUnsat64_of_texts_get`**: if for every index `i < 64` the text `cnfText (encode 6 8 11) (cubes64.get ⟨i, _⟩)` parses (by `parseDimacs`) to some `(nv, G)` with `¬ DimacsSatisfiable G`, then `CubesUnsat64`; `encB_unsat_of_texts_get`: then `¬ DimacsSatisfiable (encB 6 8 11)` | Render.lean:833, :842 | propext, choice, Quot.sound |
| `cnfText_bytes : (cnfText e cube).toUTF8.data.toList = (cnfText e cube).data.map (·.val.toUInt8)` (byte i is character i's code mod 256; that every character is ASCII is `render_ascii`, :683, and, stated on `cnfText`, `cnfText_ascii` below) | Render.lean:711 | propext, choice, Quot.sound |
| `pushNat_eq_append_toString : pushNat s n = s ++ toString n` (the printer agrees with core's `toString` on `Nat`) | Render.lean:119 | propext, Quot.sound |
| `cnfText_ascii e cube : ∀ c ∈ (cnfText e cube).data, c.toNat < 128` (review fix) | Compose.lean:45 | propext, Quot.sound |
| `parseDimacsBytes_cnfText e cube : parseDimacsBytes (cnfText e cube).toUTF8.data.toList = parseDimacs (cnfText e cube)`, where `parseDimacsBytes bs := parseDimacsChars (bs.map fun b => Char.ofNat b.toNat)` (review fix) | Compose.lean:50 | propext, choice, Quot.sound |
| `parseDimacsBytes_cube64_get i h : parseDimacsBytes (cnfText (encode 6 8 11) (cubes64.get ⟨i, h⟩)).toUTF8.data.toList = some (numVars 6 8 11, cubeCnf (encB 6 8 11) (cubes64.get ⟨i, h⟩))`: the round trip on the bytes `putStr` writes (review fix) | Compose.lean:61 | propext, choice, Quot.sound |
| **`no_model_6811_of_texts`**: if for every index `i < 64` the text `cnfText (encode 6 8 11) (cubes64.get ⟨i, _⟩)` parses (by `parseDimacs`) to some `(nv, G)` with `¬ DimacsSatisfiable G`, then `Model 6 8 11 → False` (`encB_satisfiable_6811` with `encB_unsat_of_texts_get`); `no_model_6811_of_bytes`: the same with the hypothesis on the bytes, read by `parseDimacsBytes` (review fix) | Compose.lean:72, :80 | propext, choice, Quot.sound |

- **No evaluation of (6,8,11).** The (6,8,11) theorems are term-mode applications of the general ones, with `encB_wf`
  for the clauses and `numVars_ge_45` (the 45 Y codes are allocated first) for the cube literals. The only `decide`s
  are on numerals (the 45 Y codes at t = 11 and the six cube variables). Audit check 4 lists these declarations and
  finds no risky token; Render.lean elaborates in 1.7–1.8 s.
- **Fourteen kernel-checked examples** (Render.lean:325-345) fix the language of `parseDimacs`: one accepted text and
  13 rejected ones (wrong count, a 0 inside a clause, a variable above nv, leading zeros, `-0`, double or leading
  space, no final newline, a blank line, a bare `0`, a comment line, `+1`).
- **The composition with M3 is stated (review fix).** `no_model_6811_of_texts` (Compose.lean) is
  `encB_satisfiable_6811` (M3) composed with `encB_unsat_of_texts_get`: if the 64 texts parse to unsatisfiable lists,
  no `Model 6 8 11` exists; `no_model_6811_of_bytes` puts the hypothesis on the bytes. What is still missing for an
  end-to-end theorem (a `Model` from a configuration, and `Sixfold66`) is M4–M8.
- **Characters and bytes.** `parseDimacs_cube64_get` is about the characters of the Lean string; `cnfText_bytes` says
  that its UTF-8 bytes are those characters' codes mapped by `·.val.toUInt8`. Since the review fixes the round trip is
  also stated on the bytes (`parseDimacsBytes_cube64_get`, via `cnfText_ascii`). That the compiled exe writes exactly
  these bytes is trust item E4.

### Hash binding (trust item E1)

- **How.** For each item the exe's stdout goes straight into sha256sum; no CNF file is written. The base is
  `twin-base 6 8 11`; cube I (0 ≤ I < 64) is `twin-cube64 6 8 11 I`, the string `cnfText (encode 6 8 11)
  (cubes64.get ⟨I, h⟩)` of `parseDimacs_cube64_get`. Every emitted hash is compared, on its own, with each record of
  its name, all parsed from the record files at run time:
  - base: `C6UPPER/SHA256SUMS.txt` and `C6UPPER/logs/encb_gen.log`;
  - c-cubes: `C6UPPER/SHA256SUMS.txt` and the encoder-B row of `C6UPPER/replay-2026-11-06/results.tsv`, which must be
    ACCEPTED with the cake line exactly `s VERIFIED UNSAT`;
  - n-cubes: `C6UPPER/noty12-2026-11-06/cubes.sha256` and the row of `C6UPPER/noty12-2026-11-06/results.tsv`, under
    the same rule, and its units column must equal the exe's units.
- **Further checks in the same run.** 64 distinct names, 32 c and 32 n; each name agrees with the signs of its units;
  the six variables equal the Y entries of `C6UPPER/encb/B_m6K8t11.meta.json` (1 2 3 10 11 18); every cube text ends
  with its 6 unit lines and has the header `p cnf 78059 2387089`; every record row is used exactly once.
- **Build provenance (review fix, finding L1).** Unless the exe is overridden, the script first requires
  `lake build --no-build` to report every target up to date (otherwise it stops before any emission: tested with one
  comment line added to a source, exit 1, `logs/m9_review_fix.log`), so the exe was built from the sources whose hashes
  it logs. It copies the exe into `$TMPDIR`, runs only the copy, and compares the hashes of the copy and the original
  with the start at the end. It requires `twin-cube64 6 8 11 64` to exit 2 with "cubes64 has 64 cubes" and nothing
  on stdout, which ties the compiled list's length to `length_cubes64` and to the loop over I = 0..63.
- **What exactly is bound.** For each index I, the hash of the text printed for `cubes64[I]` is compared with the
  records of the name that the exe reports for that cube on stderr (`cubeName`, derived from the cube's signs and
  checked against them). The index–name order (I = 63 − v) is not checked by this script; only `scripts/resolve.sh`
  ties index and name. This is enough for the theorems, which quantify over membership in `cubes64`
  (`cubesUnsat64_of_texts_get` covers every index), and a wrong text for a name fails (mutant B of the Lean review).
- **Numbers** (run after the A2 fixes, `logs/m9_a2fix_hash_binding.log`): base `479e31a9…`, 58,618,857 bytes, header
  `p cnf 78059 2387083`, 14.2 s; the 64 cubes 7.5–14.6 s each (832 s in all) at about 510 MB max RSS; whole run 878 s.
  The three runs (A1 exe `a0dff6f2…`, A2 exe `3d43fa8b…` twice) give the same 68 hashes. A fourth run after the review fixes (`logs/m9_review_fix_hash_binding.log`; script `3c527600…`, the same exe
  `3d43fa8b…`, run as a copy): `lake build --no-build` up to date, the range check passed, 68/68 MATCH, exit 0, 906 s
  (base 13.4 s; cubes 8.0–14.6 s each, 855 s in all, at most 510 MB max RSS); its 68 hashes equal those of
  `m9_a2fix_hash_binding.log`, item by item.
- **The 3 other instances** (6,8,9), (7,8,9), (7,8,10) have no row in `ref/hashes.tsv` (the corpus stops at t = 8),
  so they are bound against the two records each that `check_recorded.sh` uses; the log says `ref/hashes.tsv=no-row`.
  The (7,8,9) record is gen_b2.py output, not independent (see M1).
- **What this shows.** Compiled code printed, from the Lean terms `encB 6 8 11` and `cubes64`, the base file whose hash
  is on record and the 64 cube files cake_lpr certified. It is a computation, not a proof: it trusts the Lean compiler and runtime (E4), SHA-256 and the record
  files (E6, E1).

### DIMACS round trip (trust items E3, E4)

The details, and what stays trusted, are in "Trust" below. In short: the exe's twin modes print with Render's own
`pushNat`/`pushInt` (core's `toString` on negative `Int` goes through the bodiless `opaque`
`String.Internal.append` and cannot be reasoned about), and every printed character, header and count included, is
inside a proved term. Evidence for the part that stays trusted (`logs/m9_a2_cake_parse.log`, cake_lpr `c14ff498…` in
its one-argument parse-and-print mode): its printout of what it parsed is byte-identical to 21 small and medium twin
texts and to the (6,8,11) base and cubes 0 (c11111) and 63 (n00000), which have the recorded hashes (about 4.2 GB
RSS); of the 13 texts that `parseDimacs` rejects, cake_lpr rejects 5 and reads 8 the standard way (leading zeros in a
literal or in the header, two spaces, a leading space, no final newline, a bare `0` line, a comment line, `+1`), so on
these examples `parseDimacs` accepts the smaller language.

### Re-solve script (E2 provenance, risk R7)

- **Usage.** `scripts/resolve.sh CUBES OUTDIR`, with CUBES `all` or a comma-separated list of indices (0..63) and
  names; index and name are tied by I = 63 − v, v the name read as six bits with c = 1.
- **Per cube.** Emit with `twin-cube64 6 8 11 I` (index, name, units and Y map checked); compare the CNF hash with both
  records before solving (otherwise CNF-MISMATCH, nothing solved); `cadical -q --lrat --binary=false` (exit 20
  required); `cake_lpr --CML_HEAP_SIZE=8000 --CML_STACK_SIZE=4000`. ACCEPTED only with exactly one `s ` line, equal to
  `s VERIFIED UNSAT`, exit 0, and the CNF and proof hashed again after cake_lpr unchanged. lrat-check is never used.
- **Tools.** CaDiCaL 2.1.3 `4acf5860…` and cake_lpr `c14ff498…`, the binaries of the replay and of the noty12 run,
  pinned from `TOOLS_AND_PROOFS.sha256` of both records. Each tool, and the exe, is copied to
  `OUTDIR/tools/<sha256>/` and only the copy runs; its hash is checked before each cube and each run.
- **Safeguards.** Proofs are never deleted or compressed; `results.tsv` is append-only (23 columns); a killed or failed
  run gets a retryable verdict (`*-KILLED`, `*-ERROR`, `FILE-CHANGED`) and `RS_RETRY=1` starts a new attempt in new
  files; the final SUMMARY re-checks every requested cube's latest row and files and counts only rows of the pinned
  cake_lpr; it waits while Tctl ≥ 84 °C and needs 400 GiB + 6 GiB free.
- **Smoke test** (`logs/m9_resolve_fix.log`, part B; the first run, before the review fixes, is
  `logs/m9_resolve_smoke.log` with the same hashes):

  | cube | index | CNF sha256 (= both records) | CaDiCaL | proof (= recorded proof) | cake_lpr | verdict |
  |---|---|---|---|---|---|---|
  | c00100 | 27 | `67bd7187…09b2` | rc 20, 0.79 s, 243 MB | `94913b2e…`, 39,771,081 B, yes | `s VERIFIED UNSAT`, rc 0, 3.88 s, 6.8 GB | ACCEPTED |
  | n10000 | 47 | `b5cc9acd…307f` | rc 20, 0.81 s, 243 MB | `dd7b24ad…`, 39,771,102 B, yes | `s VERIFIED UNSAT`, rc 0, 3.93 s, 6.8 GB | ACCEPTED |

- **Not run.** `resolve.sh all`: from the records, about 20.1 h of CaDiCaL (the 24 phase-order cubes take
  2,320–3,921 s each, the other 40 about 1 s) plus about 1.4 h of cake_lpr, one cube at a time, and about 110 GB of
  raw proofs plus 3.75 GB of CNF. The peak memory of CaDiCaL on a phase-order cube is not on record; under the default
  4 GB cap such a run may be killed (verdict `CADICAL-KILLED`, retryable with a larger `RS_CAP_CADICAL`).
  `scripts/build_cake_lpr.sh` was not run either (only its argument checks and a dry `make -n`); its fallback that
  fetches the commit by id is untested. Its three source pins (Makefile `5e001c7e…`, basis_ffi.c `bd498883…`,
  cake_lpr.S `d20ceae0…`) are M9's own reading of the local clone (`git show 033aad53:<file> | sha256sum`,
  recomputed with the same values in `logs/m9_review_fix.log`); M9 is the first place they are recorded in full (the
  replay README has only the prefix `d20ceae0`), and the script's header says so. That a build of commit `033aad53` reproduces `c14ff498…` byte for byte is the
  replay's record (`C6UPPER/replay-2026-11-06/README.md`), not an M9 result.

### Files left on disk, and minor points

- `/path/to/data/encblean-m9/` (kept; nothing under it may be deleted by a step, since it holds CNFs and
  proofs): `resolve-smoke-fix/` (200 MB, the fixed script's smoke test), `resolve-smoke/` (188 MB, the first smoke
  test; its 21-column `results.tsv` is refused by the fixed script), `resolve-negtest/` (56 MB, the CNF-MISMATCH
  test), `review-unpinned/` (56 MB, **fake**: stub tools, an empty proof and a fake ACCEPTED row, marked by
  `FAKE-TOOLS-NOT-A-CHECK.txt`). The operator may remove them.
- `resolve.sh`'s header line `sources:` hashes only Emit.lean, Cover.lean and Coded.lean, as `hash_binding.sh` did
  before its fix; the exe that runs is pinned by its own hash snapshot, so this is provenance text only. Not changed.
- The usage text of the exe gained a line for `twin-cube64`, so the stderr of its error paths differs from the M2 exe;
  stdout, files and exit codes of the old modes are unchanged (`m9_regress_modes.log`).
- `scripts/audit.sh`: its keyword regex makes a `#guard_msgs` line join the previous declaration's block, which only
  makes check 4 stricter (`m9_audit.log`).

## M9 review fixes (2026-11-06, about 20:55–21:06 KST; not committed)

Two independent reviews of the uncommitted M9 work: a Lean-soundness review (no blocking finding, 6 minor;
`logs/m9_review_lean_soundness.log`) and a claims review of the docs and P1 (3 medium, 9 low, 1 nit; reported to the
workflow, not logged by the reviewer). Every finding was applied; nothing was declined. Record:
`logs/m9_review_fix.log` (commands, exit codes, hashes) and `logs/m9_review_fix_hash_binding.log`.

| finding | outcome |
|---|---|
| L1 `hash_binding.sh` never checked that the exe was built from the hashed sources | **fixed:** `lake build --no-build` must report the build up to date, else the run stops before any emission (tested: one comment line added to `EncB/Compose.lean`, `lake build --no-build` exit 3, script exit 1, file restored byte for byte); only a copy of the exe in `$TMPDIR` runs, and the hashes of copy and original are compared with the start at the end; `twin-cube64 6 8 11 64` must exit 2 with "cubes64 has 64 cubes" and no stdout. Full run: 68/68 MATCH, 0 FAIL, exit 0, 906 s, the range check passed and the exe copy `3d43fa8b…` was unchanged at the end; the 68 hashes equal those of the earlier runs (`m9_review_fix_hash_binding.log`) |
| L2 `audit.sh` check 4 missed `trivial`, `Eq.refl`, `simpa`, `grind`; its comment named only Cover.lean | **fixed:** `simpa`, `grind`, `trivial`, `Eq.refl`, `eq_self`, `Nat.decEq`, `decide_eq_true` added; new check 5, a time gate (`lake build --no-build`, then `timeout 60 lake env lean` on every file with a (6,8,11) declaration: Compose 0.6 s, Cover 0.3 s, Render 1.8 s, Satisfiable 0.4 s); comment updated. Negative tests: 8 declarations using the new tokens in a scratch copy (never compiled) are each flagged, AUDIT FAIL, exit 1; with the limit lowered to 1 s, Render.lean times out, AUDIT FAIL. The package: AUDIT PASS, exit 0 |
| L3 the round trip is on characters, not bytes; README annotated `cnfText_bytes` "(the text is ASCII)" | **fixed:** `EncB/Compose.lean`: `parseDimacsBytes`, `cnfText_ascii`, `parseDimacsBytes_cnfText`, `parseDimacsBytes_cube64_get` (the reviewer's text, which compiled in its scratch file); README row and DESIGN E3 reworded |
| L4 no Lean theorem joins `encB_satisfiable_6811` with `encB_unsat_of_texts_get` | **fixed:** `no_model_6811_of_texts` (and `no_model_6811_of_bytes`) in the new module `EncB/Compose.lean`, which imports Satisfiable and Render and is imported by `EncB.lean` (not by the exe, whose hash stays `3d43fa8b…`); 5 `#guard_msgs` axiom guards; P1 §8 now cites it |
| L5 two cake_lpr source pins appear in no record | **fixed (second option):** the header of `build_cake_lpr.sh` says that M9 is the first place the three hashes are recorded in full (the replay README has only the prefix `d20ceae0`) and that they are M9's own reading of the local clone; recomputed read-only with `git show`, same values (`m9_review_fix.log`). No new record file: one written by M9 would be no more independent than the script |
| L6 what the binding binds (name from stderr, not the index order) was not stated | **fixed:** a sentence in the script header and in "Hash binding" above |
| C1, C2 P1 §1 and §3 dropped the even-m restriction | **fixed** as proposed; "the assembly into one theorem" reads "… with `Sixfold66`", since `no_model_6811_of_texts` now composes part of it |
| C3 the parser agreement was credited to cake_lpr's verification | **fixed** in P1 §8, the note (G2) in both copies, P1's README and DESIGN E3 |
| C4 "65 files cake_lpr certified" (the base was never checked by cake_lpr) | **fixed** in this README (top and "Hash binding"); P1's "65 of 65" left as it is (P1's Table 7 counts base formulas among the certified files), as the review allowed |
| C5 two README cells cite logs that do not contain the stated counts | **fixed** (rows A2 check and A3 review); `m9_resolve_fix.log:5` ("as numbered in m9_review_resolve.log") is wrong but was not edited, since it is a record; the correction is here and in `m9_review_fix.log` |
| C6 "even m" without m ≥ 2; "equal output" on the grid; "every Model satisfies" | **fixed** (a)–(f) as proposed (222 of 225 grid instances equal bytes, 3 refused where gen_b2.py raises: `logs/compare_tiny_twin.log`) |
| C7 Table 7 row omitted the assembly; "through a DIMACS parser" was vague | **fixed** as proposed (with "with `Sixfold66`") |
| C8 "the text that the printer writes" in a Lean-checked item | **fixed** in P1 §8 and the note (G2), both copies |
| C9 the EncB items are also about DIMACS lists in general | **fixed**, including the optional rewording after the proof of Lemma k8s:lem:cube |
| C10 revision times later than the files' write times; the milestone parenthesis | **fixed** (20:20 → 20:10 KST in the note's and the copy's headers; 20:25 → 20:12 KST in P1's README; "M2 and M3, committed, and M9, not committed"); this round adds its own dated revision comments |
| C11 "these two under the 4 GB cap" | **fixed** ("How to build and run") |
| C12 stale `p1.tex:299` and the pre-M9 cost estimate in DESIGN | **fixed:** `p1.tex:310-312` at both places; the cost from the records (CaDiCaL 36,873.6 s + 35,410.6 s = 72,284.2 s, summed from the two `results.tsv` in `m9_review_fix.log`; the review's "35,411 s" is the noty12 README's rounding) |
| C13 the list of the 8 texts cake_lpr reads; a line break inside `EncB.Model` in `p1.pdf` | **fixed** (the list now matches `m9_a2_cake_parse.log:54-56`; `every~\mbox{\lean{EncB.Model}}`) |

**Checks after the fixes.** All in `logs/m9_review_fix.log` unless named otherwise.
- `lake build` (4 GB cap): exit 0; the first build after adding Compose built `EncB.Compose` (0.54 s) and `EncB`; the
  exe stayed `3d43fa8b…` (mtime 18:58), since Compose is not in its import closure. A final `lake build`: exit 0,
  exe unchanged.
- `scripts/audit.sh` (script `83ffabe7…`): AUDIT PASS, exit 0; time gate Compose 0.5 s, Cover 0.3 s, Render 1.8 s,
  Satisfiable 0.4 s. Negative tests as in row L2.
- Axioms of the 7 declarations of Compose.lean (`#print axioms` in a scratch file importing `EncB`): `parseDimacsBytes`
  none; `ofNat_toUInt8_ascii` [propext]; `cnfText_ascii` [propext, Quot.sound]; `parseDimacsBytes_cnfText`,
  `parseDimacsBytes_cube64_get`, `no_model_6811_of_texts`, `no_model_6811_of_bytes` [propext, Classical.choice,
  Quot.sound]. Five are also guarded at build time. Compose.lean elaborates in about 0.5 s; its (6,8,11) theorems
  are term-mode applications (`(parseDimacsBytes_cnfText _ _).trans (parseDimacs_cube64_get i h)`,
  `fun M => encB_unsat_of_texts_get h (encB_satisfiable_6811 M)`), so nothing evaluates the instance.
- `scripts/hash_binding.sh`: 68/68 MATCH, exit 0, 906 s (`logs/m9_review_fix_hash_binding.log`); the stale-build
  guard: exit 1 before any emission (row L1).
- `scripts/build_cake_lpr.sh` (comment change only): `bash -n` exit 0; no argument, exit 2; an existing directory,
  exit 2. Still not run.
- P1: `p1.pdf` three passes, each exit 0, 36 pages (35 before; the longer §1, §3 and §8), 0 errors, 0 undefined
  references or citations, 0 LaTeX warnings, the same 1 overfull and 5 underfull boxes; the same theorem and table
  numbers. Not changed: Table 7 is printed on the last page (it was already there after the 20:10 revision; HEAD
  has it on page 28 of 33). The note's wrapper compiles cleanly in a scratch directory (13 pages, no box warnings).
  `diff` of the two note copies: the 35-line header and edits 1–9 only.
- Not run: no SAT solver, no proof checker, nothing under `/path/to/data` was written; no unit was touched;
  no git commit.

## M3: combinatorial soundness (`encB_satisfiable`), 2026-11-06

**How it was made.** The plan is `docs/M3PLAN.md`, a judge's merge of two competing plans. Unit U0 copied the
frozen interface (`Model.lean`, `ModelLemmas.lean`, `SortLemmas.lean`, `SoundOlit.lean`; hashes in the plan) and
built it. Six units then worked in parallel in this directory:
- U1–U5 each proved one frozen statement in a file of its own;
- U6 wrote the early-warning test.

No unit imported another unit's file, edited an existing file or ran `lake build`; the dependencies between units
were explicit hypotheses. An independent verifier re-checked each unit and passed all six. It checked:
- the file hash;
- a capped compile;
- the `#guard_msgs` axiom guard, plus a negative control with a wrong guard, which must fail;
- the statement against plan §2.2;
- the audit;
- name collisions;
- that no other file was touched.

Integration (17:18–17:40 KST) copied the judge's `Satisfiable.lean` unchanged (sha256 `5c908151…`), added six imports
to `EncB.lean`, and ran the build, the audit, the axiom queries, the mutants and the early-warning test again.

### The theorem (`EncB/Satisfiable.lean:37`, `:43`)

```lean
theorem encB_satisfiable {m K t : Nat} (heven : m % 2 = 0) (hm : 2 ≤ m) (M : Model m K t) :
    DimacsSatisfiable (encB m K t) :=
  dimacsSatisfiable_of_holds M.τ (genCoded_sound heven hm M)

theorem encB_satisfiable_6811 (M : Model 6 8 11) : DimacsSatisfiable (encB 6 8 11) :=
  encB_satisfiable (Nat.mul_mod_right 2 3) (Nat.le_add_left 2 4) M
```

- **Hypotheses: only `heven`, `hm` and the `Model`.**
  - `Model m K t` is `EncB/Model.lean:81-102`: the 13 fields of `DESIGN.md` §2.2, with `Valid` replaced by Coded's
    `PtOk` (same body).
  - All five unit statements are proved. So the plan's fallback, which would have kept a stalled unit's statement
    as an explicit hypothesis, was not used.
  - The intermediate specs are discharged inside `genCoded_sound`: `OrbListSpec` by `orbListSpec m t`, and
    `PatternSpec` by `patternSpec_of wordSpec M`.
- **The assignment** is `M.τ` (`Model.lean`, `tauOf`):
  - `Y(i,j) ↦ psiLt i j`;
  - `orb [a,b,d] ↦ chi a b d`;
  - `F(i,l,a,b) ↦ ChainFrom m t chi i l a b`, a chain of length l from pivot (i,0) starting with a, b;
  - everything else ↦ false.

  `dimacsSatisfiable_of_holds` (M2) carries it to `encB` through the numbering.
- **Axioms:** [propext, Classical.choice, Quot.sound] for both theorems. This is checked at build time by
  `#guard_msgs in #print axioms` (Satisfiable.lean:46-50) and by the queries in `logs/axioms.log`.
- **No kernel evaluation of (6,8,11).**
  - The side conditions of `encB_satisfiable_6811` are proof terms (`2 * 3 % 2 = 0` and `2 ≤ 4 + 2`), not `decide`.
  - Audit check 4 lists this declaration and finds no risky token.
  - `Satisfiable.lean` builds in 0.35 s.
- **Scope.**
  - Even m only (`heven`; odd m, the sevenfold case, stays out, `DESIGN.md` R9).
  - The theorem is about the combinatorial `Model`. That a geometric counterexample yields a `Model` is M4–M6.
- **Read with M2.** `encB_unsat_of_cubes64` (Cover.lean:114) together with `encB_satisfiable_6811` gives:
  `CubesUnsat64` implies that no `Model 6 8 11` exists. That one-line composition was not stated in Lean in M3; since
  the M9 review fixes it is stated with the hypothesis on the 64 printed texts, `no_model_6811_of_texts`
  (Compose.lean).

### What is proved

Every row has axioms [propext, Classical.choice, Quot.sound].

| statement | file:line | unit |
|---|---|---|
| `genCoded_sound heven hm M : ∀ cl ∈ genCoded m K t, ∃ x ∈ cl, CodeLitHolds M.τc x` | Satisfiable.lean:26 | Integration (judge's text) |
| `transCl_sound M : ∀ cl ∈ transCl t, ∃ x ∈ cl, CodeLitHolds M.τc x` | SoundOrbit.lean:174 | U1 |
| `nestLits_sound M (hm : 2 ≤ m) : ∀ l ∈ nestLits m t, CodeLitHolds M.τc l` | SoundOrbit.lean:212 | U1 |
| `orbListSpec m t : OrbListSpec m t` (each `c ∈ orbList m t` is `[a, b, d]`, three distinct valid labels) | SoundOrbit.lean:161 | U1 |
| `chainCl_sound M isF : ∀ i ∈ rng 0 t, ∀ cl ∈ chainCl m K t isF i, ∃ x ∈ cl, CodeLitHolds M.τc x` (every filter `isF`) | SoundChain.lean:202 | U2 |
| `angCl_sound M heven (hOL : OrbListSpec m t) (hP : PatternSpec M) : ∀ c ∈ orbList m t, ∀ cl ∈ angClOf (angOutsC m t c).1, ∃ x ∈ cl, CodeLitHolds M.τc x` | SoundAng.lean:329 | U3 |
| `patternSpec_of (hW : WordSpec) M : PatternSpec M` (via `Rules.sortSix` :218 and the judge's glue `Rules.patternSpec_of_sort` :139) | SoundRules.lean:270 | U4 |
| `wordSpec : WordSpec` (a sorted word of six objects gives `AltCCW` or `BlockCCW`) | SoundWord.lean:222 | U5 |
| `olitSpec M : OlitSpec M` (an orbit literal holds iff `chi` of its three labels) | SoundOlit.lean:38 | U0 |

**The clause families of `genCoded` (Coded.lean:281-285).** Each family is covered once, and there is no other
clause. A filter, a key set, a `none` literal or a failing `olit` only drops clauses, so the proofs hold for any
outcome of them.

| family | clause shapes | theorem |
|---|---|---|
| ψ-order transitivity | `[-Y ij, -Y jk, Y ik]`, `[Y ij, Y jk, -Y ik]` | `transCl_sound` |
| angular, per orbit `c` | unit `[l]`, or `neg prem ++ [l]` per pattern; `l` from rule A (`±orbCode c`) or rule B (`olit a b cc`) | `angCl_sound` with `orbListSpec`, `patternSpec_of wordSpec` |
| nesting units | `[olit (i,0) (i,1) (j,k)]` | `nestLits_sound` |
| chains, per pivot | base `[F₂(a,b), -l]`, extension `[-F_lev(b,c), -lab, -lt, F_{lev+1}(a,b)]`, closing `[-F_lev(b,c), -lab, -lt]` | `chainCl_sound` |

**How the proofs go.**
- **U1, orbits and order.**
  - `Orbit.mem_dedupBy`: `dedupBy` keeps only input elements (a fold invariant).
  - `labels` is pairwise `ptLt`.
  - `Orbit.canon_eq`: `canon m tri = insSort ptLt (tri.map (rotBy m s))` for some `s`, and `rotBy` is injective on
    valid sectors. Together these give `orbListSpec`.
  - Transitivity clauses: `psiLt_trans`; the second clause uses totality, transitivity and irreflexivity.
  - Nesting: `olitSpec` with `M.nest`.
- **U2, chains.**
  - The base and extension clauses get explicit chain witnesses `q` (`Chain.chainFrom_two`,
    `Chain.chainFrom_cons`).
  - A closing clause would give a chain of length K − 1, which contradicts `M.noChain`.
- **U3, angular clauses.**
  - Existence (`Ang.exists_rkMono`): the pattern `s := insSort M.psiLt free`, with ranks `free.map s.idxOf`, follows ψ.
  - Premises (`Ang.rkMono_of_prem`): if every premise holds, the ranks follow ψ.
  - So a unit clause is that pattern's literal, and a conditional clause has a false premise or a true literal.
  - `eraseDups` is handled by a structural invariant on `eraseDupsBy.loop`.
  - `patternLit` and `angOuts` are never unfolded at a concrete list; the start file's `rfl` bridges are used instead.
- **U4, sorting (`Rules.sortSix`).** `insSort Obj.lt` puts the six objects in `objLt` order: transitivity and
  totality come from `Obj.lt_iff` and omega, then `insSort_pairwise`. The judge's glue turns `SortedSix` with
  `WordSpec` into rules A and B.
- **U5, cyclic words.** The proof reasons on positions in the sorted list (`ccwIn_getElem_iff`, omega), with no 6×6
  case split. Alternating words give `AltCCW`, including the wrap-around; a PPP run gives `BlockCCW`.

### Evidence

- **(a) Build** (`logs/m3_build.log`).
  - `lake build` under the 4 GB cap: rc 0, 2.85 s wall, 454 MB peak, no warning.
  - It rebuilt the six new modules (0.35–2.2 s each) and `EncB`. Both `#guard_msgs` in Satisfiable.lean held.
- **(b) Audit** (`logs/audit.log`). AUDIT PASS over 19 sources, including `Satisfiable.lean` and `EarlyWarning.lean`.
  New negative tests in scratch copies:
  - `encB_satisfiable_6811` written as `encB_satisfiable (by decide) (by decide) M` gives FAIL (KERNEL EVALUATION
    RISK);
  - an appended `sorry` gives FAIL.
- **(c) Axioms** (`logs/axioms.log`, regenerated by both queries).
  - 425 named declarations and 550 internal auxiliaries; none uses an axiom outside {propext, Classical.choice,
    Quot.sound}. No `sorryAx`, no `ofReduceBool`.
  - The two queries agree on all 425 names.
  - The 236 M2 lines are unchanged; the 189 new names come from the U0 and M3 modules (133 theorems written in the
    source).
  - Build-time guards: 26 (17 before M3).
- **(d) Mutants** (`logs/m3_mutants.log`). They ran in a scratch copy with its own `.lake`; ENCBLEAN was not touched.
  - **Deleting any one of the 13 `Model` fields breaks the build, 13 of 13.**
    - `chi`, `psiLt`: `Model.lean` itself fails.
    - `chi_cycle`, `chi_swap`: `ModelLemmas` (`chi_perm3`).
    - `chi_rot`: `SoundOlit`.
    - `psiLt_irrefl`: SoundOrbit, SoundRules.
    - `psiLt_trans`: SoundOrbit, SoundAng, SoundRules.
    - `psiLt_total`: SoundOrbit, SoundAng.
    - `psiLt_zero`: SoundAng.
    - `ruleA`, `ruleB`: SoundRules.
    - `nest`: SoundOrbit.
    - `noChain`: SoundChain.

    Where the failing file is a unit file, its axiom guard also reports `sorryAx`.
  - **Negating the nesting literal** in a scratch `Coded.lean` (`nestLits` only):
    - only `SoundOrbit` fails (`nestLits_sound`: type mismatch, and the guard sees `sorryAx`); the other four units
      build;
    - the early-warning run on that copy (355 s) prints `EW SUMMARY: FAIL` and exits with 1:
      - in all 30 base runs every `Model` law holds;
      - the unsatisfied clauses are exactly the nesting clauses, all of them (`nest_UNSAT` = `nest_clauses` =
        `genCoded_UNSAT`: 18 at t = 3, 60 at (6,8,5)).
  - Controls: the unmodified copy builds, and so does the copy with `Model.lean` restored after the 13 field
    mutants.
- **(e) Early-warning test** (`EncB/EarlyWarning.lean`, evidence only, interpreted by `lean --run`).
  - **U6's run** (`logs/m3_early_warning.log`, 356 s): `EW SUMMARY: PASS`.
    - 30 base runs: SIX60 sets A–D and their mirrors at (6,8,3), four at (6,8,5), non-monotone ψ, m = 4 squares, and
      plan A's ℤ[√3] polygons.
    - In every base run every `Model` law holds as a Bool over valid labels, and 0 of the `genCoded` clauses are
      unsatisfied (89,530 clauses at t = 5).
    - The `SortedSix`/`WordSpec` check finds 0 violations in 161,280 triples.
    - All 6 controls are detected.
  - **Integration's rerun** (`logs/m3_early_warning_integ.log`, 17:30 KST, 303 s): `EW SUMMARY: PASS`, exit 0, with
    the same input hashes.
    - The 162 result lines are byte-identical to U6's log once the `#` header and the per-run `(… ms)` timing lines
      are removed.
    - U6's log was kept; the rerun went to a new file.
- **(f) The units' own checks** (verifier reports, summarized):

  | unit | file | sha256 | lines (code) | verifier |
  |---|---|---|---|---|
  | U1 | SoundOrbit.lean | `ce93c201…` | 233 (176) | PASS |
  | U2 | SoundChain.lean | `d2d59081…` | 218 (181) | PASS |
  | U3 | SoundAng.lean | `6fa1ad05…` | 369 (293) | PASS |
  | U4 | SoundRules.lean | `8cb4637e…` | 276 (238) | PASS |
  | U5 | SoundWord.lean | `c1bdb417…` | 229 (180) | PASS |
  | U6 | EarlyWarning.lean | `38d3c253…` | 436 (298) | PASS |

  "Code" means not blank, not a comment and not a docstring. With the U0 files (616 lines, 467 code) and
  `Satisfiable.lean` (52, 23), M3 adds 1,993 lines of library Lean, 1,558 of them code (DESIGN estimated 1.0–1.3k).

**Minor points, none blocking.**
- `WordSpec` has a `Distinct3 a b d` hypothesis that `wordSpec` does not use, and `EncB.Word.lt3_of_perm` is unused.
- `EarlyWarning.lean` defines a root `main` (`lean --run` needs it), as `Emit.lean` does. No module imports both.
- Its `main` returns `IO UInt32`, not the plan's `IO Unit`, so that `ew_test.sh` gets an exit code.
- The module docstring of `SoundChain.lean` still calls the file a "starting point".

**Not done in M3.** No git commit. `logs/env.txt` was regenerated (see its header). M4–M9 are not started.

## M2: the functional twin and the numbering bridge

### What is proved (all Std-only; axioms in `logs/axioms.log`)

| statement | file:line | axioms |
|---|---|---|
| `numberMap_getD : v ∈ l → (numberMap l).getD v 0 = l.idxOf v + 1` | Dimacs.lean:147 | propext, choice, Quot.sound |
| `decode_numberMap : v ∈ l → decode l ((numberMap l).getD v 0) = v` | Dimacs.lean:162 | propext, choice, Quot.sound |
| `idxOf_cons_ne`, `getElem_idxOf` (Mathlib's, re-proved) | Dimacs.lean:38, 45 | propext / propext, choice, Quot.sound |
| `decodeCode_code : v.Valid m K t → decodeCode m K t (v.code m K t) = v` (layer < t, sector < m, pivot < t, level < FL; no hypothesis on K) | Coded.lean:127 | propext, Quot.sound |
| `mem_allCodes : cl ∈ genCoded m K t → x ∈ cl → x.natAbs ∈ allCodes m K t` | Coded.lean:365 | propext, Quot.sound |
| `dimacsSat_of_holds : (∀ cl ∈ genCoded m K t, ∃ x ∈ cl, CodeLitHolds (τ ∘ decodeCode m K t) x) → DimacsSat (encB m K t) (nuOf m K t τ)` | Coded.lean:381 | propext, choice, Quot.sound |
| `dimacsSatisfiable_of_holds` (the same, existential) | Coded.lean:404 | propext, choice, Quot.sound |
| `encB_wf : ∀ cl ∈ encB m K t, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ numVars m K t` | Coded.lean:410 | propext, choice, Quot.sound |
| `encB_eq`, `numVars_eq`, `allCodes_eq` (by `rfl`: `encB` is the renumbering of `genCoded`, `numVars` the length of `allCodes`) | Coded.lean:335-340 | none |
| `covers_signPatterns : (∀ v ∈ vs, v ≠ 0) → Covers (signPatterns vs)` | Cover.lean:58 | propext, choice, Quot.sound |
| `not_dimacsSatisfiable_of_cover` (H3 `Cover.lean:98`) | Cover.lean:82 | propext, Quot.sound |
| `length_cubes64 : cubes64.length = 64` | Cover.lean:105 | propext, Quot.sound |
| **`encB_unsat_of_cubes64 : (∀ c ∈ cubes64, ¬ DimacsSatisfiable (cubeCnf (encB 6 8 11) c)) → ¬ DimacsSatisfiable (encB 6 8 11)`** | Cover.lean:114 | propext, choice, Quot.sound |
| `cubeBody_eq : cubeBody (bodyL F) c = bodyL (cubeCnf F c)` (what the emitter printed for a cube in M2). **Removed in M9 A2** with `bodyL` and `cubeBody`; superseded by `renderCube_eq : renderCube nv F (bodyR F) c = render nv (cubeCnf F c)` (Render.lean:164, axioms propext, Quot.sound) | was Emit.lean:79 | propext, Quot.sound |

- **The definitions.** `genCoded`, `encB`, `numVars`, `allCodes` and `cubes64` use no axioms (`#print axioms`).
- **No kernel evaluation of (6,8,11).** `encB_unsat_of_cubes64` is
  `not_dimacsSatisfiable_of_cover (covers_signPatterns cubeVars64_ne_zero) h`. Its only `decide` is
  `cubeVars64_ne_zero` (six numerals ≠ 0), and Cover.lean builds in 0.27 s.
- **Model transfer needs no allocation lemma.** Every code of `genCoded` is in `allCodes` because `allCodes` is
  built from the codes of `genCoded` (`mem_allCodes`). That `allCodes` is exactly Python's `new()` order, so that
  the numbers agree, is checked only by bytes (D4 of `DESIGN.md`).

### How `encB` is built (Coded.lean)

- **Codes** (Coded.lean:55-65):
  - Y(i,j) ↦ 1 + i·t + j;
  - H(i) ↦ t² + 1 + i;
  - orb c ↦ oBase + triCode c;
  - F(piv,l,a,b) ↦ fBase + ((piv·FL + l)·N + ptCode a)·N + ptCode b, with N = t·m and FL = max (K−1) 3, as in
    `DESIGN.md` §3.1.
- **`genCoded`** (Coded.lean:281) = `transCl ++ angular ++ nesting ++ chains`, built only from `flatMap`,
  `filterMap`, `map` and `foldl`. It calls Gen's `canon`, `olit`, `angOuts`, `unitOf` and `triples` unchanged, with
  `orbVar := orbVarC` and `yv`, `hv` the closed-form codes:
  - the orbit list (first-seen order) is `orbList` (:187);
  - the chains per pivot are `okList` (:228), `extItems` (:242), `levelStep` (:268) and `chainCl` (:274). The key
    set of each level is an argument; it is only a filter.
- **`allCodes`** (:300): `prefixCodes` (Y, H, orbits), then the codes of `genCoded` in stream order, each kept once.
- **`encode`** (:320) computes `genCoded`, `allCodes` and `numberMap` once. `encB`, `numVars` and `allCodes` are
  its fields, so the emitter prints exactly `encB` and `numVars`.

**Deviations from `DESIGN.md` §3.1, and why:**

1. **`numberMap` is an `Array Nat` indexed by the code, not H's `Std.HashMap`.** The kernel cannot reduce a
   `HashMap`: its bucket index is a `USize`, and `USize.size` depends on an opaque platform constant. An array makes
   `decide +kernel` on `encB` possible. H's proofs carry over (`numberStep_foldl`, Dimacs.lean:101), because the
   array has `1 + (largest code)` entries.
2. **`orbVarC` returns a code only for three distinct valid labels**, not `some ∘ orbCode`. So `olit` fails
   exactly where Python raises `KeyError`, as Gen's `orbTab` lookup does, and every orbit literal of `genCoded`
   decodes to a valid triple.
3. **No `okpair` map.** In the extension step `(a, b) ∈ okpair` and `okpair[(a, b)]` are recomputed as
   `olit p a b = some lab` with `¬ is_false lab`. The literal in the clause is therefore `olit p a b` by
   definition, which M3 can use directly. This costs one extra `olit` per inner step (see the times below).
4. **`Var` has a fifth constructor, `other n`**, the image of codes outside every range; M3's τ maps it to `False`.
5. **The even kernel instance is (6,4,1), not (4,4,2).** `encB 4 4 2` in the kernel was OOM-killed at the 8 GB cap
   after 33 s. `allCodes 4 4 2` alone took 28 s and 5.5 GB: every step of its 903-entry seen-array is O(size) in
   the kernel. (6,4,1) took 7.5 s and 1.8 GB.
6. **`diagCoded`**, the refusal flags of the twin modes, does not recount failures of the extension `olit a b c`.
   Its three labels are pairwise distinct labels of Q, so `canon` of them is a key of `orb` and this `olit` cannot
   fail. This affects only the refusal, never `encB`. On the grid the twin refuses exactly the three rows where
   Python raises.
7. **The cube files render the list `cubeCnf F c` itself** (`cubeBody_eq` in M2; since M9 A2 `renderCube_eq`,
   Render.lean:164). For a non-empty F this is mkcubes' layout byte for byte. Only for an empty F would mkcubes add
   an extra newline.

### Evidence (exe `e9454996…`, built twice from clean with the same hash; load average about 30 on 32 cores)

**(a) Tiny grid, bytes: 225 of 225 agree, for `encB` and for `gen`.**
- `logs/compare_tiny_twin.log` (47.7 s): 222 byte-identical to gen_b2.py, and 3 refused where Python raises:
  (2,4,3) and (2,5,4) (`RuntimeError: conflict`) and (1,4,2) (`KeyError`).
- `logs/compare_tiny.log` (22.7 s): the same for `gen` with this exe (a regression check of M1).

**(b) `encB = gen` as Lean values: 228 of 228** (`logs/twin_check.log`, 110 s). `twin-check` compares
`encB m K t` with `(gen m K t).clauses.toList`, `numVars` with `nv`, and the refusal flags. It covers the 225 grid
rows (222 EQUAL, 3 BOTH-REFUSE) and (6,8,9), (7,8,9), (7,8,10). No printing is involved, so a bug in the text
renderer cannot hide a difference here.

**(c) Kernel** (`EncB/KernelCheckB.lean`, 19 s in the build). `decide +kernel` proves:
- `numVars 3 4 1 = 2 ∧ encB 3 4 1 = [[1], [2, -1]]`;
- the same for (3,4,2) (22 variables, 32 clauses) and (6,4,1) (20 variables, 48 clauses), against the gen_b2.py
  lists (for (6,4,1) a fresh gen_b2.py output whose SHA-256 equals the corpus row `dd42c2e8…`);
- the same for (4,5,1) (13 variables, 18 clauses), for `encB` and for `gen` (added by the review fixes; the only
  kernel instance with K > 4, see below);
- `codesDecode 3 4 2 (allCodes 3 4 2) = true`: every DIMACS variable decodes to a valid `Var` whose code it is.

**(d) Recorded instances, streamed into sha256sum: all MATCH** (`logs/check_recorded_small_twin.log`, the
hashes are read from the record files as in M1):

| instance | SHA-256 (encB = record) | encB wall / user / max RSS | gen (same exe) |
|---|---|---|---|
| (6,8,9) | `9f63854369a76998e13217e1f4208e365d0821b07f253decca2b9aed1ba1d350` | 6.29 s / 6.18 s / 211 MB | 2.65 s / 188 MB |
| (7,8,9) | `67cd613d024e36912e61aeae1bb582e1cd992659a6902dfa936ba1f1caa300aa` | 11.95 s / 11.85 s / 378 MB | 5.04 s / 348 MB |
| (7,8,10) | `b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2` | 14.29 s / 14.12 s / 550 MB | 7.72 s / 487 MB |

Every twin run also reports `"codesDecode": true`: all `numVars` DIMACS variables decode to valid variables.

**(e) (6,8,11): one emission from `encB`, 8 files, all MATCH** (`logs/check_recorded_big_twin.log`). The run
`twin-cubes64 6 8 11` took 15.26 s wall, 14.94 s user and 928 MB max RSS. That covers the generation plus writing
base and 7 cubes (8 × 58.6 MB) to the session scratchpad (`encblean/b6811`). The files were hashed and deleted.
- **Counts.** nv 78,059, ncl 2,387,083, `"codesDecode": true`.
- **Cube variables, checked by compiled code during the run, not by the kernel.** The exe's numbers of Y12 Y13 Y14
  Y23 Y24 Y34 are `[1, 2, 3, 10, 11, 18]`. That equals `cubeVars64` and the Y entries of gen_b2.py's map
  `C6UPPER/encb/B_m6K8t11.meta.json` (`68b43494…`). Decoding 1, 2, 3, 10, 11, 18 gives
  `Var.y 1 2, …, Var.y 3 4`, and every cube of `cubes64` is on these six variables.
- **Checked on the emitted file.** Clauses 1–4, 17–18 and 73–74 of the emitted `base.cnf` are the transitivity
  clauses of the triples (1,2,3), (1,2,4), (1,3,4) and (2,3,4) (gen_b2.py:79-81), written with exactly these
  numbers: `-1 -10 2 0`, `1 10 -2 0`, `-1 -11 3 0`, `1 11 -3 0`, `-2 -18 3 0`, `2 18 -3 0`, `-10 -18 11 0` and
  `10 18 -11 0`.

| file (from `cubes64`) | bytes | SHA-256 (encB = record) | record |
|---|---|---|---|
| base | 58,618,857 | `479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc` | `C6UPPER/SHA256SUMS.txt:86` |
| c11111 | 58,618,884 | `0fa206f7b75f8653e8da78dd3b750294d3ddafd8b86da53a489d8cc63fa02a8e` | `C6UPPER/SHA256SUMS.txt` B/ |
| c11011 | 58,618,885 | `32bdbdc2a615a6a8b110de612f5a3138c74559ba8f45b6d2aecc055322f4ad45` | `C6UPPER/SHA256SUMS.txt` B/ |
| c10101 | 58,618,886 | `5bfddfed9e280468eb3d616d7844886235bc5321ae94d44b8de8019cd7f68ec3` | `C6UPPER/SHA256SUMS.txt` B/ |
| c00000 | 58,618,889 | `206f2b4f3ebfbcceb2ba5dc5eb6ec68bef51059a8ca734fac9d837567d19f396` | `C6UPPER/SHA256SUMS.txt` B/ |
| n11111 | 58,618,885 | `efdf4681b3cfe45c5e0999fdf74cbce426bf627c53e71720b6a30e993e697d2d` | noty12 `cubes.sha256` |
| n10100 | 58,618,888 | `96161b8ea82e6b365e6789294d19cf81ed7ce359aaf4025310e6410b5ea64ea7` | noty12 `cubes.sha256` |
| n00000 | 58,618,890 | `33894742a77ef9fc56af7411d05c089d179bc2f5eb091a758d9bf94ee34d19d0` | noty12 `cubes.sha256` |

**(f) (6,8,11) as Lean values** (`logs/twin_check_6811.log`). `twin-check 6 8 11` gives EQUAL:
`encB 6 8 11 = (gen 6 8 11).clauses.toList` and `numVars 6 8 11 = 78059 = nv`. It writes no file; this is the
second and last compiled evaluation of `encB 6 8 11`.
- `encode` took 11.0 s and `gen` 4.6 s.
- The whole run took 17.3 s and 748 MB max RSS.

**Time and memory of `encB`.**
- **About 2.4× `gen`.** At (6,8,11), `encode` alone takes 11.0 s and the emission with 8 files 15.3 s and 928 MB,
  against `gen`'s 4.6 s and M1's 6.2 s / 428 MB. That is well inside the 8 GB cap and the design's 10× allowance.
- **Where the time goes** (`twin-profile`, `logs/twin_profile.log`; M2's numbers, when the twin was printed by
  `bodyL`, which M9 A2 replaced by Render's `bodyR`, byte for byte):

  | instance | diagCoded | genCoded | allCodesOf | renumber | bodyL | total |
  |---|---|---|---|---|---|---|
  | (6,8,9) | 0.1 s | 4.7 s | 0.3 s | 0.2 s | 0.8 s | 6.2 s, 211 MB |
  | (7,8,10) | 1.3 s | 13.4 s | 0.7 s | 0.7 s | 2.1 s | 18.3 s, 552 MB |

- **The cost is in `genCoded`,** mostly the extra `olit p a b` per extension step (deviation 3). An `okpair` table
  would remove it, at the price of a table lemma in M3. It is not needed at these sizes.

**(g) Audit** (`logs/audit.log`). `scripts/audit.sh` passes. Its check 4, as broadened by the review fixes, lists the
three declarations that mention the (6,8,11) instance (all in Cover.lean: `CubesUnsat64` and the two cover
theorems, statements and term proofs only). Six negative tests are in the log (see "M2 review fixes").

## M2 review fixes (2026-11-06, about 16:20 KST)

The review of M2 found no soundness, vacuity or byte-identity problem. It listed three minor fixes; each was checked
against the files, found real, and fixed. Only `EncB/KernelCheckB.lean`, `scripts/audit.sh`, the logs and the two
documents changed.

1. **No kernel instance had a chain of two levels.** Confirmed. Every kernel instance has K = 4: (3,4,1), (3,4,2),
   (6,4,1) here and (3,4,1), (3,4,2), (4,4,2) in `KernelCheck.lean`. At K = 4, `rng 2 (K - 1) = [2]` is one closing
   level. So neither the branch `lev + 1 < K - 1` of `extItems` (Gen: `lev + 1 < L`) nor the key set that
   `levelStep` passes to the next level was ever evaluated by the kernel.
   - **Fix:** two theorems in `KernelCheckB.lean`, both by `decide +kernel` and guarded by `#guard_msgs`:
     `encB_4_5_1 : numVars 4 5 1 = 13 ∧ encB 4 5 1 = […]` (no axioms) and `gen_4_5_1`, the same list for M1's
     `gen` ([propext]).
   - **The list:** gen_b2.py `3d47459a…` was rerun on (4,5,1). The output's SHA-256 `6b5cccde…` equals the corpus
     row, and the list equals the review's character for character.
   - **What it covers:** 6 base clauses (F₂ = variables 2–7), 6 extension clauses `[-F₂(b,c), -lab, -lt, F₃(a,b)]`
     (F₃ = variables 8–13), and 6 closing clauses `[-F₃(b,c), -lab, -lt]` on the key set of F₃.
   - **Cost:** both theorems together took 2.5 s and 750 MB in a scratch test. `KernelCheckB.lean` now builds in
     19 s (17 s before) with a 2.17 GB peak.
2. **Audit check 4 matched only the text `encB 6 8 11` on a single line.** Confirmed by negative tests. The M2
   audit passed all of these:
   - a `numVars 6 8 11` theorem with `decide` on the next line;
   - `(gen  6` / `8 11)` split over two lines and proved by `rfl`;
   - a `simp` proof of `CubesUnsat64`;
   - `set_option debug.skipKernelTC true`.

   **Fix:**
   - Check 4 now works per declaration: a column-0 command together with its continuation lines.
   - It matches `encB`, `gen`, `genCoded`, `numVars`, `allCodes`, `allCodesOf`, `encode` or `diagCoded` applied to
     `6 8 11` with any whitespace, and also `CubesUnsat64`. A declaration that matches fails the audit if it contains
     `decide`, `rfl`, `simp`, `simp_all`, `dsimp`, `omega`, `native_decide`, `of_decide_eq_true`, `example`,
     `run_cmd`, `#eval` or `#reduce` anywhere.
   - Check 1 now also forbids `set_option`, which covers `debug.skipKernelTC`, and `ofReduceBool`.
   - The header comment now names both `KernelCheck.lean` and `KernelCheckB.lean` as the build-time axiom guards.

   **Result:** the new audit passes the package and an unmodified copy, and fails on all five negative copies
   (`logs/audit.log`). It is still a text check, which indirection could evade. The real guard is the build itself:
   `Cover.lean`, which states the (6,8,11) theorems, builds in 0.27 s.
3. **`logs/axioms.log` listed 33 hand-picked names.** Confirmed: 15 M2 helper theorems (`div_mul_add`,
   `mem_dedup_clauses`, `mem_allCodesOf`, `numberMap_getD_le`, `dedupStep_spec`, …) and M1's three `gen_*` kernel
   theorems were missing. All 18 are within the three axioms. The review
   suggested appending its own list, but that would still be a list made by hand. Instead the log was regenerated
   from the environment by two queries:
   - **Query 1** (`logs/axioms_enum.lean.txt`) walks every constant declared in a module `EncB.*` and applies
     `Lean.collectAxioms`, the function behind `#print axioms`.
   - **Query 2** (`logs/axioms_query.lean.txt`) runs `#print axioms` on each of the 236 names that query 1 found.

   **Result:**
   - There are 236 named declarations: 71 theorems (47 written in the source, 24 generated, such as `injEq` and
     `sizeOf_spec`) and 165 definitions, inductives and constructors.
   - There are also 222 internal auxiliaries (`match_`, `proof_` and equation lemmas, recursors, private names).
   - All of them use only propext, Classical.choice and Quot.sound, and the two queries agree on every name.
   - The 47 source theorems are the review's 45 plus `encB_4_5_1` and `gen_4_5_1`.

**Reruns with the fixed package.** No source of the exe changed, and the exe is still `e9454996…`.
- **Build.** An incremental `lake build` returned 0 in 19.6 s with a 2.11 GB peak, rebuilding only `KernelCheckB`
  and `EncB`; the M2 clean builds already showed that the exe is reproducible. Every file was also recompiled from
  source with plain `lean` into scratch oleans. All 8 returned 0 with no message, so every `#guard_msgs` holds
  (`logs/build.log`).
- **Grid, by bytes.** `compare_b.sh twin`: 225/225 (222 MATCH, 3 REFUSED where Python raises) in 53.9 s.
  `compare_b.sh gen`: 225/225 in 25.4 s.
- **Values.** `twin_check.sh` on the grid plus (6,8,9), (7,8,9) and (7,8,10): 228/228 (225 EQUAL, 3 BOTH-REFUSE) in
  103.4 s.
- **Recorded instances.** `check_recorded.sh small twin` and `small gen`: (6,8,9), (7,8,9) and (7,8,10) all MATCH.
  The twin took 5.7 s, 11.2 s and 17.3 s.
- **(6,8,11) was not emitted again.** The exe is byte-identical to the one that made M2's emission (base and 7
  cubes, `logs/check_recorded_big_twin.log`). The review's own emission with the same exe matched the base and 7
  other cubes, but that run is not logged in this package.
- **For M3.** The review also named three lemmas that M3 needs first. They are listed under "What is NOT yet proved".

## M1 results (rerun 2026-11-06, 14:57–14:59 KST, exe `521dd64d…`)

The numbers in this section are M1's. In M2, `logs/compare_tiny.log` and `logs/check_recorded_small.log` were
rerun for `gen` with the M2 exe `e9454996…`, with the same results: 225/225 in 22.7 s, and three MATCHes at
2.65 s / 5.04 s / 7.72 s. `logs/check_recorded_big.log` and `logs/ref_regen.log` are still M1's.

The exe was rebuilt from scratch (`rm -rf .lake/build; lake build`). Its SHA-256 is
`521dd64d97cff63c4716ac6ac1cbf54863fdb3ac8d358868784a866fbdacddda`, identical to the M1 build, so the build is
reproducible. The load average was about 35 on 32 cores throughout, so all times are measured under contention.

**(a) Tiny grid: 225 of 225 agree** (`logs/compare_tiny.log`, 28.7 s).
- **Grid.** It covers every m in 3..8, K in 4..2m and t in 1..4 (192 instances), plus 33 extras:
  - K ≤ 3 and t = 0;
  - m ∈ {1, 2, 9, 10};
  - t = 5, 6 at K = 8 for m = 3..8;
  - t = 7, 8 at K = 8 for m = 6, 7.
- **222 are byte-identical** to gen_b2.py: 99 with odd m and 123 with even m.
- **On the other 3, Python raises and the exe refuses:** (2,4,3) and (2,5,4) (`RuntimeError: conflict`) and
  (1,4,2) (`KeyError`).
- **The corpus is not taken on faith.** `make_ref.py` was rerun from gen_b2.py `3d47459a…` into a scratch file in
  58.8 s. All 225 rows are identical to `ref/hashes.tsv` in every column except `seconds`; both give the column
  hash `5eba6a36…` (`logs/ref_regen.log`).

**(b) Recorded instances, streamed into sha256sum: all MATCH** (`logs/check_recorded_small.log`).

| instance | SHA-256 (Lean = record) | record read from, cross-checked against | Lean wall | max RSS |
|---|---|---|---|---|
| (6,8,9) | `9f63854369a76998e13217e1f4208e365d0821b07f253decca2b9aed1ba1d350` | `C6UPPER/logs/encb_gen.log:6` = `K8EXACT20261106/logs/regen_hashes.log:15` | 2.68 s | 188 MB |
| (7,8,9) | `67cd613d024e36912e61aeae1bb582e1cd992659a6902dfa936ba1f1caa300aa` | `K8EXACT20261106/logs/gen_m7K8t9.log` = `logs/exact_check.jsonl:2` | 5.12 s | 348 MB |
| (7,8,10) | `b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2` | `C7UPPER/SHA256SUMS.txt` (cnfb/m7K8t10.cnf) = `C6UPPER/logs/encb_gen.log:3` | 7.60 s | 488 MB |

- **Counts.** They equal Python's, e.g. (6,8,9): nv 42,728, ncl 1,040,348.
- **The (7,8,9) record is not independent.** It is gen_b2.py output of 2026-11-05 (`K8EXACT20261106/README.md`:
  "no earlier recorded hash exists"). For comparison, gen_b2.py on (7,8,10) took 18.1 s and 628 MB under the same
  load (M1 step).

**(c) (6,8,11): one generation, 8 files, all MATCH** (`logs/check_recorded_big.log`).
- **Cost.** `encb_dimacs files` took 6.21 s wall, 5.79 s user and 428 MB max RSS for the generation plus writing the
  8 files; with hashing, 6.7 s.
- **Counts.** nv 78,059, ncl 2,387,083, unit 2,347, cond 7,740, chain 2,376,426, equal to `C6UPPER/logs/encb_gen.log:8`.
- **Cleanup.** The files were written to the session scratchpad (`encblean/b6811`), hashed and deleted.

| file | bytes | SHA-256 (Lean = record) | record |
|---|---|---|---|
| base `B_m6K8t11` | 58,618,857 | `479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc` | `C6UPPER/SHA256SUMS.txt:86` |
| `full_Y12` | 58,618,861 | `1b09c21076189717407dfb4e187bbaa41fd2174f8b7eb7a5d61f7e5af2153395` | `C6UPPER/SHA256SUMS.txt:87` |
| `c00000` | 58,618,889 | `206f2b4f3ebfbcceb2ba5dc5eb6ec68bef51059a8ca734fac9d837567d19f396` | `C6UPPER/SHA256SUMS.txt` B/ |
| `c11011` | 58,618,885 | `32bdbdc2a615a6a8b110de612f5a3138c74559ba8f45b6d2aecc055322f4ad45` | `C6UPPER/SHA256SUMS.txt` B/ |
| `c10101` | 58,618,886 | `5bfddfed9e280468eb3d616d7844886235bc5321ae94d44b8de8019cd7f68ec3` | `C6UPPER/SHA256SUMS.txt` B/ |
| `c11111` | 58,618,884 | `0fa206f7b75f8653e8da78dd3b750294d3ddafd8b86da53a489d8cc63fa02a8e` | `C6UPPER/SHA256SUMS.txt` B/ |
| `n11111` | 58,618,885 | `efdf4681b3cfe45c5e0999fdf74cbce426bf627c53e71720b6a30e993e697d2d` | noty12 `cubes.sha256` |
| `n00000` | 58,618,890 | `33894742a77ef9fc56af7411d05c089d179bc2f5eb091a758d9bf94ee34d19d0` | noty12 `cubes.sha256` |

The noty12 hash list is `/path/to/data/c6upper-noty12-20261106/cubes.sha256`. It was only read; the
running unit `c6upper-noty12` was not touched. Its `results.tsv` had 8 of 32 ACCEPTED at 14:43. (Since 16:35: the
unit finished with 32/32 ACCEPTED; the list is also on record as `C6UPPER/noty12-2026-11-06/cubes.sha256`, with the
same 32 hashes, and the two rows above are in it.) The other 57 cubes
differ only in their 6-unit tail, which is printed by the same code; all 64 are checked in M9.

**(d) Kernel check and audit.**
- **Build.** The clean `lake build` builds `EncB/KernelCheck.lean` in 12 s. That file holds three `decide +kernel`
  equalities (kernel evaluation of `gen` against gen_b2.py's lists) and `#guard_msgs` on `#print axioms`
  (`[propext]`).
- **Audit.** `scripts/audit.sh` passes (`logs/audit.log`). A negative test (an appended `sorry` in a scratch copy)
  makes it fail.

**Independent review (the skeptic step, before this fix).** Its files are in the session scratchpad,
`encb-skeptic/`. It found:
- 28 MATCH and 3 REFUSED on a 31-row sample;
- 30 of 30 fresh gen_b2.py runs equal to the exe, 19 of them outside the grid;
- interpreter runs (`lake env lean --run`) equal to the compiled exe;
- no embedded hashes or paths in the exe;
- branch coverage of gen_b2.py: no branch is reached at (6,8,11) that the m = 6 tiny rows do not reach.

## How the port `gen` mirrors gen_b2.py (M1)

Nothing in gen_b2.py uses floats. The angular configuration uses only integers (`J = 2k + h` or `J = k`, ranks, `%`,
`//`), and so does the port. Determinism holds for these reasons:
- **Dicts.** Every dict is an `Array` indexed by a code of the key that is injective on keys that occur; 0 means
  absent, and every stored value is nonzero. The two dicts that are iterated, `orb` and `okpair`, also keep an
  insertion-ordered array. Each key is inserted once, so insertion order is loop order.
- **Sets.** The only `set.pop()` (line 136) happens on a one-element set; it is `unitOf`.
- **Sorting.** `sorted` is a stable insertion sort, applied only to lists with distinct entries. The `objs` tuples
  `((J, r), kind, idx)` are compared on the full tuple, with `'A' < 'P'` encoded as 0 < 1.
- **itertools.** Its orders are reproduced exactly:
  - `pairs`/`triples` for combinations;
  - `perms` for lexicographic permutations;
  - `bitTuples` for `product`, last coordinate fastest.
- **Variable allocation.** `nv` is threaded through the loops, and `fv` is inlined at its two call sites, so chain
  variables are allocated in clause-stream order.
- **Failure cases.** Where Python raises (an `assert`, a `KeyError`, either `RuntimeError`), Lean drops the literal
  and counts `bad`, or sets `conflict`, and the exe refuses to print. `bad = 0` for every m ≥ 2.
- **Array bounds.** Every `setIfInBounds` index stays in range (checked by the review). `orbTab` has N³ entries,
  `F` has `max (K−1) 3 · N²`, and `forced` has nv + 1 and is indexed only by orbit literals.

| gen_b2.py | content | Gen.lean / Emit.lean |
|---|---|---|
| 28-34 | arguments, `odd`, `nv`/`new()` (`pid` at 30 is unused, so not ported) | `gen` 240-242 |
| 36-39 | `Yv`, lexicographic | 243-248 |
| 40 | `Hv`, odd m only | 249-254 |
| 42-49 | `canon` | `rotate` 98, `canon` 103-109 |
| 50-55 | `orb`, numbered in order of first appearance over `combinations(pts, 3)` | 259-275 (`orbTab` + `orbList`) |
| 56-62 | `perm_sign` | `permSign` 91-92 |
| 63-76 | `olit`: first matching rotation, then argsort sign | `olit` 114-125 |
| 79-81 | transitivity | 277-281 |
| 83-85 | `forced`, counters, loop over `orb.items()` | 282-290 |
| 86-87 | `Ls`, `free` | `angOuts` 187-189 |
| 89-94 | `permutations` × `product`, `rk`, `h` | `angOuts` 190-196 |
| 96-102 | premises (Y literals, then H literals) | `angOuts` 198-204 |
| 104-111 | keys of the points and antipodes | `patternLit` 144-153 |
| 112-117 | equal keys give no clause (`assert not odd`) | `patternLit` 154-156 |
| 118-119 | sort, `kinds` | `patternLit` 158-161 |
| 121-124 | rule A (`PAPAPA`/`APAPAP`) | `patternLit` 162-166 |
| 126-132 | rule B: `find('PPP')` as the first cyclic start in 0..5, middle point outermost | `patternLit` 167-181 |
| 134-137 | unit when every pattern gives the same non-`None` literal | `unitOf` 210-213, `gen` 291-296 |
| 138-141 | conditional clauses `[-prem] + [l]` | `gen` 297-304 |
| 143-150 | nesting units and the conflict check | 305-316 |
| 151-153 | `is_false` | 317-321 |
| 156-160 | `L`, pivot, `Q`, fresh `F` per pivot | 322-333 |
| 161-165 | `fv` | inlined at 349-353 and 371-375 |
| 166-172 | `okpair` | 334-345 |
| 174-175 | base clauses `[F2(a,b), -l]` | 346-355 |
| 176-190 | extension and closing clauses | 356-379 |
| 191-194 | DIMACS output | Emit.lean `pushClause` 57-60, `body` 63, `header` 66 (the gen modes; the twin prints through Render.lean's `pushClauseR` 127-130, `bodyR`, `headerR`, since M9 A2) |
| — (mkcubes.py:11-15) | cube layout | Emit.lean `cubeTail` 69-70, `cubeUnits` 73-84, `mainGen` 264-314 (gen; twin: Render.lean `cubeBodyR` 140, `renderCube` 147-148) |
| 195-200 | `.map.json` and summary line | summary line only (Emit.lean `summary` 94-98); the map file is not ported |

## Trust: what the tests check and what stays trusted

**Trust items E1–E6 (`DESIGN.md` §1.4) after M9.** These are the facts between the Lean theorems and the
certificates. As of M9 they were not the only thing missing for an end-to-end theorem: that a counterexample yields
a `Model 6 8 11` (M4–M6, Mathlib) and the assembly (M8) were not proved. **Since 2026-11-07 (M4–M8, section "M4–M8
(geo)") they are the only remaining trust of the Lean route for m = 6** (`sixfold_es8_of_texts`).

| item | what M9 settled | what stays trusted |
|---|---|---|
| **E1** emitter output | **Checked by compiled code** (not proved): the exe's text for the base and for each of the 64 cubes of `cubes64`, by index, has the recorded SHA-256 of the certified file, 65/65, plus 3 other instances; three runs, two exes (`logs/m9_hash_binding.log`, `m9_a2_hash_binding.log`, `m9_a2fix_hash_binding.log`); a one-digit change in a record is caught (`m9_hash_binding_selftest.log`) | that the compiled exe computes the Lean definitions (E4); SHA-256 and the record files (E6) |
| **E2** verdicts | unchanged: the 64 hash-bound ACCEPTED verdicts on record (32 encoder-B rows of the replay, 32 noty12 rows). New: `scripts/resolve.sh` regenerates any of them with the pinned tools; run on 2 cubes, 2/2 ACCEPTED (twice, same CNF and proof hashes) | the other 62 verdicts are the records', not re-run; cake_lpr itself (its HOL4/CakeML verification); the proofs are not public |
| E2 provenance (R7) | `scripts/build_cake_lpr.sh`: the build recipe of commit `033aad53` with source hashes pinned from the local clone (first recorded by M9); **not run** | the binary `c14ff498…` is a build of `033aad53` (replay record), not of the vendored `a36874a8` |
| **E3** DIMACS semantics | **narrowed, proved:** the printed text parses back, by the reference parser `parseDimacs`, to exactly `encB 6 8 11` and `cubeCnf (encB 6 8 11) c` (`parseDimacs_render`, `parseDimacs_base6811`, `parseDimacs_cube64_get`), and verdicts on the 64 parsed texts give `CubesUnsat64` (`cubesUnsat64_of_texts_get`); since the review fixes also on the UTF-8 bytes (`parseDimacsBytes_cube64_get`) and composed with M3 (`no_model_6811_of_texts`) | that cake_lpr reads every text of `parseDimacs`'s language as `parseDimacs` does, and that its `s VERIFIED UNSAT` means `¬ DimacsSatisfiable` of that list; evidence only (`m9_a2_cake_parse.log`) |
| **E4** compiler and runtime | **narrowed:** core's `toString` (`reprFast`, `lean_string_of_usize`, the bodiless `String.Internal.append`) and the M1/M2 printers are off the twin's trust path; the header counts are inside the proved term | the Lean compiler on `encode` and on Render's printer; core's runtime (`String.push`/`++`, `Nat` arithmetic, `Nat.digitChar`, `List`/`Array`, `String.toNat?`, `putStr`); a reading of Emit's IO glue (details below) |
| **E5** kernel, Mathlib, the paper's notions | as of M9 unchanged (EncB is Std-only). Since M4 (2026-11-07) the package `geo/` uses Mathlib `f897ebcf`, the repository's revision, with the repository's definitions vendored verbatim (`geo/VENDOR.sha256`) | the kernel; Mathlib `f897ebcf`; that `Point`, `GeneralPosition`, `HasConvexNGon`, `Invariant` and `rotAbout` mean what the paper says |
| **E6** SHA-256 | unchanged | as before |

- **The object of the theorems is `encB`, and the emitter prints `encB` through a proved renderer (M9 A2).** In
  the `twin-*` modes the exe computes `e := encode m K t` (`encodeChecked`, Emit.lean:129-136), whose fields are
  `encB m K t` and `numVars m K t` by definition. `twin-base`, `twin-cube` and `twin-cube64` write the one string
  `cnfText e cube` with a single `putStr` (Emit.lean:193, :200, :182; `cube = []` for the base,
  `cube = cubes64.get ⟨i, h⟩` for `twin-cube64`), and `twin-cubes64` writes `renderCube e.nv e.clauses
  (bodyR e.clauses) c` (:165, :169). Since the package has none of the escapes listed above, the compiled program
  is the definition the kernel reduces, up to the Lean compiler and core's runtime (E4 below). The kernel and Python
  agree on (3,4,1), (3,4,2), (6,4,1) and (4,5,1) for `encB`; for `gen` on the M1 instances (3,4,1), (3,4,2) and
  (4,4,2), and on (4,5,1).
- **What is proved about the text** (`EncB/Render.lean`, Std-only; axioms within [propext, Classical.choice,
  Quot.sound], 13 of them guarded at build time by `#guard_msgs`, all of them in `logs/m9_axioms.log`):
  - `cnfText_encode` (:156, `rfl`): `cnfText (encode m K t) cube = renderCube (numVars m K t) (encB m K t)
    (bodyR (encB m K t)) cube`;
  - `renderCube_eq` (:164): `renderCube nv F (bodyR F) cube = render nv (cubeCnf F cube)`;
  - `parseDimacs_render` (:585): `parseDimacs (render nv F) = some (nv, F)` for every `F` whose literals are
    nonzero with `natAbs ≤ nv` (`encB_wf` gives this for `encB`, symbolically);
  - for (6,8,11), with no evaluation of the instance: `parseDimacs_base6811` (:806), `parseDimacs_cube64_get`
    (:800) `: parseDimacs (cnfText (encode 6 8 11) (cubes64.get ⟨i, h⟩)) = some (numVars 6 8 11, cubeCnf (encB 6 8
    11) (cubes64.get ⟨i, h⟩))`, and `cubesUnsat64_of_texts_get` / `encB_unsat_of_texts_get` (:833, :842): if each
    of the 64 texts, by index, in exactly the form the exe prints and `scripts/hash_binding.sh` hashes, parses to an
    unsatisfiable clause list, then `CubesUnsat64` and `¬ DimacsSatisfiable (encB 6 8 11)` (membership forms:
    `cubesUnsat64_of_texts`, `encB_unsat_of_texts`, :814, :821);
  - `cnfText_bytes` (:711): the UTF-8 encoding of the text (`String.toUTF8`, what `putStr` writes) is the list of its
    characters' codes mapped by `·.val.toUInt8`; with `cnfText_ascii` (Compose.lean, review fix: every character is
    ASCII) this is one byte per character, and `parseDimacsBytes_cube64_get` states the round trip on these bytes.

  `parseDimacs` (:321) is a reference parser for the plain DIMACS subset the printer writes: the line
  `p cnf <nv> <nc>`, then exactly `nc` lines `l₁ … lₖ 0` with single spaces (the empty clause is ` 0`), nonzero
  literals with no leading zero and no `+`, `|l| ≤ nv`, every line ending in `\n`, and nothing else. Fourteen
  kernel-checked examples (:325-345) fix one accepted text and 13 rejected ones. The header line and counts, the
  clause lines, the unit tail and the decimal printing are all inside the proved term; the twin uses Render's own
  `pushNat`/`pushInt`, not core's `toString`. The switch kept every byte: the A1 exe and the A2 exe agree on
  321/321 runs over all modes (`logs/m9_a2_regress_modes.log`), and the hash binding gives 68/68 with the A2 exe
  (`logs/m9_a2_hash_binding.log`, rerun after the fixes below in `logs/m9_a2fix_hash_binding.log`).
- **What stays trusted for the text** (E3/E4 of `DESIGN.md` §1.4, as narrowed by A2):
  - **E3:** cake_lpr reads every text in `parseDimacs`'s language as `parseDimacs` does, and its `s VERIFIED
    UNSAT` means `¬ DimacsSatisfiable` of that list; `cubesUnsat64_of_texts_get` states exactly this interface.
    `parseDimacs` is not modelled on cake_lpr's parser source, which is not on this machine (the `HOL/` and
    `cakeml/` submodules of the cake_lpr clone at `033aad53` are empty). Evidence, not proof
    (`logs/m9_a2_cake_parse.log`): cake_lpr's printout of what it parsed is byte-identical to 21 small and medium
    twin texts and to the (6,8,11) base and cubes 0 and 63, which have the recorded hashes; of the 13 texts
    `parseDimacs` rejects, cake_lpr rejects 5 and reads the other 8 the standard way, so on these examples the
    language accepted here is the stricter one.
  - **E4:** the Lean compiler compiles `encode` and Render's functions faithfully; core's runtime for `String.push`
    and `++`, `Nat` arithmetic, `Nat.digitChar`, `List`/`Array`, `String.toNat?` on the arguments, and `putStr`
    writing `s.toUTF8`; and a reading of Emit's IO glue: that the printed `e` is `encode m K t` and the printed cube
    is `cubes64.get ⟨i, h⟩`, and that nothing else goes to stdout.
  - **E1/E6:** SHA-256 and the record files.
  - **No longer on the twin's trust path:** core's `toString` on `Nat` (`reprFast`, `lean_string_of_usize`) and
    on `Int`, M2's printer `bodyL`/`cubeBody` (removed), M1's printer `pushClause`/`body`/`header`/`cubeTail`
    (Emit.lean:57-70, used only by the gen modes) and the header counts. `toString` still formats the stderr lines
    (summary, cube name and units), which are not hashed.
- **`allCodes` order = Python's `new()` order is tested, not proved.** Soundness does not need it (D4):
  `dimacsSat_of_holds` holds for any duplicate-free or duplicate-containing code list, and the numbering only has
  to make the hashes match.
- **The cube variables.** The cover theorem holds for any six nonzero variables. That `cubeVars64` are Y12 Y13 Y14
  Y23 Y24 Y34 in `encB 6 8 11` matters only for the reading of the cubes. It is checked by compiled code in the
  emission run and by the hashes of the c- and n-cube files against the records.

## What is NOT yet proved

- **The geometric meaning of the clauses.** Since M3, `encB_satisfiable` relates every clause of `genCoded` to a
  combinatorial `Model` (orientations `chi`, the ψ-order `psiLt`, chains), for even m. Nothing yet connects a
  `Model` to points in the plane. The missing pieces are:
  - the geometric side, labelling and `modelOfLabelling` (M4–M6, Mathlib; planned for after the campaign cutoff,
    done on 2026-11-07);
  - the assembly `sixfold_es8` (M8; done on 2026-11-07).

  So, as of M9, the sixfold bound was **not** formally verified end to end, and P1 said so.

  **Superseded on 2026-11-07 (section "M4–M8 (geo)"):** M4–M8 are done; `sixfold_es8_of_texts` proves the sixfold
  bound from the meaning of the 64 verdicts, with E1–E6 as the remaining trust. P1 was updated on 2026-11-07
  (`WRITEUP/P1/README.md`, "Revision for the end-to-end Lean check (ENCBLEAN M4–M8), 2026-11-07"): for m = 6 via
  encoder B the sixfold bound is formally verified end to end, assuming the 64 cake_lpr verdicts and E1–E6; m = 7
  stays written.
- **The hash binding is a computation, not a proof (M9).** `scripts/hash_binding.sh` shows, by running the compiled
  exe, that the texts of `encB 6 8 11` and the 64 cubes of `cubes64` have the hashes of the certified files (68/68
  with 3 other instances; `logs/m9_hash_binding.log`, `logs/m9_a2_hash_binding.log`,
  `logs/m9_a2fix_hash_binding.log`). That the compiled code computes the Lean definitions is trust item E4.
- **No equality between `encB`, `gen` and gen_b2.py is proved.** It is tested:
  - by bytes on 225 + 4 instances and 7 cubes (the M2 review checked 7 more cubes in its own emission);
  - as Lean values on 229 instances;
  - by kernel evaluation on 4 tiny instances.
- **The three lemmas that the M2 review said M3 needs first are settled.**
  - "`dedupBy` keeps only input elements" is `EncB.Orbit.mem_dedupBy` (SoundOrbit.lean:39).
  - "`canon` keeps triples valid" is part of `orbListSpec` (SoundOrbit.lean:161).
  - "Every literal of `genCoded` is `±(v.code m K t)` for a valid `v`" was not needed as a separate lemma. M3 proves
    each family's clauses directly under `M.τc = M.τ ∘ decodeCode`, through `holds_y`, `holds_orb`, `holds_f` and
    `olitSpec`, which apply `decodeCode_code` to the labels at hand. The all-literals statement itself is still
    checked only by compiled code (`codesDecode`) and by the kernel at (3,4,2).
- **The DIMACS round trip is proved (M9 A2)** against the reference parser `parseDimacs` (`parseDimacs_render`,
  and for the 64 printed (6,8,11) cube texts `parseDimacs_cube64_get`). Not proved: that cake_lpr reads these texts
  as `parseDimacs` does (trust item E3, see Trust above).
- **The verdicts are cake_lpr's.** No Lean statement is about cake_lpr; `cubesUnsat64_of_texts_get` (and its
  composition with M3, `no_model_6811_of_texts`) takes the 64 verdicts as its hypothesis. `scripts/resolve.sh` reproduced 2 of them (c00100, n10000) with the pinned tools; the
  other 62 rest on the records (replay B rows, noty12), and `resolve.sh all` (about 22 h) was not run.
- **n-cube verdicts: certified (R1 resolved, 16:35).** The c6upper-noty12 run's `run.log` says at 15:40:35: "32 of
  32 NOT-Y(1,2) cube proofs accepted by cake_lpr, hash-bound (results.tsv)". Its post-run gate `verify_final64.py`
  has since run and prints PASS (`C6UPPER/noty12-2026-11-06/verify_final64.log`), so variant A has all 64 verdicts.
  What remained for variant A after M9 was the Lean side (M4–M6 and M8), not the certificates; it is done since
  2026-11-07. This README step did not run the gate.
- **m = 7** (sevenfold) is ported for byte identity only. Its soundness is out of scope (`DESIGN.md` §1.3).

## M1 review fixes applied (2026-11-06, about 15:00 KST)

All four issues of the review were checked against the files, found real, and fixed:

1. **Stale Gen line numbers in `DESIGN.md`.** All 21 `Gen:` citations had drifted. 19 were two lines low and two
   (Gen:33-34 and Gen:25-28) had shifted less. Each was re-read against the current Gen.lean and corrected
   individually: `gen` 240-380, `patternLit` 142-181, `canon` 103-109, `unitOf` 210-213, key test 155, `Pt` 42,
   and so on. The PPP-failure branch is now cited at Gen:170. A revision note at the top of `DESIGN.md` names the
   Gen.lean hash the citations refer to.
2. **The trust list now names the emitter's text rendering.** `DESIGN.md` E3 and E4 list Emit.lean:26-40, `main`
   (:82-131) and core's `toString`, with the round trip as the optional way to remove them. This README says the
   same. Appendix A item 8 wrongly called `pushClause` Gen's; it now cites Emit.lean. (Superseded in M9 A2: the
   twin now prints through the proved `EncB/Render.lean`, and E3/E4 are narrowed; see "Trust".)
3. **Chain-variable code collision for tiny K.** In `DESIGN.md` §3.1 the code is now
   `fBase + ((piv·FL + l)·N + ptCode a)·N + ptCode b` with `FL = max (K−1) 3`, matching Gen's `FL` (Gen:325).
   The levels that occur satisfy l < FL for every K, including K ≤ 2, where F₂ exists. The `decodeCode` row now
   states the level bound and needs no hypothesis on K. (Gen itself was already safe: its `F` table is per pivot
   and sized `FL·N²`.)
4. **Minor points.**
   - The `sixfold66_of_unsat` sketch now passes both side conditions, `(by decide) (by decide)` for `heven` and
     `hm` (superseded in M3: the sketch now calls `encB_satisfiable_6811`, see DESIGN §1.1). It also uses the name `modelOfLabelling` of §2.4 consistently, in D5 and the §2.4 heading too.
   - M9 now says to emit from the Lean list `cubes64`, not from `cubeUnits`, and to read recorded hashes from
     files.
   - `check_recorded.sh` no longer hard-codes any hash. It reads each one from its record file and requires it to
     equal a second record, otherwise it reports RECORD-ERROR. A negative test with missing records exits 1. The
     (7,8,9) record is labelled as not independent.

No Lean source changed in this step: Gen.lean `ec97b335…`, Emit.lean `7cdd3f1c…` and KernelCheck.lean `6a141b39…`
are the same as in M1, and the exe hash is unchanged. `scripts/audit.sh` and the logs `build.log`, `ref_regen.log`
and `audit.log` are new.
