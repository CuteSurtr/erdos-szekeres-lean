# Section mb, round doc-r0: fix log

Inputs: the six minor notes under key "mb" in `build/open_minors.json` (from `reviews/mb-p1-diff.md`, m1–m3, and
`reviews/mb-p1-referee.md`, R1–R3). Pre-edit snapshot: `snapshots/doc-r0-pre/mb.tex`, `snapshots/doc-r0-pre/mb.map.tsv`.
Paths: `sections/`, `build/`, `reviews/`, `tools/` are relative to the staging area; `SYM5/...`, `WRITEUP/...`,
`LAYERLEAN/...`, `SYMLEAN/...`, `MIRRORETV/...` are relative to the results directory; `ErdosSzekeres/...` is relative
to the repository root. Line numbers refer to the current `sections/mb.tex` (1,204 lines).

All six notes were checked against the sources and found correct. All six are fixed; none is declined.

| # | note (lens) | summary | action | location | check against the sources |
|---|---|---|---|---|---|
| m1 | diff | map row `mb:lem:signs`: the first `;` in the `lean_name` and `file_line` columns had no following space, so `tools/make_appendix.py` (`re.split(r'[;,]\s+', s)`) would merge two names and two paths | fixed | `sections/mb.map.tsv`, row 11 (`mb:lem:signs`), columns 3 and 4 | Only the two separators changed (`diff` against the snapshot). No `;` followed by a non-space remains in any `sections/*.map.tsv`. A dry run of the generator's `split_list` on the row gives 3 names and 3 paths. The paths still name the right declarations: `Realization.lean:39` `cup_true_iff`, `ListGeometry.lean:19` `cup_sign`, `:24` `cap_sign`. The shared `appendix_map.tex` was not regenerated here (see "Other changes"). |
| m2 | diff | the path convention (everything not under `ErdosSzekeres/` or `docs/` is relative to the results directory) does not cover the bare file names `MirrorMain.lean`, `MirrorNine_append.lean`, `SymmetricReduction.lean`, `BoundaryGeometry.lean`, `Realization.lean`, `ActualRanks.lean` | fixed | mb.tex:28–29 (Sources paragraph) | Added: "A file name without a directory, such as `MirrorMain.lean`, is short for the file of that name whose full path is given in this section." A script listed every `\dirn` without a `/`. The six file names above each occur with their full path in the section: Sources list lines 32, 33, 45–54, and `SYMLEAN/SymmetricReduction.lean` at line 93. The other hits are record directories (C2FINAL, C3LEAN, SYM5, H3, ...), which the existing sentence already covers. |
| m3 | diff | Coverage: the parenthesis "they are the subject of Theorems mm:thm:mirror-polygon, ..., mm:thm:small" also covers `cap_below_lines`, `hasCap3_of`, `capacity_cup`, which section mm treats in Lemma mm:lem:slope (export) and Lemma mm:lem:cup (not exported) | fixed | mb.tex:1180–1183 | Now reads "(they are the subject of Lemma~\ref{mm:lem:slope} and of Theorems ..., or are used in their proofs; ...)". Checked: `mm.tex:233` is `mm:lem:slope` = `cap_below_lines`, and `mm.tex:815` is `mm:lem:cup` = `hasCap3_of`, `capacity_cup`. mm uses `mm:lem:cup`(b) in the proof of `mm:thm:small` (mm.tex:872, 883). In Lean, `capacity_cup` is used in `mirror_five`/`mirror_six` (MirrorMain.lean:2048, 2139), `hasCap3_of` in `capacity_cup` (:2015), and `cap_below_lines` in the three general polygon theorems (:2260–2453). `mm:lem:slope` is an mm export label, so mb may cite it. `mm:lem:cup` is not cited. |
| R1 | referee | the opening says the section restates Theorems sr:thm:main and ar:thm:main with three case classes; ar:thm:main has parts (a)–(e), and mb:thm:main3(b) restates only (a) | fixed | mb.tex:19–21 (opening); mb.tex:1078 (proof of mb:thm:main3(b)) | Opening now: "restate the reduction Theorem~\ref{sr:thm:main} and part~(a) of Theorem~\ref{ar:thm:main} (the `AffineEquiv` form) with the three remaining case classes ...". The proof now cites "Theorem~\ref{ar:thm:main}(a)". Checked: `ar.tex:647` has five parts, and (a) is `heptagon_of_nontrivial_affineEquiv` (`SYMLEAN/AffineReduction.lean:1501`, re-read). RTC contains only two `_3` theorems (4292, 4303). The other affine variants (RTC 1503, 1515, 1536, 1547) take five classes, as Remark mb:rem:main3 already says. |
| R2 | referee | Remark mb:rem:main3 says three times that "both proof checkers accepted the proof" but does not give the project's trust base (only cake_lpr counts; lrat-check is a secondary check) | fixed | mb.tex:1089–1092 (Remark mb:rem:main3, placed just before the itemized list that the sentence qualifies, after the sentence naming the records) | Added: "The project trusts one proof checker, `cake_lpr`: where a proof is said below to have been accepted by both proof checkers, `cake_lpr` accepted it, and that is the verdict that counts; `lrat-check` is only a secondary check, whose verdicts the project does not count (`WRITEUP/SYMMETRIC.md`, §3; an unpatched build of it accepts invalid proofs, `LRATCHECK20261105`)." Checked: `WRITEUP/SYMMETRIC.md` §3 "Trust base" (heading at line 202; lines 226–235: "Only cake_lpr ... is trusted"; "lrat-check ... is a secondary check only and not part of the trust base. Unpatched, it accepts invalid proofs of satisfiable formulas"; "Where this section says 'both checkers', the certificate is the cake_lpr verdict"). The same section records the threefold pieces and the central parallelograms as "each accepted by both checkers at solve time", and gives P1 and L1 cake_lpr verdicts (`SYM5/README.md`, table in §2). `LRATCHECK20261105/README.md` line 1 records the unpatched, unsound build. The wording follows section sr (sr.tex, Remark sr:rem:records) and cites the records, not `sr:rem:records`. |
| R3 | referee | the Fivefold35 item ("the encoder and the layer lemma have written proofs") understates the layer lemma and misplaces it: P1 needs no layer lemma, only L1 uses it, and the layer lemma is Lean-checked | fixed, with narrower wording than suggested | mb.tex:1105–1109 | Now: "the encoder has a written proof. The angle normal form (proof P1) needs no layer lemma; the layer normal form (proof L1) uses the layer lemma of `SYM5/README.md`, §2, whose statement that every convex layer is one orbit, and the strict nesting of the layers, are Lean-checked (Theorems~\ref{ll:thm:layers} and~\ref{lg:thm:nesting})." Checked: `SYM5/README.md` §2, notes under the table: "Each of P1 and L1 alone proves the theorem. P1 needs no layer lemma". The layer normal form adds the units "O_o is a convex polygon ..." and "every point of O_o' with o' > o is inside conv(O_o)". `LAYERLEAN/LayerLemma.lean:402` `layers_are_orbits` (export `ll:thm:layers`) and `:529` `strict_nesting` (export `lg:thm:nesting`; `LAYERLEAN/README.md`: "exactly the form of the layered encoders' nesting clauses"). `WRITEUP/SYMMETRIC.md`, Theorem 5: "The lemma, including strict nesting, is Lean-checked in LAYERLEAN". Why narrower than the suggested fix: the SYM5 statement also says "the centre lies strictly inside each layer". LAYERLEAN has no separate theorem with that conclusion, so the text names exactly the two Lean-checked parts and does not call the whole SYM5 statement Lean-checked. |

## Other changes

- R2 and R3 wording was tightened once after the first edit (no change of content): "only that verdict counts ...
  does not count" became "that is the verdict that counts; ... only a secondary check, whose verdicts the project does
  not count", and a compound "that ... and that ... is Lean-checked" became "whose statement that ..., and the strict
  nesting of the layers, are Lean-checked".
- No statement environment changed. All theorem, lemma, proposition and definition heads are identical to the snapshot
  (scripted comparison), and the statement of mb:thm:main3 is byte-identical. The only change inside a proof is "(a)"
  in the proof of mb:thm:main3(b). No label was added, removed or renamed. The map has 42 data rows of 5 fields each,
  and only row 11 changed.
- New cross-references, all to allowed export labels: `mm:lem:slope` (Coverage), `ll:thm:layers` and `lg:thm:nesting`
  (Remark mb:rem:main3). Each is defined in its section (`mm.tex`, `ll.tex`, `lg.tex`). They appear in a remark and in
  the Coverage paragraph, not in proofs, so the "Dependencies and rigour" paragraph was left unchanged.
- Not done here: regenerating `appendix_map.tex` with `tools/make_appendix.py`. It is a shared output built from every
  section map, and other sections may be under edit in this round. It should be regenerated once after all fixers of
  doc-r0 finish, which picks up the m1 fix.
- Hygiene: no machine path, no tool name, no `\newcommand`/`\usepackage`, and no "verified"/"certified" in
  `sections/mb.tex` or `sections/mb.map.tsv`.

## Compile check

`build/mb_wrapper.tex`, run twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`:
- both passes exit 0, with 16 pages;
- no line starting with `!`, and no "Missing" or "multiply defined";
- overfull boxes: 0 (none > 1pt); underfull: 3, the same count as the previous round;
- undefined references are only other sections' export labels:
  - `fd:def:{cp,gp,inv,ngon,orient,point}`;
  - `fd:lem:{affine-cp,affine-orient,collinear,cp-hull,mono,orient,pos-cycle,separation}`;
  - `mm:def:config`, `mm:lem:slope`, `mm:thm:{axis-polygon,even,line,mirror-polygon,odd,small}`;
  - `sr:def:{classes,iso}`, `sr:thm:main`, `ar:thm:main`, `ll:thm:layers`, `lg:thm:nesting`;
  - no `mb:` reference is undefined.
- The rendered text of the changed passages was read back with `pdftotext`. `cake_lpr`, `lrat-check` and the record
  paths typeset correctly.
