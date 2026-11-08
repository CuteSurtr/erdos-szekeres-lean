# Review of section `ar` (Affine symmetries): round 1, lens: rigor

Verdict: **pass**. I found no blocker and no major finding, and eight minor ones (below).

Paths are relative to STAGE (`sections/`, `build/`) or to RES (`SYMLEAN/...`), as the contract requires.

## What was checked, and how

1. **Statement fidelity, all 45 declarations of `SYMLEAN/AffineReduction.lean` lines 1059–1533.** I compared each
   statement in `sections/ar.tex` with the Lean source line by line: hypotheses, implicit and explicit binders,
   conclusions and side conditions. Specific checks:
   - `0 < n` appears only in `avgQ_ge`, `qA_pos` and `qdisc_pos`; `avgQ_mulVec` needs only `L ^ n = 1`.
   - `s ≠ 0` alone for `nsq_lin2_chol`; `s ≠ 0` and `t ≠ 0` for both inverse lemmas.
   - `hE` has exactly the binder list of lines 1331–1332, 1424–1425, 1434–1435 and 1445–1446.
   - `hN : 3 ≤ N`.
   - `(f : Point → Point) ≠ id` versus `f ≠ AffineEquiv.refl ℝ Point`.
   - `g '' ↑S ⊆ ↑S` in `heptagon_of_nontrivial_affineEquiv_image`.
   - `hdet : a * d - b * c ≠ 0` and the `![…]` form of `hg` in the coordinate versions.
   - The five class premises `h2 h3 h5 hm1 hm0`.

   Every statement is faithful. The order of the ∀-binders and premises sometimes differs from Lean, for example
   "S in general position with N ≤ |S|" is placed before f. These are all universally quantified and independent, so
   the statements are logically identical. There is no ∀/∃ alternation anywhere.
2. **File and line references.** A script compared every `\leanref` in the tex and every `file_line` in
   `sections/ar.map.tsv` with the source line. All 45 names sit exactly on the cited lines. The same holds for the
   other line numbers in the text:
   - `:69` `iterate_mem`, `:265`/`:268` `eDist2`/`IsEucIsometry`, `:271` `Invariant`, `:502` `point_ext`, `:997` in
     both files;
   - `ErdosSzekeres/Orientation.lean:9`, `Basic.lean:15`, `OrientationGeometry.lean:66`;
   - `mirror/ReductionThreeClasses.lean:4274/4282/4303`.
3. **Hashes and provenance.** These SHA-256 prefixes were recomputed and all match:
   - `41cfc0b60aec` `AffineReduction.lean`, `6d5ec90a4215` `SymmetricReduction.lean`, `f6cb9372b174` `AffineReductionAxioms.lean`, `38d0b6f59398` `logs/AffineReductionAxioms.out`;
   - `2425500eefd1` `Definitions.lean`, `f67955ac7091` `Orientation.lean`, `13667aa2d3dc` `Basic.lean`, `c7db9bbbb65e` `OrientationGeometry.lean`.

   The structural claims also hold:
   - Lines 1–1058 equal `SymmetricReduction.lean` 1–1058 (`diff`).
   - `AffineReductionAxioms.lean` equals the 1533 lines plus a blank line, nine `#print axioms` lines and one
     `#check` (`cmp`).
   - `mirror/ReductionThreeClasses.lean` 38–1559 equals `AffineReduction.lean` 12–1533 (`diff`), so the offset +26
     stated in Coverage is right.
   - Toolchain `v4.24.0` and Mathlib rev `f897ebcf72cd…` (`lean-toolchain`, `lake-manifest.json`).
4. **Axioms evidence.**
   - `logs/AffineReductionAxioms.out` lists exactly the nine theorems named, each with `[propext, Classical.choice,
     Quot.sound]`.
   - The `#check` line shows the five classes as premises.
   - `logs/AffineReduction.out` is empty, and `logs/runs.tsv` gives exit 0 on 2026-11-01.
   - The claim that every other in-scope declaration is used, directly or transitively, by one of the nine printed
     theorems holds. I traced each of the 45 declarations to a use in a proof, not only a docstring mention.
   - A scan of lines 1059–1533 for `decide|sorry|admit|native|axiom|ofReduceBool|implemented_by|unsafe|opaque` found
     nothing.
5. **Every algebraic identity, checked with sympy** (`build/ar_rigorr1_sympy.py`, run under `nice -n 15`). All 30
   checks print OK:
   - `nsq_mulVec`;
   - avgQ at (1,0) and at (−β, α), including the displayed middle expression αβ² + 2β(−β)α + γα² = α(αγ − β²);
   - `orient_lin2`, both in core form and in full point form;
   - `orient_affine` with translation;
   - `nsq_lin2_chol`, the two inverse identities, and every displayed intermediate step of Lemma `ar:lem:chol`(b),(c);
   - det T = st;
   - β²/α + (αγ − β²)/α = γ, and TᵀT = [[α, β], [β, γ]] (the Cholesky claim of the introduction);
   - the four polynomial identities of Lemma `ar:lem:fix`;
   - the two Cramer identities of Lemma `ar:lem:inj`;
   - the affine-combination identity of Step 1 of Lemma `ar:lem:cp-affine`;
   - u₀w₁ − u₁w₀ = orient(p₀, p₁, p₂) in Proposition `ar:prop:averaging`(a).
6. **End-to-end check of the construction** (`build/ar_rigorr1_construction.py`). I used exact sympy arithmetic on
   five non-orthogonal or degenerate linear parts:
   - order 3 `[[0,-1],[1,-1]]`, order 6 `[[1,-1],[1,0]]`, order 4 `[[1,-2],[1,-1]]`;
   - order 2 with det −1 `[[1,1],[0,-1]]`, and −I.

   The translation was chosen so that g has a fixed point, as it must when g permutes a set with three
   non-collinear points. In all five cases:
   - nsq(Tz) = avgQ(L, m, z), and avgQ(L, m, Lz) = avgQ(L, m, z);
   - T and T′ are mutually inverse, and det T = st > 0;
   - h = T∘g∘T′ preserves squared distance identically;
   - the order of h equals the order of g, as in Proposition (d).

   A first run with an arbitrary translation gave a glide reflection, which has infinite order. That run confirms
   that the proposition's hypotheses, finite S with three non-collinear points, are needed for (a).
7. **Proof steps, one by one.**
   - Inequality directions: avgQ ≥ nsq; α ≥ 1; α(αγ − β²) ≥ α² + β² ≥ α² > 0, hence αγ − β² > 0; s, t > 0;
     N ≤ |S| = |T(S)|.
   - Inductions: `ar:lem:iter` on k; `iterate_mem` on i inside `ar:lem:periodic`; the common period on r in Prop (a),
     where the base case r = 0 is g⁰ = id and is left implicit; the formula hᵏ = T∘gᵏ∘T′ on k in Prop (d). All are
     well founded.
   - Case splits: the four matrix entries in `ar:lem:fix`, the two coordinates in `ar:lem:inj`, and parts (a)–(e) of
     `ar:thm:main`. All are exhaustive.
   - Every use of an earlier result meets its hypotheses exactly. Examples: Lemma `ar:lem:avgq-pos` is used with
     n = m ≥ 1; `ar:lem:avgq-inv` with Lᵐ = 1; `ar:lem:chol`(b),(c) with s, t ≠ 0; `ar:lem:gp-orient` with
     D = st ≠ 0 or D = det L ≠ 0; `ar:lem:cp-affine` with T′ an injective linear (hence affine) map;
     `ar:lem:periodic` with g injective and S invariant.
   - In Theorem `ar:thm:main`, the instance E(33, 7) is exactly `heptagon_of_nontrivial_isometry h2 h3 h5 hm1 hm0`
     (line 997–1001 binder list), and 3 ≤ 33.
8. **Delegation to Lean.** None. Each Lean or Mathlib name in the text (`AffineMap.decomp`,
   `AffineMap.image_convexHull`, `LinearMap.det_toMatrix'`, `Matrix.det_fin_two_of`, `iterate_mem`) is a pointer next
   to a complete written argument. The one exception is `AffineEquiv.ext` (finding m4), a structural one-liner.
9. **Hypotheses presented as hypotheses.**
   - `hE` is stated in full in Theorem `ar:thm:transfer` and named as a parameter in Remark `ar:rem:hE`(1).
   - The five classes are hypotheses in the statement of `ar:thm:main`, in its map row and in Remark `ar:rem:classes`.
   - The remark's provenance claims match `SYMLEAN/README.md` §1, §5, §6.5 item 3 and §9, and
     `mirror/axioms.out`, which lists only the three standard axioms for `mirrorOneAxis33_proved`,
     `mirrorNoAxis34_proved` and `heptagon_of_nontrivial_affineEquiv_3`. The `_3` statement takes only `h2 h3 h5`.
   - The claim that no order-preserving affine transfer exists in Lean holds: a search of all `.lean` files of the
     checkout finds the transfer only in the SYMLEAN affine files. It also agrees with `WRITEUP/P1/p1.tex:179–182`.
10. **Contract and LaTeX rules.**
    - Compile: I used my own wrapper `build/ar_rigorr1_wrapper.tex` and ran it twice. Both passes exit 0 with
      10 pages, no overfull boxes and no errors. The only undefined references are to `fd:`, `sr:` and `mb:` labels.
    - All `\ref`s go to the section's own labels or to export labels in the contract table (`mb:thm:baek`,
      `mb:thm:classes`, `mb:thm:main3`, `sr:thm:variant` included).
    - No `\newcommand`, `\usepackage` or `\begin{document}`; no machine paths; no tool names; no
      overclaiming words. "Corollary 3" does not appear, and "proved" occurs only inside Lean names.
    - Both export labels are on the right statements.
    - Map: header correct; 30 rows for 30 statement environments, with the same labels in the same order and
      matching kinds.
    - Coverage names all 45 declarations.

## Findings (all minor)

**m1. The description of the Lean proofs at the end of the proof of Theorem `ar:thm:main` is wrong for part (b).**
Location: `sections/ar.tex:665–666`. The text says: "The Lean proofs are the same one-line applications. They pass
`heptagon_of_nontrivial_isometry`, applied to the five hypotheses …, as `hE`." For
`heptagon_of_nontrivial_affineEquiv_image`, the Lean proof (`SYMLEAN/AffineReduction.lean:1516–1517`) is
`heptagon_of_nontrivial_affineEquiv h2 h3 h5 hm1 hm0 S g hgp hcard hne (fun p hp => …)`. It applies part (a) after
turning the image inclusion into `Invariant`, and passes no `hE`. The written proof of (b) ("Now apply (a)") is
correct and matches Lean; only the summary sentence is inaccurate. Suggested fix: "For (a) and (c)–(e) the Lean proofs
are one-line applications that pass … as `hE`; for (b) the Lean proof applies (a)."

**m2. The letter b is reused inside a scope where it already names the translation.**
- Proof of Lemma `ar:lem:orient-affine` (`ar.tex:350–352`): the hypothesis is g(p) = Lp + b, and the proof then sets
  "(a,b,c,d) = (L₀₀, L₀₁, L₁₀, L₁₁)".
- Proof of Proposition `ar:prop:averaging`(b) (`ar.tex:504–505`): "(a,b,c,d) = (s, β/s, 0, t)", while b is the
  translation of g in the proposition's hypotheses.
- Similar collisions, with no effect on correctness: g_A, g_B, g_C (Gram entries, Definition `ar:def:gram`) against
  the map g; the matrix called N in "M(Nz) = (MN)z" (`ar.tex:79`) against the threshold N; s as a finite set in
  Lemma `ar:lem:cp-affine` against s = √α.

Corollary (c) already avoids this with b′. Suggested fix: write "the parameters of Lemma `ar:lem:lin2` are
(L₀₀, L₀₁, L₁₀, L₁₁)…" without reusing b, or rename the lin2 parameters in those two proofs (for example (a′,b′,c′,d′)).

**m3. "Relation to Lean" in the proof of Proposition `ar:prop:averaging` omits one step.**
Location: `ar.tex:534–538`. The list of Lean steps behind (b) and (c) leaves out the orientation factor of T. In Lean
this is `hgp'` (`SYMLEAN/AffineReduction.lean:1401–1403`), which calls `generalPosition_image_of_orient` with
`D := s * t - β / s * 0` and `orient_lin2`. The statement of (b) includes this fact. Suggested fix: add `hgp'` to the
list.

**m4. "Two affine equivalences with the same map are equal" is asserted with only a Mathlib name as justification.**
Location: `ar.tex:116–117`; used in the proof of Corollary `ar:cor:transfer-forms`(b), `ar.tex:614–616`. The section
itself defines an affine equivalence as a bijection *together with* a linear bijection f_lin. So the claim needs the
observation that f_lin is determined by f, which is a one-line identity:

    f_lin(v) = f(v + 0) − f(0).

Without it, the text leans on `AffineEquiv.ext`. This is a standard fact, and a competent reader supplies it at once,
so it is minor. Suggested fix: add "since f_lin(v) = f(v) − f(0) is determined by the map".

**m5. The overview claims more than it states.**
Location: `ar.tex:16–17`. "The symmetry g(p) = Lp + b permutes the finite set, so its linear part satisfies Lᵐ = 1."
Permuting a finite set does not by itself give Lᵐ = 1. For a one-point set fixed by g, L can be any invertible
matrix. The set must contain three non-collinear points, which the formal statements ensure through general position
and |S| ≥ N ≥ 3. Only the overview is affected; Proposition `ar:prop:averaging` and Theorem `ar:thm:transfer` are
correct. Suggested fix: "…permutes the finite set, which contains three non-collinear points, so…".

**m6. Remark `ar:rem:classes` lists only part of what supplies `HalfTurn34` and `Threefold33`.**
Location: `ar.tex:689–694`. The remark names SAT certificates, written encoder proofs and the perturbation argument.
README §5 also lists other written or computational ingredients:
- for `HalfTurn34`: the hull cover, reductions A and B (written proofs), and the composition (exact computation, with
  Lean-checked bookkeeping);
- for `Threefold33`: the normal form `C3-S/soundness.md` and the two composers.

The remark cites README §5 and the rigor label "computer-assisted" is right, so contract rule 7 is met. Suggested fix
(optional): "…and on further written reductions and exact composition checks listed in `SYMLEAN/README.md` §5".

**m7. "Word for word" overstates.**
Location: `ar.tex:456`. "This is, word for word, the type of the hypothesis `hE`." The definition is a faithful
paraphrase of the curried Lean type, with S′ and h in place of S and g, not a literal copy. Suggested fix: "This is
exactly the type of …, with S′ and h in place of S and g".

**m8. One line of the axioms file is not mentioned.**
Location: `ar.tex:39–41`. "`AffineReductionAxioms.lean` … consists of the 1533 lines …, followed by nine `#print
axioms` lines and one `#check` line." The file has 1544 lines; line 1534 is blank. This has no effect.

## Evidence files (STAGE-relative)

- `build/ar_rigorr1_sympy.py`: 30 identity checks, output `ALL_OK`.
- `build/ar_rigorr1_construction.py`: exact end-to-end check of Proposition `ar:prop:averaging` on five linear
  parts, output `ALL_OK`.
- `build/ar_rigorr1_wrapper.tex`, `build/ar_rigorr1_pass1.log`, `build/ar_rigorr1_pass2.log`,
  `build/ar_rigorr1_wrapper.log`: compile check, exit 0 twice.
- `build/ar_rigorr1_decls.txt`: the 45 in-scope declaration names, used for the checks of coverage, map and axioms.
