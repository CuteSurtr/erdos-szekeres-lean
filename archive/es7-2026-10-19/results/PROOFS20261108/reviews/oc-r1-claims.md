# Review oc, round 1, lens: claims, labels and LaTeX

Section: `sections/oc.tex` (870 lines) and `sections/oc.map.tsv` (43 rows plus header).
Verdict: **pass**. I found no blocker or major findings. There are eleven minor ones (m1 to m11 below). For m1, m6 and
m11 I say below what I am unsure about.

Paths below are relative to one of three places: the staging directory (`sections/`, `build/`), the results directory
RES (`LEANEXT/...`, `LAYERLEAN/...`, `ENCBLEAN/...`, `C6UPPER/...`, `C7UPPER/...`), or the repository root
(`ErdosSzekeres/...`, `lean-toolchain`, `lake-manifest.json`).

## What was checked, and the result

1. **Compile.** From `build/` I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
   -output-directory=claims-oc-r1 oc_wrapper.tex` twice.
   - Both passes exit 0. The output is a 12-page PDF; the log, `pass1.txt` and `pass2.txt` are in `build/claims-oc-r1/`.
   - The log has no `!` errors, no "Missing", no undefined control sequence, no "Label(s) may have changed", no
     multiply-defined labels and no hyperref token warnings. There are no overfull boxes. There are 67 underfull boxes,
     which are cosmetic: they come from `\sloppy` and the long Lean names.
   - Undefined references (all allowed):
     - `fd:` labels: `def:point`, `def:orient`, `def:gp`, `def:ngon`, `def:inv`, `def:rot`, `lem:orient`,
       `lem:affine-orient`, `lem:collinear`, `lem:cp-hull`, `lem:mono`, `lem:separation`.
     - `ll:` export labels: `def:hv`, `def:peel`, `lem:antitone`, `lem:inv-peel`, `lem:minperiod`, `thm:core-rot`.
     - `lg:` export labels: `def:polar`, `lem:centre`.

     Each of these is defined in `fd.tex`, `ll.tex` or `lg.tex`. Its environment matches the word used before
     `\ref` here (Definition, Lemma or Theorem).
2. **Machine paths and tool names.** I grepped `oc.tex` and `oc.map.tsv` for the forbidden absolute prefixes (private
   temporary, user, home and system-temporary directories), the scratch directory and the user name. I also grepped for
   tool names and for "agent", "sandbox" and a third tool word. There were no hits. The file contains no
   `\newcommand`, `\usepackage` or `\begin{document}`, and it starts with `\section{...}\label{oc:sec}`.
3. **SHA-256** (recomputed with `shasum -a 256`). All four quoted 12-digit prefixes are correct:
   - `LEANEXT/orbit/OrbitConsistency.lean` is `9b843180ac38…`.
   - `LEANEXT/merged/Merged.lean` is `245b7d65407a…`.
   - `LAYERLEAN/LayerLemma.lean` is `afb8542dceb0…`.
   - `LEANEXT/keys/KeyOrder.lean` is `6e34096cff52…`.

   The line counts are correct: 429, 1385 and 158 (each file ends with a newline). `ENCBLEAN/geo/ES8Geo/OrbitConsistency.lean`
   and `ENCBLEAN/geo/ES8Geo/KeyOrder.lean` have the same digests, so they are byte-identical as claimed.
4. **Copy claims** (checked with `diff`).
   - `Merged.lean` lines 1–1147 equal `LayerLemma.lean` lines 1–1147.
   - `Merged.lean` lines 1157–1312 against `OrbitConsistency.lean` lines 270–428: only the section header and the doc
     comments differ, so the "seven declarations … proofs identical, only the doc comments differ" claim holds.
   - `Merged.lean` lines 1148–1383 equal `LEANEXT/capstone/Capstone2.lean` lines 1156–1391.
   - The copied block of `OrbitConsistency.lean` matches `LayerLemma.lean`. Lines 49–91 equal LayerLemma 230–272,
     lines 92–104 equal 297–309, and lines 105–109 equal 465–469. The two exceptions are the doc comment of `polar`
     (see m9) and the type-variable binder of `iterate_mem`.
5. **Axiom-log citations** (I opened each log).
   - `LEANEXT/orbit/logs/axioms.log` has 15 lines with exactly the 15 names listed in oc.tex:56–60, each
     `[propext, Classical.choice, Quot.sound]`, followed by `exit=0`.
   - `LEANEXT/merged/axioms.log` lists `phase_ne_of_distinct_layers`, `not_same_ray_of_distinct_layers`,
     `phase_ne_of_not_mem_orbit`, plus `layers_are_orbits`, `convexNGon_of_layers` and `sevenfold_octagon`, each with
     the same three axioms.
   - `ENCBLEAN/logs/m4_build.log` lines 3–10 hold the 8 `#print axioms` outputs of `ES8Geo/KeyOrder.lean:151–158`, each
     with the same three axioms. `LEANEXT/keys/` has no log, so "not inside LEANEXT" is correct.
   - The helper claims are correct:
     - `preservesOrient_id`, `PreservesOrient.comp` and `preservesOrient_rotAbout` are used by
       `RotComp.preservesOrient`.
     - `rotAbout_polar` and `polar_add_int` are used by `eq_iterate_of_phase_eq` and `eq_iterate_of_phase_eq_int`.
     - The Merged restatements and the three layer helpers are used by printed Merged theorems.
     - `PreservesOrient.iterate` is used by no printed theorem; it occurs only in its own recursion, at
       OrbitConsistency.lean:139.
6. **sorry / axiom / decide.** A grep of the three files finds no `sorry`, `admit`, `axiom` or `native_decide`.
   - `decide` occurs only at OrbitConsistency.lean:236 and at Merged.lean:1125, as claimed.
   - At :236 the goal after `rw [hs]` is `-1 ≠ 1` in ℤˣ.
   - At :1125 the `decide` is the `Even 6` argument, since `centre_not_mem_of_even` takes `(hm : 0 < m) (heven : Even m)`
     (LayerLemma.lean:582).
   - Describing `decide` as kernel evaluation with no extra axiom is correct.
7. **Toolchain.** The repository's `lean-toolchain` is `leanprover/lean4:v4.24.0`, and `lake-manifest.json` pins
   Mathlib at `f897ebcf…`. These files have not changed since the initial commit. `ENCBLEAN/geo` pins the same versions.
   LEANEXT/README.md:6 does say "compiles with `lake env lean` from the repository root".
8. **Lean references.** A script checked every one of the 52 `\leanref{Name}{File:Line}` heads. In each case the named
   declaration (theorem, def or inductive) starts on exactly that line, in the stated namespace. Every name exists.
9. **Other file:line citations in the prose.** I opened each one:
   - `ErdosSzekeres/OrientationGeometry.lean:66` is `generalPosition_iff_orient_ne_zero`.
   - `LAYERLEAN/LayerLemma.lean:364` is `hullVerts_eq_orbitFS_rotAbout`; the (L3) hypotheses match.
   - In `LayerLemma.lean`: `iterate_mem` is at :52, `Invariant` at :105, the helpers at :231–308 (`rotAbout_eq_crot` ends
     at 308), `rotAbout` at :298, `rotAbout_iterate` at :465 and `polar` at :932.
   - `ENCBLEAN/geo/ES8Geo/Orbit.lean:13` is `rotAbout_eq_orbitConsistency … := rfl`.
   - `C7UPPER/gen.py:108` is `def sortpar` (bubble sort that flips the parity on each swap).
   - `C6UPPER/encb/gen_b2.py:56` is `def perm_sign` (counts inversions).
   - `LEANEXT/orbit/logs/check_literals.log` lines 1–5 hold the sortpar line and four runs. The triple counts
     42840 + 39270 + 12144 + 274560 sum to 368,814, with 0 mismatches.
   - `ENCBLEAN/DESIGN.md:625` covers the `encoder_literal_sound` mismatch and gives the verdict "Not used".
   - `ENCBLEAN/DESIGN.md:626` covers local ranks.
   - `LEANEXT/keys/REPORT.md:22–25` is the "Still hypotheses" block.

   Every cited path exists.
10. **Labels.**
    - Every `\ref` target is an own `oc:` label (all defined, none duplicated), an `fd:` label from the contract list,
      or an `ll:`/`lg:` export label from the contract table.
    - All 13 export labels of `oc` are defined on the right statements: `oc:lem:rot-inv`, `oc:lem:perm`,
      `oc:thm:literal`, `oc:thm:encoder`, `oc:lem:antipode`, `oc:lem:same-ray`, `oc:thm:phase-orbit`,
      `oc:thm:layers-ray`, `oc:thm:layers-phase`, `oc:lem:cell` (`cell_lt_iff` and `cell_eq_iff`), `oc:lem:rank`,
      `oc:lem:antipode-cell` (`antipode_odd` and `antipode_even`) and `oc:thm:key`.
11. **Map TSV.** The header is correct and every row has 5 tab-separated fields.
    - A script matched the 43 statement environments of oc.tex against the 43 rows. Labels, order, kinds, Lean names
      and file:line lists all agree.
    - The notes are consistent with the logs (for example "PreservesOrient.iterate has no recorded axiom output", and
      the KeyOrder notes point to `m4_build.log:3-10`).
12. **Hypotheses and rigor labels.**
    - No statement in scope takes `Sixfold66`, `Sevenfold70`, a case class or a SAT verdict as a hypothesis. The section
      says this correctly (oc.tex:85–86).
    - The rigor wording is "Lean-checked" plus "written proofs (not refereed)". A grep finds no "verified",
      "certified", "proved" or "exactly as written".
    - The overclaims in the docstrings and READMEs are not repeated. Remark oc:rem:phase-orbit explicitly declines the
      "nonzero phases" reading of the `phase_ne_of_not_mem_orbit` doc comment and README.md:14.
    - There is no computation needing a "computer-assisted" label. The six-case parity table is a hand check, and the
      Python checks are labelled "evidence, not proof".
13. **NOTES of the task.**
    - Remark oc:rem:parity says that the encoders compute parity by counting inversions and that Lean does not model
      this (the code correspondence and the six-case bridge are "not part of any Lean statement").
    - `toIcoMod` and the half-open intervals are stated exactly: Definition oc:def:keys(a), Lemma oc:lem:toico and
      Remark oc:rem:halfopen. The Mathlib definitions match: `toIcoDiv` is the unique `n` with `b - n•p ∈ Ico a (a+p)`,
      and `toIcoMod = b - toIcoDiv•p`.
14. **Spot checks of the content.**
    - Parity table: I recomputed `inv` and `sgn` for all six permutations, and the products of swaps agree with the
      convention `(στ)(i) = σ(τ(i))`.
    - The π/m counterexample of Remark oc:rem:layers(3) checks out, using exact rational arithmetic for general
      position and invariance.

## Findings (all minor)

**m1. Two sentences inside statement environments are literally false.**
- oc.tex:386 (Theorem oc:thm:encoder) says "the labels T(0),T(1),T(2) need not be distinct". The hypothesis
  `orient3 (P ∘ T) ≠ 0` forces P(T(0)), P(T(1)) and P(T(2)) to be pairwise distinct (fd:lem:orient(e)), so the labels
  are pairwise distinct.
- oc.tex:470 (Lemma oc:lem:same-ray) says "The hypotheses do not exclude c∈S". But x ≠ y in S gives a point of S
  different from c, and then Lemma lg:lem:centre (0<m, m even, invariance, general position) gives c∉S. This is exactly
  the argument the section itself uses in Remark oc:rem:layers(1).

The intended meaning in both places is that the property is not a separate hypothesis. Suggested wording:
- "distinctness of the labels is not a separate hypothesis; it follows from orient3(P∘T)≠0";
- "c∉S is not a hypothesis; it follows from the others by Lemma lg:lem:centre, as in Remark oc:rem:layers(1)".

I am unsure about the severity. The sentences sit inside statement environments, but they do not change the
mathematical content of the statements, so I rate them minor.

**m2. The introduction omits 0<m.** oc.tex:16–19, item (B), says: "For even m, a finite set in general position that is
mapped into itself by … ρ … contains the antipode 2c−x of each of its points, and no two of its points lie on one open
ray from c." In Mathlib, m = 0 is even, and then 2π/0 = 0 and ρ = id. So S = {x} with x ≠ c is a counterexample to the
antipode claim, and two points on one ray give a counterexample to the ray claim. The formal Lemmas oc:lem:antipode and
oc:lem:same-ray correctly assume 0<m. Fix: "For even m>0".

**m3. The path convention statement does not match the paths used.** oc.tex:32 says "File paths are relative to the
results directory of the project". But oc.tex:484 cites `ErdosSzekeres/OrientationGeometry.lean:66`, which is relative to
the repository root. The contract allows that path, but the section's own statement is then inaccurate. Several citations
also use basenames instead of RES-relative paths:
- `OrbitConsistency.lean:236` (oc.tex:77);
- `KeyOrder.lean:151--158` (oc.tex:66 and :866);
- `\dirn{:298}` and `\dirn{:932}` (oc.tex:139–140).

These are unambiguous in context (the ENCBLEAN copies are byte-identical), but I suggest stating the exception for
`ErdosSzekeres/...` in the Sources paragraph.

**m4. A literal `--` inside `\dirn` prints as two hyphens.** This happens at oc.tex:66 and :866 (`KeyOrder.lean:151--158`),
:824 (`REPORT.md:22--25`) and :863 (`LayerLemma.lean:231--308`). The PDF text shows "151--158", "22--25" and "231--308".
Put the range outside `\dirn`, for example `\dirn{KeyOrder.lean}, lines 151--158`.

**m5. The Axioms paragraph does not account for the copied lemmas that carry Lean references.** Rigor (oc.tex:80–81)
says every statement with a Lean reference is Lean-checked "in the sense of the logs above". The Axioms paragraph does not
cover these four:
- `OrbitConsistency.iterate_mem` (:39) and `OrbitConsistency.rotAbout_iterate` (:105). Both are covered transitively,
  because `antipode_mem_of_even` is printed and uses both.
- `LayerLemma.iterate_mem` (LAYERLEAN/LayerLemma.lean:52) and `LayerLemma.rotAbout_iterate` (:465). These are covered
  because the line-identical Merged.lean 1–1147 copies are used by the printed Merged theorems. They are also recorded
  directly in `LEANEXT/review/axioms.log`: line 1 gives `iterate_mem` with only `[propext, Quot.sound]`, and line 33
  gives `rotAbout_iterate` with the three standard axioms.

One sentence would close this. A related nit: the "three LAYERLEAN theorems" in `merged/axioms.log` are Merged.lean's
copies (`layers_are_orbits`, `convexNGon_of_layers`, `sevenfold_octagon`).

**m6. Remark oc:rem:parity slightly over-reads the Python test and DESIGN.md.**
- oc.tex:433–434 says "The agreement of sortpar with the permutation sign on all six orders was also tested in Python".
  The reference "sign" in `LEANEXT/orbit/check_literals.py:25–31,36–38` is its own `perm_sign`, which is again an
  inversion count. So the test compares two inversion-count parities (bubble-sort swaps against the inversion count),
  not sortpar against sgn. Suggest "agreed with an inversion count of the permutation".
- oc.tex:436–437 says the design notes "name this mismatch … as the reason". `ENCBLEAN/DESIGN.md:625` lists the mismatch
  ("A 6-case bridge would be needed") and gives the verdict "Not used". It explains that M3 proves the literal rule
  combinatorially, but it never says "because". Unsure: the causal reading is plausible but is an inference.
  "Records this mismatch; its verdict is 'Not used'" would be exact.

**m7. Remark oc:rem:keys-outside cites the wrong source for its third item.** oc.tex:819–825 lists "that sorting the keys
gives the circular order of the actual points" among the things outside Lean and cites `LEANEXT/keys/REPORT.md:22--25;
ENCBLEAN/DESIGN.md:626`. REPORT.md:22–25 lists only the decomposition hypothesis and rank monotonicity. Worse,
`LEANEXT/keys/REPORT.md:16–17` says that `reduced_lt_iff_key` "is the step 'sorting keys gives the circular order' in
gen_b2.py". The statement in the section is right. Its support is `LEANEXT/README.md:25` ("Integer (sector, rank) keys
versus the true circular order", under "Still outside Lean"). Suggest citing README.md:25, and optionally noting the
contrary wording in REPORT.md:16–17.

**m8. The Dependencies paragraph is incomplete.** oc.tex:88–97 does not mention four labels that the section references:
- `fd:lem:affine-orient` (oc.tex:210);
- `fd:lem:cp-hull` (:669);
- `fd:lem:separation` (:672);
- `ll:lem:minperiod` (:616).

All of these occur in remarks or parentheticals, and all are allowed labels.

**m9. Remark oc:rem:copies overstates the identity of the copied text.** oc.tex:130 says "with the same text (up to the
declaration of a type variable)". The doc comment of `polar` differs: OrbitConsistency.lean:111 reads "The point `c + r
(cos θ, sin θ)`.", while LayerLemma.lean:931 reads "The point at distance `r` from `c` in direction `θ`.". The declaration
code is identical (diff-checked). Suggest "the same declaration text (the doc comment of `polar` differs)".

**m10. Two copies of Merged section 13 are not mentioned.** The Sources paragraph (oc.tex:50–52) and Coverage (iv)
(oc.tex:867–868) mention copies of Merged section 13 only in `Capstone2.lean` and `ENCBLEAN/geo/ES8Geo`. There are two
more:
- `LEANEXT/linked/Linked.lean` (lines 1–1383 equal Merged.lean 1–1383);
- `LEANEXT/capstone/Capstone.lean` (lines 1156–1391 equal Merged.lean 1148–1383).

Both were diff-checked. Add them to the list of verbatim copies.

**m11. The title of Theorem oc:thm:encoder may suggest too much.** oc.tex:378 titles the theorem "label-level form as
in the encoder", echoing the Lean doc comment. Remark oc:rem:parity explains that the encoder computes parity by
inversion counting and that the code correspondence is outside Lean. "label-level form modelled on the encoder" would
avoid suggesting that the encoder code itself is covered. Unsure whether this counts as repeating overclaiming wording;
the remark that follows makes the scope clear.

## Not findings

These were checked and found correct:
- the 15-name list against the orbit axioms log;
- "exit status 0";
- the claim that `PreservesOrient.iterate` is the only declaration without recorded axiom output;
- the Capstone2 line ranges;
- the m4_build.log line range;
- the claims about which Mathlib names exist (all of them appear in the Lean sources' proofs, or are core definitions:
  `Int.ediv`, `Int.emod`, `toIcoDiv`);
- the Coverage paragraph, which lists every declaration of OrbitConsistency.lean, of Merged section 13 and of
  KeyOrder.lean as covered or as deliberately not covered (with reasons).
