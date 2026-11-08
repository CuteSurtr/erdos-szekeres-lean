# Section `oc`, polish round 1: independent referee report

**Verdict: pass.** I found no blocker and no major issue. There are two minor findings, both small imprecisions in
line ranges, with no effect on correctness.

Files reviewed: `sections/oc.tex` (936 lines, 43 statement environments) and `sections/oc.map.tsv` (header plus 43 rows).
Paths of Lean sources and records are relative to RES, except paths that start with `ErdosSzekeres/` (repository root)
or with `sections/`, `build/`, `reviews/` or `inventory/` (staging area).

I formed my view from the sources first. Only afterwards did I read the round-1 reports (`oc-r1-*`), the writer
concerns and the polish fix log. Every fix listed in `oc-polish-r1-fix.md` is present in the current text, and none of
them introduced an error.

## What was checked, and how

1. **Fidelity, statement by statement.** I compared each statement with its Lean source, binder by binder. The sources
   were:
   - all of `LEANEXT/orbit/OrbitConsistency.lean`;
   - `LEANEXT/merged/Merged.lean:1140-1385`;
   - all of `LEANEXT/keys/KeyOrder.lean`;
   - `LAYERLEAN/LayerLemma.lean:36-120, 225-470, 576-625, 932`;
   - `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry}.lean`.

   For each statement I checked:
   - hypotheses and quantifier order;
   - Finset vs Set (`cell_lt_iff_rank` takes a `Set`; the `_finset` version takes a `Finset` with `StrictMonoOn` on the
     coercion);
   - maps-into (`Invariant`);
   - casts: `(j : ℝ)`, `(k : ℤ)` to ℝ, `(m / 2 : ℕ)` cast to ℤ, and `(J + m) % (2 * m)` formed in ℤ;
   - Euclidean `%` and `/`;
   - the convention 2π/0 = 0 (`RotComp`, `rotComp_iterate`, `encoder_literal_sound`, any m);
   - the argument order `toIcoMod Real.two_pi_pos 0 x`;
   - `toLex` on ℤ × ℕ;
   - the `False`-conclusion forms (`same_ray_false`, `not_same_ray_of_distinct_layers`), stated as ≠ with an explicit
     note.

   All 43 environments match. A script resolved all 52 `\leanref{Name}{File:Line}` pairs in the heads: each line holds
   a declaration of that name, with offset 0 every time.
2. **Proofs.** I re-derived every proof step myself, including:
   - the three swap cases and the cyclic-rule steps;
   - swap induction with Mathlib's product convention `(swap x y * f) i = swap x y (f i)`;
   - the cast ℤˣ → ℤ → ℝ, which is multiplicative and injective;
   - Step 2 of the encoder proof, `σ₁(σ₂ i) = (σ₁σ₂) i`;
   - same-ray (i)-(iv);
   - the Euclidean split in `eq_iterate_of_phase_eq_int`;
   - the case split a + 1 < m or a = m − 1 (with m ≥ 1) in Lemma `oc:lem:closed`;
   - layer disjointness through `peel(S,i+1) = peel(S,i) \ hv(peel(S,i))`;
   - the trichotomy in `cell_lt_iff`;
   - `toIcoDiv` existence and uniqueness, and the three conditions of `reduce_mod_two_pi`;
   - the reductions of `antipode_odd` (N = 2m, u = π/m) and `antipode_even` (N = m, u = 2π/m, m/2 = k).

   No step is delegated to Lean. There is no circularity: the parenthetical uses of `fd:lem:affine-orient` and
   `ll:lem:minperiod` are comparisons only, and the `fd` proofs of `fd:lem:orient` and `fd:lem:affine-orient`(i) do not
   use `oc`.
3. **Symbolic and exact checks.** The script is `build/oc_p1referee_sympy.py`, run with the symvenv Python under
   `nice -n 15`. All 32 checks pass (ALL OK):
   - rot-add (a) and (b) (R_0 = R_2π = id, R_π = 2c − p);
   - the rot-inv difference equals orient·(S² + C² − 1), as a polynomial identity in free symbols C and S;
   - k·2π/(2k) = π;
   - same-ray (iii) and (iv);
   - `rotAbout_polar` and `polar_add_int`;
   - the phase-nat ratio and the phase-int split;
   - the three swap identities and the two cyclic steps;
   - the cell only-if identity, and reduce (ii) and (iii);
   - both antipode angle rewrites, plus 20,000 numeric samples of `antipode_odd` and `antipode_even` against a direct
     reduction into [0, 2π);
   - the example of Remark `oc:rem:layers`(3), in exact rationals:
     - general position over all 56 triples;
     - the four convex combinations;
     - invariance under the quarter-turn;
     - polar(0, √2/2, π/4) = (1/2, 1/2);
     - each outer point is the unique maximiser of ±x or ±y over S;
     - each inner point is the unique maximiser of ±x±y over the inner points;
   - the parity table of Remark `oc:rem:parity`, against a cycle-count sign;
   - inv(a) = inv(σ⁻¹) for the sorting permutation σ;
   - `perm_sign(order)` = sgn σ.
4. **Records.** The re-checked claims are:
   - the SHA-256 prefixes `9b843180ac38`, `245b7d65407a`, `6e34096cff52`, `afb8542dceb0` and `f8c3930c2427`;
   - the line counts 429, 1385 and 158;
   - the byte-identical ENCBLEAN copies (same digests);
   - diffs that come out as stated:
     - Merged 1-1147 equals LayerLemma 1-1147;
     - Merged 1159-1311 differs from OrbitConsistency 272-427 in doc comments only;
     - Merged 1148-1383 equals Linked 1148-1383, Capstone 1156-1391 and Capstone2 1156-1391;
     - OrbitConsistency 39-112 equals the corresponding LayerLemma declarations, except for the `iterate_mem` binder and
       the doc comment of `polar`;
   - `lean-toolchain` v4.24.0 and Mathlib `f897ebcf`;
   - the logs:
     - `orbit/logs/axioms.log`: 15 lines plus `exit=0`;
     - `orbit/logs/build.log`: `exit=0`;
     - `merged/axioms.log`: 6 lines;
     - `ENCBLEAN/logs/m4_build.log:3-10`;
     - `LEANEXT/review/axioms.log` lines 1 and 33, and `LEANEXT/review/REPORT.md:3-4`;
     - `orbit/logs/check_literals.log:1-5`: 42,840 + 39,270 + 12,144 + 274,560 = 368,814 ordered triples, 0 mismatches;
   - other files:
     - `LEANEXT/README.md:6` and `:25`;
     - `LEANEXT/keys/REPORT.md:16-17` and `:22-25`;
     - `ENCBLEAN/DESIGN.md:625-626`;
     - `ENCBLEAN/geo/ES8Geo/Orbit.lean:13` (`rfl`), with the `rotAbout` text of `ENCBLEAN/geo/ES8Geo/Capstone2.lean:306`;
   - source scans:
     - `decide` occurs only at `OrbitConsistency.lean:236` and `Merged.lean:1125`;
     - there is no `sorry`, `admit`, `axiom` or `native_decide`;
     - `PreservesOrient.iterate` is used by no printed theorem.

   The axiom accounting of the Axioms paragraph is complete. Every Lean-referenced theorem is either printed or used by
   a printed theorem, with the two exceptions that the text names. Its LAYERLEAN record (`LEANEXT/review/axioms.log`) is
   among those that `inventory/LAYERLEAN.json` lists.
5. **Python code reading** (Remarks `oc:rem:parity`, `oc:rem:keys-outside`).
   - `C7UPPER/gen.py`:
     - `sortpar` is at line 108;
     - lines 74-85 apply it to the rotations of the sorted triple, and line 120 to the ordered triple;
     - line 123 builds the literal `v if s1*s2 > 0 else -v`, which is litVal(sgn σ₁ · sgn σ₂, P∘C) with
       T₀ = T∘σ₁ and C = r^[s]∘T₀∘σ₂.
   - `C6UPPER/encb/gen_b2.py`:
     - `perm_sign` is at line 56;
     - lines 72-73 compute `order`, the sorting permutation, so σ₁ = id and σ₂ = σ;
     - lines 106-109 compute J = (2k + h_i) mod 2m for odd m, and J = k for even m.
   - `gen.py` and `gen_b2.py` each exist only once in RES.
   - `LEANEXT/orbit/check_literals.py`: lines 25-31 and 36-39 do what the remark says.
6. **References into other sections.** Each target says what `oc` uses it for:
   - `fd:lem:orient`(e) exists, with "orient = 0 when two arguments are equal";
   - `fd:lem:collinear`(b);
   - `fd:lem:mono`(c);
   - `fd:lem:affine-orient`(i);
   - `fd:lem:cp-hull`;
   - `fd:lem:separation`, whose (⇐) direction is elementary;
   - `ll:def:hv`, `ll:def:peel`, `ll:lem:antitone` and `ll:lem:inv-peel`;
   - `ll:thm:core-rot`, which is (L3) verbatim;
   - `ll:lem:minperiod`;
   - `lg:def:polar`, with r unrestricted;
   - `lg:lem:centre`, whose hypotheses are exactly those quoted in Remark `oc:rem:layers`(1).

   All are export labels allowed by the contract. Only two places outside `oc` reference `oc` labels
   (`fd.tex:520`, `:581`), and both uses match.
7. **Compile and hard rules.** `build/oc_p1referee_wrapper.tex` was compiled twice with
   `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`:
   - both passes exit 0;
   - there are 0 overfull boxes;
   - the only undefined references are the 20 `fd:`/`ll:`/`lg:` export labels.

   A grep found none of the following in `oc.tex` or `oc.map.tsv`:
   - machine paths;
   - tool names;
   - `\newcommand`, `\usepackage` or `\begin{document}`;
   - "verified", "certified" or "proved" used as a rigor claim.

   The labels of the map equal the labels of the statement environments.

### Attacks that found nothing

These are recorded so that the next reader does not repeat them.

- **Degenerate inputs:**
  - m = 0 in `RotComp`, `literal_sound` and `encoder_literal_sound` (R_{c,0} = id; the text says so);
  - K = 0 (`¬HasConvexNGon 0 S` is unsatisfiable, so the layer statements are vacuous);
  - empty S, and empty or degenerate ranks;
  - repeated labels in the encoder theorem (excluded by orient₃(P∘T) ≠ 0, as the text says);
  - c ∈ S in `same_ray_false` (excluded by `lg:lem:centre`, as the text says, and not used by the proof).
- **Natural-number subtraction:** a = m − 1 in Lemma `oc:lem:closed`, with m ≥ 1; N − 1 − R in ℤ in Lemma
  `oc:lem:reduce`.
- **Iteration convention.** The section takes f^{[s+1]} = f∘f^{[s]}, while Mathlib's `Nat.iterate` unfolds to
  f^{[s]}∘f. The parenthetical equality is standard, and the one place that uses the other form
  (Lemma `oc:lem:rotcomp-pres`(a)) works with either form.
- **Remark `oc:rem:layers`(3):** all hypotheses of `phase_ne_of_distinct_layers` hold, including K = 8 ≤ 2m and
  `¬HasConvexNGon 8 S` because |S| = 8 and S is not in convex position. The conclusion with modulus 2π/m is consistent,
  since π/4 is not a multiple of π/2, and β − α = 1·π/m shows that π/m fails.
- **Remark `oc:rem:ray`:** the m = 2 example satisfies every hypothesis, and l = −1 violates the conclusion.
- **Copies:** a grep over the repository for the headline names finds exactly the nine files named in Sources.

## Findings

### m1 (minor). The "not covered" line range includes a covered declaration

- Location: `sections/oc.tex:922-925`, Coverage, "Not covered, deliberately. (i) ... (lines 49--103: `toC`, ...,
  `rotAbout_eq_crot`)".
- Issue: the range 49-103 of `OrbitConsistency.lean` contains the definition of `rotAbout` (lines 92-95). The same
  Coverage paragraph lists `rotAbout` as covered (Definition `oc:def:basic`, `oc.tex:908`). The list of 15 names is
  right; only the range is too wide.
- Fix: write "(lines 49--91 and 97--103: ...)", or "(among lines 49--103: ...)".

### m2 (minor). The extent of the copied block is given two ways

- Location:
  - `sections/oc.tex:40` (Sources, "Lines 37--112 repeat definitions and basic lemmas");
  - `oc.tex:907` (Coverage, "Of the copied block (lines 37--112)");
  - versus `oc.tex:150` (Remark `oc:rem:copies`, "Lines 39--112 of `OrbitConsistency.lean` define their own ...").
- Issue: `OrbitConsistency.lean:37` is the header comment `/-! ## 0. Copied definitions -/` and line 38 is blank. The
  first copied declaration, `iterate_mem`, is at line 39. Both ranges are defensible, but the section uses two of them
  for the same block.
- Fix: use one range throughout, e.g. "lines 37--112 (declarations from line 39)", or 39--112 everywhere.

No other finding survived verification.
