# lg, round doc-r0: fix log

Files: `sections/lg.tex` (945 lines after the fix, was 940) and `sections/lg.map.tsv` (31 rows, unchanged).
Snapshot before editing: `snapshots/doc-r0-pre/lg.tex`, `snapshots/doc-r0-pre/lg.map.tsv`.
Paths below are relative to STAGE (`sections/`, `reviews/`, `build/`), to RES (`LAYERLEAN/...`, `WRITEUP/...`) or to
the repository root. Line numbers refer to `sections/lg.tex` after the fix.

Inputs read: the three notes for `lg` in `build/open_minors.json`, from `reviews/lg-p1-diff.md` (m1, m2) and
`reviews/lg-p1-referee.md` (F1). Sources re-read: `WRITEUP/note/k8_soundness.tex` (trust table lines 901-957, gaps
(G1)-(G4) lines 959-1026 with the trust items (E1)-(E6) at 992-1009 inside (G2)), `sections/ll.tex` lines 722-739 (the
wording of the layer-lemma section for the same ENCBLEAN route), `LAYERLEAN/README.md` (lines 97-125, "What is not in Lean" and the status list),
and the Lean declarations of `LAYERLEAN/LayerLemma.lean` that the overview summarises: `strict_nesting` (529),
`centre_not_mem_of_even` (582), `hasConvexNGon_of_fan` (700), `lin_pos_of_peel` (864), `chain_clauses_sound` (914),
`dist2_le_of_later` (1012), plus the polar rules (932-974) to confirm that they have no set `S`.

## Notes

| # | Report and id | Summary | Action | Location after the fix | Reason (declined) / note |
|---|---|---|---|---|---|
| 1 | lg-p1-diff.md m1 | "the certified files" in the paragraph *Encoders* uses a forbidden word and presents the trusted cake_lpr verdicts (trust item (E2)) as settled | fixed | *Encoders*, l. 99-102 | "certified files" replaced by "the 64 cube files that carry the cake_lpr verdicts", the wording of the layer-lemma section as the note suggested (the note cites `sections/ll.tex:735`; the sentence is at `sections/ll.tex:737` in the current file). The section now contains no "certified" and no "verified" (grep). |
| 2 | lg-p1-diff.md m2 | Overview lead "In the main statements, S is ... mapped into itself by rho" is not exact for Theorem lg:thm:fan, whose S has no centre, rotation or invariance | fixed | Overview, l. 4-9 | Now: "In the statements about the layers (Lemmas lg:lem:layer and lg:lem:halfplane, Theorems lg:thm:nesting, lg:thm:radius and lg:thm:chain) and in Lemma lg:lem:centre, S is ... mapped into itself by ... rho by 2pi/m (m >= 1) about a point c; in all of them except Lemma lg:lem:centre, also c not in S and S has no K points in convex position for some K <= 2m. Theorem lg:thm:fan, the only other statement with a set S, involves no centre and no rotation." I named the statements instead of using the suggested "In the statements about the layers" alone because Lemma lg:lem:centre (centre_not_mem_of_even) also has a rotation-invariant S but is not about the layers, and it is the one such statement without `c ∉ S` and K-freeness, so the old "in most of them" became an exact "all except". Checked against Lean: rotation-invariant S with `0 < m` / `2 ≤ m` / `3 ≤ m` in all six; `hc : c ∉ S`, `hK : K ≤ 2 * m` and `hno : ¬ HasConvexNGon K S` in all except centre_not_mem_of_even (`hm`, `heven`, `hinv`, `hgp`, `hp`, `hpc` only; `c ∉ S` is its conclusion); hasConvexNGon_of_fan has binders `S p w q n` only. A script over the statement environments confirms that these seven are exactly the statements that mention S. |
| 3 | lg-p1-referee.md F1 | (1) same "certified" problem as #1; (2) only (E1) is named, although the ENCBLEAN route assumes the 64 cake_lpr verdicts and all of (E1)-(E6); (3, optional) (G1) also trusts the Python interpreter | fixed (all three parts) | *Encoders*, l. 98-102 | (1) as #1 (duplicate of that part). (2) New text: "On that route the note lists, under gap (G2), the trust items (E1)-(E6), which are not Lean-checked: among them, that the texts printed from this definition are the 64 cube files that carry the cake_lpr verdicts is (E1), evidence from running compiled code and not a Lean theorem, and those 64 verdicts and their provenance are covered by (E2)." This matches the note: k8_soundness.tex lists (E1)-(E6) inside (G2) under "Not Lean-checked, and trusted on this route"; (E1) is the hash binding of the printed texts to the base formula and the 64 cube files ("evidence from running compiled code, not a Lean theorem"); (E2) is the 64 hash-bound cake_lpr verdicts, the provenance of the binary and the records tying verdicts to file hashes. I did not use the suggested "assumes those 64 verdicts and the trust items (E2)-(E6)" verbatim because (E2) is the verdicts themselves, so listing both would count them twice. (3) Added after "by reading the code": "with the Python interpreter trusted to run the programs as written", which is the wording of (G1) in the note ("the Python interpreter is trusted to run them as written"). |

## Other changes

None. No statement environment, label, `\leanref`, proof or map row changed (checked: the statement environments and
the sorted label lists of the snapshot and the new file are identical; `lg.map.tsv` is byte-identical to the
snapshot). The only edits are the two passages above (overview lead, l. 4-9; *Encoders*, l. 98-102). No macro or
package was added.

## Checks

- Compile: `build/lg_wrapper.tex`, two runs of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
  lg_wrapper.tex` from `build/`: exit 0 and 0; no line starting with "!"; no "Missing", "Error" or "Emergency";
  12 pages; overfull boxes: none (so none > 1pt); one page-level underfull `\vbox` (output routine), as in the
  earlier reports; no multiply defined label.
- Undefined references only to export labels of other sections: fd:def:cp, fd:def:gp, fd:def:inv, fd:def:ngon,
  fd:def:orient, fd:def:point, fd:def:rot, fd:lem:collinear, fd:lem:mono, fd:lem:orient, fd:lem:pos-triples,
  ll:def:hv, ll:def:peel, ll:lem:antitone, ll:lem:hv, ll:lem:inv-peel, ll:lem:minperiod, ll:thm:card-peel,
  ll:thm:core-rot. The new `\ref`s in the overview (lg:lem:layer, lg:lem:halfplane, lg:thm:nesting, lg:thm:radius,
  lg:thm:chain, lg:lem:centre, lg:thm:fan) are labels of this section and resolve (rendered as Lemmas 1.1 and 1.30,
  Theorems 1.16, 1.20 and 1.32, Lemma 1.18, Theorem 1.28).
- Hygiene: no machine path and no tool name in `lg.tex` or `lg.map.tsv`; "certified" and "verified" do
  not occur; "proved" occurs only for the written proofs of this document (l. 81, 93, 779, 844 and two map notes; l. 75 has
  "unproved proposition");
  no `\newcommand`, `\def`, `\usepackage` or `\sloppy`.
