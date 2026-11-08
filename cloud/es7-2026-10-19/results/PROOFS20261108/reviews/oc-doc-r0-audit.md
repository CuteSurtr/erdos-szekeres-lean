# Section `oc`, round doc-r0: diff audit

Lens: diff. Inputs:
- the pre-edit snapshot `snapshots/doc-r0-pre/oc.tex` and `oc.map.tsv`;
- the current `sections/oc.tex` (938 lines) and `sections/oc.map.tsv`;
- the fix log `reviews/oc-doc-r0-fix.md`;
- the notes it addressed: `reviews/oc-p1-diff.md` (m1) and `reviews/oc-p1-referee.md` (m1, m2), as listed for `oc`
  in `build/open_minors.json` (three notes, no others).

Paths below are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or to RES (Lean sources and
records).

**Verdict: pass.**
- No blocker, no major and no minor finding.
- 3 notes marked fixed; all 3 are fixed correctly. 0 declined.
- The build is clean: both passes exit 0, no error, 0 overfull boxes.

## 1. Hunks checked

`diff -u` gives 4 hunks in `oc.tex`. `oc.map.tsv` is byte-identical to the snapshot (`cmp`), so the map has no hunk.
The difference contains nothing else: no whitespace-only change, no change to a statement environment, a label or a
`\leanref`. The changed lines (current numbering) are 40, 885-889, 909 and 925. They contain only ASCII characters,
and their braces and `$` signs are balanced.

| # | Location (current file) | Change | Check |
|---|---|---|---|
| 1 | Sources, line 40 | "Lines 37--112 repeat ..." becomes "Lines 39--112 repeat ..." | `LEANEXT/orbit/OrbitConsistency.lean` (429 lines, SHA-256 `9b843180ac38...`, both re-checked): line 37 is `/-! ## 0. Copied definitions -/`, line 38 is blank, line 39 starts `theorem iterate_mem`, line 112 is `def polar`, line 113 is blank, line 114 is `/-! ## (a) ... -/` ("new content starts at line 114" still holds). OK |
| 2 | Remark `oc:rem:keys-outside`, lines 885-889 (remark 874-892) | "For even $m$, Theorem ... gives, for hull vertices of distinct layers given in polar form, ..." becomes "For even $m\ge2$, under the hypotheses of Theorem `oc:thm:layers-phase` on the point set (it does not contain $c$, $\rho$ maps it into itself, it is in general position, and it has no $K$ points in convex position for some $K\le2m$), that theorem gives, for hull vertices of distinct layers given in polar form with positive radii, ..." | See below. OK |
| 3 | Coverage, line 909 | "Of the copied block (lines 37--112)" becomes "(lines 39--112)" | Same facts as hunk 1. The block now has one range in all three places (lines 40, 150 and 909). `grep` finds no other mention of line 37 in `oc.tex`, and no section file or map other than `oc.tex` mentions these ranges. OK |
| 4 | Coverage, "Not covered (i)", line 925 | "(lines 49--103: ...)" becomes "(lines 49--90 and 97--103: ...)" | `OrbitConsistency.lean`: line 49 is the doc comment of `toC`. Lines 49-90 hold the 14 helpers `toC`, `ofC`, `toC_re`, `toC_im`, `ofC_zero`, `ofC_one`, `toC_ofC`, `ofC_toC`, `toC_injective`, `crot`, `toC_crot`, `crot_one`, `crot_comp` and `crot_iterate`, and line 90 is the last line of `crot_iterate`. Line 91 is blank. Lines 92-95 hold `rotAbout` (covered, Definition `oc:def:basic`), now outside the range. Lines 97-103 hold `rotAbout_eq_crot`. The 15 listed names are exactly these. The unchanged phrase "copies of declarations among lines 231--308 of `LAYERLEAN/LayerLemma.lean`" was re-checked: `toC` is at 231, `crot_iterate` at 267-271 and `rotAbout_eq_crot` at 302-308 there. OK |

**Hunk 2 in detail.** No statement environment was touched. The remark paraphrases the hypotheses of
`ErdosSzekeres.LayerLemma.phase_ne_of_distinct_layers`, so I re-read `LEANEXT/merged/Merged.lean:1363-1381`. The
Merged file has 1385 lines and SHA-256 `245b7d65407a...`. The Lean binders correspond to the remark's text as follows:

| Lean binder | Wording in the remark |
|---|---|
| `hm : 2 ≤ m` | "$m\ge2$" |
| `heven : Even m` | "even" |
| `hc : c ∉ S` | "it does not contain $c$" |
| `hinv : Invariant (rotAbout c (2 * Real.pi / m)) S`, which is maps-into | "$\rho$ maps it into itself", with $\rho=R_{c,2\pi/m}$ (Definition `oc:def:basic`) |
| `hgp : GeneralPosition S` | "it is in general position" |
| `hK : K ≤ 2 * m` and `hno : ¬ HasConvexNGon K S`, with `K` an implicit argument of the theorem | "it has no $K$ points in convex position for some $K\le2m$", which is the condition for the theorem to apply; the overview (B) uses the same wording |
| `hij : i ≠ j`, `hx`, `hy` | "hull vertices of distinct layers given in polar form" |
| `hr : 0 < r`, `hr' : 0 < r'` | "with positive radii" (new and correct; the old text omitted it) |
| conclusion `∀ k : ℤ, β - α ≠ k * (2 * Real.pi / m)` | "directions that are incongruent modulo $2\pi/m$" |

Theorem `oc:thm:layers-phase` (lines 684-692) still states exactly these hypotheses and this conclusion.

The follow-on claim is right. Take $u=2\pi/m>0$ (as $m\ge2$) and write $\alpha=J_1u+\psi_1$ and $\beta=J_2u+\psi_2$ with
$0\le\psi_i<u$. Then $\psi_1=\psi_2$ would give $\beta-\alpha=(J_2-J_1)\,u$, which the theorem excludes with
$k=J_2-J_1$. So the phases differ.

The fix log explains why the point set is not called $S$: in this subsection $S\subseteq\R$ is the set of phases
(Lemma `oc:lem:rank`, Theorem `oc:thm:key`). That is true and sensible.

Some other references in the remark were checked:
- $c$ and $\rho$ are read as those of the cited theorem.
- The Dependencies sentence "\S`oc:sub:keys` uses no other section" still holds, since the hunk adds no `\ref`.
- No rigor label appears in the hunk.

## 2. Fixer's dispositions

**Fixed (3). All are confirmed.**
- `oc-p1-diff` m1 ("For even m" drops $2\le m$ and the layer-lemma hypotheses). The fix goes beyond the suggested
  wording: it names the hypotheses and adds "with positive radii". Both additions are accurate (hunk 2).
- `oc-p1-referee` m1 (the not-covered range 49--103 contains the covered `rotAbout`). The fix uses 49--90 and 97--103
  (hunk 4). The referee suggested 49--91. Line 91 is blank, so 49--90 is the tighter and exact range.
- `oc-p1-referee` m2 (37--112 against 39--112). The fix uses 39--112 everywhere (hunks 1 and 3), and Remark
  `oc:rem:copies` (line 150) already said so.

**Declined (0).**

Other claims in the fix log were also confirmed:
- `oc.map.tsv` is byte-identical.
- The section has 51 labels, and the label list (in order) is identical to the snapshot's.
- Each of the 13 export labels is defined exactly once, on the same statements.
- No other section file mentions these ranges.
- `fd:lem:orient`(e) exists in `sections/fd.tex` (line 486: "$\orient(a,b,c)=0$ whenever two of $a,b,c$ are equal"),
  as cited at `oc.tex:418`. No change was made there.

## 3. Compile check

- Wrapper: `build/oc_docr0audit_wrapper.tex`, identical to the contract wrapper (it inputs `../preamble` and
  `../sections/oc`).
- Command, run twice from `build/`: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
  oc_docr0audit_wrapper.tex`.
- Both passes exit 0, giving 13 pages.
- The log has no `!` line, no "Missing", no undefined control sequence, no multiply defined label, no runaway and no
  "Label(s) may have changed".
- **Overfull boxes: 0**, so none exceeds 1pt.
- There are 69 underfull warnings, the same count as the polish-round build (`build/oc_p1diff_wrapper.log`). They
  come from the section-local `\sloppy` and the long Lean names. None lies in the new remark text. The only ones in
  edited paragraphs (Sources at lines 39-43 and Coverage at lines 896-923) were already there.
- Undefined references are all expected in the standalone build, and all are export labels the contract allows:
  - `fd:def:{gp,inv,ngon,orient,point,rot}`;
  - `fd:lem:{affine-orient,collinear,cp-hull,mono,orient,separation}`;
  - `lg:def:polar`, `lg:lem:centre`;
  - `ll:def:{hv,peel}`, `ll:lem:{antitone,inv-peel,minperiod}`, `ll:thm:core-rot`.
- No `oc:` reference is undefined.
- PDF text (`pdftotext`): the edited passages render as intended:
  - "Lines 39–112" in Sources, in Remark 1.2 and in Coverage;
  - "lines 49–90 and 97–103";
  - "For even m ≥ 2, under the hypotheses of Theorem 1.33 on the point set (...)". Theorem 1.33 is the
    distinct-layers phase theorem.

## 4. Global checks on `oc.tex` and `oc.map.tsv`

- No machine path (`/private`, `/Users`, `/home`, `/tmp`) and no tool name.
- No "verified", "certified", "proved" or "proves". No `lrat-check`, `Sixfold66` or case-class wording.
- No `\newcommand`, `\renewcommand`, `\def`, `\usepackage` or `\begin{document}`.
- Outside `oc.tex`, only `sections/fd.tex` references `oc` labels (`oc:lem:perm`, `oc:lem:rot-inv`). Both are
  unchanged export labels.

## 5. Findings

None.
