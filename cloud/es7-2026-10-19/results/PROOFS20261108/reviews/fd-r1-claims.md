# Review fd, round 1, lens: claims, labels and LaTeX

Section: `sections/fd.tex` (1028 lines) and `sections/fd.map.tsv` (32 rows).
Verdict: **fail**. There is one major finding (M1) and eight minor ones (m1 to m8). No blocker.

Paths below are relative to the staging directory (`sections/`, `build/`), to the results directory RES
(`LAYERLEAN/...`, `SYMLEAN/...`, `LEANEXT/...`, `MIRRORETV/...`), or to the repository root (`ErdosSzekeres/...`,
`docs/...`, `scripts/...`, `lean-toolchain`, `lake-manifest.json`). Mathlib sources were read from a Mathlib checkout
at revision `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` (read only, outside REPO); Lean core sources from the Lean
4.24.0 toolchain (`src/lean/Init/Core.lean`). Nothing under REPO was modified; no Lean, lake or solver was run.

## What was checked, and the result

1. **Compile.** From `build/`: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
   -output-directory=claims-fd-r1 fd_wrapper.tex`, twice.
   - Both passes exit 0; the PDF has 13 pages (`build/claims-fd-r1/fd_wrapper.log`, `pass1.txt`, `pass2.txt`).
   - No `!` error, no "Missing $", no undefined control sequence.
   - Undefined references: `ll:def:hv`, `ll:def:peel` (fd.tex:72), `ll:def:66-70` (:304), `oc:lem:rot-inv` (:458).
     All four are export labels of other sections in the contract. Nothing else is undefined.
   - Warnings: two overfull hboxes, 2.1pt (lines 765-766) and 5.1pt (lines 788-789); see m8(d).
2. **LaTeX rules.** The file starts with `\section{Conventions and foundations}\label{fd:sec}`. No `\newcommand`,
   `\def`, `\usepackage`, `\documentclass` or `\begin{document}`. Only preamble environments are used.
3. **Machine paths and tool names.** Grepped `fd.tex` and `fd.map.tsv` for `/private`, `/Users`, `/home`, `/tmp`,
   the scratch directory, the user name and tool names: no hits.
4. **Overclaiming words.** Grepped for verif*, certif*, proved/proven, rigorous, guarantee, confirm, establish,
   machine-checked, "exactly as written". Only allowed uses ("not proved in Lean", the definition of the labels,
   "certificate" for the `linear_combination` coefficient and for exact rational checks). See m1 for one framing sentence.
5. **Labels.** All 20 contract export labels `fd:def:{point,orient,gp,cp,ngon,forces,inv,rot}` and
   `fd:lem:{orient,affine-orient,collinear,cp-hull,mono,affine-cp,caratheodory,four-subsets,four-positive,pos-triples,
   pos-cycle,separation}` are defined, on the named statements, and appear in the contract order (the extra helper
   labels are interleaved). No duplicate labels. Every `\ref` is an own label or one of the four cross-section export
   labels above.
6. **Statement map.** 32 rows, header as required, 5 columns each. The 32 non-remark statement environments
   (9 definitions, 23 lemmas) match the map exactly in label, kind, Lean names and file:line. The 7 remark environments
   have no rows (m7).
7. **Lean names and lines.** Every Lean name in `\leanref` and `\lean` exists (repository names read in their files;
   Mathlib names `Collinear`, `vectorSpan`, `ConvexIndependent`, `ConvexIndependent.mono`,
   `convexIndependent_set_iff_notMem_convexHull_diff`, `collinear_iff_of_mem`, `AffineMap.image_convexHull`,
   `Caratheodory.minCardFinsetOfMemConvexHull`, `Function.iterate_succ_apply'`, `Function.minimalPeriod`,
   `AffineIndependent` found in the Mathlib checkout). Every file:line was opened; all declaration lines are exact:
   Definitions.lean:9,12,17,21,25; Orientation.lean:9,12,15,18; OrientationGeometry.lean:36,66; Basic.lean:6,11,15,20,
   25,31,37,47,58; Suk/FourPoint.lean:10,40; Suk/SupportingLines.lean:6,11,21,28,40,47; Suk/OrientationClique.lean:9,33;
   ConvexCycleCuts.lean:8,11,31; Suk/Reflection.lean:6,47,52 (and :55, the `rw` step); LAYERLEAN/LayerLemma.lean:52,105,
   298,302,311,319,465; SYMLEAN/SymmetricReduction.lean:271,400; LEANEXT/orbit/OrbitConsistency.lean:47,93,117;
   MIRRORETV/lean/MirrorMain.lean:2182 (proof 2184-2185); SYMLEAN/mirror/ReductionThreeClasses.lean:3741.
   Namespaces checked (`ErdosSzekeres.LayerLemma`, `.SymReduction`, `.OrbitConsistency`, top-level `MirrorOdd`).
8. **Fidelity of the statements to Lean.** Every Lean-tagged statement was compared with its declaration (hypotheses,
   strictness, Finset/Set, quantifier order). All match, including `iterate_mem` (arbitrary type, said in the text),
   `convexPosition_of_strict_supports`, `orient_support_sum` (`orient p (p+b-a) r`), the twelve support values of
   `convexPosition_four_of_positive` (q = a+b-d, b+c-a, c+d-b, d+a-c; all twelve values recomputed),
   `convexPosition_of_positive_triples` (4 ≤ |s|, p injective on all of ι), `hasConvexNGon_of_positive_cycle`
   (all increasing triples of e). The contract's fd statements are all true and match Lean; no contract discrepancy.
9. **SHA-256** (recomputed with `shasum -a 256`): all 14 prefixes in the table at fd.tex:92-105 are correct
   (`2425500eefd1`, `f67955ac7091`, `c7db9bbbb65e`, `13667aa2d3dc`, `f3783fe9766f`, `6a8e12677685`, `cf63d5219b47`,
   `b4ad0ba9e583`, `8b99cbf5fa2b`, `afb8542dceb0`, `6d5ec90a4215`, `9b843180ac38`, `ca623e55a1b9`, `0cc83994fe8c`).
10. **Axioms and build logs** (each opened).
    - `docs/validation/axiom-audit-lower-bound-2026-10-11.txt`: lines 87, 103, 113, 114, 119, 175, 176 are exactly the
      seven declarations named, each `[propext, Classical.choice, Quot.sound]`.
    - The nine declarations said to be covered transitively are indeed used in those proofs (FourPoint.lean:42,45;
      SupportingLines.lean:14,31,37,58; Reflection.lean:13,55,60; OrientationGeometry.lean:69).
    - The twelve "not covered" names indeed do not occur in the audit. The text search claim holds: the import closure
      of their files is the table files plus `Suk/BaseOrder`, `Suk/BaseChart`, `Suk/TriangleOrder` (checked), and none
      of these contains `sorry`, `admit`, an `axiom` declaration or `native_decide`.
    - Last commits of all twelve main-library files: 4 and 5 October 2026; the audit file was committed 11 October 2026.
      `lean-toolchain` (v4.24.0) and the Mathlib pin did not change after 10 October.
    - `LAYERLEAN/logs/build.log`: `lake env lean LayerLemma.lean`, exit code 0, 0 message lines.
    - `LEANEXT/review/axioms.log`: line 1 `iterate_mem` [propext, Quot.sound]; lines 22, 23, 33 `rotAbout_eq_crot`,
      `rotAbout_injective`, `rotAbout_iterate` with the three standard axioms. `LEANEXT/review/REPORT.md` confirms the
      reviewed file is LayerLemma.lean with SHA-256 `afb8542d…` (the current file).
    - `SYMLEAN/logs/runs.tsv` row 2: SymmetricReduction.lean, prefix `6d5ec90a`, exit 0, 0 output lines.
    - `LEANEXT/orbit/logs/build.log`: `exit=0`; `LEANEXT/orbit/logs/axioms.log` line 1: `orient_rotAbout_inv`, three
      standard axioms.
    - `MIRRORETV/lean/MirrorMain.out`: 0 errors, 121 warnings. `SYMLEAN/mirror/README.md:49-50`: exit 0, no errors.
    - The five research files contain no `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by` or `unsafe`.
11. **Reading conventions required by the scope.** Present: paths relative to RES or the root (fd.tex:15-21, but see
    m4), commit `7e32ee259` (= HEAD `7e32ee25931883f2…` of branch `es7-night-2026-11-01`), Lean 4.24.0 and Mathlib
    `f897ebcf` (full hash matches `lake-manifest.json`; package name `erdos_szekeres` matches `lakefile.toml`), the three
    rigor labels (:31-52), explicit casts and truncated subtraction (:54-64). The purpose paragraph states that these
    are human-readable proofs of Lean-checked results, that the Lean checks remain the primary evidence, and that the
    proofs are not refereed (:3-12).
12. **Other factual claims checked.** "19 definitions of rotAbout, all with this same body" (a grep of the research
    records finds exactly 19, all identical; none outside RES). The three `Invariant` and three `rotAbout` copies are
    textually identical and all files import `ErdosSzekeres.Definitions` (same `Point`). `Sixfold66`/`Sevenfold70` use
    real numerals 6 and 7 (LayerLemma.lean:1104,1109). `convexIndependent_of_affineIndependent` is used in the main
    library only at Basic.lean:64. The "Deliberately not covered" list is complete for the scope files Definitions,
    Orientation, OrientationGeometry, Basic, FourPoint, SupportingLines, OrientationClique and ConvexCycleCuts.
    Hypotheses (`Sixfold66`, `Sevenfold70`, SAT verdicts) are mentioned only as propositions, never as proved.

## Findings

### M1 (major) — `fd:lem:affine-orient` has an exact Lean counterpart; the section says it has none

- **Where.** fd.tex:417 (head `[Orientation under affine maps; written step]`); map row `fd:lem:affine-orient`
  (lean_name `-`); Remark `fd:rem:affine-orient-lean` (fd.tex:455-461: "Lean proves the special cases it needs
  separately"); Coverage (fd.tex:1002-1003: "Written steps without a single Lean counterpart: …
  \ref{fd:lem:affine-orient}").
- **Evidence.** `SYMLEAN/AffineReduction.lean:1241` (namespace `ErdosSzekeres.SymReduction`, line 54):
  ```
  theorem orient_affine {g : Point → Point} {L : Matrix (Fin 2) (Fin 2) ℝ} {b : Point}
      (hg : ∀ p, g p = L *ᵥ p + b) (x y z : Point) :
      orient (g x) (g y) (g z) = L.det * orient x y z
  ```
  This is exactly the main formula of `fd:lem:affine-orient` (g(x) = Ax + v ⇒ orient(g a, g b, g c) = det A ·
  orient(a,b,c)). A verbatim copy is at `SYMLEAN/mirror/ReductionThreeClasses.lean:1267`. It is Lean-checked
  transitively: `generalPosition_image_affine` (AffineReduction.lean:1278-1281) uses it, `generalPosition_image_affineEquiv`
  uses that, and `SYMLEAN/logs/AffineReductionAxioms.out` line 13 prints the latter with the three standard axioms;
  `SYMLEAN/logs/runs.tsv` row 4 records AffineReduction.lean (prefix `41cfc0b6`, the current file, full prefix
  `41cfc0b60aec`) compiling with exit 0 and no output. The `ar` section already states it
  (`ar:lem:orient-affine`, ar.tex:345) and its proof says "This is Lemma~\ref{fd:lem:affine-orient}", so the document
  as it stands contradicts itself.
- **Why major.** The scope requires each fd statement to be "tagged with its Lean name(s) where one exists", and the
  contract requires a `\leanref` in the head of every statement that corresponds to a Lean declaration. The Coverage
  sentence is a false statement about the Lean code, and the remark suggests that only special cases are in Lean.
  (Mathematics is unaffected. If the verifiers decide that the scope only covers the listed source files, this could be
  downgraded to minor; I report it as major because the claim "without a single Lean counterpart" is false.)
- **Fix.** Tag the head with `\leanref{ErdosSzekeres.SymReduction.orient_affine}{SYMLEAN/AffineReduction.lean:1241}`
  (mention the copy at `SYMLEAN/mirror/ReductionThreeClasses.lean:1267`), mark (i) and (ii) as written steps, update
  the map row, remove `fd:lem:affine-orient` from the "without a single Lean counterpart" list, reword the remark
  ("Lean also proves the special cases separately: …"), add `SYMLEAN/AffineReduction.lean` with SHA-256 prefix
  `41cfc0b60aec` to the sources table, and cite runs.tsv row 4 and AffineReductionAxioms.out line 13 in "Axioms
  evidence".

### m1 (minor, borderline) — opening sentence overstates what the written proofs give for computations

- **Where.** fd.tex:7-10: "every statement that corresponds to a Lean declaration … receives a complete proof that can
  be checked without Lean."
- **Issue.** For statements labelled computer-assisted in later sections (finite checks by `decide`/`decide +kernel`,
  certificate checks), the written proof gives the reduction and a precise description of the computation, but the
  computation itself cannot be checked by a reader without a machine. The Rigor-labels paragraph (fd.tex:43-48) says
  so correctly, and contract rule 5 uses similar wording, so I rate this minor; read alone, the sentence overclaims.
- **Fix.** Add a clause such as: "…that can be checked without Lean, except that for statements labelled
  computer-assisted the finite computation is stated precisely and reduced to, but not carried out by hand."

### m2 (minor) — further Lean counterparts are understated in Coverage and remarks

- `fd:lem:orient`(d) (sign of a permutation) has the Lean counterpart `ErdosSzekeres.OrbitConsistency.orient3_perm`
  (`LEANEXT/orbit/OrbitConsistency.lean:178`: `orient3 (t ∘ σ) = sign σ * orient3 t` for `t : Fin 3 → Point`;
  axioms.log line 5; export label `oc:lem:perm`). It is the case R = ℝ of the written (d), which is stated over any
  commutative ring. fd.tex:377 and :1003 call (d) a written step "without a single Lean counterpart".
- `fd:lem:affine-cp`: the forward directions of (b), (c), (d) are `SymReduction.convexPosition_image_affine`
  (AffineReduction.lean:1263, injective Mathlib affine map), `SymReduction.generalPosition_image_affine` (:1278, form
  `g p = L *ᵥ p + b` with `det L ≠ 0`) and `SymReduction.hasConvexNGon_image_affine` (:1298; printed at
  AffineReductionAxioms.out line 16); (a) is Mathlib's `AffineMap.image_convexHull` (named in the proof). Remark
  `fd:rem:affine-cp-lean` is accurate for "the main library", but the Coverage list should not suggest that nothing in
  Lean corresponds.
- **Fix.** Name these in the remarks (or as partial tags) and reword the Coverage sentence, e.g. "Written steps
  (some have partial Lean counterparts, named in the remarks)".

### m3 (minor) — `ConvexCycleCut` is not used in SAT searches

- **Where.** Remark `fd:rem:pos-cycle`, fd.tex:935-936: "the clause family ConvexCycleCut … used in SAT searches".
- **Evidence.** The cuts are added to Z3 coordinate-repair searches: `scripts/joint_vertical_repair.py` (Z3
  `SolverFor("QF_LRA")`, line 53) and `scripts/joint_planar_repair.py` (Z3 nonlinear real arithmetic), described in
  `docs/SAT.md:168-233`; the Lean docstrings (ConvexCycleCuts.lean:5-7, 28-30) say "used by the repair searches" and
  "This does not verify an SMT solver". Elsewhere in this document "SAT" means CNF solving with certificates, so the
  phrase can mislead.
- **Fix.** "used as cuts in the SMT (Z3) coordinate-repair searches (`docs/SAT.md`)".

### m4 (minor) — the path convention does not cover repository-root files that the section cites

- **Where.** fd.tex:17-20 say every path not starting with `ErdosSzekeres/`, `docs/`, `experiments/` or `scripts/` is
  relative to `cloud/es7-2026-10-19/results`; fd.tex:27 and :29 then cite `lean-toolchain` and `lake-manifest.json`,
  which are root files. Under the stated rule they would be RES-relative, where they do not exist (RES has such files
  only in subdirectories, e.g. `ENCBLEAN/`, `H/`, `H2/`, `H3/`).
- **Fix.** Add "and the files at the repository root (`lean-toolchain`, `lake-manifest.json`, `lakefile.toml`, …)" to
  the root-relative rule. It would also help later sections to say that the research-record Lean files are standalone,
  checked one by one with `lake env lean` from the repository root, and not part of the default build target (which is
  why build logs, not `lake build`, are cited for them).

### m5 (minor) — the computer-assisted label omits `decide +kernel` and names only one of the two native_decide axioms

- **Where.** fd.tex:43-46.
- **Issue.** (i) Most finite checks in the project use `decide +kernel` (kernel evaluation only, no extra axiom), e.g.
  main-library finite facts, the H3/V1-L/V2-L trees and the ES8 small checks (inventories `MAIN-LIBRARY-coverage`,
  `H3-V1L-V2L`, `ES8-small`); the main library also checks LRAT certificates inside Lean (`lrat_raw` producing Mathlib
  `Sat.fromLRAT` terms that the kernel checks). The reading convention should name these mechanisms. (ii) In Lean 4.24.0
  a `native_decide` proof depends on two axioms, `Lean.ofReduceBool` and `Lean.trustCompiler`: Init/Core.lean:2340
  declares `axiom trustCompiler : True`, `opaque reduceBool` uses it "so that `#print axioms` will track use", and
  :2392 declares `axiom ofReduceBool`. The text (like contract rule 6) names only `Lean.ofReduceBool`. No project file
  uses `native_decide`, so nothing is currently mislabelled.
- **Fix.** "kernel evaluation (Lean's `decide` or `decide +kernel`, which add no axiom), in-kernel checking of a
  certificate produced by an external program (for example an LRAT proof checked by Mathlib's `Sat.fromLRAT`), or
  compiled evaluation (`native_decide`, which adds the axioms `Lean.ofReduceBool` and `Lean.trustCompiler`)".

### m6 (minor) — axioms evidence is understated in three places (no overclaim)

- (i) fd.tex:127-133 list twelve main-library declarations as "not covered by a saved `#print axioms` output that we
  identified". Four of them are covered: `ErdosSzekeres.esNumber_three` (audit line 732, three standard axioms;
  `ErdosSzekeres/LowerBound/Number.lean:40`) uses `forces_triangle`, whose proof (Basic.lean:72-75) uses
  `forcesConvexNGon_iff_exact` and `convexPosition_of_card_three`; `forcesConvexNGon_iff_exact` uses
  `GeneralPosition.mono` and `HasConvexNGon.mono` (Basic.lean:45). Others are probably covered through the Suk/HMPT
  roots (e.g. `convex_orient_nonnegative` is used in Suk/SpikeGeometry.lean), but I did not trace them.
- (ii) fd.tex:152-157: `MirrorOdd.hasConvexNGon_of_le` "is not printed individually", with weaker evidence offered.
  It is used at MirrorMain.lean:2520 inside `MirrorOdd.mirror_odd_general` (proof from :2498), which
  `MIRRORETV/lean/MirrorMain.out` line 858 prints with the three standard axioms (the copy: ReductionThreeClasses.lean:4079,
  `SYMLEAN/mirror/axioms.out` line 11). By the section's own definition (fd.tex:36-38) that is direct evidence.
- (iii) `LayerLemma.rotAff` (a `def` with a proof field, cited for `fd:lem:rot`(b)) has no stated evidence. It is used
  at LayerLemma.lean:368 in `hullVerts_eq_orbitFS_rotAbout`, printed in `LEANEXT/review/axioms.log` line 26.
- **Fix.** Cite these lines and shorten the "not covered" list accordingly.

### m7 (minor, unsure) — the map has no rows for the seven remarks

- `fd:rem:norm`, `fd:rem:ngon`, `fd:rem:angles`, `fd:rem:affine-orient-lean`, `fd:rem:affine-cp-lean`,
  `fd:rem:pos-triples`, `fd:rem:pos-cycle` have no rows. The contract asks for "one row per statement environment" and
  lists `remark` among the environments; the maps of ll, oc, pc, ec, sr, ar, mb and cb include their remarks, those of
  lg and mm do not. I am not sure the contract counts remarks as statement environments; adding the rows (kind
  `remark`, lean_name `-` or the names they mention) removes the doubt.

### m8 (minor) — small imprecisions

- (a) fd.tex:391: "(unfold orient; ring)" describes (a) and (b); `orient_translate` is proved by
  `simp only [orient, Pi.add_apply]; ring` (Orientation.lean:20-21).
- (b) fd.tex:274: `map_mem_hullVerts` is cited with `LAYERLEAN/LayerLemma.lean:165`, the line of the `have himg` step;
  the declaration is at :162. By the section's own convention (fd.tex:21-22) a line attached to a declaration is the
  keyword line; write "the proof step at :165" or cite :162.
- (c) fd:lem:rot(d) (fd.tex:324-325) is attributed to `rotAbout_injective`, which states only injectivity; "bijection
  with inverse ρ_{−θ}" is a written step (proved from (c)). Split the attribution as was done for (c).
- (d) Two overfull hboxes (2.1pt at lines 765-766, 5.1pt at 788-789), from the long heads of `fd:lem:four-subsets` and
  `fd:lem:halfplane`. Cosmetic.
- (e) `ErdosSzekeres/Suk/Reflection.lean` is in the sources table, but its declarations `reflectY`, `reflectY_x`,
  `reflectY_y`, `reflectY_reflectY` and `hasConvexNGon_of_reflectY` are neither covered nor listed under
  "Deliberately not covered". Say that the list is restricted to the scope files, or add them.

## Summary for the fixer

Required for a pass: M1 (tag `fd:lem:affine-orient` with `SymReduction.orient_affine`, fix map, remark, Coverage,
sources table and axioms evidence). Recommended: m1 to m8, all one-line edits except m6 and m7.
