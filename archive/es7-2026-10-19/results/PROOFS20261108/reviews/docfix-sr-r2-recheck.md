# Section `sr` (Reduction of symmetric sets to case classes), whole-document review round 2: recheck of the fix

**Verdict: pass.** All three findings are resolved correctly. The fix introduces no new finding.
- Finding 1 (major): no `\ref` to a non-export label is left anywhere in sr.tex. The full scan in §2 found none.
- Findings 2 and 3 (minor): the new texts match the records and the Lean source.
- Compile: the wrapper compiles cleanly, with no overfull boxes.
- Two observations for the orchestrator are in §5. Neither requires a change to sr.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`, `tools/`) or to RES (Lean sources and
records). `sr.tex:N` refers to the current file.

## Inputs

- Fix log: `reviews/docfix-sr-r2-fix.md` (3 findings, 3 fixed, 0 declined).
- Before: `snapshots/docfix-r2-pre/sr.tex` (SHA-256 `d25ae5f7389b`..., 1166 lines) and
  `snapshots/docfix-r2-pre/sr.map.tsv` (`557f6af190d7`...).
- After: `sections/sr.tex` (`899f5cba0a8d`..., 1170 lines) and `sections/sr.map.tsv` (`104dc98dcd9f`...).
- These hashes match the ones in the log.
- Lean sources re-read:
  - `ErdosSzekeres/Suk/SupportingLines.lean:27-37` (`6a8e12677685`...);
  - `SYMLEAN/SymmetricReduction.lean:464-498` and `:1052-1057` (`6d5ec90a4215`...);
  - `SYMLEAN/review/ReviewSanity.lean:1580-1632` and `:1050-1073` (`ec25136849a9`...);
  - `SYMLEAN/review/VariantChecks.lean:1168-1175` (`4b823bb6cf85`...).
- Records read:
  - `C4CUT/README.md`, all 117 lines;
  - `SYM5/README.md` §1, §2 and §4;
  - `C2FINAL/README.md:1-9`;
  - the Fourfold32 entries of `SYMLEAN/README.md`, `C2ENC/class_table.md` and `WRITEUP/SYMMETRIC.md`.
- Contract: `CONTRACT.md`. Its foundations export list still omits `fd:lem:strict-supports`, so option (b) of finding 1
  did not happen and option (a) was required.

## 1. The three assigned findings

### 1 (major): `\ref{fd:lem:strict-supports}` at three places. Resolved.

- **Text.** The three references are now prose pointers:
  - sr.tex:78-79 (Dependencies);
  - sr.tex:643-644 (proof of `sr:lem:supports`);
  - sr.tex:1131-1132 (Coverage, item Geometry).

  Each says "the lemma titled ``Strict supporting lines'' in the foundations section". This is the wording ll uses for
  "Convex hulls" (ll.tex:87), so the document is uniform.
- **The pointer is unique.** fd.tex:1042 is the only fd statement with that title. Naming the section separates it from
  sr's own lemma of the same title.
- **Content.**
  - Lean (`SupportingLines.lean:28`): `convexPosition_of_strict_supports (s : Finset Point) (hs : ∀ p ∈ s, ∃ q : Point,
    ∀ r ∈ s, r ≠ p → 0 < orient p q r) : ConvexPosition s`.
  - `sr:lem:supports` (sr.tex:637-640, unchanged) and `fd:lem:strict-supports` (fd.tex:1042-1045) both state exactly
    this.
  - "the same declaration of the main library" is true: both heads carry the same `\leanref`.
  - "because Lemma sr:lem:concyclic uses it" is true. The proof of `sr:lem:concyclic` applies `sr:lem:supports` twice,
    and the Lean proof of `convexPosition_of_concyclic` begins with `apply Suk.convexPosition_of_strict_supports`.
- **Scan.** All 204 `\ref`s in sr.tex were checked against the contract, using a script that reads the allowed sets
  from CONTRACT.md:
  - the own labels are all defined;
  - every foreign label is either in the foundations export list (`fd:def:{cp,gp,inv,ngon,orient,point,rot}` and
    `fd:lem:{collinear,cp-hull,mono}`) or an export label of the table (`ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`,
    `mb:thm:classes`, `mb:thm:main3`);
  - there are no violations.
- **Map note.** The map note of `sr:lem:supports` still says "same declaration as fd:lem:strict-supports (proof
  repeated)", as the finding allows.
  - The appendix tool turns that note into a `\ref` only in the document-level `appendix_map.tex`.
  - In the full document the reference resolves: fd.tex:1042 defines the label, and the appendix lists it as its own
    row.

### 2 (minor): Fourfold32 bullet called a written proof "computer-assisted evidence". Resolved.

The new text (sr.tex:297-300) reads: "claimed in C4CUT, which states it without a rigor label. It rests on a final
certificate accepted by both checkers, on six cuts checked by exact computation and on a written proof of the encoder's
soundness." Each claim was checked against the records.

- **"states it without a rigor label".** True.
  - `C4CUT/README.md:5` opens with "**Statement.**" and gives no label.
  - Contrast `C2FINAL/README.md:7`: "Statement (claimed; computer-assisted)".
  - The record does label the parts of its evidence (lines 14-16). So the fixer's "states it without a rigor label" is
    more exact than the suggested "gives no rigor label", and I agree with the variation.
  - No other record supplies a class-level label that the bullet omits:
    - `SYMLEAN/README.md:162` lists the same three evidence parts and no overall label;
    - `C2ENC/class_table.md:34-35` gives none;
    - `WRITEUP/SYMMETRIC.md:166` says "certified in C4CUT", which the document correctly does not adopt.
- **"a final certificate accepted by both checkers".** True.
  - Line 14 has "certificate accepted by both checkers".
  - Line 68 has cake_lpr `s VERIFIED UNSAT`, and the replay of 1 November (lines 70-71) accepted the proof with
    cake_lpr as well.
  - The anchor is cake_lpr through the remark's convention sentence (sr.tex:256-258, unchanged): "where a certificate
    below is said to be accepted by both checkers, cake_lpr accepted it, and lrat-check is only a secondary check".
- **"six cuts checked by exact computation".** True.
  - Line 15: each cut is justified by a certificate checked in exact rational arithmetic.
  - Line 57: "Six cuts".
  - Lines 79-82: the independent verifier passes all six cuts.
- **"a written proof of the encoder's soundness".** True.
  - Lines 16-17: "Encoder soundness: written proof, refereed", namely the docstring argument and `SYM5/README.md` §2.
  - The record's "refereed" is not repeated. This is right: the document keeps its own rigor vocabulary.
- **Completeness of the list.** Fivefold35 also rests on the perturbation lemma; the list for Fourfold32 does not need
  it.
  - That lemma is stated "for every odd order" (`SYM5/README.md:44`).
  - For even order the encoder has no centre point (`SYM5/README.md` §4, line 137).
  - The sector representatives are unique by general position, through antipodal pairs (`C4CUT/README.md:30-32`).
  - So the three-part list matches the record's own account (lines 13-20).
- **Unchanged parts.** They are still correct.
  - "used only by Theorem sr:thm:variant" matches the docstring at `SymmetricReduction.lean:493-495`.
  - The credit to Subercaseaux, Mackey, Qian and Heule matches `C4CUT/README.md:8-9`.
- **Rigor.** The class is not presented as proved. The new lines contain no "verified", "certified" or "proved".
- **Map.** The map note of `sr:rem:records` now ends "(C4CUT states Fourfold32 without one)", in sync with the bullet.

### 3 (minor): the converse bridge was not marked conditional. Resolved.

New text (sr.tex:1164-1168): "the converse bridge Review.exclusionLine_of_mirrorOneAxis33
(SYMLEAN/review/ReviewSanity.lean:1593, an implication between two propositions, so conditional on its hypothesis
MirrorOneAxis33) with the equivalence Review.mirrorOneAxis33_iff_exclusionLine of the two propositions (line 1629 of the
same file), which asserts neither of them."

- **Lean.**
  - `ReviewSanity.lean:1593`: `theorem exclusionLine_of_mirrorOneAxis33 (h : MirrorOneAxis33) :
    MirrorExclusionLineCopy`. This is an implication with hypothesis `MirrorOneAxis33`, so "conditional on its
    hypothesis MirrorOneAxis33" is exact.
  - `:1629`: `theorem mirrorOneAxis33_iff_exclusionLine : MirrorOneAxis33 ↔ MirrorExclusionLineCopy`. It has no
    hypotheses, and an equivalence asserts neither side, so "which asserts neither of them" is exact.
  - The namespace is `ErdosSzekeres.SymReduction.Review` (`:1073`), which matches the naming convention.
  - Both line numbers were confirmed by grep.
- **The hypothesis is the document's class.** Lines 1-1059 of `ReviewSanity.lean` are byte-identical to
  `SymmetricReduction.lean` (1059 lines; checked with `cmp`). So the `MirrorOneAxis33` and `MirrorExclusionLineCopy` of
  the review theorems have the text of Definitions sr:def:classes and sr:def:exclusion-line.
- **Uniformity.** The wording now matches:
  - the Main results item (sr.tex:1146-1147), which marks the forward bridge "an implication between two propositions,
    so conditional on its hypothesis MirrorExclusionLineCopy";
  - the marking of `VariantChecks.group_form` in the same sentence, which is conditional on five classes and agrees with
    its binders `h3 h4 h5 hm1 hm0` (`VariantChecks.lean:1169-1170`);
  - Remark `sr:rem:mirror-line` (sr.tex:1074-1076), which calls the converse "the converse implication".
- **Map.** The note of `sr:rem:mirror-line` was not changed and is still accurate.

## 2. Diff review, hunk by hunk (`diff -u` of snapshot and current file)

| hunk (pre line) | change | check |
|---|---|---|
| @@75 Dependencies | `\ref{fd:lem:strict-supports}` replaced by a prose pointer; "Remarks~\ref{sr:rem:records}" now ends its source line | finding 1. The pointer is true and unique, the reference is allowed, and the PDF reads "Remarks 1.8 and 1.40" |
| @@293 `sr:rem:records`, Fourfold32 | new framing of the evidence | finding 2; every claim checked against C4CUT, SYM5, SYMLEAN/README and the class table |
| @@638 proof of `sr:lem:supports` | prose pointer | finding 1. The rest of the half-plane proof is unchanged and correct: $\varphi$ is affine, the open half-plane is convex, $s\setminus\{p\}\subseteq H$, and $\varphi(p)=0$ |
| @@1126 Coverage, Geometry | prose pointer | finding 1 |
| @@1160 Coverage, not covered | the converse is marked conditional, and the equivalence is marked as asserting neither side | finding 3 |
| map @@6 `sr:rem:records` | note extended | in sync with the bullet |

- **Statements.**
  - The statement heads of the snapshot and the current file are identical.
  - Among the statement environments, only the body of `sr:rem:records` changed, a remark with no Lean statement.
  - The Lean statements re-read for the touched passages are `convexPosition_of_strict_supports`, `Fourfold32`,
    `MirrorOneAxis33`, `MirrorExclusionLineCopy`, the two review theorems and `group_form`. All of them agree with the
    text.
- **Labels and map.**
  - The `\label` lists of the snapshot and the current file are identical (55 labels), and all 8 export labels are
    defined.
  - The map has 46 rows of 5 fields. Its labels and kinds equal the statement environments of sr.tex, in order.
- **Hygiene of sr.tex and sr.map.tsv.**
  - ASCII only.
  - No machine path and no tool name.
  - No `\newcommand`, `\def`, `\let` or `\usepackage`.
  - The 17 added lines contain no "verified", "certified" or "proved". "Certificate" occurs only as a noun.
- **LaTeX.** The quotes use LaTeX form (``...''), the apostrophe in "encoder's" is plain, `\dirn` paths have no
  spaces, and the tie in "line~1629" is fine.

## 3. Compile check

- **Wrapper.** `build/sr_recheck_r2_wrapper.tex` has the contract content. It was compiled twice from `build/` with
  `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- **Result.** Both runs exit 0, and the output has 16 pages. The log has:
  - 0 errors, 0 "Missing" and no multiply defined label;
  - no rerun request (the "rerun" matches are package information lines);
  - **0 overfull boxes**.
- **Undefined references.** All are allowed foreign labels:
  - `fd:def:{cp,gp,inv,ngon,orient,point,rot}` and `fd:lem:{collinear,cp-hull,mono}`;
  - `ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`, `mb:thm:classes` and `mb:thm:main3`.

  `fd:lem:strict-supports` no longer appears.
- **Underfull boxes.** The snapshot was compiled the same way (`build/sr_recheck_r2_pre_wrapper.tex`, from a copy in
  `build/srrecheck-r2/pre/`). Counted the same way, before and after are identical: 47 underfull hboxes (26 of them of
  badness 10000) and 2 underfull vboxes. The fixer's figure of 48 comes from a different count; with the same method,
  the fix adds none.
- **Rendered pages.** Pages 2, 5, 9, 15 and 16 contain the changed passages. Their text was extracted, and pages 5, 9,
  15 and 16 were inspected as images (`build/srrecheck-r2/img/`). The new passages typeset cleanly. The path in the
  Coverage sentence breaks at a dot ("ReviewSanity.|lean:1593"), like other `\dirn` paths in the document.

## 4. Findings

None. No blocker, major or minor finding remains, and none is introduced.

## 5. Observations (for the orchestrator; no change to sr required)

- **O1. Regenerate the appendix.** `appendix_map.tex` (written at 20:03) predates both sr fixes. Its rows are stale:
  - the `sr:rem:records` row still has the note from before round 1 ("project records and rigor labels supplying each
    class");
  - the `sr:lem:supports` row lacks "same declaration as fd:lem:strict-supports (proof repeated)".

  A dry run of `tools/make_appendix.py` on a copy (`build/srrecheck-r2/regen/`) exits 0 with 470 rows. Both sr rows
  render as intended, and the note of `sr:lem:supports` becomes `Lemma~\ref{fd:lem:strict-supports}`, which resolves in
  the full document. Run `python3 tools/make_appendix.py` before the next full build. The fixer flagged the same step.
- **O2. Option (b) of finding 1 is moot.** If the orchestrator later adds `fd:lem:strict-supports` to the foundations
  export list, the prose pointers can stay as they are; they are accurate either way.
