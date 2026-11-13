# Section `sr` (Reduction of symmetric sets to case classes), whole-document review round 1: recheck of the fix

**Verdict: fail.** One major problem was introduced by this fix.
- Six of the eight findings are resolved correctly, including the major claims finding F5 (item 4).
- Findings 1 and 3 are resolved in content, but not in form. The fix adds three `\ref{fd:lem:strict-supports}`, at
  sr.tex:78, 641 and 1130. The label exists in fd.tex and resolves in the full document. It is not, however, among the
  foundations labels that CONTRACT.md lets sections cite, and the contract adds "Nothing else". The quality bar rates
  "a \ref to a label not allowed by these rules" as major.
- In this same round, the ll fixer and the ll recheck applied this rule to `fd:lem:hull` (docfix-ll-r1-recheck.md,
  item 5: "a \ref would be a major under the quality bar"). The xref review doc-r1-xref-mmmb.md applied it in its
  finding F4. sr should follow the same rule.
- The fix is a one-line prose change in three places, or an amendment of the contract by the orchestrator (finding M1).
- There are also two minor findings and three observations.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`, `tools/`) or to RES (Lean sources and
records). `sr.tex:N` refers to the current file.

## Inputs

- Fix log: `reviews/docfix-sr-r1-fix.md` (8 findings, 8 fixed, 0 declined).
- Before: `snapshots/docfix-r1-pre/sr.tex` (SHA-256 `06d222511f76`..., 1134 lines) and `snapshots/docfix-r1-pre/sr.map.tsv`
  (`49c6586cddd4`...).
- After: `sections/sr.tex` (`d25ae5f7389b`..., 1166 lines) and `sections/sr.map.tsv` (`557f6af190d7`...).
- These hashes match the ones in the log.
- Lean sources re-read:
  - `SYMLEAN/SymmetricReduction.lean` (`6d5ec90a4215`, unchanged), lines 664-676, 734-770, 809-816 and 990-1059;
  - `ErdosSzekeres/Suk/SupportingLines.lean:28-30`;
  - `SYMLEAN/review/VariantChecks.lean` (`4b823bb6cf85`...), lines 1156-1210;
  - `SYMLEAN/review/ReviewSanity.lean` (`ec25136849a9`...), lines 1585-1630.
- Logs read:
  - `SYMLEAN/logs/VariantChecks.out`, `SYMLEAN/logs/ReviewSanity.out` and `SYMLEAN/logs/runs.tsv`.
- Records read:
  - `WRITEUP/SYMMETRIC.md` §0-§1;
  - `WRITEUP/note/symmetric_es7.tex` (theorem heads and `cor:only`);
  - `C2FINAL/README.md`, `C3FINAL/README.md`, `SYM5/README.md`, `C4CUT/README.md` and `SYMZ/README.md`;
  - `LIT/RELATED.md:236-237` and `NOVELTY20261106/README.md:132-133`.

## 1. The eight assigned findings

### 1 and 3. xref-srarcbsa finding 1 and consistency m15 (minor): duplicate of `fd:lem:strict-supports`. Resolved in content; the form is not allowed (M1).

- **Content.** Both statements are correct and agree.
  - Lean (`SupportingLines.lean:28`): `convexPosition_of_strict_supports (s : Finset Point) (hs : ∀ p ∈ s, ∃ q : Point,
    ∀ r ∈ s, r ≠ p → 0 < orient p q r) : ConvexPosition s`.
  - `sr:lem:supports` (sr.tex:635-638) and `fd:lem:strict-supports` (fd.tex:1041-1044) state exactly this.
  - fd's proof (fd.tex:1046-1052) and sr's proof (sr.tex:640-650) give the same half-plane argument; sr's proof only
    spells out the convexity of the half-plane. So "the short proof is repeated here" is accurate.
  - Dependencies (sr.tex:78-79), the proof (sr.tex:641-642), the Coverage paragraph (sr.tex:1129-1130) and the map note
    now all point to the fd lemma, as the reviewers asked.
- **Form.** The pointer is a `\ref` to a label outside the contract's list; see M1.
- **Map note.** The map note "same declaration as fd:lem:strict-supports (proof repeated)" is acceptable.
  - `tools/make_appendix.py` turns the label into a reference.
  - The appendix is generated at document level and already lists `fd:lem:strict-supports` as its own row
    (`appendix_map.tex:54`).
  - The contract's `\ref` rule governs section files.

### 2. consistency m7 (minor): "conditional" in the heads. Resolved.

- **Theorem heads.** `sr:thm:main` (sr.tex:947) and `sr:thm:variant` (sr.tex:986) now read "conditional on five case
  classes". Each takes exactly five classes:
  - `heptagon_of_nontrivial_isometry` (:997) takes `h2 h3 h5 hm1 hm0`;
  - `halfTurn_of_symmetric_counterexample` (:1024) takes `h3 h4 h5 hm1 hm0`.
- **Case-lemma heads.** The four case-lemma heads also carry the tag, and each tag names exactly the Lean binders:
  - `case_halfTurn` :670 (`h2`);
  - `case_odd_prime` :736 (`h3 h5`);
  - `case_fourfold` :763 (`h4`);
  - `case_mirror` :811 (`hm1 hm0`).
- The statements did not change and still match Lean.
- The tag is placed after the Lean reference; see observation O1. The heads of ec are outside this section.

### 4. claims F5 (major): rounding up in `sr:rem:main` and `sr:rem:records`. Resolved.

**`sr:rem:main` (sr.tex:974-978).**
- The remark now attributes the unconditional statement to the project.
- Source: Theorem A of `WRITEUP/SYMMETRIC.md` §0 is headed "(computer-assisted)". A "symmetry" there is "an isometry or
  an affine bijection of the plane", so "in its form for Euclidean isometries" is exact.
- The remark keeps "not Lean-checked as a whole" and adds "In this document the theorem is established only as the
  stated implication", in the reviewer's own wording.

**`sr:rem:records`.** No italic rigor label remains. Each attribution was checked against its source:

| class | text now | source | check |
|---|---|---|---|
| HalfTurn34 | "claimed in C2FINAL as computer-assisted" | `C2FINAL/README.md:7`: "Statement (claimed; computer-assisted)" | true |
| Threefold33 | "claimed in the records as computer-assisted" | `WRITEUP/note/symmetric_es7.tex:119` (`thm:A`, threefold, 33 points) is headed `[computer-assisted]`, and SYMMETRIC.md Theorem A covers it; C3FINAL itself uses no label | true |
| Fivefold35 | "claimed in the records as computer-assisted (SYM5/README.md)" | `SYM5/README.md:6`: "Theorem (computer-assisted)" | true |
| SYMZ mirror certificates | "claimed in the records as computer-assisted" | `symmetric_es7.tex:211/214` (`thm:M33`, `thm:M34`) are headed `[computer-assisted]` | true |
| Fourfold32 | "claimed in C4CUT, on computer-assisted evidence: ..." | see below | true; wording: m1 |
| mirror classes | "Lean-checked" (plain type) | the document's own status (section mb; SYMMETRIC.md §0) | true |

- **Fourfold32.** The C4CUT record gives no rigor label. `C4CUT/README.md:5` has "Statement."; lines 14-16 have
  "certificate accepted by both checkers", "exact computation" and "Encoder soundness: written proof, refereed".
  SYMMETRIC.md:166 says "certified in C4CUT", and the document does not adopt "certified".
- **The C4CUT certificate.** cake_lpr accepted the final proof (`C4CUT/README.md:68`, `s VERIFIED UNSAT`). The remark
  says that "accepted by both checkers" means that cake_lpr accepted.
- **The Fivefold35 sentence** (sr.tex:281-286). It is a hedged form of `SYM5/README.md:90`, "Each of P1 and L1 alone
  proves the theorem". The next sentence lists the conditions it relies on:
  - the encoder's soundness;
  - the two normal forms (the layer form rests on the layer lemma, which `SYM5/README.md` §2 states and proves);
  - the perturbation lemma (written, `C2ENC/perturbation.md`).

  So "given the written proofs listed next" is complete, and the sentence no longer suggests that one certificate alone
  establishes the class.

No sentence of the remark presents a class as proved.

### 5. claims F6 (minor): "B. C. Dumitru". Resolved.

- sr.tex:285 now has "B.~Dumitru".
- `LIT/RELATED.md:236-237` says "author Bogdan Dumitru per the arXiv metadata; the middle initial used earlier was not
  verified". `NOVELTY20261106/README.md:132-133` lists the correction to "B. Dumitru". `WRITEUP/SYMMETRIC.md:40` writes
  "B. Dumitru".

### 6. claims F11 (minor): Coverage lists conditional theorems unmarked. Resolved for sr.

- The Coverage items Cases (sr.tex:1134-1139) and Main results (sr.tex:1140-1145) mark every conditional declaration.
  Each lists the classes, and the lists match the Lean binders above.
- The variant is described as "the same classes with Fourfold32 in place of HalfTurn34", which is exact.
- The bridge is marked "an implication between two propositions, so conditional on its hypothesis
  MirrorExclusionLineCopy".
- ar, ec and mm are outside this section.
- One new sentence in the not-covered part does not follow the same convention; see m2.

### 7. claims F13 (minor): evidence for `VariantChecks.group_form`. Resolved.

Each claim at sr.tex:1021-1026 is true:
- `group_form` is at `VariantChecks.lean:1168` (grep).
- `SYMLEAN/logs/VariantChecks.out` prints "'ErdosSzekeres.SymReduction.VariantChecks.group_form' depends on axioms:
  [propext, Classical.choice, Quot.sound]".
- The row `review/VariantChecks.lean` of `SYMLEAN/logs/runs.tsv` has `sha256_prefix` `4b823bb6` and exit `0`.
- The file at the commit has SHA-256 `4b823bb6cf85e374...`.

The log begins with an informational "Try this: ring_nf" message: one `ring` call fell back to `ring_nf`. With exit
code 0 this message is not an error, so the remark's claim that the theorem is Lean-checked stands (observation O3).

### 8. completeness m2 (minor): review results excluded only at file level. Resolved.

**Coverage paragraph** (sr.tex:1160-1166). It names the two results explicitly, as not restated:
- `VariantChecks.group_form` (`VariantChecks.lean:1168`), with its condition;
- the converse bridge `Review.exclusionLine_of_mirrorOneAxis33` (`ReviewSanity.lean:1593`) with the equivalence
  `Review.mirrorOneAxis33_iff_exclusionLine` (`:1629`).

It also gives the reason: they lie in review files, and no statement of this document uses them.
- The line numbers were confirmed by grep.
- The namespaces are `ErdosSzekeres.SymReduction.VariantChecks` (`VariantChecks.lean:1076`) and
  `ErdosSzekeres.SymReduction.Review` (`ReviewSanity.lean:1073`). Both agree with the naming convention at
  sr.tex:112-117.
- A grep of all section files shows that no other section uses these results.

**Written argument for the group form** (sr.tex:1027-1031). It is correct.
- The composition is $\mathrm{halfTurn}_c\circ\mathrm{halfTurn}_d(p)=2c-(2d-p)=p+2(c-d)$.
- This map is a Euclidean isometry, it maps $S$ into itself, and it is not the identity when $c\ne d$.
- So the theorem makes it $\mathrm{halfTurn}_e$ for some $e$. At $p=e$ this gives $e=e+2(c-d)$, hence $c=d$.
- The Lean proof does the same (`halfTurn_comp`, `VariantChecks.lean:1156`; proof of `group_form`, :1168-1210).
- The theorem also gives $c\notin S$, $2\mid|S|$ and $34\le|S|$. Together with this argument, that yields the Lean
  disjunction:
  `(∀ g, IsEucIsometry g → Invariant g S → g = id) ∨ ∃ c, c ∉ S ∧ 2 ∣ S.card ∧ 34 ≤ S.card ∧ Invariant (halfTurn c) S
  ∧ ∀ g, ... → g = id ∨ g = halfTurn c`.
- The paraphrase in sr.tex:1022-1023 is faithful to this disjunction.

**Written argument for the converse** (sr.tex:1076-1079). It is correct.
- The first two steps of the proof of `sr:lem:mirror` use only $u_0^2+u_1^2=1$, general position and invariance. All of
  these are hypotheses of `MirrorExclusionLineCopy`.
- These steps give $|F|\le2$ and $2\mid|M|$. With $|F|+|M|=33$ this forces $|F|=1$, and `MirrorOneAxis33` applies.
- This is the Lean proof (`ReviewSanity.lean:1593-1626`; the `omega` step is at :1620).
- Evidence: `ReviewSanity.out` prints the axioms of the equivalence, and its proof term uses the converse. The
  `runs.tsv` row `review/ReviewSanity.lean` has prefix `ec251368` and exit 0, and it matches the current file
  (`ec25136849a9`...).

## 2. Diff review, hunk by hunk

| hunk (pre line) | change | check |
|---|---|---|
| @@75 Dependencies | pointer to fd lemma | content true; `\ref` form: M1 |
| @@257, @@265, @@276 `sr:rem:records` | labels attributed to records; Fivefold35 sentence; Dumitru; Fourfold32 | item 4 and item 5; Fourfold32 wording: m1. A line break after "was" (sr.tex:271) is in the source only |
| @@636 proof of `sr:lem:supports` | pointer to fd lemma | content true; `\ref` form: M1 |
| @@801, @@850, @@880, @@907 case-lemma heads | trailing "conditional on ..." | item 2; statements unchanged |
| @@941 main head, @@978 variant head | "conditional on five case classes" | item 2 |
| @@968 `sr:rem:main` | attribution to Theorem A | item 4 |
| @@1013 `sr:rem:variant` | line, logs, hash, written argument | items 7 and 8 |
| @@1056 `sr:rem:mirror-line` | equivalence, log, written converse | item 8 |
| @@1107 Coverage items | fd pointer; conditional marks | items 1 and 6 |
| @@1129 Coverage, not covered | "review and audit files"; the two review results named | item 8; converse marking: m2 |

- **Places that cite the review files.** The Coverage paragraph says these files are cited only in the paragraph on
  axioms and rigor and in three remarks. This is accurate: grep finds "review/" at sr.tex:60 (Axioms and rigor), 141
  (`sr:rem:sup`), 1021 and 1025 (`sr:rem:variant`), 1073 (`sr:rem:mirror-line`), and in the Coverage paragraph itself.
- **Map diff.** Only the notes of nine rows changed; label, kind, lean_name and file_line are unchanged. The map still
  has 46 rows of 5 fields. Its label set equals the set of statement labels in sr.tex, and the label set of sr.tex is
  the same as in the snapshot.
- **Hygiene of the 79 added lines.** They contain no machine path and no tool name. They are ASCII only,
  and they add no `\newcommand` or `\usepackage`.
- **Vocabulary.** The added lines contain no "verified", "certified" or "proved". "Certificate(s)" occurs only as a
  noun, and "established only as the stated implication" is the reviewer's own wording.

## 3. Compile check

- **Wrapper.** `build/sr_recheck_r1_wrapper.tex` has the contract content. It was compiled twice from `build/` with
  `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- **Result.** Both runs exit 0. The log has no errors, no "Missing", no overfull boxes and no multiply defined labels.
  The output has 16 pages.
- **Undefined references.** All are foreign labels:
  - `fd:def:{cp,gp,inv,ngon,orient,point,rot}`;
  - `fd:lem:{collinear,cp-hull,mono}`;
  - `fd:lem:strict-supports`, which is foreign but not an allowed label (M1);
  - `ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`, `mb:thm:classes` and `mb:thm:main3`.
- **Underfull boxes.** There are 49 underfull hboxes of badness 10000 now. The snapshot, compiled the same way
  (`build/sr_recheck_r1_pre_wrapper.tex`), has 48. All of them are in statement heads with long Lean names, as before.
- **Rendered pages.** Pages 4 and 11-15 were rendered and inspected. The new heads and remarks typeset cleanly.

## 4. Findings

**M1 (major, introduced by this fix): a `\ref` to a label that sections may not cite.**
- **Where.** sr.tex:78 (Dependencies), sr.tex:641 (proof of `sr:lem:supports`) and sr.tex:1130 (Coverage).
- **Problem.** All three use `Lemma~\ref{fd:lem:strict-supports}`.
  - CONTRACT.md lets a section cite its own labels, "the foundations labels (`fd:...`, listed below)" and the export
    labels of other sections, and adds "Nothing else".
  - The listed foundations labels are those under "Foundations export labels (section fd; every section may \ref
    these)", and `fd:lem:strict-supports` is not among them.
  - The quality bar rates "a \ref to a label not allowed by these rules" as major.
  - The fixer noted this risk in its log (section "Note on the label rule").
- **Precedent in this round.** The document already applies this reading:
  - the ll fixer declined `\ref{fd:lem:hull}` for this reason, and the ll recheck confirmed it as the right call;
  - the xref reviews doc-r1-xref-fdlllg.md and doc-r1-xref-mmmb.md (F4) treat non-export targets as not citable;
  - sr is now the only section that cites an fd label outside the list (checked by a scan of all section files).
- **Fix (either option).**
  - (a) Replace the three references by prose, as ll did. Use "the lemma 'Strict supporting lines' of the foundations
    section", which identifies it uniquely because the section is named. Suggested texts:
    - sr.tex:78: "Lemma~\ref{sr:lem:supports} is the lemma `Strict supporting lines' of the foundations section (the
      same declaration of the main library), repeated here with its short proof."
    - sr.tex:641: "This is the lemma `Strict supporting lines' of the foundations section, the same declaration of the
      main library; ..."
    - sr.tex:1130: "This is the lemma `Strict supporting lines' of the foundations section; the short proof is
      repeated here."

    The map note can stay, because the appendix is generated at document level and already lists the label.
  - (b) The orchestrator adds `fd:lem:strict-supports` to the foundations export list in CONTRACT.md. Then no text
    change is needed and M1 lapses.

**m1 (minor): the Fourfold32 bullet calls a written proof "computer-assisted evidence".**
- **Where.** sr.tex:296-298.
- **Problem.** The bullet reads "claimed in C4CUT, on computer-assisted evidence: a final certificate accepted by both
  checkers, six cuts checked by exact computation, and a written encoder proof". The list after the colon includes the
  written encoder proof, which is not computer-assisted evidence.
- **Severity.** This is not a rounding up: computer-assisted is the weakest label in play, and C4CUT gives no label.
  It is a small imprecision.
- **Suggested fix.** "claimed in C4CUT, which gives no rigor label; it rests on a final certificate accepted by both
  checkers, six cuts checked by exact computation, and a written encoder proof."

**m2 (minor): the converse bridge is not marked as conditional.**
- **Where.** The Coverage paragraph, sr.tex:1162-1164.
- **Problem.** In the same sentence, `VariantChecks.group_form` is marked "conditional on the five classes of Theorem
  ...". In the Main results item, the forward bridge is marked "an implication between two propositions, so conditional
  on its hypothesis MirrorExclusionLineCopy". The converse `Review.exclusionLine_of_mirrorOneAxis33` is called only
  "the converse bridge".
- **Severity.** "Bridge" and "converse" already say that it is an implication, so this is only uniformity with item 6.
- **Suggested fix.** "the converse bridge `Review.exclusionLine_of_mirrorOneAxis33` (an implication, conditional on
  `MirrorOneAxis33`) with the equivalence ...".

## 5. Observations (no action required by this recheck)

- **O1. Placement of the tag.** sr puts "conditional on ..." after the Lean reference. ll and ar put it before, and mb
  writes `\emph{conditional}` with a forced break. The placement is uniform within sr, and the fixer documents a
  typesetting reason: with a leading tag, the long Lean names caused overfull lines of 13.9 pt and 117 pt.
- **O2. Dumitru in the records.** `SYM5/README.md:14` still writes "B. C. Dumitru". That is a record outside the
  document, and `NOVELTY20261106/README.md:132-133` lists the correction as open. The document follows the corrected
  form.
- **O3. The VariantChecks log.** `SYMLEAN/logs/VariantChecks.out` opens with the "Try this: ring_nf" message of a
  `ring` call that fell back to `ring_nf`. Exit code 0 in `runs.tsv` shows that the file compiled without errors, so
  item 7 stands.
