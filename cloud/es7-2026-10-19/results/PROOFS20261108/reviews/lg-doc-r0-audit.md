# Section `lg`, round doc-r0: diff audit

Lens: diff. Inputs:
- the pre-round snapshot `snapshots/doc-r0-pre/lg.tex` (940 lines) and `lg.map.tsv`;
- the current `sections/lg.tex` (945 lines) and `lg.map.tsv` (32 lines: header + 31 rows);
- the fix log `reviews/lg-doc-r0-fix.md`;
- the notes it addressed: `reviews/lg-p1-diff.md` (m1, m2) and `reviews/lg-p1-referee.md` (F1), which are the
  three `lg` entries of `build/open_minors.json`.

Paths below are relative to STAGE (`sections/`, `reviews/`, `build/`), to RES (`LAYERLEAN/...`, `WRITEUP/...`,
`ENCBLEAN`) or to the repository root. "LL" is `LAYERLEAN/LayerLemma.lean` (1148 lines, SHA-256 afb8542dceb0...,
recomputed).

**Verdict: pass.**
- No blocker, no major, no minor finding.
- All three notes are fixed, and the fixes are correct. No note was declined.
- `lg.map.tsv` is byte-identical to the snapshot (`cmp`). No statement environment, label, `\leanref`, proof or map row
  changed.
- Build clean: both runs exit 0, no error, no overfull box.

## 1. Hunks checked (`diff -u`: tex 2 hunks, tsv none)

| # | Current lines | Change | Check |
|---|---|---|---|
| 1 | 4-9 (overview lead) | "In the main statements, S is ... (m >= 1) about a point c, and in most of them c not in S and S has no K points in convex position for some K <= 2m" is replaced by: in the statements about the layers (Lemmas lg:lem:layer and lg:lem:halfplane, Theorems lg:thm:nesting, lg:thm:radius and lg:thm:chain) and in Lemma lg:lem:centre, S is finite and mapped into itself by rho = rotAbout(c, 2pi/m), m >= 1. In all of them except lg:lem:centre, also c not in S and S has no K points in convex position for some K <= 2m. Theorem lg:thm:fan, "the only other statement with a set S", involves no centre and no rotation. | Re-read in LL. `strict_nesting` (529): `2 ≤ m`, `K ≤ 2 * m`, `c ∉ S`, `Invariant`, `¬ HasConvexNGon K S`, GP. `centre_not_mem_of_even` (582): `0 < m`, `Even m`, `Invariant`, GP, `p ∈ S`, `p ≠ c`, with `c ∉ S` as its conclusion; no K and no `c ∉ S` hypothesis. `dist2_le_of_later` (1012): `0 < m`, `K ≤ 2 * m`, `c ∉ S`, `Invariant`, `¬ HasConvexNGon K S`. `lin_pos_of_peel` (864): `3 ≤ m` plus the same four hypotheses and GP. `chain_clauses_sound` (914): `3 ≤ m`, `4 ≤ K`, the same four, GP. `hasConvexNGon_of_fan` (700): binders `S p w q n` only. Written step lg:lem:layer (lg.tex:195): `0 < m`, `K ≤ 2m`, `c ∉ S`, rho maps S into S, K-free. In all six, S is a `Finset`. So every clause of the new sentence is exact, and "m ≥ 1" is a common lower bound. I checked the claim "only other statement with a set S" with my own script over the statement environments (`build/lg_docr0audit_envS.py`). Among the 31 non-remark environments, exactly these seven mention S in math. Two remarks mention S: the one after nesting and the one after the centre lemma, which discusses S = {c}. Both concern the S of the statement they follow, and remarks are not statements here (the map lists none). The environment words match the label kinds (Lemma/Theorem). The seven new `\ref`s are lg labels and resolve to Lemmas 1.1 and 1.30, Theorems 1.16, 1.20 and 1.32, Lemma 1.18 and Theorem 1.28 (PDF page 1). OK |
| 2 | 97-102 (paragraph *Encoders*) | (a) after "by reading the code": ", with the Python interpreter trusted to run the programs as written"; (b) "(ENCBLEAN); on that route, that the texts printed from this definition are the certified files is trust item (E1), evidence ..." is replaced by "(ENCBLEAN). On that route the note lists, under gap (G2), the trust items (E1)--(E6), which are not Lean-checked: among them, that the texts printed from this definition are the 64 cube files that carry the cake_lpr verdicts is (E1), evidence from running compiled code and not a Lean theorem, and those 64 verdicts and their provenance are covered by (E2)." | Checked in `WRITEUP/note/k8_soundness.tex` (1037 lines). (a) (G1), l. 961-963: "the Python interpreter is trusted to run them as written"; the trust table, l. 923-924, says "written proof (not refereed) by reading the source". (b) (G2), l. 985-1009: the route is formalized "up to the trust items (E1)--(E6) below", and l. 990-991 say "Not Lean-checked, and trusted on this route". (E1), l. 993-995: "that these 64 texts are the certified cube files: the SHA-256 of the output of the compiled printer equals the record for the base formula and for all 64 cube files ...; evidence from running compiled code, not a Lean theorem". (E2), l. 996-999: "the 64 hash-bound cake_lpr verdicts ... and the provenance of the cake_lpr binary that gave them", plus the records that tie verdicts to file hashes. (G1), l. 975-978, also says the Lean route replaces (G1) "by the trust items of (G2)". Every claim of the new text is in the note. The text says "Lean-checked" only for the Lean part of the route, as the note does; it presents no verdict as proved; "certified" and "verified" are gone; the SAT anchor is cake_lpr. The wording "cube files that carry the cake_lpr verdicts" is the same as `sections/ll.tex:737`, so the two sections agree. The text leaves out (E1)'s hash binding of the base formula, but it names all six items as trust items and says "among them", so this is not an inaccuracy. OK |

## 2. Statements re-compared with Lean

No statement environment changed: the diff touches only lines 4-9 and 97-102, both outside any environment.
Because hunk 1 makes claims about seven statements, I re-read their text in `sections/lg.tex` and their Lean source:
- lg:lem:layer, l. 195;
- lg:thm:nesting, l. 443, against LL:529;
- lg:lem:centre, l. 490, against LL:582;
- lg:thm:radius, l. 515, against LL:1012;
- lg:thm:fan, l. 673, against LL:700;
- lg:lem:halfplane, l. 710, against LL:864;
- lg:thm:chain, l. 760, against LL:914.

Each still matches its declaration exactly on:
- hypotheses, including `2 ≤ m`, `3 ≤ m`, `4 ≤ K`, `K - 1`, maps-into and `Finset`;
- conclusion, including `False` for the chain theorem;
- binder order.

## 3. The notes

| Note | Status in the fix log | Audit |
|---|---|---|
| lg-p1-diff m1 ("certified files" in *Encoders*) | fixed | Confirmed. "certified" no longer occurs anywhere in `lg.tex` or `lg.map.tsv` (grep). The replacement is the layer-lemma section's wording, and the cake_lpr verdicts are now explicitly a trust item, (E2). |
| lg-p1-diff m2 (overview "In the main statements" does not fit lg:thm:fan) | fixed | Confirmed (hunk 1). Naming the statements instead of the suggested "In the statements about the layers" is justified: lg:lem:centre has a rotation-invariant S but is not about the layers, and it is the one such statement without `c ∉ S` and K-freeness. The old "in most of them" is now an exact "all except". |
| lg-p1-referee F1 (1) "certified"; (2) only (E1) named; (3, optional) Python interpreter in (G1) | fixed (all three parts) | Confirmed. (1) As m1. (2) All of (E1)-(E6) are now named as trust items that are not Lean-checked, with the verdicts explicitly under (E2). The fixer's reason for not using the suggested "(E2)-(E6)" phrasing, which would count the verdicts twice, is correct. (3) Added with the note's own wording. |

No note was declined.

Other claims in the fix log, re-checked:
- k8 note line ranges: trust table 901-957, gaps 959-1026, (E1)-(E6) at 992-1009 (grep).
- `sections/ll.tex:737` holds the borrowed wording.
- `lg.tex` grew from 940 to 945 lines.
- The map is byte-identical to the snapshot.
- "proved" occurs only at l. 81, 93, 779 and 844 and in two map notes, plus "unproved" at l. 75. My grep also matches "provenance" at l. 102, which is not a use of "proved".
- The undefined-reference list is as stated.

## 4. Compile check

I built my own wrapper, `build/lg_docr0audit_wrapper.tex`, with the contract's content (`\input{../preamble}`,
`\input{../sections/lg}`). I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
lg_docr0audit_wrapper.tex` twice from `build/`:
- Exit status 0 and 0, 12 pages.
- No line starting with "!". No "Missing", "Error", "Emergency", "Runaway" or "Undefined control".
- No overfull box, so none over 1pt.
- One underfull `\vbox` while `\output` is active. This comes from the page breaking of the standalone build, not from a box overflow, and it was present in the earlier rounds.
- No multiply defined label.
- Undefined references only to allowed export labels:
  - fd:def:cp, fd:def:gp, fd:def:inv, fd:def:ngon, fd:def:orient, fd:def:point, fd:def:rot;
  - fd:lem:collinear, fd:lem:mono, fd:lem:orient, fd:lem:pos-triples;
  - ll:def:hv, ll:def:peel, ll:lem:antitone, ll:lem:hv, ll:lem:inv-peel, ll:lem:minperiod, ll:thm:card-peel,
    ll:thm:core-rot.

  There is no undefined `lg:` reference.
- Rendering of the two changed passages (pages 1-2, checked as images): references resolve. "cake_lpr", "(E1)–(E6)"
  and the `\notin` signs print correctly, and no line overflows.

## 5. Hygiene

- No machine path (/private, /Users, /home, /tmp) and no tool name in `lg.tex` or `lg.map.tsv` (grep,
  case-insensitive). "Python" names the language of the encoder programs, as in the k = 8 note.
- No `\newcommand`, `\renewcommand`, `\def`, `\usepackage`, `\sloppy` or `\makeatletter`.
- Both files are ASCII only.

## 6. Findings

None.
