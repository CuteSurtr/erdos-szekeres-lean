# Final pass: consistency sweep (lens: sweep)

Verdict: **fail**, because of one major finding: the generated appendix is stale. Fixing it needs no edit to any
section. Running `python3 tools/make_appendix.py` from STAGE regenerates the appendix from the current maps and
resolves the major finding. After that, this lens finds no blocker or major finding. The other findings are minor
and optional.

Paths are relative to STAGE (`sections/`, `appendix_map.tex`, `proofs.tex`, ...) or to RES. Line numbers refer to the
current files. Nothing was edited. Scratch work was kept outside STAGE. The appendix generator was imported with
bytecode writing disabled and its output captured in memory, so neither `appendix_map.tex` nor `tools/__pycache__`
changed.

## Findings

| # | severity | location | issue | fix |
|---|---|---|---|---|
| 1 | major | appendix_map.tex:399, 498, 499, 500 (PDF of the last full build, 21:56: pp. 182, 186) | The appendix was generated at 21:39, before the final-pass map edits (cb.map.tsv 21:49, mb.map.tsv 21:50). Row 498 (`cb:thm:c2-refl`) still reads "Lean-checked (no committed axioms log; ...)". Row 399 (`mb:rem:main3`) still reads "the case-split bookkeeping (Theorem cb:thm:c2, Theorem cb:thm:c3) is Lean-checked by kernel evaluation". Rows 499-500 (`cb:fact:c2-sub`, `cb:thm:c2`) carry the old notes without the qualified label. The document inputs this file, so it still gives the C2FINAL bookkeeping the plain label that the final pass removed from cb, ar, mb, sr and their maps. | Run `python3 tools/make_appendix.py` from STAGE. An in-memory regeneration from the current maps gives 470 rows and no error. It changes exactly 8 rows (206, 248, 399, 498, 499, 500, 509, 510). Afterwards rows 498-500 begin "Lean-checked according to the record (no saved Lean output; ...)", and row 399 reads "... is Lean-checked according to the record (Theorem cb:thm:c2) or Lean-checked (Theorem cb:thm:c3), in both cases by kernel evaluation, so computer-assisted". The pc and sa rechecks compiled such a regenerated appendix standalone: exit 0, no overfull box. |
| 2 | minor | appendix_map.tex:206, 248, 509, 510 | Same cause. Row 206 (`pc:thm:word`) and row 248 (`ec:prop:ex341`) keep the old label "computer-assisted", while the heads now read "computer-assisted in Lean; written proof by hand" (pc.tex:769, ec.tex:785). Rows 509-510 keep the old sa notes. | The regeneration of finding 1 fixes these rows too. |
| 3 | minor (optional) | proofs.tex:39 with :52; cb.tex:62; fd.tex:46; fd.tex:115-116 with cb.tex:1199-1265 | Several generic, unqualified sentences cover C2FINAL. proofs.tex:39 says "The sections restate the Lean-checked results of the following files", and :52 lists `C2FINAL` among those files. cb.tex:62 says "Both files are checked with Lean~4.24.0". fd.tex:46 says the Lean files were checked with Lean 4.24.0. fd.tex:115-116 says that every head naming a declaration "is Lean-checked in this sense". cb.tex:80-88 qualifies only the three theorems, so the ten C2FINAL definitions (cb.tex:1199-1265) stay under that blanket sentence, although Lean's acceptance of them is also known only from `C2FINAL/README.md` §6. None of this is misleading: fd.tex:51 and 84-86 define the qualified label as a form of Lean-checked, and cb.tex:78-88 gives the evidence. No sentence attaches a plain label to the three theorems. | If a change is wanted: proofs.tex:52 `\item \dirn{C3LEAN} and \dirn{C2FINAL} (the latter Lean-checked according to the record), in Section~\ref{cb:sec};`. cb.tex:62 `Both files are checked with Lean~4.24.0 (for \dirn{C2FINAL/Central34Orbits.lean} according to its README; see the next paragraph).` cb.tex:81-82: say "the label of its declarations rests on that record alone: its three theorems are Lean-checked according to the record, and Lean's acceptance of its definitions likewise rests on that record". Otherwise leave as is. |
| 4 | minor (optional) | ec.tex:886-890; mb.tex:1179 | The ar Coverage now marks its conditional theorems (ar.tex:792-798), as ll.tex:800-801 and sr.tex:1138-1148 do. The ec Coverage lists the five ES(7) corollaries, which assume `Fivefold35` or `Fourfold32`, without saying that they are conditional. mb.tex:1179 says only "conditional" and does not name the hypotheses. No overclaim: the ec statements begin "Assume Fivefold35/Fourfold32", and ec.tex:66-68, 107-109 and 176-177 state the condition. | Optional, for uniformity. At the end of the first ec Coverage item add "(the three fivefold theorems conditional on \lean{Fivefold35}, the two fourfold theorems on \lean{Fourfold32})", and in mb.tex:1179 write "conditional on \lean{HalfTurn34}, \lean{Threefold33} and \lean{Fivefold35}". |
| 5 | minor (informational) | ec.tex:172 | The final pass added `Section~\ref{fd:sec}`. It is the only section-level reference to `fd:sec`, which is not in the contract's list of foundations labels. In the same pass the cb fixer avoided that reference for this reason and pointed to fd in words (cb.tex:82-83, as sa.tex:116 does). The reference resolves: fd.tex:1 defines it, proofs.tex:34 and :41 use it, and cb.tex:1516 refers to `sa:sec` in the same way. The ec recheck accepted it. | No change needed unless the strict reading of the label rule is applied. In that case write "in the foundations section". |
| 6 | minor (optional) | bibliography.tex:1 | The source comment "The sections cite them inline, by author and title" is out of date: proofs.tex:92-93 now lists more citation forms, and mb.tex:47 uses `\cite{Sch26}`. It is a comment and is not typeset. | Align the comment in a later pass, or leave it. |

## 1. The central-34 bookkeeping, C2FINAL, Central34, the three labels (task item 1)

Searched across line breaks in all twelve sections, all twelve maps, proofs.tex, preamble.tex, bibliography.tex and
appendix_map.tex. Search terms: `C2FINAL`, `Central34`, `central 34`/`34-point`, `cb:thm:c2-refl`, `cb:fact:c2-sub`,
`cb:thm:c2`, `cb:cor:c2`, `cb:rem:c2`, `closure of the central`, `subcase orbits`, `central parallelogram`,
`bookkeeping`, `case split`, `parallelogram`, `Lean-checked by`, `kernel evaluation`, and every sentence joining
`HalfTurn34` with `Lean-check`.

Correct: these places use "Lean-checked according to the record" or give no Lean label.
- cb.tex:78-83 (paragraph "Axioms") and cb.tex:85-88 (paragraph "Rigor labels and dependencies"). The latter gives
  C3LEAN the plain label and the three C2FINAL theorems the qualified one.
- cb.tex:1327 (after `cb:thm:c2-refl`), cb.tex:1376 (after `cb:fact:c2-sub`) and cb.tex:1390 (after `cb:thm:c2`), each
  "Lean-checked according to the record (paragraph ``Axioms'' in \S\ref{cb:sec:overview}), by kernel evaluation". The
  heads (cb.tex:1309, 1366, 1382) carry only the computer-assisted labels. Corollary `cb:cor:c2` (cb.tex:1401),
  Remark `cb:rem:c2-scope` (cb.tex:1418-1432), Coverage (cb.tex:1459-1464, 1477) and cb.tex:1, 5-6, 19-23, 39, 43,
  59-60, 92-96, 1194-1197, 1273-1280 give no Lean label.
- ar.tex:742-746: "the closure of the central parallelogram orbits, which is Lean-checked according to the record
  (\dirn{C2FINAL/README.md}, \S6; Theorem~\ref{cb:thm:c2})". ar.tex:727 and 736 name C2FINAL only as a record of
  claims and re-solves.
- mb.tex:1108-1111: "The bookkeeping of the subcase orbits ... is Lean-checked according to the record
  (\dirn{C2FINAL/README.md}, \S6), by kernel evaluation, so computer-assisted (Theorem~\ref{cb:thm:c2})". mb.tex:109
  only refers to the theorem. The sentence "Every Lean declaration stated below is Lean-checked" (mb.tex:109-110)
  concerns mb's own declarations.
- sr.tex:81-83: "Theorem~\ref{cb:thm:c2} is Lean-checked according to the record, Theorem~\ref{cb:thm:c3}
  Lean-checked". sr.tex:268-270: "the bookkeeping of the subcase orbits, Lean-checked according to the record
  (\dirn{C2FINAL/README.md} \S6), by kernel evaluation, and so computer-assisted (Theorem~\ref{cb:thm:c2}; ...)".
- Maps: cb.map.tsv:97-99 begin with the qualified label. cb.map.tsv:85-94 (definitions) and :100 give no Lean label.
  mb.map.tsv:41 gives no label, and mb.map.tsv:42 uses the qualified label.
- fd, ll, lg, oc, pc, ec, mm and sa do not mention the C2FINAL bookkeeping. ec.tex:120-122 cites
  `C2ENC/perturbation.md` and `C2ENC/class_table.md`, which concern the perturbation lemma.

Violations: only the stale appendix rows 399 and 498 (finding 1). The generic sentences of finding 3 are not label
violations.

Basis of the label: REPO at `7e32ee259`. A search outside `.git` and `.lake` finds `Central34`, `all_cases_closed`,
`closed_are_subcases` and `subcases_reflection` only in `C2FINAL/Central34Orbits.lean`, `C2FINAL/README.md`,
`C2FINAL/gen_lean.py`, `C2ENC/class_table.md`, `AUDIT3/reports/A5_central_geometry.md` and `WRITEUP/SYMMETRIC.md`.
None of these is Lean output. The 27 files of `C2FINAL` contain no compile, build or axioms log; the only `.out`
files are the three SAT checker outputs in `evidence/central34-cover`. So the qualified label (fd.tex:84-86) is the
right one.

## 2. "computer-assisted in Lean" (task item 2)

All uses, searched across line breaks, with the complete hand proof each relies on:

| use | statement | written proof that does not use the computation |
|---|---|---|
| cb.tex:777, 782, 790, 799 | Facts `cb:fact:refl-h3`, `refl-h6`, `topcases`, `strata` | Proposition `cb:prop:refl` (cb.tex:987-1077, "the following proof does not use the evaluation"). It uses only the written Lemmas `cb:lem:sort`, `options`, `decode`, `lex`, `orbits`, `codes`, `beq-refl` and the unfolding of `topCases`. |
| cb.tex:815 | Fact `cb:fact:roots-match` | Proposition `cb:prop:roots-match` (cb.tex:1079-1095): 100+10·81=910 by `cb:prop:refl`, decoding by `cb:lem:decode`(c). |
| cb.tex:1309 | Theorem `cb:thm:c2-refl` | cb.tex:1331-1363, from Lemma `cb:lem:c2-subsets` and Lemma `cb:lem:bits`. Checked: ρ_a is an involution of I_a with the single fixed point 9a mod 17 (9,1,10,2,11,3,12,4); 7+7=14; 14+546/2=287. |
| ec.tex:785 | Proposition `ec:prop:ex341` | ec.tex:790-798: 11·31=341; 1024=93·11+1=33·31+1=3·341+1 (each product checked); 2^340=(2^10)^34≡1 (mod 341). |
| pc.tex:23-24, 769, 998 | Theorem `pc:thm:word` | pc.tex:796-822: s=(x,y,z,¬x,¬y,¬z). All eight words and the run positions in the table were rechecked, and so was the shorter argument (s(j−1)=s(j+5)=¬s(j+2)). |
| fd.tex:12, 102-104 | definition of the label | none needed |
| cb.map.tsv:68-72, 97; ec.map.tsv:37; pc.map.tsv:29 | the same statements | as above |

No misuse. The converse also holds: the statements whose Lean proof is a finite computation and which have no hand
proof (`cb:fact:batches`, `roots-codes`, `roots-tsv`, `c2-sub`, `cb:thm:c2`) carry plain "computer-assisted".
Statements that use `decide` only for side facts (fd:lem:pos-triples, sa:lem:split, sa:thm:baek-seven, mb:prop:cap16)
are labelled not computer-assisted, as fd.tex:104-107 requires.

## 3. Consistency of the changed places (task item 3)

- C2FINAL label: the phrase "Lean-checked according to the record" is identical in cb, ar, mb, sr and the cb/mb maps.
  The pointers differ only in form: cb points to its "Axioms" paragraph, while ar and mb cite
  `\dirn{C2FINAL/README.md}, \S6` and sr cites `\dirn{C2FINAL/README.md} \S6` (sr's comma-less style, as at
  sr.tex:251 and 259). Exception: the stale appendix (finding 1).
- "computer-assisted in Lean": the phrase is identical everywhere. pc and ec add "; written proof by hand" (fd.tex's
  example). cb adds ", by kernel evaluation; written proof in Proposition~X / below". Both forms match fd.tex:102-104
  ("usually with a pointer to the written proof"). The pc Coverage (pc.tex:998) and pc's introduction (pc.tex:23-24)
  match the head. The ec Coverage (ec.tex:906-907, "a finite computation") describes the Lean proof and is
  compatible. Exception: appendix rows 206 and 248 (finding 2).
- C3LEAN label: "Lean-checked" in ar.tex:744, sr.tex:83 and 275, mb.tex:1115 ("Lean-checks") and cb.tex:85-86 and
  1132, consistent with `C3LEAN/logs/compile.log`.
- ar's conditional wording in Coverage: consistent with ll and sr. ec and mb differ (finding 4).
- Other final-pass sentences:
  - sa.tex:23-24, 44-48, 233-237, 283-285, 521-525 and 578-582 agree with ec.tex:911-912 (lines 1--1147 copy), sr.tex:298
    ("Fourfold32 (used only by Theorem sr:thm:variant)") and sr.tex:1164 (`group_form`).
  - mb.tex:1108-1110 ("canonical ... P_1,...,P_8 (to which reduction A reduces the others)") agrees with cb.tex:1426,
    sr.tex:266-267 and ar.tex:738.
  - mb.tex:119-121 ([m], Fin m) agrees with mm.tex.
  - mm.tex:991-993 (refl, isoT) agrees with mm.tex:1002-1003.
  - ec.tex:170-173 (f^n = f^{[n]}) agrees with fd.tex:133-135 and 152.
  - fd.tex:69-83 (search list) is consistent with every section that reports a rule-(a) search.
  - proofs.tex:39-43 and 92-93 are consistent with the sections.
  - preamble.tex:43-44 (`\hyphenation`) is not a macro and loads no package.

## 4. Machine paths and tool names (task item 4)

I scanned all 1107 `.tex` and `.tsv` files under STAGE: the document files, `build/`, `snapshots/` and the maps. The
patterns were the four machine-path prefixes, the scratch directory name, and a list of tool names with word
boundaries. Result: 0 hits. A plain substring search finds only "cursor" inside "recursor" (cb.tex:377), a false
positive. No `\newcommand` or `\usepackage` in the section files was introduced by the final pass.

## Checks run (all read-only)

- Diffs of every edited file against `snapshots/final-r1-pre/`: they contain only the passages described in the
  final-*-fix reports. ll, lg and oc were not edited in this pass.
- In-memory regeneration of the appendix and diff against `appendix_map.tex` (finding 1).
- pdftotext of the last full build (`build/final-recheck-front-r1/proofs.pdf`, 188 pages, 21:56; all section files
  predate it). Appendix rows 206, 248, 399 and 498 appear there unchanged, on PDF pp. 168, 171, 182 and 186.
- Read-only search of REPO at `7e32ee259` for the C2FINAL evidence (section 1).
- No pdflatex run: the last full build postdates every section edit. The rechecks compiled the regenerated appendix
  standalone, and the 8 regenerated rows reference only existing labels (`cb:thm:c2`, `cb:thm:c3`).
