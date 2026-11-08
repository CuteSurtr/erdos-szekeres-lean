# Whole-document review, round 1, lens: claims and front matter

**Verdict: does not pass.** 5 major findings (F1 to F5) and 14 minor findings (F6 to F19). There is no blocker. No
statement in the document calls a hypothesis proved, and no theorem is presented as new mathematics. Every SAT verdict
that the document relies on is anchored on cake_lpr. All 470 appendix rows match their statement heads and the Lean
sources. The major findings concern four things:
- the abstract overstates how complete the proofs are (F1);
- the scope "Stage 1" is never defined (F2);
- three works cited in the text are missing from the bibliography (F3);
- two sections give this document's label "computer-assisted" to the *unconditional* symmetric statement, which this
  document proves only conditionally (F4, F5).

Path conventions in this report:
- `proofs.tex`, `preamble.tex`, `bibliography.tex`, `appendix_map.tex`, `sections/`, `tools/`, `build/` are relative to
  STAGE;
- record paths (`LAYERLEAN/...`, `WRITEUP/...`, ...) are relative to `cloud/es7-2026-10-19/results`;
- `ErdosSzekeres/...` and `docs/...` are relative to the repository root.

## What was checked, and how

1. **Front matter.**
   - I read `proofs.tex` (title, date, abstract) and the rendered pages 1–3 of `build/doc-r1/proofs.pdf` (187 pages).
   - I compared the abstract with the "Purpose", "Rigor labels" and "Coverage" paragraphs of `sections/fd.tex`.
   - `pdfinfo` gives empty Title and Author fields.
   - `build/doc-r1/proofs.log`: no error, no undefined or multiply defined reference, no rerun request. There is one
     overfull box (F17).
2. **Bibliography.**
   - I compared each `\bibitem` with `WRITEUP/P1/p1.tex`, lines 1237–1317.
   - I grepped all 12 sections for author names, titles, arXiv numbers and venues. No section uses `\cite`; every
     citation is inline.
   - Listed works and where they are cited:
     - Baek: mb.tex:191, sa.tex:411, sr.tex:286.
     - Erdős–Szekeres 1935: mb.tex:221, mm.tex:681.
     - Rockafellar: ll.tex:81 (Theorem 2.3 is correct).
     - Rudin: fd.tex:1127–1131 (Theorems 2.41 and 4.16) and lg.tex:159 (Chapter 8). The numbering is correct.
     - Subercaseaux–Mackey–Qian–Heule: sr.tex:296.
     - Lean 4 and Mathlib: named in fd.tex:6.
   - Works cited in the text but not listed: F3.
3. **Appendix.**
   - I copied the sections, maps and generator to `build/claims_doc_r1/regen/` and ran `python3 -I tools/make_appendix.py`
     there. The output is byte-identical to `appendix_map.tex` (470 rows).
   - `build/claims_doc_r1/mapcheck.py` compares every map row with its statement environment. Results:
     - kind: all match;
     - label: all match;
     - Lean names and file:line pairs against the `\leanref` heads: the only differences are expected ones. Four fd
       remark rows list declarations that the remark discusses (see F15). Two pc rows carry the extra names on the parts
       of the statement, not in the head.
   - `build/claims_doc_r1/countpairs.py` and `nscheck.py` check all 677 (name, file:line) pairs of the maps against the
     Lean sources at commit 7e32ee259. Each line carries a declaration keyword. The full name, with the namespace
     computed from the `namespace`/`section`/`end` structure, equals the map name in all 677 cases.
   - Every path in a note exists. Every `file:line` in a note points at the declaration or log line it names.
   - I read a 42-row sample (3–4 rows per section, `build/claims_doc_r1/sample40.txt`) against the statement text. All
     rows are consistent, including the "computer-assisted" and "takes hypotheses" notes.
   - Findings on the appendix: F15–F17.
4. **Rigor and evidence claims.**
   - I grepped all sections for:
     - rigor labels and status words: Lean-checked, computer-assisted, refereed, verified, certified, proved,
       unconditional;
     - checkers and certificates: certificate, cake_lpr, lrat-check, proof checker;
     - Lean mechanics: kernel, decide, native_decide, axioms;
     - novelty words: new, first, priority.
   - I then read each hit in context, together with the intro, evidence and coverage paragraphs of every section.
   - Results:
     - No `native_decide` occurs in scope.
     - No hypothesis (Sixfold66, Sevenfold70, the case classes, (hM), MirrorExclusionLineCopy) is called proved.
     - Every mention of lrat-check carries the "secondary, not counted" disclaimer, or is covered by one in the same
       remark.
     - No novelty claim was found.
5. **Record spot checks (all consistent with the text unless a finding says otherwise).**
   - **Layer-lemma logs.**
     - `LAYERLEAN/logs/build.log`: exit 0, 0 messages.
     - `LAYERLEAN/logs/axioms.log`: 28 lines.
     - The 6 November re-check: 19 lines.
     - `LEANEXT/review/axioms.log`: 59 lines, with `iterate_mem` on `[propext, Quot.sound]`.
     - The seven theorems that lg says are missing from `axioms.log` are indeed missing.
     - Log hashes `3c4b7aac502e`, `386c4f578725`, `a59c3816cbe7`.
   - **C2FINAL.** No compile or axioms log exists anywhere in the records. README §6, line 153, says "axioms `propext`
     only, about 6 s".
   - **C3LEAN.** The axiom lines of `C3LEAN/logs/compile.log` are exactly as cb states.
   - **SYMLEAN.**
     - `SYMLEAN/logs/SymmetricReduction.out` is empty.
     - `SYMLEAN/logs/runs.tsv` rows are as cited.
     - `SymmetricReductionAxioms.out` is as cited.
   - **MIRRORETV.** `MIRRORETV/lean/MirrorMain.out`, lines 848–863, lists the 16 theorems. The log has 121 warnings and
     0 errors.
   - **Other axiom logs.** The ec logs as cited:
     - `LEANEXT/es7corr/axioms.log`;
     - `ES8SYM/lean/C6check.out`, which has no line for `m4_with_centre_counter`;
     - `PRIMEFOLD/compat/lean/PCompatCore.out`.
   - **Line counts and hashes.** I recomputed them for 20 Lean files cited in the source tables. All match, and
     `C3Cover.lean` lines 29–329 are identical to `prelude.lean` lines 1–301.
   - **ES8SYM.** `ES8SYM/README.md`, lines 258–260, gives the prefixes `8c090168` and `4d42e2fb`.
   - **Checkers and trust base.**
     - `LRATCHECK20261105/README.md` is consistent with the text.
     - `WRITEUP/note/symmetric_extremal.tex`, lines 108–114, gives the label definitions.
     - `WRITEUP/SYMMETRIC.md` §0 ("Theorem A (computer-assisted)") and §3 (trust base: only cake_lpr) are as cited.
   - **C2RECHECK.** §4: 65 of 65 Mac-only units re-solved. So the claim of ar.tex:727–728 holds.
   - **C6UPPER and C7UPPER.** The cake_lpr verdicts are as described in ll.
   - **Sixfold66 and Sevenfold70.** Only `ENCBLEAN/geo/ES8Geo/Main.lean` has theorems that conclude `Sixfold66`. None
     concludes `Sevenfold70`. Both match ll.tex:712–714.
   - **"Refereed" in the records.** `C2ENC/perturbation.md` lines 3–5 and `C4CUT/README.md` line 16 say "refereed"; see
     F12 for what that word covers.
   - **Dumitru's name.** See F6.
   - **Lean units not covered.** I counted lines starting with `theorem` or `lemma` in Lean units on symmetric sets that
     no section covers (F2).
6. **Hygiene.** No machine path and no tool name occurs in `proofs.tex`, `preamble.tex`,
   `bibliography.tex`, `appendix_map.tex`, `sections/*.tex` or `sections/*.map.tsv`.

## Findings

### F1 (major, front): the abstract overstates the completeness of the proofs

- **Location.** `proofs.tex:12–18`, the sentence "Each section … gives a complete proof that can be checked without Lean".
- **Issue.** The abstract omits both exceptions that fd's "Purpose" paragraph (fd.tex:10–13) states.
  - *Cited theorems.* Baek's theorem (Theorem 10.4, `mb:thm:baek`) and the Erdős–Szekeres cups–caps theorem
    (`mb:thm:capcup`) have no proof in this document; they are cited. Everything resting on them has a proof only modulo
    these citations: `mb:thm:seven`, `mb:thm:eight`, `mb:thm:nine`, `mb:thm:classes`, `sa:thm:baek-seven`, and the
    instances in `mm:rem:hm`.
  - *Computer-assisted statements.* Their proofs rest on a machine computation. For several, the document says
    explicitly that no hand proof is given:
    - `cb:fact:batches` (cb.tex:740);
    - `cb:fact:c2-sub` (cb.tex:1368);
    - `cb:thm:c2` (cb.tex:1379: "no hand proof is given, and none is possible without the explicit lists").

  The abstract's later sentence "Finite computations are … marked as computer-assisted" does not withdraw "checked
  without Lean". So the abstract claims more than fd does.
- **Fix.** Replace the sentence with, for example:

  > "…and gives a written proof that a mathematician can check without Lean, with two exceptions: two published
  > theorems that the Lean code uses (Baek's theorem and the cups–caps theorem of Erdős and Szekeres) are cited, not
  > reproved; and statements marked computer-assisted are reduced to a finite computation that is stated precisely but
  > not carried out by hand."

### F2 (major, front): "Stage 1" is never defined; the title suggests that all Lean-checked results on symmetric sets are covered

- **Location.**
  - `proofs.tex:6`: title "Written proofs of the Lean-checked results, Stage 1: symmetric point sets".
  - `proofs.tex:12–13`: abstract.
  - fd.tex:1242: "…lie outside Stage 1", the only other use of the term.
- **Issue.** Nowhere does the document say what Stage 1 covers. Its covered units are:
  - LAYERLEAN;
  - LEANEXT: orbit, merged, keys, phase, linked, capstone, es7corr;
  - SYMLEAN: the reduction files and `mirror/ReductionThreeClasses.lean`;
  - MIRRORETV/lean, ES8SYM/lean and PRIMEFOLD/compat/lean;
  - C3LEAN, C2FINAL, AUDIT3/A1_reduction and ES7SPLIT/review/equivalence;
  - the main-library files that these use.

  Several Lean units about symmetric point sets are not covered. Counts are lines that start with `theorem` or `lemma`:
  - `H` (125), `H2` (104), `H3` (74), `V1-L` (8), `V2-L` (1,695 `theorem` lines) and `V2-L2` (8). These hold the mirror
    encodings and the chain from CNF facts to `Mir.MirrorExclusionLine` (`V2L.mirrorExclusionLine_final`);
  - `ENCBLEAN` (551): encoder B and `EncB.Geo.sixfold66_of_cubes64`;
  - the review files under `SYMLEAN/review`, `MIRRORETV/review` and `LEANEXT/review`.

  Some sections mention these units in remarks (sr.tex:1040–1060, ll.tex:732–739). A reader of the title and abstract,
  however, will take "the Lean-checked results … symmetric point sets" to be complete.
- **Fix.**
  - In the abstract (or at the start of fd's Purpose paragraph), say which Lean units Stage 1 covers, name the units on
    symmetric sets that it does not cover, and say that those are left to later stages.
  - Consider dropping the definite article in the title: "Written proofs of Lean-checked results, Stage 1: …".

### F3 (major, front): works cited in the text are missing from the bibliography

- **Location.** `bibliography.tex:1–15`; the citations are at sr.tex:282, mb.tex:47 and the cake_lpr mentions listed
  below.
- **Issue.** `bibliography.tex` says it lists "the works that the sections cite inline (entries as in the project's paper
  P1 where it has them)". Three cited works are missing, all of which P1 has:
  - **Dumitru's preprint.** "An earlier computation reported by B. C. Dumitru (arXiv:2512.24061, §7), which has
    priority" (sr.tex:282). P1 entry: `Dum25`.
  - **M. Schroeder's archive.** mb.tex:47 cites "the strategy of M. Schroeder's archive" and lists "six files adapted
    from that archive (MIT licence)". The document gives neither a title nor a DOI, so the source of six adapted Lean
    files cannot be identified from it. P1 entry: `Sch26` ("Erdős–Szekeres: upper bounds for convex heptagons and
    octagons", archive version 1, 19 September 2026, doi:10.5281/zenodo.22842891).
  - **cake_lpr.** It is named as the only checker that the project trusts in ar.tex:728, cb.tex:1163 and 1412,
    ec.tex:111–127, lg.tex:101, ll.tex:721–737, mb.tex:1089 and sr.tex:255. The verified checker has a reference: P1
    entry `CakeLPR` (Tan, Heule and Myreen, STTT 25 (2023) 167–184).

  Recommended as well: drat-trim (P1 entry `DT`), because ec.tex:112, sr.tex:256, ar.tex:729, mb.tex:1091 and cb.tex:1161
  rest a soundness statement on a public defect of lrat-check.
- **Fix.**
  - Add `Dum25`, `Sch26` and `CakeLPR` (and optionally `DT`), copied from `WRITEUP/P1/p1.tex`.
  - In mb.tex:47, identify the archive: title and DOI, or "M. Schroeder's archive (see References)".

### F4 (major, ar): the unconditional statement is given this document's label "computer-assisted"

- **Location.** ar.tex:750–751, the last sentence of `ar:rem:classes`: "The unconditional form of Theorem 8.x is therefore
  computer-assisted, and it is not Lean-checked as a whole."
- **Issue.** fd.tex:66–75 defines "computer-assisted" for a statement *of this document* whose written proof, given here,
  reduces to a stated finite computation. The unconditional statement has no proof in this document.
  - It rests on `HalfTurn34`, `Threefold33` and `Fivefold35`, which this document only assumes.
  - The bullets just above list what those classes rest on in the records:
    - written proofs outside this document;
    - verdicts of proofs that were deleted (most parallelogram pieces and all 116,883 threefold pieces);
    - a match between classes and formulas that was "checked by reading".

  Saying "therefore computer-assisted" in the document's own voice rounds the conditional theorem up to a labelled
  result. The label is the project's own claim (`WRITEUP/SYMMETRIC.md`, §0: "Theorem A (computer-assisted)"), not one
  that this document establishes. The bullets themselves (ar.tex:723: "computer-assisted claims of the records") are
  correctly attributed.
- **Fix.** Replace the sentence with, for example:

  > "In the project the unconditional statement is claimed as computer-assisted (`WRITEUP/SYMMETRIC.md`, Theorem A),
  > with the evidence listed above. This document establishes it only as the conditional Theorem 8.x."

### F5 (major, sr): same rounding up in the status remarks of sr

- **Location.**
  - sr.tex:972–974 (`sr:rem:main`): "An unconditional statement needs the classes, … so it is computer-assisted, not
    Lean-checked as a whole".
  - sr.tex:259–295 (`sr:rem:records`): each class is labelled with the document's italic label `\emph{computer-assisted}`.
  - sr.tex:280–281: the Fivefold35 proofs "settle the class on its own".
- **Issue.** This is the same problem as F4.
  - In `sr:rem:records` the opening sentence ("None of the following is checked in this section; it follows …")
    attributes the content to the records. The italic label, however, is the typography of this document's rigor
    labels.
  - "Settles the class on its own" reads as if one certificate alone proves `Fivefold35`. The same sentence lists the
    written encoder-soundness proofs, the normal forms and the perturbation lemma as further dependencies.
- **Fix.**
  - `sr:rem:main`: "…which the project claims as computer-assisted (Remark 7.x; `WRITEUP/SYMMETRIC.md`, Theorem A); in this
    document the theorem is established only as the stated implication."
  - `sr:rem:records`: write "claimed in the records as computer-assisted", without italics.
  - sr.tex:281: "each of which would suffice for the class without the other, given the written proofs listed next".

### F6 (minor, sr): Dumitru's initials

- **Location.** sr.tex:282: "B. C. Dumitru".
- **Issue.** The records say that the middle initial was never verified:
  - `LIT/RELATED.md:237`: "author Bogdan Dumitru per the arXiv metadata; the middle initial used earlier was not
    verified";
  - `NOVELTY20261106/README.md:132` lists the correction to "B. Dumitru";
  - P1 (`Dum25`) and `WRITEUP/SYMMETRIC.md:40` write "B. Dumitru".

  Earlier reviews accepted the form in `SYM5/README.md`, which predates the correction.
- **Fix.** Write "B. Dumitru".

### F7 (minor, fd): the label "computer-assisted" is used in two senses

- **Location.**
  - The definition: fd.tex:66–75, and `fd:rem:pos-triples`(ii) at fd.tex:1052–1054.
  - Following fd: sa.tex:107–111.
  - Not following fd:
    - pc.tex:769 (head of `pc:thm:word`), whose proof is a "Written proof (by hand)", pc.tex:796;
    - pc.tex:23 and pc.tex:998;
    - ec.tex:776 (head of `ec:prop:ex341`): "The computation is small enough to do by hand, as follows";
    - cb.tex:769–807 and cb.tex:1299–1300 (Facts `refl-h3` to `roots-match` and Theorem `c2-refl`): "Computer-assisted in
      Lean, by kernel evaluation; written proof in …".
- **Issue.** By fd's rule, a statement is not computer-assisted when the written proof does not need the machine
  computation, whatever Lean's proof does; sa applies this rule. pc, ec and cb instead label statements computer-assisted
  because Lean proves them by evaluation, although a complete hand proof is given. This is not an overclaim. It does make
  the rigor vocabulary inconsistent, and the abstract's "marked as computer-assisted" then has two meanings.
- **Fix.** Either:
  - add to fd's definition a qualified label "computer-assisted in Lean" (the Lean proof is a kernel evaluation; the
    written proof here does not use it), and use exactly that wording in the heads of `pc:thm:word` and `ec:prop:ex341`
    and in their map notes; or
  - drop the label from these statements.

### F8 (minor, fd): which statements the label "Lean-checked" covers

- **Location.**
  - fd.tex:77–79: "A statement, or a part of a statement, whose head names a declaration … is Lean-checked".
  - oc.tex:97–98: "(for a definition: it is part of the compiled file)".
  - pc.tex:63–64: "Every definition, lemma, … whose head … carries a Lean reference is Lean-checked".
  - ll.tex:49–50: "being definitions, they are not Lean-checked claims".
  - lg.tex:76: definitions only "restate".
- **Issue.** Sections disagree on whether a definition whose head names a declaration is Lean-checked. fd's rule, read
  literally, says that it is.
- **Fix.** Say in fd how the label applies to definitions (for example, "for a definition the label records only that
  Lean accepted it; a definition asserts nothing"), and align ll, lg, oc and pc with it.

### F9 (minor, fd): substitute evidence for "Lean-checked" is not codified

- **Location.**
  - fd.tex:57–63: the evidence is "the saved output of `#print axioms`"; otherwise "the section says so and names the
    evidence used instead".
- **Issue.** The sections use several kinds of substitute evidence:
  - a build or compile log plus a text search:
    - fd.tex:185–197, for fd's own main-library declarations;
    - sr.tex:54–67;
    - oc.tex:84–87;
    - ec.tex:57–60;
  - `#guard_msgs` pins: pc.tex:85–86 and 834–840;
  - report statements plus builds: pc.tex:93–101;
  - for C2FINAL, only a README sentence: cb.tex:76–79. No Lean output of any kind is committed there; I confirmed this
    by searching the records.

  Each substitute is named, so the rule is formally met. But the document never defines a "compile log plus source scan"
  rule. The weakest case (C2FINAL) carries the same unqualified label as the others in the heads of `cb:thm:c2-refl`,
  `cb:fact:c2-sub` and `cb:thm:c2`.
- **Fix.**
  - In fd, list the accepted substitutes: a compile or build log with no error and no `sorry` warning, plus a text search
    of the file and its project imports for `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by` and `extern`;
    or a `#guard_msgs` pin compiled in a logged build.
  - Say that a declaration whose only evidence is a record's statement is "Lean-checked according to the record".
  - Use that wording for the three C2FINAL theorems.

### F10 (minor, ll): a fourth rigor label appears in the document's voice

- **Location.** ll.tex:726: "These unsatisfiability results have the rigor label *certificate*". The same phrase is in the
  `ll:rem:hyp` note of `sections/ll.map.tsv` and therefore in the appendix.
- **Issue.** fd.tex:49 says "We use exactly three labels", and fd.tex:81–82 says that no other words of this kind are
  used. "Certificate" is the project's label (`WRITEUP/note/symmetric_extremal.tex:108–114`).
- **Fix.** "…which the project's records label 'certificate' (cake_lpr acceptance of an LRAT proof; `WRITEUP/note/
  symmetric_extremal.tex`, lines 108–114), a label this document does not use". Make the same change in the map note.

### F11 (minor, sr): Coverage paragraphs list conditional theorems without saying so

- **Location.**
  - sr.tex:1117–1119;
  - ar.tex:787–789, and the transfer theorem in the same list;
  - ec.tex:877–881;
  - mm.tex coverage: `mirror_odd_general`, `mirror_even_general` and their `_line` versions.
- **Issue.** ll.tex:789–790 ("conditional on `Sixfold66`") and mb's coverage ("Theorem 10.x, conditional") mark their
  conditional theorems. Four other coverage paragraphs list theirs bare. The statements and the section intros are
  correct, so this is consistency only.
- **Fix.** Append "(conditional on …)" to each conditional theorem in these four coverage paragraphs.

### F12 (minor, ec): records' "refereed" reported without saying the review was internal

- **Location.** ec.tex:121 ("recorded there as a complete written proof, refereed, not Lean-checked") and ec.tex:129
  ("recorded in `C4CUT/README.md` as a written proof, refereed").
- **Issue.** The refereeing was a review inside the project, done on the same day:
  - `C2ENC/perturbation.md:3–5`;
  - `C2ENC/referee/NOTES.md`;
  - `C4CUT/README.md:16`.

  Next to this document's own "(not refereed)", the bare word "refereed" can be read as peer review. ar.tex:734 already
  says "reviewed or audited within the project".
- **Fix.** "…refereed within the project (`C2ENC/referee/NOTES.md`)", and likewise for C4CUT.

### F13 (minor, sr): a "Lean-checked" claim without named evidence

- **Location.** sr.tex:1013–1018 (`sr:rem:variant`): "`VariantChecks.group_form` … is Lean-checked".
- **Issue.** No log is named. The evidence exists: `SYMLEAN/logs/VariantChecks.out` prints
  `group_form depends on axioms: [propext, Classical.choice, Quot.sound]`, and `SYMLEAN/logs/runs.tsv` (row
  `review/VariantChecks.lean`) records exit 0.
- **Fix.** Cite these two records.

### F14 (minor, mm): "Theorem A" in the section title clashes with the project's main theorem

- **Location.** mm.tex:1 (section title, and so the table of contents): "The mirror lemma and Theorem A".
- **Issue.** In `WRITEUP/SYMMETRIC.md:17`, "Theorem A (computer-assisted)" is the project's main symmetric k = 7 theorem.
  This document proves that theorem only conditionally (`sr:thm:main`, `mb:thm:main3`). Here, "Theorem A" is
  `MIRRORETV/README.md`'s mirror reduction. A reader of the table of contents may take the title as a claim about the
  main theorem. The section intro (mm.tex:8–9) does qualify the name.
- **Fix.** Use "Theorem A of MIRRORETV" in the title, or "the mirror reduction (Theorem A of MIRRORETV)". The title comes
  from CONTRACT.md, so the contract table needs the same edit.

### F15 (minor, front): the appendix introduction does not fit all rows

- **Location.** `tools/make_appendix.py:98–102`, which generates the intro paragraph, and line 129.
- **Issue.**
  1. **Paths.** "Paths that begin with ErdosSzekeres/ are relative to the repository root; all other paths are relative
     to cloud/es7-2026-10-19/results". The note of `fd:rem:pos-cycle` cites `docs/SAT.md`, which exists only at the
     repository root; there is no `docs/` in the results directory. fd's own convention (fd.tex:20–23) also makes
     `docs/`, `experiments/` and `scripts/` root-relative.
  2. **Remark rows.** "the Lean declarations it restates" does not fit them. Four fd remark rows list declarations that
     the remark only discusses: `fd:rem:orient-lean`, `fd:rem:affine-orient-lean`, `fd:rem:affine-cp-lean` and
     `fd:rem:pos-cycle`. By the "Statement map" intro, readers may take these rows as Lean-checked statements.
  3. **"Written step".** Every row without a Lean name prints "written step", including remarks. For example,
     `sa:rem:control` is about an anonymous Lean `example`, accepted by Lean, at
     `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean:30`. `fd:def:conv` restates Mathlib definitions.
- **Fix.**
  - Use fd's path sentence.
  - Add: "For a remark, the Lean column names the declarations it discusses; remarks are commentary and carry no rigor
    label."
  - For remark rows without a Lean name, print "remark" or "--" instead of "written step".

### F16 (minor, front): the generator's undefined-label guard omits section sa

- **Location.** `tools/make_appendix.py:55`: `re.match(r'^(fd|ll|lg|oc|pc|ec|sr|ar|mm|mb|cb):', …)`.
- **Issue.** The key list predates sa. A mistyped `sa:` label in a note would be set as plain text instead of stopping
  the generator. All current `sa:` references resolve, so the output is unaffected today.
- **Fix.** Build the pattern from `KEYS`: `'^(' + '|'.join(KEYS) + '):'`.

### F17 (minor, front): a path in an appendix note runs into the margin

- **Location.** `appendix_map.tex:204`, row of `pc:rem:word-scope`; PDF page 167; `build/doc-r1/proofs.log:4038`
  (overfull \hbox, 49.4 pt).
- **Issue.** The token `ENCBLEAN/logs/m8_fix_build.log:29,35,` contains a comma inside the core, so `IDENT` does not match
  it. It is then set in roman type with no break points and visibly extends past the right margin. It is the only
  overfull box of the build.
- **Fix.** Either:
  - write "…`m8_fix_build.log:29` and `:35`" in `sections/pc.map.tsv`; or
  - allow `,` followed by digits inside the `IDENT` core.

### F18 (minor, front): one entry differs from P1, and the entries are not linked to the text

- **Location.** `bibliography.tex:13–14` (`SMQH25`) and the header comment of the same file.
- **Issue.**
  - The comment says entries are "as in the project's paper P1 where it has them". P1's `SMQH25` also gives the
    published version: CICM 2025, LNCS 16136, Springer, 29–47, doi:10.1007/978-3-032-07021-0_3.
  - Separately, no section uses `\cite`. Lean 4 and Mathlib, for example, are named in fd.tex:6 but not tied to the
    entries `Lean4` and `Mathlib`.
- **Fix.**
  - Copy P1's `SMQH25` entry.
  - Optionally, tie first mentions to the entries. If `\cite` is used, the standalone compile rule of CONTRACT.md would
    have to tolerate undefined citations.

### F19 (minor, front): empty PDF metadata

- **Location.** `proofs.tex`.
- **Issue.** `pdfinfo build/doc-r1/proofs.pdf` shows empty Title and Author fields.
- **Fix.** After `\input{preamble}`, add `\hypersetup{pdftitle={Written proofs of the Lean-checked results, Stage 1:
  symmetric point sets}}`.

## Not findings (checked and correct)

- **Fidelity of the map.** All 677 Lean (name, file:line) pairs of the maps are correct at commit 7e32ee259, including
  namespaces. The 42-row manual sample agrees with the statements.
- **Conditional theorems in statements and intros.** Every theorem with a hypothesis (Sixfold66, Sevenfold70,
  Fivefold35, Fourfold32, the five classes, (hM), hE, MirrorExclusionLineCopy, Hcap/HL/HR) says so in its statement and
  in its section intro. Every map note says "takes hypotheses". `mb:thm:main3` says "does not establish its conclusion
  unconditionally".
- **SAT verdicts and checkers.** SAT verdicts are anchored on cake_lpr in ec, ll, lg, mb, sr, ar and cb. lrat-check is
  called secondary and not counted, with `LRATCHECK20261105` and `WRITEUP/SYMMETRIC.md` §3 cited.
- **Earlier priority.** The text gives earlier priority correctly:
  - Dumitru for the fivefold case;
  - Subercaseaux–Mackey–Qian–Heule (§6.2) for the fourfold case;
  - Baek and Erdős–Szekeres as cited theorems.
- **Wording of rigor.** No "verified" or "certified" is applied to a result of this document. cb's "certified" refers
  only to the project's record status, and says so.
