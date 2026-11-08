# Review of section `sa`, round 1, lens "math" (fidelity, rigor, adversarial)

Files reviewed: `sections/sa.tex` (568 lines), `sections/sa.map.tsv` (9 rows). Sources read: the three Lean files and
their logs at commit `7e32ee259`, the vendored ETV definitions and `main`, and the cited statements of the
sections fd, ll, lg, sr, ar, mb and ec.

**Verdict: pass.** There is no blocker and no major finding. Ten minor findings follow. Most concern scope
statements that miss Lean-checked counterparts elsewhere in the document, or loose wording in the written-step
remark.

## What was checked, and how

1. **Fidelity of the 28 heads.** Each statement was compared with its Lean declaration: binders and their order,
   every hypothesis, the conclusion, natural-number semantics, the left-associated products `2 * t * k` and
   `5 * (t * k) + e`, and the absence of subtraction. All 20 theorems of `A1` match, as do the 7 theorems of
   `AssembledSizes.lean` and `baek_seven`. The anonymous `example` (line 30) is rendered correctly. A script
   compared each head with the source:
   - all 28 `\leanref` targets point at the line `theorem <name>` of the right file;
   - the 8 map rows with Lean names equal the heads (same names, same order, same file:line);
   - the kind of each row equals its environment.
2. **Sources and logs.** These were recomputed with `wc -l` and `shasum -a 256` and all agree with the table:
   - the six line counts and SHA-256 hashes;
   - the prefix `83dd0a214204` of `ErdosSzekeres/Vendor/ETV/Main/Main.lean`;
   - HEAD `7e32ee259`;
   - `lean-toolchain` v4.24.0 and Mathlib `f897ebcf72cd…`.

   Git history shows that neither the toolchain nor `ErdosSzekeres/Vendor/ETV` changed after October 2026. So the
   logs of 1 and 2 November refer to the same versions. Other checks:
   - The axiom lists were checked line by line: 6 of the `A1` theorems use `Classical.choice`, the other 14 do not.
     In `AssembledSizes`, only `halfturn_pairs` uses it.
   - The linter warning is at 24:41.
   - The three files contain no `sorry`, `admit`, `native_decide` or `axiom`.
   - A grep of every `.lean` file in the repository finds the 27 declaration names, and `baek_seven`, only in their
     own files.
   - Only these three `.lean` files exist under `AUDIT3/A1_reduction` and `ES7SPLIT/review/equivalence`.
3. **Arithmetic, exhaustively.** A Python script ran 177,576 checks; a mutation test confirmed that it detects
   failures. It covers:
   - every statement of the two files, on boxes `k,b,n <= 259`, `e <= 3`, `t,k <= 119`;
   - every intermediate claim of the written proofs: `3k>=32`, `5k>=32`, `k>=9` in (c), `k>=6` in (d), `2k>=31`,
     `k<=6` in `table_c5`;
   - that `1<=b` is not needed in `mirror_reduce_b12`;
   - that `hp` is not needed in `big_order_orbit`, for all `p <= 79` including `p < 7`;
   - `order_split` for `s < 20000`, and which disjunct the five closed instances `s = 2..6` satisfy;
   - the control `n=32, k=16`;
   - every derivation of Remark `sa:rem:use` (1), for all `s = 2..120` and `k <= 59`, with `e=0` for even `s`. For
     `m` in {2,3,5} dividing `s`, `k' = tk` gives `>=17` pairs, `>=11` orbits of size 3 and `>=7` orbits of size 5.
     Every `s >= 7` gives `k >= 1`. Every `s >= 2` has a route;
   - item (2);
   - the maxima of item (5): 31, 31, 28, 32, 30, 32 and 32;
   - `binomial(6,2)+2 = 17`, with `n = 4` the only solution of `binomial(n+2,2)+2 = 17`.

   With sympy, modulo `u0^2+u1^2=1`:
   - `reflLine` is an involution;
   - it fixes every point `a+tu`;
   - `reflLine(p)=p` is equivalent to `2du = 2(p-a)`;
   - rotations compose by adding angles;
   - `rotAbout c (2pi/2)` equals `halfTurn c`;
   - `t*(2pi/(mt)) = 2pi/m`.

   The checks found no error.
4. **Proofs.** Every step of the proofs of Propositions `sa:prop:rot`, `mirror`, `order`, `table` and `assembled`,
   of Lemmas `split` and `big-order`, of Theorem `baek-seven` and of Lemma `sa:lem:model` (a)–(c) was checked by
   hand. All are complete and correct. In particular:
   - in (a), the minimal-period argument, the pairwise distinctness through injectivity of the iterates, and the
     partition into blocks of size `s`;
   - in (b), the involution, the fixed points `= L`, the pairing argument, and `b <= 2` through Mathlib's
     `Collinear`.

   The descriptions of the Lean proofs were checked against the source: `Nat.mul_assoc` then `omega`;
   `Nat.lt_or_ge`, then `omega` and five `decide`; `cases k` and `simp at h`; `e ▸ h` and `main 4`.
5. **Cited statements say what is used.**

   | label | statement used | where in sa |
   |---|---|---|
   | `mb:thm:baek` | `main`, Main.lean:87: for all `n`, `C`, `S`, if `binom(n+2,2)+2 <= |S|` then `HasNCap 4 S ∨ HasNGon (n+3) S` | at `n=4` |
   | `ll:lem:minperiod` | `0<m`, `y≠c` ⇒ `per = m` | with `m=s` |
   | `lg:lem:centre` | `0<m` even, invariant, GP, `p∈S`, `p≠c` ⇒ `c∉S` | |
   | `sr:lem:concyclic` | equal `eDist2` to `c` ⇒ convex position; no GP needed | |
   | `sr:thm:structure(b)` | needs `1<|S|` | holds with `|S|>=33` |
   | `sr:def:classes` | exact hypotheses: `card =`, `c∉S`, `halfTurn c`, `rotAbout c (2pi/3)` and `(2pi/5)`, the one-fixed-point and no-fixed-point conditions | the subsets built in Remark `sa:rem:use` meet them |
   | `sr:thm:main`, `sr:thm:variant` | `Fourfold32` appears only in the variant | |
   | `ar:thm:transfer`, `ar:thm:main` | | consistent |
   | `mb:thm:classes`, `mb:thm:main3` | the two mirror classes are proved; `main3` is conditional on HalfTurn34, Threefold33 and Fivefold35 | |
   | `mb:thm:seven` | uses `main` at `n=4` through `capacity16` | |
   | `fd:def:*`, `fd:lem:mono` | | consistent |

   The section's description of caps, cups, `HasNCap` and `HasNGon` agrees with `Config/Defs.lean` 20–67 and with
   `Lib/List/Defs.lean` 22 and 46, and with `mb:def:config`.
6. **Records.** The paraphrases of the following records are accurate (date, commit, "claims no theorem", A1-F1
   rated minor):
   - `AUDIT3/README.md`: lines 1–13, the A1 findings, Reproduction;
   - the A1 report: lines 7, 44–64 (rows 2–9), 103–106 and 262;
   - `ES7SPLIT/README.md`: status and section 2 rigor;
   - `split_theorem.md`: status;
   - `ES7SPLIT/review/README.md`: Reproduction, "from the repository root with the repository's Lean build".
7. **Compile and rules.**
   - The section compiles standalone (own wrapper `build/sa_r1math_wrapper.tex`): two passes, exit 0. The only
     undefined references are the 18 allowed `fd:` and export labels. There is no Missing-$ error and no overfull
     box.
   - No `\lean` or `\dirn` argument contains a space.
   - No machine path and no tool name appears.
   - "proved" occurs only negated ("not proved in Lean or in this document") or as "proved here as a written step".
   - Every `\ref` is to an `sa:` label, an `fd:` label or an export label.
   - The map is ASCII with 5 fields per row.
   - The rigor wording ("Lean-checked"; `decide` on hand-checked closed facts is not computer-assisted) follows the
     convention of `fd`.

## Findings

### F1 (minor): scope statements in Remark `sa:rem:use` miss Lean-checked counterparts; one is inaccurate

**Location:** `sa.tex:483–485`, `:531–541`.

- `:483–485` reads "(Eight of the k orbits would give the 32 points of the class Fourfold32, which only
  Theorem sr:thm:variant uses.)" Item (5) of the same remark uses `Fourfold32` for the bound 28 (`:536`). Theorem
  `ec:thm:fourfold` (`LayerLemma.fourfold_heptagon`, `LEANEXT/es7corr/ES7Corollaries.lean:1216`) takes a same-text
  copy, `LayerLemma.Fourfold32` (Definition `ec:def:cases`), as its hypothesis. The sentence holds only for the
  constant `SymReduction.Fourfold32`, and only among the reduction theorems.
- `:540–541` reads "These bounds are conditional on the classes …". For reflections, the bound 32 is itself
  Lean-checked with no class hypothesis (Theorem `mb:thm:seven`(b), any line), and the two mirror classes are
  theorems (`mb:thm:classes`). For fourfold and fivefold sets, Lean-checked conditional forms of the table bounds
  exist: `ec:thm:fourfold` (Fourfold32 ⇒ at least 29 points give a convex 7-gon, that is, at most 28) and
  `ec:thm:fivefold` (Fivefold35 ⇒ at least 32 points, that is, at most 31). Unlike the files of this section, these
  forms include the geometric modelling (through the layer lemma).

**Fix.** Say that "among the reduction theorems only Theorem `sr:thm:variant` uses the class; a same-text copy is
the hypothesis of Theorem `ec:thm:fourfold`". In (5), name `mb:thm:seven`, `ec:thm:fourfold` and `ec:thm:fivefold`
as the Lean-checked (respectively Lean-checked conditional) forms of three rows. Say that the remaining rows are
conditional on HalfTurn34 or Threefold33.

### F2 (minor): "they are not Lean-checked" under-reports the Lean coverage of the modelling

**Location:** `sa.tex:37–38`.

Lemma `sa:lem:model` is correctly a written step, but parts of it are Lean-checked elsewhere in the document:
- Theorem `ec:thm:compat`(a),(b) (`PCompat.dvd_card`, `card_mod`): for a ζ-invariant finite set, with ζ of order m
  in a commutative group with zero, `m | |T|` when `0 ∉ T`, and `|S| mod m = [0∈S] mod m`. This is the abstract
  form of `n = s·k+e`.
- The layer lemma (`ll:thm:layers`, `ll:thm:card-peel`): `|S∖{c}| = m·t` for K-free S, as used in the Lean proofs
  of `ec:thm:fourfold` and `ec:thm:fivefold`.
- The half-turn facts `c ∉ S` and `2 | |S|` inside the Lean proof of `sr:thm:main`.

**Fix.** "Lemma `sa:lem:model` is a written step and not a declaration of these files (related Lean-checked facts:
Theorem `ec:thm:compat`(a),(b); the layer results used in Theorems `ec:thm:fourfold`, `ec:thm:fivefold`)."

### F3 (minor): the records' statement in Remark `sa:rem:baek-seven`(3) is out of date, and "for their use" is not in the records

**Location:** `sa.tex:381–386`.

`ES7SPLIT/README.md` §2 and `split_theorem.md` say: "not Lean-checked for n = 7; the repository's bridge covers the
octagon case only". They were committed at `9793c06e0` (2026-11-02 01:03 +0900). The Lean-checked n = 7 bridge
`MirrorOdd.capacity16` (`MIRRORETV/lean/MirrorMain.lean:1529`, used by `mb:thm:seven`) arrived later, at
`83c80f38f` (03:41 the same day). The section softens the quote to "for their use at n = 7" and then mentions
`mb:thm:seven`. A reader may still conclude that no Lean-checked bridge exists at n = 7.

**Fix.** Quote the records as written, add that they predate the Lean-checked bridge used in `mb:thm:seven`, and
say that whether that bridge covers the z-split use of ES7SPLIT is not examined here.

### F4 (minor): general position of the mirror subsets is not justified in Remark `sa:rem:use`(2)

**Location:** `sa.tex:501–507`.

The 34-point set is said to be in general position without a reference. The 33-point set for `MirrorOneAxis33`,
16 pairs and one point of `S∩L`, is not said to be in general position at all, although the class requires it.
Both follow from Lemma `sa:lem:model`(c), which item (1) cites but item (2) does not.

**Fix.** Add "in general position (Lemma `sa:lem:model`(c))" to both sets.

### F5 (minor): wording of Remark `sa:rem:use`(4)

**Location:** `sa.tex:518–523`.

- "each item exhibits a subset T that satisfies the hypotheses of one class" does not apply to the branch
  `s >= 7`, which needs no class (`:498`), or to item (3), which reduces to (1) and (2).
- "The Lean-checked form of this implication is Theorem `sr:thm:main`" covers only the isometries. The affine part
  of item (3) is `ar:thm:main`, which the section names correctly at `:40–41`.

**Fix.** Add "except for orders `s >= 7`" and "Theorems `sr:thm:main` and `ar:thm:main`".

### F6 (minor): the alternative citations "(or …)" in Remark `sa:rem:use`(1) give only part of the stated conclusions

**Location:** `sa.tex:476`, `:480`.

- For `s = 5`, "Proposition `sa:prop:rot`(b) (or `sa:prop:assembled`(c)) gives n≥35 and k≥7": part (c) of the
  assembled proposition gives only `35 <= n`. The bound `k >= 7` then needs `5k >= 34`.
- For `s = 4`, "(or `sa:prop:assembled`(f)) gives n=4k≥36, k≥8 and 2k≥17": part (f) gives only `17 <= 2k`.

**Fix.** Say which conclusion each alternative supplies.

### F7 (minor): the map has no rows for the four remark environments

**Location:** `sa.map.tsv`.

The contract asks for "one row per statement environment", and 9 of the 12 sections list their remarks. The map
has no rows for `sa:rem:big-order`, `sa:rem:control`, `sa:rem:baek-seven` and `sa:rem:use`. In particular, the
Lean-checked anonymous `example` at `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean:30`, which Remark
`sa:rem:control` covers, will not appear in the generated appendix.

**Fix.** Add the four rows. For `sa:rem:control`, use lean_name "-" (anonymous example), that file:line, and a note
saying it is not covered by `#print axioms`.

### F8 (minor): names of the namespace `A1` are abbreviated in running text

**Location:** `sa.tex:68–69`, `:127–132`, `:151–152`, `:170–174`, `:227–237`, `:477`.

The section writes `c5_reduce`, `table_mirror` and so on. The convention of `fd` (Files paragraph) says that names
in a namespace outside `ErdosSzekeres` "are always written in full", here `A1.c5_reduce`. The heads and the Coverage
paragraph do use the full names.

### F9 (minor): the place of definition of the ETV notions is imprecise

**Location:** `sa.tex:329–330`.

The notions are said to be "defined in Lean in `ErdosSzekeres/Vendor/ETV/Config/Defs.lean`, lines 20–67". But
`List.In` and `List.Chain3'`, which Cap, Cup, HasNCap and HasNGon unfold to, are defined in
`ErdosSzekeres/Vendor/ETV/Lib/List/Defs.lean:22` and `:46`, and `List.IsChain` is Mathlib's.

### F10 (minor, nits): two small precision points with no effect on correctness

- **`sa.tex:203–204`.** "The five evaluated instances are the facts 2∣2, 3∣3, 2∣4, 5∣5, 2∣6". `decide` evaluates the
  Decidable instance of each closed disjunction; for `s = 5`, for example, it also evaluates `5 % 2` and `5 % 3`. The
  listed facts are the disjuncts that make the instances true. The conclusion "not computer-assisted" stands.
- **`sa.tex:18–23`.** The citation "lines 103–106" of the A1 report supports the authorship and most of the list.
  The item "one orbit for an order of at least 7" (`big_order_orbit`) is not mentioned there; it comes from the file
  itself.

## Severity summary

| severity | count |
|---|---|
| blocker | 0 |
| major | 0 |
| minor | 10 |

The statements, the line numbers, the proofs and the arithmetic are correct, and the rigor labels are used
correctly. The section passes this lens.
