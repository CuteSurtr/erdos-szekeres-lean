# Section `ll`, round doc-r0: diff audit

Inputs: `snapshots/doc-r0-pre/ll.tex` (792 lines) and `snapshots/doc-r0-pre/ll.map.tsv` against `sections/ll.tex`
(794 lines) and `sections/ll.map.tsv`; fixer log `reviews/ll-doc-r0-fix.md`; the notes it addressed, m1 of
`reviews/ll-p1-diff.md` and m1 of `reviews/ll-p1-referee.md`. Paths below are relative to the staging directory
(`sections/`, `build/`, `reviews/`), to RES (`C6UPPER/...`, `LAYERLEAN/...`) or to the repository root
(`ErdosSzekeres/...`).

**Verdict: PASS.** No blocker, no major and no minor finding. Every hunk is correct. Both notes marked fixed are
fixed. No note was declined. Every new claim about records and Lean files checks out against the files under RES.
No statement that corresponds to a Lean declaration was touched. The compile is clean (0 overfull boxes).

## 1. Method

- `diff -u` of both file pairs. `ll.tex` has one hunk (snapshot 718-737, now 718-739) inside Remark `ll:rem:hyp`,
  second paragraph. It makes four textual changes, at current lines 721-725, 731 and 736. `ll.map.tsv` has one
  changed row (`ll:rem:hyp`, note column only).
- Records opened (relative to RES):
  - `C6UPPER/`: `README.md` (all), `SHA256SUMS.txt`, `logs/{verify_cover.log, encb_verify_cover.log, encb_gen.log}`.
  - `C6UPPER/replay-2026-11-06/`: `{results.tsv, verify_cover_A.log, verify_cover_B.log, SUMMARY.txt}`.
  - `C6UPPER/noty12-2026-11-06/`: `{README.md, results.tsv, verify_cover64.log, verify_final64.log, SUMMARY.txt}`.
  - `C7UPPER/`: `{README.md, SHA256SUMS.txt, addunits.py, logs/cake_A.out, logs/cake_B.out}`.
  - `WRITEUP/note/k8_soundness.tex`: lines 650-720 (reflection unit, soundness theorem, certified instances), 814-854
    (cube cover) and 940-1037 (trust table, (G1)-(G4), (E1)-(E6)).
  - `ENCBLEAN/README.md:1-40`, `ENCBLEAN/EncB/Coded.lean:315-345`, `ENCBLEAN/EncB/Cover.lean:85-115`,
    `ENCBLEAN/geo/ES8Geo/Main.lean:1-100`, `ENCBLEAN/geo/ES8Geo/Audit.lean` (the `#check` and `#print axioms` lines).
- Lean: `LAYERLEAN/LayerLemma.lean` lines 1096-1148, re-read. SHA-256 `afb8542dceb0c170...`, recomputed.
- Scripted checks:
  - label, `\ref` and `\leanref` sets of old against new file; map columns 1-4 of old against new;
  - field counts of the map; statement environments against map rows;
  - forbidden strings; ASCII check and a dry run of `note_tex` from `tools/make_appendix.py` on the edited row
    (`appendix_map.tex` not written);
  - a grep of every `.lean` file of the repository for `Sixfold66` and `Sevenfold70`;
  - `diff` of `LayerLemma.lean` 37-1147 against `ENCBLEAN/geo/ES8Geo/Capstone2.lean` 45-1155;
  - SHA-256 of both copies of `ErdosSzekeres/Definitions.lean`.
- Compile: own wrapper `build/ll_docr0audit_wrapper.tex` (contract content), built twice. Pages 9-10 of the PDF
  (the whole remark) were rendered and inspected.

## 2. Hunk by hunk (current line numbers)

| # | lines | change | result |
|---|---|---|---|
| 1 | 720-723 | C6UPPER sentence now ends "...whose cover is checked there: the formula of encoder B (`C6UPPER/encb/gen_b2.py`) alone, through 64 cubes, and that of encoder A (`C7UPPER/gen.py`) with an added symmetry-breaking unit clause, through 32 cubes." | correct, see 3(a)-(d) |
| 2 | 723-725 | C7UPPER parenthetical "(one of them with an added symmetry-breaking unit clause)" became "(encoder A's with an added symmetry-breaking unit clause, encoder B's alone)" | correct, see 3(e) |
| 3 | 731 | gap (G3): "the angular part of one encoder" became "the angular part of encoder A" | correct: `k8_soundness.tex:1013` "Encoder A's angular part rests on binary64 arithmetic"; `:687-690` (A classifies triples in binary64, B uses only integer comparisons) |
| 4 | 736 | "a Lean definition of one encoder's formula (`EncB.encB`)" became "...of encoder B's formula (`EncB.encB`)" | correct, see 3(f) |
| tsv | row `ll:rem:hyp` | note: "(rigor label certificate)" became "(rigor label certificate; encoder B's formula alone, encoder A's with a symmetry-breaking unit clause)" | correct for both records (3(a)-(e)). ASCII only, 5 fields. The `note_tex` dry run formats it without error. |

## 3. Record claims of the new text (all confirmed)

(a) **Encoder names and programs.**
- `C6UPPER/README.md:34` names the encoding `C7UPPER/gen.py`, and `:281` says "A: `C7UPPER/gen.py 6 8 11`".
- `:44` and `:136` say that encoder B is `encb/gen_b2.py`, the C7UPPER encoder B (`C7UPPER/gen_b.py`) extended to
  even m. `:281` says "B: `encb/gen_b2.py 6 8 11`".
- Both files exist at the cited paths, relative to RES.

(b) **Encoder B alone, 64 cubes, cake_lpr.**
- The base formula is `B_m6K8t11.cnf`, `479e31a9...` (`C6UPPER/SHA256SUMS.txt:86`).
- The 32 cubes base + Y(1,2) + pattern were accepted in the hash-bound replay. `replay-2026-11-06/results.tsv` has
  32 rows "B ACCEPTED s VERIFIED UNSAT".
- The 32 cubes base + ¬Y(1,2) + pattern were accepted in `noty12-2026-11-06/results.tsv`: 32 rows "ACCEPTED s VERIFIED
  UNSAT".
- `noty12-2026-11-06/README.md:3-13` and `C6UPPER/README.md:17-25, 42-43, 51-52, 326-336` state that the 64 cubes carry
  all 2^6 sign patterns of Y(1,2), ..., Y(3,4), so encoder B's base formula is unsatisfiable without the unit.

(c) **Encoder A with the unit, 32 cubes, cake_lpr.**
- The base formula is `542c8a3a...` (`C6UPPER/SHA256SUMS.txt:10`), and the unit Y(1,2) is variable 7635
  (`C6UPPER/README.md:96-100`).
- `replay-2026-11-06/results.tsv` has 32 rows "A ACCEPTED s VERIFIED UNSAT".
- `C6UPPER/README.md:23` and `:42-43` say encoder A still uses the unit Y(1,2).

(d) **"whose cover is checked there" now applies to both splits, and holds for both.**
- Encoder A: `logs/verify_cover.log` and `replay-2026-11-06/verify_cover_A.log` both read "OK: 32 distinct cubes,
  each = base + Y(1,2) + pattern; cover complete".
- Encoder B: `noty12-2026-11-06/verify_cover64.log` reads "64 distinct patterns on 6 variables; cover complete", and
  `noty12-2026-11-06/verify_final64.log` reads "PASS: ... cover all 2^6 assignments ...: B_m6K8t11.cnf (sha
  479e31a9e8d5...) is UNSAT".
- All of these are inside the C6UPPER record.

(e) **C7UPPER.**
- `C7UPPER/README.md:44`: "Symmetry breaking (`gen.py` only) ... the unit H(1)". `:47`: `gen_b.py` has "no symmetry
  breaking beyond theta_0 = 0". theta_0 = 0 is a normalisation built into both encodings, not an added clause.
- The certificate table (`:52-55`) has "encoder A + H(1)" (`fa297b5b...`, made by `addunits.py` from base
  `1a7c0e70...`) and "encoder B" (`b4d29017...`). Both are "VERIFIED UNSAT" by cake_lpr (`logs/cake_A.out`,
  `logs/cake_B.out`: `s VERIFIED UNSAT`).
- `k8_soundness.tex:701-702` agrees: "The sevenfold certificate for A is for F_A plus H(1) ...; the one for B is for
  F_B alone".
- The cross-record name "encoder B" is sound. At m = 7 the certified file was written by `C7UPPER/gen_b.py`, but
  `gen_b2.py 7 8 10` reproduces it byte for byte (`C6UPPER/logs/encb_gen.log:1-3, 10`; `C6UPPER/README.md:157-158`).
- `k8_soundness.tex:674` defines F_B as the output of `gen_b2.py`, and `:699-700` gives `b4d29017...` as F_B at
  (7,8,10).

(f) **`EncB.encB` as "a Lean definition of encoder B's formula".**
- The project uses these words:
  - `ENCBLEAN/README.md:3-8`: `EncB.gen` is "a Lean definition of the CNF that `C6UPPER/encb/gen_b2.py` writes", and
    `EncB.encB` is "a second definition of the same CNF";
  - `ENCBLEAN/EncB/Coded.lean:329-330`: docstring "Encoder B, functional twin", `def encB`, namespace `EncB` (line 36);
  - `k8_soundness.tex:78` and (G1) at `:963-965`: "a Lean definition of its formula, `EncB.encB`".
- Its equality with the output of `gen_b2.py` is not proved; it was checked by running compiled code (G1, `:973-976`).
  On the ENCBLEAN route, the text's next sentence already says the tie to the certified files is not Lean-checked:
  "Neither the identity of the printed texts of these formulas with the cube files that carry the cake_lpr verdicts
  ... is Lean-checked; both rest on (E1)-(E6)".
- `EncB.CubesUnsat64` (`ENCBLEAN/EncB/Cover.lean:110`) is `∀ c ∈ cubes64, ¬DimacsSatisfiable (cubeCnf (encB 6 8 11)
  c)`. `cubeVars64 = [1, 2, 3, 10, 11, 18]` are the variables of the record's 64 encoder-B cubes (`:96-101`), and
  `length_cubes64` gives 64.
- `EncB.Geo.sixfold66_of_cubes64 (h : EncB.CubesUnsat64) : Sixfold66` is at `ENCBLEAN/geo/ES8Geo/Main.lean:91`
  (namespace `EncB.Geo`, line 24). `Audit.lean:99-100` checks its type.

**Rest of the touched paragraph (unchanged text, re-checked).**
- The `.lean` grep finds only three theorems concluding `Sixfold66`, at `ENCBLEAN/geo/ES8Geo/Main.lean:78, 87, 91`,
  each with a hypothesis. No theorem concludes `Sevenfold70`.
- `Capstone2.lean` 45-1155 equals `LayerLemma.lean` 37-1147 (empty diff).
- Both `Definitions.lean` copies have SHA-256 `2425500eefd181ad...`.
- The k8 note covers the symmetry breaking (`k8s:lem:refl`, `:644`) and both cube covers (`k8s:sec:cube`,
  `:814-854`).

**Rigor.**
- The added text uses none of "verified", "certified" or "proved".
- Only cake_lpr verdicts are cited; lrat-check is not mentioned.
- The unsatisfiability results keep the label *certificate*.
- The soundness step stays a written proof (not refereed) with gaps (G1)-(G4).
- No hypothesis is presented as proved.

## 4. Notes addressed by the fixer

| note | status in log | audit |
|---|---|---|
| `ll-p1-diff.md` m1: the C6UPPER clause had no qualification, while the C7UPPER clause mentioned the unit | fixed | **Fixed.** Lines 721-723 now say what each C6UPPER certificate covers: B alone through 64 cubes; A plus the unit through 32 cubes. This is the content the note asked for, with program paths added. |
| `ll-p1-referee.md` m1: the same issue | fixed | **Fixed** (same edit) |

No note was declined. The fixer's "other changes" 1-4 (C7UPPER parenthetical, (G3) wording, `EncB.encB` wording,
map note) are the hunks 2, 3, 4 and tsv above, all correct. The log's source citations (`C6UPPER/README.md:17-25,
34, 40-52, 44, 96-102`; `noty12-2026-11-06/README.md:3-13, 40-53`; `k8_soundness.tex:667-669, 687, 697-705, 963-965,
1013`; `C7UPPER/README.md:44, 54-55`; `Coded.lean:329-330`; `Cover.lean:96-110`; `Main.lean:91`) point to the stated
content.

## 5. Statements and Lean declarations

- No statement environment corresponding to a Lean declaration was edited. The only touched environment is Remark
  `ll:rem:hyp`, a written remark with map row `-`/`-`.
- Re-read against `LAYERLEAN/LayerLemma.lean`:
  - `Sixfold66` (1102) and `Sevenfold70` (1107);
  - `sixfold_octagon` (1113) and `sevenfold_octagon` (1136).
- They are unchanged, and the section's Definition `ll:def:66-70` and Theorems `ll:thm:sixfold` and `ll:thm:sevenfold`
  still match them.
- The label set, the `\ref` set and the `\leanref` list are identical to the snapshot.
- Map columns 1-4 are identical to the snapshot.
- There are 31 statement environments for 31 map rows, and every row has 5 fields.

## 6. Compile check

`build/ll_docr0audit_wrapper.tex` (contract content: amsart 10pt, `\input{../preamble}`, `\input{../sections/ll}`),
from `build/`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice:
- **Exit codes.** Pass 1 and pass 2 both exit 0, producing 10 pages.
- **Clean log.** There is no `!` line, no "Missing", no undefined control sequence, no "Label(s) may have changed"
  and no hyperref "Token not allowed".
- **Undefined references.** Only the ten allowed `fd:` labels (`fd:def:{cp,gp,inv,ngon,point,rot}`,
  `fd:lem:{affine-cp,collinear,cp-hull,mono}`) and the `lg:` export labels `lg:lem:centre` and `lg:thm:nesting`.
- **Overfull boxes.** 0 of any size, so there is no minor finding of this kind.
- **Underfull boxes.**
  - There are 51, in paragraphs at source lines 112-114 through 759 ff.
  - None is in the edited paragraph (lines 719-739).
  - The count equals that of the fixer's pre-edit build (`build/docr0_pre/pre_wrapper.log`: 51 underfull,
    0 overfull).
- **Rendering.** The `pdftotext` text of my PDF is identical to that of the fixer's `build/ll_wrapper.pdf`. On pages
  9-10 the remark renders cleanly: the `\dirn` paths `C6UPPER/encb/gen_b2.py` and `C7UPPER/gen.py` print whole,
  with no clipping and no visibly loose line.

Hygiene: `sections/ll.tex` and `sections/ll.map.tsv` contain no machine path and none of the forbidden names. They
contain no `\newcommand`, `\usepackage`, `\def` or `\sloppy`. The fixer's log is also free of forbidden strings.

## 7. Checked, not findings

- The C7UPPER clause uses "encoder B" for the program that wrote the m = 7 file, `C7UPPER/gen_b.py`. Its output is
  reproduced byte for byte by `C6UPPER/encb/gen_b2.py`, the program the text names (3(e)). The k8 note uses the same
  identification. This is accurate.
- "A Lean definition of encoder B's formula" matches the project's wording. The fact that the definition's agreement
  with `gen_b2.py` is evidence only is covered by the caveat in the next sentence and by (E1) (3(f)). The pre-edit text
  ("one encoder's formula") made the same kind of claim and passed the polish audits.
- The fixer's log says that in the rendered paragraph "the paths break at '/'". In the actual layout, no path in that
  paragraph is split across lines. This remark concerns only the log, not the section. The log's other compile
  claims are confirmed: exit 0 twice, 0 overfull, 51 underfull equal to the pre-edit count, and the listed undefined
  references.

## 8. Findings

None.
