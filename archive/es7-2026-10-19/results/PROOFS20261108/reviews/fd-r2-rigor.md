# Review of section `fd` (round 2, lens: rigor)

Section: `STAGE/sections/fd.tex` (1189 lines) and `STAGE/sections/fd.map.tsv` (40 rows).

**Verdict: PASS.** There is no blocker and no major finding.
- Both round-1 major findings are fixed. I checked each fix against the Lean source and the logs (Section 1).
- I re-checked the whole section step by step.
- All 119 algebraic and trigonometric identities pass in sympy.
- Every contract `fd:` statement is true and matches its Lean declaration. There is no contract discrepancy.
- Eight minor findings are listed in Section 7. The most useful one is m1: the build log cited for
  `LAYERLEAN/LayerLemma.lean` was produced for an earlier version of that file.

Paths: `STAGE/...` is the staging area. `ErdosSzekeres/...`, `docs/...` and the pin files are relative to the
repository root (commit `7e32ee259`). All other paths are relative to `RES`. Nothing under REPO was modified. The only
git commands used were read-only (`rev-parse`, `log`, `diff`, `show`, `merge-base`). No Lean, lake or solver was run.

## 1. Round-1 major findings: were they fixed?

Both findings (fidelity F1, claims M1) said the same thing. `fd:lem:affine-orient`, `fd:lem:affine-cp` and, over the
reals, `fd:lem:orient`(d) have Lean counterparts, but the section did not tag them and said that none exist.

**Fixed.** Checked against the source:

- **`fd:lem:affine-orient`** is now tagged `ErdosSzekeres.SymReduction.orient_affine`
  (`SYMLEAN/AffineReduction.lean:1241`).
  - The namespace `ErdosSzekeres.SymReduction` opens at :54.
  - The Lean hypothesis is `hg : ∀ p, g p = L *ᵥ p + b`. The conclusion is
    `orient (g x) (g y) (g z) = L.det * orient x y z`.
  - The new wording ("g is a map with g(x)=Ax+v for every x") matches this with A = L and v = b.
  - The copy at `SYMLEAN/mirror/ReductionThreeClasses.lean:1267` is in the same namespace (lines 80-1559 of that
    file), and its text is identical (diff empty).
  - The proof sketch of the Lean route (`rw [hg, hg, hg, Matrix.det_fin_two]`, expand, `ring`) is accurate.
- **`fd:lem:affine-cp`.** The new items (b′)-(e′) match the Lean declarations exactly, hypothesis by hypothesis:
  - (b′) `convexPosition_image_affine` :1263: `ConvexPosition s`, an injective `f : Point →ᵃ[ℝ] Point`, conclusion on
    `s.image f`.
  - (c′) `generalPosition_image_affine` :1278 (`hg`, `L.det ≠ 0`) and `generalPosition_image_affineEquiv` :1290
    (`f : Point ≃ᵃ[ℝ] Point`).
  - (d′) `hasConvexNGon_image_affine` :1298.
  - (e′) `injective_of_affine` :1305.
- **The new proof of (b′)-(e′) is correct:**
  - (b′) and (d′) reduce to the forward directions of (b) and (d), using f(x) = A_f x + f(0) (`affineMap_eq_mulVec`
    :1284).
  - For (e′), the adjugate identity L♯L = (det L)I was checked in sympy. I also checked Lean's own certificates
    `e0` and `e1` (:1317-1320).
  - (c′) reduces to the forward direction of (c), applied to h (injective by (e′)) and to an affine bijection.
- **`fd:rem:orient-lean`** (new) is correct. With t(i) = p_{i+1}, σ(i) = π(i+1)−1 and s(i) = i+1:
  - σ = s⁻¹πs.
  - (t∘σ)(i) = p_{π(i+1)}.
  - sgn σ = sgn π.
  I checked all six permutations by script. Lean's `orient3_perm` (`LEANEXT/orbit/OrbitConsistency.lean:178`, with
  `orient3` at :168) is therefore (d) for R = ℝ.
- **The two remarks and the Coverage paragraph are rewritten.** The false sentences are gone ("Lean proves the special
  cases it needs separately"; "without a single Lean counterpart").
- **New evidence, checked line by line:**
  - `SYMLEAN/AffineReduction.lean` (prefix `41cfc0b60aec`) is in the sources table, and the hash is correct.
  - `SYMLEAN/logs/runs.tsv` line 4: `41cfc0b6`, exit 0, 0 output lines. Line 5: `AffineReductionAxioms.lean`
    `f6cb9372`, exit 0. Its current SHA-256 is `f6cb9372…`.
  - `AffineReductionAxioms.lean` is the current `AffineReduction.lean` plus appended lines (diff).
  - In `SYMLEAN/logs/AffineReductionAxioms.out`, lines 9-11, 13-15 and 16 print the stated theorems with the three
    standard axioms.
  - The usage chains are as stated:
    - `injective_of_affine` is used at :1462, inside `hasConvexNGon_of_affine_coords_symmetry`. That theorem is used
      at :1528, inside `heptagon_of_nontrivial_affine_coords`.
    - `generalPosition_image_affine` is used at :1295. `orient_affine` is used at :1281.
    - `convexPosition_image_affine` is used at :1303.

## 2. Contract statements: truth and match with Lean

All 20 contract labels are defined on the named statements, in contract order; helper labels are interleaved.

| label | Lean (file:line) | result |
|---|---|---|
| fd:def:point | `Point` Definitions.lean:9 | exact |
| fd:def:orient | `orient` Orientation.lean:9 | exact, any `CommRing`. "Over Q and Z" is true (`IntegerCertificates.lean` uses ℤ). |
| fd:def:gp | `GeneralPosition` :12 | exact. Mathlib `Collinear` (`Module.rank (vectorSpan) ≤ 1`) checked at pin f897ebcf. |
| fd:def:cp | `ConvexPosition` :17 | exact. The `ConvexIndependent` text is checked at the pin, and the reformulation for the inclusion is exact. |
| fd:def:ngon / forces | :21 / :25 | exact |
| fd:def:inv | LayerLemma:105, SymmetricReduction:271, OrbitConsistency:47 | exact (maps into); the three are textually identical |
| fd:def:rot | LayerLemma:298, SymmetricReduction:400, OrbitConsistency:93 | exact. 19 definitions in RES, all with the same body (re-counted). |
| fd:lem:orient | Orientation.lean:12, :15, :18 | (a)-(c) exact; (d), (e) written steps; real case of (d) = `orient3_perm` |
| fd:lem:affine-orient | AffineReduction.lean:1241 | exact (see §1) |
| fd:lem:collinear | OrientationGeometry.lean:36, :66 | exact |
| fd:lem:cp-hull | Basic.lean:15 | exact (Mathlib `convexIndependent_set_iff_notMem_convexHull_diff` checked at the pin) |
| fd:lem:mono | Basic.lean:11, :6, :20; `MirrorOdd.hasConvexNGon_of_le` MirrorMain.lean:2182 | exact |
| fd:lem:affine-cp | (b′)-(e′) AffineReduction.lean:1263/1278/1290/1298/1305 | exact; (a)-(d) are true |
| fd:lem:caratheodory | written step | true |
| fd:lem:four-subsets | FourPoint.lean:10, :40 | exact |
| fd:lem:four-positive | SupportingLines.lean:47 | exact |
| fd:lem:pos-triples | OrientationClique.lean:9 | exact (`LinearOrder`, p injective on all of ι, `4 ≤ s.card`) |
| fd:lem:pos-cycle | ConvexCycleCuts.lean:11 | exact (quantifier order and implicit `P` kept) |
| fd:lem:separation | written step | true, both directions proved |

Mechanical checks:
- A script resolved all 49 `\leanref{name}{file:line}`. Each cited line carries a declaration keyword and the short
  name (0 mismatches).
- The 40 map rows match the 40 statement environments in label, kind and order. All map name/line pairs resolve.
- The other `\dirn{file:N}` citations were opened one by one, and each shows what the text says:
  - Reflection.lean:42/43/44/47/52/55/64;
  - Basic.lean:45/73/75;
  - LayerLemma.lean:162/165/325/330/368;
  - AffineReduction.lean:1281/1284/1295/1303/1462/1528;
  - MirrorMain.lean:2520; ReductionThreeClasses.lean:1267/3741/4079;
  - ConvexCycleCuts.lean:8/31; docs/SAT.md:168-233.

## 3. Proof checks, step by step

Every proof was read as a referee would read it. The table lists, for each statement, the points I checked:
exhaustive case splits, well-founded inductions, inequality directions, and the hypotheses of every cited result.

| statement | what was checked | result |
|---|---|---|
| inv-image | (a) a subset of a finite set with the same cardinality is the whole set. (b) uses (a) and injectivity. (c) induction on i, plus the auxiliary identity f^[i+1] = f∘f^[i] (base case now written). | correct |
| rot | (b) displayed identity, linearity, rotAff's `map_vadd'` form, ρ(c) = c. (a) Euler's formula. (c) R_αR_β entries and R_{α+β}. Induction: ρ^[j+1] = ρ^[j]∘ρ, using the iterate convention and the cast (j+1:ℝ) = j+1. (d) from (c). (e), (f). | correct |
| orient | Bracket expansion. (a)-(c). (d): all six permutations; the two intermediate (b)-steps use the argument order correctly. (e): three coincidence cases (commutativity is used for b = c). | correct |
| affine-orient | Determinant multiplicativity. det R = 1. det F = −1, Fu = u, Fu⊥ = −u⊥, the subtraction formulas, F₀. σ fixes o + ℝu. | correct |
| collinear-mem, collinear | Span of differences = span of {p − p*}. rank ≤ 1 ⇔ contained in a line ℝv. The split b = a / b ≠ a and, inside it, u₀ ≠ 0 / u₀ = 0 is exhaustive. In the case u₀ = 0, u₁ ≠ 0 and w₀ = 0. | correct |
| hull | (a)-(d). (b): concatenation shows convexity; induction on k with the split λ_{k+1} = 1 / < 1. (c): merging and padding. (d): one coefficient is positive. | correct |
| cp-hull, mono, ngon-basic, forces-basic | Both directions of cp-hull. mono(d) chooses a sub-subset. The parenthetical forward reference in mono(d) only describes the Lean proof. | correct, no circularity |
| small | (a), (b). (c) ⇐ uses hull(c) and collinear-mem with p* = c. (c) ⇒: the parameters are pairwise distinct; the middle one is a convex combination with λ = (τz−τx)/(τz−τy) ∈ (0,1). | correct |
| affine-cp | (∗). (a) both inclusions (the Mathlib proof, checked at the pin). Kernel-vector split (α,β) ≠ 0 / α = β = 0 with (γ,δ) ≠ 0 / A = 0: exhaustive. A⁻¹. (b)-(d) both directions. (b′)-(e′) as in §1. | correct |
| caratheodory | The minimal set exists (well-ordering of ℕ). All weights positive. In the exchange step t > 0, λ′ ≥ 0 in both cases, λ′_j = 0, the sums are 1 and x, and k ≥ 2. k ≤ 3 because k−1 ≥ 3 vectors in ℝ² are dependent (the μ-from-ν identity was checked). | correct |
| four-subsets | (a) Carathéodory applied to s∖{p}; u = Y′ ∪ {p}, |u| ≤ 4, u∖{p} = Y′. (b) padding to 4 points inside s. | correct |
| halfplane, strict-supports, support-sum | Affine in r; Lean certificate (p₁q₀−p₀q₁)(u+v−1); the split u = 0 / u > 0; orient(p,q,p) = 0; linearity in w; a determinant with equal columns vanishes. | correct |
| four-positive | Four instantiations of support-sum (q = a+b−d, b+c−a, c+d−b, d+a−c) and all 12 values. "r ≠ p as points ⇒ r is one of the three other letters" needs no distinctness. | correct |
| pos-triples, neg-triples, pos-cycle | u = {i ∈ s : p(i) ∈ t}, p(u) = t, |u| = 4, sorted listing, four triples. Order dual. The transposition (1 3) has sign −1. q = p∘e. Variant (iii) for |s| ≤ 3 is exhaustive. | correct |
| separation | ⇐ via hull(d), (a). ⇒: F = ∅ handled; Δ is compact (Rudin 2.41, statement correct); minimum attained (Rudin 4.16, statement correct); x − z_t = w − t(y−q); expansion; dividing by t > 0 and letting t → 0; ℓ(x) − ℓ(q) = ‖w‖² > 0. | correct |

Circularity: the dependency graph hull → cp-hull → mono → {ngon-basic, forces-basic, small} → affine-cp has no cycle.
Carathéodory → four-subsets; halfplane → strict-supports → four-positive → pos-triples → {neg-triples, pos-cycle}.
Nothing is delegated to Lean: every "the Lean proof does X" sentence comes with a complete written argument.

## 4. Identities checked with sympy

Script: `STAGE/build/fd_rigor_r2/check_fd_r2.py`. Output: `check_fd_r2.out`. Result: **119/119 pass**.

The new material checked:
- the Lean form of `orient_affine` (with `mulVec2_fst`/`snd` and `det_fin_two`);
- L♯L = (det L)I, and the `injective_of_affine` certificates;
- A⁻¹ in both orders, and g⁻¹∘g = id;
- the `orient3_perm` index translation, combinatorially, for all six π.

All round-1 identities were re-checked as well (orient, rotations, reflections, collinearity, small(c), (∗), the kernel
vectors, Carathéodory, halfplane, support-sum, the 12 four-positive values, neg-triples, separation).

## 5. Evidence claims checked

- **Hashes and pins.** All 15 SHA-256 prefixes in the sources table match. HEAD is `7e32ee259…` on branch
  `es7-night-2026-11-01`. `lean-toolchain` is `v4.24.0`. The Mathlib rev is `f897ebcf72cd…`. The package is
  `erdos_szekeres` with `defaultTargets = ["ErdosSzekeres"]`. The pins are unchanged since the audit commit
  `7f0868fdb`, which is an ancestor of HEAD.
- **Audit lines.** Audit lines 49, 87, 88, 103, 113, 114, 119, 132, 175, 176, 178, 624, 720, 725 and 732 are exactly
  the stated declarations, each with the three standard axioms.
- **Usage claims.** Each cited usage line lies inside the stated enclosing theorem, and the names resolve as claimed
  (`open Suk` in `VisibleEdgeInsertion.lean`; `h.mono` with `h : ForcesConvexNGon`).
- **Files unchanged since the audit.** `git diff 7f0868fdb HEAD` is empty for:
  - every main-library file named;
  - their imports (BaseOrder, BaseChart, TriangleOrder, CupsCaps, the 4 Vendor files);
  - the root `ErdosSzekeres.lean`.
- **The `--wfail` fallback evidence is meaningful.** Basic, OrientationClique, Reflection, ConvexCycleCuts,
  FourPoint and SupportingLines are all in the import closure of the library root (210 modules), so
  `docs/VALIDATION.md:73` ("builds all 3,308 jobs with `--wfail`", under the heading "11 October 2026") covers them.
- **Text search.** No `sorry`, `admit`, `axiom` declaration or `native_decide` occurs in the 13 main-library files or
  the 6 research files.
- **Research-file logs.**
  - `LEANEXT/review/axioms.log` lines 1, 22, 23, 26 and 33 are as stated; line 26 uses `rotAff` at
    LayerLemma.lean:368.
  - `LEANEXT/orbit/logs/axioms.log` lines 1 and 5 are as stated, and the orbit `build.log` reads `exit=0`. Both
    were committed together with the file.
  - `MIRRORETV/lean/MirrorMain.out` line 858 is `mirror_odd_general` (0 errors). The use is at :2520, inside
    `mirror_odd_general` (:2498).
  - `SYMLEAN/mirror/axioms.out` line 11, and `README.md:49-50` (exit 0, no errors).
- **`native_decide` axioms.** The section's claim is confirmed in the Lean 4.24.0 core sources, `Init/Core.lean`:
  - :2340 `axiom trustCompiler : True`;
  - :2361 `opaque reduceBool` uses it;
  - :2392 `axiom ofReduceBool`.
- **Hygiene.** No machine paths, tool names, non-ASCII characters, `\newcommand` or preamble material.

## 6. Compile check

I used a private wrapper `STAGE/build/fd_rigor_r2/fdr2_wrapper.tex`, with the same content as the contract wrapper.
It was compiled twice with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- Both passes exit 0. The PDF has 15 pages.
- There are no errors and no "Missing $".
- The only undefined references are the allowed export labels `ll:def:hv`, `ll:def:peel`, `ll:def:66-70`,
  `oc:lem:rot-inv` and `oc:lem:perm`.
- There are 0 overfull and 82 underfull hboxes. The underfull boxes come from `\sloppy` and `\raggedright`; this is
  cosmetic.

## 7. Findings (all minor)

**m1 (minor; evidence attribution; fd.tex:186-187, also :26).**
- **Claim.** "`LAYERLEAN/logs/build.log` records that `LAYERLEAN/LayerLemma.lean` compiles (exit code 0, no
  messages)".
- **The log is for an earlier version.**
  - `build.log` was last committed in `6429e9a70` (2026-11-04 02:08:32). At that commit `LayerLemma.lean` had 454 lines
    and fewer imports, and it lacked `rotAbout_iterate`, which the section cites for fd:lem:rot(c).
  - The file then changed in `b997a2970`, `6a7ecacef`, `6e3d1feb9`, `88fe40ccc` and `393619a57` (02:43:08), which
    produced the current 1148-line file `afb8542d`. The log was never regenerated.
- **Why this is minor.** No Lean-checked claim of fd rests only on this log:
  - `LEANEXT/review/axioms.log` was made from the current file. It lists `card_peel`, `convexNGon_of_layers` and
    `sixfold_octagon` (lines 56-58), which were added in the last commit, and it covers every cited LayerLemma theorem.
  - The two definitions (`Invariant`, `rotAbout`) occur in the statement of the printed
    `hullVerts_eq_orbitFS_rotAbout`.
  - A compile record of the current file does exist:
    - `LEANEXT/review/REPORT.md` item 1, "Build. Exit 0, no messages", for SHA-256 `afb8542d`;
    - `LAYERLEAN/logs/axioms_recheck_20261106/out.txt`, exit status 0, on a file whose first 1148 lines are
      byte-identical to the current one (diff checked).
- **Uncertainty.** If the orchestrator counts a log of an earlier revision as a "wrong file", this becomes major.
- **Fix.** Cite one of the two current-file records for the compile. Keep `build.log` only for the method
  (`lake env lean` from the root).
- **Cross-section.** `ll.tex:27` and `lg.tex` cite the same log in the same way.

**m2 (minor; label definition; fd.tex:48-50).**
- **Issue.** The Lean-checked evidence is defined as `#print axioms` "for the declaration itself or for a declaration
  whose proof uses it". But the definitions are covered through the *statements* of printed theorems (fd.tex:167-171).
  These are `Point`, `orient`, `GeneralPosition`, `ConvexPosition`, `HasConvexNGon`, `ForcesConvexNGon`,
  `ConvexCycleCut`, and in the research files `Invariant`, `rotAbout` and `orient3`. The paragraph itself argues
  correctly that `#print axioms` traverses types as well as values.
- **Fix.** Write "whose statement or proof uses it".

**m3 (minor; internal inconsistency; fd.tex:1160-1163 vs Remark fd:rem:affine-cp-lean, fd.tex:850-861).**
- **Issue.** Coverage lists `HasConvexNGon.linearEquiv` and `Suk.generalPosition_reflectY` as Lean special cases of the
  *reverse* directions of (b)-(d). The remark classifies both as *forward*-direction special cases, and that is what
  they literally state. Only `Suk.hasConvexNGon_of_reflectY` is a reverse-direction statement. The other two give
  reverse directions only when applied to e⁻¹ or to σ = σ⁻¹, which the text does not say.
- **Fix.** Align the Coverage wording with the remark.

**m4 (minor; standard fact used without its definition; fd.tex:273-276 and the proof at :830-839).**
- **Issue.** Definition fd:def:conv asserts that the Mathlib affine maps of the plane are exactly x ↦ Ax + v with
  v = g(0), without stating Mathlib's definition. The definition is: a map f with a linear map `f.linear` such that
  f(v+p) = f.linear(v) + f(p). The characterization follows from it in one line (p = 0), but a reader without Lean
  cannot see this. The proof of (b′)-(e′) relies on the characterization ("By Definition fd:def:conv, a Mathlib affine
  map f of ℝ² has the form f(x) = A_f x + f(0)"). "Affine bijection (Mathlib `AffineEquiv`)" is not defined either.
- **Wording.** "with A the linear part" should read "with A the matrix of the linear part".
- **Fix.** One sentence with Mathlib's defining property and the derivation.

**m5 (minor; Coverage wording; fd.tex:1149-1150, :1156-1158).**
- (i) "No Lean declaration states the following statements … in the form given here" is literally false for two items.
  Mathlib's `collinear_iff_of_mem` states fd:lem:collinear-mem exactly, and `AffineMap.image_convexHull` states
  fd:lem:affine-cp(a) exactly. Write "no declaration of the project".
- (ii) The sentence promises that "where Lean has a special case or a partial counterpart, it is named". It does not
  name `ErdosSzekeres.Omission.BoundaryGeometry.exposed_not_in_hull` (`ErdosSzekeres/Omission/BoundaryGeometry.lean:30`;
  audit line 529). That is a main-library variant of the easy direction of fd:lem:separation, for an affine g with
  g(p) = 0 and g > 0 on S∖{p}, and mb.tex:419 already cites it as such.
- (iii) "ρ₀ = id" is marked a written step in fd:lem:rot(c) (fd.tex:391-392), but it is missing from the Coverage list
  of written steps.

**m6 (minor; fd.tex:197-198).** `SYMLEAN/AffineReductionAxioms.lean` is described as `AffineReduction.lean` "followed by
`#print axioms` commands". The diff shows nine `#print axioms` lines and one final `#check` line. This is trivial.

**m7 (minor; notation; fd.tex:510-512, :784-786).**
- The Lean-form sentence of fd:lem:affine-orient uses `b` for the translation vector (h(p) = Lp + b), in the same
  statement whose conclusion uses b as a point.
- In (c′) the letter f, already fixed as a Mathlib `AffineMap`, is reused for an `AffineEquiv`.
- Both are readability issues only; the sentences explain the identification.

**m8 (minor, trivial; fd.tex:16-24).** The path rule says that every path not beginning with `ErdosSzekeres/`,
`docs/`, `experiments/` or `scripts/` is relative to the research-records directory. Yet the same sentence names that
directory by the root-relative path `cloud/es7-2026-10-19/results`. "Of the repository" makes the intent clear. Adding
`cloud/` to the root-relative prefixes would make the rule literally consistent.

## 8. Contract discrepancies and notes for the orchestrator

- **No contract statement of `fd` is false or mismatched.**
- **Contract rule 6** names only `Lean.ofReduceBool` for `native_decide`. In Lean 4.24.0 the axiom
  `Lean.trustCompiler` is also tracked (see §5). fd states both correctly. No project file uses `native_decide`.
- **m1 applies to `ll` and `lg` as well.** Both cite `LAYERLEAN/logs/build.log` as the compile record of the current
  `LayerLemma.lean`. Current-file records exist: `LEANEXT/review/REPORT.md` and
  `LAYERLEAN/logs/axioms_recheck_20261106/out.txt`.
