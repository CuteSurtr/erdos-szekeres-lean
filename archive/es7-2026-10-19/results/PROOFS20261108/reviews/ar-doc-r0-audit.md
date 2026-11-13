# Section `ar` (Affine symmetries), round doc-r0: diff audit

Lens: diff. Inputs:
- the pre-edit snapshot `snapshots/doc-r0-pre/ar.tex` (797 lines) and `ar.map.tsv`;
- the current `sections/ar.tex` (807 lines) and `sections/ar.map.tsv`;
- the fix log `reviews/ar-doc-r0-fix.md`;
- the notes it addressed: `reviews/ar-p1-diff.md` (m1, m2, m3) and `reviews/ar-p1-referee.md` (R1, R2, R3).

Paths below are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or to RES (Lean sources and
records). Line numbers `ar.tex:N` refer to the current file.

**Verdict: pass.**
- No blocker and no major finding. There is one minor finding (m1, optional): a line reference that names the line
  where `T` is defined, not where it is applied.
- All 6 notes marked fixed are fixed correctly. None was declined.
- The build is clean: both passes exit 0, there is no error, and there are 0 overfull boxes.

## 1. Scope of the diff

- `diff -u` gives 5 hunks in `ar.tex` (797 → 807 lines). `ar.map.tsv` is byte-identical to the snapshot (`cmp`).
- No statement environment, `\label` or `\leanref` changed. The list of `\label` lines and statement-head lines is
  identical in both files. The touched passages are the introduction, the "Rigor and axioms" list,
  Remark `ar:rem:classes` and the Coverage paragraph.
- No Lean-faithful statement was edited. I re-read the Lean text that every new claim relies on (§2).
- Lean files read, with SHA-256 prefixes:
  - `SYMLEAN/AffineReduction.lean` `41cfc0b60aec` (1533 lines);
  - `SYMLEAN/SymmetricReduction.lean` `6d5ec90a4215` (1059 lines);
  - `SYMLEAN/AffineReductionAxioms.lean` `f6cb9372b174` (1544 lines);
  - `SYMLEAN/logs/AffineReductionAxioms.out` `38d0b6f59398`;
  - `C2FINAL/Central34Orbits.lean` `b396a26b2430` (298 lines);
  - `C3LEAN/C3Cover.lean` `4b64293df2ea` (2327 lines).

## 2. Hunk-by-hunk check

| # | where (current) | change | check | result |
|---|---|---|---|---|
| H1 | ar.tex:13–15 (introduction) | "take the five case classes of Definition sr:def:classes" → "take five of the six case classes of Definition sr:def:classes (all except `Fourfold32`)" | `sections/sr.tex:209–228`: the definition says "The following six propositions are defined" and lists six, the sixth being `Fourfold32`. `sr.tex:239`: sr:thm:main takes the first five. Lean premises of the five theorems (`AffineReduction.lean:1478–1479`, `1490–1491`, `1502–1503`, `1511–1512`, `1522–1523`): exactly `HalfTurn34`, `Threefold33`, `Fivefold35`, `MirrorOneAxis33`, `MirrorNoAxis34`. The other mentions of "five case classes" (ar.tex:73, 656) refer to the theorems' premises, not to the definition | correct |
| H2 | ar.tex:60–70 (Rigor and axioms, 4th bullet) | supplement to the axioms inference for `lin2_fst`, `lin2_snd` | see §3 | correct; minor m1 |
| H3 | ar.tex:727–728 (Remark ar:rem:classes, "SAT certificates") | "including every piece of their case splits" → "including those of the pieces of their case splits" | Narrows the claim to the certificates that are used. Central: `C2FINAL/recount.py:16–17` counts a record only with `cake_lpr` = `s VERIFIED UNSAT` (and lrat-check, status UNSAT). `C2FINAL/README.md:58` lists 2,385 UNSAT and 107 UNKNOWN records, so not every subcase has a certificate, and the new wording no longer suggests it. Threefold: `C3FINAL/README.md` ("Every certified record used here was accepted by both proof checkers ... cake_lpr `s VERIFIED UNSAT`"). Fivefold: `WRITEUP/SYMMETRIC.md` Theorem 5 names proofs P1 and L1, and `SYM5/README.md:84–85` records `s VERIFIED UNSAT` for both. L2 (no cake_lpr run) is not used by the claim. The anchor is cake_lpr, and lrat-check stays "a secondary check only" (`SYMMETRIC.md` §3, "Revised 6 November 2026") | correct |
| H4a | ar.tex:736 | "the normal form `C3-S/soundness.md` of `Threefold33`" → "the normal form of `Threefold33` (`C3-S/soundness.md`)" | `C3-S/soundness.md` exists ("hull and convex-layer normalization — soundness argument"; "Normal form (C3a/C3b)"). `SYMMETRIC.md:58` lists it as "A projective normal form (`C3-S/soundness.md`, written proof, audited)" | correct |
| H4b | ar.tex:739–742 | "Two bookkeeping steps are Lean-checked:" → "Two bookkeeping steps are Lean-checked, and computer-assisted because their finite checks are kernel evaluations (`decide +kernel`):" | `Central34Orbits.lean:291–292`: `all_cases_closed` is `decide +kernel` (as are `subcases_reflection`, `:273`, and `closed_are_subcases`, `:284`). `C3Cover.lean:2251–2261`: `all_roots_covered` uses `roots_match` (`:1720–1722`) and `roots_codes_match` (`:1725–1726`), both `decide +kernel`, then `all_checked`, which chains `batch0`…`batch126` (all 127 are `decide +kernel`, by script), and the proof `checkRoot_sound`. There is no `native_decide` in `C3Cover.lean` except the header comment at line 13 ("no `native_decide`") and none in `Central34Orbits.lean`. Section cb labels both theorems computer-assisted (`cb.map.tsv` rows 83 and 99; heads `cb.tex:1119`, `:1370`). Both labels are kept and nothing is rounded up | correct |
| H5 | ar.tex:797–798 (Coverage) | "a verbatim duplicate of `SymmetricReduction.lean`" → "a verbatim duplicate of lines 1--1058 of `SymmetricReduction.lean`" | `cmp` on the first 1058 lines of the two files: identical. `SymmetricReduction.lean` has 1059 lines; its line 1059 (`end ErdosSzekeres.SymReduction`) is line 1533 of `AffineReduction.lean`. This now matches the Sources item (ar.tex:29–30). `iterate_mem` is at line 69 and `point_ext` at line 502, as cited | correct |

## 3. Hunk H2 in detail (the new axioms argument)

The bullet keeps its original two sentences. It then says that the inference "used in the proof, so no further axiom"
needs a supplement for `lin2_fst` and `lin2_snd`, and gives one. I checked each claim.

1. "Their Lean proofs are `rfl`". `AffineReduction.lean:1174–1175`: both are `@[simp] theorem ... := rfl`. A grep
   of lines 1059–1533 finds no other theorem proved by `rfl`. The other `rfl` occurrences are `obtain ⟨_, _, rfl⟩`
   patterns at 1255–1257, 1269, 1409, 1415–1416 and 1517.
2. "used only inside `simp only` (`SYMLEAN/AffineReduction.lean`, lines 1180, 1187, 1193 and 1197)". These four lines
   are the only textual uses. Both lemmas carry `@[simp]`, so I also checked the implicit uses. The calls after line
   1175 that use the default simp set are `simp` at 1203, 1238, 1456 and 1458, `simpa [orient]` at 1358, `field_simp`
   at 1188, 1193, 1197 and 1381, and `norm_num` at 1485, 1496, 1507 and 1529. At 1188, 1193 and 1197 the `simp only`
   has already removed every `lin2` term. At the other lines the goals are, in order, iterates at 0, matrix entries,
   coordinates of `!![a, b; c, d] *ᵥ p`, the orientation of `p1 - p0, p2 - p0`, `β²/α + (αγ − β²)/α = γ`, and
   `3 ≤ 33`. None contains a `lin2` term. So the claim is exact.
3. A script (`build/ar_docr0audit_uses.py`) classified the uses of all 45 declarations of lines 1059–1533.
   - `lin2_fst` and `lin2_snd` are the only ones that occur solely in simp lists.
   - The three with no use (`heptagon_of_nontrivial_affineMap`, `_affineEquiv_image`, `_affine_coords`) are
     themselves among the nine printed theorems.
   - The definitions that are also unfolded by `simp` (`nsq`, `gA`, `gB`, `gC`, `avgQ`, `qA`, `qB`, `qC`) also occur
     in statements or definition bodies that are reached (e.g. `qA` in `avgQ_eq`, used by `rw` at 1383, and `gA`
     in the body of `qA`).
   - `mulVec2_fst` and `mulVec2_snd` are proved by `simp [...]`, not by `rfl`, and are also used by `rw` (1455, 1457).

   So the supplement is needed for exactly these two lemmas, as the text implies.
4. "may apply such lemmas as definitional rewrites without recording them in the proof term". This is hedged
   ("may", "need not"). It holds whether or not this Lean version treats these two lemmas as definitional simp
   lemmas, and the replacement argument does not depend on it.
5. "their statements and proofs mention only `lin2` applied to points and the coordinates, additions and
   multiplications in the definition of `lin2`". Here `lin2` (line 1167) is a bundled linear map with
   `toFun p := ![a * p 0 + b * p 1, c * p 0 + d * p 1]`. The statement `lin2 a b c d p 0 = a * p 0 + b * p 1` uses the
   coercion of `lin2 a b c d` to a function ("applied to points"), the literals `0`, `1 : Fin 2`, and real `+`, `*`,
   all of which occur in that definition. The proof term is `rfl` at the left-hand side.
6. "The axioms check of `hasConvexNGon_of_affine_symmetry` reaches all of these". It is one of the nine
   `#print axioms` lines (`AffineReductionAxioms.lean:1540`; log: `[propext, Classical.choice, Quot.sound]`). Its
   proof sets `T := lin2 s (β / s) 0 t` (line 1373) and applies `T` to points (1375–1376, 1385, 1398, 1401–1405).
   `#print axioms` follows constants through definition bodies. `T` is the map of Proposition
   `ar:prop:averaging`(b) (ar.tex:497–499: `T = lin2(s, β/s, 0, t)`). Lemma `ar:lem:lin2`(a) is the statement of
   `lin2_fst` and `lin2_snd` (ar.tex:276–277).
7. Conclusion "these two lemmas depend on no further axiom either": it follows from 5 and 6, and it is true.

The rigor vocabulary is respected. The text says "Their Lean proofs are `rfl`", not "proved by", and it adds no new
label.

## 4. Notes marked fixed, declined or duplicate

| note | fixed by | judgement |
|---|---|---|
| p1-diff m1 (bookkeeping theorems without "computer-assisted") | H4b | fixed. The text keeps "Lean-checked", adds "computer-assisted" with the reason (kernel evaluation, `decide +kernel`), and matches `cb.map.tsv`. It does not claim that `all_roots_covered` is one single evaluation |
| p1-diff m2 ("every piece of their case splits") | H3 | fixed as the note suggested |
| p1-diff m3 (file name standing for the normal form) | H4a | fixed as the note suggested |
| p1-referee R1 (axioms inference does not cover the rfl lemmas) | H2 | fixed. The supplement is correct and complete (§3). It is longer than the referee's one-clause suggestion but contains no false claim |
| p1-referee R2 ("the five case classes of Definition sr:def:classes", which has six) | H1 | fixed |
| p1-referee R3 (Coverage overstates the duplicate) | H5 | fixed. It now agrees with the Sources item |

No note was declined and none was marked duplicate.

## 5. Contract checks

- Machine paths (`/private`, `/Users`, `/home`, `/tmp`): no hit in `ar.tex` or `ar.map.tsv`.
- Tool names: no hit in `ar.tex` or `ar.map.tsv` (case-insensitive grep).
- Rigor vocabulary: "verified", "certified", "proved" and "proven" occur only in the Lean names
  `mirrorOneAxis33_proved` and `mirrorNoAxis34_proved`. "certif" also matches the noun "certificate(s)" at lines 722,
  727 and 746, which is fine. No hypothesis is presented as proved. Remark `ar:rem:classes` still ends with "The
  unconditional form of Theorem ar:thm:main is therefore computer-assisted, and it is not Lean-checked as a whole."
- Macros and packages: no `\newcommand`, `\renewcommand`, `\def`, `\let`, `\usepackage` or similar.
- `\lean`/`\texttt`: the new Lean expressions with spaces use `\texttt` (`simp only`, `\#print axioms`,
  `decide +kernel`). `\lean{rfl}`, `\lean{lin2}` and the theorem names have no spaces.
- References: the foreign references are the same 19 export labels as before (fd ×10, `sr:def:iso`,
  `sr:def:classes`, `sr:thm:main`, `sr:thm:variant`, `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`, `cb:thm:c2`,
  `cb:thm:c3`), all allowed. The two new references, `ar:lem:lin2` and `ar:prop:averaging`, are internal and defined.
- Map: unchanged and still accurate. The row `ar:rem:classes` reads "what supplies the five class hypotheses and with
  which rigor label".

## 6. Compile check

`build/ar_docr0audit_wrapper.tex` has the contract's wrapper content (`\documentclass[10pt]{amsart}`,
`\input{../preamble}`, `\input{../sections/ar}`). From `build/`,
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error ar_docr0audit_wrapper.tex` was run twice. The outputs
are `build/ar_docr0audit_run1.txt`, `build/ar_docr0audit_run2.txt` and `build/ar_docr0audit_wrapper.log`.
- Both passes exit 0. The document has 11 pages. There is no `!` error, no "Missing", no multiply-defined label and no
  rerun request (the only "rerun" lines are `rerunfilecheck` package information).
- **Overfull boxes: none** (0 of any size). There are 68 underfull warnings, the same number as in the p1 audits.
- Undefined references are all allowed export labels of other sections: `fd:def:{cp,gp,inv,ngon,orient,point}`,
  `fd:lem:{affine-cp,affine-orient,collinear,cp-hull}`, `sr:def:classes`, `sr:def:iso`, `sr:thm:main`,
  `sr:thm:variant`, `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`, `cb:thm:c2`, `cb:thm:c3`.
- Rendered text (`build/ar_docr0audit.txt`) and pages 2 and 10 were inspected. The new bullet, the nested list of the
  remark and the Coverage item are set correctly, and `simp only`, `#print axioms` and `decide +kernel` keep their
  spaces.

## 7. Findings

**m1 (minor, optional): "(Lean line 1373)" names the line that defines `T`, not a line that applies it to points.**
- Location: ar.tex:67–68. "because its proof applies the map $T$ of Proposition ar:prop:averaging(b), a value of
  `lin2`, to points (Lean line 1373)".
- Issue: line 1373 is `set T := lin2 s (β / s) 0 t with hT`. It shows that `T` is a value of `lin2`, but it does not
  apply `T` to a point. The first applications are at lines 1375–1376 (`Ti (T x)`, `T (Ti x)`), then 1385 and 1398.
  The reference is off by two lines at most, and the argument is unaffected.
- Fix: "(Lean lines 1373–1376)", or "(`T` is set at Lean line 1373 and applied to points from line 1375 on)".

## 8. Notes (not findings)

- The fix log cites `sections/cb.tex:1116` and `:1366` for the cb heads. In the current `cb.tex`, which was edited in
  the same round, the heads of `cb:thm:c3` and `cb:thm:c2` are at lines 1119 and 1370. This concerns only the log. The
  section refers to these theorems by label, and the map rows the log cites (`cb.map.tsv` 83 and 99) are correct.
- Evidence script: `build/ar_docr0audit_uses.py`, a use classification of the 45 declarations of lines 1059–1533,
  run with `nice -n 15 python3`.
