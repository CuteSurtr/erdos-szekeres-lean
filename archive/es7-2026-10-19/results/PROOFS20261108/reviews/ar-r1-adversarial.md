# Review of section `ar` (Affine symmetries), round 1, lens: adversarial

Verdict: **pass** (no blocker, no major; four minor findings).

Files reviewed: `sections/ar.tex` (752 lines), `sections/ar.map.tsv` (30 rows), against
`SYMLEAN/AffineReduction.lean:1059-1533` (paths relative to the results root RES unless they start with
`ErdosSzekeres/` or `sections/`), `SYMLEAN/README.md` (sections 1-9), `SYMLEAN/logs/AffineReductionAxioms.out`,
`SYMLEAN/logs/runs.tsv`, `SYMLEAN/mirror/ReductionThreeClasses.lean:4270-4322`, `SYMLEAN/mirror/axioms.out`,
`WRITEUP/P1/p1.tex:160-183`, `AUDIT3/reports/A1_reduction.md`, the inventory `inventory/SYMLEAN-core.json`, and the
statement of `sr:thm:main` / `sr:def:iso` in `sections/sr.tex`.

## Findings

### F1 (minor) - overview sentence omits the spanning hypothesis
- Location: `sections/ar.tex:16-17` (introductory "The idea is as follows").
- Text: "The symmetry g(p)=Lp+b permutes the finite set, so its linear part satisfies L^m=1 for some m>=1."
- Problem: as written this is a non sequitur. It needs the set to contain three non-collinear points.
  Counterexample to the sentence read literally: S = {0}, g(p) = 2p. g is injective and maps S into S, but L = 2*1
  has no finite order. The same happens for any collinear S with a map scaling the orthogonal direction.
- Effect: none on the formal content. Proposition `ar:prop:averaging`(a) and Theorem `ar:thm:transfer` carry the
  needed hypotheses (general position, |S| >= N >= 3), and the proof of (a) uses them.
- Suggested fix: "permutes the finite set, which contains three non-collinear points, so ...".

### F2 (minor) - closing sentence of the proof of Theorem ar:thm:main over-generalises the Lean proofs
- Location: `sections/ar.tex:665-666`.
- Text: "The Lean proofs are the same one-line applications. They pass heptagon_of_nontrivial_isometry, applied to
  the five hypotheses h2, h3, h5, hm1 and hm0, as hE."
- Problem: this holds for four of the five theorems. `heptagon_of_nontrivial_affineEquiv_image`
  (`SYMLEAN/AffineReduction.lean:1516-1517`) passes no hE. It calls `heptagon_of_nontrivial_affineEquiv` after turning
  the inclusion `g '' S ⊆ S` into `Invariant g S`. The written proof of (b) ("Now apply (a)") follows Lean correctly;
  only the summary sentence is inaccurate.
- Suggested fix: "Four of them pass ... as hE; the image form applies (a), as in Lean."

### F3 (minor) - description of the axioms file omits a blank line
- Location: `sections/ar.tex:39-41`.
- Text: "consists of the 1533 lines of SYMLEAN/AffineReduction.lean, followed by nine #print axioms lines and one
  #check line."
- Evidence: `SYMLEAN/AffineReductionAxioms.lean` has 1544 lines: lines 1-1533 match `AffineReduction.lean` (diff),
  line 1534 is blank, and lines 1535-1544 are the 9 `#print axioms` lines and the `#check` line.
- Effect: none. Optional fix: "followed by a blank line, nine ... and one ...".

### F4 (minor) - "word for word" overstates Definition ar:def:E
- Location: `sections/ar.tex:456-457`.
- Text: "This is, word for word, the type of the hypothesis hE".
- Problem: the definition is a faithful paraphrase, not a literal copy. It renames the bound variables
  (S to S', g to h) and unfolds `IsEucIsometry` and `Invariant`. I checked the content and it matches Lean exactly:
  the same quantifiers in the same order, the same five premises in the same order, and the same conclusion. Only
  the wording "word for word" is too strong.
- Suggested fix: "This is the type of the hypothesis hE, with IsEucIsometry and Invariant unfolded and the bound
  variables renamed."

## Attacks on the main statements and why they survive

### Theorem ar:thm:transfer (`hasConvexNGon_of_affine_symmetry`, `SYMLEAN/AffineReduction.lean:1330`)
- Fidelity: the written statement follows the Lean binders one by one, in the same order:
  N, n; hE (for all S, g: GeneralPosition S, N <= card S, IsEucIsometry g, g != id, Invariant g S give
  HasConvexNGon n S); hN: 3 <= N; S, g, L, b; hg: for all p, g p = L p + b; hinj; hgp; hcard; hne; hinv.
  `IsEucIsometry` is unfolded correctly (eDist2 for all p, q in the plane, `:268`), and `Invariant` is unfolded
  correctly (maps into, `:271`). As NOTES requires, hE is stated as a parameter, the Euclidean statement for the same
  N and n, in the theorem, in Definition ar:def:E and in Remark ar:rem:hE(1).
- Degenerate inputs:
  - n = 0: the conclusion holds trivially (the empty set), and the proof still goes through.
  - N <= 2: excluded by hN.
  - card S = 3: Proposition (a) still finds three non-collinear points.
  - g != id but g = id on S: impossible under the hypotheses. Fixing three non-collinear points forces L = 1 and then
    b = 0, so the case cannot arise and nothing is assumed silently.
  - g not injective (for example L = 0, b in S): excluded by hinj. Remark ar:rem:hE(3) says correctly that
    injectivity is a separate hypothesis.
  - The sup-metric trap is avoided: the section uses eDist2 throughout (`sections/ar.tex:98-103`).
- Proof (written step Proposition ar:prop:averaging plus the theorem's proof), checked line by line:
  - (a) Lemma ar:lem:periodic gives the periods, and m = m0 m1 m2 is a common period. Lemma ar:lem:iter gives
    L^m(p1-p0) = p1-p0 and L^m(p2-p0) = p2-p0, and det = orient(p0,p1,p2) != 0, so L^m = 1 by Lemma ar:lem:fix.
    Then g^m = id. The proof is correct. It is not in Lean, and the section says so.
  - (b) Lemma ar:lem:avgq-pos needs only m >= 1. s = sqrt(alpha) > 0 and t = sqrt(disc/alpha) > 0. The Cholesky
    identity and both inverse identities hold. The orientation factor is st - (beta/s)*0 = st > 0, and
    beta^2/alpha + (alpha gamma - beta^2)/alpha = gamma.
  - (c) The chain eDist2(hx,hy) = nsq(T(Lw)) = avgQ(Lw) = avgQ(w) = nsq(Tw) = nsq(x-y) is correct. It uses L^m = 1
    only in Lemma ar:lem:avgq-inv, whose case n = 0 is also handled.
  - (d) h^k = T g^k T' by induction. h^k = id holds if and only if g^k = id, using that T is injective. Hence
    h != id if and only if g != id, and h and g have the same order. The proof is correct, and the section labels
    it as not in Lean.
  - The pull-back V = T'(U) is a subset of S, has card n because T' is injective, and is in convex position by
    Lemma ar:lem:cp-affine, since T' is linear, hence affine, and injective. This matches Lean lines 1413-1420.
- Exact symbolic check with sympy 1.13.3:
  - all identities used: orient_lin2, nsq_lin2_chol, both inverse identities, the written formula for T'x, the gamma
    identity, the evaluation of the form at (-beta, alpha) as written, the four linear combinations of
    matrix_eq_one_of_fix, the two of injective_of_affine, and nsq_mulVec;
  - an end-to-end run on the non-orthogonal order-3 matrix L = [[0,-1],[1,-1]] with b = (1,2): it gives
    (alpha, beta, gamma) = (4, -2, 4) and T L T^{-1} = rotation by 2pi/3 (orthogonal, det 1);
    nsq(Tz) = avgQ(L,3,z); and for k = 1..6, h^k = id exactly when g^k = id (k = 3, 6).
  - All checks returned 0 or True.
- No circularity. Every lemma cited in the proofs appears earlier in the section, or is an fd: or sr: export label.
  The proofs use nothing from fd:lem:affine-orient or fd:lem:affine-cp; those are mentioned only as identifications.

### Corollary ar:cor:transfer-forms (`:1423`, `:1433`, `:1444`)
- (a) AffineMap: the statement has Injective f and (⇑f) != id. The proof uses affineMap_eq_mulVec (via
  AffineMap.decomp) and is correct.
- (b) AffineEquiv: the statement has f != refl. The proof uses f.injective, and AffineEquiv.ext turns f != refl into
  ⇑f != id. Correct.
- (c) Coordinates: the statement has ad - bc != 0, g p = (a p0 + b p1 + e, c p0 + d p1 + f), and the clash between
  the real f and the vector b is handled explicitly (b'). det = ad - bc (det_fin_two_of), and injectivity follows
  from Lemma ar:lem:inj. Correct.
- The binders in (a)-(c) are permuted (S's premises come before f) only among independent premises. The order of
  quantifiers over S and f is unchanged.

### Theorem ar:thm:main (five heptagon theorems, `:1477`, `:1489`, `:1501`, `:1510`, `:1521`)
- Fidelity:
  - All five match Lean, including the explicit binders for the five classes (h2, h3, h5, hm1, hm0), 33 <= card S,
    and != refl versus != id.
  - The image form `g '' (S : Set Point) ⊆ S` is stated as an inclusion of sets and converted to maps-into.
  - The theorems are labelled conditional in the head, the statement and the introduction. Remark ar:rem:classes
    names the records and rigor labels.
  - The theorem's proof states E(33,7) and checks it against `sections/sr.tex`. Theorem sr:thm:main, after the five
    classes are assumed, has exactly the premises GeneralPosition, 33 <= card, IsEucIsometry, g != id and Invariant,
    and the conclusion HasConvexNGon 7.
- Remark ar:rem:classes, checked against the sources:
  - the class summaries agree with the definitions at `SYMLEAN/AffineReduction.lean:467-492`: exact sizes, c not in
    S, angles 2pi/3 and 2pi/5, unit u, exactly one fixed point or none;
  - the line numbers 4274, 4282 and 4303 in `SYMLEAN/mirror/ReductionThreeClasses.lean` are right, and
    `heptagon_of_nontrivial_affineEquiv_3` assumes only HalfTurn34, Threefold33 and Fivefold35;
  - `SYMLEAN/mirror/axioms.out` shows only the three standard axioms;
  - README sections 5 and 9 support the rest: C2FINAL, C3FINAL and SYM5 computer-assisted; SYMZ certificates for
    the mirror classes; deleted proofs for the parallelogram pieces and for the 116,883 pieces of Threefold33;
    the perturbation argument for Threefold33 and Fivefold35. (SYM5 route P1 needs no layer lemma, so no layer-lemma
    dependency is omitted.) The record directories SYMZ, SYM5, C2FINAL and C3FINAL exist.
- Remark ar:rem:hE(2) and the P1 cross-references are accurate:
  - `WRITEUP/P1/p1.tex:173-182` (Remark rem:affine) asks for the order-preserving form and says it is not formalized.
  - Searching every .lean file of the checkout for avgQ, hasConvexNGon_of_affine and affine_symmetry finds only
    AffineReduction, its axioms copy and the mirror copy. No order-preserving transfer exists anywhere.

### Supporting lemmas (all 46 declarations of lines 1059-1533)
- Every declaration is stated at its exact line (all 46 checked) and listed in Coverage.
- The side conditions match Lean:
  - s != 0 (nsq_lin2_chol); s != 0 and t != 0 (the two inverse lemmas);
  - 0 < n (avgQ_ge, qA_pos, qdisc_pos); only L^n = 1 (avgQ_mulVec);
  - det L != 0 (generalPosition_image_affine, injective_of_affine); D != 0 without injectivity
    (generalPosition_image_of_orient);
  - injective AffineMap (convexPosition_image_affine, hasConvexNGon_image_affine); AffineEquiv
    (generalPosition_image_affineEquiv).
- The degenerate cases hold:
  - n = 0 sums are 0;
  - avgQ_mulVec at n = 0 is trivially true, as the section notes;
  - cp-affine on the empty set and gp-orient on sets with fewer than 3 points are vacuous;
  - the x/0 = 0 convention is stated for T and T'.
- The proof of Lemma ar:lem:cp-affine Step 1 proves both inclusions of f(conv A) = conv f(A) (image of a convex set,
  and preimage of a convex set). Step 2 uses injectivity for f(s) \ {f q} = f(s \ {q}).
- Tacit uses from lines 1-1058: an identifier scan shows that the affine part uses only eDist2, IsEucIsometry,
  Invariant, the five classes, heptagon_of_nontrivial_isometry, iterate_mem and point_ext. All are named in Sources
  or Coverage, at lines 265, 268, 271, 997, 69 and 502, and all of these lines are correct.

## Bookkeeping checks (all passed)
- SHA-256 prefixes recomputed:
  - `SYMLEAN/AffineReduction.lean` 41cfc0b60aec;
  - `SYMLEAN/SymmetricReduction.lean` 6d5ec90a4215;
  - `ErdosSzekeres/Definitions.lean` 2425500eefd1;
  - `ErdosSzekeres/Orientation.lean` f67955ac7091;
  - `ErdosSzekeres/Basic.lean` 13667aa2d3dc;
  - `ErdosSzekeres/OrientationGeometry.lean` c7db9bbbb65e;
  - `SYMLEAN/AffineReductionAxioms.lean` f6cb9372b174;
  - `SYMLEAN/logs/AffineReductionAxioms.out` 38d0b6f59398.
  All match.
- Copies:
  - lines 1-1058 of AffineReduction equal lines 1-1058 of SymmetricReduction (diff);
  - lines 1-1533 of the axioms file equal AffineReduction (diff);
  - lines 38-1559 of the mirror file equal AffineReduction 12-1533 (offset +26, diff).
- Logs:
  - `AffineReduction.out` is empty, and runs.tsv records exit 0 on 2026-11-01;
  - the axioms log lists the nine theorems with [propext, Classical.choice, Quot.sound], and the #check line shows
    the five classes as premises;
  - lines 1059-1533 contain no decide, native_decide, sorry, admit or axiom.
- Toolchain: lean-toolchain v4.24.0; lake-manifest pins mathlib f897ebcf72cd.
- Repository facts:
  - namespace ErdosSzekeres.SymReduction (lines 54-1533);
  - Definitions.lean (Point, GeneralPosition, ConvexPosition, HasConvexNGon);
  - Orientation.lean:9 (orient), Basic.lean:15 (convexPosition_iff), OrientationGeometry.lean:66
    (generalPosition_iff_orient_ne_zero).
- LaTeX:
  - all labels carry the prefix ar:, and both export labels are defined on the right statements;
  - every \ref goes to ar:, fd: or an allowed export label (sr:def:iso, sr:def:classes, sr:thm:main, sr:thm:variant,
    mb:thm:baek, mb:thm:classes, mb:thm:main3);
  - no \newcommand, \def or other macro definitions, and no machine paths or tool names;
  - two compile passes of `build/ar_r1adv_wrapper.tex` both exit 0, with no errors, no "Missing" and no overfull
    boxes; the only undefined references are fd:, sr: and mb: labels.
- Map: 30 rows with 5 tab-separated columns each. They match the 30 statement environments one to one, with the same
  label and kind. The notes record the conditional hypotheses and the written steps.
