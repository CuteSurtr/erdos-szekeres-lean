# Review fd, round 2, lens: fidelity

Section: `sections/fd.tex` (1189 lines, modified 17:01), map `sections/fd.map.tsv` (40 rows plus header).
Lean sources read: `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry,Basic,ConvexCycleCuts}.lean`,
`ErdosSzekeres/Suk/{FourPoint,SupportingLines,OrientationClique,Reflection}.lean`, `LAYERLEAN/LayerLemma.lean`,
`SYMLEAN/SymmetricReduction.lean`, `SYMLEAN/AffineReduction.lean`, `LEANEXT/orbit/OrbitConsistency.lean`,
`MIRRORETV/lean/MirrorMain.lean` and `SYMLEAN/mirror/ReductionThreeClasses.lean`. Mathlib definitions were read from a
local Mathlib checkout at the pinned revision (`git rev-parse HEAD` = `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`).

**Verdict: PASS.** No blocker or major finding; 7 minor findings.
- Every Lean-tagged statement and definition matches its declaration exactly: hypotheses, conclusion, quantifier
  order, Finset vs Set, strict vs weak inequalities, maps-into vs equality, and casts.
- All 49 `\leanref`s name a declaration at exactly the cited line.
- All 20 contract `fd:` statements are true. Each is defined exactly once, on the statement named for it, in the
  contract's order.
- Both round-1 major findings are fixed.

## 1. Round-1 major findings: checked

| round-1 finding | status | evidence |
|---|---|---|
| [fidelity, major] The Lean counterparts of `fd:lem:affine-orient`, of the forward directions of `fd:lem:affine-cp` and of `fd:lem:orient`(d) over ℝ were not tagged; a remark and Coverage said none exist | **fixed** | **affine-orient.** The head is now `\leanref{ErdosSzekeres.SymReduction.orient_affine}{SYMLEAN/AffineReduction.lean:1241}` (fd.tex:504). The statement now uses "a map with g(x)=Ax+v for every x", which is Lean's hypothesis `hg : ∀ p, g p = L *ᵥ p + b`, and the conclusion `orient (g x) (g y) (g z) = L.det * orient x y z` matches. **affine-cp.** New items (b′)–(e′) (fd.tex:777-789) state the Lean forms exactly. They match :1263 (injective `Point →ᵃ[ℝ] Point`), :1278 (hg, `L.det ≠ 0`), :1290 (`Point ≃ᵃ[ℝ] Point`), :1298 and :1305. **orient(d).** New Remark `fd:rem:orient-lean` (fd.tex:489-502) states `orient3_perm` (OrbitConsistency.lean:178) correctly; the index translation σ = s⁻¹πs was checked. **Wording.** The false sentences are gone: grep finds neither "special cases it needs" nor "single Lean counterpart". Coverage (fd.tex:1149-1170) is rewritten. |
| [claims, major] `fd:lem:affine-orient` was tagged "written step" although it is exactly `SymReduction.orient_affine` | **fixed** | As above. Map row 18 now reads `ErdosSzekeres.SymReduction.orient_affine`, `SYMLEAN/AffineReduction.lean:1241`. The verbatim copy at `SYMLEAN/mirror/ReductionThreeClasses.lean:1267` is identical, and its namespace `ErdosSzekeres.SymReduction` opens at :80. |

## 2. Method (fresh full pass)

**Contract and inventories.**
- Read the contract and both inventories (`MAIN-LIBRARY-coverage.json`, `LAYERLEAN.json`), including their risks.
- Then read the whole section and map.

**Mechanical checks** (short scripts; scratch files only):
- **leanrefs.** Each of the 49 `\leanref{name}{file:line}` resolves under the section's path convention. In every
  case, the cited line carries the declaration keyword followed by the declaration's short name. Result: 0 mismatches.
- **Namespaces.** Each full name was checked against the `namespace` blocks of its file: `ErdosSzekeres`,
  `ErdosSzekeres.Suk` (including the nested `namespace Suk` in Reflection.lean), `ErdosSzekeres.LayerLemma`,
  `ErdosSzekeres.SymReduction` (AffineReduction.lean :54-1533), `ErdosSzekeres.OrbitConsistency` and the top-level
  `MirrorOdd` (MirrorMain.lean :12-2660). There are no nested namespaces before the cited lines. No research file
  redefines `Point`, `HasConvexNGon`, `ConvexPosition` or `GeneralPosition` locally.
- **Map against environments.** The 40 statement environments and the 40 map rows agree in label, kind and order.
  - All rows have 5 columns.
  - For every statement with a Lean tag, the map's `lean_name`/`file_line` equal the head's `\leanref`s.
  - The 4 remark rows list the declarations named in the remark bodies, and their lines are right.
- **Lines cited in running text.** Every `\dirn{file:N}` the section cites, 42 in all, was printed and checked against
  its claim (uses of lemmas inside proofs, evidence lines). The "line~N" citations into logs and into proofs (audit
  lines, `axioms.log` lines, LayerLemma.lean lines 165 and 330) were checked separately.
- **Cross-section references.** The section refers outside itself only to `ll:def:hv`, `ll:def:peel`, `ll:def:66-70`,
  `oc:lem:perm` and `oc:lem:rot-inv`. All five are contract export labels and are defined in ll.tex and oc.tex on the
  right environments. Every `fd:` label that other sections reference is defined here and is a contract export.
- **Source hashes.** All 15 SHA-256 prefixes in the source table were recomputed. All match.
- **Pins and paths.**
  - The commit `7e32ee259` (HEAD, branch `es7-night-2026-11-01`), `lean-toolchain` (= `leanprover/lean4:v4.24.0`), the
    Mathlib rev in `lake-manifest.json`, `lakefile.toml` (`defaultTargets = ["ErdosSzekeres"]`, package
    `erdos_szekeres`) are all correct.
  - `lean-toolchain` and `lake-manifest.json` are absent from RES and present at the repository root.
  - Every toolchain file inside RES also pins v4.24.0.
- **The section's path convention, applied to all section files.** Every cited path resolves, except bare file names
  used after the full path and directory mentions. Both are allowed by the convention.
- **Line-number keyword convention, applied to all 634 `\leanref` lines of all sections.** The keywords found are
  theorem, def, noncomputable def, structure, abbrev, lemma and inductive, all of which the convention covers.
- **Compile.** A private wrapper in my own scratch directory, compiled twice with
  `nice -n 15 pdflatex -halt-on-error`, exits 0 both times. The PDF has 15 pages and there are 0 overfull boxes. The
  only undefined references are the 5 export labels above.
- **Hygiene.** There are no non-ASCII characters, no machine paths and no tool names. Grep finds no
  overclaiming vocabulary.
- **sympy 1.13.3.** The following were checked: the orient_affine identity for a general 2×2 matrix; the adjugate
  identity L♯L = (det L)I used for (e′); F_φu = u, F_φu⊥ = −u⊥ and det F_φ = −1; the invariance of orient under
  rotation; and that σ(i) = π(i+1)−1 has the same sign as π for all 6 permutations. All pass.

**Evidence, line by line.**
- Audit `docs/validation/axiom-audit-lower-bound-2026-10-11.txt`, lines 49, 87, 88, 103, 113, 114, 119, 132, 175, 176,
  178, 624, 720, 725 and 732 print what the section says they print.
- Every traced use site lies inside the claimed enclosing theorem: Construction.lean:118 inside :115, :54 inside :35;
  Placement.lean:20 inside :18; Number.lean:40-41; Basic.lean:73, :75, :45; OrientationObstructions.lean:64 and :68
  inside :55, in `namespace Omission.Configuration` (:48); SpikeChain.lean:140 inside :120; VisibleEdgeInsertion.lean:77
  inside :59; FiniteDensityBound.lean:66 inside :36; Reflection.lean:55.
- `git diff --stat 7f0868fdb HEAD` over all 16 main-library files the paragraph names is empty.
- `docs/VALIDATION.md:73` is the `--wfail` build record under the heading of 11 October 2026.
- The computed import closure of Basic, OrientationClique and Reflection is exactly the files the section lists.
- Grep for sorry, admit, native_decide and `axiom` declarations is clean in all 9 main-library table files, in their
  imports (including the 4 Vendor files) and in the 6 research files.
- `LEANEXT/review/axioms.log` lines 1, 22, 23, 26 and 33 are right. That review is of `LayerLemma.lean` with SHA
  `afb8542d`, the current file.
- `LayerLemma.lean:368` uses `rotAff`.
- `SYMLEAN/logs/runs.tsv` lines 2, 4 and 5 are right: the hashes are `6d5ec90a`, `41cfc0b6` and `f6cb9372`, all current.
- `AffineReductionAxioms.lean` is byte-identical to `AffineReduction.lean` for its first 1533 lines (cmp).
- `AffineReductionAxioms.out` lines 9-11, 13-15 and 16 are right. The use sites :1528→:1462, :1295→:1281 and :1303 are
  right.
- `LEANEXT/orbit/logs/axioms.log` lines 1 and 5 are right, and `build.log` reads `exit=0`.
- `MirrorMain.out` line 858 is `mirror_odd_general`; the file has 0 occurrences of "error", and the use is at
  MirrorMain.lean:2520.
- `SYMLEAN/mirror/axioms.out` line 11 is right; the use is at ReductionThreeClasses.lean:4079. The README there records
  exit 0 with no errors.

**Mathlib definitions at the pin.**
- `ConvexIndependent` (Independent.lean:53): `∀ s x, p x ∈ convexHull 𝕜 (p '' s) → x ∈ s`.
- `convexIndependent_set_iff_notMem_convexHull_diff` (:145): `ConvexIndependent 𝕜 ((↑) : s → E) ↔ ∀ x ∈ s, x ∉
  convexHull 𝕜 (s \ {x})`.
- `Collinear` (AffineSpace/FiniteDimensional.lean:366): `Module.rank k (vectorSpan k s) ≤ 1`.
- `vectorSpan`: `span (s -ᵥ s)`.
- `collinear_iff_of_mem` (:420).
- `AffineIndependent` (Independent.lean:46).
- `convexHull`: `.ofCompletePred (Convex 𝕜)`.
- `AffineMap.image_convexHull` (Hull.lean:193). Its proof is the one the section describes: the preimage of a convex
  set is convex, and so is the image.

The section restates each of these faithfully.

## 3. Statement-by-statement fidelity

| label | Lean (file:line) | result |
|---|---|---|
| fd:def:point | `Point` Definitions.lean:9 | exact (`abbrev Point := Fin 2 → ℝ`); Finset/Set convention correct |
| fd:def:orient | `orient` Orientation.lean:9 | exact, any `CommRing`; use over ℚ (Orientation.lean:23-35) and ℤ (IntegerCertificates.lean:15-25) confirmed |
| fd:def:conv | Mathlib only | faithful (see above) |
| fd:def:gp | `GeneralPosition` :12 | exact (pairwise distinct; `¬ Collinear ℝ ({a,b,c} : Set Point)`) |
| fd:def:cp | `ConvexPosition` :17 | exact (subtype inclusion; Mathlib definition quoted correctly) |
| fd:def:ngon | `HasConvexNGon` :21 | exact (`t ⊆ s ∧ t.card = n ∧ ConvexPosition t`; exact cardinality) |
| fd:def:forces | `ForcesConvexNGon` :25 | exact (`GeneralPosition s → N ≤ s.card → …`) |
| fd:def:inv | `Invariant` LayerLemma:105, SymmetricReduction:271, OrbitConsistency:47 | exact (maps into); three textually identical |
| fd:lem:inv-image | (c) `LayerLemma.iterate_mem` :52 | conclusion exact; stated for ℝ² while Lean has an arbitrary type, disclosed in the text (see m4) |
| fd:def:rot | `rotAbout` LayerLemma:298, SymmetricReduction:400, OrbitConsistency:93 | exact; 19 definitions in RES, all with this body (re-counted) |
| fd:rem:angles | `Sixfold66`/`Sevenfold70` :1102/:1107 | correct (`2 * Real.pi / 6`, `/ 7`, real numerals) |
| fd:lem:rot | :302, :311, :465, :319 | (a) Lean form quoted exactly (`crot (toC c) (Complex.exp (θ * I))`; `crot` :252, `toC` :231); (b) `rotAff` linear part `!![cos, −sin; sin, cos]`, `map_vadd'`; (c) `(j:ℝ) * α`; (d) injectivity only, with the extra content marked written step; ρ(c)=c traced to :330 of `invariant_erase_centre` (:325) |
| fd:lem:orient | (a)-(c) Orientation.lean:12, :15, :18 | exact, any `CommRing`; (d), (e) written steps |
| fd:rem:orient-lean | `orient3_perm` :178, `orient3` :168 | exact (`∀ t, orient3 (t ∘ σ) = ((sign σ : ℤ) : ℝ) * orient3 t`) |
| fd:lem:affine-orient | `SymReduction.orient_affine` AffineReduction:1241 | exact |
| fd:rem:affine-orient-lean | copy :1267; `orient_rotAbout_inv` :117; `Suk.orient_reflectY` Reflection:47 | exact |
| fd:lem:collinear-mem | Mathlib `collinear_iff_of_mem` | exact (`p = r • v +ᵥ p₀`) |
| fd:lem:collinear | OrientationGeometry:36, :66 | exact; proof follows the Lean proof, including the private helper's case split |
| fd:lem:cp-hull | `convexPosition_iff` Basic:15 | exact |
| fd:lem:mono | Basic:11, :6, :20; `MirrorOdd.hasConvexNGon_of_le` MirrorMain:2182 | exact (renaming m→n, n→n′); copy at ReductionThreeClasses:3741 identical |
| fd:lem:ngon-basic | Basic:25, :31 | exact |
| fd:lem:forces-basic | Basic:47, :37 | exact (`N ≤ M`; `s.card = N`) |
| fd:lem:small | last assertion `convexPosition_of_card_three` Basic:58 | exact; rest marked written step |
| fd:lem:affine-cp | (b′) :1263, (c′) :1278 and :1290, (d′) :1298, (e′) :1305 | (b′)–(e′) exact; (a) and (b)–(d) in both directions are written steps with full proofs |
| fd:rem:affine-cp-lean | Reflection:6, :34, :42, :43, :44, :52, :64 | exact (but see m1 for the Coverage sentence) |
| fd:lem:four-subsets | FourPoint:10, :40 | exact (`t.card ≤ 4`; `4 ≤ s.card`, `t.card = 4`) |
| fd:lem:halfplane | SupportingLines:6, :11, :21 | exact; certificate `(p1 q0 − p0 q1)(u+v−1)` matches `linear_combination` |
| fd:lem:strict-supports | :28 | exact (∀p ∃q ∀r ≠ p, 0 < orient p q r) |
| fd:lem:support-sum | :40 | exact |
| fd:lem:four-positive | :47 | exact; the four q's match `a+b−d`, `b+c−a`, `c+d−b`, `d+a−c` |
| fd:lem:pos-triples | OrientationClique:9 | exact (linear order; p injective on all of ι; `4 ≤ s.card`; strict) |
| fd:lem:neg-triples | :33 | exact (`< 0`; reversed order `ιᵒᵈ`) |
| fd:lem:pos-cycle | ConvexCycleCuts:11 | exact (all increasing triples; `Fin k ↪ Fin N`; `∀ i, p (e i) ∈ P`) |
| fd:rem:pos-cycle | :8, :31 | exact (≤ 0 in `ConvexCycleCut`); `docs/SAT.md:168-233` describes these cuts |

**Contract check.** Every contract `fd:` statement is true and matches its Lean declaration where one is named. There
is no discrepancy to report to the orchestrator.

**Coverage check.** All declarations of the 9 main-library files in the source table were enumerated. Each is
covered, named in a remark, or listed under "Deliberately not covered" with a reason. The in-scope items the
inventories mark headline or supporting are covered: `Suk.convexPosition_of_positive_triples`,
`hasConvexNGon_of_positive_cycle`, `generalPosition_iff_orient_ne_zero`, `rotAbout_iterate`, `rotAff`, `Invariant`,
`rotAbout`, and the core definitions. The remaining inventory items (`esNumber`, Suk, HMPT, Omission, LowerBound) lie
outside the contract's fd list.

## 4. Findings (all minor)

### m1 (minor): Coverage files forward-direction special cases under the reverse directions of `fd:lem:affine-cp`

- **Where.** fd.tex:1159-1163: "…and the reverse directions of (b)--(d) (Lean special cases
  `HasConvexNGon.linearEquiv`, `Suk.generalPosition_reflectY` and `Suk.hasConvexNGon_of_reflectY`, Remark
  fd:rem:affine-cp-lean)".
- **Evidence.** The remark itself classifies these differently (fd.tex:850-861, matching the Lean statements):
  - `linearEquiv` is "the forward direction of (d) for g=e": Reflection.lean:6, `HasConvexNGon n S →
    HasConvexNGon n (S.image e)`.
  - `generalPosition_reflectY` is "the forward direction of (c) for g=σ": :52.
  - Only `hasConvexNGon_of_reflectY` is "the reverse direction of (d) for g=σ": :64.
- **Why it is wrong.** The first two give reverse directions only after a further step: applying them to `e.symm`, or
  using σ∘σ = id. The section does not say so.
- **Fix.** For example: "the reverse directions of (b)–(d) (Lean special case `Suk.hasConvexNGon_of_reflectY`; the
  forward-direction special cases `HasConvexNGon.linearEquiv` and `Suk.generalPosition_reflectY` are in Remark
  fd:rem:affine-cp-lean)".

### m2 (minor): the Coverage scope sentence is imprecise about research declarations named only as evidence

- **Where.** fd.tex:1185-1187: "Of the research files in the table, only the declarations named in this section belong
  to its scope".
- **Evidence.** The axioms-evidence paragraph names research declarations that are outside fd's scope. They appear in
  neither the "Covered" list nor the "named only in remarks or in proofs" list:
  - `LayerLemma.hullVerts_eq_orbitFS_rotAbout` (fd.tex:191)
  - `SymReduction.heptagon_of_nontrivial_affine_coords` (:200)
  - `SymReduction.hasConvexNGon_of_affine_coords_symmetry` (:202)
  - `MirrorOdd.mirror_odd_general` (:215)
- **Fix.** Say "only the declarations named in statement heads, remarks or proofs of this section", or add "(the
  theorems cited in the axioms-evidence paragraph only as evidence belong to other sections)".

### m3 (minor, informational): the definition of "Lean-checked" excludes native_decide-based theorems

- **Where.** fd.tex:46-48 define Lean-checked as "using no axioms other than the three standard axioms". fd.tex:59-61
  say that `native_decide` adds `Lean.ofReduceBool` and `Lean.trustCompiler`.
- **Conflict with the contract.** Contract rule 6 contemplates Lean theorems proved with `native_decide`, which are
  labelled computer-assisted. Rule 8 says the Lean theorems "keep their label Lean-checked". Under fd's definition such
  a theorem could never be Lean-checked.
- **No current effect.** No Stage-1 section has such a theorem. The evidence paragraphs of the other sections each
  state that there is no native_decide, and `C3LEAN/C3Cover.lean` uses `decide +kernel`.
- **Future effect.** The research records do contain native_decide files (`V1-L/V1L/Cover.lean`,
  `V2-L/V2L/Facts.lean`, `H/ETVEncoding/*.lean`, `ENCBLEAN/EncB/{Gen,KernelCheck}.lean`), which later stages may cite.
  The fixer's note "No project file uses native_decide" (r1-fix concerns) is therefore inaccurate for RES. It is
  accurate for the files of Stage 1.
- **Fix (optional).** Add "…or, for a statement whose Lean proof uses `native_decide`, additionally the axioms
  `Lean.ofReduceBool` and `Lean.trustCompiler`, which the section then names".

### m4 (minor): `fd:lem:inv-image`(c) specialises a Lean theorem stated for an arbitrary type

- **Where.** fd.tex:323-331.
- **What happens.** The head tags (c) with `LayerLemma.iterate_mem`. Its statement is for ℝ², whereas Lean is
  `{α : Type*} {f : α → α} {S : Finset α}` (LayerLemma.lean:52).
- **Why it is only minor.** The text discloses this ("In Lean, (c) is stated for an arbitrary type … the proof below
  works verbatim in that generality"), so the weakening is not silent. Strictly, contract rule 4 asks for the exact
  Lean statement, or a variant labelled as such.
- **Fix.** State (c) for an arbitrary set X and a finite S ⊆ X, since nothing in the proof uses ℝ². Alternatively,
  call the ℝ² form the case X = ℝ² of the Lean statement.

### m5 (nit): the description of `AffineReductionAxioms.lean` omits one `#check`

- **Where.** fd.tex:197-198 say that `AffineReductionAxioms.lean` is `AffineReduction.lean` "followed by #print axioms
  commands".
- **Evidence.** The appended block (lines 1534-1544) is nine `#print axioms` lines and one `#check` line. The first
  1533 lines are byte-identical (cmp).
- **Fix.** "followed by `#print axioms` commands and one `#check`".

### m6 (nit): two map notes are incomplete

- **Row `fd:lem:rot`.** The written-step list omits "ρ_0 = id in (c)", which fd.tex:391-392 mark as a written step.
- **Row `fd:lem:pos-triples`.** The note says "Lean uses decide only for Fin 4 order facts". `decide` also proves
  `Finset.univ = {0,1,2,3}` in `Fin 4` (OrientationClique.lean:23), as Remark `fd:rem:pos-triples`(ii) correctly says.

### m7 (nit): the Coverage reason for `conjecturedBound` is imprecise

- **Where.** fd.tex:1173-1175 list `conjecturedBound`, `ErdosSzekeresConjecture` and `HeptagonConjecture` as
  "statements of open conjectures".
- **Evidence.** `conjecturedBound` (Definitions.lean:28) is the numeric function n ↦ 2^(n−2)+1, which uses truncated
  natural subtraction. It is not a conjecture.
- **Fix.** "the bound function `conjecturedBound` and the open conjectures `ErdosSzekeresConjecture`,
  `HeptagonConjecture`". No other Stage-1 section uses `conjecturedBound` (grep), so no convention is needed for it.

## 5. Checked and found correct (no action)

- **Purpose paragraph.** It says that the Lean checks are the primary evidence and that the proofs are not refereed,
  and it gives the exception for computations.
- **Conventions.**
  - Paths relative to RES or to the repository root, including the root files.
  - The commit, branch and package.
  - Lean 4.24.0 and Mathlib `f897ebcf…`.
  - The three rigor labels. The rule that only head-tagged parts count as Lean-checked.
  - Explicit `(m:ℝ)` casts, `x/0 = 0`, truncated subtraction written as max(a−b,0) or with b ≤ a.
  - The iterate order `f^[n+1] = f^[n] ∘ f`, and `minimalPeriod` (0 if aperiodic).
  - Bare file names after a full path. The namespace rule for `MirrorOdd`.
- **Written proofs that claim to follow Lean.** These do follow the Lean proofs: collinear, mono, ngon-basic,
  forces-basic, four-subsets, strict-supports, four-positive, pos-triples, neg-triples and pos-cycle.
- **Lean proof descriptions.** The descriptions of the Lean proofs (tactics, certificates, Mathlib lemmas used) are
  accurate, including:
  - `unfold orient; ring`
  - `simp only [orient, Pi.add_apply]; ring`
  - the `linear_combination` certificate
  - `ConvexIndependent.mono`
  - `affineIndependent_iff_not_collinear_set` with `convexIndependent_of_affineIndependent`
  - Carathéodory via `minCardFinsetOfMemConvexHull` and `card_le_finrank_succ`
  - `rotAbout_eq_crot` / `crot_iterate` / `crot_injective` for (c) and (d)
- **Coverage lists.** "Deliberately not covered" is complete for the main-library files of the table, including
  the private `exists_smul_of_det_zero`. `convexIndependent_of_affineIndependent` is used only in
  `convexPosition_of_card_three` (grep).
