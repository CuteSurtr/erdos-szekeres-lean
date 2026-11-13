# lg, round 1, lens: fidelity

Section file: `sections/lg.tex` (854 lines). Map: `sections/lg.map.tsv` (31 rows).
Lean source: `LAYERLEAN/LayerLemma.lean` (SHA-256 afb8542dceb0..., 1148 lines; hash re-computed and matching).

**Verdict: PASS.** There are no blocker or major findings. All 27 in-scope declarations are stated faithfully, at the
exact cited lines. Five minor findings follow.

## What was checked

1. **Every Lean-cited head against the Lean source.** For each of the 27 declarations I opened the cited line and
   compared the following:
   - hypotheses and their order;
   - the conclusion;
   - types (Finset vs Set, ℕ vs ℝ, casts);
   - natural-number subtraction (`m - 1`, `K - 1`, `i - 1`) and the natural-number quotient `m / 2`;
   - strict vs weak inequalities;
   - maps-into (`Invariant`) vs equality.

   The table below lists the result for each one.
2. **Heads, map and Lean lines.** A script compared the `\leanref` heads with the map rows and with the Lean file
   (`lg_fid_checks/heads.py`, a scratch script that is not kept):
   - 31 statement environments in the tex, 31 map rows;
   - kinds and written-step tags agree;
   - every Lean name sits exactly on its cited line (offset 0).
3. **Definitions used.**
   - `lin`, `dist2`, `fanPt` and `polar` are restated verbatim.
   - `rotAbout` (via fd:def:rot), `orient` (Orientation.lean:9), `hullVerts`/`peel` (via ll), `orbitFS` (:48) and
     `Invariant` (maps into) match Lean.
4. **Borrowed facts.** (L1)–(L4) and the fd facts used match the statements in `ll.tex` (ll:lem:hv(c),
   ll:lem:antitone, ll:lem:inv-peel, ll:thm:core-rot, ll:lem:minperiod) and in `fd.tex` (fd:lem:orient(b),
   fd:lem:collinear(b), fd:lem:mono(c), fd:lem:pos-triples). The Lean sources of these facts match too
   (LayerLemma.lean:146, 386, 364, 460; OrientationGeometry.lean:66; Suk/OrientationClique.lean:9).
5. **Identities, checked with sympy 1.13.3** (`lg_fid_checks/ids.py`). All return 0:
   - orient_rotAbout, as a pure polynomial identity with no trigonometric simplification, which confirms the
     "Lean proves it by ring" remark;
   - trig_layer and the intermediate line of its proof;
   - lin_rotAbout (the identity behind lin_orbit_pos);
   - orient_polar, and det(r e(φ), s e(ψ)) = rs sin(ψ−φ);
   - the key identities of orient_trans_halfplane (lg:eq:trans), fan_step (lg:eq:fanstep) and lin_pos_of_peel
     (lg:eq:key);
   - orient_eq_lin;
   - the Cramer identity, coordinatewise and both corollaries, including the 3×3 expansion used in its proof;
   - each orient = det(...) substitution in the proofs of fan_step and lin_pos_of_peel;
   - the rule-B decomposition r_a(r_b−r_d)sin x + r_d(r_b−r_a)sin y + r_ar_d(sin x+sin y−sin(x+y));
   - the disk identity u|A|²+v|B|²−|uA+vB|² = uv|A−B|² for u+v = 1;
   - (O4) affinity;
   - rotation composition and distance;
   - rotAbout(c,π)p = 2c−p and orient(p,c,2c−p) = 0;
   - the closed form 4|x−c|² sin t sin jt sin(j−1)t;
   - the (m−1)t = π−t substitution;
   - the J identities (lg:eq:J).

   A numeric spot check (m ≤ 12, all j ≤ m; `lg_fid_checks/num.py`) confirms the closed form, the nonnegativity for
   j ≤ m, and the zero set {1, m} in the remark after Lemma lg:lem:regular.
6. **Export labels (contract table).** All 13 are defined, on the right declarations:
   lg:lem:orient-rot, lg:lem:regular, lg:thm:nesting, lg:lem:centre, lg:thm:fan, lg:lem:halfplane, lg:thm:chain,
   lg:def:polar, lg:lem:polar, lg:lem:ruleA, lg:lem:sinadd, lg:lem:ruleB, lg:thm:radius. See finding m2 on
   "with trig_layer".
7. **References.**
   - All `\ref`s to other sections go to allowed export labels: fd:def:{point, orient, gp, cp, ngon, inv, rot},
     fd:lem:{orient, collinear, mono, pos-triples}, and ll:{def:hv, def:peel, lem:hv, lem:antitone, lem:inv-peel,
     thm:core-rot, lem:minperiod, thm:card-peel}.
   - Every one of these labels exists in fd.tex or ll.tex.
8. **Compile.** The check ran on a private copy, so the writer's build directory was not touched. Two pdflatex runs
   exit 0. There are no errors, no "Missing", no overfull boxes, and the only undefined references are the expected
   fd:/ll: ones.
9. **Hygiene.** There are no machine paths and no tool names in lg.tex or lg.map.tsv. There is no
   `\newcommand`, `\usepackage`, `\def` or `\begin{document}`.
10. **Factual claims in Sources, Axioms and Coverage.**
    - All 9 quoted SHA-256 prefixes match the files.
    - build.log: exit 0, no messages.
    - LayerLemma.lean contains no sorry, admit, axiom or native_decide (grep).
    - lakefile.toml has defaultTargets = ["ErdosSzekeres"], so the file is not in the default target.
    - axioms.log covers exactly 16 of the 23 in-scope theorems. The 7 listed exceptions are exactly the missing ones.
    - LEANEXT/review/axioms.log covers all 23. Its 59 names are exactly the 59 non-@[simp] `theorem` declarations
      of the file (diffed).
    - The re-check out.txt covers exactly 11 of the 23.
    - All of these logs show only [propext, Classical.choice, Quot.sound].
    - peel_antitone is at :460, and card_peel at :1037 with its docstring at :1036.
    - The four files named as verbatim copies do contain lines 11–1147 verbatim (diffed). See finding m1.

## Per-declaration comparison (all faithful)

| tex label | Lean name | cited line | result |
|---|---|---|---|
| lg:lem:rot-iter | rotAbout_iterate | 465 | exact (j cast to ℝ) |
| lg:lem:orient-rot | orient_rotAbout | 472 | exact |
| lg:lem:trig | trig_layer | 480 | exact |
| lg:lem:regular | orient_regular_nonneg | 488 | exact: 0<m, j≤m, weak 0≤, no x≠c |
| lg:def:lin | lin | 625 | exact |
| lg:lem:lin-rot | lin_rotAbout | 794 | exact (c−p coordinatewise) |
| lg:lem:lin-orbit | lin_orbit_pos | 801 | exact: p≠c, 0<m, 0<j, j<m, strict |
| lg:lem:next-prev | orient_next_prev_pos | 830 | exact: p≠c, 3≤m, ρ^{m−1} with ℕ-subtraction |
| lg:lem:halfplane-convex | convex_orient_nonneg | 516 | exact (Set, closed half-plane) |
| lg:def:dist2 | dist2 | 999 | exact |
| lg:lem:disk | convex_disk | 1002 | exact (any R ∈ ℝ) |
| lg:thm:nesting | strict_nesting | 529 | exact: 2≤m, K≤2m, c∉S, Invariant, K-free, GP, n<n', strict |
| lg:lem:centre | centre_not_mem_of_even | 582 | exact: 0<m, Even m, Invariant, GP, p∈S, p≠c; no K, no c∉S |
| lg:thm:radius | dist2_le_of_later | 1012 | exact: 0<m, K≤2m, c∉S, Invariant, K-free, n≤n' (weak), no GP |
| lg:lem:trans | orient_trans_halfplane | 629 | exact (c generic, noted) |
| lg:lem:fan-step | fan_step | 641 | exact (same 5 hypotheses, same order) |
| lg:lem:orient-lin | orient_eq_lin | 653 | exact |
| lg:lem:fan-pos | fan_positive | 658 | exact (H/F/T ranges and both conclusions) |
| lg:def:fanpt | fanPt | 694 | exact (Fin (n+1), implicit n) |
| lg:thm:fan | hasConvexNGon_of_fan | 700 | exact: 3≤n, p∈S, q_s∈S for s<n, H/F/T; HasConvexNGon (n+1) S |
| lg:lem:halfplane | lin_pos_of_peel | 864 | exact: 3≤m, K≤2m, c∉S, Inv, K-free, GP, p∈hv(peel S i), y∈peel S i, y≠p |
| lg:thm:chain | chain_clauses_sound | 914 | exact: 3≤m, 4≤K, K≤2m, ...; ranges s<K−1, s+1<K−1, s+2<K−1; False |
| lg:def:polar | polar | 932 | exact (no sign condition) |
| lg:lem:polar | orient_polar | 935 | exact |
| lg:lem:ruleA | orient_polar_centre_inside | 943 | exact (six angle bounds, three positive radii) |
| lg:lem:sinadd | sin_add_lt | 956 | exact |
| lg:lem:ruleB | orient_polar_halfplane | 974 | exact (r_a≤r_b, r_d≤r_b weak; no r_b>0 hypothesis) |

The coverage of the inventory's scope is complete:
- headline: strict_nesting, centre_not_mem_of_even, chain_clauses_sound, orient_polar, orient_polar_centre_inside,
  orient_polar_halfplane, dist2_le_of_later;
- supporting: the remaining 16 theorems;
- definitions: lin, fanPt, polar, dist2.

## Findings

### m1 (minor): the Coverage list of verbatim copies is incomplete

- **Location.** lg.tex:848–853.
- **Text.** "the verbatim copies of these declarations in other units ... each of the following files contains lines
  11–1147 of LAYERLEAN/LayerLemma.lean verbatim: [4 files]".
- **What is wrong.** The sentence reads as a complete list of the verbatim copies. Diffing the block of 1137 lines
  shows four more files that contain it verbatim:
  - LEANEXT/capstone/Capstone.lean (from line 19);
  - LEANEXT/linked/Linked.lean (from line 11);
  - LEANEXT/review/VacuityTest.lean (from line 11);
  - LAYERLEAN/logs/axioms_recheck_20261106/LayerLemmaAxioms.lean, whose first 1148 lines are byte-identical to the
    file (cmp).
- **Impact.** None on the validity of the coverage, since duplicates are a valid reason.
- **Fix.** Add these files, or write "for example".

### m2 (minor; I am not sure this is required): lg:lem:regular does not include trig_layer

- **Location.** lg.tex:238 and 254.
- **Contract.** The contract assigns "`lg:lem:regular` orient_regular_nonneg (with trig_layer)". Other "X (with Y)"
  entries (for example ll:lem:hv) put Y in the same labelled statement.
- **Section.** Here lg:lem:regular sits on orient_regular_nonneg alone, and trig_layer is a separate Lemma
  lg:lem:trig.
- **Impact.** No other section `\ref`s lg:lem:regular (grep over all sections), so nothing breaks, and trig_layer is
  fully covered.
- **Fix, if the orchestrator reads the contract strictly.** Add a second `\leanref` for trig_layer to the head of
  lg:lem:regular, or state in Coverage that trig_layer is Lemma lg:lem:trig.

### m3 (minor): the overview credits the fan theorem with a stronger conclusion than Lean states

- **Location.** lg.tex:17–19.
- **Text.** "a pivot followed by n≥3 chain points ... is a convex (n+1)-gon (Theorem lg:thm:fan)".
- **Lean.** The Lean conclusion is only `HasConvexNGon (n + 1) S`, that is, *some* (n+1)-subset of S is in convex
  position. The statement environment itself is faithful (line 606–607).
- **Why minor.** The stronger fact is true and is shown by the written proof, and the remark at lines 632–635 says
  "the proof shows". The overview sentence attributes it to the theorem anyway.
- **Fix.** Write "contains a convex (n+1)-gon", or cite "Theorem lg:thm:fan and the remark after it".

### m4 (minor, style): item labels (i)–(iv) clash with the layer index i

- **Location.** Theorem lg:thm:chain, lg.tex:694–704.
- **What is wrong.** Item (i) reads "q_s ∈ peel(S,i)", and the proof says "by (i)" in a sentence that also uses the
  index i.
- **Fix.** Rename the items to (C1)–(C4) or (a)–(d).

### m5 (minor, nit): REPORT.md does not use the gloss "non-simp"

- **Location.** lg.tex:46–48.
- **Text.** "which according to LEANEXT/review/REPORT.md covers all 59 non-simp theorems of the reviewed file".
- **What is wrong.** REPORT.md says only "All 59 theorem declarations were checked". It does not say "non-simp".
- **Why minor.** The gloss is correct. I checked that the 59 names in LEANEXT/review/axioms.log are exactly the 59
  non-@[simp] `theorem` declarations; the file has 66 in all, 7 of them @[simp]. Only the attribution is loose.
- **Fix (optional).** Write "covers all 59 theorem declarations (the file's non-simp theorems)".

## No blocker or major findings

- No statement differs from its Lean declaration.
- No line number is off.
- No label is missing.
- No `\ref` is disallowed.
- The section compiles.
- No rigor label is overclaimed: every written step is tagged "written step", and every Lean-backed statement is
  labelled Lean-checked, with the logs named correctly.
