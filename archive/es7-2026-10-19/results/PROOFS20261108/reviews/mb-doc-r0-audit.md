# Section mb, round doc-r0: diff audit (lens: diff)

**Verdict: pass.** No blocker, no major and no minor finding. All six notes of the round (m1-m3 from
`reviews/mb-p1-diff.md`, R1-R3 from `reviews/mb-p1-referee.md`) are fixed correctly; none was declined.

**Inputs.**
- Before: `snapshots/doc-r0-pre/mb.tex` (1,196 lines) and `snapshots/doc-r0-pre/mb.map.tsv`.
- After: `sections/mb.tex` (1,204 lines) and `sections/mb.map.tsv` (42 data rows).
- Fix log `reviews/mb-doc-r0-fix.md`; the six notes as listed under key `mb` in `build/open_minors.json`.
- Saved diffs: `build/mb_docr0audit_tex.diff` (5 hunks), `build/mb_docr0audit_tsv.diff` (1 hunk).

**Path conventions in this report.** `sections/`, `build/`, `reviews/`, `snapshots/`, `tools/` are relative to the
staging area; `SYM5/...`, `WRITEUP/...`, `LAYERLEAN/...`, `SYMLEAN/...`, `C2FINAL/...`, `C3LEAN/...`,
`LRATCHECK20261105/...`, `MIRRORETV/...` are relative to the results directory; `ErdosSzekeres/...` is relative to the
repository root. RTC is `SYMLEAN/mirror/ReductionThreeClasses.lean`. `mb.tex:N` is a line of the current file.

## 1. Scope of the diff

- A script compared all 42 statement environments of the two versions. Only the body of Remark `mb:rem:main3` changed.
  Every theorem, lemma, proposition and definition is byte-identical (head and body), so no `\leanref`, no hypothesis
  and no conclusion changed. The only change inside a proof is the reference "(a)" in the proof of
  Theorem `mb:thm:main3`(b).
- No label was added, removed or renamed. New `\ref` targets: `mm:lem:slope`, `ll:thm:layers`, `lg:thm:nesting`
  (all three are export labels in the contract) and `ar:thm:main` with a part suffix.
- Map: only row 11 (`mb:lem:signs`) changed, and only in two separators.
- Every added line is pure ASCII.

## 2. Hunk-by-hunk check

| # | where (current) | change | check | result |
|---|---|---|---|---|
| H1 | mb.tex:19-21 (opening; note R1) | "restate the reduction Theorem sr:thm:main and part (a) of Theorem ar:thm:main (the AffineEquiv form) with the three remaining case classes as their only case-class hypotheses" | `ar.tex:656`: `ar:thm:main` has parts (a)-(e); (a) is `heptagon_of_nontrivial_affineEquiv` (`SYMLEAN/AffineReduction.lean:1501`, copy RTC:1527, re-read). RTC has exactly two `_3` theorems: `heptagon_of_nontrivial_isometry_3` (4292-4297) applies `heptagon_of_nontrivial_isometry` (RTC:1023) to `h2 h3 h5 mirrorOneAxis33_proved mirrorNoAxis34_proved`; `heptagon_of_nontrivial_affineEquiv_3` (4303-4309) applies `heptagon_of_nontrivial_affineEquiv` in the same way. The other affine variants (RTC 1503, 1515, 1536, 1547) take five classes | correct |
| H2 | mb.tex:25-30 (Sources; note m2) | "A file name without a directory, such as MirrorMain.lean, is short for the file of that name whose full path is given in this section." | A script listed every `\dirn` argument without `/`: six file names and twelve record directories. The six file names are MirrorMain.lean, MirrorNine_append.lean, SymmetricReduction.lean, BoundaryGeometry.lean, Realization.lean and ActualRanks.lean. Each matches exactly one full path in the section: `MIRRORETV/lean/...` (lines 32-33), `SYMLEAN/SymmetricReduction.lean` (line 93), `ErdosSzekeres/Omission/...` (lines 45-54). The twelve directories are C2C34, C2FINAL, C2P, C2P5, C2RECHECK, C3FINAL, C3LEAN, C3SPOT, C3a, H3, LRATCHECK20261105 and SYM5. All exist under the results directory, and the existing sentence covers them. No file name (`.lean`, `.md`, `.out`, `.py`, ...) occurs outside `\dirn` or `\leanref` | correct |
| H3 | mb.tex:1078 (proof of mb:thm:main3(b); note R1) | "Theorem ar:thm:main(a)" | `ar.tex` uses `label=\textup{(\alph*)}`; part (a) is the declaration named in the parenthesis; the statement of mb:thm:main3 is unchanged and was re-read against RTC:4292-4309 (`IsEucIsometry` RTC:294, `eDist2` :291, `Invariant` :297): exact | correct |
| H4 | mb.tex:1089-1092 (Remark mb:rem:main3; note R2) | trust-base sentence: only cake_lpr counts; where "both proof checkers" accepted, cake_lpr accepted; lrat-check secondary, not counted; unpatched build accepts invalid proofs | See §3, rows R2a-R2d | supported |
| H5 | mb.tex:1105-1109 (Remark mb:rem:main3, Fivefold35 item; note R3) | "the encoder has a written proof. The angle normal form (proof P1) needs no layer lemma; the layer normal form (proof L1) uses the layer lemma of SYM5/README.md, §2, whose statement that every convex layer is one orbit, and the strict nesting of the layers, are Lean-checked (Theorems ll:thm:layers and lg:thm:nesting)" | See §3, rows R3a-R3d | supported |
| H6 | mb.tex:1177-1183 (Coverage; note m3) | "(they are the subject of Lemma mm:lem:slope and of Theorems ..., or are used in their proofs; ...)" | `mm.tex:233` is `mm:lem:slope` (`cap_below_lines`, MirrorMain.lean:2204, a lemma environment); `mm.tex:818` is `mm:lem:cup` (`hasCap3_of` :1991, `capacity_cup` :2002), used in the proof of `mm:thm:small` (`mm.tex:875`, `886`); `mm:lem:slope` is an mm export label, `mm:lem:cup` is not cited | correct |
| T1 | map row 11 `mb:lem:signs` (note m1) | `;` followed by a space in `lean_name` and `file_line` | `split_list` of `tools/make_appendix.py` now gives 3 names and 3 paths. Lines re-read: Realization.lean:39 `cup_true_iff`, ListGeometry.lean:19 `cup_sign`, :24 `cap_sign`. No `;` followed by a non-space remains in any `sections/*.map.tsv`. Map: header correct, 42 rows of 5 fields, labels and kinds equal to the 42 environments in order | correct |

## 3. New claims about records and Lean files

| claim (mb.tex) | evidence | result |
|---|---|---|
| R2a "The project trusts one proof checker, cake_lpr ... that is the verdict that counts" (1089-1091) | `WRITEUP/SYMMETRIC.md` §3 "Trust base" (heading line 202), lines 229-231: "Only cake_lpr (a36874a8, ...) is trusted, and a verdict counts only if it prints the line `s VERIFIED UNSAT`" | ok |
| R2b "where a proof is said below to have been accepted by both proof checkers, cake_lpr accepted it" | The two checkers are lrat-check and cake_lpr in every case below. HalfTurn34 parallelograms: `C2FINAL/README.md` §2, lines 62-63 (an orbit is closed only by a record with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`); `AUDIT3/README.md` line 46. Threefold33: `C3LEAN/README.md` §4 (certified = `certified` true, lrat_check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`). Fivefold35: `SYM5/README.md` §2 table (P1 and L1, cake_lpr `s VERIFIED UNSAT`); `SYM5/chk_P1_cake_lpr_heap30000.out` and `SYM5/chk_L1_cake_lpr.out`, line 1. Also `WRITEUP/SYMMETRIC.md` line 235: "Where this section says 'both checkers', the certificate is the cake_lpr verdict" | ok |
| R2c "lrat-check is only a secondary check, whose verdicts the project does not count (WRITEUP/SYMMETRIC.md, §3 ...)" | `WRITEUP/SYMMETRIC.md` lines 231-232 ("a secondary check only and not part of the trust base") and line 237 ("Accepted by lrat-check only (not certificates)") | ok |
| R2d "an unpatched build of it accepts invalid proofs, LRATCHECK20261105" | `LRATCHECK20261105/README.md` line 1 ("the unpatched, unsound build"); item 2: on the satisfiable `p cnf 1 1 / 1 0` with proof `2 0 0` it prints `c VERIFIED`; `WRITEUP/SYMMETRIC.md` line 233 ("Unpatched, it accepts invalid proofs of satisfiable formulas"). The wording agrees with sections sr (sr.tex:253-254), ec (ec.tex:111-113), cb (cb.tex:1161-1163) and ar (ar.tex:728-729) | ok |
| R3a "the encoder has a written proof" | Unchanged content, minus the layer lemma. `WRITEUP/SYMMETRIC.md` §3, "Written proofs, refereed or audited": `symcnf.py`, `SYM5/symcnf_layers.py` (`AUDIT3` A4) | ok |
| R3b "The angle normal form (proof P1) needs no layer lemma; the layer normal form (proof L1) uses the layer lemma of SYM5/README.md, §2" | `SYM5/README.md` §2 (heading line 46): the angle form (lines 62-64) and the layer form (65-67, whose units are "O_o is a convex polygon ..." and "every point of O_o' with o' > o is inside conv(O_o)"); the table (84-85) has P1 = angle and L1 = layer; the note at line 90 says "P1 needs no layer lemma"; the layer lemma is at lines 69-78 of §2. `WRITEUP/SYMMETRIC.md` Theorem 5: "the angle form (proof P1) and the layer form (proof L1)" | ok |
| R3c "whose statement that every convex layer is one orbit ... [is] Lean-checked (Theorem ll:thm:layers)" | SYM5 statement (lines 69-70): m-fold rotation, m >= 4, no centre point, no K-gon with K <= 2m implies every convex layer is exactly one orbit. `LAYERLEAN/LayerLemma.lean:402` `layers_are_orbits` has weaker hypotheses (0 < m, K <= 2m, c not in S, `Invariant (rotAbout c (2π/m)) S`, no K-gon) and concludes that for every nonempty `peel S n` the hull vertices are one orbit of m points. `LAYERLEAN/logs/axioms.log` line 3: three standard axioms. `ll.tex:523-524`: `ll:thm:layers` is a theorem environment on this declaration | ok |
| R3d "and the strict nesting of the layers, are Lean-checked (Theorem lg:thm:nesting)" | `LAYERLEAN/LayerLemma.lean:529` `strict_nesting` (adds 2 <= m and `GeneralPosition S`: for n < n', 0 < orient x (ρx) y), which is step 4 of the SYM5 proof (line 77). Fivefold35 concerns sets in general position. `axioms.log` line 5. `lg.tex:443`: `lg:thm:nesting` is a theorem environment. `LAYERLEAN/README.md` (table "Where the lemma is used"): for SYM5 "the layer lemma, from 'written proof' to 'Lean-checked'"; `WRITEUP/SYMMETRIC.md` lines 150-151: "The lemma, including strict nesting, is Lean-checked in LAYERLEAN". The text does not claim the clause "the centre lies strictly inside each layer" of the SYM5 statement; it understates, it does not overclaim | ok |

Rigor labels in the new text:
- "Lean-checked" is used only for `layers_are_orbits` and `strict_nesting` (axioms log).
- No case class is presented as proved; the closing sentence "So the three hypotheses are not Lean-checked" is unchanged.
- SAT verdicts are now anchored on cake_lpr, as the contract requires.

## 4. The fixer's dispositions

| note | status in log | audit |
|---|---|---|
| m1 (map separator) | fixed | fixed (T1) |
| m2 (bare file names) | fixed | fixed (H2) |
| m3 (Coverage parenthesis) | fixed | fixed (H6) |
| R1 (scope of the restatement) | fixed, also in the proof | fixed (H1, H3) |
| R2 (trust base for "both checkers") | fixed | fixed (H4, §3 R2a-R2d); cites the records, not `sr:rem:records` |
| R3 (layer lemma understated/misplaced) | fixed, narrower than suggested | fixed (H5, §3 R3a-R3d). The narrower wording is the accurate choice: LAYERLEAN has no single theorem whose conclusion is the SYM5 clause "the centre lies strictly inside each layer" |

Declined notes: none.

The fix log's other claims also check out:
- the statement heads are unchanged (scripted, §1);
- the map has 42 rows of 5 fields, and only row 11 changed;
- the hygiene claims hold.

`build/open_minors.json` lists exactly these six notes under `mb`.

## 5. Compile check

The wrapper is `build/mb_docr0audit_wrapper.tex`. It is the contract's wrapper: `\input{../preamble}`, then
`\input{../sections/mb}`. I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice from `build/`.
- Both passes exit 0, with 16 pages.
- There is no line starting with `!`, and no "Missing", "multiply defined" or "Missing character". The two `microtype`
  lines that mention a missing character are protrusion Info messages.
- Overfull boxes: 0, so none is over 1pt.
- Underfull boxes: 3, all cosmetic and the same as the previous round: the hbox in the axioms paragraph (lines 71-78),
  and two vboxes while `\output` is active.
- Undefined references are only allowed external labels:
  - `fd:def:{cp,gp,inv,ngon,orient,point}` and `fd:lem:{affine-cp,affine-orient,collinear,cp-hull,mono,orient,pos-cycle,separation}`;
  - `mm:def:config`, `mm:lem:slope` and `mm:thm:{axis-polygon,even,line,mirror-polygon,odd,small}`;
  - `sr:def:{classes,iso}`, `sr:thm:main`, `ar:thm:main`, `ll:thm:layers` and `lg:thm:nesting`.

  No `mb:` reference is undefined. All 75 distinct `\ref` targets in `mb.tex` are the section's own labels, `fd:`
  labels, or export labels listed in the contract.
- **Rendering.** `pdftotext` shows the changed passages correctly: `cake_lpr`, `lrat-check`, the record paths, `§2` and
  `§3`, and "Theorem ??(a)" in the standalone build. Pages 15-16, rendered at 70 dpi, lay out the remark and the
  Coverage list cleanly.

## 6. Hygiene

- There is no machine path in `mb.tex` or `mb.map.tsv`.
- There is no tool name. The only grep hit is a substring of `smallmatrix`, a false positive.
- There is no `\newcommand`, `\usepackage` or other macro definition.
- The words "verified" and "certified" do not occur. "Certificate" occurs only in passages this round did not change:
  `linear_combination` coefficients, "no SAT certificate", and "what its certificate proves".

## 7. Findings

None.

## 8. Notes (not findings)

- **Placement of the trust sentence.** In Remark `mb:rem:main3` (mb.tex:1088-1092), the trust-base sentence stands
  between "supplied by the following records (...)" and the itemized list. It reads naturally in the PDF, because it
  qualifies the list that follows, so no change is needed.
- **"the AffineEquiv form".** Part (b) of `ar:thm:main` (`..._affineEquiv_image`) also uses an `AffineEquiv`. The
  phrase in the opening (mb.tex:20) still identifies part (a) without ambiguity, since "part (a)" is named explicitly.
  It also matches the remark's own usage (mb.tex:1116-1121), which lists `_image` among the other variants.
- **The appendix.** `appendix_map.tex` is currently a 14-byte placeholder. Regenerating it with
  `tools/make_appendix.py` after all doc-r0 fixers finish will pick up m1, as the fix log says.
