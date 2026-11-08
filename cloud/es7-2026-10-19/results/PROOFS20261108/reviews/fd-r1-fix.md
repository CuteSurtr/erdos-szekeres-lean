# fd, round 1: fixer changelog

Files: `sections/fd.tex` and `sections/fd.map.tsv`.

Compile: `build/fd_wrapper.tex`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`, run twice.
- Both passes exit 0. The PDF has 15 pages.
- No errors, no "Missing $", no overfull boxes (before the fix there were two).
- Undefined references are only the export labels `ll:def:hv`, `ll:def:peel`, `ll:def:66-70`, `oc:lem:rot-inv` and
  `oc:lem:perm`. `oc:lem:perm` is newly referenced.
- No non-ASCII characters, machine paths or tool names.
- All 20 contract labels are defined once each, on the named statements.

## Major findings (all fixed)

Two verifiers (fidelity F1, claims M1) report one issue: Lean counterparts exist for `fd:lem:affine-orient` and
`fd:lem:affine-cp`, but the section said they did not. I checked this against the source and the evidence:
- `SYMLEAN/AffineReduction.lean:1241`, `orient_affine` (namespace `ErdosSzekeres.SymReduction`, opened at :54).
  Its hypothesis is `hg : ∀ p, g p = L *ᵥ p + b`; its conclusion is `orient (g x) (g y) (g z) = L.det * orient x y z`.
  This is exactly fd:lem:affine-orient.
- The other declarations are at `:1263` `convexPosition_image_affine`, `:1278` `generalPosition_image_affine`,
  `:1290` `generalPosition_image_affineEquiv`, `:1298` `hasConvexNGon_image_affine` and `:1305` `injective_of_affine`.
- `orient_affine` is copied verbatim at `SYMLEAN/mirror/ReductionThreeClasses.lean:1267` (diff empty).
- SHA-256 of `AffineReduction.lean` is `41cfc0b60aec…`.
- `SYMLEAN/logs/runs.tsv`: line 4 records AffineReduction.lean (`41cfc0b6`) with exit 0 and no output; line 5 records
  AffineReductionAxioms.lean with exit 0. AffineReductionAxioms.lean is AffineReduction.lean plus 10 appended
  `#print`/`#check` lines (diff checked).
- `SYMLEAN/logs/AffineReductionAxioms.out` prints three theorems with the three standard axioms:
  - lines 9–11, `heptagon_of_nontrivial_affine_coords`. It uses `injective_of_affine` through
    `hasConvexNGon_of_affine_coords_symmetry` (:1528, :1462).
  - lines 13–15, `generalPosition_image_affineEquiv`. It uses `generalPosition_image_affine` (:1295), which uses
    `orient_affine` (:1281).
  - line 16, `hasConvexNGon_image_affine`. It uses `convexPosition_image_affine` (:1303).

Changes:
- **fd:lem:affine-orient**
  - The head is now `\leanref{ErdosSzekeres.SymReduction.orient_affine}{SYMLEAN/AffineReduction.lean:1241}; (i), (ii)
    written step`.
  - The statement now reads "g is a map with g(x)=Ax+v for every x", matching Lean's hypothesis `hg`.
  - A sentence gives the Lean form (L=A, b=v), and the proof says how the Lean proof works.
- **fd:rem:affine-orient-lean** is rewritten. It names `orient_affine` and its verbatim copy. It says Lean proves (i)
  (`OrbitConsistency.orient_rotAbout_inv`, stated exactly) and the case o=0, φ=0 of (ii) (`Suk.orient_reflectY`). The
  false sentence "Lean proves the special cases it needs separately" is gone.
- **fd:lem:affine-cp**
  - The contract content (a)–(d) is unchanged.
  - The head names Mathlib `AffineMap.image_convexHull` for (a), plus five `\leanref`s for (b′)–(e′), and "the rest
    written step".
  - New items (b′)–(e′) inside the statement give the exact Lean forms:
    - (b′) `convexPosition_image_affine`, for an injective Mathlib affine map f.
    - (c′) `generalPosition_image_affine` (h(p)=Lp+b with det L≠0) and `generalPosition_image_affineEquiv` (AffineEquiv).
    - (d′) `hasConvexNGon_image_affine`.
    - (e′) `injective_of_affine`.
  - The proof now proves (b′)–(e′). For (e′) it uses the adjugate identity L♯L=(det L)I, which is new and complete.
    It also says which Lean proofs follow which route, and cites `affineMap_eq_mulVec` (:1284).
- **fd:rem:affine-cp-lean** is rewritten to list the main-library special cases: `HasConvexNGon.linearEquiv`,
  `Suk.reflectY` with its simp lemmas, `Suk.generalPosition_reflectY` (forward direction of (c)) and
  `Suk.hasConvexNGon_of_reflectY` (reverse direction of (d) for the reflection).
- **fd:lem:orient(d)**: a new remark **fd:rem:orient-lean** shows that `OrbitConsistency.orient3_perm`
  (`LEANEXT/orbit/OrbitConsistency.lean:178`, `\ref{oc:lem:perm}`) is the case R=ℝ, with the index translation
  t(i)=p_{i+1}, σ(i)=π(i+1)−1. The remark proves that σ = s⁻¹πs, so σ and π have the same sign. The head of
  fd:lem:orient still says "(d), (e) written step", because (d) is stated over any commutative ring, which is more
  general than Lean.
- **Coverage** is rewritten.
  - "Covered" now includes `orient_affine` and the five transport theorems.
  - The old sentence "Written steps without a single Lean counterpart" is replaced by an accurate list of written steps
    and parts, each pointing to the remark that names its Lean special or partial counterpart.
  - The list of declarations named only in remarks or proofs is completed.
- **Source table**: added `SYMLEAN/AffineReduction.lean`, `41cfc0b60aec`.
- **Axioms evidence**: added the runs.tsv and AffineReductionAxioms.out evidence above, and line 5 of
  `LEANEXT/orbit/logs/axioms.log` (`orient3_perm`).
- **Map**:
  - fd:lem:affine-orient now has `ErdosSzekeres.SymReduction.orient_affine` at `SYMLEAN/AffineReduction.lean:1241`.
  - fd:lem:affine-cp now lists the five declarations and their lines.

## Minor findings

- **Rotations (F2, M3, m6, m8c)**: fixed.
  - (b): stated the exact `rotAff` property ρ(p+v)=ρ(p)+R_θ v and proved it. A parenthesis says ρ(c)=c is a written
    step, proved in Lean in the step at :330 of `invariant_erase_centre` (:325).
  - (c): ρ_0=id is now also marked as a written step.
  - (d): a parenthesis says Lean states injectivity only.
- **Paths, keywords, namespaces (F3, F4, F5, M1, M2, m3, m4)**: fixed.
  - `lean-toolchain`, `lake-manifest.json` and `lakefile.toml` are now root-relative. Checked: they are absent from RES
    and present at the repository root.
  - The keyword list now reads theorem/lemma/def/abbrev/structure/inductive, possibly preceded by an attribute or by
    noncomputable/private. Checked mechanically on all 588 cited lines of all section maps: the keywords found are
    theorem, def, noncomputable def, structure, lemma, abbrev and inductive.
  - Names outside `ErdosSzekeres` (for example `MirrorOdd`) are always written in full.
  - Research Lean files are checked separately, as in `LAYERLEAN/logs/build.log`.
  - A section may use a bare file name after the full path has been given.
- **Evidence understated (F6, M7, M8, m2, m6)**: fixed. Each use was traced in the current source. All files involved
  are unchanged since the audit commit `7f0868fdb` (`git diff` is empty). Audit lines and the declarations they cover:
  - line 725 covers `ForcesConvexNGon.mono` (Construction.lean:118).
  - line 732 (`esNumber_three`, via `forces_triangle`, Basic.lean:73, :75, :45) covers `forcesConvexNGon_iff_exact`,
    `convexPosition_of_card_three`, `GeneralPosition.mono` and `HasConvexNGon.mono`.
  - line 720 (Construction.lean:54, then Placement.lean:20) covers `orient_translate`.
  - line 624 (OrientationObstructions.lean:64, :68) covers `orient_swap` and `orient_cycle`.
  - line 132 (SpikeChain.lean:140) covers `ConvexPosition.hasConvexNGon`.
  - line 49 (VisibleEdgeInsertion.lean:77) covers `convex_orient_nonnegative`.
  - line 178 (FiniteDensityBound.lean:66) covers `hasConvexNGon_of_reflectY`.
  - line 88 covers `ConvexCycleCut`, and the definitions occur in the statements of the printed theorems.

  Other evidence:
  - Only `HasConvexNGon.card_le`, `convexPosition_of_negative_triples` and the rfl/simp lemmas `reflectY_x`, `_y` and
    `_reflectY` remain without a printed line. For them the section now names the build record
    `docs/VALIDATION.md:73` (lake build --wfail on 11 Oct), plus a text search of the full import closure, which is
    clean.
  - `MirrorOdd.hasConvexNGon_of_le` is covered by `MIRRORETV/lean/MirrorMain.out` line 858 (use at
    MirrorMain.lean:2520), and its copy by `SYMLEAN/mirror/axioms.out` line 11 (use at :4079).
  - `rotAff` is covered by `LEANEXT/review/axioms.log` line 26 (use at LayerLemma.lean:368).
- **SAT vs SMT (F7, m3)**: fixed. The text now reads "used as cuts in the SMT coordinate-repair searches described in
  `docs/SAT.md:168`–`233`". `docs/SAT.md` names the solver in that passage. The section does not name it, to keep tool
  names out of the output.
- **Map (F8, M9, m5, m7)**: fixed.
  - Rows were added for all 8 remarks: the 7 old ones and the new fd:rem:orient-lean. The 40 rows match the 40
    statement environments in label, kind and order (checked by script).
  - The lean_name column now holds only bare names, or `-`. Part annotations and Mathlib names have moved to the note
    column.
  - All 49 `\leanref`s and all map name/line pairs were checked by script against the declaration lines: 0 mismatches.
- **Reflection.lean coverage (F9, M10, m8e)**: fixed. All 8 declarations of the file are now named in
  fd:rem:affine-cp-lean or listed in Coverage. Coverage also says that for the research files only the declarations
  named here are in scope.
- **Computer-assisted label (M4, m8 adv., m5 claims)**: fixed.
  - The label is now defined by the written proof.
  - The definition mentions `decide`/`decide +kernel` (no extra axiom), the kernel replay of external certificates
    (LRAT), and `native_decide`.
  - `native_decide` now adds both `Lean.ofReduceBool` and `Lean.trustCompiler`. This was checked in the Lean 4.24.0
    sources: `Init/Core.lean:2340` declares `axiom trustCompiler`, `reduceBool` uses it, and :2392 declares
    `axiom ofReduceBool`.
  - fd:rem:pos-triples(ii) was reworded to match.
- **Which parts are Lean-checked (m7 adv.)**: added the rule. A head naming "Lean: name, file:line" is Lean-checked; a
  part marked "written step" is not; a Mathlib name in a head only identifies the Mathlib counterpart.
- **Purpose paragraph (m1 claims)**: added the exception for computer-assisted statements.
- **Heine–Borel and extreme value theorem (M5)**: these are now cited precisely, as Rudin, PMA 3rd ed., Thms 2.41 and
  4.16. fd:rem:norm now says that compactness is used in R^m.
- **Base case of the iterate identity (M6)**: added f^[1]=f∘f^[0].
- **Lean tactic wording (m8a)**: (a), (b) use `unfold orient; ring`; (c) uses `simp only [orient, Pi.add_apply]; ring`.
- **map_mem_hullVerts line (m8b)**: now cited as "the step at line 165 of the proof of map_mem_hullVerts,
  LayerLemma.lean:162".
- **Overfull boxes (M13, m9, m8d)**: fixed. amsthm builds theorem heads in an hbox (`\sbox\@labels`), so url's math-mode
  break penalties never appear in heads. The three lemmas with long heads (affine-cp, four-subsets, halfplane) now use
  `\raggedright` inside the environment, and the Coverage paragraph is in a `\sloppy` group. The result has 0 overfull
  boxes.
- **Export list (M12, informational)**: no change. See concerns.

## Concerns for the orchestrator

- **Contract statements.** All fd contract statements were checked again: they are true and match their Lean
  declarations. fd:lem:affine-orient now carries its exact Lean counterpart. For fd:lem:affine-cp, only the forward
  directions and the converse (e′) are in Lean. Its contract wording ("preserves and reflects …") is kept, and the
  Lean forms appear as (b′)–(e′).
- **Contract rule 6** says that native_decide adds only `Lean.ofReduceBool`. In Lean 4.24.0 it also adds
  `Lean.trustCompiler`, which `#print axioms` reports. fd now names both. Sections that copy rule 6 word for word
  might be updated the same way. No project file uses native_decide.
- **Export list (rigor M12, informational).** fd:lem:rot, fd:lem:small, fd:lem:hull and others are proved here but are
  not export labels. The orchestrator may add them, for example fd:lem:rot and fd:lem:small.
- **New label.** fd now `\ref`s `oc:lem:perm`, which is an export label of oc. The new local label is
  `fd:rem:orient-lean`.
