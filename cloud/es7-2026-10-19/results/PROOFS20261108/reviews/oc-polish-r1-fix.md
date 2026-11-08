# Section `oc`, polish round 1: fix log

Inputs: `reviews/oc-r1-fidelity.md` (F1-F4), `reviews/oc-r1-rigor.md` (M1-M11 and one note), `reviews/oc-r1-adversarial.md`
(m1-m8), `reviews/oc-r1-claims.md` (m1-m11), `reviews/oc-writer-concerns.md`. Pre-edit snapshot:
`snapshots/polish-r1-pre/oc.tex` and `snapshots/polish-r1-pre/oc.map.tsv`. Line numbers below refer to `sections/oc.tex`
after the fix. Paths of Lean sources and records are relative to the results directory, as in the section.

All 34 finding ids are resolved: 20 fixed, 14 duplicates, 0 declined. Every label is kept (the label lists before and
after are identical), and all 13 export labels stay on the same statements.

## Findings

| report / id | summary | action | location after the fix |
|---|---|---|---|
| fidelity F1 | Remark `oc:rem:copies` says "same text (up to the declaration of a type variable)", but the doc comment of `polar` also differs | fixed: "the same declaration text ..., except that `iterate_mem` declares its type variable in its own binder (in `LAYERLEAN/LayerLemma.lean` it is a section variable) and that the doc comment of `polar` is worded differently; neither difference affects the meaning". Re-checked with `diff` (OC 39-112 against LL 52-57, 104-105, 230-271, 297-308, 465-469, 931-932) | Remark `oc:rem:copies`, lines 150-157 |
| fidelity F2 | Overview item (B) says "for even m" without `m > 0`; for m = 0 (even in Mathlib) both claims fail | fixed: "for even m > 0" in the item title, the first sentence and the last sentence | overview (B), lines 17-26 |
| fidelity F3 | The stated axiom evidence does not cover every Lean-referenced statement: `PreservesOrient.iterate` (no axiom output; build log not cited) and the LAYERLEAN declarations cited in Lemmas `oc:lem:iterate`, `oc:lem:iter-mem` | fixed: the Axioms paragraph now (a) names the copied `iterate_mem`, `rotAbout_iterate` of `OrbitConsistency.lean` as covered transitively (both used by the printed `antipode_mem_of_even`); (b) exception (i): `PreservesOrient.iterate` has no axiom output, its compilation is recorded by `LEANEXT/orbit/logs/build.log` (exit 0); (c) exception (ii): `ErdosSzekeres.LayerLemma.rotAbout_iterate` and `.iterate_mem` are recorded in `LEANEXT/review/axioms.log` lines 33 and 1 (review of 4 November 2026 of `LAYERLEAN/LayerLemma.lean`, `LEANEXT/review/REPORT.md` lines 3-4): three axioms, resp. only `propext` and `Quot.sound`. "remaining declarations" became "remaining theorems" (the definitions are covered by the Rigor paragraph). Map notes of `oc:lem:iterate`, `oc:lem:iter-mem`, `oc:lem:rotcomp-pres` updated | Axioms paragraph, lines 75-91; Rigor paragraph, lines 97-99; `oc.map.tsv` rows `oc:lem:iterate`, `oc:lem:iter-mem`, `oc:lem:rotcomp-pres` |
| fidelity F4 | The Dependencies paragraph omits `fd:lem:affine-orient`, `ll:lem:minperiod`, `fd:lem:cp-hull`, `fd:lem:separation` | fixed: all four added, each with the place and role of its use (parenthetical comparison, example in a remark, comparison with the Lean proof); `lg:lem:centre` now "only in comments on hypotheses (Lemma `oc:lem:same-ray` and Remark `oc:rem:layers`)" because of the claims m1 fix | Dependencies paragraph, lines 106-119 |
| rigor M1 | Remark `oc:rem:parity` says `sortpar` was tested against "the permutation sign"; `check_literals.py` compares it with its own inversion count | fixed: "The Python script `LEANEXT/orbit/check_literals.py` checked (lines 36-39) that `sortpar` sorts each of the six orders of (0,1,2) and returns the same parity as the script's own inversion count `perm_sign` (lines 25-31); this compares two inversion counts, not `sortpar` with Mathlib's sgn." Also added that bubble sort ends with no inversions, so the number of exchanges is inv(a) | Remark `oc:rem:parity`, lines 438-440 and 473-478 |
| rigor M2 | Section 13 of `Merged.lean` is also copied verbatim in `LEANEXT/linked/Linked.lean` and `LEANEXT/capstone/Capstone.lean` | fixed: Sources lists Linked.lean 1148-1383, Capstone.lean and Capstone2.lean 1156-1391 (all re-checked with `diff`, empty), and `ENCBLEAN/geo/ES8Geo/Capstone2.lean` as a byte-identical copy of Capstone2.lean (same SHA-256 `f8c3930c2427`); Coverage (iv) refers to this list | Sources, lines 53-58; Coverage (iv), lines 930-934 |
| rigor M3 | Axiom records of the LAYERLEAN-located references are not among "the logs above" | duplicate of fidelity F3 | as F3 |
| rigor M4 | Dependencies paragraph incomplete | duplicate of fidelity F4 | as F4 |
| rigor M5 | Overview drops `0 < m` (B) and writes orient for orient₃ in (A) | fixed: (B) as in F2 (duplicate part); (A) now defines orient₃(t) = orient(t(0),t(1),t(2)) inline and uses orient₃(t), orient₃(C) | overview (A), lines 9-16 |
| rigor M6 | Remark `oc:rem:layers`(3): the general-position argument does not say why lines through two points of the same kind suffice, and "the convex hull {\|x\|+\|y\|<=2} of the outer points" is asserted | fixed: pigeonhole sentence added ("among any three points of S two are of the same kind ..., so it suffices that the line through two points of the same kind contains no third point of S"); the hull claim replaced by the explicit convex combination (ε₁/2, ε₂/2) = 3/8(2ε₁,0) + 3/8(0,2ε₂) + 1/8(-2ε₁,0) + 1/8(0,-2ε₂). Checked in exact arithmetic (`build/oc_polish_r1_check.py`, ALL OK) | Remark `oc:rem:layers`(3), lines 710-723 |
| rigor M7 | Literal `--` inside `\dirn{...}` prints as a double hyphen (4 places) | fixed: all four line ranges moved outside `\dirn` ("Lines 151--158 of `KeyOrder.lean`", "`LEANEXT/keys/REPORT.md` (lines 22--25)", "lines 231--308 of `LAYERLEAN/LayerLemma.lean`"); no `\dirn{...--...}` remains; the PDF text has no "--" | lines 73, 880-881, 926, 929 |
| rigor M8 | "Same text" in Remark `oc:rem:copies` | duplicate of fidelity F1 | as F1 |
| rigor M9 | Overloaded slash "J/N = floor(J/N)" in Definition `oc:def:keys`(b) | fixed: "Lean's integer quotient `J / N` (`Int.ediv`) is ⌊J/N⌋, the floor of the rational number J/N, and Lean's remainder `J % N` (`Int.emod`) is J mod N = J - N⌊J/N⌋" | Definition `oc:def:keys`(b), lines 747-751 |
| rigor M10 | Remark `oc:rem:keys-outside` says the distinctness of phases "is" Theorem `oc:thm:layers-phase`; turning incongruence mod 2π/m into ψ_i ≠ ψ_j needs the decomposition θ = Ju + ψ | fixed: "For even m, Theorem `oc:thm:layers-phase` gives, for hull vertices of distinct layers given in polar form, directions that are incongruent modulo 2π/m; once these directions are written as Ju+ψ with u = 2π/m and 0 <= ψ < u, it follows that their phases ψ differ." | Remark `oc:rem:keys-outside`, lines 885-890 |
| rigor M11 | Multiplicativity of the real image of sgn is used but not stated | fixed: "This map is multiplicative, as a composite of monoid homomorphisms, so (S2) also holds for these real numbers; and it is injective because 1 ≠ -1 in R." | Fact `oc:fact:sign`, lines 317-319 |
| adversarial m1 | Intro item (B) false for m = 0 | duplicate of fidelity F2 | as F2 |
| adversarial m2 | "the labels T(0),T(1),T(2) need not be distinct" suggests a generality that does not exist (orient₃(P∘T) ≠ 0 forces distinct labels) | fixed: "Distinctness of the labels T(0),T(1),T(2) is not a separate hypothesis; it follows from orient₃(P∘T) ≠ 0, because orient vanishes when two of its arguments are equal (Lemma `fd:lem:orient`(e))." The formal statement is unchanged and matches `OrbitConsistency.lean:253-257` | Theorem `oc:thm:encoder`, lines 415-418 |
| adversarial m3 | The Python parity test is not independent evidence for agreement with Mathlib's sgn | duplicate of rigor M1 | as M1 |
| adversarial m4 | Remark `oc:rem:parity` does not say which list each encoder counts inversions of (`gen_b2.py` applies `perm_sign` to `order`, the sorting permutation); `\lean{}` used for Python functions | fixed: `sortpar` (gen.py:108) is applied to the ordered label triple (line 120) and to the rotations of the sorted triple (line 78); `perm_sign` (gen_b2.py:56) is applied (lines 72-73) to the list σ(0)σ(1)σ(2) of the permutation that sorts the rotated triple, so that encoder corresponds to σ₁ = id, σ₂ = σ; the conclusion is derived separately for both (`perm_sign` gives (-1)^inv(σ) = sgn σ by the table; `sortpar` gives (-1)^inv(a) = sgn(σ⁻¹) = sgn σ). Python functions now typeset with `\texttt` and called "function"; the code reading is listed among the things that are not part of any Lean statement | Remark `oc:rem:parity`, lines 436-472 |
| adversarial m5 | Verbatim copies of section 13 listed incompletely | duplicate of rigor M2 | as M2 |
| adversarial m6 | Dependencies paragraph incomplete | duplicate of fidelity F4 | as F4 |
| adversarial m7 | Evidence chain for the LAYERLEAN-located Lean names not named | duplicate of fidelity F3 | as F3 |
| adversarial m8 | Overloaded notation in Definition `oc:def:keys`(b) | duplicate of rigor M9 | as M9 |
| claims m1 | Two sentences inside statement environments are literally false: (i) labels need not be distinct (Theorem `oc:thm:encoder`); (ii) "The hypotheses do not exclude c ∈ S" (Lemma `oc:lem:same-ray`), whereas x ≠ y and Lemma `lg:lem:centre` give c ∉ S | fixed: (i) as adversarial m2 (duplicate part); (ii) "The condition c ∉ S is not a hypothesis; it follows from the others by Lemma `lg:lem:centre`, since x ≠ y gives a point of S other than c, but the proof below does not use it." The formal statement is unchanged and matches `OrbitConsistency.lean:295-298` / `Merged.lean:1181-1184` | Lemma `oc:lem:same-ray`, lines 512-516 |
| claims m2 | Introduction omits 0 < m | duplicate of fidelity F2 | as F2 |
| claims m3 | The path convention ("relative to the results directory") does not match `ErdosSzekeres/...` paths and bare basenames; `\dirn{:298}`, `\dirn{:932}` | fixed: Sources now says that paths beginning with `ErdosSzekeres/` are relative to the repository root and that a bare file name (`OrbitConsistency.lean`, `Merged.lean`, `KeyOrder.lean`) refers to the file of that name listed there; `:298`, `:932` expanded to `LAYERLEAN/LayerLemma.lean:298` and `:932`; the two other bare names introduced in this round were written in full (`LAYERLEAN/LayerLemma.lean`, `C6UPPER/encb/gen_b2.py`); `\dirn{LayerLemma}` (a namespace, not a file) replaced by "the definitions of the namespace `ErdosSzekeres.LayerLemma`" | Sources, lines 34-37 and 48; Remark `oc:rem:copies`, lines 156 and 164-166 |
| claims m4 | Literal `--` inside `\dirn` | duplicate of rigor M7 | as M7 |
| claims m5 | Axioms paragraph does not account for the copied lemmas with Lean references; nit: the "three LAYERLEAN theorems" of `merged/axioms.log` are `Merged.lean`'s copies | fixed: main part as fidelity F3 (duplicate); nit: "(and for the copies in `Merged.lean` of three theorems of `LAYERLEAN/LayerLemma.lean`: `layers_are_orbits`, `convexNGon_of_layers` and `sevenfold_octagon`)" | Axioms paragraph, lines 71-73 |
| claims m6 | Remark `oc:rem:parity` over-reads the Python test, and DESIGN.md:625 does not say "because" | fixed: Python part as rigor M1 (duplicate part); DESIGN part: "The design notes of the ENCBLEAN route record, in their entry for this theorem, the mismatch between sgn and the inversion count and that a six-case bridge would be needed, and give the verdict 'Not used' (`ENCBLEAN/DESIGN.md:625`)." No causal claim remains | Remark `oc:rem:parity`, lines 479-481 |
| claims m7 | Remark `oc:rem:keys-outside` cites `LEANEXT/keys/REPORT.md:22-25` for "sorting the keys gives the circular order", which that block does not list; REPORT.md:16-17 even says the opposite | fixed: the first two steps (form Ju+ψ, strictly increasing local ranks) are cited to `LEANEXT/keys/REPORT.md` lines 22-25 (and `ENCBLEAN/DESIGN.md:626`), the third to `LEANEXT/README.md` line 25 ("Still outside Lean"); added: "(Lines 16-17 of `LEANEXT/keys/REPORT.md` call `reduced_lt_iff_key` the step 'sorting keys gives the circular order' in `C6UPPER/encb/gen_b2.py`; Theorem `oc:thm:key` states that step only for real numbers already in the form above, with a rank as above.)" | Remark `oc:rem:keys-outside`, lines 876-885 |
| claims m8 | Dependencies paragraph incomplete | duplicate of fidelity F4 | as F4 |
| claims m9 | Remark `oc:rem:copies` overstates the identity of the copied text | duplicate of fidelity F1 | as F1 |
| claims m10 | Two copies of Merged section 13 not mentioned | duplicate of rigor M2 | as M2 |
| claims m11 | Title "label-level form as in the encoder" echoes the doc comment and may suggest the encoder code is covered | fixed: title now "literal soundness, label-level form modelled on the encoder" (the map has no title column, so no map change) | Theorem `oc:thm:encoder` head, line 407 |

Writer concerns (`reviews/oc-writer-concerns.md`): the full-document build had no overfull box > 1pt; the standalone build
after this round has none either. The section-local `\begingroup\sloppy\emergencystretch=15em ... \endgroup` was left in
place, as allowed (it causes no problem). The remaining writer items are contract notes, not findings about the text.

## Other changes

1. Statement bodies that began directly with a list now begin with a sentence (the `\leavevmode` before the list was
   removed): Lemma `oc:lem:rotcomp-pres` (line 264, "The following properties of orientation-preserving maps ... and of
   the sets RotComp(c,m) ... hold."), Lemma `oc:lem:polar-rot` (line 541), Definition `oc:def:keys` (line 739), Lemma
   `oc:lem:antipode-cell` (line 826). The items of these statements are unchanged.
2. Remark `oc:rem:ray` (rigor, "Notes (no finding)"): added that admissible sets exist, e.g. m = 2 and S = {x, 2c-x} with
   x ≠ c (general position holds vacuously), so the counterexample to "l ≠ 0" is not empty (line 536).
3. Remark `oc:rem:copies`: "`EncB.Geo.rotAbout_eq_orbitConsistency` ... proves the equality" became "the Lean theorem
   ... states the equality of the two `rotAbout`, with proof `rfl`", and it now says which copy of
   `ErdosSzekeres.LayerLemma.rotAbout` that build uses (`ENCBLEAN/geo/ES8Geo/Capstone2.lean`, whose `rotAbout` text equals
   `LAYERLEAN/LayerLemma.lean:298`; checked with `diff`).
4. Overview (B): the layer-lemma hypotheses used by Theorems `oc:thm:layers-ray` and `oc:thm:layers-phase` are now named
   (c not in the set; no K points in convex position for some K <= 2m), and "one ray through a rotated point" became "one
   open ray from c through a rotated point", matching `not_same_ray_of_distinct_layers` (l > 0).
5. Rigor paragraph: "in the sense of the logs above" became "in the sense of the records above (for a definition: it is
   part of the compiled file)".
6. Remark `oc:rem:keys-outside`: the description of encoder B's cell index is now exact for both parities ("J = 2k + h_i,
   reduced modulo 2m, for odd m, and J = k for even m"; `C6UPPER/encb/gen_b2.py`, lines 106-109). The old text gave only
   the odd-m formula.
7. Map `oc.map.tsv`: notes of `oc:lem:iterate`, `oc:lem:iter-mem` (axiom sources) and `oc:lem:rotcomp-pres` (build log
   of `PreservesOrient.iterate`) updated; still 43 rows plus header, 5 columns each, labels, kinds, Lean names and
   file:line lists equal to the statement heads (script check).
8. Exact check script `build/oc_polish_r1_check.py` (run with the symvenv Python under `nice -n 15`): convex
   combination of Remark `oc:rem:layers`(3) for all four sign choices; general position of S over all 56 triples and the
   pigeonhole form (no third point on a line through two points of one kind); invariance under the quarter-turn; the
   m = 2 example of Remark `oc:rem:ray`; the parity table against a cycle-count sign, `perm_sign` applied to the sorting
   permutation, `sortpar` on all orders of a 3-list, and inv(a) = inv(σ⁻¹). Output: ALL OK.

## Compile check

`build/oc_wrapper.tex` (contract wrapper), run twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode
-halt-on-error oc_wrapper.tex`: both passes exit 0; no `!` errors, no "Missing", no undefined control sequence, no
multiply-defined label, no "Label(s) may have changed" after pass 2. Overfull boxes: 0 (> 1pt: 0). Undefined references
(expected in the standalone build, all export labels of other sections): `fd:def:{point,orient,gp,ngon,inv,rot}`,
`fd:lem:{orient,affine-orient,collinear,cp-hull,mono,separation}`, `ll:def:{hv,peel}`,
`ll:lem:{antitone,inv-peel,minperiod}`, `ll:thm:core-rot`, `lg:def:polar`, `lg:lem:centre`. No machine path, tool name, `\newcommand`, `\usepackage` or `\begin{document}` in `oc.tex` or `oc.map.tsv` (grep).
