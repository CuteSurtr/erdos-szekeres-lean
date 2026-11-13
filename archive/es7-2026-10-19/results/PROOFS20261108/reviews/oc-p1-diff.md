# Section `oc`, polish round 1: diff audit

Lens: diff. Inputs:
- the passed snapshot `snapshots/sections-r1pass/oc.tex` and `oc.map.tsv`;
- the current `sections/oc.tex` and `oc.map.tsv`;
- the fix log `reviews/oc-polish-r1-fix.md`;
- the round-1 reports `reviews/oc-r1-{fidelity,rigor,adversarial,claims}.md` and `reviews/oc-writer-concerns.md`.

No earlier polish-round audit or referee report for `oc` exists. Paths below are relative to STAGE, to RES (Lean
sources and records) or to the repository root (`ErdosSzekeres/...`).

**Verdict: pass.**
- No blocker or major finding.
- One minor finding (m1).
- 20 fixes confirmed, 14 duplicates accepted, none declined.
- The build is clean: both passes exit 0, with no overfull box.

## 1. Hunks checked (tex: 20 hunks; tsv: 3 rows)

Every hunk is listed in the fix log; no undocumented change was found. For each hunk, the cited Lean source or record
was re-read. "OK" means the mathematics is correct, the claim is supported, and no rigor label is raised.

| # | Location (current file) | Change | Check |
|---|---|---|---|
| 1 | Overview (A), lines 9-16 | orient₃(t) defined inline and used for t and C | Matches `literal_sound` / `encoder_literal_sound` (OrbitConsistency.lean:228, 253). OK |
| 2 | Overview (B), lines 17-26 | "even m > 0"; layer-lemma hypotheses named; "open ray from c" | Hypotheses of `not_same_ray_of_distinct_layers` / `phase_ne_of_distinct_layers` (Merged.lean:1350, 1367): 2 ≤ m, Even m, K ≤ 2m, c ∉ S, Invariant, GP, ¬HasConvexNGon K S. For even m, m > 0 ⇔ m ≥ 2. OK |
| 3 | Sources, lines 34-37 | path convention: `ErdosSzekeres/` paths are relative to the repository root; bare names are the listed files | All 39 `\dirn` targets resolve (checked with ls); the only bare names are OrbitConsistency/Merged/KeyOrder.lean and line suffixes of them. OK |
| 4 | Sources, line 48 | "the definitions of the namespace `ErdosSzekeres.LayerLemma`" | OK |
| 5 | Sources, lines 53-58 | copies of section 13 in Linked, Capstone and Capstone2; ENCBLEAN Capstone2 is byte-identical (`f8c3930c2427`) | `diff` of Merged 1148-1383 against Linked 1148-1383, Capstone 1156-1391 and Capstone2 1156-1391: all empty. `cmp` Capstone2 against ENCBLEAN Capstone2: identical. sha256 `f8c3930c2427` for both. OK |
| 6 | Axioms, lines 71-95 | Merged's LAYERLEAN copies named; remaining theorems listed with usage; exceptions (i) and (ii) | See below. OK |
| 7 | Rigor, lines 97-99 | "records above (for a definition: it is part of the compiled file)" | OK |
| 8 | Dependencies, lines 106-119 | adds fd:lem:affine-orient, fd:lem:cp-hull, fd:lem:separation, ll:lem:minperiod; restricts lg:lem:centre to comments | Every external `\ref` (20 distinct labels: fd/ll/lg exports only) is listed, and its stated place of use is correct (lines 237, 664, 515, 705, 722, 725). OK |
| 9 | Remark oc:rem:copies, lines 149-169 | "same declaration text" except for the `iterate_mem` binder and the `polar` doc comment; EncB `rfl` theorem reworded; Capstone2 copy named | `diff` of OC 39-112 against LL 52-57, 104-105, 230-271, 297-308, 465-469, 931-932 shows exactly these 2 lines. Orbit.lean:13-14 is `LayerLemma.rotAbout c θ = OrbitConsistency.rotAbout c θ := rfl` and imports ES8Geo.Capstone2; the only ES8Geo definition of `LayerLemma.rotAbout` is Capstone2.lean:306, whose text equals LL:297-300. OK |
| 10 | Lemma oc:lem:rotcomp-pres, lines 264-265 | intro sentence | Statement unchanged; Lean names and lines 127/129/134/141/150/157 re-read. OK |
| 11 | Fact oc:fact:sign, lines 317-319 | multiplicativity of ℤˣ → ℤ → ℝ | Composite of monoid homs. OK |
| 12 | Theorem oc:thm:encoder, lines 407, 415-418 | title "modelled on the encoder"; labels' distinctness follows from orient₃(P∘T) ≠ 0 | Statement re-read against OrbitConsistency.lean:253-257: unchanged and exact. fd:lem:orient(e) exists in the current fd.tex and in the snapshot ("orient(a,b,c)=0 whenever two of a,b,c are equal ..."). If T(i)=T(j) then P(T(i))=P(T(j)). OK |
| 13 | Remark oc:rem:parity, lines 436-481 | code reading per encoder; corrected Python-evidence wording; DESIGN wording | See below. OK |
| 14 | Lemma oc:lem:same-ray, lines 514-516 | c ∉ S follows by lg:lem:centre | `centre_not_mem_of_even` (LayerLemma.lean:582): 0<m, Even m, Invariant, GP, p ∈ S, p ≠ c ⇒ c ∉ S. Since x ≠ y, one of them is ≠ c. Statement unchanged against OC:295-298 / Merged:1181-1184. OK |
| 15 | Remark oc:rem:ray, lines 536-537 | example m = 2, S = {x, 2c−x} | ρ = R_{c,π} swaps the two points; GP is vacuous; y−c = −(x−c), y ≠ x. OK |
| 16 | Lemma oc:lem:polar-rot, lines 541-542 | intro sentence | (a), (b) unchanged and exact (OC:355, 383; Merged:1241, 1269). OK |
| 17 | Remark oc:rem:layers(3), lines 710-723 | pigeonhole sentence; explicit convex combination | Exact check (sympy): the combination holds for all four sign pairs (weights 3/8, 3/8, 1/8, 1/8); GP over all 56 triples; no third point on any same-kind line; quarter-turn invariance; c ∉ S. OK |
| 18 | Definition oc:def:keys, lines 739, 747-751 | intro sentence; `Int.ediv` = ⌊J/N⌋ for N > 0, `Int.emod` | Correct for N > 0. OK |
| 19 | Lemma oc:lem:antipode-cell, lines 826-827 | intro sentence | (a), (b) unchanged and exact (KeyOrder.lean:100, 115). OK |
| 20 | Remark oc:rem:keys-outside, lines 876-889 | three steps outside Lean; gen_b2 cell index for both parities; source per step; REPORT.md:16-17; phases differ via Ju+ψ | gen_b2.py:106-109: `J = (2*k + h[i]) % (2*m)` (odd), `J = k` (even). keys/REPORT.md:22-25 lists the first two steps as hypotheses; README.md:25 lists the third under "Still outside Lean"; REPORT.md:16-17 is quoted correctly. The math holds: equal ψ would give β−α = (J₂−J₁)u. OK, except m1 |
| 21 | Coverage (i), (iii), (iv), lines 925-934 | ranges outside `\dirn`; complete copy list | OK |
| 22 | map rows `oc:lem:iterate`, `oc:lem:iter-mem`, `oc:lem:rotcomp-pres` | axiom sources in the notes | Notes agree with the text and the logs. Script check: 43 rows plus header, 5 columns each; labels, kinds, Lean names and file:line lists equal the statement heads. OK |

**Hunk 6 (Axioms paragraph) in detail.**
- `merged/axioms.log` lines 3, 5 and 6 are `layers_are_orbits`, `convexNGon_of_layers` and `sevenfold_octagon`. These
  are theorems of LAYERLEAN (LL:402, 1066, 1136); Merged 1-1147 equals LL 1-1147.
- `KeyOrder.lean` 151-158 are the eight `#print axioms` lines, and `m4_build.log` 3-10 are their outputs.
- Every theorem said to be "used by printed theorems" is used by one:
  - OC `iterate_mem` (line 276) and OC `rotAbout_iterate` (line 286) are used by `antipode_mem_of_even`;
  - `preservesOrient_id`, `.comp` and `preservesOrient_rotAbout` are used by `RotComp.preservesOrient` (153-154);
  - `rotAbout_polar` (370) and `polar_add_int` (410, 413) are used by the printed phase lemmas;
  - in Merged, the restatements chain into the printed theorems at 1186, 1256, 1259, 1296, 1300 and 1310;
  - `not_mem_hullVerts_peel_of_lt/_ne` and `iterate_mem_hullVerts_peel` are used at 1325, 1357, 1359, 1379 and 1381.
- Exception (i): `PreservesOrient.iterate` is referenced nowhere else in RES; `orbit/logs/build.log` is `exit=0`.
- Exception (ii): `review/axioms.log` line 1 is `iterate_mem` with [propext, Quot.sound], and line 33 is
  `rotAbout_iterate` with the three axioms. `review/REPORT.md` lines 3-4 give 4 November 2026 and LayerLemma.lean,
  SHA-256 `afb8542d…`, 1148 lines. `LAYERLEAN/logs/axioms.log` has neither name, so the review log is the right
  citation.
- Re-grepped: no `sorry`, `admit`, `axiom` or `native_decide` in the three files; `decide` occurs only at OC:236 and
  Merged:1125.

**Hunk 13 (Remark oc:rem:parity) in detail.**
- `C7UPPER/gen.py`:
  - line 108: `sortpar` is a bubble sort with a strict `>` that flips `par` at each exchange;
  - line 120: it is applied to `(a, b, c)`;
  - line 78: it is applied to `rt`, the rotation of a sorted `combinations` triple.
  - Line 123 builds the literal from `s1*s2`, matching σ₁, σ₂ as described.
- `C6UPPER/encb/gen_b2.py`:
  - line 56: `perm_sign` counts inversions;
  - lines 72-73: `order = sorted(range(3), key=lambda r: rt[r])` (σ sorts the rotated triple), then
    `perm_sign(order)`.
  - The triple is not pre-sorted, so σ₁ = id and σ₂ = σ is right.
- `check_literals.py`: lines 25-31 are its own `perm_sign`; lines 36-38 assert sorting and parity equality on the six
  orders; line 39 prints.
- `check_literals.log` lines 2-5: 42840 + 39270 + 12144 + 274560 = 368,814 triples, 0 mismatches.
- `ENCBLEAN/DESIGN.md:625` records the mismatch, "A 6-case bridge would be needed", and the verdict "Not used". No
  causal claim remains in the remark.
- The six-case table and inv(a) = inv(σ⁻¹) were re-checked by script against a cycle-count sign.

Global checks:
- grep finds no machine path, no tool name, no `\newcommand`, `\usepackage` or `\begin{document}`, and no
  "verified", "certified", "proved" or "proves" in `oc.tex` or `oc.map.tsv`. No `\dirn{...--...}` remains.
- Python functions are now `\texttt`, and no `\lean{sortpar}` or `\lean{perm_sign}` is left.
- The label list is identical to the snapshot, in the same order. All 13 export labels sit on the same statements with
  the same Lean names.

## 2. Fixer's dispositions

**Fixed (20). All are confirmed fixed correctly.**
- fidelity F1-F4;
- rigor M1, M2, M5 (A part), M6, M7, M9, M10, M11;
- adversarial m2, m4;
- claims m1 (ii), m3, m5 (nit), m6 (DESIGN part), m7, m11.

The record-based ones were re-verified against RES:
- F3: build.log, review/axioms.log:1/33, REPORT.md:3-4;
- M2: four diffs and one cmp;
- m3: path resolution;
- m6: DESIGN.md:625;
- m7: REPORT.md:16-17 and 22-25, README.md:25.

**Duplicates (14). All are acceptable.** Each points to a fix that covers its full content:
- rigor M3, M4, M8;
- adversarial m1, m3, m5, m6, m7, m8;
- claims m2, m4, m8, m9, m10.

The partial duplicates are also covered: rigor M5 (B part), claims m1 (i), claims m5 (main part) and claims m6 (Python
part).

**Declined (0).**

## 3. Compile check

- Wrapper: `build/oc_p1diff_wrapper.tex`, the contract wrapper.
- Command, run twice from `build/`: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error oc_p1diff_wrapper.tex`.
- Both passes exit 0, giving 13 pages.
- The log has no `!` error, no "Missing", no undefined control sequence and no multiply defined label.
- **Overfull boxes: 0.** There are underfull warnings only, caused by the section-local `\sloppy`.
- Undefined references, all expected in the standalone build:
  - `fd:def:{point,orient,gp,ngon,inv,rot}`;
  - `fd:lem:{orient,affine-orient,collinear,cp-hull,mono,separation}`;
  - `ll:def:{hv,peel}`, `ll:lem:{antitone,inv-peel,minperiod}`, `ll:thm:core-rot`;
  - `lg:def:polar`, `lg:lem:centre`.
- No `oc:` reference is undefined.
- In the PDF text, no "--" artefact appears.

## 4. Findings

### m1 (minor): Remark `oc:rem:keys-outside` still says "For even m" where Theorem `oc:thm:layers-phase` needs m ≥ 2
- Location: `sections/oc.tex` lines 885-887. The sentence was rewritten in this round (rigor M10).
- Issue: the text reads "For even m, Theorem oc:thm:layers-phase gives, for hull vertices of distinct layers given in
  polar form, directions that are incongruent modulo 2π/m". The theorem assumes `2 ≤ m` (Merged.lean:1367) and the
  layer-lemma hypotheses (c ∉ S, invariance, general position, no K points in convex position with K ≤ 2m).
- Under the section's own convention, m = 0 is even (`Even`, 2π/0 = 0). For m = 0 the theorem gives nothing.
- This is the same imprecision that F2, M5, adversarial m1 and claims m2 fixed in the overview.
- There is no effect on correctness: the next clause, "with u = 2π/m and 0 ≤ ψ < u", is vacuous for m = 0.
- Suggested fix: "For even m ≥ 2, under the hypotheses of Theorem oc:thm:layers-phase, that theorem gives …".
