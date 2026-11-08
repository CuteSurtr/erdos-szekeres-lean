# ll, round doc-r0: fix log

Input: the two open minor notes of `build/open_minors.json` key `ll` (from `reviews/ll-p1-diff.md` and
`reviews/ll-p1-referee.md`). Snapshot before editing: `snapshots/doc-r0-pre/ll.tex`, `snapshots/doc-r0-pre/ll.map.tsv`.

## Notes

| # | lens | summary | action | location | reason if declined |
|---|---|---|---|---|---|
| 1 | diff | Remark ll:rem:hyp says C6UPPER gives the unsatisfiability of the hexagon encodings with no qualification, while the C7UPPER clause mentions the added symmetry-breaking unit. At (6,8,11), encoder A's certificate covers F_A plus the unit Y(1,2) (32 cubes); only encoder B's base formula is certified alone (64 cubes). | fixed | `sections/ll.tex:720-725` (Remark `ll:rem:hyp`, second paragraph) | - |
| 2 | referee | Same issue (open since ll-p1-diff m1): a reader may infer that no C6UPPER certificate uses symmetry breaking. | fixed | `sections/ll.tex:720-725` (same sentence) | - |

Fix for both notes. The C6UPPER sentence now ends: "... by cake\_lpr verdicts on cube formulas whose cover is checked
there: the formula of encoder~B (`C6UPPER/encb/gen_b2.py`) alone, through $64$ cubes, and that of encoder~A
(`C7UPPER/gen.py`) with an added symmetry-breaking unit clause, through $32$ cubes." The encoders are named after their
generator programs, so the names A and B make sense without the note.

Sources checked (paths relative to RES):
- `C6UPPER/README.md:17-25` (addendum of 6 November: encoder B's base formula UNSAT on its own by 64 cubes; "Encoder A,
  the cross-check, still uses the unit Y(1,2)"), `:40-52`, `:96-102` (encoder A: base + Y(1,2) + 32 patterns; cover
  check `tools/verify_cover.py`).
- `C6UPPER/noty12-2026-11-06/README.md:3-13, 40-53`: the 64 encoder-B cubes are base ± Y(1,2) plus the 2^5 patterns,
  64 cake\_lpr verdicts bound to the hashes; the cover is checked by `verify_cover64.py` and `verify_final64.py` (PASS),
  so "whose cover is checked there" holds for both encoders.
- `WRITEUP/note/k8_soundness.tex:667-669, 697-705` (at (6,8,11) the certificate for B covers F_B alone through 64 cubes;
  the certificate for A covers F_A plus Y(1,2) through 32 cubes; at (7,8,10) A with H(1), B alone).
- `C6UPPER/README.md:34, 44` (encoder A is `C7UPPER/gen.py`, encoder B is `encb/gen_b2.py`); `C7UPPER/README.md:44,
  54-55` (unit H(1) only in `gen.py`; certificate rows "encoder A + H(1)" and "encoder B").

## Other changes

1. `sections/ll.tex:725`, C7UPPER clause: "(one of them with an added symmetry-breaking unit clause)" became
   "(encoder~A's with an added symmetry-breaking unit clause, encoder~B's alone)", parallel to the C6UPPER sentence.
   Sources: `C7UPPER/README.md:44, 54-55`; `WRITEUP/note/k8_soundness.tex:701-702`.
2. `sections/ll.tex:731`: "the angular part of one encoder rests on binary64 floating-point arithmetic" became "the
   angular part of encoder~A ...". Source: gap (G3), `WRITEUP/note/k8_soundness.tex:1013` ("Encoder A's angular part
   rests on binary64 arithmetic"), and `:687`.
3. `sections/ll.tex:736`: "a Lean definition of one encoder's formula (EncB.encB)" became "a Lean definition of
   encoder~B's formula (EncB.encB)". This ties the 64 cubes of `EncB.CubesUnsat64` to the 64 encoder-B cubes named
   above. Sources: `ENCBLEAN/EncB/Coded.lean:329-330` (docstring "Encoder B, functional twin", `def encB`),
   `ENCBLEAN/EncB/Cover.lean:96-110` (`cubeVars64` = Y(1,2), ..., Y(3,4) of `encB 6 8 11`; `CubesUnsat64`),
   `ENCBLEAN/README.md:3-8`, gap (G1) of the note (`:963-965`). The sentence that follows keeps the caveat that the
   identity of the printed texts with the certified cube files is not Lean-checked (trust items (E1)-(E6)).
4. `sections/ll.map.tsv`, row `ll:rem:hyp` (note column only): "(rigor label certificate)" became "(rigor label
   certificate; encoder B's formula alone, encoder A's with a symmetry-breaking unit clause)". The note holds for both
   records. It is ASCII only, and a dry run of `note_tex` from `tools/make_appendix.py` formats it without error
   (`appendix_map.tex` was not regenerated). Labels, kinds, Lean names and file:line columns are unchanged.

No statement corresponding to a Lean declaration was edited. The Lean names in the edited paragraph were re-read
before and after the edit and are unchanged and existing: `EncB.encB` (`ENCBLEAN/EncB/Coded.lean:330`, namespace
`EncB`), `EncB.CubesUnsat64` (`ENCBLEAN/EncB/Cover.lean:110`), `EncB.Geo.sixfold66_of_cubes64`
(`ENCBLEAN/geo/ES8Geo/Main.lean:91`, namespace `EncB.Geo`). The set of labels is unchanged, and the 31 statement
environments match the 31 map rows.

## Compile check

`build/ll_wrapper.tex`, compiled twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`:
- Both passes exit 0, with 0 errors and 0 overfull boxes.
- The 51 underfull hbox warnings are the same count as a compile of the pre-edit snapshot (`build/docr0_pre/`). All are
  in statement heads, and none is in the edited paragraph.
- Undefined references are only to other sections' labels: fd:def:cp, fd:def:gp, fd:def:inv, fd:def:ngon,
  fd:def:point, fd:def:rot, fd:lem:affine-cp, fd:lem:collinear, fd:lem:cp-hull, fd:lem:mono, lg:lem:centre,
  lg:thm:nesting.
- The rendered paragraph was read with pdftotext: the paths break at "/", and no line is overfull.

Hygiene: no machine paths or tool names in `sections/ll.tex` or `sections/ll.map.tsv`, and no "verified", "certified"
or "proved" in the added text.
