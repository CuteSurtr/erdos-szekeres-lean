# Re-check of section mm, final pass, round 1

Inputs:
- `reviews/final-mm-r1-fix.md` (the fixer's log; used only as a pointer, every claim re-checked below);
- `snapshots/final-r1-pre/mm.tex` and `snapshots/final-r1-pre/mm.map.tsv` (before) and the current
  `sections/mm.tex` and `sections/mm.map.tsv` (after);
- the Lean source `MIRRORETV/review/MirrorA.lean` (in RES; 891 lines, SHA-256 `1a8a62cb4385...`, the hash prefix
  that mm.tex cites).

Paths are relative to STAGE (sections, snapshots, build, reviews) or to RES (records and Lean sources). No git
command, no Lean tool and no SAT tool was run.

**Verdict: pass.** The fixer addressed one finding (minor) and fixed it. The fix is correct, and the edit introduces
no blocker, major or minor problem. No finding remains.

## 1. The finding

| # | finding | fixer | re-check | evidence |
|---|---|---|---|---|
| 1 | minor: `mm.tex:991`, "\lean{refl} and \lean{isoT} for the reflection in a line ..." reads as if both were the reflection | fixed | **resolved** | See below. |

The current text (`sections/mm.tex:991-992`) reads: "..., \lean{MirrorSym}, \lean{refl}, the reflection in the line
through a point with a given unit direction, and \lean{isoT}, the rigid motion that maps this line onto the
$x$-axis." This is the wording the finding asked for, verbatim.

Checked against the source, `MIRRORETV/review/MirrorA.lean`:
- l. 705-708: docstring "reflection in the line through `p0` with unit direction `u`", and
  `refl p0 u p = p0 + 2((p - p0)·u) u - (p - p0)` (written componentwise in Lean).
- l. 710-712: docstring "the rigid motion taking the line `p0 + ℝ u` to the x-axis", and
  `isoT p0 u p = (u.1 (p.1 - p0.1) + u.2 (p.2 - p0.2), -u.2 (p.1 - p0.1) + u.1 (p.2 - p0.2))`.

So only `refl` is the reflection, and `isoT` is a different map. The new sentence describes each one correctly.
I checked the geometry independently with sympy (`build/final_mm_r1_recheck_refl_isoT.py`, all identities reduced
modulo the ideal $(u_1^2+u_2^2-1)$; output "ALL OK"):
- `isoT p0 u (p0 + t u) = (t, 0)`. As $t$ runs over $\R$, the line is mapped onto the $x$-axis, so "onto" is right.
- `isoT p = A (p - p0)` with `A = [[u1, u2], [-u2, u1]]`, and `A^T A = I`, `det A = 1`. So `isoT` is a rigid motion
  (orientation-preserving). Without the unit condition, `det A = u1^2 + u2^2`, so "rigid motion" needs the unit
  direction; the sentence supplies it ("a given unit direction", and "this line" is the same line).
- `refl` fixes `p0 + t u` for every `t` and sends `p0 + s n` to `p0 - s n`, where `n = (-u2, u1)`. So `refl` is the
  orthogonal reflection in the line (the content of `refl_fix_line`, l. 837, and `refl_normal`, l. 845).
- `isoT (refl p) = mu (isoT p)` (the content of `isoT_refl`, l. 714), consistent with "transport" at
  `mm.tex:1002-1003` ("by the rigid motion \lean{isoT}").

"Unit direction" also matches how the definitions are used: `transport` (l. 771), `theoremA_even_line` (l. 810) and
`theoremA_odd_line` (l. 821) all take `hu : u.1 ^ 2 + u.2 ^ 2 = 1`.

The fixer dropped the "and" before `\lean{refl}`. Without that, the list would read "\lean{MirrorSym}, and \lean{refl},
..., and \lean{isoT}, ...". The change is part of the replaced phrase and is needed for grammar, so it does not go
beyond the finding.

## 2. Diff review (snapshot vs current)

`diff -u snapshots/final-r1-pre/mm.tex sections/mm.tex` has exactly one hunk (`@@ -988,8 +988,9 @@`): two source
lines became three. The third line ("The main results are \lean{lemma31} (282: a cap, in the") is a re-wrap of text
that was already there, with the same content. Everything else is byte-identical (the file grew from 1060 to 1061
lines). `mm.map.tsv` is byte-identical to the snapshot (same SHA-256 `0d3f3b5d...`). The edit is in the Coverage
paragraph, which is not a statement environment and has no map row, so no map change is needed and the generated
appendix is unaffected.

Referee checks on the hunk:
- Mathematics: correct (section 1).
- Faithfulness to Lean: no statement environment touched. The two definitions described were re-read (l. 705-712)
  and are described correctly.
- Claims about files: the unchanged counts in the same item still hold. MirrorA.lean has 16 `def`s (orient, mu,
  muL, ConvexPos, IsCapSeq, IsCupSeq, V, GenPos, XDistinct, HasGon, HasCap, HasCup, InClass, MirrorSym, refl, isoT,
  exactly the listed ones), 55 theorems and lemmas (52 plain plus 3 `@[simp] lemma` at l. 27-29), and one
  `example` (l. 852). The line numbers cited in the same item are exact: lemma31 282, cap_convexPos 352,
  cup_convexPos 417, theoremA_even 593, theoremA_odd 615, theoremA_even_bound 685, theoremA_odd_bound 694,
  transport 771, theoremA_even_line 810, theoremA_odd_line 821; and 10 main results + 45 auxiliary = 55.
- Rigor labels: the hunk contains no rigor wording ("verified", "certified", "proved" or a label); nothing rounded
  up or down.
- Machine paths and tool names: a case-insensitive grep for the four forbidden machine-path prefixes of the contract
  and for tool names, over `sections/mm.tex` and `sections/mm.map.tsv`, finds nothing.
- Labels: the 22 `\label`s are identical before and after (`diff` of the extracted label lists is empty).
- LaTeX: `\lean{refl}` and `\lean{isoT}` contain no spaces, so `\nolinkurl` is fine; `$x$-axis` is sound; no macro
  defined, no package loaded.

## 3. Compile

Wrapper `build/mm_final_recheck_r1_wrapper.tex` (same content as the contract wrapper), compiled twice from
`build/` with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`:
- Exit 0 both times. No `!` error, no "Missing $", no multiply defined label, no rerun request. 14 pages.
- Overfull boxes: 0 (so none above 1pt).
- Undefined references only to `fd:` labels (fd:def:cp, fd:def:gp, fd:def:inv, fd:def:ngon, fd:def:orient,
  fd:def:point, fd:lem:affine-cp, fd:lem:affine-orient, fd:lem:collinear, fd:lem:cp-hull, fd:lem:mono,
  fd:lem:orient, fd:lem:pos-cycle) and to the export labels ar:thm:main, mb:thm:baek, mb:thm:seven, mb:thm:eight,
  mb:thm:nine, mb:thm:main3, sr:thm:main. All of these are allowed by the contract and are expected in the
  standalone check.
- For comparison I compiled the pre-edit snapshot the same way (`build/mm_final_recheck_r1_snapwrapper.tex`). The
  multisets of Overfull/Underfull warnings, with source line numbers masked, are identical. Neither build has a box
  warning in source lines 960-1061. So the edit adds no typesetting warning.
- `pdftotext` shows the new sentence set as intended: "..., MirrorSym, refl, the reflection in the line through a
  point with a given unit direction, and isoT, the rigid motion that maps this line onto the x-axis. The main
  results are ...".

## 4. Remaining findings

None.

Observation, not raised as a finding: "\lean{isoT}, the rigid motion that maps this line onto the $x$-axis" uses
the definite article although many rigid motions map a given line onto the $x$-axis. `isoT` is the one that sends
`p0` to the origin and `u` to `(1, 0)`. The appositive follows the name, which fixes the map. The wording is the
Lean docstring's ("the rigid motion taking the line `p0 + ℝ u` to the x-axis") and the one the finding prescribed.
It has no effect on correctness, and changing it in the final pass would be churn, so I do not ask for an edit.
