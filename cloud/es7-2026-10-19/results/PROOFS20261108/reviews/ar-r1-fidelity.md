# Review ar, round 1, lens: fidelity

Section: `STAGE/sections/ar.tex` (752 lines), map: `STAGE/sections/ar.map.tsv` (30 rows).
Lean source: `SYMLEAN/AffineReduction.lean`, lines 1059-1533 (paths relative to RES).

**Verdict: pass.** No blocker and no major finding. Six minor findings (F1-F6). None of them affects a statement.

## 1. What was checked

### 1.1 Statement against Lean, one by one

For each statement environment with a `\leanref`, I opened the Lean declaration at the cited line. I compared the
hypotheses, the conclusion, the binder order, the types (Finset vs Set, matrix vs vector, ℕ vs ℝ), strict vs weak
inequalities, maps-into vs equality, and `≠ id` vs `≠ refl`.

| label | Lean declaration(s), line | result |
|---|---|---|
| ar:def:nsq | nsq 1088 | `v 0 ^ 2 + v 1 ^ 2`: matches |
| ar:lem:mulvec | mulVec2_fst 1097, mulVec2_snd 1101 | matches (`(A *ᵥ z) i`, entries as stated) |
| ar:lem:nsq | nsq_nonneg 1090, eDist2_eq_nsq 1094 | matches |
| ar:def:gram | gA 1106, gB 1107, gC 1108 | matches: `A00²+A10²`, `A00·A01+A10·A11`, `A01²+A11²` |
| ar:lem:nsq-mulvec | nsq_mulVec 1110 | matches, including the factor 2 on the cross term |
| ar:def:avgq | avgQ 1116, qA/qB/qC 1120-1122 | matches: sums over `Finset.range n` of `nsq (L^k *ᵥ z)`, `gA (L^k)`, etc. |
| ar:lem:avgq-eq | avgQ_eq 1124 | matches; no hypothesis on n |
| ar:lem:avgq-pos | avgQ_ge 1133, qA_pos 1152, qdisc_pos 1158 | matches; each part has `0 < n` (implicit `{n}`); (c) is `0 < qA*qC - qB^2` |
| ar:lem:avgq-inv | avgQ_mulVec 1139 | matches; the only hypothesis is `L ^ n = 1` |
| ar:def:lin2 | lin2 1167 | matches: `p ↦ ![a p0 + b p1, c p0 + d p1]`, bundled `Point →ₗ[ℝ] Point` |
| ar:lem:lin2 | lin2_fst 1174, lin2_snd 1175, orient_lin2 1177 | matches; factor `a*d - b*c` |
| ar:lem:chol | nsq_lin2_chol 1184, lin2_chol_inv_left 1191, lin2_chol_inv_right 1195 | matches: T = lin2 s (β/s) 0 t, T' = lin2 (1/s) (-β/(s^2 t)) 0 (1/t); (a) needs only `s ≠ 0`, (b) and (c) need `s ≠ 0`, `t ≠ 0` |
| ar:lem:iter | iterate_sub_of_affine 1199 | matches: `g^[k] p - g^[k] q = L^k *ᵥ (p - q)` under hg |
| ar:lem:periodic | exists_periodic_of_injective 1208 | matches: injective g, `Invariant g S`, `q ∈ S` ⇒ ∃ m, 0 < m ∧ g^[m] q = q |
| ar:lem:fix | matrix_eq_one_of_fix 1217 | matches: `u0 w1 - u1 w0 ≠ 0`, `M u = u`, `M w = w` ⇒ `M = 1` |
| ar:lem:orient-affine | orient_affine 1241 | matches: factor `L.det` |
| ar:lem:inj | injective_of_affine 1305 | matches: hg and `L.det ≠ 0` ⇒ Injective g |
| ar:lem:matrix-form | affineMap_eq_mulVec 1284 | matches: `f p = toMatrix' f.linear *ᵥ p + f 0` |
| ar:lem:gp-orient | generalPosition_image_of_orient 1249 | matches: `D ≠ 0`, scaling identity for all x y z, Finset S; no injectivity (the section says so) |
| ar:lem:gp-affine | generalPosition_image_affine 1278, generalPosition_image_affineEquiv 1290 | matches |
| ar:lem:cp-affine | convexPosition_image_affine 1263 | matches: ConvexPosition s, f an injective `Point →ᵃ[ℝ] Point` ⇒ ConvexPosition (s.image f) |
| ar:lem:ngon-affine | hasConvexNGon_image_affine 1298 | matches |
| ar:thm:transfer | hasConvexNGon_of_affine_symmetry 1330 | matches. hE is stated in full: ∀ finite S', ∀ h, GP S' → N ≤ \|S'\| → IsEucIsometry h → h ≠ id → Invariant h S' → HasConvexNGon n S'. Same quantifiers, same hypothesis order. The order of the other binders (hN, S, g, L, b, hg, hinj, hgp, hcard, hne, hinv) is exactly Lean's |
| ar:cor:transfer-forms | hasConvexNGon_of_affineMap_symmetry 1423, ..._affineEquiv_symmetry 1433, ..._affine_coords_symmetry 1444 | matches: (a) injective AffineMap with `⇑f ≠ id`; (b) AffineEquiv with `f ≠ refl`, no injectivity hypothesis; (c) `a d - b c ≠ 0` and `g p = ![a p0 + b p1 + e, c p0 + d p1 + f]`, no injectivity hypothesis |
| ar:thm:main | heptagon_of_nontrivial_affineEquiv 1501, ..._affineEquiv_image 1510, ..._affineMap 1489, ..._affine 1477, ..._affine_coords 1521 | matches. The five classes are explicit hypotheses. `33 ≤ S.card`. (b) has the set inclusion `g '' ↑S ⊆ ↑S`, not equality. (d) keeps `Injective g` |

Reordering note (no finding). In ar:cor:transfer-forms and ar:thm:main, the shared hypotheses "S in general position,
N ≤ |S|" are stated before the map is introduced. In Lean they come after it. They do not mention the map and no
existential quantifier is involved, so the two forms are logically identical.

The definitions used by the section match Lean: `eDist2` (:265), `IsEucIsometry` (:268, all p, q of the plane),
`Invariant` (:271, maps into), `HasConvexNGon` (`ErdosSzekeres/Definitions.lean:21`), `GeneralPosition` (:12),
`ConvexPosition` (:17, used through `convexPosition_iff`, `ErdosSzekeres/Basic.lean:15`), `orient`
(`ErdosSzekeres/Orientation.lean:9`), `AffineMap` / `AffineEquiv` / `refl` / `toMatrix'`, matrix power and `det_fin_two`.
No name in the namespace shadows the repository's `orient`, `GeneralPosition`, `ConvexPosition` or `HasConvexNGon`;
the `#check` output prints `ErdosSzekeres.GeneralPosition` and `ErdosSzekeres.HasConvexNGon`. The section writes the
iterate recursion as g^{k+1} = g ∘ g^k. Lean's `Nat.iterate` recurses as g^[k+1] = g^[k] ∘ g. The two agree
(`Function.iterate_succ'`), and the section does not claim that its recursion is Lean's definition.

### 1.2 Names, lines, map

- The section's `\leanref` heads cite 45 distinct names. Lines 1059-1533 contain exactly 45 `theorem`/`def`
  declarations, and the two lists are the same. Every cited line equals the actual declaration line (offset 0).
- The map has the correct header (tab-separated) and 30 rows. They are the 30 statement environments, in the order of
  the section. For each label, the names in the map equal the names in the `\leanref` head, in the same order, and
  every map file:line equals the actual line (45 of 45).
- Every other Lean or Mathlib name the section cites occurs in the compiled source, directly or through dot notation:
  `AffineMap.decomp` (as `f.decomp`, 1287), `AffineMap.image_convexHull` (1272), `LinearMap.toMatrix'_mulVec` (1286),
  `LinearMap.det_toMatrix'` and `LinearEquiv.isUnit_det'` (1293-1294), `Matrix.det_fin_two` (1244), `Matrix.det_fin_two_of`
  (1460), `AffineEquiv.ext` (1441), `Ti.toAffineMap` (1420). The proof-step names `hLm`, `hTiT`, `hTTi`, `hnT`, `hiso`,
  `hinv'` and `hne'` exist at 1356-1412. Outside the scope: `iterate_mem` (:69) and `point_ext` (:502) are correct;
  `mirrorOneAxis33_proved` (mirror file :4274), `mirrorNoAxis34_proved` (:4282) and
  `heptagon_of_nontrivial_affineEquiv_3` (:4303) are correct, and the last one is part (a) with only `h2 h3 h5`.

### 1.3 Sources, hashes, axioms

- All eight SHA-256 prefixes in the section are correct (recomputed): AffineReduction.lean `41cfc0b60aec`,
  SymmetricReduction.lean `6d5ec90a4215`, AffineReductionAxioms.lean `f6cb9372b174`, logs/AffineReductionAxioms.out
  `38d0b6f59398`, Definitions.lean `2425500eefd1`, Orientation.lean `f67955ac7091`, Basic.lean `13667aa2d3dc`,
  OrientationGeometry.lean `c7db9bbbb65e`.
- Lines 1-1058 of AffineReduction.lean are byte-identical to lines 1-1058 of SymmetricReduction.lean (cmp). Lines 1-1533
  of AffineReductionAxioms.lean equal AffineReduction.lean. Lines 38-1559 of mirror/ReductionThreeClasses.lean equal
  AffineReduction.lean 12-1533 (offset +26, as the section says).
- The axioms log lists exactly the nine theorems named in the section, each with `[propext, Classical.choice,
  Quot.sound]`. The `#check` line shows the five classes as premises of heptagon_of_nontrivial_affineEquiv.
  `logs/AffineReduction.out` is 0 bytes; `runs.tsv` gives exit 0 on 2026-11-01. The toolchain (`v4.24.0`, Mathlib
  `f897ebcf72cd`) matches.
- The claim "every other declaration is used in the proof of one of the nine" holds. I traced all 45: for example,
  `orient_affine` → `generalPosition_image_affine` → `generalPosition_image_affineEquiv` (printed), and
  `injective_of_affine` → `..._coords_symmetry` → `heptagon_of_nontrivial_affine_coords` (printed).
- Lines 1059-1533 contain no `decide`, `native_decide`, `sorry`, `admit` or `axiom`.

### 1.4 Coverage, export labels, references

- Coverage: all 45 declarations of lines 1059-1533 are covered by label. The exclusions are valid: lines 1-1058 are a
  verbatim duplicate; the Axioms file adds only `#print`/`#check` lines; the mirror copy is verbatim.
- Export labels: `ar:thm:transfer` is on hasConvexNGon_of_affine_symmetry, and `ar:thm:main` is on
  heptagon_of_nontrivial_affineEquiv together with the four variants (affine, affineMap, image, coords). Both are as the
  contract requires.
- References: own labels, the fd labels (all exist in fd.tex), sr:def:iso, sr:def:classes, sr:thm:main, sr:thm:variant,
  mb:thm:classes, mb:thm:baek and mb:thm:main3. All are export labels listed in the contract. sr:thm:main
  (sr.tex:893) states heptagon_of_nontrivial_isometry in the form the proof of ar:thm:main uses (E(33,7)).
- Hypotheses: the five classes are presented as hypotheses (title, statement, map note, Remark ar:rem:classes).
  Remark ar:rem:classes names their sources (C2FINAL, C3FINAL, SYM5, SYMZ, SYMLEAN/mirror) with rigor labels that
  agree with SYMLEAN/README.md §5 and §9. hE is stated as a parameter for the same N and n (Theorem ar:thm:transfer,
  Remark ar:rem:hE(1)).
- The section contains no machine paths, no tool names and no "Corollary 3" docstring wording. The existing compile
  log (`build/ar_r1adv_wrapper.log`, newer than the section) has no errors; its only undefined references are fd:, sr:
  and mb: export labels.

## 2. Findings

### F1 (minor): the description of the Axioms file omits a blank line
- Location: ar.tex:39-41 (Rigor and axioms, first bullet).
- Issue: the section says the file "consists of the 1533 lines of SYMLEAN/AffineReduction.lean, followed by nine #print
  axioms lines and one #check line". The file has 1544 lines: 1-1533 are the copy, 1534 is blank, 1535-1543 are the nine
  `#print axioms` lines and 1544 is the `#check` line.
- Evidence: `wc -l` gives 1544; line 1534 is empty.
- Fix: "... followed by a blank line, nine `#print axioms` lines and one `#check` line". Not material.

### F2 (minor): the summary of the Lean proofs of ar:thm:main is inaccurate for part (b)
- Location: ar.tex:665-666.
- Issue: "The Lean proofs are the same one-line applications. They pass heptagon_of_nontrivial_isometry, applied to the
  five hypotheses ..., as hE." For heptagon_of_nontrivial_affineEquiv_image (AffineReduction.lean:1516-1517) the Lean
  proof does not pass hE. It applies `heptagon_of_nontrivial_affineEquiv h2 h3 h5 hm1 hm0` (part (a)) to the converted
  inclusion. The written proof of (b), "Now apply (a)", does match Lean; only the summary sentence is wrong for (b).
  (Each Lean proof is also a two-line term, which is cosmetic.)
- Fix: "For (a), (c), (d) and (e) the Lean proofs pass ... as hE; for (b) the Lean proof converts the inclusion and
  applies (a)."

### F3 (minor): the "Relation to Lean" list for Proposition ar:prop:averaging is incomplete
- Location: ar.tex:534-538.
- Issue: the list after the colon reads as complete, but it leaves out two steps. The orientation factor st of part (b)
  is Lean step `hgp'`, through `generalPosition_image_of_orient (D := s * t - β / s * 0)` and `orient_lin2`
  (AffineReduction.lean:1401-1403). The injectivity of T and T' is `hTinj`/`hTiinj` (1392-1393). Nothing stated is false.
- Fix: add `hgp'`, `hTinj` and `hTiinj` to the list, or say "among them".

### F4 (minor): "word for word" overstates the match of E(N,n) with the type of hE
- Location: ar.tex:456-457 (Definition ar:def:E).
- Issue: the rendering is faithful: same quantifiers, same five premises in the same order, same conclusion. It is not
  literally word for word. The bound variables S and g are renamed S' and h, and `IsEucIsometry` and `Invariant` are
  unfolded.
- Fix: "This is, up to the names of the bound variables, the type of the hypothesis hE".

### F5 (minor): the same letters name different things within ar:thm:main
- Location: ar.tex:636-644.
- Issue: f is a Mathlib affine map in (c) and a real coefficient in (e). b is a vector in (d) and a matrix entry in (e).
  Each part binds its own variables, so the meaning is unambiguous. Corollary ar:cor:transfer-forms(c) adds "(here f is
  a real number)"; Theorem ar:thm:main(e) does not.
- Fix: add the same parenthesis in (e).

### F6 (minor, probably not an error): references to mb: labels
- Location: ar.tex:683, 686, 688, 750 (`mb:thm:classes`, `mb:thm:baek`, `mb:thm:main3`).
- Issue: the task notes say "You may \ref sr: and fd: export labels". The section also refers to three mb: labels.
  These are export labels of section mb listed in the contract table, and the contract allows `\ref` to the export
  labels of other sections. Under the binding contract this is therefore allowed. It is reported only in case the task
  note was meant as a restriction.
- Fix: none needed under the contract.

## 3. Conclusion

All 25 Lean-referenced statements (45 declarations) match their Lean declarations exactly in hypotheses, conclusions and
binder order. The definitions match, the line numbers are exact, coverage is complete, the export labels are on the
right statements, hE is stated precisely as a parameter for the same N and n, and the five classes are presented as
hypotheses. The fidelity lens passes, with minor findings F1-F6.
