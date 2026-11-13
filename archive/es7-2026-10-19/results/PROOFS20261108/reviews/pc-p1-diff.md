# Section `pc`, polish round 1: diff audit

Lens: diff. Inputs:
- the passed snapshot `snapshots/sections-r1pass/pc.tex` and `pc.map.tsv`;
- the current `sections/pc.tex` (996 lines) and `pc.map.tsv` (32 rows plus header);
- the fix log `reviews/pc-polish-r1-fix.md`;
- the round-1 reports `reviews/pc-r1-{fidelity,rigor,adversarial,claims}.md` and `reviews/pc-writer-concerns.md`.

No earlier polish-round audit or referee report for `pc` exists. Paths below are relative to STAGE (sections, build,
reviews), to RES (Lean sources and records) or to the repository root.

**Verdict: pass.**
- No blocker or major finding.
- Two minor findings (m1, m2). Both are about how records are cited; neither affects correctness.
- 15 fixes confirmed, 16 duplicates accepted, 1 decline accepted.
- The build is clean: both passes exit 0, there are no errors and there is no overfull box.

## 1. Hunks checked (tex: 18 hunks; tsv: 9 rows)

Every hunk is listed in the fix log. No undocumented change was found. For each hunk, the cited Lean source or record
was re-read. "OK" means three things: the mathematics is correct, the claim is supported by RES, and no rigor label
is raised.

| # | Location (current file) | Change | Check |
|---|---|---|---|
| 1 | Intro, lines 16-18 | Rule B bullet: the gap not adjacent to the middle point is ≠ π; the other two radii are positive and at most the middle radius | (B) has g3 = α+2π−δ ≠ π, 0<ra, 0<rd, ra≤rb, rd≤rb. (D) has g1 = β−α ≠ π, 0<ra, 0<rb, rb≤rd, ra≤rd. (A) has g2 = δ−β ≠ π, 0<rb, 0<rd, rb≤ra, rd≤ra (PhaseClassification.lean:310-313, 318-321, 342-345). In each case the named gap is the one not adjacent to the middle direction. Weak inequalities as in Lean. OK |
| 2 | Intro, lines 20-21 | "with a written proof by hand here" | Rigor vocabulary. OK |
| 3 | Sources, lines 29-31 | REPORT.md gives 540 lines with the same hash prefix | `LEANEXT/phase/REPORT.md:3`: "(540 lines, 32 theorems, SHA-256 `490efcd0…`)"; `wc -l` gives 545; shasum gives `490efcd0a7e4…`. OK |
| 4 | Sources, lines 51-58 | hashes of ModelOfLabelling.lean and SoundWord.lean; pins qualified | shasum: `5b532f49cc11…` and `c1bdb4175ee5…`. `ENCBLEAN/lean-toolchain` is v4.24.0, and `ENCBLEAN/lakefile.toml` says "Std-only: no `[[require]]`, so no Mathlib". `ENCBLEAN/geo/lakefile.toml` and `lake-manifest.json` pin Mathlib `f897ebcf`. The repository has v4.24.0 and Mathlib `f897ebcf`. OK |
| 5 | Rigor, lines 60-61 | "cites a Lean declaration, in its head or in one of its parts" | Matches the new placement of the references (hunk 14). See observation O2. OK |
| 6 | Rigor, lines 73-91 | uses on the ENCBLEAN route; pinned declarations; remaining declarations unused | See section 3. OK |
| 7 | Conventions, lines 134-136 | every statement involving polar names its constant | Checked statement by statement. pc:def:polar and pc:lem:polar-facts name it; so do pc:lem:periodic, pc:lem:exists-polar and pc:thm:sign; pc:lem:helpers names it per part. The subsection conventions (lines 598-599 and 838) cover rule-alt, rule-run, phase, centre, halfplane, layers and cor:alt-polar. OK |
| 8 | Lemma pc:lem:polar-facts, lines 141-160 | head keeps (a); parts (b)-(e) carry their own `\leanref`; "polar is PhaseClassification.polar" | Re-read PhaseClassification.lean:44, 407, 51, 64 and 80. Every hypothesis and conclusion is unchanged and exact: rule A bounds use α−δ+2π, and rule B does not assume 0<rb. OK |
| 9 | after the lemma, lines 162-165 | (a), (c), (e) are lg:lem:polar/ruleA/ruleB with the other constant; (d) is lg:lem:sinadd; same Lean proofs | lg.tex:798-870 re-read: the same statements. `diff` of PhaseClassification 40-102 against LayerLemma 931-996 shows that only the 5 docstrings differ. OK |
| 10 | Lemma pc:lem:periodic, line 202 | names the constant | Lean :106, :111, :485 re-read. OK |
| 11 | Lemma pc:lem:exists-polar, lines 218-219 | names the constant | Lean :459 re-read. OK |
| 12 | Remark pc:rem:reading, lines 289-298 | gap sentences moved; the PAPAPA/PPP reading only when α<β<δ<α+2π and no gap equals π | Given the order, two of the three directions differ by an amount in (−2π, 2π)∖{0}. So a direction x and an antipode y+π coincide modulo 2π iff x−y = ±π, that is, iff β−α, δ−β or δ−α equals π, that is, iff g1, g2 or g3 equals π. An exact rational grid (1081 ordered triples, boundary cases included) gives 0 mismatches. The PAPAPA/PPP reading is right for six distinct points. OK |
| 13 | Lemma pc:lem:shift, lines 355-358 | "disjunct by disjunct, keeping the witness k or changing it by +1 or −1" | PhaseClassification.lean:327-335 has witnesses k, k, k+1 (first conjunct) and k, k, k+1 (second). Lines 350-362 have k, k+1, k+1 and k−1, k, k. OK |
| 14 | Theorem pc:thm:alternating head, line 440 | short name "alternation iff all gaps are <π" | Statement unchanged; Lean :210 re-read. OK |
| 15 | Theorem pc:thm:sign, lines 713-717 | names the constant | Lean :496-520 re-read: 3 positivity and 2 `toIcoMod ≠ α` hypotheses, then two implications with 7 premises each. Radius roles in (ii) are as in Lean. OK |
| 16 | "How Lean checks it", lines 766-782 | per-function check; premise first; elaborator then kernel; M7 described; PPAPPA as own example | The proof is `by decide` at :543, with the default configuration, not `+kernel`. The implication instance decides p first and q only under p, so only the 8 premise words reach the conclusion. The elaborator then reduces the instance, the term is `of_decide_eq_true … (Eq.refl true)`, and the kernel re-checks it. `mutants.py`: M7 replaces `(∀ i : Fin 6, s (i + 3) = !s i) →` by `True →`. `mutants.log` M7: "exit=1 errors=1 first=… error: Tactic `decide` proved that the proposition" (the script keeps only lines containing ": error"). PPAPPA was checked exactly: it violates the premise (s(3)=s(0)), is not alternating and has no cyclic PPP. OK, except m1 |
| 17 | proof of pc:thm:word, lines 805-809 | cross-check sentence deleted | The hand proof is complete without it. OK |
| 18 | Remark pc:rem:word-scope, lines 812-826 | scoped to LEANEXT; ENCBLEAN encoder-B counterpart | See section 3. OK, except m2 |
| 19 | Theorem pc:thm:layers, lines 852-898 | head keeps (a); parts (b)-(e3) carry the six Capstone `\leanref`s; short name | All seven declarations re-read: Linked:1398, Capstone:1977, Capstone2:2011, 2031, 2082, 2098, 2115. Statement text unchanged and exact: hull vertex and index inequalities per case, (P) with three positive radii, (P√) without radius variables, gap condition per case. OK |
| 20 | Corollary pc:cor:alt-polar head, line 935 | short name "rule A restated" | Statement still names `LayerLemma.polar`; Capstone:1992 re-read. OK |
| 21 | Remark pc:rem:layers-scope, lines 948-959 | (a) listed separately (0<β−α, 0<δ−β, δ−α<π); the middle point defined for (a) and (b)-(e) | Matches Linked:1398-1404 and the six Capstone statements. OK |
| 22 | Coverage, lines 964-966 | "whose originals also have written proofs in the section on layer geometry" | lg.tex has proofs of lg:lem:polar, ruleA, sinadd and ruleB. OK |
| 23 | map rows pc:def:polar, pc:lem:polar-facts, pc:lem:periodic, pc:lem:exists-polar, pc:lem:helpers, pc:thm:word, pc:rem:word-scope, pc:thm:layers, pc:cor:alt-polar | notes only | Every path is now RES-relative (`LEANEXT/…`, `ENCBLEAN/…`). The notes agree with the text and the records. Labels, kinds, Lean names and file:lines are unchanged. All fields are ASCII; 32 rows with 5 fields each. OK |

## 2. Touched statements re-read against Lean

Hunks 8, 10, 11, 14, 15, 16, 19, 20 and 21 touch statement environments or their heads. For each of them the Lean
declaration was re-read in full. These are PhaseClassification.lean:44, 51, 64, 80, 106, 111, 210, 407, 459, 485, 496
and 539, Linked.lean:1398, Capstone.lean:1977 and 1992, and Capstone2.lean:2011, 2031, 2082, 2098 and 2115. No
hypothesis, conclusion, quantifier order, strictness or constant changed relative to the passed snapshot, and every
statement is still exact.

Scripted checks (`build/pc_p1diff_mapcheck.py`):
- 32 statement environments equal the 32 map rows in label, kind, Lean-name list and file:line list, in order.
- All 54 `\leanref`s point at the declaration line of the named constant.

The label set, the `\ref` set and the ordered `\leanref` list are identical to the passed snapshot, and the 10 export
labels are defined once each.

## 3. New claims about records, checked against RES

- **ENCBLEAN route (Rigor and axioms, hunk 6).** The claimed uses and dependencies were traced in the sources:
  - `Labelling.lean:63-65`: `Capstone.ne_of_mem`, `Capstone.exists_angle` and `Capstone.sqrt_dist2_pos`, all in
    `Lab.exists_layer_polar`, which `labelling_of_counterexample` uses at `:84`.
  - `Labelling.lean:133`: `dist2_polar`, inside `labelling_of_counterexample`. It resolves to
    `ErdosSzekeres.LayerLemma.dist2_polar`, the only definition of that name in the package (`ES8Geo/Capstone2.lean:1398`).
  - `Capstone2.lean:2070`: `polar_zero` is used in the proof of `sqrt_dist2_pos`.
  - `ArcBridge.lean:155-156`: `PhaseClassification.polar_add_int_two_pi` and `Capstone.polar_eq`, in `P_eq_polar`.
    `P_eq_polar` is used by `arcFrame` (`:427-428`), and `arcFrame` by `labelling_ruleA`/`labelling_ruleB`
    (`:463`, `:480`).
  - `ArcBridge.lean:464, 481`: `orient_pos_of_alternating` and `orient_pos_of_runMidB`.
  - `ModelOfLabelling.lean:29-30`: the `ruleA`/`ruleB` fields of `modelOfLabelling`.
  - `Audit.lean:45-49` pins `modelOfLabelling` and `labelling_of_counterexample` to [propext, Classical.choice,
    Quot.sound]. `logs/m8_fix_build.log:49,51` records "Built ES8Geo.Audit" and a successful build.
  - The inference "used by a pinned declaration, so its axioms are among the three" is sound, since `#print axioms`
    collects axioms transitively.
- **Remaining declarations.** `orient_pos_of_layers`, the six layer rules and `orient_pos_of_alternating_polar` are
  "not used outside the copy". A grep over all of ENCBLEAN finds these names only in `geo/ES8Geo/Capstone2.lean` and in
  `DESIGN.md`. No `#print axioms` output for any new Linked/Capstone/Capstone2 declaration exists in RES (grep, including
  `LEANEXT/review/axioms.log`). The two REPORTs state the axioms: `linked/REPORT.md:15`, `capstone/REPORT.md:7, 29`.
- **Encoder-B counterpart (hunk 18).**
  - `ENCBLEAN/EncB/SoundWord.lean:222` is `theorem wordSpec : WordSpec`.
  - `EncB/Model.lean:181-194` defines `WordSpec`. Its second conjunct takes three cyclically consecutive point
    positions st, st+1, st+2 of the sorted word to `BlockCCW` of their labels. `BlockCCW` (`Model.lean:58`) is
    KeysDistinct, a ccw triple and two empty `ArcHasAntipode` arcs.
  - `ArcBridge.lean:393` (`arcFrame`) gives true directions α<β<δ<α+2π with each `EncB.ArcHasAntipode` test equivalent
    to the `PhaseClassification.arcHasAntipode` test of its arc. `labelling_ruleB` (`:473`) builds `RunMidB α β δ`
    from these (`:483`) and applies `orient_pos_of_runMidB` (`:481`).
  - `word_dichotomy` occurs in ENCBLEAN only in the Capstone2 copy and in DESIGN.md, so "does not use Theorem
    pc:thm:word" is right.
  - ENCBLEAN is encoder B in Lean (`ENCBLEAN/README.md:1-3`).
  - No claim is made that the antipodal property of the sorted word is proved, and none should be.
- **REPORT "Not in Lean", item 2** (`LEANEXT/phase/REPORT.md:51-52`) is quoted correctly, now scoped to LEANEXT.

## 4. The fixer's dispositions

| id(s) | disposition | audit judgement |
|---|---|---|
| fid-1 | fixed | correct (hunk 1) |
| fid-2; adv-F3 (dup) | fixed / duplicate | correct (hunk 21) |
| fid-3; rig-F1, adv-F1, cl-1 (dup) | fixed / duplicates | correct (hunk 16). The per-function check is stated. Premise-first evaluation and the 8-word count are accurate. The elaborator/kernel split is accurate for default `decide`. No claim about early exit inside the Fin 6 quantifiers. |
| fid-4; rig-F7, adv-F6, cl-4 (dup) | fixed / duplicates | correct (hunk 6). The two pinned declarations are named, and the chains were traced (section 3). |
| fid-5; cl-5 (dup) | fixed | correct: no LEANEXT-relative path remains in the map or in the tex (grep) |
| fid-6; adv-F5 (shared) | fixed | correct (hunks 7, 8, 10, 11, 15) |
| fid-7; rig-F6, adv-F7, cl-6, WC-overfull (dup) | fixed / duplicates | correct: 0 overfull boxes. The passed snapshot, compiled with the current preamble, still has 8 (11.7, 5.8, 1.2, 6.5, 59.0 ×3 and 42.1 pt), so the restructuring was needed. See O1. |
| rig-F2; adv-F2, cl-2 (dup) | fixed / duplicates | correct (hunk 17) |
| rig-F3; cl-7 (dup) | fixed / duplicate | correct (hunk 2) |
| rig-F4; cl-8 (dup) | fixed / duplicate | correct in substance. The log truncation is stated, and PPAPPA is the writer's own checked example. The `True` replacement is cited to the log; it is in `mutants.py` (m1). |
| rig-F5 | fixed | correct (hunk 13) |
| adv-F4 | fixed | correct (hunk 12) |
| cl-3 | fixed | correct (hunk 18); evidence citation for the new Lean-checked attribution missing (m2) |
| WC-540 | fixed | correct (hunk 3) |
| WC-split | declined | acceptable. The contract assigns `pc:thm:layers` to "orient_pos_of_layers and the Capstone layer rules" together. Each part now cites its own declaration. |

## 5. Findings

### m1 (minor): the `True` replacement of mutant M7 is attributed to the mutation log
- **Location:** pc.tex:777-778 ("In the mutation log `LEANEXT/phase/logs/mutants.log`, mutant M7 replaces the premise
  by `True`").
- **Issue:** The log line for M7 reads "M7 drop antipodal premise in word_dichotomy: exit=1 errors=1 first=…". The
  replacement by `True` is defined in `LEANEXT/phase/mutants.py` (the M7 entry replaces `(∀ i : Fin 6, s (i + 3) = !s i)
  →` by `True →`), not in the log. The claim is true, but a reader who checks the cited log will not find it.
- **Fix:** For example: "mutant M7 (`LEANEXT/phase/mutants.py` replaces the premise by `True`; the log calls it 'drop
  antipodal premise') fails to compile …".

### m2 (minor): the new "Lean-checked" attribution in Remark pc:rem:word-scope does not cite its evidence
- **Location:** pc.tex:817-824.
- **Issue:** The remark calls `EncB.wordSpec`, `EncB.Geo.Arc.arcFrame` and `EncB.Geo.labelling_ruleB` a "Lean-checked
  counterpart". Elsewhere the section names the axiom record for every Lean-checked claim; here it gives none. The
  evidence exists:
  - `wordSpec`: its `#guard_msgs` axiom pin at `ENCBLEAN/EncB/SoundWord.lean:228-229`, `ENCBLEAN/logs/axioms.log:446`
    and the build in `ENCBLEAN/logs/m3_build.log:9`;
  - `arcFrame` and `labelling_ruleB`: `ENCBLEAN/logs/m8_fix_build.log:29,35`, and they are on the dependency path of
    `modelOfLabelling`, pinned at `Audit.lean:45-46`.
- **Fix:** Add one parenthesis, e.g. "(axioms: the `#guard_msgs` line after `wordSpec`, and for the two ArcBridge
  declarations the pin of `EncB.Geo.modelOfLabelling` described under Rigor and axioms)".

## 6. Build

My wrapper `build/pc_p1diff_wrapper.tex` has the contract content. I ran `nice -n 15 pdflatex -interaction=nonstopmode
-halt-on-error pc_p1diff_wrapper.tex` twice from `build/`:
- Both passes exit 0, giving 12 pages. There are no `!` errors, no "Missing" and no multiply defined labels.
- **Overfull boxes: 0** (none of any size), so this item gives no finding.
- The undefined references are exactly the 14 allowed labels of other sections: fd:def:inv, fd:def:ngon, fd:def:orient,
  fd:def:point, fd:def:rot, fd:lem:orient, lg:def:polar, lg:lem:polar, lg:lem:ruleA, lg:lem:ruleB, lg:lem:sinadd,
  lg:thm:radius, ll:def:hv and ll:def:peel.
- There are 51 underfull warnings, from the loosely set multi-reference heads and part references. The snapshot
  build gives 52. The fix log's count of 49 was probably made differently; this has no effect.
- I looked at the rendered pages 1-5 and 9-12. Every changed head and part reference stays inside the margins.

Other checks:
- No machine path and no tool name in pc.tex or pc.map.tsv.
- No `\newcommand`, `\def`, `\usepackage` or `\begin{document}`.
- No `\lean`/`\dirn` argument contains a space (after the `\lean{Eq.refl}~\lean{true}` fix).
- Rigor vocabulary is fine. "proved" occurs only negatively ("is not proved in LEANEXT") or in the quoted Lean error
  message. "verif" occurs once, as mathematical usage ("verify the two inequalities", unchanged).
- `build/pc_p1diff_checks.py` (exact) confirms three things:
  - 8 of the 64 words satisfy the premise, and all 8 satisfy (i) and (ii);
  - PPAPPA refutes the M7 mutant;
  - the reading-remark grid above gives 0 mismatches.

## 7. Observations (no finding)

- **O1. Head format.** The heads of Lemma pc:lem:polar-facts and Theorem pc:thm:layers carry one `\leanref` each, plus
  "the declarations cited in (b)–(e)". The other references now sit at the start of the parts they belong to. This
  departs from the literal head form of the contract. I accept it for three reasons:
  - cl-6 proposed this remedy;
  - it is needed to remove the overfull boxes (see fid-7 above);
  - every reference is still in the statement, exact and in map order, and the appendix is generated from the map.
- **O2. Scope of the rigor sentence** (lines 60-61). "Cites a Lean declaration" read loosely could include Remark
  pc:rem:gaps(2), which mentions `gap_classification`. The qualifier "in its head or in one of its parts", the
  document's use of "cite" (with file:line), and the remark's own label ("a written observation, not part of the Lean
  statement") rule this reading out. Optional tightening: "every theorem, lemma, proposition, corollary and definition
  that carries a Lean reference …".
- **O3. Cosmetic.** The part references end with a sentence period inside the parentheses, right after the line
  number: "(Lean: …, …lean:407.)". The rendered text is unambiguous.

Evidence files (STAGE): `build/pc_p1diff_wrapper.{tex,log,pdf}`, `build/pc_p1diff_snapwrapper.{tex,log}` (the passed
snapshot with the current preamble), `build/pc_p1diff_mapcheck.py` and `build/pc_p1diff_checks.py`.
