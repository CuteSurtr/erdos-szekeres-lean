# Review of section `cb`, round 1, lens: rigor (referee)

Section: `sections/cb.tex` (1440 lines), map `sections/cb.map.tsv` (100 rows).
Sources read: `C3LEAN/C3Cover.lean` lines 1-422 and 1705-2327 (plus a declaration index of all 2327 lines),
`C3LEAN/tools/prelude.lean`, `C3LEAN/README.md`, `C3LEAN/logs/compile.log`, `C3LEAN/review/logs/*`
(main_compile, indep_audit.json, revctrl_pass, revctrl_mut), `C3LEAN/c3cover_summary.json`, `C3LEAN/review/RevCtrl_pass.lean`
(lines 300-319), `C2FINAL/Central34Orbits.lean` (lines 1-50, 262-298 and the data, parsed), `C2FINAL/README.md`,
the inventory `inventory/C3-C2-misc.json`, and the cited anchors in `C3-S/soundness.md`, `C3H6M/soundness_h6m.md`,
`C3U2/sigma_split.md`, `WRITEUP/note/symmetric_extremal.tex:108-116`.

## Verdict: PASS (0 blocker, 0 major, 7 minor)

Every written proof was checked step by step and is correct and complete. Every case split is exhaustive, every
induction is well founded, and every use of an earlier result meets its hypotheses. Nothing is silently delegated to
Lean: the five statements without hand proofs (Fact `cb:fact:batches`, Facts `cb:fact:roots-codes`,
`cb:fact:roots-tsv`, Fact `cb:fact:c2-sub`, Theorem `cb:thm:c2`) are labelled computer-assisted, and the section says
what the kernel evaluates for each. The statements match the Lean declarations.

## What was checked, with evidence

### 1. Statements against Lean (fidelity as a precondition of rigor)

Every definition and theorem head was compared clause by clause with the Lean source. They agree, including the
following details:
- truncated subtraction in `mirror`, `phi` (`a + m - t.1` parsed as `(a+11)∸r`), `bitsOf` (`(K∸1)∸j`), `decodeLayer`
  (`c∸1`, `c∸34`) and `Central34.refl`;
- the `refl` match (`[(0,0)]`, then `[(0,0),(a,s)]`, else identity);
- the order and premises of the three `Covered` constructors, including `0 < K` and the explicit `K`;
- the clause order of `run`, with `d = 0` consuming a key and the split cases keeping `ks`;
- `checkRoot` with fuel `10^6`; `unpack` stopping when the remaining number is 0 (the code, not the docstring);
- the six components of `reflectionFacts`;
- the Boolean `==`/`≤` items of `subcases_reflection`; `closed` with its default `[]`.

`run_sound`, `checkRoot_sound`, `Covered.mono`, `beqList_eq`, `beqTok_eq`, `beqNode_eq`, `all_append_of`,
`all_checked` and `all_roots_covered` are stated with the same hypotheses, conclusion and quantifier order as in Lean.

A script compared every `\leanref{name}{file:line}` in the section with the line of the declaration `name` in the
named file. All are exact, as are the family formulas: `batchN` at `1740+4N`, so `batch126` at 2244;
`reflection_facts_H6_a_s` at `370+3(2a+s-2)`, the last at 397; `closedP1..8` at 51, 78, ..., 240, with the data
ending at line 264. The `certs126` data end at line 1711, and the section says 1713, which is within the tolerance.

### 2. Proofs, step by step

- **Lemma `cb:lem:bits`.** The induction on `l` for all `z` is correct, and uses `β(x or y)=β(x)∪β(y)` and
  `β(2^c)={c}`.
- **`Covered` as the least `S`-closed predicate.** The intersection argument is correct, and so is the identification
  with the Lean inductive. The Lean predicate is `S`-closed by its constructors, and the recursor puts it inside every
  `S`-closed predicate. The induction hypothesis for the premise `∀ c ∈ l, Covered S c` is the one that Lemma
  `cb:lem:mono` and the remark on intended use need.
- **Lemma `cb:lem:mono`.** `Covered(T)` is `S`-closed, and the induction principle finishes the proof. Correct.
- **Lemmas `cb:lem:beqlist`, `cb:lem:beqtok`, `cb:lem:beqnode`, `cb:lem:beq-refl`.** Correct. All four cases of the
  list induction are covered.
- **Lemma `cb:lem:run` (a).** The statement `Φ(f)` quantifies over all `stk`, `ds` and `ks`, which the recursive
  calls need, since they use other stacks. The empty stack is handled for every `f`, and `f = 0` falsifies the
  hypothesis by (R2). The step from `f` to `f+1` splits into `d = 0`, `d = 1` and `d ≥ 2`, which is exhaustive.
  - `d = 0`: `ks = []` gives `false`; otherwise `beqNode` gives `n0 = decodeKey(k)` with `k ∈ ks`. This gives
    (cert), and `Φ(f)` on `(rest, ds', ks')` holds because `ks' ⊆ ks`.
  - `d = 1` and `d ≥ 2`: the three conjuncts give the side conditions, with `K = d-1 ≥ 1`. `Φ(f)` on
    `children ++ rest` with the same `ks` covers every child and every node of `rest`. Rule (layer) or (sigma) then
    applies.

  **(b)** is a correct instance of (a).
- **Lemma `cb:lem:append` and Lemma `cb:lem:all-checked`.** Correct. The descent along the right-nested append
  matches `certs` (line 1714: `certs0 ++ (certs1 ++ (... ++ certs126))`, all 127 in order). The proof term at line
  2248 has exactly 126 `all_append_of` and `batch0..batch126`.
- **Lemma `cb:lem:codes`.** Correct, including the base case and the `acc` bookkeeping.
- **Lemma `cb:lem:sort`.** Correct.
- **Lemma `cb:lem:options`.**
  - (a): the count `4|l'| + 4C(|l'|,2) = 4C(|l'|+1,2)` holds. Duplicate-freeness holds: distinct `(c,σ,τ)` in the
    first part, and first residue `b` versus first residues in `l'`. The converse inclusion holds in both cases.
  - (b): `rem(U)` is strictly increasing, and the one-token and two-token parts are disjoint by length. The
    characterisation by `isOption` uses `Nat.blt r 11 ⇔ r ≤ 10` and `Nat.blt s 2 ⇔ s ∈ {0,1}`.
  - (c) is correct.
- **Lemma `cb:lem:decode`.** The bounds are correct: `tokCode ≤ 32`, `layerCode ∈ [1,33]` or `[34,1122]`, and
  `1122 < 1123`. The Euclidean-division identities are exact.
- **Lemma `cb:lem:lex`.**
  - (a) and (b) are correct.
  - (c): the case analysis rules out `a<b` and `b<a`, so `a = b`, and both tails are `lexLe`. The induction is on `x`
    for all `y`.
- **Lemma `cb:lem:orbits`.**
  - (b): `κ(r,s) = 3r + e(s)`, with `e` the bijection `2↦0, 0↦1, 1↦2`, so `κ` is injective on valid tokens.
    `okey(y) = map(κ, y)` for sort-fixed `y`, so `okey` is injective on `set(X)`. Totality and antisymmetry of
    `lexLe` give "exactly one".
  - (c): the involution partition counts correctly.
- **Proposition `cb:prop:refl`.**
  - Below H3: `11-r` is an involution of `{1..10}` with no fixed point, and the image of a two-token option is
    re-sorted correctly. The fixed points are `c = 11-b`, `τ = 1-σ` with `1 ≤ b ≤ 5`, so `F = 10`.
  - Below H6: `r* = a-r` for `r < a` and `r* = a+11-r` for `r > a`. This split is exhaustive because `a ∉ R`. `r*`
    lies in `R` and preserves `[r<a]`, so `f_{r*} = f_r`. Involution: `h∘h = id` on tokens, and re-sorting
    (`sortTok` of `o` or of its reversal is `o`). The unique fixed residue is `r0`: `a/2` for even `a`, `(a+11)/2`
    for odd `a`. A fixed two-token option needs `c = b*`, since the case `b* = b`, `c* = c` is impossible, and then
    `τ = σ ⊕ f_b`. So `F = 9`, with one fixed option in `X1` and eight in `X2`.
  - Counting: Lemma `cb:lem:orbits` applies to `O`, `X1` and `X2`. Its hypotheses hold: `O` is duplicate-free by
    `cb:lem:options`(b), entries are valid and sort-fixed by (c), and `ι` maps each list into itself because it
    preserves the number of tokens. The counts are 100, 5, 95 and 81, 5, 76.
  - (F1)-(F6) and the strata follow.
  - The fixed-point lists were recomputed independently and match the statement for all 11 top cases (below).
- **Proposition `cb:prop:roots-match`.** `|roots| = 100 + 10·81 = 910` by (L3). Each root is `⟨[t,o],[]⟩` with `t` and
  `o` valid, so `cb:lem:decode`(c) and `cb:lem:beq-refl` apply. Correct.
- **Corollary `cb:cor:roots`.** (a) and (b) are correct. Distinctness of the roots goes from codes to nodes.
- **Theorem `cb:thm:c3`.** Steps (1)-(5) are correct. Each cited result is used within its hypotheses, and `c ∈ certs`
  gives `keys(c) ⊆ certifiedKeys` by (L2).
- **Lemma `cb:lem:c2-subsets`.** Correct.
  - The recurrences `(k-1) + C(k-1,2) = C(k,2)` and `C(k-1,2) + C(k-1,3) = C(k,3)` hold.
  - The coverage argument by first element is correct, and choose3 uses the choose2 claim on `xs`.
  - The bijection holds by length and because a strictly increasing list is determined by its set.
- **Theorem `cb:thm:c2-refl`.**
  - `ρ(i) = (a+17-i) mod 17` is an involution of `{0..16}` with `ρ(0) = a` and `ρ(a) = 0`, so it preserves `I_a`.
  - (ii): the pairing `V ↦ V'` is unique by the bijection, and `|ρ(set V)| = |set V|` because `ρ` is injective.
  - (iv): the unique fixed class is `9a mod 17 ∈ I_a`. The unions of orbits with 2 or 3 elements are 7 + 7 = 14,
    which is exhaustive.
  - (iii): the count is `14 + 546/2 = 287`.
- **Corollary `cb:cor:c2`.** Correct.

### 3. Independent recomputation of the claims the section makes from data or by hand

Two short scripts reimplemented the definitions from the Lean text and parsed the generated data, reading the Lean
files only as data. They ran with low priority in under a second each. Results:
- `reflectionFacts` is `(190,T,T,10,100,T)` for H3 and `(153,T,T,9,81,T)` for all ten H6(a,s).
- The strata are `[5]*11` and `[95]+[76]*10`.
- `roots` has 910 distinct entries, and `decodeRoot∘rootCode` is the identity on the roots.
- The fixed points of `refl` are exactly as listed in Proposition `cb:prop:refl`. The fixed residues are `6,1,7,2,8`.
- The certificate data:
  - there are 127 lists with 910 certificates; `bounds` is the size list, with 127 entries between 1 and 85 and sum
    910;
  - `map(rootCode, roots)` equals the certificate roots in order;
  - `tsvRootCodes` has 910 distinct entries, and its set equals the set of root codes;
  - 554 certificates have `ds = 0`, and each of them unpacks to exactly one key that decodes to its root;
  - the largest decision digit is 4.
- `decodeKey(8615616512) = ⟨[[(0,0)],[(1,2)]], [(2,0),…,(7,0)]⟩`, as in Remark `cb:rem:keys`.
- Central34, for `a = 1..8`:
  - each case has 560 subcases, and (ii) holds;
  - 287 subcases satisfy `≤` and 14 satisfy `=`;
  - the fixed class is `9a mod 17` (`9,1,10,2,11,3,12,4`);
  - every closed entry is a subcase, and `uncovered` is empty;
  - `closedP_a` has 287 entries, or 288 for `a = 6`;
  - there are no duplicate sets, and exactly one orbit has both members listed, `[1,7]`/`[5,16]` in `closedP6`;
  - `uncovered(a, []) = subcases(a)` has 560 entries.

### 4. Identities checked with sympy (all OK)

- Binomial identities: `4n+4C(n,2)=4C(n+1,2)`, `(k-1)+C(k-1,2)=C(k,2)` and `C(k-1,2)+C(k-1,3)=C(k,3)`, symbolically.
- Option and kept counts: `190, 153, 180, 144`; `100, 5, 95, 81, 5, 76`.
- Totals: `910 = 100+10·81`; `90 = 190-100` and `720 = 10·72`; `810 = 90+720`; `76256 = 73567+1747+942`.
- Code bounds: the maximum token code `32` and the maximum layer code `1122`. The divisions by 3, 33 and 1123 were
  checked exhaustively on the ranges used.
- Powers: `2^22 = 4194304`, `2^11 = 2048`, `2^64 = 18446744073709551616`.
- Reflections: `2·9 ≡ 1 (mod 17)` and the values of `9a mod 17`; `ρ_a` swaps 0 and `a` and is an involution;
  `ρ_6({1,7}) = {5,16}`.
- Counts and line formulas: `C(15,2)+C(15,3) = 560`; `14 + 546/2 = 287`; the batch and refl line formulas.

### 5. Records the section cites

The cited records agree with the section:
- SHA-256 prefixes of all eight Lean files named.
- Lines 29-329 of `C3Cover.lean` are byte-identical to lines 1-301 of `tools/prelude.lean`. Lines 1-301 of the five
  control and review files are byte-identical to the prelude.
- The axiom lines of `logs/compile.log` and `review/logs/main_compile.log` match the Axioms paragraph exactly.
- No compile or axioms log exists anywhere in `C2FINAL`, as the section says, and README §6 says "propext only, about
  6 s".
- `c3cover_summary.json` and `review/logs/indep_audit.json` agree with the counts in the section.
- The README anchors agree: §1 for the 849-node certificate; §3, §4 and §5 finding 3 for the other claims.
- `RevCtrl_pass.lean:307` and `:315` agree.
- `symmetric_extremal.tex:112` lies inside the cited passage.
- The cited project documents exist: Lemmas 2, 4 and 5 in `C3-S/soundness.md`, rules 2 and 3 in
  `C3U2/sigma_split.md`, and the cover with the reduced cut in `C3H6M/soundness_h6m.md`.
- The Mathlib pin is `f897ebcf` and the toolchain is v4.24.0.

### 6. Compile and bookkeeping

- The compile check was run twice in a separate build file. It exits 0. The only undefined reference is
  `sr:def:classes`, an allowed export label of section `sr`, defined at `sections/sr.tex:192`. There are no overfull
  boxes.
- The section has 100 statement environments with 100 map rows, in the same order and with matching kinds.
- All labels start with `cb:`, and all `cb:` references resolve.
- The three export labels `cb:lem:run`, `cb:thm:c3` and `cb:thm:c2` are defined on the right statements.
- There are no machine paths or tool names.

## Findings (all minor)

**m1. The statements of Theorem `cb:thm:c3` and Lemma `cb:lem:all-checked` do not say that they rest on
computer-assisted facts.** (cb.tex:732-737 and 1093-1100)
- Theorem `cb:thm:c2` carries "(Computer-assisted.)" inside its statement. Theorem `cb:thm:c3` and Lemma
  `cb:lem:all-checked` do not, although their proofs use Fact `cb:fact:batches` (and, for c3, Fact
  `cb:fact:roots-codes`). The paragraph after Theorem `cb:thm:c3` discloses this (lines 1098-1100), and the proof of
  `cb:lem:all-checked` cites the Fact, so there is no overclaim.
- Readers who skim theorem heads would see an unqualified "Lean-checked" theorem.
- Suggested fix: add one sentence inside both statements, e.g. "(Its proof uses the computer-assisted
  Facts `cb:fact:batches` and `cb:fact:roots-codes`.)", so that the label travels with the statement when
  `cb:thm:c3` is cited from other sections.

**m2. Notation is overloaded in the central-34 part.** (cb.tex:1276-1277, 1347, 1363; 1291, 1355)
- `B_a(V)` is the Boolean "mask of the double reflection equals mask V" in Theorem `cb:thm:c2-refl`(ii). A few lines
  later, `B_a = bitset(closedP_a)` is a number in the commentary of Theorem `cb:thm:c2` and in the proof of Corollary
  `cb:cor:c2`.
- Similarly, `ρ` denotes a root in §§ on C3 and the reflection on `{0..16}` in the proof of `cb:thm:c2-refl`. That
  proof is next to `ρ_a` of Corollary `cb:cor:c2`, which is the same map written with integer `mod`.
- Nothing is wrong, but a referee has to re-bind the symbols.
- Suggested fix: rename the predicate of (ii) (e.g. `Inv_a(V)`), and use `ρ_a` consistently for the reflection.

**m3. The statement of Proposition `cb:prop:refl` refers to an object defined only in its proof.** (cb.tex:964)
- The statement uses "the involution `r ↦ r*` of `R` defined in the proof" to describe the eight fixed two-token
  layers below H6, so the statement is not self-contained.
- Suggested fix: define `r* = ((a+11)∸r) mod 11` (equivalently `a-r` for `r<a` and `a+11-r` for `r>a`) in the
  statement.

**m4. "Each Lean declaration of the scope has its own statement below" is slightly inaccurate.** (cb.tex:82-83)
- Several declarations share one statement: the families `batch0..batch126` (Fact `cb:fact:batches`),
  `reflection_facts_H6_*` (Fact `cb:fact:refl-h6`), `certs0..certs126` and `closedP1..closedP8`, and also
  `run_sound` and `checkRoot_sound` (Lemma `cb:lem:run`, as the contract requires).
- Suggested fix: rephrase to "each Lean declaration (or numbered family of declarations) of the scope has a statement
  below whose head carries its Lean reference".

**m5. Remark `cb:rem:cert` says "a σ-split on `K` digits".** (cb.tex:551)
- The split is on the `K` smallest free residues, that is, on `K` σ bits. "digits" collides with the base-16 decision
  digits being discussed in the same sentence.
- Suggested fix: "a σ-split on `K` free residues (`2^K` children)".

**m6. The Coverage paragraph says `RevDiff.lean` is "without theorems".** (cb.tex:1437-1438)
- `C3LEAN/review/RevDiff.lean` contains the seven prelude theorems (`Covered.mono`, `beqList_eq`, `beqTok_eq`,
  `beqNode_eq`, `run_sound`, `checkRoot_sound`, `all_append_of` at lines 125-299). Its lines 1-301 are byte-identical
  to the prelude.
- The next sentence ("their prelude copies duplicate covered declarations") makes the intent clear, so this is
  wording only.
- Suggested fix: "without theorems of its own".

**m7. Remark `cb:rem:use` paraphrases its source more strongly than the source.** (cb.tex:1132-1134)
- The remark says "the project later recorded that `lrat-check` verdicts alone carry no weight".
- The cited source (`WRITEUP/note/symmetric_extremal.tex:111-114`) says "Acceptance by lrat-check alone is not a
  certificate ... lrat-check verdicts cited here are supporting only". "Carry no weight" is stronger than "supporting
  only".
- Suggested fix: quote or paraphrase faithfully, e.g. "that acceptance by `lrat-check` alone is not a certificate
  (its verdicts are supporting only)".

## Points I was unsure about (no finding)

- Remark `cb:rem:keys` calls `rev_parent_decodes` (`C3LEAN/review/RevCtrl_pass.lean:315`) a "Lean-checked control".
  That file has no `#print axioms` line for this theorem. Its log (`review/logs/revctrl_pass.log`) shows no error, and
  errors do appear in such logs (see `logs/control_record.log`). The value was also recomputed independently and
  matches, so I accept the wording.
- The label "Lean-checked" for the three `Central34` theorems rests only on `C2FINAL/README.md` §6, since no log is
  committed. The section states this explicitly (Axioms paragraph and map notes), which is the honest treatment. I
  report no finding.
- The section states without proof the semantics of Lean's `Nat.lor`, `<<<` and `Nat.testBit` (`β(x or y) =
  β(x) ∪ β(y)`, `1 <<< c = 2^c`, `testBit(n,i) ⇔ i ∈ β(n)`), as the meaning of these core operations. I regard this as
  stating definitions, not as a gap.
