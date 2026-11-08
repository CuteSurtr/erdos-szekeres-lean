# Section `mb`, round 1, adversarial lens

Verdict: **PASS**. No blocker or major finding. Nine minor findings are listed below.

Paths: `MIRRORETV/...` and `SYMLEAN/...` are relative to the results directory. `ErdosSzekeres/...` and `docs/...` are
relative to the repository root. RTC = `SYMLEAN/mirror/ReductionThreeClasses.lean`.

## How I checked

- **Lean statements.** I compared every statement environment of `mb.tex` with its Lean declaration: hypotheses,
  conclusion, quantifier order and implicit arguments. I read the sources directly:
  - `ErdosSzekeres/Vendor/ETV/{Config/Defs,Config/Lemmas,Main/Main,Main/CapCup,Lib/List/Defs}.lean`;
  - `ErdosSzekeres/Omission/{Realization,ActualRanks,PlanarChains,ListGeometry,BoundaryGeometry,BaekGeometry,Baek}.lean`;
  - `MIRRORETV/lean/MirrorMain.lean` (lines 1–25, 205–420, 632–840, 1500–2000, 2195–2677);
  - `MIRRORETV/lean/MirrorNine_append.lean` (all of it);
  - RTC lines 1–60, 285–300, 440–530, 1015–1095, 1495–1560 and 4230–4322.
- **Copies, hashes and logs.**
  - The byte-identity claims hold. With `sed` and `diff`, RTC 1562–4236 equals `MirrorMain.lean` 3–2677, RTC 38–1559
    equals `AffineReduction.lean` 12–1533, and RTC 38–1084 equals `SymmetricReduction.lean` 12–1058.
  - All 18 SHA-256 prefixes in the "Sources" list match the files.
  - The cited axiom lines match the logs: `MirrorMain.out` 848–863, `MirrorNine.out` 879–882, and `axioms.out` (whose
    `#check` lines are truncated, as the section says). The appended-file offset of 2677 matches the warning at line
    2746 (append line 69).
- **Grep claims.** No `native_decide`, `sorry` or `axiom` occurs in the three files or in the twelve vendored and
  bridge files. `decide` occurs only on `Fin` comparisons and on C(6,2), C(8,2) and C(9,3).
- **Line numbers.** Every `\leanref` and every `file:line` in the map points at the named declaration. So do all
  in-text line references: Defs.lean:30 and :46, List/Defs:22, BoundaryGeometry:30, :56, :64, :69, :77 and :120,
  MirrorMain:1543, :1886, :2233, :2309, :2403, :2498, :2631, :2636 and :2641, RTC 1023, 1050, 1078, 1503, 1515, 1527,
  1536 and 1547, `SymmetricReduction.lean`:423 and :997, `AffineReduction.lean`:1501.
- **Identities.** I checked these by exact symbolic expansion:
  - the four-point identities (mb:eq:four-left, mb:eq:four-right) and the chord identity (mb:eq:chord);
  - the interior identity of Lemma mb:lem:interior;
  - the four frame identities of Lemma mb:lem:frame and "second coordinate = n0 p0 + n1 p1 − cν";
  - both coordinates of reflLine − lineRefl = 2w_i(u0² + u1² − 1), and the two displayed intermediate forms;
  - orient(mir a, mir b, mir d) = −orient(a, b, d);
  - orient(p, q, mir p) = 0 when x(q) = x(p), and orient = 0 for three points on the axis.
- **Compile and labels.** A standalone compile in a separate directory exits 0 on both passes. There are no errors and
  no overfull boxes. The only undefined references are `fd:`, `mm:`, `sr:` and `ar:` labels. Every `\ref` is to an `mb:`
  label or to an allowed `fd:`, `mm:`, `sr:` or `ar:` export label, and all seven `mb:` export labels are defined on the
  right statements. There are 42 statement environments and 42 map rows. The section has no `\newcommand`,
  `\usepackage`, machine path or tool name.
- **Citation.** I compared Remark mb:rem:baek with the arXiv v2 text of Baek's paper (arXiv:2206.04260, retrieved for
  this review):
  - Theorem 1.6 is "For any n ≥ 3, the statement P(n,4,n) holds. That is, C(n−1,2)+2 points on a plane in general
    position determine either a 4-cap or a n-gon". This matches the remark.
  - Definition 2.4 defines weak and strong gons. This matches "Baek calls such gons weak".
  - Theorem 2.6 is the set-theoretic cups–caps theorem, consistent with `Config.cap_cup`.
  - Theorem 2.7: see finding 1.

## Why each main statement survives the attacks

- **mb:thm:baek (`main`) and mb:thm:capcup (`Config.cap_cup`).** Both are stated exactly as in the Lean source (type
  class, finiteness, thresholds C(n+2,2)+2 ≤ |S| and C(a+b,a) < |S|, conclusions with n+3, a+2 and b+2). Degenerate
  values are not a problem: n = 0 gives threshold 3 and "4-cap or 3-gon", and a = 0 or b = 0 is the 2-cap/2-cup base
  case. Both are cited, not claimed as proved.
- **Bridge (Lemmas mb:lem:signs, mb:lem:four, mb:lem:chain, mb:lem:lists, mb:lem:boundary; Proposition mb:prop:gon).**
  - In Lemma mb:lem:chain, the downward induction and the inner induction (Steps A and B) use exactly the two
    conclusions of (mb:eq:trans), with the right index ranges (k−1 > i+1 in Step A). Lists of length r ≤ 2 are
    vacuous.
  - Lemma mb:lem:lists uses Lemma mb:lem:signs only for increasing triples of indices < n.
  - Lemma mb:lem:boundary:
    - s = 0 or t = 0 (B = {L, R} when s = t = 0) is handled.
    - L ≠ R follows from the strict x-order.
    - U ∩ V = {L, R} is proved, not assumed.
    - The strict cases of (mb:eq:edge) and (mb:eq:upper-edge) cover w = v_j with 0 < j < t+1 through the chord
      identity.
    - Every p ∈ B is L, R, an interior u_i or an interior v_j, and each case has an exposing affine function that is
      strictly positive on B \ {p}. I checked the w = u_{i−1} and w = v_{j+1} subcases.
  - The statement is the Lean `Boundary` structure after the substitution v_j = ρ(w_j). I checked that this is an exact
    equivalence (x preserved, orientation negated, `first_eq` gives u_0 = ρ(ρ(v_0)) = v_0), and Remark mb:rem:boundary
    explains it.
  - Proposition mb:prop:gon: s = |l'|−2 is Lean `l` and t = |l|−2 is Lean `k`, which matches
    `boundaryOfGon : Boundary l k`. The natural-number subtractions are safe because both lengths are ≥ 2.
- **mb:prop:cap16, mb:lem:gc22, mb:prop:cap22, mb:prop:cap113.** These are faithful (`S ⊆ range n` in
  `geometric_capacity22`; `Finset.univ.image c.point`). Thresholds: 17, 23, and 30 in Theorem mb:thm:nine(a).
- **mb:lem:split.**
  - (a) Mirroring is a bijection between R(S) and the points below the axis.
  - (b) Three axis points have orient = 0.
  - (c) p, q and mir p are pairwise distinct (from y(q) ≥ 0 > −y(p)), and orient(p, q, mir p) = 0.
  - The axis-uniqueness hypothesis is exactly that of `injOn_x`.
- **mb:lem:seven-of.** The case split on y(d_0), y(d_3), y(d_1), y(d_2) is exhaustive and matches the Lean `rcases`
  tree. The hypothesis lists of (HL) and (HR) match Lean exactly, including membership order. Counting:
  - if A = ∅, |S| = 2|R| ≤ 32;
  - otherwise |R| + 1 ≤ 16, so |S| ≤ 30 + 2 = 32.

  A key set T with |T| ≤ 3 cannot contain a 4-cap, so small cases are covered.
- **mb:lem:polygons.** The derivation from mm:thm:mirror-polygon and mm:thm:axis-polygon is valid, and those
  statements match `cap_mirror_polygon`, `axis_left_polygon` and `axis_right_polygon`.
  - (a) Adding mir c_0 and then deleting it is fine even if mir c_0 ∈ P already.
  - (c) and (d) use mir a = a because y(a) = 0.

  No circularity: mm refers to mb only in remarks.
- **mb:thm:seven, mb:thm:eight, mb:thm:nine.** All six Lean statements are matched exactly: `sym` as "maps into", the
  hypothesis `n0² + n1² = 1` in the `_line` versions, and the bounds 32, 46 and 226. In Theorem mb:thm:nine(a):
  - Claim 1 uses that the head of a 4-cap in S \ T lies in S, hence in T.
  - Claim 2 uses q < r, r ∈ S and p ∈ T ⊆ S. The 9-cup becomes a 9-gon by `ncup_is_ngon` (9 ≥ 2).

  The proof of (b) and (c) through mm:thm:odd and mm:thm:line uses j = 4 ≥ 2, M = 113 and hypothesis (hM), which is
  exactly Proposition mb:prop:cap113. There is no circularity: Proposition mb:prop:cap113 is proved from part (a)
  before (b) and (c).
- **Lemma mb:lem:transport with m = 0.** The hypothesis "no 0 points in convex position" is unsatisfiable, so the
  lemma holds vacuously.
- **mb:thm:refl32.** The identity holds for all p under u0² + u1² = 1 (checked). Part (b) has no condition on the
  points on the mirror, and the substitution n = (−u1, u0) has n0² + n1² = 1.
- **mb:thm:classes.** Both class definitions (RTC 508 and 514) are restated exactly. The axis hypotheses are unused,
  and the section says so.
- **mb:thm:main3.** Both statements are faithful:
  - `IsEucIsometry` is only the eDist2 identity;
  - `g ≠ AffineEquiv.refl` is the hypothesis of the affine version;
  - "Invariant" means "maps into".

  The theorem is clearly labelled conditional on HalfTurn34, Threefold33 and Fivefold35, in the statement, in the
  status line and in Remark mb:rem:main3. That remark names the certificate records (C2FINAL with C2C34, C3FINAL with
  C3LEAN, SYM5) and their rigour. I verified the status paragraph of `C2FINAL/README.md` and the existence of C3SPOT.
  The uses of sr:thm:main and ar:thm:main rely on the byte-identity, which I verified.

## Findings (all minor)

1. **Remark mb:rem:baek(1), mb.tex:181–183: Theorem 2.7 is stronger than `main`.** In arXiv v2, Theorem 2.7 reads "For
   any n ≥ 3, any configuration of size C(n−1,2)+2 contains either a 4-cap, n-cup or a (3, n−1)-gon". The remark says
   `main` "is" Theorem 2.7, but `main` is its consequence: an n-cup is a weak n-gon (Lemma mb:lem:config-mono(b)), and
   a (3, n−1)-gon is a weak n-gon because 3 + (n−1) = n+2. The section attributes the numbering to
   `MIRRORETV/README.md` §8, which says only "Baek's Theorem 2.7 holds for all colourings with weak gons".
   *Fix:* say that `main` follows from Theorem 2.7 by these two observations.
2. **Remark mb:rem:capcup, mb.tex:204–205: off-by-one.** "Split S into the first entries of (a+2)-caps" is off by one
   relative to the theorem's (a, b). In the vendored induction step (`CapCup.lean`:57–69, parameters (a+1, b+1),
   target (a+3)-cap), T is the set of first entries of (a+2)-caps. For the target (A+2)-cap of `cap_cup A B` this means
   first entries of (A+1)-caps. Theorem mb:thm:nine(a), which "repeats the induction step", splits by 4-caps for the
   target 5-cap (A = 3). *Fix:* write "(a+1)-caps".
3. **Sources, mb.tex:39–41: `Realization.lean` is misattributed.** It is listed among "the bridge files (adapted from
   M. Schroeder's archive, MIT licence)". It is the only one of the seven with no adaptation header (its line 1 is an
   import). `docs/THIRD_PARTY.md` (lines 111–118) says its connections "were added here, using the archive's
   balanced-state/cycle strategy", so it is project code. This is a provenance slip with no mathematical effect.
   *Fix:* list it separately as project code.
4. **mb.tex:71–73 and 92–93, Lemma mb:lem:signs (mb.tex:248): `Configuration.cup_false_iff` is not covered by the axiom
   lines.** The section says the recorded `#print axioms` lines cover the bridge lemmas and that every stated
   declaration is Lean-checked by that evidence. `Configuration.cup_false_iff` (`Realization.lean`:44) is not in the
   dependency cone of any printed theorem. It is used only by `ListGeometry.listCap_of_hasCap` (`ListGeometry.lean`:156)
   and the endingPath lemmas, none of which is on the mirror path; `cap_sign` uses `cup_sign` and `generalPosition`
   directly. It is still compiled as part of an imported module. *Fix:* say so, or drop it from the Lean names of the
   lemma (`cap_sign` is the declaration on the path).
5. **Remark mb:rem:baek(3), mb.tex:191–193: "every N-gon".** The remark says "every N-gon of C_c yields N points in
   convex position (Proposition mb:prop:gon)". Proposition mb:prop:gon is stated only for m ∈ {7, 8, 9}, although its
   proof works for every m. *Fix:* restrict the sentence to N = 7, 8, 9, or note that the proof is general.
6. **Remark mb:rem:generated, mb.tex:645–647: not all four are special cases.** "The generated statements are special
   cases of them" is true for (b), (c) and (d). `cap_mirror_heptagon` (part (a)) is instead a 7-point subset of the
   m = 4 octagon, which needs the deletion step done in the proof. *Fix:* "special cases or sub-polygons of them".
7. **Coverage paragraph (mb.tex:1068–1113) and map.**
   - (i) Several `BoundaryGeometry` helpers on the Lean path of Lemma mb:lem:boundary are neither named in its proof nor
     listed: `supporting_edges_expose`, `affine`, `affine_mix`, `affine_positive_convex`, `point_x_bounds`,
     `first_x_strict`, `last_x_strict`, `reflect_mem_flip`, `Boundary.points`, `Boundary.finite_coe`,
     `reflect_reflect`, `orient_reflect`, `first`, `last`.
   - (ii) The Coverage paragraph lists `Config.Cap3` as covered by Definition mb:def:config, but the map row for
     `mb:def:config` omits it.
8. **Notation overloads.**
   - "Configuration" names both Baek's abstract configurations (Definition mb:def:config) and x-sorted point
     configurations (mb.tex:227–233).
   - The letter c is both a point configuration and the offset of lineRefl in the same passage (statement of Theorem
     mb:thm:nine(c) and proof of (b), (c), mb.tex:871–928).
   - n is both Baek's parameter and the configuration size in the proof of Proposition mb:prop:cap16 (mb.tex:476–477).
   - In Lemma mb:lem:boundary(b) the generic element of B is called v, while the v_j are the cap points.

   No mathematical error results; the issue is readability only.
9. **Optional: duplication with `mm`.** Lemmas mb:lem:polygons, mb:lem:split, mb:lem:sort, mb:lem:frame,
   mb:lem:affine, mb:lem:transport and Definition mb:def:frame restate and reprove declarations that `mm` also covers
   (mm:prop:small-polygons, mm:lem:count, mm:lem:injx, mm:lem:sort, mm:def:frame, mm:lem:frame, mm:lem:ngon,
   mm:thm:line(a)). The two versions agree, and the duplication is forced by the export-label rules. The Coverage
   paragraph could say that `mm` also states them, so the appendix map does not look like conflicting coverage.

## Not findings (attacks that failed)

- Lemma mb:lem:boundary is stated in u/v form rather than with the `Boundary` structure. I checked that the change of
  variables is an exact equivalence, so the statement is faithful. Remark mb:rem:boundary documents it.
- The polynomial identities are justified by "expand". I re-derived all of them; each is checkable by hand.
- Part C's line range 4238–4322 versus the README's 4237–4322: line 4237 is blank, so the section is correct.
