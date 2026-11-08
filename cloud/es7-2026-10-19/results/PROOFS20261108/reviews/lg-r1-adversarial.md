# Review of section `lg` (Geometry of the layers: nesting, chains and polar rules), round 1, lens: adversarial

Verdict: **pass** (no blocker, no major; five minor findings).

Files reviewed: `sections/lg.tex` (854 lines) and `sections/lg.map.tsv` (31 rows). I checked them against
`LAYERLEAN/LayerLemma.lean`, reading lines 1-460 for the definitions and the layer-lemma results used, and
lines 460-1036 for the scope. I also used `LAYERLEAN/README.md`, `LAYERLEAN/logs/axioms.log`, `LAYERLEAN/logs/build.log`,
`LAYERLEAN/logs/axioms_recheck_20261106/{out.txt,README.txt,LayerLemmaAxioms.lean}`, `LEANEXT/review/axioms.log`,
`LEANEXT/review/REPORT.md`, `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry}.lean`,
`ErdosSzekeres/Suk/OrientationClique.lean`, `inventory/LAYERLEAN.json`, and the `ll:`/`fd:` statements that lg cites
(`sections/ll.tex`, `sections/fd.tex`). Paths are relative to the results root RES, unless they start with
`ErdosSzekeres/` (repository root) or with `sections/`, `build/`, `inventory/` (staging area).

## Method

1. **Fidelity.** I compared all 27 scope declarations (23 theorems and 4 definitions) binder by binder with
   the Lean source: hypotheses, implicit and explicit order, strict vs weak inequalities, `j ≤ m` vs `j < m`,
   natural-number subtraction, casts, and `Finset` membership.
2. **Symbolic algebra.** `build/lg_r1adv_sympy.py` (sympy 1.13.3) ran 56 independent checks, and all passed.
   - The identities checked are: rotation facts (a)-(d); `R_θX = cosθ X + sinθ JX`; the five `J` identities;
     `orient_rotAbout` as a *polynomial* identity in independent symbols for cos α, sin α, cos β, sin β (this confirms
     the claim that no Pythagorean relation is used); `trig_layer` and its displayed intermediate step; the Remark
     formula `F = 4 sin(π/m) sin(jπ/m) sin((j-1)π/m)`; the three angle facts in `orient_next_prev_pos`;
     `lin_rotAbout`; the affinity (O4); the `convex_disk` identity; the three Cramer identities and the 3×3
     expansion; the `orient_trans_halfplane` key identity; the `fan_step` key identity together with all six `det`
     rewrites in its proof and the displayed Cramer instance; `orient_eq_lin`; the `lin_pos_of_peel` key identity for
     five *arbitrary* points, with its three `det` rewrites; the half-turn `rotAbout(c,π)p = 2c-p` and
     `orient(p,c,2c-p)=0`; `k·2π/(2k)=π`; `orient_polar` and its two intermediate steps; `sin(z+2π)=sin z`; the
     rule-B decomposition and the specialisation of `orient_polar` used there; `sin` addition.
   - Negative control: the checker flags `sin x - cos x` and a sign-flipped `lin_rotAbout` as FAIL.
3. **Proof steps.** I checked every step, including every instantiation of a hypothesis inside the inductions of
   `fan_positive` (the index ranges `s+1<n`, `s+2<n`, `i<s+1<n`, `i<t<n`).
4. **Numeric attacks.** `build/lg_r1adv_numeric.py` ran 200 random pairs (c,x) with m = 1..9 and j = 0..m.
   - `orient_regular_nonneg` and the Remark formula hold; for m ≥ 2 the value is zero exactly for j ∈ {1, m}.
   - `lin_orbit_pos` holds for 0 < j < m, and `orient_next_prev_pos` for m ≥ 3.
   - On the review instance S4 = {(±2,0),(0,±2),(±½,±½)}, c = 0, m = 4: strict nesting holds for all 16 pairs, the
     tangent half-plane condition for all pairs in both layers, and the radius order.
   - The m = 2 segment argument of Remark (2) after Theorem `lg:thm:nesting` holds: the orientation is 0 for λ ∈
     {0, ¼, ½, 1}.
5. **Records.** All nine SHA-256 prefixes in the Sources/Axioms paragraphs match the files.
   - `LAYERLEAN/logs/axioms.log` prints exactly 16 of the 23 scope theorems; the 7 missing are exactly the ones named.
   - `LEANEXT/review/axioms.log` prints all 23, each with `[propext, Classical.choice, Quot.sound]`, out of 59 printed
     declarations.
   - The 2026-11-06 re-check lists exactly 11 scope theorems.
   - The Lean file has 1148 lines and no `sorry`/`admit`/`axiom`/`native_decide`. `lakefile.toml` has only
     `lean_lib ErdosSzekeres` as default target. `build.log` records exit 0 with 0 message lines.
   - The four copies named in Coverage contain lines 11-1147 verbatim (diff).
6. **Compile.** `build/lg_r1adv_wrapper.tex`, two `pdflatex` passes: exit 0, only undefined `fd:`/`ll:` references
   (41 warnings, all to export labels allowed by the contract), no overfull boxes, 10 pages.
7. **Labels, refs and map.**
   - All 13 export labels are defined on the right statements. Every `\ref` points to an own label, a contract
     `fd:` label or an `ll:` export label, and the referenced `fd:`/`ll:` labels exist in `fd.tex`/`ll.tex` with
     matching content.
   - The map has 31 rows with 5 tab-separated columns, one per statement environment. Kinds, Lean names and
     file:line agree with the `\leanref` heads, and the "written step" tags are present.
   - The tex and map contain no machine paths and no tool names.

## Findings

### F1 (minor): the qualifier "non-simp" is attributed to REPORT.md, which does not say it
- Location: `sections/lg.tex:46-48`.
- Text: "The review log LEANEXT/review/axioms.log ... which according to LEANEXT/review/REPORT.md covers all 59
  non-simp theorems of the reviewed file ..."
- Evidence: `LEANEXT/review/REPORT.md` (Results, item 2) says "All 59 theorem declarations were checked", and F6
  says "the file has 59 theorems in all". It never says "non-simp". In fact `LAYERLEAN/LayerLemma.lean` has 66
  `theorem` declarations, 7 of them `@[simp]` (grep), and the review log prints 59 declarations, which are exactly the
  non-simp ones. So the section's count is right, but the qualifier is the inventory's, not REPORT.md's, and
  REPORT.md's own wording is inaccurate.
- Effect: none on correctness; a records-level misattribution.
- Suggested fix: "... prints 59 declarations, namely all theorems of the file except its 7 `@[simp]` lemmas
  (REPORT.md speaks of 'all 59 theorem declarations') ...".

### F2 (minor): the Coverage list of verbatim copies is incomplete
- Location: `sections/lg.tex:848-853`.
- Text: "the verbatim copies of these declarations in other units, which are duplicates; each of the following files
  contains lines 11--1147 of LAYERLEAN/LayerLemma.lean verbatim: [four files]".
- Evidence: a repository-wide grep for `theorem chain_clauses_sound` finds eight copies besides the canonical file.
  Besides the four listed, these also contain lines 11-1147 verbatim (I diffed the 1137-line block):
  - `LEANEXT/capstone/Capstone.lean`
  - `LEANEXT/linked/Linked.lean`
  - `LEANEXT/review/VacuityTest.lean`
  - `LAYERLEAN/logs/axioms_recheck_20261106/LayerLemmaAxioms.lean`
- Effect: none (the copies are out of scope). The sentence reads as an exhaustive list.
- Suggested fix: add the four files, or write "for example".

### F3 (minor): the "lines 465--1032" sentence is literally too broad
- Location: `sections/lg.tex:26-27`.
- Text: "Every Lean declaration stated in this section is in the file LAYERLEAN/LayerLemma.lean ..., lines 465--1032".
- Evidence: the section also states, with Lean names, recalled results outside that range:
  - (L1) `subset_convexHull_hullVerts` (`:146`);
  - (L3) `invariant_peel` (`:386`);
  - (L4) `hullVerts_eq_orbitFS_rotAbout` (`:364`);
  - in the Notation, `orbitFS` (`:48`).

  The definitions `Invariant` (`:105`), `rotAbout` (`:298`), `hullVerts` (`:111`) and `peel` (`:374`) are also used
  outside the range. All of these are recalled from `ll`/`fd`, so nothing is mis-cited; only the sentence is
  imprecise.
- Suggested fix: "Every Lean declaration that heads a statement of this section ...".

### F4 (minor): the main-library list in Sources omits `orient_cycle`
- Location: `sections/lg.tex:29-38`.
- Evidence: the Lean proof of `hasConvexNGon_of_fan` uses `ErdosSzekeres.orient_cycle` (`LAYERLEAN/LayerLemma.lean:742,
  747, 767, 772`; defined at `ErdosSzekeres/Orientation.lean:15`). The list "From the main library the section uses
  the following" names `orient`, `generalPosition_iff_orient_ne_zero` and `Suk.convexPosition_of_positive_triples`,
  but not `orient_cycle`.
- Effect: none. The written proofs use the counterpart `fd:lem:orient`(b), which the Dependencies paragraph cites.
- Suggested fix: add `ErdosSzekeres.orient_cycle` (`ErdosSzekeres/Orientation.lean:15`), or write "among others".

### F5 (minor): "written steps ... collect facts that the Lean proofs establish inline" is too strong for two of them
- Location: `sections/lg.tex:57-58` and `:841-842`.
- Evidence:
  - The general Cramer identity (`lg:lem:cramer`) is not established by any Lean proof. Lean proves only the three
    specific instances, each by `ring` (`LayerLemma.lean:632-634, 644-646, 901-904`).
  - The composition rule `lg:lem:rotfacts`(b) corresponds to the helper lemma `crot_comp` (`:262`) used through
    the complex form, not to an inline step.
- Effect: wording only. Both written steps are fully proved in the section.
- Suggested fix: "they are devices of the written proofs; Lean proves the corresponding instances inline (by `ring`)
  or through helper lemmas".

## Attacks on the main statements and why they survive

- **`lg:lem:rot-iter`** (`rotAbout_iterate`, `:465`).
  - Fidelity: the statement is over all c, all real α and all natural j, as an equality of maps with j cast to ℝ.
  - Attacks: j = 0 (both sides are the identity, since 0·α = 0); the order of the iterate recursion (f∘f^j vs f^j∘f,
    noted as equal in the text).
  - Sympy confirms the composition rule R_αR_β = R_{α+β} coordinatewise.
- **`lg:lem:orient-rot`** (`:472`).
  - Fidelity: exact, for all c, x, α, β.
  - Attack: whether the proof secretly needs cos² + sin² = 1. Sympy verifies it as a polynomial identity in four
    independent symbols, so the claim "No relation between cos and sin is used" is true.
- **`lg:lem:trig`** (`:480`). The identity holds for all s, t (sympy), and the intermediate line is correct.
- **`lg:lem:regular`** (`:488`).
  - Fidelity: the range `j ≤ m` is kept (contract NOTE), with `0 < m`.
  - Attacks: j = 0 (handled separately: F = 0); j = m (ρ^m x = x, value 0); m = 1 (t = π, all factors still ≥ 0);
    x = c (value 0).
  - Remark: for m ≥ 2 the value vanishes exactly for j ∈ {1, m}. This was confirmed numerically, and analytically:
    sin(jπ/m) = 0 iff j ∈ {0, m}, and sin((j-1)π/m) = 0 iff j = 1 within 1 ≤ j ≤ m.
- **`lg:lem:lin-rot`, `lg:lem:lin-orbit`** (`:794`, `:801`).
  - Fidelity: exact, with p ≠ c, 0 < m, 0 < j < m.
  - The angle θ = j·2π/m lies strictly inside (0, 2π), so 1 - cos θ > 0.
  - For m = 1 the statement is vacuous, and m = 2, j = 1 gives 1 - cos π = 2. Checked numerically.
- **`lg:lem:next-prev`** (`:830`). The cast of `m - 1` is legitimate (m ≥ 3). At the boundary m = 3, π - 2t = π/3 > 0.
  The angle facts (m-1)t = π - t and (m-1)t - t = π - 2t were checked with sympy.
- **`lg:lem:halfplane-convex`, `lg:lem:disk`, `lg:def:dist2`** (`:516`, `:1002`, `:999`). The affinity (O4) and the
  identity u|A|² + v|B|² - |uA+vB|² = uv|A-B|² (with u+v = 1) were checked with sympy. The radius R can be any real;
  the empty set is convex.
- **`lg:thm:nesting`** (`strict_nesting`, `:529`).
  - Fidelity: all seven hypotheses and `n < n'` match.
  - Attack m = 2. Remark (2) is a valid derivation: L = {x, ρx}, and y in the segment forces orient = 0, which
    contradicts the (proved) conclusion, so the hypotheses never hold together. This was confirmed numerically.
  - Attack "x ≠ ρx silently assumed": it is proved via `lin_orbit_pos` with j = 1 < m. That needs m ≥ 2, which holds.
    `lin_orbit_pos` is proved earlier and independently of nesting, so the argument is not circular.
  - y ∉ L comes from Lemma `lg:lem:layer`(d). General position is applied to the triple (x, ρx, y), which lies in S
    by (b) and (L2). The proof uses no K-freeness beyond (L4).
  - S4 instance: all 16 (layer-0 vertex, layer-1 point) pairs are positive.
- **`lg:lem:centre`** (`:582`).
  - Fidelity: no `c ∉ S` and no K-freeness, exactly as in Lean.
  - Attacks: m = 2 (k = 1, half-turn); m = k + k gives m/2 = k; the cast 2πk/(2k) = π (sympy);
    q = 2c - p (sympy); orient(p, c, q) = 0 (sympy); the distinctness of p, c, q, all three cases.
  - The counterexample S = {c} in the Remark is correct (ρ(c) = c, and S is vacuously in general position).
- **`lg:thm:radius`** (`dist2_le_of_later`, `:1012`).
  - Fidelity: the inequality is weak, `n ≤ n'` (so n = n' is allowed), and there is no general position, as in Lean.
  - Attacks: n = n' with y = x (equality); m = 1 (then K ≤ 2 forces |S| ≤ 1, trivial).
  - Every vertex is equidistant from c by `lg:lem:rotfacts`(d) (sympy).
- **`lg:lem:trans`, `lg:lem:fan-step`, `lg:lem:orient-lin`** (`:629`, `:641`, `:653`).
  - Fidelity: exact, with the hypotheses in the Lean order. The generic point named c in `orient_trans_halfplane` is
    flagged as not the centre.
  - The key identities were checked with sympy for arbitrary points, as were all the (O2)-based `det` rewrites.
  - Attack with coincident points: the identities are unconditional, and the positivity hypotheses exclude the
    degenerate cases.
- **`lg:lem:fan-pos`** (`:658`).
  - Fidelity: exact, with no `3 ≤ n`.
  - Attack on the induction bookkeeping: every instance of (H), (F), (T), of the induction hypothesis, and of part (a)
    used inside (b₀) and (b) is within its range. For example, the base of (b₀) needs i+2 < n, which follows from
    s+1 < n with s = i+1. The fan step needs (F) at s+1 (from s+2 < n) and (a) at (i, s+1) (from i < s+1 < n).
  - n ≤ 2 is vacuous or immediate.
- **`lg:def:fanpt`, `lg:thm:fan`** (`:694`, `:700`).
  - The `i - 1` truncation is guarded by i ≠ 0, and n is implicit.
  - Attacks: repeated chain points (Step 2 shows that the positivity hypotheses force distinctness; a third index
    exists since n+1 ≥ 4); n = 3 (n+1 = 4 meets the `4 ≤ card s` of `fd:lem:pos-triples`); general position is not
    used.
- **`lg:lem:halfplane`** (`lin_pos_of_peel`, `:864`).
  - Fidelity: exact (m ≥ 3, K ≤ 2m, c ∉ S, invariance, K-free, general position, p a hull vertex of
    `peel(S,i)`, y ∈ `peel(S,i)`, y ≠ p).
  - Attacks: the case y ∈ L with j = 0 is excluded by y ≠ p. In the case y ∉ L, y ∈ `peel(S,i+1)`.
  - p' = ρ^{m-1}p lies in L, and ρ(p') = ρ^m p = p by `lg:cor:period` (m ≥ 1).
  - (e1) and (e2) use nesting with (i, i+1). (w2) needs 0 < m-1 < m, and (o) needs m ≥ 3: m = 3 is the boundary and
    passes.
  - The key identity holds for five arbitrary points (sympy). S4: all pairs positive.
- **`lg:thm:chain`** (`:914`).
  - Fidelity: exact (3 ≤ m, 4 ≤ K ≤ 2m, conclusion `False`).
  - Attacks: `K - 1` underflow is impossible since K ≥ 4, and (K-1)+1 = K. The chain points need not be distinct
    (handled by the fan theorem). The step from HasConvexNGon of `peel(S,i)` to HasConvexNGon of S is
    `fd:lem:mono`(c) with (L2).
- **`lg:def:polar`, `lg:lem:polar`, `lg:lem:ruleA`, `lg:lem:sinadd`, `lg:lem:ruleB`** (`:932`, `:935`, `:943`,
  `:956`, `:974`).
  - Fidelity: `polar` has no sign condition. Rule A has all six strict angle bounds and three positive radii.
    Rule B has no `0 < r_b` hypothesis, as in Lean; the remark correctly notes that it follows.
  - Attacks on boundary angles: all bounds are strict. In rule A the upper bounds and the sum 2π force the lower ones,
    so the hypotheses are consistent and non-vacuous. In rule B, x = (x+y) - y < π.
  - The orient_polar formula and the rule-B decomposition were checked with sympy.

## Checks that found nothing
- No circularity, and no use of a result before it is available: the written-step lemmas and corollary appear
  before their first use. The only forward mention, of rule B in the remark after `lg:thm:radius`, is not used in a
  proof.
- No silent extra hypotheses (general position, distinctness, nonemptiness, c ∉ S) beyond those in Lean.
- No overclaiming. The rigor labels are "Lean-checked" and "written proofs (not refereed)", and none of the
  statements takes an unproved proposition as a hypothesis or is a computation.
