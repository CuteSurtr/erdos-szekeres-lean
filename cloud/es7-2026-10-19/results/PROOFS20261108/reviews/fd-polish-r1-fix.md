# fd, polish round 1: fixer log

Files: `sections/fd.tex` (now 1241 lines) and `sections/fd.map.tsv` (header + 40 rows, unchanged labels, kinds and
order). Snapshot before editing: `snapshots/polish-r1-pre/fd.tex`, `snapshots/polish-r1-pre/fd.map.tsv`.
Line numbers below refer to the new `sections/fd.tex`.

## Compile check (contract wrapper `build/fd_wrapper.tex`, run from `build/`, two passes)

- `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error fd_wrapper.tex`, twice: both exit 0; 16 pages.
- No `!` errors, no "Missing $", no multiply-defined labels.
- Overfull boxes: **0** (none of any size). Underfull boxes: 70, from `\sloppy`/`\raggedright` (cosmetic).
- Undefined references, all export labels of other sections: `ll:def:hv`, `ll:def:peel`, `ll:def:66-70`,
  `oc:lem:perm`, `oc:lem:rot-inv`, and the new `mb:thm:baek` (purpose paragraph).
- No non-ASCII characters, no machine paths, no tool names in `fd.tex` or `fd.map.tsv`.
- Mechanical checks: all 50 `\leanref`s point at a line that carries the declaration keyword and name (the new one,
  `OrbitConsistency.orient_rotAbout_inv`, is `LEANEXT/orbit/OrbitConsistency.lean:117`); the map's `lean_name` /
  `file_line` equal the `\leanref`s of every non-remark head; map rows and environments agree in label, kind and order
  (9 definitions, 23 lemmas, 8 remarks); every `\ref{fd:...}` target exists; all 20 contract export labels are
  defined once.
- sympy (`build/fd_polish_r1/check_polish.py`, all OK): `D3.reflC` with u = (cos phi, sin phi) equals o + F_phi(x - o);
  the Mathlib affine-map identity f(w+p) = A w + f(p) for f(x) = Ax + v; the identity of `Review.orient_rotAbout`
  (= Lemma fd:lem:rot(e)); `rotAbout c th c = c`; `exposed_not_in_hull` as the easy direction of separation with
  l(z) = -(A z0 + B z1).

## Findings of round 2 (and open items of round 1)

| report, id | summary | action | location after the fix / reason |
|---|---|---|---|
| fd-r2-fidelity m1 | Coverage filed the forward-direction special cases `HasConvexNGon.linearEquiv`, `Suk.generalPosition_reflectY` under the reverse directions of fd:lem:affine-cp | fixed | Coverage, written steps, fd:lem:affine-cp entry, lines 1202-1206: only `Suk.hasConvexNGon_of_reflectY` is given as a reverse-direction special case; the other two are named as forward-direction special cases of Remark fd:rem:affine-cp-lean |
| fd-r2-fidelity m2 | Coverage scope sentence ignored research theorems named only as axioms evidence | fixed | lines 1236-1239: scope = declarations named in the statements, remarks or proofs; evidence-only theorems and the other declarations are treated elsewhere or lie outside Stage 1 |
| fd-r2-fidelity m3 | definition of Lean-checked excluded native_decide-based theorems (contract rules 6, 8) | fixed | rigor labels, lines 51-56: `Lean.ofReduceBool`, `Lean.trustCompiler` allowed for such a declaration and named by the citing section; none in fd |
| fd-r2-fidelity m4 | fd:lem:inv-image(c) stated for R^2 while `iterate_mem` is for an arbitrary type | fixed | lines 351-359: the lemma now fixes an arbitrary set X, f: X -> X, finite S; (a),(b) take X = R^2 (Invariant is defined for maps of the plane); (c) is the Lean statement; map row updated |
| fd-r2-fidelity m5 | AffineReductionAxioms.lean also has one `#check` | fixed | lines 215-217: "followed by nine #print axioms commands and one #check command" (checked: 1533 identical lines, then 9 + 1) |
| fd-r2-fidelity m6 | map notes: rot row omitted rho_0 = id; pos-triples row described decide incompletely | fixed | map rows fd:lem:rot and fd:lem:pos-triples |
| fd-r2-fidelity m7 | `conjecturedBound` is a bound function, not a conjecture | fixed | lines 1222-1225: "the bound function conjecturedBound (n -> 2^max(n-2,0)+1) and the open conjectures ..." |
| fd-r2-rigor m1 | `LAYERLEAN/logs/build.log` was made for an earlier LayerLemma.lean | fixed | lines 198-205: compile evidence is now `LEANEXT/review/REPORT.md` item 1 (file afb8542d, 1148 lines, exit 0, no messages) and `LAYERLEAN/logs/axioms_recheck_20261106/out.txt` (exit status 0; first 1148 lines byte-identical, checked with diff; only Lean output = 19 axiom lines); build.log is not used ("does not name the hash"); conventions example, lines 28-30, now cites the recheck README |
| fd-r2-rigor m2 | evidence rule should say "whose statement or proof uses it" | fixed | lines 56-59 |
| fd-r2-rigor m3 | Coverage forward/reverse inconsistency | duplicate of fd-r2-fidelity m1 | lines 1202-1206 |
| fd-r2-rigor m4 | Mathlib AffineMap characterization used without Mathlib's definition; "matrix of the linear part"; AffineEquiv undefined | fixed | fd:def:conv, head line 287 and lines 296-304 (Mathlib definition f(w+p) = f.linear(w) + f(p), derivation of f(x) = A_f x + f(0) and of the converse, AffineEquiv defined; checked against the pinned Mathlib source); proof of fd:lem:affine-cp refers to it, lines 858ff, 866-868 |
| fd-r2-rigor m5(i) | "No Lean declaration states ..." literally false (Mathlib `collinear_iff_of_mem`, `AffineMap.image_convexHull`) | fixed | lines 1178-1184, rewritten (see also "other changes" 1: the old universal claims were false for project declarations too) |
| fd-r2-rigor m5(ii) | `exposed_not_in_hull` (variant of the easy direction of separation) not named | fixed | lines 1207-1211 (statement of the Lean theorem); axioms evidence: audit line 529, lines 177-179 (line checked) |
| fd-r2-rigor m5(iii) | rho_0 = id missing from the Coverage list of written steps | fixed | line 1194 |
| fd-r2-rigor m6 | `#check` omitted | duplicate of fd-r2-fidelity m5 | lines 215-217 |
| fd-r2-rigor m7 | `b` used for Lean's translation vector next to the point b; `f` reused for an AffineEquiv | fixed | translation vector renamed w with "(Lean's b)": lines 538-541, 563, 808-809, 862; the affine equivalence is now phi: lines 813-814, 866-872; map rows say so |
| fd-r2-rigor m8 | path rule names `cloud/es7-2026-10-19/results` although `cloud/` is not a root prefix | fixed | lines 25-27: "the research-records directory, whose path from the repository root is cloud/es7-2026-10-19/results" |
| fd-r2-adversarial m1 | fd:lem:affine-orient(i) is exactly `OrbitConsistency.orient_rotAbout_inv` but was tagged written step | fixed | head line 532 tags (i) with `\leanref{ErdosSzekeres.OrbitConsistency.orient_rotAbout_inv}{LEANEXT/orbit/OrbitConsistency.lean:117}`; (i) quantifiers reordered as in Lean (o, theta, a, b, d), line 544; Remark fd:rem:affine-orient-lean rewritten, lines 577-585 (copy of rotAbout, centre c); Coverage covered list line 1156-1157; written-steps entry now only (ii), line 1186-1191; map rows fd:lem:affine-orient and fd:rem:affine-orient-lean; axioms evidence already cites `LEANEXT/orbit/logs/axioms.log` line 1 ("named in this section", line 232) |
| fd-r2-adversarial m2 | `LEANEXT/orbit/logs/build.log` records only the exit code | fixed | lines 228-231: the log contains only the exit code; `LEANEXT/orbit/REPORT.md` line 3 identifies the file (429 lines, SHA-256 9b843180, current; checked) |
| fd-r2-adversarial m3 | `#check` omitted | duplicate of fd-r2-fidelity m5 | lines 215-217 |
| fd-r2-adversarial note 1 | `Suk.reflectY_x`, `reflectY_y` probably covered by audit line 176 (and 178) | declined | they are rfl lemmas used through `simp only`; such lemmas need not occur in the proof term, so coverage by `#print axioms` cannot be asserted (fd-r2-claims note 1 says the same); the hedged sentence ("not covered by a printed line that we identified", lines 185-188) is accurate and the stated fallback evidence is sound |
| fd-r2-adversarial note 2 | optional pointer to `exposed_not_in_hull` | duplicate of fd-r2-rigor m5(ii) | lines 1207-1211 |
| fd-r2-claims m1 | affine-orient(i) exact counterpart; Coverage lists composition law but not rho_0 = id | duplicate of fd-r2-adversarial m1 and fd-r2-rigor m5(iii) | see those rows |
| fd-r2-claims m2 | purpose paragraph omits cited published theorems (Baek) and generality differences | fixed | lines 10-17: two exceptions (computer-assisted; cited published theorems, e.g. Theorem mb:thm:baek, not reproved) and "a convenient variant ... is labelled as a variant"; the inv-image instance is fixed by fd-r2-fidelity m4 |
| fd-r2-claims m3 | `#check` omitted | duplicate of fd-r2-fidelity m5 | lines 215-217 |
| fd-r2-claims m4 | bare `:N` shorthand undefined | fixed | lines 35-36: "A bare :N written after a file has been cited refers to line N of that file" |
| fd-r2-claims note 1 | `reflectY_reflectY` probably covered by audit line 178 | declined | same reason as fd-r2-adversarial note 1 (simp use of a lemma need not leave it in the proof term); the hedged sentence stays |
| fd-r1-rigor M12 (informational) | fd helper labels (fd:lem:rot, fd:lem:small, ...) are not export labels | declined | the export list is fixed by the contract; a section cannot add export labels. The labels remain defined, so the orchestrator can export them by a contract change |

Round-1 findings fixed in round 1 and confirmed fixed by round 2 (no action this round): fd-r1-fidelity F1-F9;
fd-r1-rigor M1-M11, M13; fd-r1-adversarial m1-m9; fd-r1-claims M1, m1-m8 (a)-(e). The confirmations are in
fd-r2-fidelity §1, §3, §5, fd-r2-rigor §1, §3, §5, fd-r2-adversarial §1-3 and fd-r2-claims §1-2 (path rule and root
files, keyword rule, namespace rule, evidence lines 725/732/720/624/132/49/178, SMT wording, map rows, Reflection.lean
coverage, computer-assisted label, Rudin references, base case, MirrorMain.out:858, VALIDATION.md:73, orient3_perm,
0 overfull boxes, tactic wording, LayerLemma.lean:165). The writer-concerns file lists no overfull boxes; there are
still none.

## Other changes (not requested by a finding)

1. **Coverage, written steps: false universal claims removed** (lines 1178-1219). The old text said "No Lean
   declaration states the following ... ; where Lean has a special case or a partial counterpart, it is named". A search
   of the research records shows this was false: `SYMLEAN/review/ReviewSanity.lean` states rho_theta(c) = c
   (`SymReduction.Review.rotAbout_center`, :1086) and the identity of fd:lem:rot(e)
   (`SymReduction.Review.orient_rotAbout`, :1091, with `eDist2 p c`); `H2/D3Encoding/Geometry.lean:87`
   (`D3.orient_reflC`) states fd:lem:affine-orient(ii) with a unit direction vector instead of the angle (identity
   checked with sympy); many further orient lemmas exist (e.g. `ErdosSzekeres/Omission/CycleSigns.lean`
   swap/reverse lemmas, `MirrorOdd.orient_rev`, `MirrorOdd.orient_mir3`). New text: "We found no declaration in the files
   of the table of sources that states one of them in the form given here" (checked by enumerating the declarations of
   LayerLemma, SymmetricReduction, OrbitConsistency and by keyword searches of AffineReduction, MirrorMain,
   ReductionThreeClasses and the nine main-library files), an explicit statement that the list of counterparts is not
   complete, the exact counterparts above named, and the reason the two review-file lemmas are not cited as
   Lean-checked (no theorem whose axioms `SYMLEAN/logs/ReviewSanity.out` prints uses them; checked by text search: neither
   is referenced elsewhere in the file except `orient_rotAbout` inside the unprinted `orient_rot5_pos`; neither has a
   simp attribute). Added: "Naming a counterpart does not make a written step Lean-checked ...; we give axioms evidence
   for such a counterpart only where we say so."
2. **Rigor-label rule** (lines 76-79): "a part marked written step does not carry this label, even where the text names
   a Lean counterpart of it elsewhere" (was "is not [Lean-checked]", which read as a claim about Lean).
3. **Header of the list of other named declarations** (lines 1211-1219): the old header "named only in remarks or in
   proofs" was inaccurate (`LayerLemma.invariant_erase_centre` is named in a statement; `Sixfold66` etc. are named in a
   remark but were not meant to be listed). New header: declarations named "as Lean counterparts, as definitions and
   lemmas that these rely on, or as the location of a proof step"; `OrbitConsistency.orient_rotAbout_inv` moved to the
   covered list; `D3.orient_reflC`, the two Review lemmas and `exposed_not_in_hull` added.
4. **`--wfail` typesetting** (line 190): `\texttt{lake build --wfail}` printed an en dash; now `-{}-`.
5. **`forces_triangle`** (lines 1233-1234): "not used here" -> "not used by the facts of this section;
   forces_triangle is named above only in the axioms evidence".
6. **fd:lem:affine-orient hypotheses** (line 533): reordered to g, A, v as in Lean (g, L, b); no change of meaning.
7. **Axioms paragraph**: "the theorems of that file" -> "of LAYERLEAN/LayerLemma.lean" (line 206), since the previous
   sentence now cites other records; orbit axioms log described as listing "the two theorems of that file named in this
   section" (line 232; `orient_rotAbout_inv` is now in a head).
8. **Map** (`sections/fd.map.tsv`): rows fd:def:conv (AffineEquiv, Mathlib definition), fd:lem:inv-image (arbitrary set),
   fd:lem:rot (rho_0 = id; counterparts in Coverage), fd:lem:affine-orient (second name and line
   `ErdosSzekeres.OrbitConsistency.orient_rotAbout_inv`, `LEANEXT/orbit/OrbitConsistency.lean:117`; w for Lean's b),
   fd:rem:affine-orient-lean (note), fd:lem:affine-cp (w, phi), fd:lem:pos-triples (decide uses),
   fd:lem:separation (exposed_not_in_hull). 41 lines, 5 tab-separated fields each.

## Notes for the orchestrator

- The new evidence sentence for `exposed_not_in_hull` (audit line 529) is covered by the paragraph's statement that
  every main-library file named there is unchanged since `7f0868fdb`. I did not run git (not on the allowed command
  list). This rests on the round-2 adversarial reviewer's read-only git check ("7f0868fdb ... the last commit touching
  ErdosSzekeres/"), and the file's current SHA-256 (`f55a711e7aa9...`) equals the hash recorded for it in
  `docs/validation/source-manifest-cover-2026-10-10.json` and the other 10 October validation records.
- Sections `ll` and `lg` cite `LAYERLEAN/logs/build.log` as the compile record of the current LayerLemma.lean (round-2
  rigor m1, cross-section note); current-file records are `LEANEXT/review/REPORT.md` item 1 and
  `LAYERLEAN/logs/axioms_recheck_20261106/out.txt`.
- Round-2 fidelity m3 says some research files "contain native_decide". The hits I checked (`H/ETVEncoding`, `V1-L`,
  `V2-L`, `ENCBLEAN`) are all in comments that say native_decide is not used. fd makes no claim about the research
  records as a whole, only that no declaration cited in fd uses it.
- fd now references `mb:thm:baek` (an mb export label) in the purpose paragraph.
