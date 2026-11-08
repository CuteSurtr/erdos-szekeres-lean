# Whole-document review, round doc-r1, lens: completeness

Scope: the document `proofs.tex` (sections fd, ll, lg, oc, pc, ec, sr, ar, mm, mb, cb, sa, the generated appendix and
the bibliography) against the Lean declarations of the Stage 1 units LAYERLEAN, LEANEXT, SYMLEAN-core, SYMLEAN-mirror,
MIRRORETV, C3-C2-misc and ES8-small (ES8SLACK excluded by the task). Paths: RES = `cloud/es7-2026-10-19/results`
(relative to REPO); section files are `sections/<key>.tex` in STAGE.

**Verdict: FAIL.** 4 major, 3 minor findings. Every Coverage paragraph is accurate about the files it claims
(line ranges, verbatim-copy claims, counts, line numbers all check out). The gaps are Stage 1 Lean files that no
section claims and no Coverage paragraph lists with a reason: 176 declaration occurrences (157 distinct
declarations; 19 more are a byte-identical copy) in 9 files.

## 0. Method (reproducible)

- `reviews/checks/completeness_check.py` (read-only; prints a report). It walks all 55 `.lean` files under the unit
  directories `RES/{LAYERLEAN, LEANEXT, SYMLEAN, MIRRORETV, C3LEAN, C2FINAL, C3L, AUDIT2, AUDIT3/A1_reduction, ES7SPLIT,
  ES8SYM, PRIMEFOLD, ES8SLACK}`. It extracts every top-level `theorem`, `lemma`, `def`, `abbrev`, `structure`,
  `instance`, `inductive`, `class` and `example`, with its namespace and line, outside comments. That gives 2,776
  occurrences. Each one is then classified:
  - restated: its full name is a `\leanref` head or a statement-map row;
  - a member of a generated family (`certs0..126`, `batch0..126`, `reflection_facts_H6_*`, `closedP1..8`) whose
    first member heads a statement;
  - named in a Coverage paragraph;
  - inside a range or file that a Coverage paragraph declares a verbatim copy or excludes;
  - ES8SLACK, excluded by the task;
  - NEITHER.
- Result: 547 restated, 268 family members, 32 named in Coverage, 1,704 in declared copies or excluded files, 49
  ES8SLACK, **176 NEITHER**. Generic short names were checked by hand; for example `MirrorA.orient_affine` is not the
  `SymReduction.orient_affine` that fd and ar name.
- The script re-checks 31 verbatim-copy claims by comparing the line ranges: **all SAME**. I also ran `cmp` and
  `diff` by hand on every range quoted in a Coverage or Sources paragraph (§2).
- Independent checks:
  - all 663 `\leanref{name}{file:line}` heads match the declaration line exactly (0 off);
  - the 27 "name (line N)" claims inside Coverage paragraphs are exact;
  - the SHA-256 prefixes of 29 cited files (28 Lean files and `LAYERLEAN/README.md`) match;
  - every `\lean{...}` name in a Coverage paragraph exists (apart from Mathlib names, namespaces, local `have`
    names, tactic names and name fragments such as `_line`);
  - every `\ref` in a Coverage paragraph resolves.
- A main-library check for fd: all 57 declarations of the nine main-library files in fd's table of sources are
  either restated, named as counterparts, or in fd's "Deliberately not covered" list, as fd claims. I checked the
  reasons given there (the private helper, and the use of `convexIndependent_of_affineIndependent` only by
  `convexPosition_of_card_three`).

## 1. Stage 1 declarations neither covered nor listed (major)

**M1 (lg; also concerns ll). The LEANEXT non-vacuity tests are not listed.**
- What is missing: `RES/LEANEXT/review/tests_tail.lean` has 19 declarations in namespace
  `ErdosSzekeres.LayerLemma.Review`:
  - definitions: `L4` (12), `S4` (15), `H6` (124);
  - theorems: `mem_S4` (17), `card_S4` (21), `angle4` (23), `rot4` (25), `hc4` (30), `inv4` (35), `gp4` (41),
    `inner4` (54), `hno4` (69), `hv4` (77), `peel1_4` (91), `nest4` (96), `orbit4` (102), `layers4` (106),
    `chain4` (117), `inv6` (128).
- `RES/LEANEXT/review/VacuityTest.lean` lines 1149–1297 are byte-identical to `tests_tail.lean` (checked with
  `cmp`), so the same 19 declarations sit there at lines 1160–1276.
- No section names either file's tests. lg's Coverage (lg.tex:929–940) lists `VacuityTest.lean` only as one of the
  eight files that contain LayerLemma lines 11–1147. That is true but incomplete: the file is LayerLemma.lean lines
  1–1148 followed by the test tail.
- These are tests: the 8-point set `S4` with m = 4, K = 8 discharges the hypotheses of `strict_nesting`,
  `hullVerts_eq_orbitFS_rotAbout`, `layers_are_orbits` and `chain_clauses_sound`, and `inv6` checks a hexagon. The
  inventory calls them "audit only".
- Fix: add an item to lg's "Deliberately not covered" list, or to ll's, which names the 19 declarations, says they
  are tests and not results, and corrects the description of `VacuityTest.lean`.

**M2 (mm). `MIRRORETV/review/` is excluded without a reason, and the description is inaccurate.**
- The only text is mm.tex:960–962: "the independent re-formalizations in `MIRRORETV/review/`, which are outside the
  scope of this section". No other section takes these files, so the document leaves them out with no reason given.
- Two of the four files are not re-formalizations: `FarFlatExtra.lean` holds Theorem B estimates and
  `ReplayRepo.lean` is an audit command.
- The inventory lists several of these theorems as results of the unit (roles "supporting" and "duplicate").
- Content not covered (95 occurrences):
  - `MirrorA.lean` (namespace `MirrorA`; 71 declarations and one example at line 852). Its own definitions
    (`orient`, `mu`, `ConvexPos`, `IsCapSeq`, `IsCupSeq`, `V`, `GenPos`, `XDistinct`, `HasGon`, `HasCap`, `HasCup`,
    `InClass`, `MirrorSym`, `refl`, `isoT`, ...) and the theorems `theoremA_even` (593), `theoremA_odd` (615),
    `theoremA_even_bound` (685), `theoremA_odd_bound` (694), `theoremA_even_line` (810), `theoremA_odd_line` (821),
    `lemma31` (282), `cap_convexPos` (352) and `cup_convexPos` (417), with their helpers.
    - This is not a pure duplicate. Its odd case k = 2j−1 with j ≥ 2 includes k = 3, which Theorem mm:thm:odd
      excludes (mm's own Remark mm:rem:hm says so).
  - `MirrorCap.lean` (namespace `MirrorCap`; 16 declarations). `convex_position` (292) and `convexIndependent` (316)
    are the mirror lemma under consecutive-triple cap hypotheses with end heights ≥ 0, a formulation different from
    `cap_mirror_polygon`. `coincidences` (327) is the count |V| = 2m − #(endpoints on the axis), which no section
    states.
  - `FarFlatExtra.lean` (namespace `FFX`; 7 declarations): `orient`, `orient_sum`, `bary_of_neg`, `bary_of_pos`,
    `gp_cross_axis` (60), `a1_inside` (69) and `lemma51_core` (91). These are estimates for the far-flat lower-bound
    construction (Theorem B), not a re-formalization.
  - `ReplayRepo.lean`: one `elab` command `#replay_repo` and its invocation, which replay the repository constants
    used by `MirrorMain.lean` in the kernel. It is an audit, with no declaration of the kinds listed and no
    mathematical statement.
- Fix: replace the clause with one item per file that names its declarations (or their families) and gives a
  document-level reason. For example: "independent review formalizations of Theorem A and of the mirror lemma; not
  restated; their content overlaps Theorems mm:thm:odd, mm:thm:even, mm:thm:line and mm:thm:mirror-polygon, except
  the case k = 3 and the coincidence count". For FarFlatExtra.lean and ReplayRepo.lean, give the reasons above. The
  alternative is to cover them.

**M3 (cb). The C3L CNF generator (41 declarations) is not named anywhere.**
- It belongs to unit C3-C2-misc:
  - `RES/C3L/C3Encoding/Gen.lean`, 33 declarations in namespace `C3`: `pairs`, `triples`, `quads`, `perms2`,
    `others`, `key3`, `paritySort`, `rot`, `eps`, `orbits`, the structure `Tables`, `mkTables`, `Tables.s`, `.sig`,
    `.Cl`, `.Tl`, `.invv`, `.Bvv`, `.B`, `.ccw`, `addCl`, `push`, `xor0`, `secSig`, `secSb`, `secPrefix`,
    `secForced`, `secXorB`, `secXorT`, `chainVars`, `secChain`, `numVars`, `baseClauses`;
  - `C3Encoding/Case.lean`: `C3.Layer` (abbrev), `parseLayers`, `layerOrder`, `layerUnits`;
  - `C3Encoding/Emit.lean`: root-namespace `clauseLine`, `body`, `writeCnf`, `main`;
  - `C3L/C3Encoding.lean` has only imports.
- No section names `C3L`.
- The reason for leaving it out exists but is not written: the package states no theorem ("There are no theorems
  yet", `C3L/README.md:16`), and the planned `c3_base_sound` does not exist. CNF encodings are already listed as not
  established (cb, "What is not established here", item (ii)).
- Fix: add an item to cb's "Not covered, deliberately" list (cb.tex:1454ff).

**M4 (cb). The AUDIT2 Lean scripts are not named anywhere.**
- The only declarations are `AUDIT2/A1/A1Dump.lean` lines 5–6, `cube` and `main`: an IO program that dumps V2L/V1L
  data.
- `AUDIT2/A1/A1Audit.lean`, `AUDIT2/A2/Ax.lean`, `AUDIT2/A2/Ax2.lean` and `AUDIT2/A6/scripts/A6Check.lean` contain
  only `#check`, `#print`, `#print axioms` and `#eval` commands for the H3/V1-L/V2-L mirror-class theorems (Stage 2).
- They belong to unit C3-C2-misc, and the document never mentions them. (sr.tex:274 names `C3AUDIT2`, a different
  directory.)
- Fix: one item in cb's Coverage, next to the "Treated in another section" paragraph (cb.tex:1482): "audit scripts
  with no theorems of their own; the audited theorems belong to Stage 2".

## 2. Accuracy of the Coverage paragraphs (all claims checked; no error found)

| sec | claims checked | result |
|---|---|---|
| fd | All 57 declarations of the 9 main-library files of the table are restated, named as counterparts or listed. The reasons hold: `exists_smul_of_det_zero` is `private` and used only at OrientationGeometry.lean:51; `convexIndependent_of_affineIndependent` is used only at Basic.lean:64. | OK |
| ll | Scope lines 1–469 and 1034–1148: 55 declarations, all restated. "Nothing ... deliberately left out" is true. `rotAbout_iterate` (465) is shared with lg, and both sections say so. | OK |
| lg | "All 27 declarations of lines 465–1032 (23 theorems and 4 definitions)": exact. The eight copies of LayerLemma 11–1147 are exact (cmp), and a repository-wide search finds no ninth. `peel_antitone` (460) and `card_peel` (1037, docstring 1036) are exact. Incompleteness: see M1. | OK, M1 |
| oc | OrbitConsistency copied block 39–112, new content from 114, helpers 49–90 and 97–103: exact. The helpers equal LayerLemma 230–308 apart from LayerLemma's two extra lemmas (diff). Merged 1–1147 = LayerLemma. Merged §13 is lines 1149–1383, and 1148–1383 = Linked 1148–1383 = Capstone/Capstone2 1156–1391. Merged 1160–1311 vs OrbitConsistency 273–427 differ only in doc comments (diff: 4 comment hunks). KeyOrder 151–158 are `#print axioms`. The ENCBLEAN copies are byte-identical. All 45 + 12 + 8 declarations are restated or listed. | OK |
| pc | PhaseClassification 40–102 vs LayerLemma 931–996 differ in docstrings only. Linked 1–1384 = Merged 1–1384. Capstone = 18-line header + Linked 11–1416 (19–1424) + blank + PhaseClassification 6–545 (1426–1965) + 1966–2004. Capstone2 1–2003 = Capstone. Offsets +1420 and +8 are right. All 39 + 2 + 3 + 9 declarations are restated. | OK |
| ec | Ranges 1148–1233, 1–123, 1–132, 1–291 and 1–152. Copy 1–1147. `#print` lines 119–123, 127–132, 285–291 and 152. All 7 + 12 + 13 + 13 + 4 declarations are restated. | OK |
| sr | "All 72 declarations": exact. SymmetricReductionAxioms 1–1059 = SymmetricReduction, followed by a blank line and 2 `#print axioms`. AffineReduction 1–1058 is identical. ReviewSanity and VariantChecks 1–1059 are identical. Review files are excluded at file level (79, 13 and 18 own declarations). See m2. | OK, m2 |
| ar | 45 declarations in 1059–1533, all restated. `heptagon_of_nontrivial_isometry` at 997, `iterate_mem` at 69 and `point_ext` at 502 are exact. AffineReductionAxioms = file + blank + 9 `#print axioms` + 1 `#check`. RTC 38–1559 = AffineReduction 12–1533 (+26). | OK |
| mm | Lines 22–1506 hold 5 `cyc*` helpers and 9 polygons. RTC 1562–4236 = MirrorMain 3–2677 (+1559). The ten line numbers of the mb-bound theorems and of `mirror_seven'`/`mirror_eight'` are exact, and the primed theorems have the same statements as `mirror_seven`/`mirror_eight`. `#print axioms` lines 2662–2677. FarFlat's 7 declarations at 12, 15, 34, 55, 60, 67 and 89 are exact, and FarFlat.out prints 5 of the 6 theorems (not `orient_cyclic`). Incompleteness: see M2 and m1. | OK, M2, m1 |
| mb | Part C 4238–4322 (6 theorems, restated). `#check` lines 4312–4316. `MirrorExclusionLineCopy` at RTC 1078. All 79 MirrorMain declarations are restated by mm or mb. All 5 MirrorNine_append declarations are restated. The four big polygons use `cyc7`/`cyc8`, and the small ones use `cyc4`–`cyc6` (grep). | OK |
| cb | C3Cover 29–329 = prelude 1–301; the five other prelude copies are exact. Line ranges 335–365, 367–409, 1720–1733, 413, 423–1717, 1737, 1740–2245, 2247, 2251, 2266–2297 (controls at 2266/70/74/78/82/86/92) and 2301–2327 are exact. Must-fail theorems at 305. RevCtrl_mut has 9 controls; RevCtrl_pass has 2 controls + `rev_parent_decodes`. RevDiff's own declarations are three `def`s (`encN`, `samples`, `line`), so "without theorems of its own" is true. Central34 has 20 declarations, all covered. Incompleteness: see M3 and M4. | OK, M3, M4 |
| sa | 20 + 7 theorems + 1 example = "28 theorems and the one example". Lines 16–80 / 84–103, 6/9/12/15/18/21/24/30 / 33–39, and 6/11/12 are exact. Line counts and the full SHA-256 of all six files are exact. The SizeArith/AssembledSizes names occur in no other Lean file (grep). | OK |

## 3. Declarations of Stage 1 left out on purpose, and whether the reasons hold

| what (section that says so) | reason given | holds? |
|---|---|---|
| Verbatim copies, all diff/cmp-checked SAME (lg, oc, pc, ec, sr, ar, mm, cb):<br>- LayerLemma 11–1147 in 8 files;<br>- Merged §13 in Linked, Capstone, Capstone2 and ENCBLEAN Capstone2;<br>- PhaseClassification 6–545 in Capstone and Capstone2;<br>- SymmetricReduction 1–1058/1059 in AffineReduction, SymmetricReductionAxioms, ReviewSanity, VariantChecks and RTC 38–1084;<br>- AffineReduction in AffineReductionAxioms and RTC 38–1559;<br>- MirrorMain 3–2677 in RTC 1562–4236;<br>- the C3LEAN prelude in C3Cover 29–329 and 5 control/review files | duplicates | yes |
| OrbitConsistency complex helpers (15 declarations, lines 49–90 and 97–103) (oc) | separate constants with the same text as LayerLemma 231–308, which ll restates; not needed | yes |
| `MirrorOdd.mirror_seven'`, `mirror_eight'` (mm, mb) | consistency duplicates | yes (same statements as `mirror_seven`, `mirror_eight`) |
| C3Cover's 7 negative controls; Control_record/Control_sibling (must-fail); RevCtrl_mut (9), RevCtrl_pass (3), RevDiff (3 defs) (cb) | tests and audits | yes |
| SYMLEAN review files ReviewSanity (79 own declarations), VariantChecks (13), SupMetric (18) (sr) | audit files | mostly; see m2 for `group_form` and the converse bridge |
| `MIRRORETV/lean/FarFlat.lean`, 7 declarations (mm) | far-flat lower bound (Theorem B), outside the section; not used | true, but stated per section only (m1) |
| Vendored proofs of `main` and `Config.cap_cup` (mb) | cited published theorems | yes |
| Main-library declarations listed in fd (`conjecturedBound`, the two conjectures, the rational-certificate transfer, the private helper, the conjecture corollaries, the two `insert` variants) | outside the foundations list; not used | yes (checked) |
| `#print axioms` / `#check` / `#eval` lines (ec, cb, mm, mb, oc, sa) | commands, not declarations | yes |
| ES8SLACK Lean files (ec) | out of scope; written proofs in `ES8SLACK/proofs.md` (exists) | yes (excluded by the task) |
| Not listed: tests_tail/VacuityTest tail, MIRRORETV/review, C3L, AUDIT2 | none | M1–M4 |

## 4. Minor findings

- **m1 (mm.tex:950–958).** FarFlat.lean is excluded "for the far-flat lower-bound construction (Theorem B ...),
  which is outside this section". No other section covers it, so the omission is document-wide. Say so ("not
  treated in this document"), and add FarFlat.lean, with FarFlatExtra.lean, to the README list.
- **m2 (sr.tex:1131–1133).** The review files are excluded as "audit files". However, the inventory lists
  `VariantChecks.group_form` (VariantChecks.lean:1168) and `Review.mirrorOneAxis33_iff_exclusionLine`/
  `Review.exclusionLine_of_mirrorOneAxis33` (ReviewSanity.lean:1629/1593) as supporting results, not audits. The
  section's own Remarks sr:rem:variant and sr:rem:mirror-line present them as Lean-checked results, the first
  without any written proof. Name these two results explicitly in the Coverage as not restated, with the reason
  (review file; group form and converse not used by any statement here), or restate and prove them.
- **m3 (front: proofs.tex abstract, fd.tex:3 "Purpose of this document").** The document never says what Stage 1
  covers or what it leaves out. "Stage 1" appears only in the title and once in fd's Coverage ("lie outside
  Stage 1"). The abstract speaks of "parts of its results on symmetric point sets". Stage 2 holds further Lean-checked
  results on symmetric sets: the H3/V1-L/V2-L mirror chain and the ENCBLEAN sixfold k = 8 route. Fix: add a short
  "Scope" paragraph that names the Stage 1 units, the units left to Stages 2 and 3, and ES8SLACK, and points to the
  Coverage paragraphs (or to the README list below) for the Stage 1 files deliberately left out.

## 5. For the README: what the document does not cover

1. **Stage 2 units** (not treated):
   - ENCBLEAN-EncB: encoder B CNF as a Lean program and its soundness;
   - ENCBLEAN-geo: ES8Geo, the polar labelling of counterexamples and the assembly of the sixfold k = 8 route. Its
     byte-identical copies of `Capstone2.lean`, `OrbitConsistency.lean` and `KeyOrder.lean` are covered through the
     LEANEXT originals in sections oc and pc;
   - H-H2: ETVEncoding and D3Encoding, the CNF generators and their soundness;
   - H3-V1L-V2L: `Mir.MirrorExclusionLine` from named CNF-unsatisfiability hypotheses. Section mb proves the
     stronger bound without SAT input.
2. **Stage 3 units** (not treated):
   - COMPACT-CHECKER: the reflective omission-certificate checker for the ES(8) ≤ 311 exclusions;
   - MAIN-LIBRARY-coverage: the main library `ErdosSzekeres`. Exceptions: the foundations restated in section fd,
     and the vendored Baek/ETV and Omission bridge declarations that sections mb and mm restate, use or cite.
3. **Excluded unit files**: `ES8SLACK/review/*` (EarlyVertex.lean, Identity.lean; Composition311.lean and
   TemplateRowsC3.lean were never compiled). Written proofs are in `ES8SLACK/proofs.md`.
4. **Stage 1 declarations left out on purpose** (reasons in the Coverage paragraphs):
   - verbatim copies (§3, first row);
   - the OrbitConsistency complex-coordinate helper copies (15);
   - `mirror_seven'`/`mirror_eight'`;
   - tests, controls and audit files: the 7 C3Cover negative controls, Control_record/Control_sibling, RevCtrl_mut,
     RevCtrl_pass, RevDiff, and the SYMLEAN review files ReviewSanity, VariantChecks and SupMetric. These include
     `VariantChecks.group_form` and the converse bridge `Review.exclusionLine_of_mirrorOneAxis33`;
   - `MIRRORETV/lean/FarFlat.lean` (far-flat Theorem B estimates);
   - the vendored proofs of Baek's theorem and of the cups–caps theorem (cited);
   - `#print`/`#check`/`#eval` commands.
5. **Stage 1 files not yet listed in the document** (findings M1–M4; once fixed they belong under item 4):
   - `LEANEXT/review/tests_tail.lean` (= `VacuityTest.lean` 1149–1297; 19 non-vacuity tests);
   - `MIRRORETV/review/MirrorA.lean`, `MirrorCap.lean`, `FarFlatExtra.lean`, `ReplayRepo.lean`;
   - `C3L/C3Encoding*.lean` (41 definitions of a CNF generator, no theorems);
   - `AUDIT2/*.lean` (audit scripts; two definitions).
