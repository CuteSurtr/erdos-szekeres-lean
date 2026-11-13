# Section `pc`, round doc-r0: diff audit

Lens: diff. Inputs:
- the pre-edit snapshot `snapshots/doc-r0-pre/pc.tex` (996 lines) and `pc.map.tsv`;
- the current `sections/pc.tex` (1014 lines) and `sections/pc.map.tsv`;
- the fix log `reviews/pc-doc-r0-fix.md`;
- the notes it addressed: `reviews/pc-p1-diff.md` (m1, m2) and `reviews/pc-p1-referee.md` (F1, F2, F3), the five
  notes listed for `pc` in `build/open_minors.json`.

Paths below are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`), to RES (Lean sources and
records) or to the repository root (`ErdosSzekeres/...`). The repository checkout is at commit `7e32ee259`.

**Verdict: pass.**
- No blocker, no major and no minor finding.
- 5 notes marked fixed; all 5 are fixed correctly. 0 declined.
- The build is clean: both passes exit 0, no error, 0 overfull boxes; 51 underfull boxes, the same as the snapshot
  built with the same preamble (`build/docr0_snapcheck/`).
- Two observations (O1, O2) with optional wording improvements; neither is an inaccuracy.

## 1. Hunks checked

`diff -u` gives 5 hunks in `pc.tex` (current lines 6-10, 63-66, 86-93, 788-794, 836-843) and 2 changed rows in
`pc.map.tsv` (note column only). This matches the fix log; there is no undocumented change. A scripted comparison
with the snapshot shows: the 34 labels are identical and in the same order; the 54 `\leanref` pairs are identical;
the only `\ref` added is `pc:rem:reading` (own label); of the 32 statement environments only Remark
`pc:rem:word-scope` changed. No Lean-referenced statement, head or part changed.

| # | Location (current file) | Change | Check |
|---|---|---|---|
| 1 | Opening, lines 4-10 | The six directions are "distinct unless one of the gaps β−α, δ−β, α+2π−δ equals π, in which case a direction and an antipode coincide (Remark pc:rem:reading)"; "these six points" becomes "these points, expressed by the arc predicates of Definition pc:def:arc (which are defined in every case)" | Proof: given α<β<δ<α+2π, two directions (or two antipodes) differ by an amount in (−2π,2π)∖{0}, so they never coincide mod 2π; a direction x and an antipode y+π coincide mod 2π iff x−y ≡ π, i.e. (x≠y) iff β−α, δ−β or δ−α equals π, i.e. iff g1, g2 or g3 equals π (g3 = 2π−(δ−α)). So "distinct unless a gap equals π" and "then a direction and an antipode coincide" are both exact. My own exact check (`build/pc_docr0audit_check.py`, angles in units of π/24, α ∈ {0, π/7, −5π/3}): 3243 ordered triples, 207 with a gap equal to π, 0 mismatches for both claims. The remark cited says the same (lines 302-305). The arc predicates are defined for all real α, β, δ (Definition pc:def:arc). OK |
| 2 | Rigor and axioms, lines 63-66 | "Every definition, lemma, proposition, theorem and corollary below whose head or one of whose parts carries a Lean reference is Lean-checked; ... Remarks are commentary and, even when they name Lean declarations, are not Lean-checked as a whole; the mathematical claims they add to the Lean statements are written observations." | The section has 32 environments: 8 remarks, 1 written step (Lemma pc:lem:shift, no Lean reference) and 23 definitions/lemmas/propositions/theorems/corollaries, each with a Lean reference in its head (pc:lem:polar-facts and pc:thm:layers also in their parts); no `fact` environment. Every part of these 23 statements is a Lean statement (re-read pc:lem:polar-facts, pc:lem:helpers, pc:def:polar, pc:def:arc). The sentence narrows the old one, so no rigor label is raised. It agrees with the local labels in pc:rem:gaps(2) ("a written observation, not part of the Lean statement") and pc:rem:runs ("a written observation, not Lean-checked") and with the Coverage paragraph. Remark pc:rem:word-scope attributes "Lean-checked" only to named ENCBLEAN declarations, which is compatible with "not Lean-checked as a whole". OK |
| 3 | Rigor and axioms, lines 86-93 | The ENCBLEAN geometric package compiles the copy "from the same sources, against the same imports, as the original file": byte-identical copy, common pins, and the ten repository modules that `Capstone2.lean` needs compiled from verbatim copies whose SHA-256 hashes are in `ENCBLEAN/geo/VENDOR.sha256` and agree with the repository files | See section 3. OK |
| 4 | "How Lean checks it", lines 788-794 | M7's replacement by `True` is credited to `LEANEXT/phase/mutants.py`; the log is cited for the mutant's name and the error; "the script logs only the first line of the first error message" | `mutants.py:23-24`: M7 "drop antipodal premise in word_dichotomy" replaces `    ∀ s : Fin 6 → Bool, (∀ i : Fin 6, s (i + 3) = !s i) →` by `    ∀ s : Fin 6 → Bool, True →` (the script asserts the pattern occurs once). `logs/mutants.log:7`: "M7 drop antipodal premise in word_dichotomy: exit=1 errors=1 first=Mutant7.lean:543:2: error: Tactic `decide` proved that the proposition". `mutants.py:38-40` keeps the lines containing ": error" and prints `errs[0]` (path prefix stripped, cut at 110 characters; this line has 70), i.e. the first line of the first error message. Lean 4.24.0 `Lean/Elab/Tactic/ElabTerm.lean:506-508` (local toolchain sources, read only): "Tactic `{tacticName}` proved that the proposition{indentExpr expectedType}\nis false", so "continues with the proposition and 'is false'" is right. `PhaseClassification.lean:539-543` re-read (statement unchanged; `decide` at line 543, as in the log position). OK |
| 5 | Remark pc:rem:word-scope, lines 836-843 | Axiom evidence for `EncB.wordSpec`, `EncB.Geo.Arc.arcFrame`, `EncB.Geo.labelling_ruleB` | See section 3. OK |
| 6 | Map row `pc:lem:helpers`, note | appended: the copy is compiled against verbatim copies of the ten repository modules (`ENCBLEAN/geo/VENDOR.sha256`, hashes equal to the repository files) | Same facts as hunk 3. OK |
| 7 | Map row `pc:rem:word-scope`, note | appended: `SoundWord.lean:228-229` (with `logs/axioms.log:446`), `logs/m8_fix_build.log:29,35`, `Audit.lean:45-46` | Same facts as hunk 5; `Audit.lean:45-46` is exactly the `modelOfLabelling` pin (lines 48-49 are the `labelling_of_counterexample` pin). OK |

Map integrity (script): header unchanged; 32 rows, 5 fields each, all ASCII; labels and kinds equal the 32
environments in order; columns 1-4 of both changed rows are unchanged.

## 2. Touched statements re-read against Lean

No statement environment that corresponds to a Lean declaration was touched (scripted comparison, section 1). The
one touched environment is Remark pc:rem:word-scope, whose Lean sources I re-read:
- `ENCBLEAN/EncB/SoundWord.lean` (229 lines, SHA-256 `c1bdb4175ee5...`): `theorem wordSpec : WordSpec` at line 222.
- `ENCBLEAN/geo/ES8Geo/ArcBridge.lean` (497 lines, `46966b48a101...`): `theorem arcFrame` at line 393 (true
  directions α<β<δ<α+2π); `theorem labelling_ruleB` at line 473, which calls `Arc.arcFrame` at line 480 and
  `PhaseClassification.orient_pos_of_runMidB` at line 481.
- `ENCBLEAN/geo/ES8Geo/ModelOfLabelling.lean:30`: `ruleB := labelling_ruleB hm heven L`.

The hunk-4 paragraph sits next to Theorem pc:thm:word, so I also re-read `PhaseClassification.lean:539-543`; the
theorem text in pc.tex is unchanged and still exact (premise `∀ i, s (i + 3) = !s i`, conclusion (i) ∧ (ii)).

## 3. New claims about Lean files and records, checked against RES

**Hunk 3 (vendored modules; referee F3).**
- `LEANEXT/capstone/Capstone2.lean` imports the repository modules `ErdosSzekeres.Definitions` (line 1),
  `.OrientationGeometry` (2), `.Suk.OrientationClique` (3) and `.Orientation` (10); the rest are Mathlib imports. The
  four modules named in the text are exactly these.
- Their transitive closure among repository modules (script over `import` lines, repository checkout) has exactly
  10 modules: Basic, Definitions, Orientation, OrientationGeometry, Suk.BaseChart, Suk.BaseOrder, Suk.FourPoint,
  Suk.OrientationClique, Suk.SupportingLines, Suk.TriangleOrder. These are the 10 entries of
  `ENCBLEAN/geo/VENDOR.sha256`, the 10 files under `ENCBLEAN/geo/ErdosSzekeres/` and the 10 globs of the
  `ErdosSzekeres` lean_lib in `ENCBLEAN/geo/lakefile.toml`.
- `shasum -a 256 -c` of the hash lines of `VENDOR.sha256`: all 10 OK against the vendored copies, and all 10 OK
  against `ErdosSzekeres/...` of the repository checkout.
- Same module names: `ENCBLEAN/geo/lakefile.toml:5-8` says the repository is not required by path and the ten
  modules are "copied verbatim into ErdosSzekeres/ ... so every constant keeps its repository name". The `encblean`
  path dependency is the Std-only root package (`lean_lib EncB` only), so no other `ErdosSzekeres` modules can
  enter.
- Pins: repository `lean-toolchain` v4.24.0 and Mathlib `f897ebcf72cd...` (repository `lake-manifest.json`);
  `ENCBLEAN/geo/lean-toolchain` v4.24.0 and Mathlib `f897ebcf72cd...` (lakefile rev and `lake-manifest.json`). The
  only build option is the repository's `weakLeanArgs = ["-j1"]` (thread count; no effect on elaboration).
- The original side: `LEANEXT/README.md:6` says each LEANEXT file "compiles with `lake env lean` from the
  repository root". Git history: the ten modules were last changed on 2026-10-04, before LEANEXT (2026-11-04), so
  the original was compiled against the same module sources. The vendored copies were committed once (`862d95ed5`,
  2026-11-07, with the M4-M8 builds and `Audit.lean`) and never changed. `VENDOR.sha256` was later edited only in
  its comment line (commit citation); its hash lines are unchanged.
- `Capstone2.lean` and `ENCBLEAN/geo/ES8Geo/Capstone2.lean`: both SHA-256 `f8c3930c2427...`.
- So "The package compiles the copy from the same sources, against the same imports, as the original file" is true,
  and the conclusion "So the axioms of the declarations used are among these three as well" is a sound inference.

**Hunk 5 (axiom evidence for the encoder-B counterpart; diff m2).**
- `SoundWord.lean:228-229`: `/-- info: 'EncB.wordSpec' depends on axioms: [propext, Classical.choice, Quot.sound] -/`
  and `#guard_msgs in #print axioms EncB.wordSpec`, right after the theorem at 222. OK.
- `ENCBLEAN/logs/m3_build.log:9`: "Built EncB.SoundWord (1.4s)"; rc=0 (line 3). `SoundWord.lean` has one commit
  (`73928596f`, M3), and its hash `c1bdb4175ee5...` is the one in `ENCBLEAN/logs/env.txt:24` and
  `m9_review_lean_soundness.log:61`. OK.
- `ENCBLEAN/logs/axioms.log:446`: "'EncB.wordSpec' depends on axioms: [propext, Classical.choice, Quot.sound]"
  (header: M3 step, against the `.olean` files of `m3_build.log`). OK.
- `ENCBLEAN/logs/m8_fix_build.log:35`: `EncB.Geo.Arc.arcFrame`, and `:29`: `EncB.Geo.labelling_ruleB`, both
  [propext, Classical.choice, Quot.sound]. The text pairs "arcFrame and labelling_ruleB" with "lines 35 and 29" in
  that order, which is right. The log positions `ArcBridge.lean:490:0`-`497:0` are the `#print axioms` lines of
  the current file (497 lines); its hash `46966b48a101...` is recorded in `ENCBLEAN/logs/m5m6_G9rules.log:3`, and
  the file has a single commit. OK.
- The pin of `modelOfLabelling` is at `Audit.lean:45-46` (inside the range 45-49 cited under Rigor and axioms), and
  `modelOfLabelling` uses `labelling_ruleB` (`ModelOfLabelling.lean:30`), which uses `arcFrame`
  (`ArcBridge.lean:480`). OK.
- "depend only on propext, Classical.choice and Quot.sound" is the exact record for all three. No rigor label is
  raised: the claim is about named Lean declarations with cited `#guard_msgs`/`#print axioms` records.

## 4. The fixer's dispositions

| Note | Disposition | Audit judgement |
|---|---|---|
| diff m1 (M7 replacement cited to the log) | fixed | Correct (hunk 4). The replacement is now credited to `mutants.py`, the log only for the name and the error, and the truncation is attributed to the script, which is accurate. |
| diff m2 (no evidence for "Lean-checked counterpart") | fixed | Correct (hunk 5, map row). Every cited line was re-read and says what the text says. |
| referee F1 (rigor sentence covers remarks) | fixed | Correct (hunk 2). Not adopting "labelled as such" is right: pc:rem:alt-boundary and pc:rem:runB-example carry no such label in their own text, and the new wording does not need one. |
| referee F2 (six points asserted unconditionally) | fixed | Correct (hunk 1), with the exact condition and a pointer to the remark that proves it. |
| referee F3 (vendored modules unmentioned) | fixed | Correct (hunk 3, map row), and more complete than the suggested half-sentence. |

No note was declined.

## 5. Findings

None.

## 6. Observations (no finding)

- **O1 (sourcing of "the original file", hunk 3).** The text sources the copy side (VENDOR.sha256, hashes equal to
  the repository files) but leaves implicit that the LEANEXT original is compiled against the repository modules;
  the record for that is `LEANEXT/README.md:6` ("Each file compiles with `lake env lean` from the repository root").
  The claim is true (section 3), and the Sources paragraph's "these are the repository's pins" already points the
  reader there. Optional tightening: add "(the LEANEXT files compile with `lake env lean` from the repository root,
  `LEANEXT/README.md`, line 6)" after "as the original file".
- **O2 (wording, hunk 3).** "The package compiles the copy" refers back to the ENCBLEAN geometric package named in
  Sources; "The ENCBLEAN geometric package compiles the copy" would avoid the backward search. Cosmetic.

## 7. Build

My wrapper `build/pc_docr0audit_wrapper.tex` has the contract content (`\input{../preamble}`,
`\input{../sections/pc}`). I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
pc_docr0audit_wrapper.tex` twice from `build/`:
- both passes exit 0; 13 pages;
- no `!` error, no "Missing", no "Missing character", no multiply defined label, no rerun request;
- **overfull boxes: 0** (so no overfull-box finding);
- 51 underfull boxes, the same as `build/docr0_snapcheck/pc_snap_wrapper.log` (the snapshot with the same
  preamble: 51 underfull, 0 overfull), so the edits cause no layout regression;
- the undefined references are exactly the 14 allowed labels of other sections: fd:def:inv, fd:def:ngon,
  fd:def:orient, fd:def:point, fd:def:rot, fd:lem:orient, lg:def:polar, lg:lem:polar, lg:lem:ruleA, lg:lem:ruleB,
  lg:lem:sinadd, lg:thm:radius, ll:def:hv, ll:def:peel. Both new own references (pc:rem:reading, pc:def:arc)
  resolve.
- I looked at the rendered pages 1, 2, 10 and 11 (`build/pc_docr0audit_pg-*.png`) and the extracted text
  (`build/pc_docr0audit.txt`): every changed passage reads as intended and stays inside the margins.

Other checks on `pc.tex` and `pc.map.tsv`:
- no machine path and no tool name;
- no `\newcommand`, `\renewcommand`, `\def`, `\let`, `\usepackage` or `\begin{document}`;
- no `\lean`/`\dirn` argument contains a space; the new Lean expressions with spaces use `\texttt`
  (`\#guard\_msgs`, `\#print axioms`);
- rigor vocabulary: the edits add no "verified", "certified" or "proved"; the only occurrences in the file are the
  three accepted before (the mathematical "verify the two inequalities", the quoted Lean message, "is not proved in
  LEANEXT").

Evidence files (STAGE): `build/pc_docr0audit_wrapper.{tex,log,pdf}`, `build/pc_docr0audit_pass{1,2}.out`,
`build/pc_docr0audit_check.py`, `build/pc_docr0audit.txt`, `build/pc_docr0audit_pg-{01,02,10,11}.png`.
