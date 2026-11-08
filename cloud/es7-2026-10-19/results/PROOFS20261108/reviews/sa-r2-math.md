# Review of section `sa`, round 2, lens "math" (fidelity, rigor, adversarial)

Files reviewed: `sections/sa.tex` (611 lines) and `sections/sa.map.tsv` (13 rows plus header), as left by the round-2
fixes (`reviews/sa-r2-fix.md`). Sources: the three Lean files and their logs (paths relative to RES), the vendored ETV
files (relative to the repository root), and the cited statements of the sections fd, ll, lg, ec, sr, ar, mm and mb.

**Verdict: pass.** I found no blocker and no major finding. There are three minor findings (M1 to M3) and two nits
(M4, M5). None of them affects the correctness of a statement or a proof.

## 1. Fidelity of the statements (all 28 heads and the example)

Each statement was compared, binder by binder, with its declaration: argument order, every hypothesis, the conclusion,
the natural-number reading, the left-associated products and the absence of subtraction.

- `SizeArith.lean`, namespace `A1`, 20 theorems at lines 16, 19, 22, 25, 28, 31, 34, 37, 42, 47, 52, 61, 62, 65, 66, 69,
  70, 73, 76 and 79. All match: `sa:prop:rot` (a)–(e), `sa:prop:mirror` (a)–(b), `sa:prop:order` (a)–(c),
  `sa:lem:split` and `sa:prop:table` (a)–(i).
  - `(2t)k` renders `2 * t * k`. The conclusion `5 * (t * k) + e` of `A1.mult5_order_reduce` is kept, and the
    section lists the Lean terms explicitly.
  - In `A1.table_c5` the strict `<` is kept. `≠` is kept in `A1.c3_no32` and `A1.c5_gap`. The two implications of
    `A1.table_mirror` keep their order.
- `AssembledSizes.lean`, root namespace, 7 theorems at lines 6, 9, 12, 15, 18, 21 and 24. All match, including the
  order `(n k e p)` and `hp, he, h, h33` of `big_order_orbit`.
- The anonymous `example` at line 30 is rendered exactly: `¬ (∀ n k, n = 2k → 32 ≤ n → 17 ≤ k)`.
- `baek_seven` (`BaekSeven.lean:6`) matches. `γ : Type` is implicit with `[LinearOrder γ]`, then `C`, `S`, and
  `h : 17 ≤ S.card`. The conclusion is `C.HasNCap 4 S ∨ C.HasNGon 7 S`.
- The description of `Config`, `Cap3`, `Cap`, `Cup`, `Gon`, `NGon`, `HasNCap` and `HasNGon` agrees with
  `ErdosSzekeres/Vendor/ETV/Config/Defs.lean` 20–67. The list predicates also agree: `List.In` at line 22 and
  `Chain3'`/`Chain3` at lines 46 and 42 of `Lib/List/Defs.lean`.
  - `List.IsChain` is the inductive predicate of Batteries (`Batteries/Data/List/Basic.lean:562`). That is the
    Batteries revision 8da40b72 pinned in `lake-manifest.json`, and the toolchain's `Init` has no `IsChain`. So
    "which Mathlib takes from its dependency Batteries" is right.
- `#check @main` (`BaekSeven.out` 1–2) agrees with `Main.lean:87` and the `variable` line 26, and with
  Theorem `mb:thm:baek`. Remark `sa:rem:baek-seven` (1)–(2) describes the difference (n = 4; universe) correctly.

A script (`build/sa_r2_math/mapcheck.py`) parsed the 13 statement environments and checked them against the map rows.
It printed `MAP_OK`:
- labels, kinds and order agree;
- the `\leanref` pairs agree with the map names and file:line entries;
- every file:line points at the line `theorem <name>` of the right file;
- the `A1.` names lie in `namespace A1`;
- the four remarks and the written-step lemma carry `-`.

The other line references in the prose were checked by hand, and all are exact:
- `SizeArith.lean`: 1–9, 4–8, 13–56, 58–80 and 84–103;
- `AssembledSizes.lean`: 25–27, 29, 30 and 33–39, and 24:41 for the linter warning;
- `BaekSeven.lean`: 11 and 12;
- the A1 report: 93, 103–106, 106, 107 and 262, and trust rows 2–9, 4, 8 and 9;
- `ES7SPLIT/README.md` 78–79, which lie in the Rigor paragraph of §2 (§2 spans lines 44–84), and
  `split_theorem.md` 13–15;
- `MirrorMain.lean:1529`. `capacity16` lies in `section Baek17` inside `namespace MirrorOdd`, so the name
  `MirrorOdd.capacity16` is correct.

## 2. Proofs (checked step by step)

- **Propositions `sa:prop:rot`, `mirror`, `order`, `table` and `assembled`, Lemmas `split` and `big-order`, and the
  control.** Every step is correct and complete.
  - The claim "(So the statement records the weaker bound 8 ≤ k.)" is right: the sharp bound is k ≥ 9.
  - `1 ≤ b` is indeed unused in `mirror_reduce_b12` and `mirror_b12`, and `hp` in `big_order_orbit`.
  - The descriptions of the Lean proofs match the source:
    - `Nat.mul_assoc` then `omega`;
    - `Nat.lt_or_ge`, `omega`, then five `decide` calls. The remark that, for s = 5, the instance of the
      disjunction evaluates `5 % 2`, `5 % 3` and `5 % 5` matches the lazy `instDecidableOr`;
    - `cases k`, then `simp at h` turning `n = p * 0 + e` into `n = e`;
    - `rfl`, `decide`, `omega`;
    - `decide` on `Nat.choose (4+2) 2 + 2 = 17`, then `main 4 C S (e ▸ h)`.
- **Theorem `sa:thm:baek-seven`.** Correct: `binom(6,2) + 2 = 17`, and it is the instance n = 4 of
  `mb:thm:baek` (n = 4 is the only n with `binom(n+2,2) + 2 = 17`).
- **Lemma `sa:lem:model`.**
  - (a): injectivity of the iterates, the minimal period through `ll:lem:minperiod` (unpacked through (P1)/(P2) of
    the `ll` conventions), pairwise distinctness, invariance of O(y), the partition, `n = s k + e`, and `e = 0`
    through `lg:lem:centre`. The hypotheses 0 < m, m even, invariance, general position and p ≠ c are all
    available.
  - (b): ⟨σ(p)−a,u⟩ = d, the involution, fixed points = L, the pairing and `b ≤ 2` through Mathlib's `Collinear`
    (vector span of differences).
  - (c): `fd:lem:mono` (b), (c), and unions of invariant sets.

  All correct.
- **Remark `sa:rem:use`.** Every derivation is correct (see §3 for the exhaustive checks):
  - (1): s = 2, 3, 4, 5, 6, the general route through `sa:lem:split` and `sa:prop:order` with k' = tk, and the case
    s ≥ 7 through `sa:lem:big-order`, `sr:lem:concyclic` and `fd:lem:mono`(a);
  - (2): b = 0 gives `MirrorNoAxis34`, b ∈ {1,2} gives `MirrorOneAxis33`;
  - (3): `sr:thm:structure`(b) with |S| ≥ 33 > 1; the order s of a; a^j = e^{2πi/s}; g^[j] = ρ_{c,2π/s};
    `ar:thm:transfer` with N = 33, n = 7;
  - (4) and (5) were checked as described in §4.

  The subsets built in (1) and (2) meet the exact hypotheses of the classes (`SYMLEAN/SymmetricReduction.lean`
  467–499):
  - card = 34, 33 or 35 and c ∉ T;
  - invariance under `halfTurn c` (pointwise equal to ρ_{c,π}), `rotAbout c (2π/3)` or `rotAbout c (2π/5)`;
  - for the mirror classes, u0²+u1² = 1 and exactly one, respectively no, fixed point.

## 3. Exhaustive and symbolic checks

- `build/sa_r2_math/arith.py` (plain Python) ran **2,593,275 checks**, all passing (`ALL_OK`):
  - all 27 arithmetic statements on boxes k, b, n ≤ 259, e ≤ 3, t, k ≤ 119, `order_split` for s < 20000, and
    `big_order_orbit` for n < 120, k, p < 40;
  - that `1 ≤ b` and `hp` are not needed;
  - that `e ≤ 1` is needed in `A1.c3_reduce` and `A1.c3_no32`;
  - the control at n = 32, k = 16;
  - every intermediate claim of the written proofs (3k ≥ 32, 5k ≥ 32, k ≥ 9 in (c), k ≥ 6 in (d), 2k ≥ 31,
    k ≤ 6 in `table_c5`, the gaps 32–34);
  - the disjuncts 2|2, 3|3, 2|4, 5|5, 2|6, and `binom(6,2)+2 = 17`;
  - every route of Remark (1) for s = 2..300, k ≤ 80, with e = 0 for even s. Each n ≥ 33 has a route, and every
    route delivers ≥ 17 pairs, ≥ 11 triples, ≥ 7 fivefold orbits (with 5tk ≥ 34), or k ≥ 1 for s ≥ 7;
  - the s = 4 and s = 6 bullets (k' = 2k; 2k triples and 3k pairs);
  - Remark (2);
  - the maxima of Remark (5): 31, 31, 28 (32 with HalfTurn34 only), 30 (also 30 with HalfTurn34 only), 32 and 32.

  A mutation self-test confirmed that the checker detects false variants.
- `build/sa_r2_math/geom.py` (sympy, reduction modulo u0²+u1²−1 by polynomial remainder) confirmed:
  - for reflLine: ⟨σ(p)−a,u⟩ = d, the involution, σ(p)−p = 2du−2(p−a), d(a+tu) = t, fixed points a+tu, and
    that it preserves `eDist2`;
  - for rotations: composition by adding angles, ρ_{c,2π/2} = halfTurn c, ρ(c) = c, preservation of |·−c|, and the
    complex form c+e^{iθ}(z−c);
  - t·2π/(mt) = 2π/m, 2·2π/4 = π, 2·2π/6 = 2π/3 and 3·2π/6 = π;
  - that primitive roots generate μ_s (s ≤ 60);
  - that three points of a line have orient 0.

## 4. Cited statements of other sections say what is used

| label | what sa uses | status |
|---|---|---|
| `mb:thm:baek` | for all n, C, S: `binom(n+2,2)+2 ≤ |S|` ⇒ HasNCap 4 ∨ HasNGon (n+3); used at n = 4 | matches `main` and the `#check` output |
| `mb:thm:seven`, `mb:thm:refl32`(b), `mb:thm:classes`, `mb:thm:main3` | bound 32 for any line (u0²+u1²=1), with no class hypothesis; mirror classes proved; main3 conditional on HalfTurn34, Threefold33, Fivefold35 | as stated in item (5) and (4) |
| `mm:def:config` | configuration of n points, geometric k-cap; `capacity16` is n ≤ 16 under no 4-cap and no convex 7-gon | matches `MirrorMain.lean:1529` |
| `sr:def:classes` | the six classes with c ∉ S, card, angles 2π/3, 2π/5, 2π/4, the fixed-point conditions | matches the Lean source and the subsets of Remark (1), (2) |
| `sr:thm:structure`(b) | needs 1 < |S|, g ≠ id, Invariant; crot with a ≠ 1, a^m = 1, m > 0, or reflLine with u0²+u1² = 1 | used correctly |
| `sr:lem:concyclic` | equal `eDist2` to c ⇒ convex position (no general position needed) | used correctly |
| `sr:lem:orbit`, `sr:thm:main`, `sr:thm:variant` | orbit selection; main takes the five classes and passes to a half-turn or odd prime power; variant takes Fourfold32 | used correctly (see M3) |
| `ar:thm:transfer`, `ar:thm:main` | (hE) with N = 33, n = 7, 3 ≤ N; affine forms conditional on the five classes | used correctly |
| `ll:lem:minperiod`, `lg:lem:centre` | 0 < m, y ≠ c ⇒ per = m; 0 < m even, invariant, general position, p ∈ S, p ≠ c ⇒ c ∉ S | hypotheses met |
| `ll:thm:layers`, `ll:thm:card-peel`, `ec:thm:fourfold`, `ec:thm:fivefold` | layer route to exactly 32/35 points; Fourfold32 ⇒ ≥ 29 points give a 7-gon; Fivefold35 ⇒ ≥ 32 | matches `ES7Corollaries.lean` 1164–1231 |
| `ec:thm:compat`(a),(b) | (O) = exact order m; m divides |T| for 0 ∉ T; |S| mod m = [0 ∈ S] mod m | "abstract form of the count" is fair |
| `fd:def:rot/inv/gp/ngon`, `fd:lem:mono` | (a) convex position, (b) general position, (c) HasConvexNGon monotone | used correctly |

All refs are to `sa:` labels, `fd:` labels or contract export labels.

## 5. Records, rigor and build

- **Records.** The paraphrases agree with the sources:
  - `AUDIT3/README.md`: lines 1–13, Reproduction;
  - the A1 report: lines 3–24, 44–64, 68–76, 93, 103–107 and 262;
  - `ES7SPLIT/README.md`: lines 10–16 and 71–79;
  - `split_theorem.md`: lines 6–15;
  - `ES7SPLIT/review/README.md`: Reproduction (`lake env lean` from the root);
  - `WRITEUP/SYMMETRIC.md` §2 (the size table at line 160).
- **Hashes.** The six SHA-256 hashes and line counts of the table were recomputed and agree. The prefix
  `83dd0a214204` of `Main.lean` also agrees, as do `lean-toolchain` v4.24.0 and Mathlib `f897ebcf72cd…` in the
  manifest.
- **Logs.** Their axiom lists were checked line by line: 6 + 14 for `SizeArith`, 1 + 6 for `AssembledSizes`, and
  `baek_seven`.
- **Text searches.** In the 1064 `.lean` files, every one of the 28 names occurs only in its own file. The three
  files contain no `sorry`, `admit`, `native_decide` or `axiom`.
- **Commit hashes and times.** I did not re-check the commit hashes and times in `sa:rem:baek-seven`(3) (9793c06e0
  at 01:03 +0900, 83c80f38f at 03:41), because version-control commands are outside this round's allowed commands.
  They agree with the records' dates: ES7SPLIT and MIRRORETV both report runs on 1 November 2026 UTC, which is
  16:03 and 18:41 UTC for the two commits.
- **Rigor.**
  - "Lean-checked" is used only for headed declarations. The convention of `fd` (`decide` on facts established by
    hand) is applied correctly to the three uses of `decide` and to the `rfl` of the control.
  - No class is presented as proved, and Fourfold32, HalfTurn34, Threefold33 and Fivefold35 are hypotheses
    throughout. No SAT certificate or checker is mentioned, so the cake_lpr rule does not arise.
  - "Proved" occurs only negated or as "proved here as a written step". There is no "verified" or "certified".
- **Hygiene.** `sa.tex` and `sa.map.tsv` contain no machine path, no tool name, and no non-ASCII byte.
  No `\lean`/`\dirn` argument contains a space. The map has 5 fields per row and a final newline.
- **Compile.** `build/sa_r2math_wrapper.tex` was run twice and exits 0 with 8 pages. It has no `!` error, no
  "Missing" and no overfull box. Its 26 undefined references are all `fd:` labels or export labels. The only other
  log entries are 2 underfull vboxes at page breaks.
- **Full document.** A copy in `build/sa_r2_math/full/`, with its own generated appendix of 470 rows, ran three
  passes, each exiting 0. It has no undefined or multiply defined label, and all 19 `sa:` labels are in the aux
  file. The single overfull box is in another section's appendix row (`ENCBLEAN/logs/...`).

## Findings

### M1 (minor): "each statement assumes the bound on k as a hypothesis" is not accurate for all nine statements

**Location:** `sa.tex:225–227` (introduction of §`sa:ssec:table`).

**Issue:** The sentence covers all nine statements of `sa:prop:table`, but several have no bound on k:
- `A1.c3_no32` and `A1.c5_gap` take no hypothesis besides `e ≤ 1`; they are size gaps.
- `A1.table_c5` assumes a bound on the size, `5k + e < 35`, which is the form that the fivefold case theorem gives.
- `A1.table_c4_only_c2` and `A1.table_c6` bound `2k`.

The map note ("the bounds on k from the case classes are hypotheses") has the same looseness.

**Fix:** "each statement that depends on a case theorem assumes the bound that it gives (on k, on 2k, or on 5k+e) as a
hypothesis; `A1.c3_no32` and `A1.c5_gap` need none."

### M2 (minor): item (5) of Remark `sa:rem:use` silently leaves the standing hypothesis n ≥ 33 and the case k = 0

**Location:** `sa.tex:563–572`.

**Issue:** The remark starts "Let S be … with n = |S| ≥ 33". Item (5) is about sets without 7 points in convex
position, of any size, and says "the case classes bound k through item (1) or (2)".
- What is used is the subset selection of items (1) and (2), that is Lemma `sa:lem:model` (a)–(c) and the class.
  It is not their arithmetic, which needs n ≥ 33.
- The fourfold, sixfold and half-turn bounds ("so n ≤ 28 by part (e)", parts (g), (h)) use n = sk, that is e = 0.
  This needs S ⊄ {c}. It holds as soon as k ≥ 1, and for k = 0 one has n = e ≤ 1. So the bounds hold, but this
  case is not mentioned.

**Fix:** add one sentence to (5): "Here S need not have 33 points: if k reached the number of orbits or pairs that a
class requires, the subset T built in item (1) or (2) would satisfy its hypotheses. For even s, e = 0 as soon as
k ≥ 1, and k = 0 gives n ≤ 1."

### M3 (minor): "Among the reduction theorems only Theorem `sr:thm:variant` uses this class" omits the group form

**Location:** `sa.tex:511–513` (bullet s = 4 of Remark `sa:rem:use`(1)).

**Issue:** `VariantChecks.group_form` (`SYMLEAN/review/VariantChecks.lean:1168`) also takes `Fourfold32` as a
hypothesis, `(h4 : Fourfold32)` at line 1169. It is the Lean-checked group form of Corollary `cor:only`, which section
`sr` itself mentions in its remark on the variant. The sentence is true of the reduction theorems that this document
states.

**Fix:** "Among the reduction theorems stated in this document, only Theorem `sr:thm:variant` uses this class (so does
the review-file group form `VariantChecks.group_form`)". Alternatively, drop "only".

### M4 (nit): location of the fixed-point computation in section sr

**Location:** `sa.tex:468–469`.

**Issue:** "(This is also shown after Definition `sr:def:classes`.)" is imprecise. The computation that the fixed
points of reflLine are the points of a + ℝu is the last paragraph of Definition `sr:def:classes` itself, inside the
environment. Its complex form is given after Definition `sr:def:maps`.

**Fix:** "(This is also shown at the end of Definition `sr:def:classes`.)"

### M5 (nit): "gives one orbit"

**Location:** `sa.tex:23–24` (file list, item 2).

**Issue:** "an order of at least 7 gives one orbit" can be read as "exactly one". The lemma gives `1 ≤ k`, that is,
at least one orbit other than the centre. The lemma's own head says it correctly ("an orbit").

**Fix:** "gives at least one orbit other than the centre".

### Observation, no action required

The appendix generator prints a map row with lean_name `-` as "written step". So the row for Remark `sa:rem:control`
reads "written step" next to `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean:30`, the file:line of an anonymous
example that Lean accepted. The note of the row explains it ("anonymous example … accepted by Lean … not covered by
#print axioms"), and the conservative label is consistent with the `fd` convention: a Lean-checked label needs a head
naming a declaration and an axioms output. No change is needed.

## Severity summary

| severity | count |
|---|---|
| blocker | 0 |
| major | 0 |
| minor | 3 (M1–M3) |
| nit (reported as minor) | 2 (M4, M5) |

The section passes this lens:
- every statement is faithful to its Lean declaration, with exact line numbers in the heads and in the map;
- every proof step is correct, and the arithmetic holds exhaustively on large boxes;
- the claims of the remark on how the arithmetic is used are correct;
- the cited statements of other sections say what is used.

## Outputs of this review

- `build/sa_r2_math/arith.py`: the exhaustive arithmetic check (`ALL_OK`, 2,593,275 checks, with a mutation test).
- `build/sa_r2_math/geom.py`: the symbolic checks (`ALL_OK`).
- `build/sa_r2_math/mapcheck.py`: the map and head check (`MAP_OK`).
- `build/sa_r2math_wrapper.{tex,log,pdf,txt}` and `build/sa_r2math_pass{1,2}.txt`: the standalone compile check.
- `build/sa_r2_math/full/`: the full-document build on a copy, with its own generated `appendix_map.tex`. STAGE's own
  `appendix_map.tex` was not touched.
