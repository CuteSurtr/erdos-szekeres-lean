# Final pass, round 1: fixes for section sa

Files edited: `sections/sa.tex`, `sections/sa.map.tsv`. Snapshot before editing: `snapshots/final-r1-pre/sa.tex`,
`snapshots/final-r1-pre/sa.map.tsv`. Labels unchanged (the list of `\label{...}` is identical before and after). No
statement environment was changed. I re-read the Lean statements in the sources: `AUDIT3/A1_reduction/SizeArith.lean`
lines 61-80, `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean` lines 6-27,
`SYMLEAN/review/VariantChecks.lean` lines 1116-1306, and `LEANEXT/es7corr/ES7Corollaries.lean` lines 1-12 and
1148-1233. Propositions sa:prop:table and sa:prop:assembled and Lemma sa:lem:big-order still match Lean exactly.

Six findings, six fixed, none declined.

## Finding 1 (minor): the hypotheses of the table statements. Fixed.

Checked against `SizeArith.lean` lines 61-80. `table_c3` (k <= 10), `table_c4` (k <= 7) and `table_c2` (k <= 16) bound
k. `table_c4_only_c2` (2*k <= 16) and `table_c6` (2*k <= 10) bound 2k. `table_c5` (5*k + e < 35) bounds 5k+e.
`table_mirror` bounds k separately for b = 0 and for 1 <= b. `c3_no32` and `c5_gap` have only `he : e <= 1`. The
finding is right.

Location: sa.tex, introduction of Subsection sa:ssec:table (old lines 231-232, now 233-237).

Old: "... are not part of the statements: each statement assumes the bound on $k$ as a hypothesis
(Remark~\ref{sa:rem:use}, item~(5))."

New: "... are not part of the statements: each part of Proposition~\ref{sa:prop:table} that rests on a case theorem
assumes the bound that the theorem gives as a hypothesis, on $k$ in parts (a), (e) and~(h), on $2k$ in parts (f)
and~(g), on $5k+e$ in part~(c), and on $k$, separately for $b=0$ and for $1\le b$, in part~(i)
(Remark~\ref{sa:rem:use}, item~(5)). Parts (b) and~(d), \lean{A1.c3_no32} and \lean{A1.c5_gap}, rest on no case
theorem: their only hypothesis is $e\le1$."

Map, row sa:prop:table, note. Old: "linear arithmetic over N (omega in Lean); the bounds on k from the case classes are
hypotheses, not part of the statements". New: "linear arithmetic over N (omega in Lean); the bounds that the case
theorems give are hypotheses, not part of the statements: on k in table_c3, table_c4, table_c2; on 2k in
table_c4_only_c2, table_c6; on 5k+e in table_c5; on k for b = 0 and for 1 <= b in table_mirror; c3_no32 and c5_gap
assume only e <= 1".

## Finding 2 (minor): item (5) of Remark sa:rem:use drops n >= 33. Fixed.

I checked every claim of the added sentence against Lemma sa:lem:model, items (1)-(2) and the class definitions
(`SYMLEAN/SymmetricReduction.lean` lines 467-500):
- The size table is about sets of any size, so the standing hypothesis 33 <= n does not hold there.
- The subsets T of items (1)-(2) need only the count, not 33 <= n. If the count reaches what a class needs, T satisfies
  every hypothesis of the class: 11 orbits for Threefold33, 7 for Fivefold35, 8 for Fourfold32, 17 pairs for
  HalfTurn34 and MirrorNoAxis34 (b = 0), 16 pairs plus one axis point for MirrorOneAxis33 (b >= 1). T is in general
  position, has the exact size, avoids c and is invariant (Lemma sa:lem:model(c)); the mirror pairs avoid L. The class
  then gives HasConvexNGon 7 T, hence HasConvexNGon 7 S.
- The count is k, except for rho^[2] when s = 4 (2k half-turn pairs) and s = 6 (2k threefold orbits). In both cases
  n = s*k + e = m*k' + e with the same e, so k' = 2k. The sentence states this explicitly ("$k$, or $2k$ for
  $\rho^{[2]}$ when $s=4$ or $s=6$") instead of the suggested "if $k$ reached".
- For even s, k >= 1 gives a point of S other than c, so e = 0 by Lemma sa:lem:model(a). k = 0 gives n = e <= 1. Parts
  (e)-(h) bound s*k, so they need n = s*k, that is, e = 0.

Location: sa.tex, Remark sa:rem:use, item (5), after "... turn these bounds into bounds on $n$." (now lines 578-582).

Old: (no sentence)

New: "Here $S$ need not have $33$ points: if the number of orbits or pairs to which a class is applied below ($k$, or
$2k$ for $\rho^{[2]}$ when $s=4$ or $s=6$) reached the number that the class requires, the subset $T$ built in
item~(1) or~(2) would satisfy the hypotheses of the class, which would then give $7$ points of $S$ in convex
position; for even $s$, $e=0$ as soon as $k\ge1$ (Lemma~\ref{sa:lem:model}(a)), and $k=0$ gives $n=e\le1$."

Changes to the suggested wording: the count is "$k$, or $2k$ ..." instead of "$k$". The consequence of the class
(7 points of S in convex position) is stated. The reference for e = 0 is added, and $n\le1$ is written as
$n=e\le1$. Map: no change needed; the note of sa:rem:use stays true.

## Finding 3 (minor): uses of Fourfold32 outside this document. Fixed, with an adjusted wording.

Checked `SYMLEAN/review/VariantChecks.lean`. Lines 1-1058 are a copy of `SymmetricReduction.lean` (banner at 1060).
`group_form` is at line 1168 and takes `(h4 : Fourfold32)` at line 1169. Its axioms are printed in
`SYMLEAN/logs/VariantChecks.out` line 15, and Remark sr:rem:variant calls it Lean-checked. The file has other checks of
the variant that also use the class:
- `fourfold36_of_fourfold32` (line 1220) takes `(h4 : Fourfold32)`;
- `variant_unfolded` (line 1116) takes the class with its definitions unfolded;
- `variant_with_fourfold36` (line 1275) uses `Fourfold36` instead.
So a parenthetical that names only `group_form` would be true but incomplete. I wrote "some checks ..., among them its
group form" so that it does not suggest that `group_form` is the only one.

Location: sa.tex, Remark sa:rem:use, item (1), bullet s = 4 (old lines 516-518, now 521-525).

Old: "Among the reduction theorems only Theorem~\ref{sr:thm:variant} uses this class; a same-text copy, ..."

New: "Among the reduction theorems stated in this document, only Theorem~\ref{sr:thm:variant} uses this class (so do
some checks of that theorem in the review file \dirn{SYMLEAN/review/VariantChecks.lean}, among them its group form
\lean{VariantChecks.group_form}); a same-text copy, ..."

Map: no change needed.

## Finding 4 (minor): big_order_orbit gives at least one orbit. Fixed.

Checked `AssembledSizes.lean` line 24. The conclusion is `1 <= k`, where k counts the non-central orbits (comment at
line 23: "at least one non-central orbit").

Location: sa.tex line 23.

Old: "that an order of at least $7$ gives one orbit (\lean{big_order_orbit})"

New: "that an order of at least $7$ gives at least one orbit other than the centre (\lean{big_order_orbit})"

Map: no change needed.

## Finding 5 (minor): AssembledSizes.lean restates parts of statements. Fixed.

Checked. `fivefold_size` (line 12) concludes only `35 <= n`, the first conclusion of `A1.c5_reduce`.
`fourfold_via_halfturn` (line 21) concludes only `17 <= 2 * k`, the third conclusion of `A1.c4_reduce`. The other four
restate `c2_reduce`, `c3_reduce`, `mirror_reduce_b0` and `mirror_reduce_b12` in full.

Location: sa.tex, introduction of Subsection sa:ssec:assembled (old line 278, now 283).

Old: "restates six of the statements above with the size $n$ as an explicit variable"

New: "restates six of the statements above, or parts of them, with the size $n$ as an explicit variable"

Map, row sa:prop:assembled, note, changed to match the text. Old: "verifier file of finding A1-F1; restatements with
explicit n (omega in Lean)". New: "verifier file of finding A1-F1; restatements of six SizeArith.lean statements, or
parts of them (fivefold_size: first conclusion of c5_reduce; fourfold_via_halfturn: third conclusion of c4_reduce),
with explicit n (omega in Lean)".

## Finding 6 (minor): the ec proofs use copies of the layer results. Fixed.

Checks:
- `LEANEXT/es7corr/ES7Corollaries.lean` imports only `ErdosSzekeres.*` and Mathlib modules (lines 1-9), not
  `LAYERLEAN/LayerLemma.lean`.
- `diff` shows that its lines 1-1147 are identical to lines 1-1147 of `LAYERLEAN/LayerLemma.lean` (ec.tex lines 81-85
  and 910-912 say the same).
- `fivefold_heptagon` (1183) goes through `fivefold_heptagon_of_erase`, and `fourfold_heptagon` (1216) through
  `fourfold_heptagon_of_erase` (and the copy of `centre_not_mem_of_even`). Both call the copy of
  `convexNGon_of_layers` (line 1066, ll:thm:reduction). That copy builds the subset of exactly m*t = 32 or 35 points
  and calls the copy of `card_peel` (1037), which calls the copy of `layers_are_orbits` (402).

Location: sa.tex, paragraph "What the files do not contain" (old lines 44-46, now 44-48).

Old: "the layer results (Theorems~\ref{ll:thm:layers} and~\ref{ll:thm:card-peel}), through which the Lean proofs of
Theorems~\ref{ec:thm:fourfold} and~\ref{ec:thm:fivefold} pass from a symmetric set to a subset of exactly $32$,
respectively $35$, points;"

New: "the layer results (Theorems~\ref{ll:thm:layers} and~\ref{ll:thm:card-peel}), through verbatim copies of which,
and of Theorem~\ref{ll:thm:reduction}, the Lean proofs of Theorems~\ref{ec:thm:fourfold} and~\ref{ec:thm:fivefold}
pass from a symmetric set to a subset of exactly $32$, respectively $35$, points (the file of these proofs repeats
lines 1--1147 of \dirn{LAYERLEAN/LayerLemma.lean} instead of importing it);"

ll:thm:reduction is an export label of section ll, so the reference is allowed. Map: no change needed. The note of
sa:lem:model lists ll:thm:layers and ll:thm:card-peel as related Lean-checked forms, which is still true.

## Checks

- Compile: `build/sa_wrapper.tex` run twice from `build` with `nice -n 15 pdflatex -interaction=nonstopmode
  -halt-on-error`. Both runs exit 0. There are no `!` errors and no overfull boxes. The only undefined references are
  the allowed `fd:` labels and export labels of other sections (now including ll:thm:reduction). The log has two
  "Underfull \vbox ... while \output is active" notices. The snapshot compiled the same way has one, and the page count
  went from 8 to 9 because of the added text. These are page-break notices, not overfull boxes.
- Hygiene: no machine paths, no tool names, no `\newcommand`/`\def`/`\usepackage` in sa.tex or
  sa.map.tsv. Every map row still has 5 tab-separated fields.
- Appendix: `tools/make_appendix.py`, run on a scratch copy of the sections (`build/sa_final_r1_app`, not the real
  `appendix_map.tex`), accepts the new notes (470 rows, no error). `appendix_map.tex` itself was not regenerated, since
  it is outside the files this fixer may edit.
