# Section `ec`: polish round 1, fix log

Input: `sections/ec.tex` and `sections/ec.map.tsv` as snapshotted in `snapshots/polish-r1-pre/`. All four round-1
reports (fidelity, rigor, adversarial, claims) and `ec-writer-concerns.md` were read; every minor finding, and every
remark that points to an inaccuracy, is listed below. Line numbers are those of `sections/ec.tex` after the fix
(891 lines). Paths are relative to the staging area or to `RES = cloud/es7-2026-10-19/results`.

## Findings

| report, id | summary | action | location after the fix |
|---|---|---|---|
| fidelity F1 | Overview item (2): threshold arithmetic with an unquantified `e`; false for m = 4 with e = 1 | fixed: the four equivalences are written out, with `e` only for m = 5, 7 and "for all t, e with e <= 1" (matches `thr_m4`..`thr_m7`) | overview item (2), lines 12-15 |
| fidelity F2 | Overview item (1) drops finiteness | fixed: "every finite set of points ... invariant under the rotation by 2pi/5 about some point" | overview item (1), lines 7-11 |
| fidelity F3 | Gloss of `CommGroupWithZero` omits 0^{-1} = 0 and the division; the role of decidable equality is too narrow (also `insert` in `exists_card1` and the test `0 ∈ S` in `card_mod`) | fixed: gloss now says inverse map with a a^{-1} = 1 for a ≠ 0 and 0^{-1} = 0, plus division and integer powers (unused); decidable equality "for image, difference, erasure and insertion, and for the test 0 ∈ S in Theorem ec:thm:compat(b); mathematically no restriction" (checked against Mathlib f897ebcf, `GroupWithZero/Defs.lean:203-207`) | Subsection 1.4 intro, lines 621-626 |
| fidelity F4 | Remark ec:rem:cases: "no step ... is checked in Lean" ignores that the layer lemma used by the layered encodings is Lean-checked (but unconnected) | fixed (one action with rigor F4, adversarial 5, claims m2): "Apart from the layer lemma, none of these written arguments is checked in Lean. The layer lemma has a Lean-checked form (Theorem ll:thm:layers), but nothing in Lean connects it to the formulas, and no Lean theorem links a formula or a certificate to these propositions." | Remark ec:rem:cases, lines 126-128 |
| fidelity F5 | Unused notation C_r clashes with C_4, C_5 | fixed: C_r removed; the circle is named as Lean's `sphere 0 r` without a symbol | Conventions of Subsection 1.2, lines 252-256 |
| fidelity F6 | Five overfull boxes in statement heads (5.1, 4.4, 10.6, 1.1, 30.8 pt) | fixed by shorter short names (widths measured with the shared preamble): Lemma ec:lem:pc-basic "basic facts" -> "powers"; Definition ec:def:compat "size compatibility" -> "size condition"; Proposition ec:prop:parity "parity cases" -> "parity"; Theorem ec:thm:compat "size compatibility" -> "compatibility"; Theorem ec:thm:l0 "symmetric sets of 2^{m-1} points in C" -> "sets of 2^{m-1} points". Build: 0 overfull boxes | heads at lines 639, 677, 682, 705, 817 |
| rigor F1 | Overview threshold arithmetic | duplicate of fidelity F1 | lines 12-15 |
| rigor F2 | Overview drops finiteness | duplicate of fidelity F2 | lines 7-11 |
| rigor F3 | Remark ec:rem:thr: "c ∉ S for even m (Lemma lg:lem:centre)" omits the hypothesis p ∈ S, p ≠ c (false for S = {c}) | fixed: "If moreover S ⊄ {c} (for instance if |S| >= 2), then c ∉ S for even m"; "e = 0 for m = 4, 6 when |S| >= 2"; also says the layer results are applied to S \ {c}, which is invariant (rotation injective, fixes c), and that t counts the layers of S \ {c} | Remark ec:rem:thr, lines 424-436 |
| rigor F4 | Remark ec:rem:cases omits the centre-perturbation lemma behind SYM5 and the records' label | fixed (one action with fidelity F4, adversarial 5, claims m2): Fivefold35 item names the encoder soundness ("recorded as a written proof, reviewed in the audit", `AUDIT3`, A4), the normal-form lemma, and the centre-perturbation lemma (`C2ENC/perturbation.md`, "recorded there as a complete written proof, refereed, not Lean-checked"); also notes that the two certificates are two normal forms of one encoder (`AUDIT3`, A4-3) and points to `C2ENC/class_table.md` | Remark ec:rem:cases, lines 110-118 |
| rigor F5 | Remark ec:rem:es7-sharp: no bridge from the note's "symmetry C_s" to `rotAbout(c, 2pi/s)` | fixed: a rotation of order s about c is rotAbout(c, 2pi k/s) with gcd(k, s) = 1; for j with jk ≡ 1 (mod s), rho^j = rotAbout(c, 2pi/s) by the complex form of fd:def:rot; forward invariance passes to powers; so the theorems apply to every set with symmetry C_5, resp. C_4 | Remark ec:rem:es7-sharp, lines 221-225 |
| rigor F6 | Remark ec:rem:big-order calls layers.md Lemma 2(a) "the following corollary", but layers.md assumes general position | fixed: the planar statement ("stated there for sets in general position") "follows from the following corollary, which does not assume general position"; also says that Lean checks only the complex form | Remark ec:rem:big-order, lines 370-374 |
| rigor F7 | Five overfull boxes | duplicate of fidelity F6 | heads at lines 639, 677, 682, 705, 817 |
| adversarial 1 | Overview item (2), e undefined | duplicate of fidelity F1 | lines 12-15 |
| adversarial 2 | Remark ec:rem:thr, e = 0 for m = 4, 6 needs S ⊄ {c} | duplicate of rigor F3 | lines 424-436 |
| adversarial 3 | "For the next two lemmas let D, Sigma", but Sigma is used in three lemmas and Prop ec:prop:layered | fixed: "For the rest of this subsection, for real phi_1, ..., u_3 let" | line 472 |
| adversarial 4 | Coverage calls Fact ec:fact:prim "not in Lean", but its items are Mathlib lemmas | fixed: Coverage now says the written steps are "not declarations of the five Lean files; only the Fact has Lean counterparts, the Mathlib lemmas named in its proof"; the Rigor paragraph says the same ("Fact restates Mathlib lemmas, and Corollary ec:cor:planar has no Lean counterpart") | Coverage lines 888-890; Rigor paragraph lines 64-66 |
| adversarial 5 | Remark ec:rem:cases omits the SYM5 perturbation lemma and the C4CUT sector-unit step that `AUDIT3` A4-1 found not written down | duplicate of rigor F4 (same action); the Fourfold32 item now names the soundness of the layered encoder ("recorded in C4CUT/README.md as a written proof, refereed"), the layer lemma, and the sector normal form "whose argument the audit found not written down (AUDIT3, A4-1; C4CUT/README.md, Section 1, now gives it in one sentence)" | Remark ec:rem:cases, lines 119-124 |
| adversarial 6 | Overview item (1), finiteness | duplicate of fidelity F2 | lines 7-11 |
| adversarial 7 | `CommGroupWithZero` gloss omits 0^{-1} = 0 | duplicate of fidelity F3 | lines 621-626 |
| adversarial 8 | `\ref{sr:def:classes}` is a forward reference to a later section | declined: CONTRACT.md lists `sr:def:classes` among the export labels that any section may \ref; it is defined in `sections/sr.tex:192` on the case-class definition (which includes `SymReduction.Fivefold35` at :477 and `Fourfold32` at :496), so the reference is correct and resolves in the full document | lines 73, 130 |
| adversarial 9 | Five overfull boxes | duplicate of fidelity F6 | heads at lines 639, 677, 682, 705, 817 |
| claims m1 | Overview threshold arithmetic | duplicate of fidelity F1 | lines 12-15 |
| claims m2 | Remark ec:rem:cases lists the outside-Lean dependencies incompletely (perturbation lemma; layer lemma Lean-checked in LAYERLEAN; C4CUT sector-unit step) | duplicate of rigor F4 / fidelity F4 (same action) | Remark ec:rem:cases, lines 106-135 |
| claims m3 | "It is the Lean check of part (a)" without saying that Lean checks the complex form | fixed: "the Lean check of a complex form of part (a) of Lemma 2 of ES8SYM/proofs/layers.md (the planar form is Corollary ec:cor:planar, a written step)" | Subsection 1.2 intro, lines 248-250 |
| claims m4 | Remark ec:rem:thr, e = 0 without S ≠ {c} | duplicate of rigor F3 | lines 424-436 |
| claims m5 | Sources column "lines covered" contradicts Coverage (the `#print axioms` lines are not covered) | fixed: column renamed "Lean file (lines in scope)", plus the sentence "The line ranges are the scope of this section; the Coverage paragraph at the end lists what in them is not covered"; Coverage marks lines 1-1147 of ES7Corollaries.lean as "outside the scope of this section" | Sources lines 25-31; Coverage lines 878-879 |
| claims m6 | Five overfull boxes | duplicate of fidelity F6 | heads at lines 639, 677, 682, 705, 817 |
| claims m7 | Theorem ec:thm:compat(d) quantifies m a second time | fixed: preamble "Let m ∈ N, and in (a)-(c) let K be a commutative group with zero and ζ ∈ K"; (d) "If 1 <= m, then ...". Re-checked against `PCompatCore.lean:67,112,174,253`: same hypotheses and conclusions | Theorem ec:thm:compat, lines 706 and 715 |
| claims m8 | Bare file names (`ES7Corollaries.lean`, `C6check.lean`, ...) instead of RES-relative paths | fixed: every bare name replaced by its full RES-relative path | lines 42-43, 133, 432, 878-883 |
| claims (unsure 1) | Rigor paragraph calls the ES8SYM theorems Lean-checked without repeating the hash caveat | fixed: "for the two ES8SYM files this rests on the logs of the compiled versions, which according to the records differ from the present copies only in comment lines (see Sources)" | Rigor paragraph, lines 62-64 |
| claims (unsure 2) | "the Lean proofs bridge them by a cast lemma"; Lean uses `exact_mod_cast` | fixed: "the Lean proofs pass between the two forms with the cast-normalizing tactic exact_mod_cast" (checked at ES7Corollaries.lean:1175, 1177, 1208, 1210, 1228) | Conventions of Subsection 1.1, lines 92-94 |
| claims (unsure 3) | "two files that were never compiled"; the record says a compile was stopped and "It has not been compiled" | fixed: "the two files that according to ES8SLACK/README.md have not been compiled" (README lines 402-404) | Coverage, lines 885-887 |
| writer concerns, overfull list | 5 overfull boxes > 1pt in the full-document build | duplicate of fidelity F6 | as above |
| writer concerns, local `\begingroup\sloppy` | section-local `\sloppy` group around the body | declined: the task says to leave it unless it causes a problem; it causes none (build clean, 0 overfull) | lines 3, 891 |
| writer concerns, other items | ES8SYM hash mismatch, conditional theorems, export-label layout, hypotheses hr0/hdisj, `m4_with_centre_counter` without axiom line | declined (no change needed): each is already stated correctly in the section; the hash caveat is now also in the Rigor paragraph (claims unsure 1) | Sources, Axioms, Remarks ec:rem:cases, ec:rem:compat |

## Other changes

1. Subsection 1.3 intro (lines 441-443): "the Lean check of Lemma 1 of ES8SYM/proofs/layers.md (lines 15-29)" read as
   if the whole consequence paragraph were Lean-checked; now "Lemma 1 (lines 15-23) and part of the consequence stated
   after it (lines 25-29; see Remark ec:rem:polar(iii))". Remark ec:rem:polar(iii) (lines 613-615) adds that the
   cell statement of layers.md (lines 26-27; order type constant on the cells of a central hyperplane arrangement) is
   not formalized as such. Source of the concern: inventory `ES8-small.json`, risk on `nested_regular_orient`.
2. Remark ec:rem:es7-sharp (lines 218-226): says precisely how the note derives N(C_5) <= 31 and N(C_4) <= 28 (from the
   35-point fivefold and the 32-point fourfold case by orbit counting, `lem:sizes`; checked at
   `WRITEUP/note/symmetric_es7.tex:58-68, 326-345`), and that the SYMMAX examples "rest on exact computations outside
   Lean, which were not repeated for this document" (was: "are exact computations outside Lean").
3. Remark ec:rem:cases, besides the findings: the two SYM5 certificates are described as "two normal forms of one SAT
   encoder (not independent encodings: AUDIT3, A4-3)" and as accepted by lrat-check and cake_lpr (the old text named
   only cake_lpr); C4CUT likewise. Records checked: `SYM5/README.md` (table of runs, Section 1), `C4CUT/README.md`
   (status, Sections 1 and 3), `C2ENC/perturbation.md` (status line), `C2ENC/README.md` Section 6,
   `C2ENC/class_table.md` (Fivefold35 row, Fourfold32 paragraph, last sentence), `AUDIT3/README.md` (Section 2 table,
   A4 findings). The records' word "refereed" is quoted as the records' label, attributed to them.
4. Rigor paragraph (lines 66-68): adds that Lemma ec:lem:pc-exist and Theorem ec:thm:compat(c) take hypotheses on r
   that Lean does not discharge (Remark ec:rem:compat).
5. Remark ec:rem:big-order (lines 370-374): names the k = 8 tables (`ES8SYM/README.md`, `WRITEUP/note/symmetric_extremal.tex`)
   whose row "order >= 8" is labelled Lean-checked, and says that Lean checks only the complex form; the passage to
   the plane is the written step Corollary ec:cor:planar.
6. Map TSV: notes of `ec:def:cases` and `ec:rem:cases` updated to mention the written arguments outside Lean. No row
   added, removed or renamed (41 rows, 5 columns each); the TSV has no title column, so the five shortened head names
   need no map change.
7. A stray source line break inside Remark ec:rem:es7-sharp ("The\nlogs") was joined.

## Statements whose text changed

- `ec:thm:compat`: preamble and part (d) reworded (no change of content; still exactly `dvd_card`, `card_mod`,
  `exists_iff`, `classification`).
- Head short names only: `ec:lem:pc-basic`, `ec:def:compat`, `ec:prop:parity`, `ec:thm:compat`, `ec:thm:l0`.
- No hypothesis, conclusion, label or `\leanref` changed; all 49 `\leanref` name/line pairs re-checked against the Lean
  sources (0 mismatches).

## Compile check

`build/ec_wrapper.tex`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error ec_wrapper.tex` twice from
`build/`: exit 0 both times; no errors, no "Missing", no multiply defined labels. Undefined references only to export
labels of other sections: `fd:def:{point,orient,gp,cp,ngon,inv,rot}`, `ll:thm:reduction`, `ll:lem:minperiod`,
`ll:thm:layers`, `ll:thm:card-peel`, `lg:lem:centre`, `lg:lem:polar`, `sr:def:classes`. Overfull boxes > 1pt: 0
(before: 5). Underfull warnings: 21 (before: 22), all in statement heads with long Lean names or in the Coverage list.
Map check: 41 labelled environments, 41 rows, kinds and `\leanref` columns identical; 47 labels, all `ec:`, no
duplicates; the seven export labels are defined. No machine paths or tool names in `ec.tex` or `ec.map.tsv`. Nothing
under the repository was modified; no Lean, lake or solver was run.
