# Section `oc`, round doc-r0: fix log

Inputs: the three minor notes for `oc` in `build/open_minors.json` (from `reviews/oc-p1-diff.md` and
`reviews/oc-p1-referee.md`). Pre-edit snapshot: `snapshots/doc-r0-pre/oc.tex` and `snapshots/doc-r0-pre/oc.map.tsv`.
Line numbers refer to `sections/oc.tex` after the fix. Lean paths are relative to the results directory, as in the
section.

All 3 notes resolved: 3 fixed, 0 declined.

## Notes

| # | lens | summary | action | location after the fix |
|---|---|---|---|---|
| 1 | diff | Remark `oc:rem:keys-outside`: "For even m, Theorem `oc:thm:layers-phase` gives ..." drops `2 <= m` and the layer-lemma hypotheses. By the section's own convention m = 0 is even (2π/0 = 0), and for m = 0 the theorem gives nothing | fixed: the sentence now reads "For even $m\ge2$, under the hypotheses of Theorem `oc:thm:layers-phase` on the point set (it does not contain $c$, $\rho$ maps it into itself, it is in general position, and it has no $K$ points in convex position for some $K\le2m$), that theorem gives, for hull vertices of distinct layers given in polar form with positive radii, directions that are incongruent modulo $2\pi/m$; ...". The point set is not named $S$ because this subsection already uses $S\subseteq\R$ for the set of phases (Lemma `oc:lem:rank`, Theorem `oc:thm:key`). "With positive radii" was added because the theorem requires `0 < r`, `0 < r'`. The rest of the sentence (writing the directions as $Ju+\psi$ shows the phases differ) is unchanged and still follows: equal $\psi$ would make $\beta-\alpha=(J_2-J_1)u$. Checked against `LEANEXT/merged/Merged.lean:1367-1372` before and after the edit: `hm : 2 ≤ m`, `heven : Even m`, `hK : K ≤ 2 * m`, `hc : c ∉ S`, `hinv : Invariant (rotAbout c (2 * Real.pi / m)) S`, `hgp : GeneralPosition S`, `hno : ¬ HasConvexNGon K S`, `hr : 0 < r`, `hr' : 0 < r'`, conclusion `∀ k : ℤ, β - α ≠ k * (2 * Real.pi / m)` | Remark `oc:rem:keys-outside`, lines 885-891 (remark at lines 874-892) |
| 2 | referee | Coverage, "Not covered, deliberately (i)": the range "lines 49--103" of `OrbitConsistency.lean` includes the definition of `rotAbout` (lines 92-95), which the same paragraph lists as covered (Definition `oc:def:basic`) | fixed: "(lines 49--90 and 97--103: ...)". Checked in `LEANEXT/orbit/OrbitConsistency.lean`: line 49 is the doc comment of `toC`, the 14 helpers `toC` ... `crot_iterate` end at line 90, line 91 is blank, `rotAbout` is at lines 92-95 (doc comment and definition), and `rotAbout_eq_crot` is at lines 97-103. The list of 15 helper names is unchanged and complete. Line 90 is the exact last line of `crot_iterate`, so the referee's "49--91" was tightened to 49--90. The neighbouring phrase "copies of declarations among lines 231--308 of `LAYERLEAN/LayerLemma.lean`" stays: it gives a location ("among"), and the copies are indeed there (`toC` at 231, ..., `crot_iterate` at 267-271, `rotAbout_eq_crot` at 302-308) | Coverage (i), line 925 |
| 3 | referee | The copied block of `OrbitConsistency.lean` is given as "lines 37--112" in Sources and Coverage but as "Lines 39--112" in Remark `oc:rem:copies` | fixed: 39--112 everywhere. Line 37 of `OrbitConsistency.lean` is the header comment `/-! ## 0. Copied definitions -/`, line 38 is blank, the first copied declaration (`iterate_mem`) starts at line 39, and the last (`polar`) is at line 112. Sources now reads "The new content starts at line 114. Lines 39--112 repeat ...", and Coverage reads "Of the copied block (lines 39--112): ...". Remark `oc:rem:copies` already said 39--112 and is unchanged. No other section file mentions these ranges (checked with grep over `sections/*.tex` and `*.map.tsv`) | Sources, line 40; Coverage, line 909; Remark `oc:rem:copies`, line 150 (unchanged) |

## Other changes

None. No statement environment, label or Lean reference changed. The label list is identical to the snapshot (51
labels; all 13 export labels on the same statements). `sections/oc.map.tsv` needed no change (no row refers to these
ranges or to the remark's wording) and is byte-identical to the snapshot. The only edits are the four text changes
above (lines 40, 885-889, 909 and 925).

While checking, I also confirmed that the reference `Lemma fd:lem:orient(e)` in Theorem `oc:thm:encoder` is valid:
`sections/fd.tex` defines item (e), "orient(a,b,c) = 0 whenever two of a,b,c are equal". No change.

## Checks

- `build/oc_wrapper.tex`, compiled twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode
  -halt-on-error`: both runs exit 0, no `!` errors, no "Missing $", 0 overfull boxes (none at all, so none > 1pt),
  13 pages. No multiply-defined labels.
- Undefined references, all to other sections' allowed labels: `fd:def:gp`, `fd:def:inv`, `fd:def:ngon`,
  `fd:def:orient`, `fd:def:point`, `fd:def:rot`, `fd:lem:affine-orient`, `fd:lem:collinear`, `fd:lem:cp-hull`,
  `fd:lem:mono`, `fd:lem:orient`, `fd:lem:separation`, `lg:def:polar`, `lg:lem:centre`, `ll:def:hv`, `ll:def:peel`,
  `ll:lem:antitone`, `ll:lem:inv-peel`, `ll:lem:minperiod`, `ll:thm:core-rot`. No undefined `oc:` reference.
- No machine paths and no tool names in `sections/oc.tex` or `sections/oc.map.tsv` (grep).
- The PDF text (pdftotext) shows the edited passages as intended ("For even m ≥ 2, under the hypotheses of Theorem
  1.33 ...", "lines 39–112" in Sources, Remark 1.2 and Coverage, "lines 49–90 and 97–103").
