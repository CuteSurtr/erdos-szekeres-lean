# Review of section `fd` (round 1, lens: rigor)

Section: `STAGE/sections/fd.tex` (1029 lines) and `STAGE/sections/fd.map.tsv` (32 rows).
Lean sources read in full: `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry,Basic}.lean`,
`ErdosSzekeres/Suk/{FourPoint,SupportingLines,OrientationClique,Reflection}.lean`, `ErdosSzekeres/ConvexCycleCuts.lean`.
Research files read at the cited places: `LAYERLEAN/LayerLemma.lean` (1-120, 155-340, 455-480, 1098-1148),
`SYMLEAN/SymmetricReduction.lean` (265-275, 395-410), `LEANEXT/orbit/OrbitConsistency.lean` (40-50, 88-125, 166-186),
`MIRRORETV/lean/MirrorMain.lean` (2170-2190, 2498-2520), `SYMLEAN/mirror/ReductionThreeClasses.lean` (3730-3750).
Inventories: `LAYERLEAN.json`, `MAIN-LIBRARY-coverage.json`.

**Verdict: PASS.** No blocker and no major finding. Every proof was checked step by step, every algebraic and
trigonometric identity was checked with sympy (87 checks, all pass), every use of an earlier result was checked against
its hypotheses, and every contract statement of `fd` was checked for truth and against its Lean declaration. No contract
statement is false or mismatched. Thirteen minor findings (M1-M13) are listed in Section 6.

## 1. Contract statements: truth and match with Lean

All 8 contract definitions and 12 contract facts are defined in the section, on the named statements, in the contract
order (with additional helper statements interleaved). Every `\leanref` file and line is exact (0 off); each cited line
carries the declaration keyword.

| label | Lean declaration (file:line) | check |
|---|---|---|
| fd:def:point | `Point` (Definitions.lean:9, `abbrev`) | `Fin 2 → ℝ`; Finset vs Set coercion described correctly |
| fd:def:orient | `orient` (Orientation.lean:9) | formula and `[CommRing R]` generality match; det form verified |
| fd:def:gp | `GeneralPosition` (Definitions.lean:12) | pairwise distinct a,b,c; `¬ Collinear ℝ {a,b,c}`; Mathlib `Collinear` = `Module.rank (vectorSpan) ≤ 1` stated correctly |
| fd:def:cp | `ConvexPosition` (Definitions.lean:17) | `ConvexIndependent ℝ` of the inclusion; Mathlib definition (∀ t x, p x ∈ conv (p '' t) → x ∈ t) stated correctly; the reformulation for the inclusion is exact |
| fd:def:ngon | `HasConvexNGon` (Definitions.lean:21) | exactly n points, no emptiness condition; K-free defined |
| fd:def:forces | `ForcesConvexNGon` (Definitions.lean:25) | `N ≤ card` (at least), general position; match |
| fd:def:inv | `Invariant` (LayerLemma.lean:105, SymmetricReduction.lean:271, OrbitConsistency.lean:47) | maps into; the three bodies are textually identical (checked) |
| fd:def:rot | `rotAbout` (LayerLemma.lean:298, SymmetricReduction.lean:400, OrbitConsistency.lean:93) | formula matches; 19 definitions in the research records, all with this body (checked by text search) |
| fd:lem:orient | `orient_swap` :12, `orient_cycle` :15, `orient_translate` :18 | (a)-(c) match; (d), (e) written steps; true over any commutative ring |
| fd:lem:affine-orient | written step | true (det multiplicativity); rotation det 1, reflection det −1 verified |
| fd:lem:collinear | `orient_eq_zero_iff_collinear` (OrientationGeometry.lean:36), `generalPosition_iff_orient_ne_zero` (:66) | match, degenerate triples included |
| fd:lem:cp-hull | `convexPosition_iff` (Basic.lean:15) | match (`∀ p ∈ ↑s, p ∉ convexHull ℝ (↑s \ {p})`) |
| fd:lem:mono | `ConvexPosition.mono` :11, `GeneralPosition.mono` :6, `HasConvexNGon.mono` :20, `MirrorOdd.hasConvexNGon_of_le` (MirrorMain.lean:2182) | match (variables m,n of the last renamed n,n'); verbatim copy at ReductionThreeClasses.lean:3741 in the same namespace `MirrorOdd` (checked) |
| fd:lem:affine-cp | written step | true; statement (a) holds for every affine map, (b)-(d) for injective ones |
| fd:lem:caratheodory | written step | true |
| fd:lem:four-subsets | `Suk.convexPosition_of_subsets_card_le_four` (FourPoint.lean:10), `Suk.convexPosition_of_four_subsets` (:40) | match (Finset subsets, `card ≤ 4`; `4 ≤ s.card` and `card = 4`) |
| fd:lem:four-positive | `Suk.convexPosition_four_of_positive` (SupportingLines.lean:47) | match (four strict inequalities; Finset `{a,b,c,d}`) |
| fd:lem:pos-triples | `Suk.convexPosition_of_positive_triples` (OrientationClique.lean:9) | match exactly: `[LinearOrder ι]`, `p` injective on all of ι, Finset `s`, `4 ≤ s.card`, `i < j → j < k` |
| fd:lem:pos-cycle | `hasConvexNGon_of_positive_cycle` (ConvexCycleCuts.lean:11) | match exactly: `4 ≤ k`, `p` injective, `e : Fin k ↪ Fin N`, `∀ i, p (e i) ∈ P`, all increasing triples; quantifier order kept |
| fd:lem:separation | written step | true; both directions proved |

Helper statements (also checked against Lean where tagged): fd:lem:inv-image(c) = `LayerLemma.iterate_mem` (:52);
fd:lem:rot (a) `rotAbout_eq_crot` :302, (b) `rotAff` :311 (a `def` whose `map_vadd'` field is the affine property with
linear part `toLin' !![cos, −sin; sin, cos]`), (c) `rotAbout_iterate` :465 (`(rotAbout c α)^[j] = rotAbout c (↑j * α)`),
(d) `rotAbout_injective` :319 (see M3); fd:lem:ngon-basic `HasConvexNGon.card_le` :25, `ConvexPosition.hasConvexNGon`
:31; fd:lem:forces-basic `ForcesConvexNGon.mono` :47, `forcesConvexNGon_iff_exact` :37; fd:lem:small last assertion
`convexPosition_of_card_three` :58; fd:lem:halfplane `orient_affine_combination` :6, `convex_orient_positive` :11,
`convex_orient_nonnegative` :21; fd:lem:strict-supports :28; fd:lem:support-sum :40 (Lean `p + b - a` = `(p+b)−a`);
fd:lem:neg-triples (OrientationClique.lean:33). All match.

## 2. Proof checks (step by step)

- **fd:lem:inv-image.** (a) both directions correct (subset of a finite set with equal cardinality is the whole set).
  (b) correct; uses global injectivity, which is assumed. (c) induction on i correct; the auxiliary identity
  f^[i+1] = f∘f^[i] is derived from Lean's convention f^[n+1] = f^[n]∘f (`Nat.iterate` unfolds as `iterate op k (op a)`,
  so the convention stated in the arithmetic paragraph is right); the step of that auxiliary induction is correct, the base
  case is left implicit (M6).
- **fd:lem:rot.** (b) the displayed identity ρ_θ(p)−c = R_θ(p−c) verified; (a) Euler's formula and the product
  (cos θ + i sin θ)(u_0 + iu_1) verified; (c) the displayed product R_αR_β entry by entry and R_αR_β = R_{α+β} verified,
  ρ_0 = id, and the induction ρ^{[j+1]} = ρ^{[j]}∘ρ = ρ_{jα}∘ρ_α = ρ_{jα+α} uses the composition law with the right order
  of factors and the cast (j+1:ℝ) = (j:ℝ)+1; (d) from (c) with ±θ; (e) the middle expression and the final form
  sin θ·|p−c|² verified, and sin θ > 0 on (0,π); (f) verified.
- **fd:lem:orient.** The six-term expansion and the bracket decomposition [a,b]+[b,c]+[c,a] verified; (a), (b), (c)
  verified; (d) the enumeration of the six permutations of {1,2,3} is exhaustive and each of the six identities was
  verified, including the two intermediate steps "by (b) applied to (p2,p1,p3)" and "(p3,p2,p1)" (the argument order of
  (b) is used correctly); (e) all three coincidence cases verified.
- **fd:lem:affine-orient.** orient(g a, g b, g c) = det A · orient(a,b,c) verified for a general 2×2 matrix;
  det R_θ = 1, det F_φ = −1, F_φ u = u, F_φ u^⊥ = −u^⊥, the two subtraction formulas, F_0 = diag(1,−1), and the sign
  reversal for σ verified.
- **fd:lem:collinear-mem.** The span of differences equals the span of {p − p*}; rank ≤ 1 ⇔ contained in a line ℝv.
  Correct (standard linear algebra). The statement matches Mathlib `collinear_iff_of_mem`.
- **fd:lem:collinear.** (⇒) verified symbolically. (⇐) the case split b = a / b ≠ a, and within b ≠ a the split
  u_0 ≠ 0 / u_0 = 0, is exhaustive; r = w_0/u_0 gives r u_1 = w_1 using u_0w_1 = u_1w_0 (verified); in the case
  u_0 = 0 the deduction u_1 ≠ 0 (since u ≠ 0) and w_0 = 0 is correct. (b) immediate. This is the Lean route
  (`collinear_iff_of_mem`, private `exists_smul_of_det_zero`).
- **fd:lem:hull.** (a) correct, including conv ∅ = ∅ and conv{y} = {y}. (b) C convex (concatenation of combinations),
  and the induction on k with the split λ_{k+1} = 1 / λ_{k+1} < 1 is correct (s = 1 − λ_{k+1} > 0). (c) merging repeated
  points and padding with zeros is correct; the two-point case covers y = z. (d) the strict inequality argument is
  correct (one of λ, μ is positive); it also covers w = 0.
- **fd:lem:cp-hull.** Both directions correct from the reformulated definition; uses hull(a) monotonicity.
- **fd:lem:mono.** (a) correct via cp-hull twice. (b), (c) correct. (d) correct (choose a sub-subset of size n′); the
  parenthetical forward reference to ngon-basic(b) only describes the Lean proof and creates no circularity
  (ngon-basic(b) uses mono(a) only).
- **fd:lem:ngon-basic, fd:lem:forces-basic.** Correct; (b) of forces-basic uses mono(b), mono(c) with their hypotheses.
- **fd:lem:small.** (a), (b) correct. (c) non-collinear ⇒ convex position: a = λb + (1−λ)c = c + λ(b−c) gives
  collinearity via collinear-mem with p* = c; symmetric for b, c. Collinear ⇒ not convex position: the parameters
  0, r_b, r_c are pairwise distinct, the middle one is a convex combination of the outer two with
  λ = (τ(z)−τ(x))/(τ(z)−τ(y)) ∈ (0,1) (identity verified), and {a,b,c}∖{x} = {y,z}. The last assertion follows from the
  definition of general position. Correct.
- **fd:lem:affine-cp.** (∗) verified. (a) both inclusions correct (this is the Mathlib proof of
  `AffineMap.image_convexHull`, as claimed). The kernel-vector case split ((α,β) ≠ 0; α = β = 0 with (γ,δ) ≠ 0; A = 0)
  is exhaustive and A(β,−α) = (0, −det A) verified; the inverse formula verified. (b), (c), (d) correct; (c) uses
  affine-orient and collinear(b); (d) converse uses T = g⁻¹(T′) ∩ S with g(T) = T′.
- **fd:lem:caratheodory.** Minimal cardinality choice is well founded (T_0 exists). Positivity of all λ_j, the
  exchange step (t > 0 because all λ_i > 0; λ′_i ≥ 0 in both cases μ_i ≤ 0 / μ_i > 0; λ′_j = 0; sums 1 and x), the
  remark that k ≥ 2 in the exchange step, and the bound k ≤ 3 via dependence of k−1 ≥ 3 vectors in ℝ² (the μ built from
  ν verified: Σμ = 0 and Σμ_i y_i = Σν_i(y_i − y_1)) are all correct.
- **fd:lem:four-subsets.** (a) Y′ ⊆ s∖{p}, p ∉ Y′, u = Y′ ∪ {p}, |u| ≤ 4, u∖{p} = Y′; correct. (b) padding t to
  4 points inside s (|s∖t| ≥ 4 − |t|) and mono(a); correct. Matches the Lean route
  (`Caratheodory.minCardFinsetOfMemConvexHull`, `Finset.exists_subsuperset_card_eq`).
- **fd:lem:halfplane.** (a) affine in r; the Lean certificate `(p1 q0 − p0 q1)(u+v−1)` verified exactly. (b) the
  split u = 0 / u > 0 is exhaustive given u ≥ 0; (c) correct.
- **fd:lem:strict-supports.** Correct: H convex, s∖{p} ⊆ H, orient(p,q,p) = 0 by orient(e).
- **fd:lem:support-sum.** Identity verified, also the two determinant steps (linearity in w; equal columns).
- **fd:lem:four-positive.** The four instantiations of support-sum (p = a, q = a+b−d; p = b, q = b+c−a; p = c,
  q = c+d−b; p = d, q = d+a−c) and all twelve displayed values verified symbolically (each equals the stated sum of
  o_abc, o_abd, o_acd, o_bcd). The reduction "r ≠ p as points ⇒ r equals one of the three other letters" is valid even
  without distinctness (if r equalled the letter of p as a point, then r = p).
- **fd:lem:pos-triples.** u = {i ∈ s : p(i) ∈ t}, p(u) = t, |u| = 4 by injectivity, increasing listing; the four
  triples (e0,e1,e2), (e0,e1,e3), (e0,e2,e3), (e1,e2,e3) give exactly abc, abd, acd, bcd. Hypotheses of
  four-subsets(b) (|p(s)| ≥ 4) and four-positive met. Correct. Remark (iii) variant for |s| ≤ 3 is correct.
- **fd:lem:neg-triples.** Reversed order; orient(i,j,k) = −orient(k,j,i) verified (transposition (1 3) in (d)).
- **fd:lem:pos-cycle.** q = p∘e injective, T = q(Fin k) ⊆ P, |T| = k, pos-triples with ι = Fin k, s = univ, |s| = k ≥ 4.
  Correct. Remark fd:rem:pos-cycle matches `ConvexCycleCut` (∃ i<j<l with orient ≤ 0) and `convexCycleCut_of_avoids`.
- **fd:lem:separation.** (⇐) correct (hull(d), hull(a)). (⇒) F = ∅ handled; Δ compact, h continuous, minimiser q ∈
  conv F by hull(c); z_t ∈ conv F; x − z_t = w − t(y−q) and the expansion of ‖w − t(y−q)‖² verified; dividing by t > 0
  and letting t → 0 gives ⟨w, y−q⟩ ≤ 0; ℓ(x) − ℓ(q) = ‖w‖² > 0. Inequality directions correct.
- **Remarks.** fd:rem:ngon (contrapositive of mono(d) with n′ = K, n = K′) correct; fd:rem:angles correct (real
  numerals 6, 7 equal the casts of the naturals; Sixfold66/Sevenfold70 at LayerLemma.lean:1102-1109 checked).

No proof step is delegated to Lean: every "the Lean proof does X" sentence is accompanied by a complete written argument.
Circularity check: hull → cp-hull → mono → ngon-basic/forces-basic/small → affine-cp; caratheodory uses hull only;
four-subsets uses caratheodory, cp-hull, mono; four-positive uses support-sum, strict-supports, halfplane; pos-triples
uses four-subsets, four-positive; no cycle.

## 3. Identities checked with sympy

Script `STAGE/build/fd_rigor_r1/check_fd.py` (output `check_fd.out`): 87 symbolic checks, 0 failures. They cover:
orient = det(b−a | c−a) and the example value 1; the six-term and bracket expansions; orient_swap, orient_cycle,
orient_translate; all six permutation signs and the two intermediate (b)-steps; the three degenerate cases; the affine
law with det A; det R_θ, det F_φ, F_φ u, F_φ u^⊥, the subtraction formulas, F_0, reflection sign; rot (a) complex form,
(b) both affine forms and ρ(c) = c, (c) R_αR_β (displayed entries and R_{α+β}) and ρ_α∘ρ_β = ρ_{α+β}, ρ_0 = id, (d)
ρ_{−θ}∘ρ_θ = id, (e) both displayed expressions, (f), invariance of orient under ρ; the collinearity computations;
(∗) of affine-cp, the kernel vectors and A⁻¹; the middle-parameter identity of small(c); the Carathéodory μ
construction; the halfplane Lean certificate; support-sum and its two determinant steps; the four support-sum
instantiations and all twelve values of four-positive; the neg-triples sign; the separation expansion and x − z_t.

## 4. Evidence claims checked

- SHA-256 prefixes of all 14 files in the source table: all match the files at commit 7e32ee259.
- Commit 7e32ee259 on branch es7-night-2026-11-01; package `erdos_szekeres`, default target `ErdosSzekeres`
  (lakefile.toml); `lean-toolchain` = v4.24.0; Mathlib rev f897ebcf72cd16f89ab4577d0c826cd14afaafc7 (lake-manifest.json).
  The pins were last changed on 2026-10-10, before the 2026-10-11 audit.
- `docs/validation/axiom-audit-lower-bound-2026-10-11.txt` lines 87, 103, 113, 114, 119, 175, 176: exactly the stated
  declarations, three standard axioms. The dependency claims (convexPosition_iff, ConvexPosition.mono,
  convex_orient_positive, orient_affine_combination, orient_support_sum, orient_reflectY,
  generalPosition_iff_orient_ne_zero at Reflection.lean:55, orient_eq_zero_iff_collinear) are correct by reading the
  proofs. The twelve "not covered" declarations are indeed not printed in any saved audit under `docs/validation/`.
- Last commits of the cited main-library files: 2026-10-04 and 2026-10-05 (git log, read only): correct.
- `LAYERLEAN/logs/build.log` (exit 0, 0 lines of messages); `LEANEXT/review/axioms.log` lines 1, 22, 23, 33 as stated;
  `SYMLEAN/logs/runs.tsv` (6d5ec90a, exit 0, 0 lines); `LEANEXT/orbit/logs/build.log` (exit=0) and `axioms.log` line 1;
  `MIRRORETV/lean/MirrorMain.out` has 121 warnings and no error (its warning at line 265 matches the current file);
  `SYMLEAN/mirror/README.md:49-50` records exit 0. Text search of the five research files and of the main-library files
  named finds no `sorry`, `admit`, `axiom` declaration or `native_decide`.
- No machine path and no tool name in `fd.tex` or `fd.map.tsv`. All `\ref`s are to `fd:` labels or to
  contract export labels (`ll:def:hv`, `ll:def:peel`, `ll:def:66-70`, `oc:lem:rot-inv`).

## 5. Compile check

Private wrapper `STAGE/build/fd_rigor_r1/fdr1_wrapper.tex` (same content as the contract's wrapper), compiled twice with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`: exit 0 both times. Undefined references only to the four
allowed export labels of other sections. No "Missing $" or other error. Two overfull boxes (M13).

## 6. Findings (all minor)

- **M1 (minor; conventions, fd.tex:16-20 vs 27-29).** The path rule says that every path not beginning with
  `ErdosSzekeres/`, `docs/`, `experiments/` or `scripts/` is relative to `cloud/es7-2026-10-19/results`, but the same
  paragraph names the root files `lean-toolchain` and `lake-manifest.json`, which do not exist under the results
  directory. Read literally, the convention points to nonexistent files. I rate this minor because the two files are
  the standard Lake root files and are named as files rather than cited locations; a strict reading of the quality bar
  ("wrong file") could rate it major. Fix: say "at the repository root" for these two files, or add bare root file
  names to the root-relative rule.
- **M2 (minor; conventions, fd.tex:21-22).** "For a declaration it is the line that carries the keyword `def`,
  `abbrev` or `theorem`." Other sections cite `structure` and `inductive` declarations (checked on the cited lines of all
  section maps: keywords def, abbrev, theorem, structure, inductive occur). Fix: list all declaration keywords used
  (structure, inductive; also `noncomputable def`, `@[simp] theorem` lines are fine as they carry the keyword).
- **M3 (minor; fd:lem:rot(d), fd.tex:309, 324-325).** The statement tagged with `rotAbout_injective` claims that
  ρ_θ is a bijection with inverse ρ_{−θ}; the Lean conclusion is only `Injective (rotAbout c θ)`. The extra content is
  proved correctly (from (c)), and "in particular it is injective" isolates the Lean conclusion, but unlike (c) there is
  no sentence saying which part is the Lean declaration (contract rule 4: a strengthening must be labelled). This is a
  fidelity matter more than a rigor gap; the fidelity lens may rate it higher. Fix: add "(The Lean declaration cited for
  (d) is the injectivity; the inverse is a written step.)".
- **M4 (minor; rigor-label definition, fd.tex:43-48 vs Remark fd:rem:pos-triples(ii)).** "Computer-assisted: a
  statement whose proof contains ... kernel evaluation of a decision procedure (Lean's `decide`)". Read literally, the
  Lean proof of fd:lem:pos-triples contains `decide`, so the remark has to argue that the statement is "not
  computer-assisted in substance". Fix: define the label by the written proof (a statement whose written proof relies on a
  machine computation that is not carried out by hand), so that Lean's discharge of trivial facts such as 0 < 1 in
  `Fin 4` does not trigger it.
- **M5 (minor; fd:lem:separation, fd.tex:959-961; Remark fd:rem:norm, fd.tex:183).** The proof uses Heine–Borel
  (closed and bounded ⇒ compact) and the extreme value theorem without a reference; contract rule 5 asks for a precise
  statement and a reference for cited textbook facts. Also Remark fd:rem:norm says the topology of ℝ² "enters only
  through compactness", but in this section compactness is used for the simplex Δ ⊂ ℝ^m (harmless). Alternative: avoid
  compactness by minimising over the finitely many faces, or cite e.g. Rudin, Principles of Mathematical Analysis,
  Theorems 2.41 and 4.16.
- **M6 (minor; fd:lem:inv-image(c), fd.tex:281-283).** The auxiliary induction for f^[i+1] = f∘f^[i] shows only the
  step; the base case f^[1] = f^[0]∘f = f = f∘f^[0] is left implicit. Trivial.
- **M7 (minor; axioms evidence, fd.tex:152-157).** The section says `MirrorOdd.hasConvexNGon_of_le` "is not printed
  individually" and relies on a no-error compile log. Stronger evidence exists in the same log, in the sense used for
  the main library: `MirrorOdd.mirror_odd_general` (MirrorMain.lean:2498) uses `hasConvexNGon_of_le` at line 2520, and
  `MIRRORETV/lean/MirrorMain.out:858` prints it with the three standard axioms. Suggest adding this.
- **M8 (minor; axioms evidence, fd.tex:133).** For the twelve main-library declarations without a printed axiom line,
  the evidence is "they compile as part of the main library" plus a source scan, but no build record is named. Suggest
  naming one (e.g. that the 2026-10-11 audit imports the built library and the files are unchanged since, or a CI
  record).
- **M9 (minor; map, fd.map.tsv).** The map has rows for the 9 definitions and 23 lemmas but none for the 7 remark
  environments (fd:rem:norm, fd:rem:ngon, fd:rem:angles, fd:rem:affine-orient-lean, fd:rem:affine-cp-lean,
  fd:rem:pos-triples, fd:rem:pos-cycle). The contract asks for one row per statement environment and 8 of the 10 other
  maps list their remarks; fd:rem:pos-triples(iii) contains a proved variant.
- **M10 (minor; Coverage, fd.tex:1012-1028).** `ErdosSzekeres/Suk/Reflection.lean` is in the source table, but its
  declarations `Suk.reflectY`, `reflectY_x`, `reflectY_y`, `reflectY_reflectY` and `Suk.hasConvexNGon_of_reflectY` are
  neither covered nor listed as deliberately not covered (contract rule 9).
- **M11 (minor; fd:lem:orient(d), fd.tex:377).** (d) is tagged "written step", but its exact Lean counterpart over ℝ
  exists: `ErdosSzekeres.OrbitConsistency.orient3_perm` (`LEANEXT/orbit/OrbitConsistency.lean:178`, export label
  `oc:lem:perm`), `orient3 (t ∘ σ) = sign σ · orient3 t`. Suggest naming it in a remark with `\ref{oc:lem:perm}`.
- **M12 (minor, informational; cross-section).** Helper statements proved here (fd:def:conv, fd:lem:inv-image,
  fd:lem:rot, fd:lem:hull, fd:lem:small, fd:lem:ngon-basic, fd:lem:forces-basic, fd:lem:halfplane,
  fd:lem:strict-supports, fd:lem:support-sum, fd:lem:neg-triples) are not in the contract's export list, so other
  sections may not `\ref` them. I checked that the other sections reference only contract-listed `fd:` labels, and use
  only parts that exist here with the same meaning (mono (a)-(d), orient (a), (b), (d)). Some facts are re-derived
  elsewhere (e.g. `ll` re-proves the rotation facts of fd:lem:rot). The orchestrator may wish to export fd:lem:rot and
  fd:lem:small.
- **M13 (minor; LaTeX).** Two overfull boxes (2.1 pt and 5.1 pt) at the statement heads of fd:lem:four-subsets and
  fd:lem:halfplane (fd.tex:764-766, 787-789). Cosmetic.

## 7. Contract discrepancies

None. Every contract statement of `fd` is true, and every statement tagged with a Lean name matches its declaration
(M3 concerns only an added, proved strengthening attached to `rotAbout_injective`).
