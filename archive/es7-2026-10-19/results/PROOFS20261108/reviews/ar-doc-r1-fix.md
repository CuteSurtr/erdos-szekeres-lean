# Section `ar` (Affine symmetries), round doc-r1: fix log

Input: `reviews/ar-doc-r0-audit.md` (diff audit of round doc-r0). It has no blocker or major findings and one minor
finding (m1, optional). Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or to RES (Lean
sources). `ar.tex:N` refers to the current file.

Snapshot taken before editing: `snapshots/doc-r1-pre/ar.tex` (SHA-256 `319ff012e464`, 807 lines) and
`snapshots/doc-r1-pre/ar.map.tsv` (SHA-256 `2b8e9d4786b3`).

## Summary

| finding | severity | action |
|---|---|---|
| m1: "(Lean line 1373)" names the line that defines `T`, not a line that applies `T` to points | minor | fixed |

1 finding, 1 fixed, 0 declined.

## m1 (fixed)

Location: ar.tex:67–69 ("Rigor and axioms", 4th bullet, the supplement for `lin2_fst` and `lin2_snd`).

Lean check: I re-read `SYMLEAN/AffineReduction.lean`. Its SHA-256 is `41cfc0b60aec` and it has 1533 lines, as in the
Sources paragraph.
- 1330: `theorem hasConvexNGon_of_affine_symmetry {N n : ℕ}`, the head of the theorem whose proof the bullet cites.
- 1373: `set T := lin2 s (β / s) 0 t with hT`. This shows that `T` is a value of `lin2`, but it does not apply `T` to a
  point.
- 1374: `set Ti := lin2 (1 / s) (-β / (s ^ 2 * t)) 0 (1 / t) with hTi`.
- 1375: `have hTiT : ∀ x, Ti (T x) = x := lin2_chol_inv_left hs.ne' ht.ne'`. This is the first application of `T` to a
  point.
- 1376: `have hTTi : ∀ x, T (Ti x) = x := lin2_chol_inv_right hs.ne' ht.ne'`.
- Later applications are at 1377 (`nsq (T z)`), 1385 (`T (g (Ti x))`), 1398 (`T p`), and 1401, 1404 and 1407
  (`S.image T`).

The finding is correct.

I also re-checked the other claims of the same bullet:
- `lin2_fst` and `lin2_snd` (1174–1175) are `@[simp] theorem ... := rfl`.
- Their only textual uses are the four `simp only` calls at 1180, 1187, 1193 and 1197.
- `T = lin2(s, β/s, 0, t)` in Proposition `ar:prop:averaging`(b) (ar.tex:500) is the `T` of line 1373.

Change (ar.tex:68), one line:

```
- ... a value of \lean{lin2}, to points (Lean line 1373), and the
+ ... a value of \lean{lin2}, to points (Lean lines 1373--1376), and the
```

The range covers both claims of the clause: line 1373 shows that `T` is a value of `lin2`, and lines 1375–1376 apply
`T` to points. This is the auditor's first suggested wording.

Choice of wording: I first tried a more explicit parenthetical, "(the map is defined at Lean line 1373 and applied from
line 1375 on)". It is equally accurate but made the bullet one rendered line longer. That pushed a three-line item from
the foot of page 2 to page 3, and the shipout of page 2 then added one underfull `\vbox` (badness 3525). I replaced it
with the range above. With the range, the bullet keeps its three rendered lines and the page breaks and underfull
warnings are the same as in the audited build.

## What did not change

- No statement environment, `\label`, `\leanref` or proof text changed. `diff` against the snapshot shows exactly one
  changed line (ar.tex:68).
- `sections/ar.map.tsv` is byte-identical to the snapshot (SHA-256 `2b8e9d4786b3`).

## Contract checks (ar.tex and ar.map.tsv)

- Machine paths (`/private`, `/Users`, `/home`, `/tmp`): none.
- Tool names: none (case-insensitive grep).
- `\newcommand`, `\renewcommand`, `\def`, `\let`, `\providecommand`, `\usepackage`: none.
- Rigor vocabulary is unchanged:
  - "proved" occurs only in the Lean names `mirrorOneAxis33_proved` and `mirrorNoAxis34_proved` (ar.tex:715–716).
  - ar.tex:611 has "involves no unproved claim", which was already there and is negated.
  - "verified" and "certified" do not occur.

## Compile check

From `build/`: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error ar_wrapper.tex`, run twice. The wrapper has
the contract's content. Outputs: `build/ar_docr1_run1.txt`, `build/ar_docr1_run2.txt` and `build/ar_wrapper.log`.

- Exit codes: 0 and 0. 11 pages.
- Errors (`^!`): 0. "Missing": 0. Multiply-defined labels: 0. Rerun requests: 0. The only "rerun" lines are
  `rerunfilecheck` package information.
- **Overfull boxes: 0** (0 of any size, so 0 above 1pt).
- Underfull warnings: 68. The list (`build/ar_docr1_uf_new.txt`) is identical to the list in the r0 audit's log
  (`build/ar_docr1_uf_old.txt`, from `build/ar_docr0audit_wrapper.log`).
- Undefined references: only the 19 allowed foreign export labels, the same set as in the r0 audit:
  - `fd:def:{cp,gp,inv,ngon,orient,point}` and `fd:lem:{affine-cp,affine-orient,collinear,cp-hull}`;
  - `sr:def:classes`, `sr:def:iso`, `sr:thm:main`, `sr:thm:variant`;
  - `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`;
  - `cb:thm:c2`, `cb:thm:c3`.
- Rendered text (`build/ar_docr1.txt`):
  - Compared with the r0 audit's PDF, the only change is the reflow of this paragraph. The same paragraph still has the
    same number of lines, and pages 2 and 3 have the same line counts.
  - Page 2 was also inspected as an image (`build/ar_docr1_page-02.png`). The bullet reads "... to points (Lean lines
    1373–1376), and the check also follows definitions." with an en dash.
