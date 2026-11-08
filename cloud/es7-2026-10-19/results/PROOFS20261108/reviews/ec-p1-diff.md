# Diff audit: section `ec`, polish round 1

**Verdict: PASS.** There are no blocker or major findings and 4 minor findings (§5).

Paths: `sections/`, `snapshots/`, `build/` and `reviews/` are relative to the staging area. Research paths are relative
to `RES = cloud/es7-2026-10-19/results`. Nothing under the repository was modified. Lean, lake and solvers were not run.

**Inputs.**
- The passed version, `snapshots/sections-r1pass/ec.tex` and `.map.tsv`. It is byte-identical to
  `snapshots/polish-r1-pre/`, the fixer's input.
- The current version, `sections/ec.tex` (891 lines) and `sections/ec.map.tsv`.
- The fix log, `reviews/ec-polish-r1-fix.md`.
- The four round-1 reports and `reviews/ec-writer-concerns.md`.
- No earlier `ec-p*-diff.md` or `ec-p*-referee.md` exists.

## 1. What changed

`diff -u` shows 21 hunks in `ec.tex` (850 → 891 lines). In `ec.map.tsv` only the notes of `ec:def:cases` and
`ec:rem:cases` changed. The map still has 41 rows with 5 fields each.

Statement environments touched:
- `ec:thm:compat`: the preamble and part (d) are reworded.
- Five heads have shorter names: `ec:lem:pc-basic`, `ec:def:compat`, `ec:prop:parity`, `ec:thm:compat`, `ec:thm:l0`.
- No `\leanref`, label, hypothesis or conclusion changed.

All other changes are in prose: the overview, the Sources, Rigor and Coverage paragraphs, the subsection intros and
Remarks `ec:rem:cases`, `ec:rem:es7-sharp`, `ec:rem:big-order`, `ec:rem:thr` and `ec:rem:polar`.

## 2. Hunk-by-hunk verification

| hunk (current lines) | change | checked against | result |
|---|---|---|---|
| Overview (1), 7-11 | adds "finite", "about some point" | `fivefold_heptagon` / `fourfold_heptagon` (ES7Corollaries.lean:1183, 1216): `Finset`, `∀ c`, GP, `Invariant (rotAbout c (2π/5 or 2π/4))`, `32 ≤`, `29 ≤` | correct |
| Overview (2), 12-15 | threshold arithmetic written out | `thr_m4`..`thr_m7` (C6check.lean:108-111): `c ≤ 1` only for m = 5, 7. The extra quantifier on `e` for m = 4, 6 is vacuous. Brute force over t < 300, e ∈ {0,1} | correct |
| Sources, 25-31 | "lines in scope" plus a scope sentence | line counts 1233/123/132/291/152; Coverage lists the `#print axioms` lines and 1-1147 | consistent |
| Sources, 41-47 | full RES paths | SHA-256 recomputed (5883c8ebac55, 92f15b5cc907, 6e54f5f83a19, ebc6aacefadb, 05a67c3b8b16); REPORT.md:3, PRIMEFOLD/README.md:35,38 | correct (wording nit m4) |
| Rigor, 62-68 | ES8SYM hash caveat; what the written steps are; hypotheses on r | ES8SYM/README.md:258-260. The only "written step" heads are Fact `ec:fact:prim` and Cor. `ec:cor:planar`. No Lean file except PCompatCore.lean uses `exists_card0/1`/`exists_iff` (grep), so (R0)/(RD) are never discharged | correct |
| Conventions 1.1, 91-94 | `exact_mod_cast` | ES7Corollaries.lean:1175, 1177, 1208, 1210, 1228 | correct |
| Remark `ec:rem:cases`, 106-135 | rewritten support chain | SYM5/README.md (table P1/L1, l. 44, 90-91); AUDIT3 A4 report (trust table rows 2-10, A4-1, A4-3, A4-5); C2ENC/perturbation.md status line; C2ENC/class_table.md (Fivefold35 row, l. 34-36, l. 120); C4CUT/README.md (l. 14-20, 28-32, 68-71) | facts and attributions correct, including the records' "refereed" labels, which are attributed to the records. Two minor points: m1 (Lean coverage understated) and m2 (lrat-check) |
| Remark `ec:rem:es7-sharp`, 214-231 | `lem:sizes`; bridge from "symmetry C_s" to `rotAbout(c, 2π/s)` | symmetric_es7.tex:55-68 (`lem:sizes`), 326-345 (`prop:C`). Bridge: ρ = rotAbout(c, 2πk/s) with gcd(k, s) = 1, jk ≡ 1 (mod s), ρ^j = rotAbout(c, 2π/s). Checked for s = 4, 5 and all coprime k in [-3s, 3s] at 50-digit precision: error 0 | correct (wording nit m3) |
| Subsection 1.2 intro, 248-250 | "complex form of part (a)" | layers.md:31-43 | correct |
| Conventions 1.2, 252-256 | `C_r` dropped | grep: no `C_r` remains; `closedBall`/`sphere` are empty for r < 0 | correct |
| Remark `ec:rem:big-order`, 367-375 | "stated there for sets in general position", "follows from" | layers.md:6 (Notation assumes GP), :33; ES8SYM/README.md:33 and symmetric_extremal.tex:550 (row "order ≥ 8", "Lean-checked") | correct |
| Remark `ec:rem:thr`, 424-436 | layer results applied to S∖{c}; `S ⊄ {c}` | `layers_are_orbits`/`card_peel` require `c ∉ S` (LayerLemma.lean:402, 1037), so applying them to S∖{c} is needed. Invariance of S∖{c} via injectivity. `centre_not_mem_of_even` needs p ∈ S, p ≠ c (:582). Arithmetic m t + e checked exhaustively | correct |
| Subsection 1.3 intro, 441-443 | line ranges 15-23, 25-29 | layers.md:15-29 | correct |
| D/Σ scope, 472 | "for the rest of this subsection" | D and Σ are used in Lemmas `det-mul`, `polar-u`, `polar-cross`, Prop. `layered` and Remark `polar`(ii); no clash | correct |
| Remark `ec:rem:polar`(iii), 613-615 | cell statement not formalized | layers.md:26-27 | correct |
| Subsection 1.4 intro, 621-626 | `CommGroupWithZero` gloss; role of `DecidableEq` | Mathlib f897ebcf `GroupWithZero/Defs.lean:203-207, 227` (Nontrivial, `inv_zero`, `mul_inv_cancel`, `DivInvMonoid`); PCompatCore.lean:33-35 (`omit`), 77, 88 (image, sdiff), 114, 116 (`if 0 ∈ S`, erase), 164 (`insert`) | correct |
| Heads, 639/677/682/705/817 | short names only | `\leanref` pairs unchanged (script: 41/41 envs = map rows; 49 name/line pairs exact) | correct |
| Theorem `ec:thm:compat`, 706-717 | "Let m ∈ ℕ, and in (a)-(c) …"; (d) "If 1 ≤ m" | `dvd_card` :67, `card_mod` :112, `exists_iff` :174, `classification` :253, re-read in full: hypotheses, the conclusions `m ∣ T.card`, `S.card % m = (if 0 ∈ S then 1 else 0) % m`, the iff with `N % m = 0 ∨ N % m = 1 % m`, and `m = 1 ∨ (∃ a, 1 ≤ a ∧ m = 2^a) ∨ (Odd m ∧ 3 ≤ m ∧ 2^(m-1) % m = 1)` | exact |
| Coverage, 878-890 | full paths; "outside the scope"; "have not been compiled"; Fact vs Mathlib | ES8SLACK/README.md:402-404; LayerLemma diff (copy, 1-1147) | correct |
| map TSV notes | outside-Lean support | consistent with the Remark; no overclaim ("never proved in Lean" is negative) | correct |

Other checks:
- No machine path or tool name in `ec.tex` or `ec.map.tsv` (grep).
- No "verified" or "certified". "proved" occurs only in the map note "never proved in Lean". "refereed" occurs only in
  quotes of the records' labels (l. 117, 123).
- No new `\ref` outside the allowed set: `ll:thm:layers` and `fd:def:rot` are allowed export labels.
- No new macros and no packages.

## 3. The fixer's items

All "fixed" items are fixed correctly:
- **Fidelity:** F1-F6.
- **Rigor:** F3-F6.
- **Adversarial:** 3, 4, 5.
- **Claims:** m3, m5, m7 and m8. For m8, every remaining bare `\dirn` is a RES directory.
- **Claims "unsure":** 1-3.
- **Other changes 1-6.**

Each was checked against the source named in §2.

Duplicates: all map to fixed items, and the mapping is correct.

Declined:
- **Adversarial 8 (`\ref{sr:def:classes}`): acceptable.** The contract lists it as an `sr` export label. It is defined at
  `sections/sr.tex:208` (the log says :192; the file has moved). It sits on the case-class definition that includes
  `SymReduction.Fivefold35` (:477) and `Fourfold32` (:496).
- **Writer's local `\begingroup\sloppy`: acceptable.** The task says to leave it, and it causes no problem.
- **Writer's other items: acceptable.** They are already stated correctly.

Note on the log, not a finding: "Other change 7" says a source line break "The⏎logs" in `ec:rem:es7-sharp` was joined.
In fact the current source has that break (l. 227-228) and the passed version did not. Source line breaks do not change
the output.

## 4. Compile check

The wrapper is `build/ec_p1diff_wrapper.tex`, with the contract's content. From `build/`, I ran
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error ec_p1diff_wrapper.tex` twice.
- Exit codes: 0 and 0. The output is 11 pages.
- No `!` errors, no "Missing $", no undefined control sequences and no multiply-defined labels. The only "missing" line
  is a microtype info about a small-caps glyph.
- **Overfull boxes > 1pt: none** (0 overfull boxes in total).
- 21 underfull warnings, all in statement heads with long `\leanref` lists or in the Coverage list. The PDF text looks
  normal.
- Undefined references go only to allowed export labels: `fd:def:{point,orient,gp,cp,ngon,inv,rot}`,
  `ll:thm:reduction`, `ll:lem:minperiod`, `ll:thm:layers`, `ll:thm:card-peel`, `lg:lem:centre`, `lg:lem:polar`,
  `sr:def:classes`. Each is defined once in its own section file.
- Logs and the helper scripts are in `build/ec_p1diff/`: pass1/pass2, `mapcheck.py`, `check.py`, `check2.py`.

## 5. Findings (all minor)

**m1 (minor). Remark `ec:rem:cases` understates what is Lean-checked (l. 119-128).**
- **The issue.** The new sentence "Apart from the layer lemma, none of these written arguments is checked in Lean" is
  contradicted by the records and by this document's own section `oc`.
- **The sector normal form for even m.** This is the argument that AUDIT3 A4-1 found unwritten: no point of another
  orbit lies on a ray from c through a point of orbit 0, because the antipode is in S and general position holds. Its
  geometric content is Lean-checked in `LEANEXT/orbit/OrbitConsistency.lean`:
  - `same_ray_false`, :295: for even m, no two points of an invariant set in general position lie on one open ray
    from c;
  - `phase_ne_of_not_mem_orbit`, :420: points of different orbits have phases that are incongruent modulo 2π/m.
- **What the records say.** `LEANEXT/README.md` (4 November) lists these as Lean-checked: "for even m, no two points of
  S on one ray from c, so distinct layers have distinct, nonzero phases with no perturbation". The same document proves
  them as Lemma `oc:lem:same-ray` and Theorem `oc:thm:phase-orbit`.
- **What follows from them.** Exactly one of the four points of each inner orbit lies in the open quadrant, by a
  trivial counting step.
- **Same for the triple-orbit variables.** symcnf.py's "one variable per orbit of triples, with sign bookkeeping" has a
  Lean-checked general form in `encoder_literal_sound` (`oc:thm:encoder`), though the records attach that one to
  gen.py.
- **Why it matters.** Like the layer lemma, none of these is connected to the formulas. The remark should treat them
  the same way. The Fourfold32 bullet also presents the sector argument only as "not written down … now one sentence".
- **Direction.** This understates coverage. No statement or proof is affected.
- **Fix.** Write "Apart from the layer lemma and the even-order ray fact behind the sector normal form
  (Lemma `oc:lem:same-ray`, Theorem `oc:thm:phase-orbit`; `LEANEXT/orbit/OrbitConsistency.lean`), none of these
  written arguments is checked in Lean; these Lean-checked forms are not connected to the formulas …". Both labels are
  allowed `oc` export labels.

**m2 (minor). lrat-check is newly named as a co-checker without the records' caveat (l. 113, 121).**
- **What changed.** The passed text named only cake_lpr. The new text says the proofs "were accepted by the checkers
  lrat-check and cake_lpr".
- **Is it accurate?** Yes, as a record. The SYM5 table for P1/L1, C4CUT/README.md §3 and `final.json` all show both
  verdicts.
- **What the records add.**
  - The project anchors certificates on cake_lpr alone, because the upstream lrat-check build is unsound
    (`LRATCHECK20261105/README.md` "Consequences"; `AUDIT.md` §1 and §5 item 7, "so that cake_lpr alone is the
    anchor").
  - For C4CUT, the lrat-check binary is not recorded (AUDIT3 A4-5).
- **The effect.** Listing both checkers on equal footing suggests double assurance that the records do not claim.
- **Fix.** Write "accepted by cake_lpr (the project's anchor; lrat-check also accepted it, but the project does not
  count lrat-check verdicts, `LRATCHECK20261105`)", or drop lrat-check.

**m3 (minor, wording). Remark `ec:rem:es7-sharp`, l. 225-226.** The sentence "So the two theorems apply to every set
with symmetry C_5, respectively C_4" drops finiteness and general position. These are needed by the theorems and are
part of the note's N(Γ).
- **Fix.** Write "to every finite set in general position with symmetry C_5, respectively C_4".

**m4 (minor, wording). Sources, l. 42-43.** "The two files in `PRIMEFOLD/compat/lean`" is loose, because that directory
holds four files: two `.lean` and two `.out`.
- **Fix.** Write "the two Lean files in `PRIMEFOLD/compat/lean`".

## 6. Checked and found correct (no finding)
- The new mathematics.
  - The power-of-rotation bridge (`ec:rem:es7-sharp`).
  - The S∖{c} argument and the S ⊄ {c} condition (`ec:rem:thr`).
  - The overview thresholds.
  - The `CommGroupWithZero` gloss.
  - The rewording of Theorem `ec:thm:compat`.
- Every new claim about records, except as noted in m1 and m2:
  - SYM5 P1/L1 and A4-3;
  - the perturbation.md status;
  - the class_table rows;
  - the C4CUT labels and §1;
  - the "order ≥ 8" rows labelled Lean-checked;
  - layers.md lines 6, 15-29, 26-27 and 31-43;
  - `lem:sizes` and `prop:C`;
  - `exact_mod_cast`;
  - ES8SLACK "have not been compiled";
  - the ES8SYM hash caveat.
- Rigor labels are not rounded up.
  - The case statements stay hypotheses.
  - The planar corollary stays a written step.
  - The k = 8 tables' "Lean-checked" label is attributed to the tables. The section says that Lean checks only the
    complex form.
