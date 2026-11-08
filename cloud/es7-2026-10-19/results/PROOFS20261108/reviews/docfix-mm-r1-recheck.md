# Recheck of section `mm` after the whole-document review, docfix round 1

Inputs: fix log `reviews/docfix-mm-r1-fix.md`; `diff -u` of `snapshots/docfix-r1-pre/mm.{tex,map.tsv}` against
`sections/mm.{tex,map.tsv}` (mm.tex 966 -> 1060 lines; map 22 rows, columns 1-4 unchanged, notes of 4 rows changed).
Sources re-read (paths relative to RES unless they start with `ErdosSzekeres/`): `MIRRORETV/lean/MirrorMain.lean`
(2498-2510, 2596-2606, 2626-2660, 1935-1950, 1512-1977 heads), `MIRRORETV/lean/MirrorNine_append.lean`,
`MIRRORETV/lean/FarFlat.lean` + `.out`, all four files of `MIRRORETV/review/` with their `.out` logs,
`MIRRORETV/README.md`, `MIRRORETV/PROOFS.md` (Lemma 3.1, Theorem B, Lemma 5.1), `MIRRORETV/SHA256SUMS`,
`WRITEUP/SYMMETRIC.md` section 0, and the sections `mb`, `sr`, `ar`, `sa` for the cross-references.

**Verdict: pass.** All six findings are resolved within `mm`'s files. No blocker or major finding remains or was
introduced. Two minor items remain: one wording nit, and follow-ups outside `mm`'s files.

## 1. The six findings

| # | finding | status | evidence |
|---|---|---|---|
| 1 | xref-mmmb (minor): pointers to mb:thm:seven/eight for non-export statements | resolved | Coverage (mm.tex 951-960) now says the eight declarations are "treated in the section of" mb:thm:seven/eight: `mirror_seven`, `mirror_eight` and the `_line` versions *are* those theorems (mb heads at mb.tex 829-833, 869-872), and the other four are statements used in their proofs. Checked against mb: `hasNGon_heptagon` = mb:prop:gon, `capacity16` = mb:prop:cap16, `mirror_seven_of` = mb:lem:seven-of, `capacity22g` = mb:prop:cap22. All are used, directly or through mb:prop:cap16 / mb:lem:gc22, in the proofs of mb:thm:seven/eight (mb.tex 715, 737, 845, 884, 891). Remark mm:rem:hm(1) (mm.tex 680-684): the three capacity bounds are mb:prop:cap16/cap22/cap113, used in those proofs (mb.tex 845, 884, 982). `mirror_seven'`/`mirror_eight'` are in mb:rem:seven and mb:rem:eight (mb.tex 857-863, 901-905). `C12Check.mirror_nine` is mb:thm:nine(b). The MirrorNine_append item now says five declarations (checked: lines 24, 99, 116, 131, 136, all in `C12Check`), of which `config_capacity113`, `mirror_nine` and `mirror_nine_line` are mb:thm:nine. All correct. |
| 2 | consistency (minor): "unproved hypothesis" / "conditional on (hM)" | resolved | Rigor (82-83), theorem bodies of mm:thm:odd/even (612-613, 643-644), mm:thm:line(b),(c) (799-800, 803-804), Remark (1) (665-669) and the map notes now say "parametric hypothesis". The statements still assume (hM) explicitly ("assume the following parametric hypothesis on M, which is part of the statement"), so no hypothesis is presented as proved. No "unproved hypothesis" or "conditional on (hM)" is left in mm.tex or mm.map.tsv (grep). The wording matches ar's and mb's treatment of parametric premises and README section 1 ("with the value of N as a hypothesis"). |
| 3 | claims (minor): title "Theorem A" collides with WRITEUP/SYMMETRIC.md Theorem A | resolved in mm; contract row open | Title: "The mirror lemma and the mirror reduction (Theorem A of MIRRORETV)", with `\texorpdfstring`. The TOC entry and the PDF bookmark are clean (checked in the aux and in the fixer's full build `build/mm_docfix_r1_full/proofs.{toc,out}`). Subsection 9.5 is renamed "The mirror reduction". The intro (10-13) fixes the convention. Its new sentence on WRITEUP Theorem A is accurate: WRITEUP/SYMMETRIC.md:17-18 is "Every set of at least 33 points in general position that has a symmetry contains a convex 7-gon", and sr:thm:main, ar:thm:main (five case classes) and mb:thm:main3 (three case classes) are its only restatements in this document. sa states only the arithmetic lemmas, and sr.tex 974-979 and ar.tex 753-757 say the same ("establishes it only conditionally"). Every other "Theorem A" in mm.tex means the mirror reduction (grep). **Open, outside mm:** CONTRACT.md:154 still lists the title "The mirror lemma and Theorem A". |
| 4 | completeness (major): MIRRORETV/review/ excluded without reason, described inaccurately | resolved | One item per file, with a document-level reason. All factual claims were re-checked against the files (details in section 2): line counts, SHA-256 prefixes, declaration counts (MirrorA: 16 defs, 46 lemmas + 9 theorems = 55, 1 example; 10 main results; the other 45 are all `lemma`; MirrorCap: 3 defs + 8 lemmas + 5 theorems = 16), every cited line number, every statement gloss, and the three `.out` logs (8 / 3 / 5 `#print axioms` lines, standard axioms; FarFlatExtra 4 unused-variable warnings). The k = 3 extension and `MirrorCap.coincidences` are now stated (the latter with its exact Lean conclusion; the count |V| = 2m - e is attributed to the file's comment, which is correct). ReplayRepo is described as an audit (elab at 51, run at 118; header lines 44-48; log: 57 modules, 497 footprint constants, 0 axioms, replay succeeded). FarFlatExtra is no longer called a re-formalization. Every inventory "main result" from these files (`inventory/MIRRORETV.json`) is named. "Written by reviews" and "importing only Mathlib" are as in MIRRORETV/README.md:82-83. No Lean file of the repository imports any of the four (grep of `import` lines), and no other section mentions them (grep). |
| 5 | completeness (minor): FarFlat.lean exclusion read as section-local | resolved in mm; README open | FarFlat.lean and FarFlatExtra.lean form one item with the reason "This document treats no part of Theorem B, so no section restates either file". True: no other section mentions Theorem B, far-flat, FarFlat or FFX (grep). Both import only Mathlib, and README section 3 / PROOFS.md section 5 confirm Theorem B is the far-flat construction. FarFlat facts unchanged and re-verified (lines 12, 15, 34, 55, 60, 67, 89; FarFlat.out prints 5 of 6 theorems). **Open, outside mm:** STAGE has no README yet. Its future list of Stage 1 files left out on purpose should name FarFlat.lean, FarFlatExtra.lean, MirrorA.lean, MirrorCap.lean and ReplayRepo.lean. |
| 6 | typesetting (minor): loose Sources/Coverage, gap before "Coverage." | resolved | Sources and Coverage are inside `{\raggedright ... \par}`, and the Sources file list is itemized. Standalone build: no underfull line in Sources or Coverage. The 47 badness-10000 hboxes are all in statement heads (front-matter issue F1, not assigned here). Rendered pages 1, 12, 13, 14 show no gap, and "Coverage." follows the proof directly. In the fixer's full build (pp. 103, 114-115) there is also no visible gap. Note: the fix log's "0 underfull vboxes" for that build is not exact. Its mm segment has 2 ("while \output is active", pp. 103 and 115), but both pages are full and show no gap. |

## 2. Hunk-by-hunk check (referee)

- **Title, l. 1:** sound LaTeX (`\texorpdfstring{\dirn{MIRRORETV}}{MIRRORETV}`). The aux writes `\nolinkurl {MIRRORETV}` (robust), and the bookmark text is plain.
- **Intro, ll. 10-13:** checked as in finding 3. New refs sr:thm:main, ar:thm:main and mb:thm:main3 are export labels.
- **Sources, ll. 35-64:** the content is unchanged apart from the regrouping and the new last sentence ("FarFlat.lean ... and the four Lean files of MIRRORETV/review/ are not used here"). MIRRORETV/review has exactly four Lean files, and MIRRORETV has seven Lean files in all, every one accounted for. All seven SHA-256 prefixes re-computed: MirrorMain `ca623e55a1b9`, Realization `ae4970e0808e`, ConvexCycleCuts `b4ad0ba9e583`, Definitions `2425500eefd1`, Basic `13667aa2d3dc`, Orientation `f67955ac7091`, OrientationGeometry `c7db9bbbb65e`, plus the SYMLEAN copy `0cc83994fe8c`. MirrorMain has 2677 lines.
- **Rigor, ll. 81-83:** no rigor label is rounded up. (hM) stays a hypothesis, and the discharged instances are Lean-checked theorems (Remark (1)).
- **mm:thm:odd / mm:thm:even bodies, mm:thm:line(b),(c):** wording only. The Lean sources were re-read: `mirror_odd_general` (2498), `mirror_even_general` (2599), `transport` (1937), `mirror_odd_general_line` (2641) and `mirror_even_general_line` (2650). Hypotheses, conclusions and quantifier order still match exactly (`2 ≤ j`, hM over all n and `Configuration n` with `¬ c.HasCap (j+1)` / `¬ c.HasCap j`, `GeneralPosition S`, maps-into symmetry, `S.card ≤ 2*M` / `2*M+2`, `n0^2+n1^2 = 1`).
- **Remark mm:rem:hm(1), (2):** the new sentences are correct (finding 1). "As soon as (hM) is proved for that pair" is hypothetical and does not overclaim. (2) now points to the Coverage paragraph.
- **Subsection rename:** consistent with the convention; no reference depends on it.
- **Coverage, ll. 911-1057:** the MirrorMain items are unchanged except item 1 (finding 1). The line numbers of the eight declarations were re-checked: 1512, 1529, 1676, 1803, 1812, 1820, 1969, 1977. The new items were checked statement by statement against the Lean files:
  - **MirrorA:**
    - `lemma31` (282): IsCapSeq with all ordinates >= 0, so V m c is ConvexPos. This matches PROOFS.md Lemma 3.1.
    - `cap_convexPos` (352) and `cup_convexPos` (417) are as described.
    - `theoremA_even` (593) and `theoremA_odd` (615): j >= 2, MirrorSym, GenPos, no 2j (resp. 2j-1) points in convex position, so there exists X with InClass (2j) j (2j) X (resp. (2j-1) j (2j-1)) and |S| <= 2|X|+2 (resp. 2|X|). X ⊆ S is not stated, and the text correctly says "some set X".
    - `_bound` (685, 694), `transport` (771, a `lemma`), `_line` (810, 821), `refl_refl`, `refl_fix_line`, `refl_normal` and the `example` (852) are as described.
    - j = 2 in `theoremA_odd` gives k = 3.
  - **MirrorCap:** hypotheses hx, hcap (consecutive), hint, h0, hlast, hone; the conclusion is v ∉ conv(V \ {v}). `coincidences` (327) has exactly the stated three-part conclusion.
  - **"Beyond this overlap":** mm's mirror lemma (mm:thm:mirror-polygon/axis-polygon) covers no point on the axis or one endpoint on it, never both. mm:thm:odd needs k >= 5. mm states no consecutive-triple convex position of caps or cups (mm:lem:cup's proof uses the all-triples positive-cycle lemma). So the listed extras are accurate.
  - **FFX:** the declaration lines are 20, 22, 28, 44, 60, 69 and 91. `orient_sum` and `bary_of_neg` have the same statements as FarFlat's `orient_sum`/`inside_triangle` (compared token by token). The glosses of `gp_cross_axis`, `a1_inside` and `lemma51_core` match their docstrings and PROOFS.md section 5.
  - **ReplayRepo:** checked as in finding 4.
- **Map:** 22 rows, 5 columns, ASCII only; labels and columns 1-4 unchanged. `tools/make_appendix.py`, run on a scratch copy (`build/mm_recheck_r1_app/`), exits 0 (470 rows). The real `appendix_map.tex` is stale for several sections fixed this round, mm's four note rows among them, and must be regenerated centrally.
- **Hygiene:** no machine path and no tool name in mm.tex or mm.map.tsv (grep; the only hit for the tool-name pattern is "psmallmatrix"). The ReplayRepo header's author tag is not reproduced. No "verified"/"certified". Every external `\ref` (ar:thm:main, mb:thm:baek, mb:thm:eight, mb:thm:main3, mb:thm:nine, mb:thm:seven, sr:thm:main, fd:*) is allowed by the contract.

## 3. Compile

The wrapper `build/mm_recheck_r1_wrapper.tex` has the contract wrapper's content. It was compiled twice from `build/`, starting from an empty aux:
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.

- Both passes exit 0, with no `!` error, no "Missing $", no multiply defined label and no hyperref warning.
- 0 overfull boxes, so none above 1pt.
- 14 pages.
- Undefined references only to fd: labels and to the export labels listed above (expected in the standalone check).
- 57 underfull hboxes, 47 of them badness 10000, all in statement heads. 2 underfull vboxes with no visible gap.
- Pass 2 ends with "Label(s) may have changed" because it started from an empty aux. A third pass leaves the aux unchanged and the warning gone. The full document is built with three passes anyway.

## 4. Remaining items (all minor)

- **m1 (follow-up, outside mm's files):**
  - CONTRACT.md:154 still gives the old title "The mirror lemma and Theorem A". Change it to "The mirror lemma and the mirror reduction (Theorem A of MIRRORETV)".
  - The planned README list of Stage 1 files left out on purpose does not exist yet. It should name MIRRORETV/lean/FarFlat.lean and MIRRORETV/review/FarFlatExtra.lean (far-flat Theorem B estimates), MIRRORETV/review/MirrorA.lean and MirrorCap.lean (independent review formalizations), and MIRRORETV/review/ReplayRepo.lean (kernel-replay audit).
  - `appendix_map.tex` must be regenerated.
- **m2 (wording), mm.tex:991:** "\lean{refl} and \lean{isoT} for the reflection in a line through a point with a unit direction" reads as if both were the reflection. `isoT` is the rigid motion taking the line p0 + R u to the x-axis (MirrorA.lean:710-712), as l. 1001-1002 itself says. Suggested: "\lean{refl}, the reflection in the line through a point with a given unit direction, and \lean{isoT}, the rigid motion that maps this line onto the $x$-axis".
