# Review of section `cb`, round 1, lens: fidelity

Section: `sections/cb.tex` (1,440 lines, 100 statement environments) and `sections/cb.map.tsv` (100 rows).
Lean sources (paths relative to RES): `C3LEAN/C3Cover.lean` (2,327 lines, SHA-256 `4b64293df2ea...`, matches the
section), `C3LEAN/tools/prelude.lean` (`cdcf96de7739...`), `C2FINAL/Central34Orbits.lean` (298 lines, `b396a26b2430...`),
the READMEs of `C3LEAN` and `C2FINAL`, and the logs `C3LEAN/logs/*.log`, `C3LEAN/review/logs/*`.

**Verdict: pass.** No blocker and no major finding. Seven minor findings (presentation, wording and label
consistency), listed at the end. Every definition and statement that cites a Lean name matches its Lean declaration.

## 1. Names and line numbers

All 81 (name, file:line) pairs in the statement heads and in the map were checked mechanically against the Lean
files (a declaration `def|theorem|abbrev|structure|inductive <name>` at the cited line). **All 81 are exact (offset 0).**
The heads in the TeX and the map rows agree: same labels (100 = 100), same kinds, same Lean names, same file:line,
in the same order. The family statements cite their first member: `certs0` (423), `batch0` (1740),
`reflection_facts_H6_1_0` (370), `closedP1` (51). Their line formulas were checked too:
- `batchN` is at 1740 + 4N, and `batch126` is at 2244.
- `reflection_facts_H6_a_s` is at 370 + 3(2a + s - 2), and the last one is at 397.
- `certs126` is at 1668.
- `closedP1..8` are at 51, 78, 105, 132, 159, 186, 213 and 240, and the data end at 264.

All other cited locations exist and hold the cited content:
- `C3LEAN/review/RevCtrl_pass.lean:307` (`rev_uncertified_leaf_passes`) and `:315` (`rev_parent_decodes`);
- `Control_record.lean:305` and `Control_sibling.lean:305`;
- the controls of `C3Cover.lean` at 2266, 2270, 2274, 2278, 2282, 2286 and 2292;
- `#print axioms` at 2301-2327 and at `Central34Orbits.lean:296-298`;
- `Elab.async` at 27;
- `WRITEUP/note/symmetric_extremal.tex:112`, `LRATCHECK20261105`, `C3-S/soundness.md` (Lemmas 2, 4, 5),
  `C3H6M/soundness_h6m.md` (Lemma H6M, the cover theorem with the reduced cut), `C3U2/sigma_split.md` (rules 2 and 3),
  `C2P/review`, `C2ENC`, `C3U2/tools/hullcase.py`, `C3U2/tools/compose.py`, `C3LEAN/tools/*.py`,
  `C3LEAN/review/indep_audit.py`, `C2FINAL/gen_lean.py`, `C2FINAL/hashmatch.py` and
  `C3FINAL/C3FINAL_mirrorh6_roots.tsv`.

## 2. Definitions compared with Lean, one by one

Each definition was read against the Lean source, including the natural-number subtractions, the ordering of
clauses, local `let`s, and Bool versus Prop. Everything matches.

- **m, Tok, Layer, Node, Node.used** (34-51): m = 11; Tok = ℕ×ℕ; Layer = list of tokens. A Node is the structure
  (layers, cube). `used` = flatMap of `map fst`. Exact.
- **pairOptions** (54): the order of Q_{b,c} is (0,0), (0,1), (1,0), (1,1), followed by the recursive call. Exact.
- **layerOptions** (61): `rem` = `filter (!used.contains r) (range 11)`; the singletons `[(r,2)]` come first, then
  `pairOptions rem`. Exact.
- **insTok, sortTok** (66, 71): the comparison `t.1 ≤ u.1` goes to the head. Exact.
- **topCases** (77): `[(0,0)] :: flatMap (i ↦ [[(0,0),(i+1,0)],[(0,0),(i+1,1)]]) (range 5)`. Exact.
- **okey** (82): κ(r,2) = 3r and κ(r,s) = 3r + s + 1 otherwise, after `sortTok`. Exact.
- **lexLe** (85): the three clauses. `a < b || (a == b && ...)`. Exact.
- **mirror** (91): ((11 ∸ r) mod 11, 2 if s = 2 else 1 ∸ s), then `sortTok`. Exact, with ∸ marked.
- **phi** (95): `(a + m - t.1) % m` parses as ((a+11) ∸ r) mod 11. The flip condition
  `decide (t.1 < a) != decide (s = 0)` reads "exactly one of r < a, s = 0". Exact.
- **refl** (101): the patterns `[(0,0)]`, then `[(0,0),(a,s)]`, then the identity. Exact.
- **keptOptions, roots** (109, 113): exact.
- **Node.free** (116): r ≠ 0, r not in used, r not in the cube residues, over range 11. Exact.
- **bitsOf** (120): ⌊i / 2^((K∸1)∸j)⌋ mod 2 (Lean's `K - 1 - j` is (K∸1)∸j). Exact.
- **addBits, sigmaChildren** (123, 127): `foldl (c,t) ↦ insTok t c`. `bits = take K free`; children over
  `range (2^K)`. Exact.
- **conflicts, layerChildren** (132, 137): `t.2 != 2 && C.any (c.1 == t.1 && c.2 != t.2)`. The filter
  `!conflicts`, then append `[o]`. Exact.
- **Covered** (146): the three constructors, with the premises in Lean's order (sigma: K, 2 ≤ |layers|, 0 < K,
  K ≤ |free|, children). The text's "least S-closed predicate" agrees with the inductive definition. Exact.
- **decodeTok, decodeLayer, decodeLayers, decodeCube, decodeKey** (165-191):
  - `Nat.ble c 33` means c ≤ 33. Then c ∸ 1, c ∸ 34, /33 and mod 33.
  - The fuel clauses come first; then `Nat.beq lk 0`, `Nat.beq cm 0` and `Nat.beq (cm % 2) 1`.
  - 4194304 = 2^22 and 2048 = 2^11.

  Exact.
- **beqList, beqTok, beqNode, beqLayer** (194, 199, 202, 335): exact.
- **tokCode, layerCode, rootCode, decodeRoot** (223-238): exact. The fallback 0 for other shapes is stated.
- **Cert, unpack, Cert.keys, run, checkRoot** (245-277):
  - unpack: fuel, then the remaining number is tested against 0 (the section follows the code, not the inaccurate
    docstring "first zero remainder").
  - run: the three match clauses (R1)-(R3), the d = 0, 1, ≥ 2 branches with d ∸ 1, and the fuel 10^6. Exact.
- **isOption, distinctCodes, codeSet, reflectionFacts** (340-365): `Nat.blt` / `Nat.beq` read as <, =. The six
  components (F1)-(F6) match the tuple, with the local `used`, `O` and `kept`. Exact.
- **tsvRootCodes, certs0..certs126, certs, bounds, certifiedKeys** (413, 423-1711, 1714, 1717, 1737):
  - `certs` is right-nested certs0 ... certs126, in order. The only difference from the section's display is a
    redundant pair of parentheses around `certs126`.
  - `bounds` has 127 entries, min 1, max 85 and sum 910. It equals the sizes of the 127 lists (recomputed), and no
    declaration uses it.
  - `certifiedKeys = certs.flatMap Cert.keys`.
- **Central34** (21-269):
  - `inner`, `choose2`, `choose3`, `subcases`, `mask` and `bitset` are exact.
  - `refl` = map ((a+17) ∸ i) mod 17. Exact.
  - `uncovered` has the local B and the negated disjunction of the two `testBit`s. Exact.
  - `closed` sends 1..8 to closedP1..8 and everything else to []. Exact.

## 3. Statements compared with Lean, one by one

- **Covered.mono** (153): the hypothesis S → T pointwise, then Covered S n → Covered T n. Same hypotheses, same
  quantifiers.
- **beqList_eq** (204): `{α : Type}`; the hypothesis eq a b = true → a = b; then for all l1, l2, beqList = true →
  l1 = l2. Exact. **beqTok_eq** (213) and **beqNode_eq** (218) are exact.
- **run_sound** (279): S and fuel, then ∀ stk ds ks, run = true → (∀ k ∈ ks, S (decodeKey k)) → ∀ n ∈ stk,
  Covered S n. The quantifier order is identical.
- **checkRoot_sound** (323): the leaf predicate is `fun n => ∃ k ∈ c.keys, decodeKey k = n`. Exact.
- **all_append_of** (327): exact.
- **batch0..126**: `certsN.all (fun c => checkRoot (decodeRoot c.root) c) = true`. Exact.
- **all_checked** (2247): exact. The term on line 2248 has 126 nested `all_append_of`, matching the proof text.
- **reflection_facts_H3 / H6_a_s** (367-397): the literal tuples (190, true, true, 10, 100, true) and
  (153, true, true, 9, 81, true). The tops are the literal `[(0,0)]` and `[(0,0),(a,s)]`. Exact.
- **topCases_eq** (401) and **strata** (406): exact (`·.length == 1`, `replicate 11 5`, `95 :: replicate 10 76`).
- **roots_match** (1720): `roots.length = 910 ∧ roots.all (beqNode (decodeRoot (rootCode ρ)) ρ) = true`. Exact.
- **roots_codes_match** (1725): `beqList Nat.beq (roots.map rootCode) (certs.map Cert.root) = true`. Exact.
- **roots_eq_tsv** (1730): the four conjuncts. Exact.
- **all_roots_covered** (2251): `∀ ρ ∈ roots, Covered (fun n => ∃ k ∈ certifiedKeys, decodeKey k = n) ρ`. Exact.
  The text truthfully lists the facts its proof uses (`roots_match`, `roots_codes_match`, `all_checked`), and it
  correctly does not list `roots_eq_tsv`, which the Lean proof does not use.
- **subcases_reflection** (273): `all (range 8) (k ↦ Q(k+1))`, with `let a`, `let S`, the four Bool conjuncts, `≤`
  on masks and `==` on masks. Exact.
- **closed_are_subcases** (284): exact. **all_cases_closed** (291): exact. The rewording "uncovered(a, closedP_a) = []
  for a = 1..8" is justified in the text.

**Export labels.**
- `cb:lem:run` is on the lemma whose head cites `run_sound` (279) and `checkRoot_sound` (323).
- `cb:thm:c3` is on `all_roots_covered` (2251).
- `cb:thm:c2` is on `all_cases_closed` (291).

All three are correct.

## 4. Numerical and factual claims, checked independently

- The SHA-256 of all eight Lean files cited (C3Cover, prelude, Central34Orbits, Control_record, Control_sibling,
  RevCtrl_mut, RevCtrl_pass, RevDiff) equals the prefix quoted. Lines 29-329 of C3Cover equal the prelude
  byte for byte. Lines 1-301 of the five control and review files equal the prelude.
- Axioms (`C3LEAN/logs/compile.log`, identical in `review/logs/main_compile.log`):
  - `all_roots_covered`, `run_sound` and `checkRoot_sound`: [propext, Quot.sound].
  - The 11 `reflection_facts`, `roots_eq_tsv` and `all_checked`: [propext].
  - `topCases_eq`, `strata`, `roots_match` and `roots_codes_match`: none.

  All exactly as stated. No Central34 axioms log exists anywhere under RES (checked by searching), as the section says.
- Generated data, recomputed from the Lean source:
  - 910 certificates in 127 lists; 73,567 keys; 942 layer splits and 1,747 σ-splits; 76,256 cover nodes.
  - The largest certificate has 849 nodes.
  - **554** certificates have ds = 0, each with exactly one key.
  - The certificate roots are 910 distinct codes with the same set as `tsvRootCodes` (910 distinct). Root 100 has
    code 41560.
- Model, recomputed by a literal transcription of the Lean definitions:
  - `reflectionFacts` gives (190, T, T, 10, 100, T) for H3 and (153, T, T, 9, 81, T) for all ten H6(a,s).
  - The fixed options are exactly those listed in Proposition `cb:prop:refl`, with r0 = 6, 1, 7, 2, 8 and the
    eight pairs with τ = σ ⊕ f_b.
  - strata = [5]*11 and [95] + [76]*10; |roots| = 910; the strict reduction gives 810.
- Central34, recomputed:
  - closedP1..8 have 287 entries each, and 288 for P6; all masks are distinct, and every entry is a subcase.
  - `uncovered` is empty for every a.
  - Every a has 560 subcases, 14 fixed and 287 with mask V ≤ mask ρ(V). The fixed class is 9, 1, 10, 2, 11, 3, 12, 4.
  - closedP6 contains both [1,7] and [5,16] (one orbit), and no other case contains both members of an orbit.
- `decodeKey 8615616512` was evaluated by hand to ⟨[[(0,0)],[(1,2)]], [(2,0),...,(7,0)]⟩, as in Remark `cb:rem:keys`.
  `decodeLayer 0 = decodeLayer 1 = [(0,0)]`, which confirms the non-injectivity remark.
- The review controls: nine `= false` theorems in RevCtrl_mut, and `rev_extra_key` and `rev_extra_decision` have
  byte-identical certificates. RevCtrl_pass has two `= true` theorems plus `rev_parent_decodes`. The must-fail logs
  end with "Tactic `decide` proved that the proposition ... is false".
- A standalone compile check (two passes, separate job name) exits 0. The only undefined reference is
  `sr:def:classes`, an allowed export label. There are no new macros and no forbidden content (machine paths, tool
  names).

## 5. Coverage

Every declaration of the scope (C3Cover lines 29-2299 and Central34Orbits) is either covered by its own or by a
family statement, or listed under "Not covered, deliberately" with a valid reason:
- the seven negative controls, as tests;
- the `#print axioms` lines;
- the prelude, as the verbatim source;
- Control_record and Control_sibling, as must-fail files;
- RevCtrl_mut, RevCtrl_pass and RevDiff, as review tests or harness.

The headline declarations of the scope in the inventory (`all_roots_covered`, `all_cases_closed`) and all supporting
ones (`all_checked` and the batches, `run_sound`, `checkRoot_sound`, `Covered.mono`, the `beq` lemmas,
`all_append_of`, `roots_match`, `roots_codes_match`, `roots_eq_tsv`, `reflection_facts_*`, `topCases_eq`, `strata`,
`subcases_reflection`, `closed_are_subcases`) are covered.

*Note for the orchestrator (not a finding against `cb`).* The inventory unit `C3-C2-misc` also contains
`AUDIT3/A1_reduction` (`SizeArith.lean`, 20 lemmas; `AssembledSizes.lean`, 7 lemmas including `big_order_orbit`) and
`ES7SPLIT/review/equivalence/BaekSeven.lean` (`baek_seven`). These are outside the scope assigned to `cb` (C3Cover and
Central34). A search of `sections/*.tex` shows that no Stage-1 section mentions them.

## 6. Findings (all minor)

1. **minor: the head of the export lemma `cb:lem:run` is typeset badly** (`sections/cb.tex:560`).
   - The head puts the two `\leanref`s in a `tabular[b]`. In the compiled section (page 7 of the standalone PDF), the
     line "Lean: C3Cover.run_sound, C3LEAN/C3Cover.lean:279," is set as a separate line *above*
     "Lemma 1.53 (Checker soundness; Lean: C3Cover.checkRoot_sound, ...)". It reads as part of the preceding Remark.
   - The contract prescribes the plain form `\leanref{A}{F:l1}, \leanref{B}{F:l2}`.
   - Fix: replace the tabular with that plain form.
2. **minor: wrong word "digits" in Remark `cb:rem:cert`** (`cb.tex:551`).
   - The text says "d = 1+K with 1 ≤ K ≤ 14 a σ-split on K digits". The σ-split is on the K smallest free residues
     (`sigmaChildren n K`, 2^K children, K σ bits). "digit" is already used for the base-16 digits of ds.
   - Fix: write "a σ-split on the K smallest free residues (K σ bits)".
3. **minor: `mod` is used on a possibly negative number** (Corollary `cb:cor:c2`, `cb.tex:1355`; also lines 21
   and 1236).
   - ρ_a(i) = (a − i) mod 17 is applied with a − i < 0 for i > a. The Notation (line 87) defines x mod y only for
     x, y ∈ ℕ (Lean's remainder). The proof of the corollary clarifies the meaning, but the statement itself relies
     on an undefined convention.
   - Fix: define ρ_a(i) as the residue of a − i modulo 17 in {0, ..., 16}, i.e. ((a+17) ∸ i) mod 17.
4. **minor (rigor label consistency; I am unsure whether the contract requires it): computer-assisted labels.**
   - Theorem `cb:thm:c3` (export) and Lemma `cb:lem:all-checked` rest on the computer-assisted Facts
     `cb:fact:batches` and `cb:fact:roots-codes`. Their statements carry no "(Computer-assisted.)", while Theorem
     `cb:thm:c2` does. The paragraph after `cb:thm:c3` states the dependence correctly, so nothing is overclaimed.
   - The `decide +kernel` theorems `reflection_facts_*`, `topCases_eq`, `strata`, `roots_match` and
     `subcases_reflection` are also not labeled computer-assisted. Here the omission is justified by the complete
     written proofs given (Proposition `cb:prop:refl`, Proposition `cb:prop:roots-match`, proof of
     `cb:thm:c2-refl`), but contract rule 6 literally asks for the label on every Lean finite computation.
   - Suggest "(Lean check: computer-assisted; written proof below)" or similar.
5. **minor: one sentence overstates how statements map to declarations** (`cb.tex:82`).
   - The sentence "Each Lean declaration of the scope has its own statement below, so that its head can carry its
     Lean reference" is not literally true. The families `certs0..certs126`, `batch0..batch126`, the ten
     `reflection_facts_H6_*` and `closedP1..closedP8` each share one statement whose head cites only the first member.
     The others are located by line formulas in the text.
   - Fix: reword to "each Lean declaration, or family of generated declarations, ...".
6. **minor: a paraphrase in Remark `cb:rem:use` is slightly stronger than its source** (`cb.tex:1133`).
   - The remark says "lrat-check verdicts alone carry no weight". The cited lines say that acceptance by lrat-check
     alone "is not a certificate" and that lrat-check verdicts "are supporting only"
     (`WRITEUP/note/symmetric_extremal.tex:112-114`).
   - Fix: use the source's wording.
7. **minor: the overview leaves out two facts the proof uses** (overview item (1), `cb.tex:14-16`).
   - The overview says the proof of `all_roots_covered` combines `run_sound` with the kernel evaluation of the 910
     certificates (Fact `cb:fact:batches`). It does not mention that the proof also needs the computer-assisted
     `roots_codes_match` and `roots_match`.
   - The paragraph after Theorem `cb:thm:c3` is correct.
   - Fix: add "and the computer-assisted match of root codes (Fact `cb:fact:roots-codes`)".

Not findings, but checked and correct:
- The section states `unpack` from the code, not from its inaccurate docstring.
- "lines 423-1713" for the certificate data: the last data line is 1711 and line 1713 is the docstring of `certs`,
  which is within tolerance.
- The section correctly treats `rev_parent_decodes` as a theorem proved by `decide +kernel`. Its file compiled
  (`revctrl_pass.log`, exit 0); its axioms are not printed.
