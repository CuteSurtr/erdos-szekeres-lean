# Review ll, round 1, lens: fidelity

Section: `STAGE/sections/ll.tex` (761 lines), map `STAGE/sections/ll.map.tsv` (31 rows).
Lean source: `LAYERLEAN/LayerLemma.lean` (1148 lines, SHA-256 `afb8542dceb0c17005b4eccec1b79abbb57099c0768e1a4bbb1cf52ad797257f`, recomputed: matches).

**Verdict: PASS** (no blocker, no major; 6 minor findings below).

## 1. Method

- Read the contract, the inventory `STAGE/inventory/LAYERLEAN.json` (main results, outlines, risks), the whole section and
  map, `LayerLemma.lean` lines 1-1148 (scope 1-469 and 1034-1147 in detail, 470-1032 for context, in particular
  `centre_not_mem_of_even` at 582), `ErdosSzekeres/Definitions.lean`, `ErdosSzekeres/Basic.lean`,
  `ErdosSzekeres/Orientation.lean`, the LAYERLEAN logs, `LEANEXT/review/{axioms.log,REPORT.md}`, the heads of
  `C6UPPER/README.md` and `C7UPPER/README.md`, the ENCBLEAN README, `WRITEUP/note/k8_soundness.tex` (lines 1-135) and
  `SYM5/README.md` lines 60-80.
- Mechanical checks (scripted): every `\leanref{Name}{File:Line}` (55 of them) against the Lean file; every `\ref`
  target against the section's own labels, the contract's `fd:` list and the `lg:` export list; map rows against the
  statement environments (label, kind, Lean names, lines, column count); the declarations of the scoped line ranges
  against the Coverage paragraph; forbidden paths/tool names/macros; a compile in a separate wrapper
  (`STAGE/build/ll_fidr1_wrapper.tex`, `nice -n 15 pdflatex` twice).
- Statement-by-statement comparison of hypotheses, conclusion, quantifier order, types and casts (table in section 2).
- Checked Mathlib's `Set.extremePoints` at the pinned revision `f897ebcf72` (it is
  `{x ∈ A | ∀ x₁ ∈ A, ∀ x₂ ∈ A, x ∈ openSegment 𝕜 x₁ x₂ → x₁ = x}`), against convention (C4).

## 2. Statement-by-statement fidelity (all names exist at exactly the cited line)

| label | Lean (line) | result |
|---|---|---|
| ll:def:orbit | orbitFS (48) | exact: image of `range p` under `i ↦ f^[i] x`; empty for p = 0 noted |
| ll:lem:orbit (a)-(f) | iterate_mem 52, mem_orbitFS_self 59, orbitFS_subset 62, orbitFS_invariant 68, card_orbitFS_of_minimalPeriod 80, mem_orbitFS_of_not_disjoint 91 | exact (hypotheses 0<p, f^[p] x = x, f^[p] y = y, ¬Disjoint; card for minimalPeriod = p incl. p = 0) |
| ll:def:inv | Invariant (105) | exact: maps into |
| ll:def:hv | hullVerts (111) | exact: filter of S by x ∉ conv(S \ {x}) |
| ll:lem:hv-basic | mem_hullVerts 114, hullVerts_subset 118 | exact |
| ll:lem:hv (a)-(d) | convexPosition_hullVerts 121, extreme_mem_hullVerts 130, subset_convexHull_hullVerts 146, hullVerts_nonempty 139 | exact; (C4) matches Mathlib's `Set.extremePoints` at the pin |
| ll:lem:map-hv | map_mem_hullVerts (162) | exact: `Point →ᵃ[ℝ] Point`, injective, maps-into |
| ll:thm:core | hullVerts_eq_orbitFS (189) | exact: injective affine f, 0<m, K≤2m, maps-into, minimalPeriod f y = m on S, ¬HasConvexNGon K S, ∀ x ∈ hv(S); Finset equality; no general position |
| ll:lem:inv-sdiff | invariant_sdiff_hullVerts (217) | exact (0<m, maps-into, f^[m] y = y on S) |
| ll:def:complex | toC 231, ofC 234, crot 252 | exact |
| ll:lem:complex (a)-(g) | toC_re 236 … crot_injective 287 (13 names) | exact (w ≠ 1 in (f), w ≠ 0 in (g), k ∈ ℕ in (e)) |
| ll:def:rot | rotAbout (298) | exact coordinate formula; (C7) cast/division-by-0 convention stated |
| ll:lem:rot (a)-(d) | rotAbout_eq_crot 302, rotAff 311 (def), rotAbout_injective 319, rotAbout_iterate 465 | exact; rotAff's linear part `Matrix.toLin' !![cos,−sin;sin,cos]` = column-vector action, as stated; j cast to ℝ in (d) |
| ll:lem:erase | invariant_erase_centre (325) | exact (any real θ) |
| ll:lem:minperiod | minimalPeriod_rotAbout (336) | exact (0<m, y ≠ c, angle `2*π/(m:ℝ)`) |
| ll:thm:core-rot | hullVerts_eq_orbitFS_rotAbout (364) | exact (0<m, K≤2m, c ∉ S, Invariant, K-free, ∀ x ∈ hv(S)) |
| ll:def:peel | peel (374) | exact |
| ll:lem:peel-basic | peel_succ 378, peel_subset 381 | exact |
| ll:lem:antitone | peel_antitone (460) | exact (n ≤ n' ⇒ peel S n' ⊆ peel S n) |
| ll:lem:inv-peel | invariant_peel (386) | exact (0<m, c ∉ S, Invariant; ∀ n) |
| ll:thm:layers | layers_are_orbits (402) | exact: ∃ x ∈ peel S n with (a) equality, (b) card = m, (c) weak containment in conv |
| ll:lem:exists-layer | exists_layer (419) | exact, no other hypotheses |
| ll:thm:card-peel | card_peel (1037) | exact incl. truncated `m * (t - 1) < S.card` and ∀ n ≤ t |
| ll:cor:decomp | written step | correctly labelled "written step", not presented as Lean |
| ll:thm:reduction | convexNGon_of_layers (1066) | exact: (H) with the same hypothesis order, size bound on `S.erase c`, c ∈ S allowed, truncated t∸1 |
| ll:def:66-70 | Sixfold66 1102, Sevenfold70 1107 | exact (real numerals 6, 7 noted; 66, 70; c ∉ T) |
| ll:thm:sixfold | sixfold_octagon (1113) | exact: hypothesis Sixfold66 stated in the statement; 61 ≤ \|S\|; no c ∉ S hypothesis |
| ll:thm:sevenfold | sevenfold_octagon (1136) | exact: hypothesis Sevenfold70; 65 ≤ \|S\|; centre allowed |

No strengthening or weakening found. Strict/weak inequalities, maps-into vs equality, `Finset` vs `Set` coercions,
ℕ vs ℝ casts and truncated subtraction all agree with Lean.

## 3. Coverage and export labels

- All 15 export labels of the contract row `ll` are defined on the named statements (ll:def:hv, ll:def:peel, ll:lem:hv
  with all four declarations, ll:lem:minperiod, ll:thm:core, ll:thm:core-rot, ll:lem:inv-peel, ll:thm:layers,
  ll:lem:exists-layer, ll:lem:antitone, ll:thm:card-peel, ll:thm:reduction, ll:def:66-70, ll:thm:sixfold,
  ll:thm:sevenfold).
- Every declaration in lines 1-469 and 1034-1147 (55 declarations: 11 defs and 44 theorems, one `\leanref` each) is
  covered by a labelled statement; the Coverage paragraph lists them all and correctly states that nothing in scope is
  left out.
- `\ref` targets: only own labels (all defined), the allowed `fd:` labels (fd:def:point, gp, cp, ngon, inv, rot;
  fd:lem:cp-hull, mono, collinear, affine-cp) and `lg:` export labels (lg:thm:nesting, lg:lem:centre). None disallowed.
- Map: 31 rows = 31 statement environments; header and 5 tab-separated columns correct; kinds, Lean names and lines
  agree with the heads in the same order.
- Compile: exit 0 on both passes; the only undefined references are `fd:`/`lg:` ones (expected). No forbidden paths,
  tool names, `\newcommand` or `\usepackage`.

## 4. Record and evidence claims checked

- SHA-256 of `LayerLemma.lean` (afb8542d…) and of `ErdosSzekeres/Definitions.lean` (2425500eefd1…): match.
- `LAYERLEAN/logs/build.log`: exit 0, no messages; Lean 4.24.0 (`lean-toolchain`), Mathlib f897ebcf (manifest): match.
- `axioms.log` 28 theorems, `axioms_recheck_20261106/out.txt` 19 theorems, all three standard axioms; the first 1148
  lines of `LayerLemmaAxioms.lean` are identical to `LayerLemma.lean` (diff empty): match.
- `LEANEXT/review/axioms.log`: 59 names = all non-`@[simp]` theorems of the file (59 + 7 `@[simp]` = 66), every
  theorem of this section among them, `iterate_mem` with [propext, Quot.sound]: match.
- Only `decide` at line 1125 (`Even 6`); no sorry/admit/axiom/native_decide: match.
- Remark ll:rem:hyp: C6UPPER (cube formulas, cover checks, cake_lpr verdicts; written encoder soundness in
  `WRITEUP/note/k8_soundness.tex`, which covers both C6UPPER and C7UPPER per its line 2), C7UPPER (two encoders, each
  with a cake_lpr verdict), and ENCBLEAN (`EncB.Geo.sixfold66_of_cubes64 : CubesUnsat64 → Sixfold66`, README line
  223): accurate. No Lean file proves `Sixfold66`, `Sevenfold70`, `Fivefold35` or `Fourfold32` unconditionally (grep).
- Sixfold66/Sevenfold70 are presented as hypotheses in the statements of ll:thm:sixfold/ll:thm:sevenfold and in
  Remark ll:rem:hyp (rule 7 satisfied); real-cast numerals explained in Remark ll:rem:numerals (`exact_mod_cast`,
  `simpa` as in lines 1126-1130 and 1141-1143).

## 5. Findings (all minor)

**M1 (minor) — overbroad sentence about (H).** ll.tex lines 607-608: "The premise (H) is an explicit hypothesis of
the theorem; no Lean theorem proves it for any $m,t$."
Evidence: for large t, (H) is a few-line consequence of main-library theorems: `Suk.classical_upper_bound`
(`ErdosSzekeres/Suk/CupsCaps.lean:74`, `ForcesConvexNGon ((2n-4).choose (n-2) + 1) n`) and
`forcesConvexNGon_esNumber` (`ErdosSzekeres/LowerBound/Number.lean:12`); e.g. m = 6, K = 8 and any t ≥ 155
(6t ≥ 925 = C(12,6)+1). Also (H) is trivially true for K = 0. The sentence is literally about theorems whose
statement is (H), which is not something a reader can check, and in spirit it is misleading. Unsure whether the
writer meant only the instances used. Suggested fix: "This file does not prove (H); the instances used below are
\lean{Sixfold66} and \lean{Sevenfold70}, which no Lean file of the project proves unconditionally
(Remark~\ref{ll:rem:hyp})."

**M2 (minor) — "used inside printed theorems" for the seven `@[simp]` lemmas.** ll.tex lines 35-36.
Evidence: `toC_ofC` (used at 255), `ofC_toC` (249) and `toC_crot` (264, 277, 284, 290, 306) are used, but
`ofC_zero`/`ofC_one` (238-239) have no explicit use and none of the `simp` calls in the file evidently needs them
(they rewrite `ofC z 0`, `ofC z 1`, which do not occur in those goals); `toC_re`/`toC_im` are plausibly used by the
`simp` at line 308. I cannot settle this without running Lean (forbidden). Harmless for soundness: these lemmas are
`rfl`/`ext` proofs, the build log has no messages, and the file has no sorry/axiom. Suggested fix: "which are checked
by the build (no messages) and are proved by `rfl` or `Complex.ext`/`funext`".

**M3 (minor) — "Lean proofs use Krein–Milman" is imprecise for (b).** Coverage paragraph (ll.tex lines 733-734) and
map row `ll:lem:hv` note: "(b)–(d) … differ from the Lean proofs, which use Krein–Milman".
Evidence: `extreme_mem_hullVerts` (130-137) uses `extremePoints_convexHull_subset` and
`Convex.mem_extremePoints_iff_convex_diff`, not Krein–Milman; `hullVerts_nonempty` uses
`IsCompact.extremePoints_nonempty` (existence of extreme points); only `subset_convexHull_hullVerts` uses
`closure_convexHull_extremePoints`. The proof paragraph of Lemma ll:lem:hv (lines 185-188) states this correctly; only
the summary lines overstate. Suggested fix: "which use Mathlib's extreme-point results (Krein–Milman for (c))".

**M4 (minor) — intro summary slightly stronger than Lean for S = ∅.** ll.tex lines 8-10: "then the hull vertices of S
form a single f-orbit". For S = ∅, hv(S) = ∅ is not an orbit; the Lean statement is "for every x ∈ hv(S),
hv(S) = orb_m(f,x)", vacuous for S = ∅. Theorem ll:thm:core and Remark ll:rem:core(2) are correct; only the bullet
is loose. Suggested fix: "… then for every hull vertex x, the hull vertices of S are exactly the f-orbit of x".

**M5 (minor) — "review … of the same file".** ll.tex line 33. `LEANEXT/review/REPORT.md` lines 3-4 give the reviewed
file's SHA-256 afb8542d…, but the axioms were printed from a separate copy (`AxiomsCheck.lean`, REPORT.md line 62)
that is not kept in the record, so identity rests on the report's statement (unlike the 6 November re-check, whose
copy is kept and was diffed). Suggested fix: "(review of 4 November 2026; its report `LEANEXT/review/REPORT.md` gives
the reviewed file's SHA-256 afb8542d…)".

**M6 (minor, layout) — overfull boxes in multi-reference heads.** Compile log: overfull `\hbox` up to 149 pt in the
heads of Lemma ll:lem:orbit (source lines 104-111), ll:lem:complex (323-337), ll:lem:rot (383-388) and around
lines 509-512. No effect on content; may need a preamble-level fix (e.g. allowing breaks inside `\leanref`) or
splitting long heads.

## 6. What I did not find

No missing, extra or changed hypothesis; no changed conclusion or quantifier order; no wrong line number (all 55
references exact); no nonexistent name; no overclaimed rigor label (the conditional theorems are presented as
conditional, the written corollary as a written step); no disallowed reference; no machine path or tool name.
