# Section `ar` (Affine symmetries), round doc-r1: diff audit

Lens: diff. Inputs:
- the pre-edit snapshot `snapshots/doc-r1-pre/ar.tex` (807 lines, SHA-256 `319ff012e464`) and
  `snapshots/doc-r1-pre/ar.map.tsv` (`2b8e9d4786b3`);
- the current `sections/ar.tex` (807 lines, `4172a12b50ad`) and `sections/ar.map.tsv` (`2b8e9d4786b3`);
- the fix log `reviews/ar-doc-r1-fix.md`;
- the notes behind it: `reviews/ar-doc-r0-audit.md` (m1), and the earlier `reviews/ar-p1-diff.md` (m1–m3) and
  `reviews/ar-p1-referee.md` (R1–R3), which were fixed in round doc-r0.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or to RES (Lean sources and records).
`ar.tex:N` refers to the current file.

**Verdict: pass.**
- No blocker, no major and no minor finding.
- The one note marked fixed (doc-r0 audit m1) is fixed correctly. No note was declined.
- The earlier p1 fixes are all still in place.
- The build is clean: both passes exit 0, there is no error, and there are 0 overfull boxes.

## 1. Scope of the diff

- `diff -u` gives one hunk in `ar.tex` with one changed line (ar.tex:68). The line count stays at 807.
- `ar.map.tsv` is byte-identical to the snapshot (`cmp`, same SHA-256).
- No statement environment, `\label`, `\leanref` or proof changed. The touched line is in the "Rigor and axioms" list,
  4th bullet (the supplement for `lin2_fst` and `lin2_snd`).
- The snapshot hashes in the fix log (`319ff012e464`, `2b8e9d4786b3`) are correct.

## 2. The hunk

```
- the map $T$ of Proposition~\ref{ar:prop:averaging}(b), a value of \lean{lin2}, to points (Lean line 1373), and the
+ the map $T$ of Proposition~\ref{ar:prop:averaging}(b), a value of \lean{lin2}, to points (Lean lines 1373--1376), and the
```

I re-read `SYMLEAN/AffineReduction.lean` (SHA-256 `41cfc0b60aec`, 1533 lines).
- `hasConvexNGon_of_affine_symmetry` starts at line 1330, and its proof runs past line 1420. So lines 1373–1376 lie
  inside the proof that the sentence talks about.
- 1373: `set T := lin2 s (β / s) 0 t with hT`. This line shows that `T` is a value of `lin2`.
- 1374: `set Ti := lin2 (1 / s) (-β / (s ^ 2 * t)) 0 (1 / t) with hTi`.
- 1375: `have hTiT : ∀ x, Ti (T x) = x := lin2_chol_inv_left hs.ne' ht.ne'`. This is the first application of `T` to a
  point.
- 1376: `have hTTi : ∀ x, T (Ti x) = x := lin2_chol_inv_right hs.ne' ht.ne'`. This is the second.
- Later applications (1377 `nsq (T z)`, 1385 `T (g (Ti x))`, 1398 `T p`, and `S.image T` at 1401, 1404 and 1407)
  are as the fix log lists them.

The range therefore covers both parts of the clause: "`T` is a value of `lin2`" (1373), and "the proof applies `T`
to points" (1375–1376). It is the first wording that the doc-r0 audit suggested. The lines are the same in
`SYMLEAN/AffineReductionAxioms.lean`, whose first 1533 lines equal `AffineReduction.lean` (`diff`), so the citation is
unambiguous.

The rest of the clause is unchanged and still correct:
- Proposition `ar:prop:averaging`(b) puts $T=\operatorname{lin2}(s,\beta/s,0,t)$ (ar.tex:500). This is the `T` of
  line 1373.
- `lin2` (line 1167) has body `![a * p 0 + b * p 1, c * p 0 + d * p 1]`.
- `lin2_fst` and `lin2_snd` (1174–1175) are `@[simp] theorem ... := rfl`. Their only textual uses are the four
  `simp only` calls at 1180, 1187, 1193 and 1197, as ar.tex:63 says.
- `hasConvexNGon_of_affine_symmetry` is among the nine `#print axioms` lines (`AffineReductionAxioms.lean:1540`). Its
  log entry is `[propext, Classical.choice, Quot.sound]` (`SYMLEAN/logs/AffineReductionAxioms.out`).

Mathematics, fidelity and rigor:
- The hunk changes only a line citation and adds no mathematical claim.
- No Lean-faithful statement is touched. A script check (`build/ar_docr1audit_refcheck.py`) confirms that all 45
  `\leanref` pairs still point at a declaration of the named Lean name. It also confirms that the 30 map rows match the
  30 statement heads in label and order.
- No rigor word is added.

LaTeX: line 68 is pure ASCII. `1373--1376` renders as an en dash ("Lean lines 1373–1376"; checked in the text dump
and on the page-2 image). The paragraph keeps the same number of rendered lines.

## 3. Notes marked fixed, declined or duplicate

| note | status in log | judgement |
|---|---|---|
| doc-r0 audit m1 ("(Lean line 1373)" names the definition of `T`, not an application) | fixed | fixed correctly (§2) |
| p1-diff m1 (bookkeeping theorems also computer-assisted) | fixed in doc-r0 | still in place: ar.tex:739–742 ("Lean-checked, and computer-assisted because their finite checks are kernel evaluations (`decide +kernel`)") |
| p1-diff m2 ("every piece of their case splits") | fixed in doc-r0 | still in place: ar.tex:727 ("including those of the pieces of their case splits") |
| p1-diff m3 (file name standing for the normal form) | fixed in doc-r0 | still in place: ar.tex:736 ("the normal form of `Threefold33` (`C3-S/soundness.md`)") |
| p1-referee R1 (axioms inference for the rfl lemmas) | fixed in doc-r0 | still in place: ar.tex:60–70, now with the corrected line range |
| p1-referee R2 ("the five case classes" of a definition with six) | fixed in doc-r0 | still in place: ar.tex:14–15 ("five of the six case classes ... (all except `Fourfold32`)") |
| p1-referee R3 (Coverage overstates the duplicate) | fixed in doc-r0 | still in place: ar.tex:797–798 ("lines 1--1058 of `SymmetricReduction.lean`") |

No note was declined and none was marked duplicate.

## 4. Claims of the fix log

All checked and true:
- one changed line (ar.tex:68);
- the map is unchanged;
- the Lean lines 1330 and 1373–1376, and the later applications, are as listed;
- `lin2_fst` and `lin2_snd` are at 1174–1175 and are used only at 1180, 1187, 1193 and 1197;
- `T` is at ar.tex:500;
- the rigor-word positions (ar.tex:611, 715–716);
- the build numbers (0 overfull, 68 underfull, 19 allowed undefined references).

## 5. Contract checks (current `ar.tex` and `ar.map.tsv`)

- Machine paths (`/private`, `/Users`, `/home`, `/tmp`): none.
- Tool names: none (case-insensitive grep).
- Macros and packages: no `\newcommand`, `\renewcommand`, `\providecommand`, `\def`, `\let`, `\usepackage` or similar.
- `\lean{...}` and `\dirn{...}`: none contains a space.
- Rigor vocabulary:
  - "verified" and "certified" do not occur.
  - "proved" occurs only in the Lean names `mirrorOneAxis33_proved` and `mirrorNoAxis34_proved` (ar.tex:715–716).
  - "unproved" occurs only in the negated phrase at ar.tex:611.
  - "prove" occurs at ar.tex:699 (the Lean term proves $3\le33$ by `norm_num`) and at ar.tex:746 ("what its
    certificates prove", in a sentence saying that the match was checked by reading). Both are outside this diff, were
    passed in earlier rounds, and give no label.
  - The SAT-certificate anchor is still `cake_lpr`, with lrat-check "a secondary check only", as in
    `WRITEUP/SYMMETRIC.md:232`.
  - The remark still ends with "The unconditional form of Theorem ar:thm:main is therefore computer-assisted, and it is
    not Lean-checked as a whole".
- References from other sections to `ar:` labels are only `ar:thm:main` and `ar:thm:transfer`, both export labels
  and both defined. The ar labels are unchanged, so the generated appendix is not affected.

## 6. Compile check

`build/ar_docr1audit_wrapper.tex` has the contract's wrapper content (`\documentclass[10pt]{amsart}`,
`\input{../preamble}`, `\input{../sections/ar}`). From `build/`,
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error ar_docr1audit_wrapper.tex` was run twice. The outputs
are `build/ar_docr1audit_run1.txt`, `build/ar_docr1audit_run2.txt` and `build/ar_docr1audit_wrapper.log`.
- Exit codes: 0 and 0. The document has 11 pages.
- Log contents: no `!` error, no "Missing", no multiply-defined label and no rerun request.
- **Overfull boxes: 0** (0 of any size). So there is no minor finding from the build.
- Underfull warnings: 68. Each warning, with the line that follows it, is identical to the doc-r0 audit's log
  (`build/ar_docr1audit_uf.txt` against `build/ar_docr1audit_uf_r0.txt`).
- Undefined references: only the 19 allowed foreign export labels, namely
  `fd:def:{cp,gp,inv,ngon,orient,point}`, `fd:lem:{affine-cp,affine-orient,collinear,cp-hull}`, `sr:def:classes`,
  `sr:def:iso`, `sr:thm:main`, `sr:thm:variant`, `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`, `cb:thm:c2` and
  `cb:thm:c3`.
- Rendered text (`build/ar_docr1audit.txt`):
  - It differs from the doc-r0 audit's text only in the reflow of this one paragraph, which keeps its line count.
  - Pages 1–3 have 55, 58 and 57 text lines.
  - Page 2 was inspected as an image (`build/ar_docr1audit_page-02.png`).

## 7. Findings

None.
