# doc-r1, lens "consistency" (whole document)

Build reviewed: `build/doc-r1/` (proofs.pdf, proofs.log, proofs.txt, proofs.toc). Sources: `sections/{fd,ll,lg,oc,pc,ec,sr,ar,mm,mb,cb,sa}.tex`,
their `.map.tsv`, `appendix_map.tex`, `bibliography.tex`, `proofs.tex`. Records were read (read-only) in the repository
checkout at commit 7e32ee259 to settle factual questions; no build or solver was run.

## Method

1. Read all twelve section files (fd, ll, lg, oc, pc, ec, sa in full; sr, ar, mm, mb, cb in full apart from routine
   proof passages that restate no shared convention or record fact).
2. Shared conventions of fd checked in every section: orient formula and sign, rotAbout formula and direction,
   Invariant (maps into), hv/peel (indexing from 0), HasConvexNGon (no emptiness), general position via collinearity,
   natural subtraction, iterates, division by zero.
3. Lean declarations restated in more than one section: found by Lean name across the `*.map.tsv` files (44 names,
   in fd/ll/lg/oc, fd/ar, fd/sr, fd/mm, sr/mb, mm/mb, lg/pc). Each pair of statements compared (hypotheses,
   conclusion, line numbers). Copy blocks compared against the files with `diff`/`sed`: Merged.lean 1-1147 =
   LayerLemma.lean 1-1147; AffineReduction.lean 1-1058 = SymmetricReduction.lean 1-1058; RTC 38-1559 =
   AffineReduction.lean 12-1533; RTC 1562-4236 = MirrorMain.lean 3-2677; 19 definitions of rotAbout in the records.
4. Record facts compared across sections: supply of Sixfold66/Sevenfold70 (C6UPPER, C7UPPER, ENCBLEAN, k8 note
   G1-G4, E1-E6; checked against `WRITEUP/note/k8_soundness.tex` and `C6UPPER/README.md`), supply of each case class
   (sr, ar, mb, ec, sa; checked against `WRITEUP/SYMMETRIC.md` section 3), counts (64/32 cubes, 910 roots, 116,883
   pieces, 2,120 re-solves, 204 sigma-cube pieces, 120 hexagonal hulls, 73,567 leaves, 1,198+1+121+74,000 facts),
   cake_lpr/lrat-check trust statement, Lean 4.24.0 / Mathlib f897ebcf / commit 7e32ee259, axioms logs (counts
   28 / 19 / 59 verified against the logs), SHA-256 prefixes cited for the same file in several sections (all agree).
5. Rigor vocabulary tallied per section; every statement-head tag and map note with "computer-assisted",
   "written step", "conditional", "certificate", "refereed", "certified" compared.
6. TOC (`proofs.toc`, rendered TOC in proofs.txt), section titles, numbering, ref words vs environments (script:
   every "Lemma/Theorem/... \ref" matches the environment of its label), undefined references (none in proofs.log).

## Summary

3 major, 21 minor. No blocker. The shared geometric conventions (orient, rotAbout, Invariant, hv/peel, HasConvexNGon,
general position, division by zero), all duplicated Lean statements, all copy-block descriptions, the counts, the
versions/commit and the cake_lpr trust statement are consistent across sections. The major problems are in the rigor
vocabulary (the label "computer-assisted" is defined one way in fd and applied another way in pc, ec and cb, while sa
applies fd's definition; ll introduces a fourth label "certificate") and in one record description (ll relies on a
build log that fd excludes and that belongs to an older version of the file).

## Major findings

### M1 [fd] "computer-assisted" is defined in fd in a way that pc, ec and cb contradict and sa follows
- fd.tex:10-12 (Purpose: a computer-assisted statement is reduced to a computation "not carried out by hand") and
  fd.tex:65-75 (definition: "a statement whose written proof relies on a finite computation that is carried out by a
  machine and not by hand ... A Lean proof that uses decide only for facts that ... the written proof establishes by
  hand ... does not make a statement computer-assisted").
- Contradicting uses: pc:thm:word (pc.tex:23-24, 769, 998; "computer-assisted in Lean, with a written proof by hand
  here"), ec:prop:ex341 (ec.tex:776-788; head "computer-assisted", proof "small enough to do by hand"), cb Facts
  cb:fact:refl-h3, refl-h6, topcases, strata, roots-match and cb:thm:c2-refl (cb.tex:81-89, 770-808, 1300; "Computer-
  assisted in Lean, by kernel evaluation; written proof in ..."). By fd's text none of these is computer-assisted.
- Following fd: sa.tex:104-111 declares sa:lem:split, sa:thm:baek-seven and the control not computer-assisted
  "by the convention that accompanies the rigor labels", because decide is used "on closed numerical facts that the
  written proofs check by hand" -- exactly the situation of ec:prop:ex341.
- Visible in the appendix: ec:prop:ex341 "computer-assisted ...; arithmetic also done by hand" vs sa:thm:baek-seven
  "decide in Lean, checked by hand; not computer-assisted".
- Fix (preferred, matches CONTRACT rule 6 and the majority use): rewrite the definition in fd: a Lean theorem whose
  Lean proof is itself a finite computation (the whole statement decided by decide / decide +kernel / native_decide,
  or replayed from generated data or certificates) is labelled computer-assisted, also when this document gives a
  hand proof as well (then say "computer-assisted in Lean; written proof by hand", the phrase cb and pc already use);
  decide used only for side facts inside a proof of a statement that is not itself a finite computation (0<1 in
  Fin 4; the five closed instances of A1.order_split; C(6,2)+2=17 in baek_seven) does not make the statement
  computer-assisted. Change the Purpose sentence to "need not be carried out by hand". Then align ec:prop:ex341's head
  with the cb/pc phrase and reword sa's rationale (see m1). (Alternative: keep fd and drop the label from pc:thm:word,
  ec:prop:ex341 and the six cb statements; then cb.tex:81-89 must change too.)

### M2 [ll] ll introduces a fourth rigor label, "certificate"
- ll.tex:725-726 "These unsatisfiability results have the rigor label \emph{certificate}"; ll.map.tsv row ll:rem:hyp
  ("rigor label certificate"), reproduced in appendix_map.tex:94.
- fd.tex:49 "We use exactly three labels"; fd.tex:65-71 puts SAT certificates checked outside Lean under
  "computer-assisted". sr (Remark sr:rem:records), ar (ar:rem:classes), mb (mb:rem:main3) and ec (ec:rem:cases) label
  the same kind of evidence (UNSAT verdicts of cake_lpr) "computer-assisted".
- Fix: "These unsatisfiability results are computer-assisted (cake_lpr verdicts, checked outside Lean)"; the same in
  ll.map.tsv; regenerate the appendix.

### M3 [ll] ll cites LAYERLEAN/logs/build.log as the compile record of the current file; fd excludes that log
- ll.tex:28-30: "... by lake env lean ...; LAYERLEAN/logs/build.log records exit code 0 and no messages."
- fd.tex:204-206: "The log LAYERLEAN/logs/build.log does not name the hash of the file it was made for, and we do not
  use it." lg.tex:55-60 also notes that the log names no hash and rests on REPORT.md and the 6 November re-check.
- Record check: build.log was committed with the first version of LayerLemma.lean (commit 6429e9a70, 454 lines,
  SHA-256 prefix 804b1d25f79a) and never updated; LayerLemma.lean was changed in five later commits (last 393619a57,
  1148 lines, afb8542dceb0). So the log does not record a compile of the file ll treats.
- Fix: as fd does, say that build.log names no hash (it was committed with an earlier, 454-line version) and is not
  used; rest the compile evidence on the 6 November re-check (axioms_recheck_20261106, exit status 0 on a file whose
  first 1148 lines are this file) and on LEANEXT/review/REPORT.md. (lg's wording is compatible; see m19.)

## Minor findings

- m1 [sa] sa.tex:107-111 and the sa.map.tsv notes of sa:lem:split / sa:thm:baek-seven justify "not computer-assisted"
  by "closed numerical facts that the written proofs check by hand", which also describes ec:prop:ex341 (labelled
  computer-assisted). After M1, say instead that decide closes side facts inside proofs of statements that are not
  themselves finite computations.
- m2 [fd] fd.tex:77-80 says every statement whose head names a declaration is Lean-checked; ll.tex:49-51 says
  definitions with Lean heads "are not Lean-checked claims"; oc.tex:97-98 and pc.tex:63-64 call such definitions
  Lean-checked; lg.tex:75-76 says they "restate" the definition. Fix: fd states once how the label applies to a
  definition (Lean accepted it; it asserts nothing), and ll/oc/pc follow that wording.
- m3 [fd] fd.tex:89-91 promises natural-number differences as max(a-b,0) or with b<=a stated; ll (C7) and cb
  (Notation) use a ∸ b (defined there), ec writes "t-1 (natural subtraction)". Fix: allow "a∸b = max(a-b,0), defined
  where used" in fd's convention.
- m4 [ec] ec.tex:157-162, item (R) restates convexNGon_of_layers with "m·(t-1) ... (natural subtraction)"; ll states
  the same declaration with m·(t∸1). Fix: use ll's notation or max(t-1,0).
- m5 [fd] fd.tex:91-105 announces f^{[n]} and ρ_{c,θ} as notation "shared by all sections", but ll, lg, ar, ec write
  iterates as f^n / ρ^j (ll, lg, oc, sr, ar take f^{n+1}=f∘f^n as the defining recursion), the rotation is written
  rotAbout(c,θ) (lg, ec), R_{c,θ} (oc), rotAbout_{c,θ} (sr), the rotation matrix R_θ (fd, lg), A_θ (ll), M_θ (oc), and
  HasConvexNGon is typeset five ways. Fix: call these the default notation and say that a section using another one
  defines it (all do).
- m6 [oc] oc.tex:138-143 uses R_{c,θ} for the rotation map while fd (Lemma fd:lem:rot) and lg use R_θ for the
  rotation matrix. Fix: rename (e.g. ρ_{c,θ} as in fd) or add a sentence noting the clash.
- m7 [sr] Theorems that take the unproved case classes as hypotheses carry "conditional" in their heads in ll
  (ll:thm:sixfold/sevenfold), ar (ar:thm:main) and mb (mb:thm:main3), but not in sr (sr:thm:main, sr.tex:944;
  sr:thm:variant, sr.tex:981) or ec (ec.tex:172-221, five theorems). The statements themselves say "Assume". Fix: add
  "conditional on ..." to these heads (or drop the tag everywhere).
- m8 [ec] ec.tex:7, 97, 107, 169 call Fivefold35/Fourfold32 "case statements"; sr, ar, mb, sa call the same
  propositions (same text) "case classes". Fix: "case classes".
- m9 [ec] ec.tex:113 cites the records directory \dirn{E2} for the lrat-check defect, while ll and lg use "(E2)" for
  trust item E2 of the k8 note. Fix: cite E2/logs/lrat_check_soundness.md (or "record E2") to avoid the collision.
- m10 [ec] ec.tex:121 and 129 call C2ENC/perturbation.md and the C4CUT encoder proof "refereed" (quoting the
  records), next to this document's label "written proof (not refereed)"; ar.tex:734 describes the same proofs as
  "reviewed or audited within the project". Fix: "refereed within the project (internal review)" or ar's wording.
- m11 [pc] pc.tex:65-66, 564, 596, 1012-1013 and pc.map.tsv introduce "written observation(s)", a term not in fd's
  vocabulary; other sections call such content "written step" (sa: "Remark sa:rem:use is a written step"). Fix: use
  "written step", or define the term in fd.
- m12 [cb] cb.tex:36-37, 1154-1155, 1269 ("a record that it counts as certified", "uncertified node") use "certified",
  which fd.tex:81-82 and the binding vocabulary exclude; sr/ar/mb phrase the same status as "a recorded cake_lpr
  verdict". Fix: "a record with a recorded cake_lpr verdict (the project's term: certified)".
- m13 [mm] mm.tex:72-73 says Theorems mm:thm:odd/even "take an unproved hypothesis (hM)" and mm:rem:hm(1) calls them
  "conditional on (hM)"; (hM) is a parametric premise (free M), treated as such by ar ((hE): "a parameter ... It
  involves no unproved claim of the project", ar.tex:8-9, 611) and mb (Hcap/HL/HR, "parametric premises"). fd reserves
  "conditional" for propositions not proved in Lean such as SAT verdicts. Fix: "a parametric hypothesis (hM)".
- m14 [fd] fd.tex:237-238 writes "MirrorOdd.mirror_odd_general (MIRRORETV/lean/MirrorMain.lean:2520)"; by fd's own
  rule (fd.tex:32-35) this reads as the declaration line, but 2520 is the line where hasConvexNGon_of_le is used;
  mm and mb cite mirror_odd_general at :2498. Fix: "is used at line 2520, in the proof of mirror_odd_general (:2498)".
- m15 [sr] sr:lem:supports (sr.tex:633-647) restates ErdosSzekeres.Suk.convexPosition_of_strict_supports, which fd
  states and proves as Lemma fd:lem:strict-supports, without pointing to it (the Dependencies paragraph omits it).
  Fix: add "(also Lemma fd:lem:strict-supports)".
- m16 [ll] ll.tex:79-81 (C3) cites Rockafellar for the description of conv as convex combinations, which fd proves
  (Lemma fd:lem:hull(a),(b)) for the whole document. Fix: cite fd:lem:hull (optionally keep the textbook reference).
- m17 [lg] lg.tex:890 uses \subsection*{Coverage}: the TOC shows an unnumbered "Coverage" line between 3.6 and 4;
  oc (4.7) and cb (11.11) have numbered Coverage subsections; the other nine sections use \paragraph{Coverage.}, which
  does not appear in the TOC. Fix: \paragraph{Coverage.} in lg (and preferably in oc and cb).
- m18 [ar] ar.tex:25, 44, 81, 91, 109, 120, 127, 766 write \paragraph{\textbf{...}}: ar's paragraph heads are bold,
  all other sections' are not. Fix: drop \textbf.
- m19 [lg] lg.tex:55-56 "The log LAYERLEAN/logs/build.log records exit code 0 and no messages. That log names no file
  hash" is compatible with fd but still reads as a record of this file. Fix: add that it was committed with the first,
  454-line version (cf. M3).
- m20 [front] bibliography.tex (said to list "the works that the sections cite inline") lacks B. Dumitru,
  arXiv:2512.24061, cited inline in sr.tex:282 (P1 has it as Dum25). Fix: add the entry; use one form of the name.
- m21 [front] proofs.tex:12-14 abstract: "gives a complete proof that can be checked without Lean" omits the second
  exception of fd's Purpose paragraph (cited published theorems: Baek's theorem, the cups-caps theorem). Fix: add
  "apart from cited published theorems".

## Checked and consistent (no finding)

- orient = (b0-a0)(c1-a1)-(b1-a1)(c0-a0), positive = counterclockwise, in all sections (ec's C7.cross with the stated
  coordinate shift; mm/mb caps = negative, cups = positive).
- rotAbout formula and counterclockwise direction identical in fd, ll, lg, oc, sr, sa; the three cited copies and all
  19 definitions in the records have the same body (fd's count confirmed).
- Invariant = maps into, everywhere; equality f(S)=S only noted as a consequence for injective f.
- hv/peel definitions and 0-based layer indexing identical in fd, ll, lg, oc, pc.
- HasConvexNGon without emptiness condition (fd, ec, mb explicit; others refer to fd).
- General position via collinearity / orient != 0 for pairwise distinct triples, everywhere.
- x/0 = 0 and 2π/0 = 0 stated consistently (fd, ll, lg, oc, ec, ar).
- Duplicated Lean declarations (iterate_mem, rotAbout*, Invariant copies, orient_rotAbout_inv, orient3(_perm),
  strict_supports, the six SymReduction affine lemmas fd/ar, reflLine sr/mb, the MirrorOdd lemmas mm/mb,
  hasConvexNGon_of_le fd/mm, dist2 lg/pc): same hypotheses, conclusions and line numbers in every restatement.
- Copy blocks (Merged/Linked/Capstone/Capstone2/ENCBLEAN copy, ES7Corollaries, OrbitConsistency copied block,
  AffineReduction, RTC parts A/B, the +26 and +1559 offsets) described identically in oc, pc, lg, ec, sr, ar, mm, mb,
  fd and confirmed against the files.
- Supply of Sixfold66/Sevenfold70 (ll, lg): C6UPPER (encoder B alone, 64 cubes; encoder A with unit clause, 32
  cubes), C7UPPER, ENCBLEAN sixfold66_of_cubes64, gaps G1-G4 and trust items E1-E6 as in the k8 note (apart from M2).
- Supply of HalfTurn34, Threefold33, Fivefold35, Fourfold32 and the mirror classes (sr, ar, mb, ec, sa): same
  records, same counts, same rigor labels (computer-assisted / Lean-checked), consistent with WRITEUP/SYMMETRIC.md §3.
- Trust statement: cake_lpr only, lrat-check secondary (ec, sr, ar, mb, cb), revision of 6 November 2026 (sr, ar).
- Lean 4.24.0, Mathlib f897ebcf, commit 7e32ee259 (fd, sa, appendix) in every section that names them.
- Axioms logs: LAYERLEAN axioms.log 28 theorems (ll) / 16 of lg's 23 (lg); re-check 19 (fd, ll) / 11 of lg's (lg);
  review log 59 (ll, lg); iterate_mem propext+Quot.sound only (fd, ll, oc); MirrorMain.out lines 848-863 (fd, mm, mb);
  SYMLEAN/mirror/axioms.out line 11 / lines 1-16 (fd, mm).
- TOC: 12 numbered sections with the contract's titles, Appendix A, References; no undefined reference; every
  "Lemma/Theorem/... \ref" word matches the environment of its label.
- Note (outside this lens): cb.tex refers to sa:sec, which is not in the contract's export list (sa is new); it
  resolves in the build.
