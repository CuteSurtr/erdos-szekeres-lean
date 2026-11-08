# docfix ll, round 1: re-check

Verdict: **pass**. All six findings are resolved in `sections/ll.tex` and `sections/ll.map.tsv`. No blocker or major
finding remains or was introduced. Two minor items are open: an optional clarification, and the appendix, which still
has to be regenerated.

Read: `CONTRACT.md`; the fix log `reviews/docfix-ll-r1-fix.md`; `diff -u` of `snapshots/docfix-r1-pre/ll.{tex,map.tsv}`
against `sections/ll.{tex,map.tsv}` (5 hunks in the .tex, 1 row in the map); the current `sections/ll.tex` (lines 1-140
and 655-775 in full; the rest through the diff and greps); `sections/fd.tex` (rigor labels 48-82, Lean records 190-225,
Definition fd:def:orient 274-286, Lemma "Convex hulls" fd:lem:hull 630-668); `sections/lg.tex` 50-80; `sections/sr.tex`
240-265; `sections/ec.tex` 105-115; the reviews `doc-r1-consistency.md` (M3, m19) and `doc-r1-xref-fdlllg.md`.

Records (RES-relative): `LAYERLEAN/LayerLemma.lean` (1148 lines, SHA-256 afb8542dceb0...; lines 1095-1148 re-read);
`LAYERLEAN/logs/build.log`, `logs/axioms.log`, and `logs/axioms_recheck_20261106/{README.txt,run.sh,out.txt,LayerLemmaAxioms.lean}`;
`LEANEXT/review/REPORT.md` and `LEANEXT/review/axioms.log`; `WRITEUP/note/symmetric_extremal.tex` lines 98-122;
`C6UPPER/README.md` and `C7UPPER/README.md` (cake_lpr verdicts). Also read: the repository's `lakefile.toml` and
`ErdosSzekeres/Orientation.lean:9-10`. Read-only git queries (log/show, no state change) on the history of the LAYERLEAN files.

## The six findings

1. **[xref, minor] fd:def:orient not cited or listed: RESOLVED.** The Dependencies paragraph (ll.tex:61) now lists
   Definition fd:def:orient. Step 2 of the proof of Theorem ll:thm:sixfold (ll.tex:688) says "by the formula of
   Definition fd:def:orient". The identity orient(p,c,2c-p) = (c0-p0)*2(c1-p1) - (c1-p1)*2(c0-p0) = 0 was re-derived
   with sympy from Lean's `orient` (`ErdosSzekeres/Orientation.lean:9-10`, same formula as fd:def:orient). The
   surrounding steps also check out: rotAbout c pi p = 2c-p, 3*(2pi/6) = pi, and q = c or q = p each force p = c.
   fd:def:orient is a foundations export label. After the fix, ll's external refs are exactly the 11 fd labels in
   the Dependencies list, plus lg:lem:centre (also listed) and lg:thm:nesting. lg:thm:nesting is only a pointer in
   "Sources", not a use, so "Nothing else from other sections is used" holds.
2. **[xref, minor] "certificate" reads as a fourth label: RESOLVED** (merged with 3 and 6). ll.tex:733-737 now reads:
   "In the terms of this document these unsatisfiability results are *computer-assisted*: they rest on LRAT proofs
   checked by cake_lpr, outside Lean. The project's records call such a result a 'certificate' (...;
   WRITEUP/note/symmetric_extremal.tex, lines 109--114); that is a label of the project, not one of the labels of this
   document."
   - This matches fd's three labels. fd.tex:65-72 puts "a certificate ... checked by a separate program outside Lean"
     under computer-assisted.
   - It matches ec:rem:cases ("computer-assisted results outside Lean") and sr's treatment.
   - The cited lines are exact: symmetric_extremal.tex:109 begins `\emph{Certificate}:` and the definition ends at
     line 114 ("... supporting only."). Line 108 is the Lean-checked label, so 109-114, not 108-114, is right.
   - The parenthetical paraphrase ("an unsatisfiability claim whose LRAT proof cake_lpr accepted") is faithful. The
     note's further clause, that the encoding's soundness is a written proof, is said separately in the next sentence.
   - The anchor is cake_lpr; lrat-check is not mentioned.
   - The records support "rest on LRAT proofs checked by cake_lpr":
     - C6UPPER: 64 of 64 hash-bound cake_lpr verdicts for encoder B, and the 32 encoder-A cubes with the unit
       Y(1,2), all `VERIFIED UNSAT`.
     - C7UPPER section 3: both encodings `VERIFIED UNSAT` by cake_lpr.
3. **[consistency, major] fourth label in ll, the map and the appendix: RESOLVED in ll's sources; appendix
   regeneration pending.** ll.tex is fixed (see 2). The ll:rem:hyp note in `ll.map.tsv` now reads "(computer-assisted:
   LRAT proofs checked by cake_lpr outside Lean; the project's records call such a result a certificate, a label this
   document does not use; ...)". `appendix_map.tex` (generated 20:03) still has the old text "rigor label certificate"
   at line 94; the fixer may not edit it. I ran `make_appendix.py` on a private copy of the current sections
   (`build/llrecheck_r1/regen/`): 470 rows, no error. Its ll:rem:hyp row is the corrected one, and among the ll rows
   it is the only one that differs from the current appendix. A wrapper with the preamble and the regenerated
   appendix compiles with exit 0, and the ll row renders correctly. **The orchestrator must run
   `python3 tools/make_appendix.py`.** Until then the appendix still carries the old label (minor item R2 below).
4. **[consistency, major] build.log used as the compile record of the current file: RESOLVED.** ll.tex:28-46 now rests
   the compile evidence on two records:
   - `LEANEXT/review/REPORT.md` of 4 November (item 1). It says "Build. Exit 0, no messages." and names the reviewed
     file as "SHA-256 `afb8542d...`, 1148 lines". Correct.
   - The re-check `axioms_recheck_20261106/out.txt`. It records `Exit status: 0` and `exit 0`, and its only Lean
     output is the 19 `depends on axioms` lines. I compared the first 1148 lines of the archived `LayerLemmaAxioms.lean`
     with the current `LayerLemma.lean` byte for byte using cmp: identical. The archived file is 1168 lines: those
     1148, one blank line and 19 `#print axioms` lines. Correct.

   The build.log account checks out against the git history:
   - build.log has a single commit, 6429e9a70. Its content there equals the current file, and it names no hash.
   - At 6429e9a70 LayerLemma.lean has 454 lines, SHA-256 prefix 804b1d25f79a.
   - LayerLemma.lean changed in exactly five later commits: b997a2970, 6a7ecacef, 6e3d1feb9, 88fe40ccc and 393619a57.
     The last gives 1148 lines, afb8542dceb0, and nothing in LAYERLEAN changed it after that.
   - The account agrees with fd.tex:199-206 and lg.tex:54-63.

   The other claims kept in the paragraph also hold:
   - `axioms.log` has 28 lines, all with the three standard axioms, and all 28 names are theorems of the current file.
   - The review log has 59 entries, with iterate_mem only [propext, Quot.sound].
   - The seven @[simp] lemmas (lines 236-255) are printed in none of the three logs.
   - The only `decide` is at line 1125.
   - The default lake target is `ErdosSzekeres` only (`lakefile.toml`).
5. **[consistency, minor] (C3) cites Rockafellar instead of fd's lemma: RESOLVED in substance; declining a literal
   \ref is right.** ll.tex:87-89 now gives the description as "part (b) of the lemma titled 'Convex hulls' in the
   foundations section, where it is proved for the whole document (see also Rockafellar ...)". fd:lem:hull(b) states
   exactly this (fd.tex:637). The title "Convex hulls" uniquely identifies fd:lem:hull: the other fd heads are
   "Convex position via hulls" etc. The Dependencies paragraph names the lemma too.

   Not writing `\ref{fd:lem:hull}` is correct. fd:lem:hull is not among the foundations labels listed in CONTRACT.md,
   and the contract allows "Nothing else", so a \ref would be a major under the quality bar. The xref review
   (doc-r1-xref-fdlllg.md) endorses naming non-export targets in words. "Proved" here refers to fd's written proof,
   which is fd's own usage (fd.tex:80, "a statement that is proved here"), so this is not rounding up. Roc70 stays in
   bibliography.tex and ll still cites it.
6. **[claims, minor] same sentence and map note: RESOLVED** (see 2 and 3). The wording follows the claims reviewer's
   source, with the corrected line range 109-114.

## Hunk-by-hunk referee check (diff -u against snapshots/docfix-r1-pre)

- **Hunk @@26 (Lean evidence).** Every claim was checked against the records (item 4). No rigor label changes. No
  statement is affected. The sentence on definitions ("which the same build type-checks") still has an antecedent:
  the compile described at the start of the paragraph.
- **Hunk @@52 (Dependencies).** Correct and complete; see item 1.
- **Hunk @@78 ((C3)).** Correct (item 5). It only inserts a pointer; the mathematics is unchanged.
- **Hunk @@677 (Step 2 of ll:thm:sixfold).** Only "by the formula of Definition fd:def:orient" is added. The math is
  right. I re-read the Lean source of the touched statement, `sixfold_octagon` (LayerLemma.lean:1113-1132):
  hypotheses `H : Sixfold66`, `GeneralPosition S`, `Invariant (rotAbout c (2 * Real.pi / 6)) S`, `61 ≤ S.card`;
  conclusion `HasConvexNGon 8 S`. The theorem text at ll.tex:671-675 matches it, and its head is unchanged.
  `Sixfold66` and `Sevenfold70` at lines 1102 and 1107 match ll:def:66-70.
- **Hunk @@722 (Remark ll:rem:hyp).** Correct (items 2/3/6). Hypotheses are still presented as hypotheses. "Verified",
  "certified" and "proved" are not newly used. The next sentence's antecedent ("these unsatisfiability results") is
  clear.
- **Map row ll:rem:hyp.** Correct. The map has the right header, 31 rows of 5 fields and is ASCII only. Its labels are
  exactly the 31 statement-environment labels of ll.tex.
- **Labels and heads.** The 32 `\label`s and all statement heads are identical to the snapshot. No `\newcommand` or
  `\usepackage`.
- **Forbidden content.** No machine path (scanned for the four forbidden root prefixes of the contract) and no tool name in ll.tex or ll.map.tsv.
- **LaTeX.** `\dirn` arguments contain no spaces. The Lean expressions with spaces use `\texttt`.

## Compile

Wrapper `build/ll_recheck_r1_wrapper.tex`, the same content as the contract wrapper. I ran
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice from `build/`.
- Both runs exit 0, with no `!` errors and no "Missing $" etc.
  - The log has one microtype info line ("Character 029 is missing in T1/lmr/m/sc/10"). It appears in every wrapper
    build of the project and is harmless.
- No overfull boxes. There are 51 underfull boxes, the same count as the fixer's build. They are all in statement
  heads or environments, none in the edited paragraphs.
- No rerun request. The PDF has 10 pages.
- Undefined references are only the export labels fd:def:{point,orient,gp,cp,ngon,inv,rot},
  fd:lem:{cp-hull,mono,collinear,affine-cp}, lg:lem:centre and lg:thm:nesting, as expected in the standalone check.
- The rendered text of the edited paragraphs was inspected with pdftotext.

## Remaining items

- **R1 (minor, optional; ll.tex:35-40).** The new text drops build.log because it "names no file hash" and belongs to
  the 454-line version. It then uses `LAYERLEAN/logs/axioms.log`, which also names no hash, without saying why that
  log qualifies. It was last changed in commit 393619a57, together with the current 1148-line file, and all 28 names
  in it are theorems of that file. This has no effect on correctness: every theorem of the section is also covered by
  the hash-tied re-check (19) or the report-identified review log (59). Suggested clause: "(updated in the commit of
  the current version, unlike build.log)". lg uses the same log the same way, so if this is changed it should be
  changed in both.
- **R2 (minor, orchestrator action; appendix_map.tex:94).** The appendix still shows the old ll:rem:hyp note
  ("rigor label certificate"). Regenerate with `python3 tools/make_appendix.py`. I checked a regenerated copy (item 3).
  Without regeneration, finding 3 would remain open in the appendix.

## Outside this section (for the orchestrator)

- In the regenerated appendix, the pc row pc:rem:word-scope has a new map note containing the token
  `ENCBLEAN/logs/m8_fix_build.log:29,35,`. It is set without break points and gives an overfull hbox of 49.4pt
  (regenerated appendix lines 204-205). The current appendix does not have this row text yet. This concerns pc's
  map, not ll.
