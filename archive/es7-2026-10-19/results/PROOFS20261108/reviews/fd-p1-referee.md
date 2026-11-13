# Referee report: section `fd`, polish round 1 (independent full read)

Files: `sections/fd.tex` (1241 lines) and `sections/fd.map.tsv` (header + 40 rows), read in full. Lean sources: every
declaration named in a head, remark, proof or the axioms paragraph, read at the cited lines in the repository checkout
(commit `7e32ee259`, branch `es7-night-2026-11-01`, worktree clean). I formed my view before reading
`reviews/fd-r1-*`, `fd-r2-*` and `fd-polish-r1-fix.md`.

**Verdict: PASS.** No blocker and no major finding. One minor finding (m1). Two notes need no action.

## 1. What was checked

**Fidelity to Lean.** I compared every statement head with its source, one hypothesis at a time.
- **Definitions.** `Definitions.lean:9-26`: `Point`, `GeneralPosition`, `ConvexPosition` (Mathlib `ConvexIndependent` of
  the subtype inclusion), `HasConvexNGon` and `ForcesConvexNGon` (`N ≤ card`). Also `Orientation.lean:9` (any
  `CommRing`) and the three `Invariant` copies (maps into, textually identical).
- **Rotations and invariance.** The three `rotAbout` copies (19 copies in the research records, all with the same
  body), `iterate_mem` (arbitrary type, `DecidableEq` omitted), `rotAbout_eq_crot`, `rotAff` (its `map_vadd'`
  obligation), `rotAbout_iterate` (with the cast `(j:ℝ)`) and `rotAbout_injective`.
- **Orientation.** `orient_swap`, `orient_cycle`, `orient_translate`, `SymReduction.orient_affine` (`hg` precedes
  `x y z`), `OrbitConsistency.orient_rotAbout_inv`, `orient3`, `orient3_perm` (sign cast ℤ→ℝ),
  `orient_eq_zero_iff_collinear` and `generalPosition_iff_orient_ne_zero`.
- **Basic.lean.** Every theorem.
- **Affine maps.** The five `SymReduction` affine theorems at `AffineReduction.lean:1263/1278/1290/1298/1305`:
  `AffineMap` versus a map with `g p = L *ᵥ p + b`, `det ≠ 0`, `AffineEquiv`.
- **Suk files.** `FourPoint`, `SupportingLines` (all six), `OrientationClique` (positive and negative triples: order
  on ι, injective on all of ι, `4 ≤ s.card`, `i<j → j<k`), `ConvexCycleCuts` (`Fin k ↪ Fin N`, all increasing
  triples, `P` any finite set containing the image) and `Reflection.lean` (all eight declarations).
- **Mirror copies.** `MirrorOdd.hasConvexNGon_of_le` (both copies).

All of these match. The quantifier order, Finset/Set, maps-into, casts and `x/0 = 0` are as stated, and there is no
natural-number subtraction in scope.

**Mechanical reference checks** (script `build/fd_p1ref_refs.py`):
- All 50 `\leanref`s resolve to a line that carries the declaration keyword and the cited name: 0 mismatches.
- All 46 `\dirn{file:N}` citations, including the bare `:N` forms, were printed and inspected. Each points at the
  claimed declaration or proof step: `LayerLemma.lean:165/330/368`, `Reflection.lean:55`, `Construction.lean:54/118`,
  `Placement.lean:20`, `OrientationObstructions.lean:64/68`, `SpikeChain.lean:140`, `VisibleEdgeInsertion.lean:77`
  (name resolution via `open Suk`; unique `convex_orient_nonnegative`), `FiniteDensityBound.lean:66`,
  `AffineReduction.lean:1281/1284/1295/1303/1462/1528`, `MirrorMain.lean:2520`, `ReductionThreeClasses.lean:1267/3741/4079`,
  `ReviewSanity.lean:1086/1091`, `H2/D3Encoding/Geometry.lean:87`, `BoundaryGeometry.lean:30` and
  `docs/SAT.md:168-233`.
- Each cited proof line lies inside the named enclosing declaration.

**Proofs.** I re-derived every step by hand. All proofs are complete and correct:
- The collinearity case split ($u_0\ne0$ / $u_0=0$; $b=a$).
- Carathéodory: positivity of the weights, the exchange step, the forced $k\ge2$, $k\le3$.
- The middle-parameter argument of `small`(c).
- The kernel vectors for $\det A=0$, including $A=0$.
- The reverse directions of `affine-cp` (b)-(d).
- The twelve support values of `four-positive`. The "r is one of the three other letters" step needs no distinctness.
- The reversed order in `neg-triples` and the transposition sign.
- `pos-cycle` through `pos-triples` with ι = Fin k.
- Separation: the minimiser on the compact simplex (Rudin 2.41, 4.16 are Heine–Borel and the extreme value theorem),
  the first-order inequality and the strict final inequality.
- The iterate identity `f^[i+1] = f ∘ f^[i]` from Lean's convention `f^[n+1] = f^[n] ∘ f`.

There is no circularity: `mono`(d) cites `ngon-basic`(b) only to describe the Lean proof.

**Symbolic checks** (sympy 1.13.3, `build/fd_p1ref_sympy.py`): 58 identities, all zero. They cover:
- `orient` = [a,b]+[b,c]+[c,a]; swap, cycle and translate; all six permutations with their signs; (e); the affine law
  with det.
- rot (a) complex form; (b) all three forms and ρ(c)=c; (c) R_αR_β=R_{α+β} and R_0=I; (e); (f); det R=1; invariance
  of `orient`.
- The reflection: det F=−1, Fu=u, Fu⊥=−u⊥=(sinφ,−cosφ), the two subtraction formulas, the sign of `orient`,
  F_0=diag(1,−1), and 2uuᵀ−I=F (the `D3.reflC` comparison).
- The adjugate identity and A⁻¹; the two kernel vectors; (*); the halfplane identity and the Lean certificate
  (p₁q₀−p₀q₁)(u+v−1); the support sum; the twelve four-positive values; the separation expansion; the
  `small`(c) parameter identity.

**Evidence paragraph.**
- **Pins and hashes.** All 15 SHA-256 prefixes match. `lean-toolchain` = v4.24.0 and the manifest pins Mathlib at
  `f897ebcf72cd…`. Neither file has changed since `07c94a2ac`/`a429df30a` (4 and 10 October), so the 11 October
  audit was produced with the same Lean and Mathlib.
- **Audit and later commits.** No commit after `7f0868fdb` touches `ErdosSzekeres/`. The audit lines
  49(-51)/87/88/103/113/114/119/132/175/176/178/529/624/720/725/732 are as cited. `VALIDATION.md:73` (`--wfail`) is
  as cited.
- **Text search.** No `sorry`/`admit`/`axiom`/`native_decide` in the 13-file import closure plus the four Vendor
  files, or in the six research files.
- **LayerLemma.** The recheck copy's first 1148 lines are byte-identical (`diff`), and `out.txt` has 19 axiom lines
  with exit status 0. `LEANEXT/review/REPORT.md` (header and item 1) identifies `afb8542d`, 1148 lines, exit 0. It
  was committed after the last change to `LayerLemma.lean` (4 Nov 09:34 vs 02:43). `axioms.log` lines
  1/22/23/26/33 are as cited.
- **SYMLEAN.** `runs.tsv` lines 2/4/5 are as cited. `AffineReductionAxioms.lean` = 1533 identical lines + 9
  `#print axioms` + 1 `#check`. The `AffineReductionAxioms.out` lines 9-11/13-15/16 are as cited.
- **OrbitConsistency.** The orbit `build.log` holds only the exit code, and `REPORT.md:3` identifies `9b843180`.
  The orbit `axioms.log` lines 1/5 are as cited.
- **Mirror files.** `MirrorMain.out:858` is as cited, and `MIRRORETV/README.md:73` ties it to `ca623e55`.
  `SYMLEAN/mirror/axioms.out:11` comes from `#print axioms MirrorOdd.mirror_odd_general` at
  `ReductionThreeClasses.lean:4231`. `SYMLEAN/mirror/README.md:49-50` records exit 0 and no errors.
- **native_decide axioms.** `Init/Core.lean` of the 4.24.0 toolchain has `axiom trustCompiler` (:2340), which
  `reduceBool` references, and `axiom ofReduceBool` (:2392). The native_decide sentence is therefore right.
- **ReviewSanity lemmas.** `Review.rotAbout_center` is unused, and `Review.orient_rotAbout` is used only in the
  unprinted `orient_rot5_pos`. The claim that no printed theorem uses them holds.

**Cross-section references.** All six outgoing references are contract export labels, and each target says what fd
claims:
- `mb:thm:baek` is a theorem, "Baek's theorem, cited".
- `ll:def:hv` and `ll:def:peel` are the definitions of `hullVerts` and `peel`.
- `ll:def:66-70` defines the two propositions and notes the real numerals; the Lean source writes
  `2 * Real.pi / 6` and `/ 7` in ℝ.
- `oc:lem:perm` is `orient3_perm`, and `oc:lem:rot-inv` is `orient_rotAbout_inv`.

In the other direction, every `\ref{fd:…}` in the other ten sections is a contract label. The part references
(`mono`(a)-(d), `orient`(a),(b),(d),(e)) exist here with the meaning used there.

**Coverage.** Every declaration of the nine main-library files in the table is either covered or listed with a
reason. A search of the table's files found no declaration that states a written step "in the form given here"; only
special cases such as `Suk.orient_reflectY` and `MirrorOdd.orient_mir3` exist, and the text says the list of
counterparts is not complete.

**LaTeX and hygiene.**
- Two pdflatex passes of a private wrapper (`build/fd_p1ref_wrapper.tex`) both exit 0.
- There are 0 overfull boxes. The only undefined references are the six expected export labels.
- There is no `\newcommand`/`\def`/`\usepackage`, no machine path, no tool name and no non-ASCII
  character.
- The 40 map rows match the 40 environments in label, kind and order, and all 20 contract `fd:` labels are defined
  on the named statements.

**Rigor vocabulary.**
- "Proved" is used only for the written proofs ("proved here", "we prove").
- "Verified" and "certified" occur only in the sentence that bans them.
- No hypothesis is presented as proved: `Sixfold66` and `Sevenfold70` appear only in a remark about angle notation.
- Nothing is computer-assisted; `decide` is used only for order facts in Fin 4, as Remark `fd:rem:pos-triples` says.

## 2. Findings

### m1 (minor; rigor-label precision): fd.tex:411-417, Lemma `fd:lem:rot`(b)

- **Claim.** Part (b) is tagged `\leanref{ErdosSzekeres.LayerLemma.rotAff}{LAYERLEAN/LayerLemma.lean:311}`. It
  asserts three things:
  1. $\rho_\theta(p)=c+R_\theta(p-c)=R_\theta p+(c-R_\theta c)$;
  2. the affine law $\rho_\theta(p+v)=\rho_\theta(p)+R_\theta v$;
  3. $\rho_\theta(c)=c$.

  The parenthetical says that `rotAff` supplies item 2 and that item 3 is a written step. By the rule at
  fd.tex:76-79, item 1 is then presented as Lean-checked through the tag.
- **Evidence.** `rotAff` (LayerLemma.lean:311-317) is a `def` whose only checked content is the `map_vadd'`
  obligation, `rotAbout c θ (v +ᵥ p) = linear v +ᵥ rotAbout c θ p`, that is, item 2. Item 1 is not stated there. It
  follows from item 2 only together with item 3, which is a written step. Directly, item 1 is the coordinate formula
  of the Lean-tagged Definition `fd:def:rot` (LayerLemma.lean:298-300) written with the matrix $R_\theta$. So nothing
  false is claimed, but the source of the label for item 1 is misattributed.
- **Fix.** Add to the parenthetical: "the first identity is Definition `fd:def:rot` written with the matrix
  $R_\theta$". Alternatively, mark item 1 like ρ(c)=c, for example: "(the first identity restates Definition
  `fd:def:rot` in matrix form; the identity ρ(c)=c is a written step …)".

## 3. Notes (no finding)

- **`reflectY` simp lemmas.** `Suk.reflectY_x` and `reflectY_y` are `rfl`-lemmas used through `simp only` in
  `orient_reflectY`, so their presence in a printed proof term cannot be asserted. The hedge at fd.tex:185-188 ("not
  covered by a printed line that we identified") is therefore accurate, and the build-plus-text-search fallback is
  sound. The import closure is complete: BaseOrder→BaseChart→TriangleOrder→OrientationGeometry, and
  CupsCaps→Vendor×4.
- **Notation (style only, not a finding).** In `fd:lem:orient`(d) and its proof, $p_1,p_2,p_3$ name three points,
  while Definition `fd:def:point` reserves $p_0,p_1$ for the coordinates of a point $p$. The meaning is clear from
  "$p_1,p_2,p_3\in R^2$". Renaming the points to $x_1,x_2,x_3$ (also in Remark `fd:rem:orient-lean`) would remove the
  clash.
