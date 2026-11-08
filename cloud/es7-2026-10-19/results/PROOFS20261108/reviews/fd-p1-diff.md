# fd, polish round 1: diff audit

**Inputs**
- Passed snapshot: `snapshots/sections-r1pass/fd.tex` and `fd.map.tsv`. They are identical to `snapshots/polish-r1-pre/`.
- Current files: `sections/fd.tex` (1241 lines) and `sections/fd.map.tsv`.
- Fixer log: `reviews/fd-polish-r1-fix.md`.
- No earlier `fd-p*-diff.md` or `fd-p*-referee.md` exists.

**Path conventions.** Paths are relative to STAGE (`sections/`, `build/`, `reviews/`), to RES (`LAYERLEAN/...`, `SYMLEAN/...`, `LEANEXT/...`, `H2/...`) or to the repository root (`ErdosSzekeres/...`, `docs/...`).

**What was run.** Read-only tools only: cat, sed, grep, diff, cmp, shasum, pdflatex under `nice -n 15`, and one sympy script. I did not run git, lake, lean or any solver.

## Verdict: PASS

There is no blocker and no major finding. There are two minor findings, m1 and m2.

- **Mathematics.** Every hunk was checked against the Lean source, the Mathlib source at the pin, and the records under RES. The mathematics is correct.
- **Touched statements.** Every touched statement matches its Lean declaration exactly.
- **Rigor labels.** None is rounded up.
- **Hygiene.** No machine path and no tool name appears.
- **Compile.** The section compiles cleanly, with 0 overfull boxes.
- **Fixer's decisions.** Every finding marked "fixed" is fixed correctly. The "declined" and "duplicate" decisions are acceptable.

## 1. Hunk-by-hunk check (20 tex hunks, 8 map rows)

| hunk (new lines) | change | check | result |
|---|---|---|---|
| 7-17 | Purpose paragraph. Two exceptions: computer-assisted statements, and cited published theorems such as Theorem `mb:thm:baek`. Variants are labelled as variants. | `mb:thm:baek` is a contract export label of mb. It is defined in mb.tex:182-183 in a `theorem` environment, "Baek's theorem, cited". mb.tex:199 says "cited, not reproved". mb's remark gives the publication: Eur. J. Combin. 124 (2025). | correct |
| 25-36 | Research-records directory "whose path from the repository root is ..."; example of `lake env lean`; definition of a bare `:N`. | `LAYERLEAN/logs/axioms_recheck_20261106/README.txt` says "from the repository root" and records `LayerLemmaAxioms.lean` = `LayerLemma.lean` plus 19 `#print axioms` lines. `run.sh` does a `cd` to the repository and runs `lake env lean`. All 15 bare `\dirn{:N}` in fd (and the one in ar) refer to the file cited immediately before. | correct |
| 51-61 | Lean-checked label now allows `Lean.ofReduceBool` and `Lean.trustCompiler` for native_decide declarations. Evidence is a `#print axioms` output for a declaration "whose statement or proof uses it". | Consistent with contract rules 6 and 8. "No declaration cited in this section is of this kind" holds, including the newly named counterparts: text search of the two new research files and of `BoundaryGeometry.lean`'s proof found no native_decide. See m2 for one wording point. | correct (m2) |
| 76-79 | A "written step" part "does not carry this label, even where the text names a Lean counterpart". | Wording only. | correct |
| 177-179 | Audit line 529 prints `Omission.BoundaryGeometry.exposed_not_in_hull` (`ErdosSzekeres/Omission/BoundaryGeometry.lean:30`). | Line 529 of `docs/validation/axiom-audit-lower-bound-2026-10-11.txt` is exactly this name with the three standard axioms. Line 30 carries `theorem exposed_not_in_hull`, namespace `ErdosSzekeres.Omission.BoundaryGeometry` (:9). See note (a) on "unchanged since 7f0868fdb". | correct |
| 190 | `--wfail` is typeset as `-{}-`. | The PDF shows `lake build --wfail`. | correct |
| 198-211 | LayerLemma compile evidence: `LEANEXT/review/REPORT.md` item 1, plus the re-check `out.txt`. `build.log` is not used. | See the evidence list below this table. | correct |
| 215-217 | `AffineReductionAxioms.lean` = `AffineReduction.lean` followed by nine `#print axioms` commands and one `#check` command. | The first 1533 lines are identical (cmp). The appended part is one blank line, 9 `#print axioms` lines and 1 `#check` line. | correct |
| 228-234 | The orbit `build.log` contains only the exit code; `LEANEXT/orbit/REPORT.md` line 3 identifies the file; the orbit `axioms.log` lists "the two theorems of that file named in this section". | `build.log` is the 7 bytes `exit=0\n`. REPORT.md line 3 reads "OrbitConsistency.lean (429 lines, SHA-256 9b843180…)", and the current file has 429 lines and SHA-256 `9b843180ac38…`. In `axioms.log`, line 1 is `orient_rotAbout_inv` and line 5 is `orient3_perm`. These are the only OrbitConsistency theorems that fd names; `Invariant`, `orient3` and `rotAbout` are definitions. | correct |
| 287, 295-304 | `fd:def:conv`: Mathlib `AffineMap` (with `f(w+p) = f_lin(w) + f(p)`) and `AffineEquiv`. | Checked against the pinned Mathlib checkout (`.git/HEAD` = `f897ebcf72cd…`). `structure AffineMap` has `toFun`, `linear` and `map_vadd' : toFun (v +ᵥ p) = linear v +ᵥ toFun p`. `structure AffineEquiv ... extends P₁ ≃ P₂` has `linear : V₁ ≃ₗ[k] V₂` and the same `map_vadd'`. The derivation p = 0 ⇒ f(x) = A_f x + f(0), and its converse, were checked in sympy. | correct |
| 351-359 | `fd:lem:inv-image`: arbitrary set X; (a), (b) for X = ℝ²; (c) as in Lean. | `LAYERLEAN/LayerLemma.lean:52`: `iterate_mem {α : Type*} {f : α → α} {S : Finset α} (hinv : ∀ y ∈ S, f y ∈ S) {x : α} (hx : x ∈ S) : ∀ i, f^[i] x ∈ S` (with `omit [DecidableEq α]`). Hypothesis, conclusion and quantifier order (x before i) all match. The proof of (c) uses nothing about ℝ². (a) and (b) are unchanged in content. | exact |
| 532-546 | `fd:lem:affine-orient`. The head now tags (i) with `OrbitConsistency.orient_rotAbout_inv` (`LEANEXT/orbit/OrbitConsistency.lean:117`). Hypotheses are reordered (g, A, v). Lean's `b` is renamed w. The quantifiers of (i) are reordered to (o, θ, a, b, d). | :117 is `theorem orient_rotAbout_inv (c : Point) (θ : ℝ) (a b d : Point) : orient (rotAbout c θ a) (rotAbout c θ b) (rotAbout c θ d) = orient a b d`. With o = c, (i) is exactly this, in the same order. `OrbitConsistency.rotAbout` (:93) is one of the three copies cited in `fd:def:rot`. `SYMLEAN/AffineReduction.lean:1241` (`{g} {L} {b} (hg : ∀ p, g p = L *ᵥ p + b) (x y z)`) matches the main formula and the parenthetical. | exact |
| 563 | The proof substitutes g(p) = Lp + w. | Renaming only. | correct |
| 577-586 | `fd:rem:affine-orient-lean` rewritten: (i) is the separate theorem `orient_rotAbout_inv` for the OrbitConsistency copy, with centre c; (ii) is a written step whose case o = 0, φ = 0 is `Suk.orient_reflectY`. | `Reflection.lean:47`: `orient (reflectY a) (reflectY b) (reflectY c) = -orient a b c`, with `reflectY p = ![p 0, -p 1]` (:34-35) = F₀. | correct |
| 805-817 | `fd:lem:affine-cp`: (c′) now uses φ for the `AffineEquiv`; w is Lean's `b`. | :1290 is `generalPosition_image_affineEquiv {S} (hgp : GeneralPosition S) (f : Point ≃ᵃ[ℝ] Point) : GeneralPosition (S.image f)`. :1278 and :1305 use `hg : ∀ p, g p = L *ᵥ p + b`. | exact |
| 858-872 | Proof of (b′)-(e′): w and φ; "a Mathlib affine equivalence is an injective affine map (Definition fd:def:conv)". | This follows from the new definition, since an `AffineEquiv` satisfies `map_vadd'` with a linear map. The description of the Lean proof of :1290 (`LinearEquiv.isUnit_det'`, `affineMap_eq_mulVec`) is accurate. | correct |
| 1151-1157 | Coverage, covered list: `AffineEquiv`; `orient_rotAbout_inv` for part (i). | Consistent with the head. | correct |
| 1178-1219 | Coverage, written steps: rewritten preamble; counterparts named; list of other named declarations. | Item by item, in the bullets below this table. | correct (m1 is in the axioms paragraph) |
| 1221-1241 | Deliberately not covered: `conjecturedBound` (n ↦ 2^{max(n−2,0)}+1); conjectures "defined but not asserted"; `forces_triangle` "named above only in the axioms evidence"; the scope sentence. | `Definitions.lean:28` is `2 ^ (n - 2) + 1` with truncated subtraction, which is correct. `forces_triangle` occurs only at fd.tex:162 (axioms evidence) and :1232-1234. The scope sentence is precise. | correct |
| map, 8 rows | conv, inv-image, rot, affine-orient, affine-orient-lean, affine-cp, pos-triples, separation | The 40 rows match the 40 environments in label, kind and order. For every non-remark row, the name and line columns equal the head's `\leanref`s; this includes the new two-name row of `fd:lem:affine-orient`. The decide description is right: `OrientationClique.lean:23` proves `Finset.univ = {0,1,2,3}` and :28-31 prove the `e.strictMono` order facts. The file has 41 lines of 5 tab-separated fields, LF endings, and no non-ASCII. | correct |

**LayerLemma compile evidence (hunk at lines 198-211).**
- **REPORT.md.** `LEANEXT/review/REPORT.md` names `LayerLemma.lean`, SHA-256 `afb8542d…`, 1148 lines. Its item 1 reads "Build. Exit 0, no messages". The current file is 1148 lines with SHA-256 `afb8542dceb0…`.
- **Re-check output.** `out.txt` contains exactly 19 lines of the form `... depends on axioms: [propext, Classical.choice, Quot.sound]`, then the `time -v` block ("Exit status: 0") and `exit 0`.
- **Re-check file.** `LayerLemmaAxioms.lean` has 1168 lines. Its first 1148 lines are identical to `LayerLemma.lean` (cmp). They are followed by one blank line and 19 `#print axioms` lines.
- **build.log.** `LAYERLEAN/logs/build.log` reads "command: lake env lean LayerLemma.lean ... exit code: 0 / messages: 0 lines". It names no hash, so fd's sentence about it is true.

**Coverage, written steps (hunk at lines 1178-1219), item by item.**
- **`D3.orient_reflC`.** At `H2/D3Encoding/Geometry.lean:87`, in the top-level namespace `D3` (:22), so the name is written in full as the convention requires. It reads `(c u a b d : Point) (hu : u 0 ^ 2 + u 1 ^ 2 = 1) : orient (reflC c u a) (reflC c u b) (reflC c u d) = -orient a b d`. `reflC c u p = c + 2⟨p−c,u⟩u − (p−c)` (:75-77). With u = (cos φ, sin φ) this equals o + F_φ(p − o), which I checked in sympy. So it is (ii) with a unit direction vector in place of the angle, as the text says.
- **`SymReduction.Review.rotAbout_center` and `SymReduction.Review.orient_rotAbout`.**
  - **Location.** `SYMLEAN/review/ReviewSanity.lean:1086` is `rotAbout c θ c = c`, and :1091 is `orient c p (rotAbout c θ p) = Real.sin θ * eDist2 p c`. Both are in namespace `ErdosSzekeres.SymReduction.Review` (:1073).
  - **Definitions used.** `eDist2 p q = (p0−q0)²+(p1−q1)²` (:265). The copy of `rotAbout` is at :400; the banner at :1060ff says it is a byte copy of SymmetricReduction.
  - **Identities.** These are fd:lem:rot(b)'s ρ(c) = c and the identity of (e); both checked in sympy.
  - **Why they are not cited as Lean-checked.** `SYMLEAN/logs/ReviewSanity.out` prints the axioms of 12 `Review.*` theorems. `rotAbout_center` is referenced nowhere else. `orient_rotAbout` is referenced only in `orient_rot5_pos` (:1098), which is itself referenced nowhere. Neither carries `@[simp]` or an `attribute` line. The stated reason for not citing them as Lean-checked is therefore true.
- **`exposed_not_in_hull`.** Lean: `(S : Set Point) (p : Point) (A B C : ℝ) (zero : affine A B C p = 0) (positive : ∀ q ∈ S \ {p}, 0 < affine A B C q) : p ∉ convexHull ℝ (S \ {p})`, with `affine A B C p = A*p 0+B*p 1+C` (:10). The Coverage description matches it exactly: a set S, strict >0 on S∖{p}. It is a variant of the easy direction of `fd:lem:separation`, with ℓ(z) = −(Az₀+Bz₁) (sympy).
- **Reverse directions.** `Suk.hasConvexNGon_of_reflectY` (`Reflection.lean:64`: `HasConvexNGon n (S.image reflectY) → HasConvexNGon n S`) is the reverse direction of (d) for σ. `linearEquiv` (:6) and `generalPosition_reflectY` (:52) are forward-direction cases. The Coverage text now says exactly this.
- **"We found no declaration in the files of the table of sources that states one of them in the form given here."**
  - **Main-library files.** I listed every declaration of the 9 main-library table files. None states a written step.
  - **Research files.** I grepped the 6 research table files for rotation, invariance, hull, Carathéodory, separation, reflection and `orient` lemmas.
  - **Counterparts found.** Only counterparts in another form exist:
    - `crot_one`, `crot_comp`, `crot_eq_self_iff`, in complex form;
    - `eDist2_crot_center`;
    - `LayerLemma.orient_rotAbout`, a different identity, orient(x, ρ_α x, ρ_β x);
    - `MirrorOdd.orient_mir3`, `MirrorOdd.orient_rev`, which are special cases.
  - **Conclusion.** The claim, which is hedged and limited to the table, holds. The text says explicitly that the list of counterparts is not complete.
- **Completeness of the written-steps list.** The list covers every head part marked "written step": inv-image (a),(b); rot (b)/(c)/(d) extras, (e), (f); orient (d),(e); affine-orient (ii); collinear-mem; hull; small; affine-cp (a) and the reverse directions; caratheodory; separation.

**Mechanical checks**
- **`\leanref`s.** All 50 resolve: each cited line carries the declaration keyword and the name. Six use dotted names such as `theorem ConvexPosition.mono`.
- **`\ref`s.** Every `\ref` is an fd label or one of the export labels `ll:def:hv`, `ll:def:peel`, `ll:def:66-70`, `oc:lem:perm`, `oc:lem:rot-inv`, `mb:thm:baek`. The environment words used before them match the target environments (Definition, Lemma, Theorem).
- **Labels.** All 20 contract labels are defined exactly once, and no label is duplicated.
- **Forbidden constructs.** There is no `\newcommand`, `\usepackage`, `\input` or `\documentclass`.
- **Hygiene.** fd.tex and fd.map.tsv contain no machine path, no tool name and no non-ASCII character. The new text contains no "verified", "certified" or "proved" except "not proved in Lean" and "proved here".
- **Other sections.** I checked how other sections use `fd:lem:affine-orient`: ar.tex:76/280/366, mb.tex:436/553/782, mm.tex:760, and oc.tex:112/237. All of them remain consistent with the current statement. oc's proof of `oc:lem:rot-inv` only compares with fd. No circularity arises, because fd proves (i) from the main formula.
- **sympy** (`build/fd_p1diff_sym.py`): reflC = σ, det F = −1, rot(e), ρ(c) = c, the Mathlib affine identity and its p = 0 case, and the exposed_not_in_hull functional. All 11 checks pass.

**Note (a): "unchanged since 7f0868fdb".** The axioms paragraph now names `ErdosSzekeres/Omission/BoundaryGeometry.lean`, so its sentence "Every main-library file named in this paragraph is unchanged since commit 7f0868fdb" now covers that file. I could not run git under this task's rules, so I did not check this directly. It is supported by two facts:
- the file's current SHA-256 `f55a711e7aa9…` equals the hash recorded for it in `docs/validation/{recovery-checks,structural-checks,extensions-checks,source-manifest-cover}-2026-10-10.json`;
- the round-2 adversarial reviewer's read-only git check found that 7f0868fdb is "the last commit touching ErdosSzekeres/".

I accept the claim on this basis.

## 2. Fixer decisions

| finding | fixer | audit |
|---|---|---|
| fidelity m1 (Coverage forward vs. reverse) | fixed | **Confirmed.** fd.tex:1203-1206 match Reflection.lean:6/52/64. |
| fidelity m2 (scope sentence) | fixed | **Confirmed** (:1236-1239). |
| fidelity m3 (native_decide in Lean-checked) | fixed | **Confirmed** (:53-56). A wording refinement remains; see m2. |
| fidelity m4 (inv-image(c) generality) | fixed | **Confirmed.** It is now exact for an arbitrary set or type, and the map row is updated. |
| fidelity m5 (`#check`) | fixed | **Confirmed** (9 + 1, cmp). |
| fidelity m6 (map notes) | fixed | **Confirmed** (rot row: ρ₀ = id; pos-triples row: both decide uses). |
| fidelity m7 (`conjecturedBound`) | fixed | **Confirmed.** |
| rigor m1 (stale `LAYERLEAN/logs/build.log`) | fixed | **Confirmed.** It is replaced by current-file records, checked above. |
| rigor m2 ("statement or proof") | fixed | **Confirmed.** |
| rigor m3 | duplicate of fidelity m1 | Correct mapping. |
| rigor m4 (Mathlib AffineMap and AffineEquiv) | fixed | **Confirmed** against the pinned Mathlib source. "Matrix of the linear part" is now precise. |
| rigor m5 (i), (ii), (iii) | fixed | **Confirmed.** (i) The universal claim is replaced by a hedged one limited to the table, which holds. (ii) `exposed_not_in_hull` is stated exactly. (iii) ρ₀ = id is listed. |
| rigor m6 | duplicate of fidelity m5 | Correct. |
| rigor m7 (b and f reuse) | fixed | **Confirmed.** No `Lp+b` remains. φ is used for the AffineEquiv, and its letter differs from the angle φ in affine-orient(ii). |
| rigor m8 (path rule) | fixed | **Confirmed.** |
| adversarial m1 ((i) tagged) | fixed | **Confirmed.** The head, statement order, remark, Coverage and both map rows are consistent. The evidence is the orbit `axioms.log` line 1. |
| adversarial m2 (orbit build.log) | fixed | **Confirmed.** |
| adversarial m3 | duplicate | Correct. |
| adversarial note 1, claims note 1 (`reflectY_x`, `reflectY_y`, `reflectY_reflectY` probably covered) | declined | **Acceptable.** The sentence "not covered by a printed line that we identified" is true; it is an understatement, not an inaccuracy. rfl simp lemmas need not occur in the proof term. The fallback evidence (`--wfail` build record plus text search) is sound. |
| adversarial note 2 | duplicate of rigor m5(ii) | Correct. |
| claims m1 | duplicate (adversarial m1 + rigor m5(iii)) | Correct. |
| claims m2 (purpose paragraph) | fixed | **Confirmed** against mb.tex. |
| claims m3 | duplicate | Correct. |
| claims m4 (bare `:N`) | fixed | **Confirmed.** Every use in fd and ar refers to the file cited immediately before. |
| r1-rigor M12 (helper labels are not exports) | declined | **Acceptable.** The export list is fixed by the contract. |

The "other changes" in the log (items 1-8) were checked as part of the hunks above, and all are correct.

## 3. Compile check

Wrapper: `build/fd_p1diff_wrapper.tex`, with the same content as the contract wrapper (diff against `build/fd_wrapper.tex` is empty).

Command, run from `build/` twice: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error fd_p1diff_wrapper.tex`.

- Both passes exit 0, and the PDF has 16 pages.
- The log has no `!` error and no "Missing $".
- There are **0 overfull boxes** and 70 underfull boxes (cosmetic).
- No label is multiply defined.
- The only undefined references are the allowed export labels `ll:def:hv`, `ll:def:peel`, `ll:def:66-70`, `mb:thm:baek`, `oc:lem:perm` and `oc:lem:rot-inv`.

## 4. Findings

**m1 (minor; wording made imprecise by the new citations; fd.tex:242-244).**
- **The sentence.** "A text search of the six cited research files finds no sorry, admit, axiom declaration or native_decide."
- **Why it is now imprecise.** The Coverage paragraph now also cites the research Lean files `H2/D3Encoding/Geometry.lean` and `SYMLEAN/review/ReviewSanity.lean`, so "the six cited research files" no longer identifies a set. (`SYMLEAN/AffineReductionAxioms.lean` was already cited as well.)
- **No false statement.** The search result also holds for the two new files; I checked by grep.
- **Fix.** "the six research files of the table of sources".

**m2 (minor, optional; definition wording; fd.tex:53-56).**
- **The sentence.** The new allowance reads "for a declaration whose proof uses Lean's native_decide, the two further axioms ... are allowed as well".
- **Why it is imprecise.** `#print axioms` also reports these axioms for a declaration that uses native_decide only indirectly, through a lemma it depends on. Read literally, the rule would deny such a declaration the Lean-checked label.
- **No current effect.** No declaration cited in fd, or, according to the round-2 reports, in Stage 1, uses native_decide.
- **Fix.** "whose proof uses native_decide, directly or through a declaration it depends on".

## 5. Notes for the orchestrator (no finding for fd)

- **Cross-section.** fd now says it does not use `LAYERLEAN/logs/build.log`, because the log names no file hash; round-2 rigor m1 showed it predates the current 1148-line file. `ll.tex:29` and `lg.tex:52` still cite that log as the compile record of `LayerLemma.lean`. The current-file records are `LEANEXT/review/REPORT.md` item 1 and `LAYERLEAN/logs/axioms_recheck_20261106/out.txt`.
- **git.** I did not run git (it is not on this task's command list). See note (a) for the one claim that depends on repository history.
