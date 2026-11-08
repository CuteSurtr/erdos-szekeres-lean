# Section `ar` (Affine symmetries), round doc-r0: fix log

Input: the six minor notes of `build/open_minors.json`, key `ar` (from `reviews/ar-p1-diff.md` m1–m3 and
`reviews/ar-p1-referee.md` R1–R3). Pre-edit snapshot: `snapshots/doc-r0-pre/ar.tex`, `snapshots/doc-r0-pre/ar.map.tsv`.
Paths below are relative to STAGE (`sections/`, `build/`, `reviews/`) or to RES (`SYMLEAN/...`, `C2FINAL/...`, ...).
Line numbers `ar.tex:N` refer to the edited file (807 lines; 797 before).

All six notes were checked against the sources and found correct. All six are fixed; none is declined.

## Notes

| # | note (lens) | action | location (now) | check against the sources |
|---|---|---|---|---|
| 1 | m1 (diff): the two bookkeeping theorems (cb:thm:c3, cb:thm:c2) are called "Lean-checked" without their label computer-assisted | fixed | ar.tex:739–742 | `C2FINAL/Central34Orbits.lean:291–292`: `all_cases_closed` is `decide +kernel`. `C3LEAN/C3Cover.lean:2251–2261`: `all_roots_covered` combines `all_checked` (batch facts, each `decide +kernel`), `roots_codes_match` (`:1725–1726`, `decide +kernel`) and `checkRoot_sound`. The file has no `native_decide` (its only occurrence is in the header comment, line 13). `sections/cb.tex:1116` and `:1366` and `sections/cb.map.tsv` lines 83 and 99 label both theorems computer-assisted. New text: "Two bookkeeping steps are Lean-checked, and computer-assisted because their finite checks are kernel evaluations (`decide +kernel`): ...". This keeps "Lean-checked" and does not claim that `all_roots_covered` is one single evaluation |
| 2 | m2 (diff): "including every piece of their case splits" can be read as "every subcase has its own certificate" | fixed | ar.tex:727–728 | `C2FINAL/README.md:58`: 2,385 UNSAT and 107 UNKNOWN records in the central case, so not every subcase has a certificate. Rewritten as the note suggests: "Every certificate that these claims use, including those of the pieces of their case splits, carries a recorded acceptance by the proof checker `cake_lpr`." The claim is now only about certificates that are used, which is what the records support (diff report §3) |
| 3 | m3 (diff): "the normal form C3-S/soundness.md of Threefold33" reads as if the file were the normal form | fixed | ar.tex:736 | `C3-S/soundness.md` exists under RES. New text: "the normal form of `Threefold33` (`C3-S/soundness.md`)" |
| 4 | R1 (referee): "used in the proof ... So it depends on no further axiom" does not cover `lin2_fst` and `lin2_snd` | fixed | ar.tex:60–70 (Rigor and axioms, fourth bullet) | `SYMLEAN/AffineReduction.lean:1174–1175`: both are `@[simp]` theorems with proof `rfl`. They are the only theorems of lines 1059–1533 proved by `:= rfl` (grep). Their only uses are inside `simp only` at lines 1180, 1187, 1193 and 1197; no plain `simp` after line 1175 meets a `lin2` term. Every other declaration of lines 1059–1533 enters a proof of the nine printed theorems as a term, through `rw`, or through a non-rfl simp lemma, or (definitions) through the statement of such a declaration; I rechecked all 45. The added text says that the inference needs a supplement for these two lemmas, which `simp` may apply as definitional rewrites without recording them in the proof term. It then gives the replacement argument. `rfl` and equality use no axiom. The other constants in their statements and proofs are `lin2` applied to points and the coordinates, additions and multiplications of `lin2`'s definition. The axioms check of `hasConvexNGon_of_affine_symmetry` reaches all of them, because its proof applies `T`, a value of `lin2` (Lean line 1373, `set T := lin2 s (β / s) 0 t`), to points, and `#print axioms` follows definitions as well. The wording is hedged ("may", "need not"), since I cannot inspect proof terms without running Lean. It refers to Lemma ar:lem:lin2(a) and Proposition ar:prop:averaging(b), not to the symbols s, β, t, which are introduced only later. I wrote "Their Lean proofs are `rfl`" rather than "proved by rfl" to keep the rigor vocabulary clean |
| 5 | R2 (referee): "the five case classes of Definition sr:def:classes", which defines six | fixed | ar.tex:14–15 | `sections/sr.tex:209`: "The following six propositions are defined"; the sixth is `Fourfold32`. `sr.tex` also says that sr:thm:main "takes the first five as hypotheses". The Lean premises of the five theorems (`SYMLEAN/AffineReduction.lean:1478–1479`, `:1490–1491`, `:1502–1503`, `:1511–1512`, `:1522–1523`) are `HalfTurn34`, `Threefold33`, `Fivefold35`, `MirrorOneAxis33` and `MirrorNoAxis34`. New text: "take five of the six case classes of Definition sr:def:classes (all except `Fourfold32`) as hypotheses". The head of Theorem ar:thm:main ("conditional on the five case classes") does not refer to the definition, and its body names the five, so it was left unchanged |
| 6 | R3 (referee): Coverage calls lines 1–1058 a verbatim duplicate of the whole of SymmetricReduction.lean, which has 1,059 lines | fixed | ar.tex:797–798 | `wc -l`: `SYMLEAN/SymmetricReduction.lean` has 1059 lines and `SYMLEAN/AffineReduction.lean` 1533. `cmp` of the first 1058 lines of each: identical. Line 1059 of the first file is `end ErdosSzekeres.SymReduction`, which is line 1533 of the second. New text: "They are a verbatim duplicate of lines 1--1058 of `SYMLEAN/SymmetricReduction.lean`", which matches the Sources paragraph (ar.tex:29–30) |

## Other changes

- None beyond the six notes. Two refinements were made inside fix 4 after the first build: the line numbers 1180–1197
  now name their file, and the map `T` is identified through Proposition ar:prop:averaging(b) instead of
  undefined symbols.
- No statement environment changed. The 31 `\label`s and the 30 statement heads are byte-identical to the snapshot
  (checked with `diff`). The only remark touched is ar:rem:classes (fixes 1–3); its row in the map is still accurate.
  So `sections/ar.map.tsv` is unchanged (`cmp` against the snapshot).
- No Lean-faithful statement was edited, so no statement needed re-checking against Lean. The Lean text that the new
  wording relies on was read before and after the edits: `SYMLEAN/AffineReduction.lean:1167–1197`, `:1330–1420`,
  `:1477–1529`; `C2FINAL/Central34Orbits.lean:273–298`; `C3LEAN/C3Cover.lean:1725–1726`, `:2247–2261`.
- One new internal reference, `\ref{ar:prop:averaging}`, points to a label of this section. No new foreign reference,
  no macro, and no package was added.
- Checks on `sections/ar.tex` and `sections/ar.map.tsv`: no machine path; no tool name; the
  words "verified", "certified" and "proved" occur only in Lean names (`mirrorOneAxis33_proved`,
  `mirrorNoAxis34_proved`), and "unproved" occurs in the earlier sentence "no unproved claim".

## Compile check

`build/ar_wrapper.tex` (contract wrapper). From `build/`, `nice -n 15 pdflatex -interaction=nonstopmode
-halt-on-error ar_wrapper.tex` was run twice (outputs `build/ar_docr0_run1.txt`, `build/ar_docr0_run2.txt`, log
`build/ar_wrapper.log`).

- Exit 0 on both passes. 11 pages. No `!` error, no "Missing", no multiply defined label, no rerun request.
- Overfull boxes: 0 (none of any size). Underfull warnings: 68, the same number as in the p1 audit.
- Undefined references, all export labels of other sections: `fd:def:{cp,gp,inv,ngon,orient,point}`,
  `fd:lem:{affine-cp,affine-orient,collinear,cp-hull}`, `sr:def:classes`, `sr:def:iso`, `sr:thm:main`,
  `sr:thm:variant`, `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`, `cb:thm:c2`, `cb:thm:c3`.
- I checked the text of every changed passage with `pdftotext` (`build/ar_docr0.txt`). The `\lean` names and
  `\texttt{simp only}`, `\texttt{\#print axioms}` and `\texttt{decide +kernel}` render with their spaces where
  `\texttt` is used.
