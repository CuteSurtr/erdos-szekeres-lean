# pc, polish round 1: fix log

Files: `sections/pc.tex` (now 996 lines) and `sections/pc.map.tsv` (32 rows, 5 columns). The pre-polish versions are in
`snapshots/polish-r1-pre/`. Paths below are relative to the staging area (sections, reviews, build). Lean paths are
relative to the results directory (RES) or the repository root, as in the section. Line numbers are those of `sections/pc.tex`
after the fix.

Ids:
- `fid-n`: finding n of `reviews/pc-r1-fidelity.md`.
- `rig-Fn`: finding Fn of `reviews/pc-r1-rigor.md`.
- `adv-Fn`: finding Fn of `reviews/pc-r1-adversarial.md`.
- `cl-n`: finding n of `reviews/pc-r1-claims.md`.
- `WC-*`: items of `reviews/pc-writer-concerns.md`.

## Findings

| id | summary | action | location after the fix | reason / note |
|---|---|---|---|---|
| fid-1 | intro bullet for rule B omits the gap hypothesis (and the positive outer radii) | fixed | pc.tex:15-19 (4th bullet) | Rule B now reads: gap not adjacent to the middle point differs from π, and the other two radii are positive and at most the middle radius (weak inequalities, as in Lean). |
| fid-2 | Remark pc:rem:layers-scope lists "gap ≠ π and pattern" as hypotheses of all parts; (a) has 0<β−α, 0<δ−β, δ−α<π instead | fixed | Remark pc:rem:layers-scope, pc.tex:948-959 | (a) and (b)-(e) are now listed separately; "the middle point" is defined for (a) (the point b of the middle direction) and for (b)-(e). |
| fid-3 | "How Lean checks it" does not state the per-function check, and says the conclusion is evaluated for all 64 functions | fixed | paragraph "How Lean checks it", pc.tex:766-782 | Now: for each of the 64 functions the procedure decides premise ⇒ (i)∧(ii); the implication instance evaluates the conclusion only when the premise holds (8 functions, listed in the proof). Checked against Lean 4.24 core: `instance [Decidable p] [Decidable q] : Decidable (p → q)` (Init/Core.lean) and `decide`'s `doElab`/`mkDecideProof` (elaborator reduces the instance, proof term `of_decide_eq_true` with `Eq.refl true`, which the kernel re-checks). No claim is made about short-circuiting inside the ∀/∃ over Fin 6. |
| fid-4 | "final theorems of the ENCBLEAN geometric package (Labelling.lean and ArcBridge.lean)" is ambiguous | fixed | paragraph "Rigor and axioms", pc.tex:73-91 | Now names the two pinned declarations that depend on the helpers: `EncB.Geo.labelling_of_counterexample` (Labelling.lean) and `EncB.Geo.modelOfLabelling` (ModelOfLabelling.lean). Their axioms are pinned at Audit.lean:45-49. Chains re-traced: exists_layer_polar (Labelling:63-65) → labelling_of_counterexample (:84); dist2_polar (Labelling:133); polar_zero (Capstone2:2070); polar_eq/polar_add_int_two_pi → P_eq_polar (ArcBridge:155-156) → arcFrame (:427) → labelling_ruleA/B (:463, :480) → modelOfLabelling (ModelOfLabelling:29-30); orient_pos_of_alternating/runMidB (ArcBridge:464, :481). Neither of the two pinned declarations takes a SAT hypothesis, so no hypothesis is presented as proved. |
| fid-5 | map notes use LEANEXT-relative paths | fixed | pc.map.tsv rows pc:def:polar, pc:lem:polar-facts, pc:lem:periodic, pc:lem:exists-polar, pc:rem:word-scope | All prefixed with `LEANEXT/`. |
| fid-6 | Theorem pc:thm:sign does not name its polar constant | fixed | Theorem pc:thm:sign, pc.tex:712-717 | "where polar is PhaseClassification.polar" (as in Lean, namespace PhaseClassification). |
| fid-7 | overfull boxes (59, 42, 12, 6 pt) in statement heads | fixed | heads of Lemma pc:lem:polar-facts (141), Theorem pc:thm:alternating (440), Theorem pc:thm:layers (852), Corollary pc:cor:alt-polar (935) | Standalone build: 0 overfull boxes (was 8). Full-document build, done in an isolated output directory (`build/pc_polish_tests/full`): 0 overfull boxes in the pc part. See "Layout" below. |
| rig-F1 | `decide` evaluation described inaccurately (conclusion evaluated only when the premise holds) | duplicate of fid-3 | as fid-3 | |
| rig-F2 | unrecorded computer cross-check sentence inside the hand proof | fixed | proof of Theorem pc:thm:word, pc.tex:809 | Sentence deleted. The hand proof is complete without it. |
| rig-F3 | "proved by hand here" uses "proved" for a written proof | fixed | intro, pc.tex:20-21 | "computer-assisted in Lean, with a written proof by hand here". |
| rig-F4 | the PPAPPA example reads as if it came from the mutant log | fixed | pc.tex:777-782 | M7 is described as in `LEANEXT/phase/mutants.py`: the premise is replaced by `True`. The log keeps only the first line of Lean's error ("Tactic `decide` proved that the proposition"). The continuation "... is false" is stated as Lean's message format (Lean 4.24 source, Elab/Tactic/ElabTerm.lean). PPAPPA is presented as our own example: it violates the premise (s(3)=s(0)) and is neither alternating nor has a cyclic PPP. |
| rig-F5 | "shifting the witness k by ±1" ignores the unchanged witnesses | fixed | end of the proof of Lemma pc:lem:shift, pc.tex:355-358 | "disjunct by disjunct, keeping the witness k or changing it by +1 or −1, as (a) and (b) do above". Checked against PhaseClassification.lean:323-335 (k, k, k+1) and 346-362 (k, k+1, k+1, k−1, k, k). |
| rig-F6 | overfull boxes | duplicate of fid-7 | as fid-7 | |
| rig-F7 | "final theorems" parenthetical | duplicate of fid-4 | as fid-4 | |
| adv-F1 | `decide` description (premise-first evaluation; elaborator then kernel) | duplicate of fid-3 | as fid-3 | The elaborator/kernel split it mentions is also stated now. |
| adv-F2 | unrecorded cross-check claim | duplicate of rig-F2 | as rig-F2 | |
| adv-F3 | scope remark misdescribes part (a) | duplicate of fid-2 | as fid-2 | |
| adv-F4 | Remark pc:rem:reading assumes six distinct points (no gap = π) | fixed | Remark pc:rem:reading, pc.tex:284-299 | The PAPAPA/PPP reading is now stated only when α<β<δ<α+2π and no gap equals π. The text says why: a direction and an antipode coincide mod 2π exactly when β−α, δ−β or δ−α equals π, i.e. when g1, g2 or g3 equals π. The gap sentences were moved before this reading. |
| adv-F5 | polar constant implicit in Lemmas pc:lem:periodic, pc:lem:exists-polar and Theorem pc:thm:sign | fixed | Lemma pc:lem:periodic (202), Lemma pc:lem:exists-polar (218-219), Lemma pc:lem:polar-facts (142-143), Theorem pc:thm:sign (714-715) | Each statement now names PhaseClassification.polar. The convention after Definition pc:def:polar now says that every statement involving polar names its constant, directly or through its subsection convention (pc.tex:134-136). The pc:thm:sign part is shared with fid-6. |
| adv-F6 | wording about where the ENCBLEAN final theorems are | duplicate of fid-4 | as fid-4 | |
| adv-F7 | overfull lines in statement heads | duplicate of fid-7 | as fid-7 | |
| cl-1 | `decide` description over-describes the evaluation | duplicate of fid-3 | as fid-3 | |
| cl-2 | cross-check sentence is an unrecorded process claim | duplicate of rig-F2 | as rig-F2 | |
| cl-3 | Remark pc:rem:word-scope: "not proved in Lean" is out of date for encoder B | fixed | Remark pc:rem:word-scope, pc.tex:812-826 | Scoped to LEANEXT. Added the Lean-checked encoder-B counterpart of the run link, which does not use Theorem pc:thm:word: `EncB.wordSpec` (ENCBLEAN/EncB/SoundWord.lean:222; its axioms are in its own `#guard_msgs` line and in ENCBLEAN/logs/axioms.log), `EncB.Geo.Arc.arcFrame` and `EncB.Geo.labelling_ruleB` (ArcBridge.lean:393, :473; used by the pinned modelOfLabelling). It is described as a property of the encoder's Lean version only. No claim is made that the antipodal property s(i+3)=¬s(i) is proved anywhere. |
| cl-4 | "final theorems" parenthetical | duplicate of fid-4 | as fid-4 | |
| cl-5 | map paths not relative to RES | duplicate of fid-5 | as fid-5 | |
| cl-6 | overfull boxes | duplicate of fid-7 | as fid-7 | The suggested remedy (keep one `\leanref` in the head, move the others into the statement) is the one used for the two long heads. |
| cl-7 | "proved by hand here" | duplicate of rig-F3 | as rig-F3 | |
| cl-8 | mutant log line is truncated; PPAPPA reads as if from the log | duplicate of rig-F4 | as rig-F4 | The truncation is now stated explicitly. |
| WC-overfull | writer's list of 6 overfull boxes in the full-document build | duplicate of fid-7 | as fid-7 | |
| WC-split | pc:thm:layers bundles 7 declarations; a verifier may prefer to split off the intrinsic versions | declined | — | The export label pc:thm:layers is assigned to "orient_pos_of_layers and the Capstone layer rules" together, and no reviewer asked for a split. The layout problem is solved without restructuring: each part now cites its own declaration. |
| WC-540 | contract discrepancy "REPORT.md says 540 lines" was reported as noted in the text, but it was not | fixed | Sources, pc.tex:29-31 | Added: LEANEXT/phase/REPORT.md gives 540 lines for this file, with the same hash prefix. Checked: `wc -l` gives 545; the REPORT says "(540 lines, 32 theorems, SHA-256 `490efcd0…`)". |

Counts: 32 rows: 15 fixed, 16 duplicates, 1 declined.

Writer concerns reviewed, no action needed:
- Uneven axioms evidence. The text already stated it. The wording was made precise under fid-4. "have no recorded axiom check" became "no `#print axioms` output is saved", because the two REPORTs do state the axioms.
- Section-local `\begingroup\sloppy`. Kept, as instructed. It causes no problem.
- Lemma pc:lem:polar-facts duplicates section lg. Kept for self-containment. The sentence after the lemma was made precise (see "Other changes").
- Written observations in remarks. They are already labelled "not Lean-checked".
- Docstring "exactly one" (Remark pc:rem:gaps(2)), README "standalone" vs import (Sources), one file:line per `\leanref` with the offsets rule, blank Capstone line 1425. All are already in the text.

## Layout (fid-7 and duplicates)

amsthm boxes the statement head, so url break points inside `\lean`/`\dirn` are lost there and a head can break only at spaces. Measured chunk widths (10pt): Lean names 160-323pt, file:line 166-223pt, line width 484.2pt. In the 5- and 7-reference heads, some unbreakable "file, Lean: name" pairs exceed the line, so these heads cannot be set without overflow.

- Lemma pc:lem:polar-facts: the head keeps `\leanref` for (a). Parts (b)-(e) each start with their own `\leanref` (orient_polar_centre :407, orient_polar_centre_inside :51, sin_add_lt :64, orient_polar_halfplane :80). Body text can break inside the names.
- Theorem pc:thm:layers: the head keeps `\leanref` for (a) (orient_pos_of_layers, Linked:1398). Parts (b), (c), (d), (e1), (e2), (e3) now carry the full `\leanref` of the six Capstone declarations instead of the bare short name. The short name changed from "rule B on layers" to "rule B on the convex layers", so that the first head line is well filled.
- Theorem pc:thm:alternating: the short name "alternation iff all gaps are below π" became "alternation iff all gaps are <π".
- Corollary pc:cor:alt-polar: the short name "rule A with LayerLemma.polar" became "rule A restated". The statement still says "with polar the constant LayerLemma.polar".

Result: the per-statement list of `\leanref` (names and file:lines, in order) is identical to the map (scripted comparison). All 54 `\leanref` lines point exactly at the declaration line of the named constant (scripted check against the Lean files). Statements are mathematically unchanged.

## Other changes

1. Sentence after Lemma pc:lem:polar-facts (pc.tex:162-165). It said that parts (a), (c), (d), (e) are the lg lemmas "for the constant PhaseClassification.polar". That is imprecise for (d) (sin_add_lt has no polar). It now reads: (a), (c), (e) are lg:lem:polar, lg:lem:ruleA, lg:lem:ruleB with PhaseClassification.polar in place of LayerLemma.polar, and (d) is lg:lem:sinadd. The lg statements were re-read (lg.tex:766-830).
2. Sources (pc.tex:50-58). Added the SHA-256 prefixes of the two newly cited files: ENCBLEAN/geo/ES8Geo/ModelOfLabelling.lean `5b532f49cc11` and ENCBLEAN/EncB/SoundWord.lean `c1bdb4175ee5` (shasum). The pins sentence was qualified: the EncB package of SoundWord.lean is built with Lean 4.24.0 and no Mathlib (ENCBLEAN/lean-toolchain, lakefile.toml "Std-only"). The other files use Mathlib `f897ebcf` (geo lake-manifest has the same rev).
3. "Rigor and axioms", first sentence (pc.tex:60-61). It now reads "Every statement below that cites a Lean declaration, in its head or in one of its parts, is Lean-checked", because some references now sit in parts.
4. "Rigor and axioms". The remaining new declarations (orient_pos_of_layers, the six layer rules, orient_pos_of_alternating_polar) are said to be "not used in the ENCBLEAN geometric package outside the copy itself" (grep of ES8Geo/*.lean, excluding Capstone2.lean: no use). This replaces "have no recorded axiom check", which clashed with the REPORTs stating the axioms.
5. Map TSV, notes only (labels, kinds, Lean names and file:lines unchanged):
   - pc:lem:helpers: the pinned declarations and Audit.lean:45-49;
   - pc:thm:word: the evaluation as now described;
   - pc:rem:word-scope: the LEANEXT scope and the ENCBLEAN counterpart;
   - pc:thm:layers: the angle conditions of (a) vs (b)-(e), "no saved axiom output", and part-level references;
   - pc:cor:alt-polar: "no saved axiom output (REPORT states standard axioms)";
   - pc:lem:polar-facts: part-level references.
6. While fixing fid-3 I first wrote `\lean{Eq.refl true}`. url-style macros drop spaces, and the PDF showed "Eq.refltrue". It is now `\lean{Eq.refl}~\lean{true}`. A scan finds no other `\lean`/`\dirn` argument with a space.
7. Coverage, rigor vocabulary (pc.tex:965-966). "these are the copies of lines 931-996 of LayerLemma.lean, also proved in the section on layer geometry" now reads "..., whose originals also have written proofs in the section on layer geometry". The only remaining uses of "proved" are mathematical ("This proves (i)"), negative ("is not proved in LEANEXT") or a quote of Lean's error message.

## Compile check (contract)

`build/pc_wrapper.tex` (inputs ../preamble and ../sections/pc). Two runs of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error pc_wrapper.tex` from `build/`:
- Both exit 0, 12 pages.
- No `!` errors and no "Missing".
- 0 overfull boxes (> 1pt: 0).
- The undefined references are only fd:def:inv, fd:def:ngon, fd:def:orient, fd:def:point, fd:def:rot, fd:lem:orient, lg:def:polar, lg:lem:polar, lg:lem:ruleA, lg:lem:ruleB, lg:lem:sinadd, lg:thm:radius, ll:def:hv and ll:def:peel. All are allowed labels of other sections.

Other checks:
- The forbidden-text scan of pc.tex and pc.map.tsv (machine paths, tool names) finds nothing.
- No `\newcommand`, `\def` or `\usepackage`.
- Labels and kinds are identical to the map (32 environments).
- All export labels are kept.
- Underfull boxes: 49 vs 50 before. They are the loosely set multi-reference heads, as before.
