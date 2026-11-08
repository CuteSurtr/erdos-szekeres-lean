# Re-check of section fd after the whole-document review, round 1

Inputs:
- `reviews/docfix-fd-r1-fix.md` (the fixer's log);
- `snapshots/docfix-r1-pre/fd.tex` and `fd.map.tsv` (before) and `sections/fd.tex` and `sections/fd.map.tsv` (after);
- the Lean sources and records of the repository at 7e32ee259;
- the current files of pc, ec, cb, sa, ll, lg, oc, sr and ar, read for the cross-section points.

Paths below are relative to STAGE (sections, build, reviews), to RES (records and research Lean files), or to the
repository root (`ErdosSzekeres/`, `docs/`). No git command was run. The two statements about git history are
discussed under hunk H9.

**Verdict: pass.** The fixer addressed all eleven findings and declined one detail of finding 9. All eleven are
resolved in fd, and the decline is right. The edits introduce no blocker or major problem.

The major finding (2) is resolved: fd's definition of "computer-assisted" now classifies every current use in pc, ec,
cb and sa consistently. Four minor follow-ups remain (N1–N4 in section 4). Three of them are in other sections
(pc/ec heads, cb's C2FINAL label, ec's ρ^j), because those sections were fixed before fd's new rule existed. The
fourth is an optional completeness note on fd's evidence rule (a).

## 1. The eleven findings

| # | finding | fixer | re-check | evidence |
|---|---|---|---|---|
| 1 | xref-fdlllg, minor: "Notation shared by all sections" is inaccurate; R clash | fixed | **resolved** | The paragraph is now "Default notation" (fd.tex:131-146). It says that in fd, R_θ always denotes the rotation matrix of Lemma fd:lem:rot, not a map. That is true: every R_θ in fd (fd.tex:474-526, 617, 637-638) is the matrix. It also says that a later section may use other symbols and defines them. Its examples cover oc's R_{c,θ}/M_θ (oc.tex:140-144), sr's rotAbout_{c,θ} (sr.tex:189) and lg's rotAbout(c,θ). |
| 2 | consistency, **major**: one label, two incompatible rules | fixed (preferred fix) | **resolved** | The new rule (fd.tex:81-105) is CONTRACT rule 6. A statement is computer-assisted if its Lean proof, or that of one of its parts, is itself a finite computation, or if its written proof uses a machine computation not done by hand. It is "computer-assisted in Lean" if a complete hand proof is also given. `decide` used only for side facts inside a proof of a statement that is not a finite computation does not count. The Purpose (fd.tex:10-13) now says "need not be carried out by hand". Checked against the current texts. pc:thm:word: `decide` decides the whole statement over 64 words, and an 8-word hand proof is given. ec:prop:ex341: closed numerals, `decide`, and a hand computation at ec.tex:789-797. Both are computer-assisted in Lean. cb's Facts refl-h3 … roots-match and cb:thm:c2-refl already say "Computer-assisted in Lean, by kernel evaluation; written proof in …" (cb.tex:772-810, 1304), and cb.tex:83-91 states the same rule. sa:lem:split, sa:thm:baek-seven and the control use `decide` only for closed instances s = 2..6, for C(6,2)+2 = 17 and for 32 ≤ 32, inside universally quantified statements, and check these by hand (sa.tex:104-115, 215-223; map notes). By fd's sentence on side facts, which names "closed instances that the written proof checks by hand", they are not computer-assisted. So the appendix rows ec:prop:ex341 and sa:thm:baek-seven now follow one rule. Residual: two heads still carry the bare umbrella label (N1, minor; pc and ec). |
| 3 | consistency, minor: what "Lean-checked" means for a definition | fixed in fd | **resolved** | fd.tex:107-111: "For a definition this records only that Lean accepted the definition: a definition asserts nothing, and what this document claims for it is that the written definition restates the Lean definition." The current wordings are all compatible with this sentence: ll.tex:55-56 ("restate Lean definitions …; being definitions, they are not Lean-checked claims"), oc.tex:97, pc.tex:63-64 (the label applies to every statement with a Lean reference) and lg.tex:79-80 ("restates that Lean definition"). They differ in words but no longer conflict. |
| 4 | consistency, minor: a∸b not in fd's convention | fixed | **resolved** | fd.tex:122-124 adds "or as a∸b = max(a−b,0) where a section defines this symbol". ll typesets the same glyph (`\mathbin{\dot{-}}`, ll.tex:113) and defines it there. The glyph renders correctly (checked on page 2 at 150 dpi). |
| 5 | consistency, minor: f^[n] and ρ_{c,θ} announced as shared | fixed | **resolved** | Same change as finding 1. The new pointer is correct. Lean's `Nat.iterate` recursion is f^[n+1] = f^[n]∘f, and the proof of fd:lem:inv-image(c) (fd.tex:442-446) derives f^[i+1] = f∘f^[i] by induction, so both recursions define the same maps. ll, lg, oc, sr and ar define their iterate and rotation symbols (ll.tex:74, lg.tex:151-152, oc.tex:140-144, sr.tex:189, ar.tex:102-103). ec does not define its ρ^j (N4, minor). |
| 6 | consistency, minor: MirrorMain.lean:2520 reads as a declaration line | fixed | **resolved** | fd.tex:301-309 now says "used at MIRRORETV/lean/MirrorMain.lean:2520, in the proof of MirrorOdd.mirror_odd_general (declared at …:2498)". Likewise "used at ReductionThreeClasses.lean:4079, … declared at :4057". Both are correct: each line contains `hasConvexNGon_of_le`, and the nearest preceding declaration is `theorem mirror_odd_general` at 2498 and 4057. The fixer applied the same convention to the whole paragraph. I checked all 20 "used at" lines and the "declared at" lines (Number.lean:40, BoundaryGeometry.lean:30). Every line contains the named declaration, and every one lies inside the proof named (nearest preceding declaration). Three uses are dot notation. At Construction.lean:118, `h.mono` has `h : ForcesConvexNGon N n`. At Basic.lean:45, `hgp.mono` has `hgp : GeneralPosition s`, and `(h t …).mono` is applied to a `HasConvexNGon n t`. So these resolve to ForcesConvexNGon.mono, GeneralPosition.mono and HasConvexNGon.mono. The map note of fd:lem:mono cites :2498. |
| 7 | claims, minor: two senses of computer-assisted; define "computer-assisted in Lean" | fixed in fd | **resolved** | The qualified label is defined at fd.tex:92-96 and announced at fd.tex:51 and 10-13. Remark fd:rem:pos-triples (ii) and two map notes give the side-fact reason. Using the wording in the pc and ec heads is left to those sections (N1). |
| 8 | claims, minor: definitions with Lean heads | fixed in fd | **resolved** | Same change as finding 3. |
| 9 | claims, minor: substitute evidence not codified; C2FINAL | fixed; implemented_by/extern declined | **resolved; decline right** | See the details after this table. |
| 10 | typesetting, minor: sources table leaves a quarter page blank | fixed | **resolved** | The table is now a `longtable`; longtable and booktabs are loaded by the preamble. In my standalone build the table is complete on p3. In my own full build of proofs.tex (three passes, exit 0), p4 is full and the table is complete on p5 with no gap (rendered and inspected). |
| 11 | typesetting, minor: loose Axioms-evidence and Coverage runs | fixed | **resolved** | Both runs are now itemized lists inside `{\raggedright … \par}` (fd.tex:186-314, 1218-1324). My standalone log has no underfull hbox in either range. All remaining badness-10000 hboxes are in statement heads, which is a preamble matter. The underfull vbox warnings fall on standalone pp. 1, 2, 4 and 17 and on full-build pp. 4 and 6. Rendered, these pages are full with no visible gap. |

**Finding 9 in detail.** The Lean-checked bullet (fd.tex:59-78) now lists two substitutes for saved axiom output and
one qualified label:
- (a) evidence that the current file compiled with exit status 0, together with a text search of the file and its
  imported project files;
- (b) a `#guard_msgs` pin of `#print axioms` in a logged build;
- "Lean-checked according to the record" when only a record's statement exists.

fd's own uses of kind (a) are sound:
- `docs/VALIDATION.md:73` is the 11 October 2026 `--wfail` build line, in the same record section as the audit.
- The audit prints theorems of OrientationClique.lean (line 119) and Reflection.lean (lines 175, 176).
- `HasConvexNGon.card_le`, `Suk.convexPosition_of_negative_triples` and `reflectY_x/_y/_reflectY` are not printed
  (checked).
- The main-library import closure of Basic.lean, OrientationClique.lean and Reflection.lean is exactly the nine table
  files, BaseOrder, BaseChart, TriangleOrder, CupsCaps and the four Vendor files that fd.tex:252-254 names.

I ran the text search over these 17 files and the six research files. It finds only the comment "not declared as a
theorem or an axiom" (Definitions.lean:30) and the word "admits" (BaseOrder.lean:17). There is no `implemented_by`,
`extern`, `+native`, `ofReduceBool`, `ofReduceNat` or `skipKernelTC`. So fd.tex:255-256 and 310-312 are true. The
research files import only main-library files that this search covers, so rule (a) also holds for the definitions
fd cites from SymmetricReduction.lean and OrbitConsistency.lean.

The decline is correct. `implemented_by` and `extern` change only compiled code, and the kernel sees compiled code
only through `Lean.ofReduceBool` and `Lean.ofReduceNat`. A search of every .lean file of the repository finds the two
attributes only in comments (ENCBLEAN). Two items remain: cb does not yet use the new qualified label (N2), and
rule (a) has an optional completeness gap (N3).

## 2. Each hunk checked as a referee

`diff -u` gives 11 hunks for fd.tex and 1 hunk (5 rows) for fd.map.tsv. The label lists before and after are
identical. The map still has one row per statement environment: 40 rows, with the same labels and kinds in the same
order (checked by script). Only one statement environment changed, Remark fd:rem:pos-triples.

- **H1, Purpose (fd.tex:10-13).** It is consistent with the rule at fd.tex:81-105. Statements that are
  "computer-assisted in Lean" do get a hand proof, and the sentence says so. It rounds no label up.
- **H2, "exactly three labels" (fd.tex:51).** The qualified forms belong to the first label ("Lean-checked according
  to the record") and to the third ("computer-assisted in Lean"). Both are defined below. Correct.
- **H3, Lean-checked bullet (fd.tex:59-78).** It is sound as a standard of evidence. A sorry gives only a warning and
  exit status 0, so the text search (or `--wfail`) is what excludes it. That clause is right. A record-only label is
  qualified, never rounded up. The only optional point is N3.
- **H4, Computer-assisted bullet (fd.tex:81-105).**
  - The mathematics and the description of Lean are correct: `decide` and `decide +kernel` add no axiom; the
    native_decide sentence is unchanged from the snapshot.
  - The SAT sentence matches its sources. LRATCHECK20261105/README.md says that cake_lpr "also exits 0, so only its
    line `s VERIFIED UNSAT` counts" and that a statement accepted only by lrat-check "is not certified".
    WRITEUP/SYMMETRIC.md §3 ("Trust base") says: "Only cake_lpr … is trusted, and a verdict counts only if it prints
    the line `s VERIFIED UNSAT`" and "lrat-check … is a secondary check only and not part of the trust base". Both
    files exist at the cited RES-relative paths.
  - Record results are presented as claims of the records, and theorems that assume them as conditional. This agrees
    with CONTRACT rule 7.
- **H5, definitions (fd.tex:107-111).** Correct (see finding 3).
- **H6, arithmetic (fd.tex:122-127).** Correct: Lean's `Nat.iterate` is f^[n+1] = f^[n]∘f, and the pointer is
  correct (finding 5).
- **H7, Default notation (fd.tex:131-146).** True (finding 1). The descriptive claim that every other section defines
  its symbols has one exception (N4).
- **H8, table (fd.tex:156-184).** The rows are unchanged. The longtable syntax is sound: first head, repeated head and
  a foot used on every page. "The table of sources" is the name used later in the section.
- **H9, Axioms evidence (fd.tex:186-314).**
  - The new opening conventions are kept: every bare "line N" refers to the log, audit or report named last before it.
  - Every cited line was re-checked:
    - audit lines 49, 87, 88, 103, 113, 114, 119, 132, 175, 176, 178, 529, 624, 720, 725 and 732, each with the
      three standard axioms;
    - MirrorMain.out:858 and SYMLEAN/mirror/axioms.out:11 (both `MirrorOdd.mirror_odd_general`; MirrorMain.out
      contains no "error");
    - LEANEXT/review/axioms.log lines 1, 22, 23, 26 and 33 (line 1 has propext and Quot.sound only);
    - SYMLEAN/logs/runs.tsv lines 2, 4 and 5 (exit 0, output lines 0, 0 and 27);
    - AffineReductionAxioms.out lines 9-11, 13-15 and 16;
    - LEANEXT/orbit/logs/axioms.log lines 1 and 5, and LEANEXT/orbit/REPORT.md line 3 (429 lines, 9b843180).
  - All "used at" lines were checked (finding 6).
  - New claim: LAYERLEAN/logs/build.log "names no file hash". This is true (3 lines: command, exit code 0, messages
    0).
  - The other new claims rest on git history, which I did not re-run:
    - The statement that build.log was "committed with the first, 454-line version of the file and has not been
      updated since" was established with read-only git by the fixer and independently by three reviews:
      doc-r1-consistency M3, docfix-ll-r1-recheck and docfix-lg-r1-recheck. All three give commit 6429e9a70, 454
      lines and SHA-256 804b1d25f79a.
    - The unchanged statement "unchanged since 7f0868fdb" was re-checked by the fixer with read-only git.
  - The current LayerLemma.lean has 1148 lines and SHA-256 afb8542dceb0, as the paragraph and table state.
- **H10, Remark fd:rem:pos-triples (ii) (fd.tex:1118-1124).** This is faithful to the Lean proof
  (ErdosSzekeres/Suk/OrientationClique.lean:9-29). `decide` closes only `Finset.univ = {0,1,2,3}` in Fin 4 and the
  order facts passed to `e.strictMono`. The statement quantifies over arbitrary ι, p and s, so it is not a finite
  computation. "Not computer-assisted" follows fd's rule.
- **H11, Coverage (fd.tex:1218-1324).** A word-level comparison with markup removed shows only the three new item
  headings and one moved "and". The coverage content is unchanged.
- **Map hunk.** The five notes are accurate: :2498 is the declaration line; card_le, negative_triples and the reflectY
  lemmas are not printed in the audit; and the side-fact wording matches H10. I ran `tools/make_appendix.py` on a copy
  (build/fd_recheck_r1_apptest): 470 rows, and the new notes typeset correctly (it turns "(fd:sec)" into
  "Section~\ref{fd:sec}"). The real appendix_map.tex was not touched.
- **Hard rules.**
  - fd.tex and fd.map.tsv contain no machine path and no tool name.
  - There is no `\newcommand`, `\def`, `\usepackage` or other new macro or package.
  - No `\lean{…}` or `\dirn{…}` argument contains a space.
  - Every `\ref` points to an fd label or to an export label of another section: ll:def:hv, ll:def:peel, ll:def:66-70,
    mb:thm:baek, oc:lem:perm and oc:lem:rot-inv.
  - "Verified", "certified" and "proved" occur only in the quoted checker line `s VERIFIED UNSAT`, in "not proved in
    Lean" and in the unchanged meta-sentences.

## 3. Compile

- **Standalone wrapper.** `build/fd_recheck_r1_wrapper.tex` (the contract wrapper) was run twice from `build/` with
  `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
  - Both passes exit 0, with no errors and 0 overfull boxes. The PDF has 18 pages.
  - The only undefined references are the six export labels listed above.
  - There are no longtable or rerun warnings.
- **Full document.** `proofs.tex` was built with `-output-directory build/fd_recheck_r1_full`, so nothing was written
  to STAGE.
  - Three passes, all exit 0. The PDF has 192 pages.
  - fd's part of the log has no overfull box. The only overfull box (49.4pt) is in the stale generated appendix,
    another section's row, and is not fd's.

## 4. Remaining minor points

- **N1 (minor; pc.tex:769, 998; ec.tex:784; map notes of pc:thm:word and ec:prop:ex341).** fd now prescribes "computer-assisted in Lean" when the Lean proof is a finite
  computation and a complete hand proof is given (fd.tex:92-96). pc:thm:word and ec:prop:ex341 are of that kind, but
  their heads carry the bare "computer-assisted". pc's own intro, pc.tex:23-24, already says "computer-assisted in
  Lean". This understates and does not overclaim. Fix: write "computer-assisted in Lean; written proof by hand" in
  both heads, at pc.tex:998, and in the two map notes.
- **N2 (minor; cb.tex:78-81 and the heads at cb.tex:1303, 1359, 1374).** fd.tex:76-78 now requires "Lean-checked
  according to the record" when no Lean output is saved and the label rests only on a record. The three C2FINAL
  theorems are exactly this case: no compile or axioms log is committed, and C2FINAL/README.md §6 is the only basis.
  cb discloses this at cb.tex:81 but uses the unqualified label. Fix: use the qualified label at cb.tex:81 and in the
  heads or map notes of cb:thm:c2-refl, cb:fact:c2-sub and cb:thm:c2.
- **N3 (minor, optional; fd.tex:69-72).** Rule (a)'s search list names `native_decide` but not the other ways to
  reach the same axioms: `decide +native` and a direct `Lean.ofReduceBool`/`Lean.ofReduceNat`. It also omits
  `debug.skipKernelTC`, which skips the kernel check. No Lean file of the repository uses any of these outside
  comments, and fd's own searches cover them, so no label is affected. Fix: add `+native`, `ofReduceBool` and
  `skipKernelTC` to the list.
- **N4 (minor; fd.tex:142-146 vs ec.tex:171, 250-251, 263, 401-403).** fd says that a section writing iterates
  differently defines its symbols where it introduces them. ec writes ρ^j and rotAbout(c,2π/m)^{m/2} for iterates, in
  remarks, without a defining clause. Every other section defines its symbols. The power notation is unambiguous.
  Fix: ec adds "ρ^j, the j-fold composite of ρ", or fd exempts the usual power notation for iterates.
