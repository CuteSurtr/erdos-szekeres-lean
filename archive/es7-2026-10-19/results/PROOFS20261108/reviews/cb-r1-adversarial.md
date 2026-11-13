# Review cb, round 1, lens: adversarial

Section: `sections/cb.tex` (1,440 lines) with `sections/cb.map.tsv` (100 rows).
Sources compared: `C3LEAN/C3Cover.lean` (lines 1-422 and 1700-2327 in full, data parsed), `C3LEAN/tools/prelude.lean`,
`C3LEAN/README.md`, `C3LEAN/logs/*`, `C3LEAN/review/*` (Lean files and logs), `C3LEAN/c3cover_summary.json`,
`C2FINAL/Central34Orbits.lean` (full), `C2FINAL/README.md`, the inventory `C3-C2-misc.json`, and the cited project
notes (`C3-S/soundness.md`, `C3H6M/soundness_h6m.md`, `C3U2/sigma_split.md`, `WRITEUP/note/symmetric_extremal.tex`).

## Verdict: PASS (no blocker, no major finding; 6 minor findings)

I tried to break every statement of the section. All definitions and all Lean-referenced statements are faithful to
the Lean source. All written proofs are complete and correct. Every numerical and bibliographic claim I could check
holds, and I reproduced the computed ones independently.

## How the section was attacked

### 1. Fidelity of statements (character by character against Lean)

I compared each of the 81 `\leanref` heads (name and line) with the Lean file, using a script that opens the cited file
at the cited line. All 81 hit the named declaration, with no line offsets. The two `\dirn{...lean:N}` references
(`RevCtrl_pass.lean:307`, `:315`) are exact.

I then compared every definition with the Lean code. Points checked in detail:
- `mirror`: `(m - r) % m` is written as (11 ∸ r) mod 11. `phi`: `(a + m - r) % m` parses as ((a+11) ∸ r) mod 11. The
  σ-flip condition `decide (r < a) != decide (s = 0)` is "exactly one of r<a, s=0".
- `refl`: Lean's match order (`[(0,0)]`, then `[(0,0),(a,s)]`, then default) is kept.
- `okey` (κ(r,2)=3r, κ(r,s)=3r+s+1 otherwise) and `lexLe` (three clauses).
- `bitsOf`: `i / 2 ^ (K - 1 - j) % 2` parses as ⌊i/2^((K∸1)∸j)⌋ mod 2.
- `free` (with r ≠ 0), `conflicts`, `layerChildren`, `sigmaChildren` (`take`, `zip`).
- `decodeLayer` (`Nat.ble c 33`), `decodeLayers`, `decodeCube`, `decodeKey` (2^22, 2^11), `unpack`. The section follows
  the code, not the docstring of `unpack`, which is wrong.
- `run`: clauses R1-R3, the first applicable clause wins. `checkRoot` (fuel 10^6). `isOption` (`Nat.blt`/`Nat.beq`),
  `distinctCodes`, `codeSet`, `reflectionFacts` (six components in order).
- Central34: `inner`, `choose2`, `choose3`, `subcases`, `mask`, `refl` ((a+17)∸i) mod 17, `bitset`, `uncovered`, `closed`.

Theorem statements checked against Lean:
- `run_sound`: quantifier order S, fuel, then ∀ stk ds ks, then two implications, then ∀ n ∈ stk.
- `checkRoot_sound`, `Covered.mono`, `beqList_eq`, `beqTok_eq`, `beqNode_eq`, `all_append_of`.
- The 127 batch theorems, `all_checked`, the 11 reflection facts, `topCases_eq`, `strata`.
- `roots_match`, `roots_codes_match` and `roots_eq_tsv`, each as one conjunction.
- `all_roots_covered`, `subcases_reflection` (the `let a := k+1` and `let S` are unfolded correctly),
  `closed_are_subcases` and `all_cases_closed`.

No hypothesis is missing, added or changed. The `Covered` constructors have the same premises in the same order. The
section's least-fixed-point reading matches the Lean recursor: the recursor's extra hypothesis `Covered S c` in the
minor premises only makes it easier to use, so the inductive predicate is contained in every S-closed predicate.

The export labels `cb:lem:run`, `cb:thm:c3` and `cb:thm:c2` are defined on the right statements. The map has exactly one
row per statement environment (100 of 100), with matching kinds, Lean names and lines.

### 2. Degenerate inputs and hidden hypotheses (general lemmas)
- **`run_sound`** (Lemma cb:lem:run). Cases tried:
  - `stk = []`: vacuous, for every fuel.
  - fuel 0 with a nonempty stack: R2 gives false.
  - d = 0 with ks = []: false.
  - d ∈ {2..15}: K = d−1 ≥ 1, so the premise 0 < K of the (sigma) rule holds.
  - a node with arbitrary contents (tokens with s > 2, layers of length ≠ 1, 2): no step of the proof uses validity.
  - keys equal to 0: harmless, since the proof only uses k ∈ ks.

  Keys are consumed only at leaves, so the key hypothesis passes to the recursive calls unchanged. I found no gap.
  Note that `sigmaChildren(n,0) = [n]`; the rule needs 0 < K, so no self-loop can arise.
- **Lemma cb:lem:codes** (`distinctCodes`). Tried l = [] with any acc, and l = [5,5] (rejected at the second entry).
  The equivalence holds.
- **Lemma cb:lem:sort.** Equal residues give [t,u] (t.1 ≤ u.1), as stated.
- **Lemma cb:lem:options.**
  - (a) for the empty list and for one-element lists (0 = 4·C(1,2)).
  - (b) for arbitrary U, including U containing numbers > 10, and for layers with residues ≥ 11 or 0/≥3 tokens
    (`isOption` false, not in O(U)).
  - Duplicate-freeness across the one-token and two-token parts holds by length.
- **Lemma cb:lem:decode.**
  - Validity (r ≤ 10, s ≤ 2) is exactly what the bound layerCode ≤ 1122 < 1123 needs.
  - One-token layers with s ∈ {0,1} are valid and decode correctly.
  - The digits 0 and 1 both decode to [(0,0)]. This is the non-injectivity noted in Remark cb:rem:keys, and the decoding
    lemma does not need injectivity.
- **Lemma cb:lem:orbits.** The pair argument needs okey(ι x) = map(κ, ι x). This holds because ι x ∈ X is fixed by
  sortTok, and that is a hypothesis. κ is injective on tokens with s ≤ 2. (|X|−F)/2 is exact because the non-fixed
  elements pair up.
- **Proposition cb:prop:refl.** I checked by hand that r* ∈ R, [r*<a] = [r<a], f_{r*} = f_r, and the fixed-point
  analysis for odd and even a. In particular, no residue r ≥ 1 can map to 0, because r ∈ R excludes 0 and a.
- **Lemma cb:lem:c2-subsets and Theorem cb:thm:c2-refl.**
  - For a = 16, inner(16) = {1..15} = I_16. For a = 0 or a ≥ 17 there are 16 inner classes, but the lemma only claims
    1 ≤ a ≤ 16.
  - ρ(0) = a and ρ(a) = 0 need a < 17, which holds for a ≤ 8.
  - The unique fixed class is 9a mod 17. It lies in I_a because 8a ≢ 0 (mod 17).
- **Corollary cb:cor:c2.** For i ∈ {0..16}, ((a+17)∸i) mod 17 equals the residue of a−i. The entries of subcases lie in
  I_a.

### 3. Independent reproduction of every number in the section

I wrote a separate Python transcription of the Lean definitions and parsed the Lean data: the 127 `certsN` blocks,
`tsvRootCodes`, `bounds` and `closedP1..8`. It took a few seconds under `nice`, with no Lean and no solver. Results:

| claim in cb.tex | reproduced |
|---|---|
| reflectionFacts(H3) = (190,T,T,10,100,T); H6(a,s) = (153,T,T,9,81,T) for all 10 | yes |
| fixed points: H3 = ten layers [(b,σ),(11−b,1−σ)], b ≤ 5; H6: [(r0,2)] with r0 = 6,1,7,2,8 plus 8 layers [(b,σ),(b*,σ⊕f_b)] | yes, layer by layer for all 11 top cases |
| strata 5 ×11; 95 then 76 ×10 | yes |
| 910 roots, decodeRoot∘rootCode = id, roots distinct | yes |
| map rootCode roots = certificate roots in order; 910 distinct; same set as tsvRootCodes (910 distinct) | yes |
| bounds: 127 numbers, min 1, max 85, sum 910, equal to the sizes of certs0..certs126 | yes |
| certs126 at line 1668; batch N at line 1740+4N; 126 `all_append_of` in `all_checked`; `certs` right-nested | yes |
| all 910 certificates pass a literal transcription of `run`; 76,256 nodes = 73,567 leaves + 1,747 σ-splits + 942 layer splits; largest certificate 849 nodes | yes |
| 554 certificates with ds = 0, each with exactly one key | yes |
| decodeKey(8615616512) = ⟨[[(0,0)],[(1,2)]],[(2,0),…,(7,0)]⟩ | yes (also by hand) |
| root 0 = 1129, root 1 = 1132, root 100 = 41560 (controls) | yes |
| C2: |subcases(a)| = 560; (ii) holds; 287 and 14; closed_are_subcases; uncovered(a, closedP_a) = []; uncovered(a,[]) has 560 entries | yes, for a = 1..8 |
| closedP_a: 287 entries (288 for a = 6); sorted, no duplicates; closedP6 hits orbit {1,7}/{5,16} twice and every other orbit once | yes |
| x0 = 9,1,10,2,11,3,12,4 | yes |

### 4. Records and citations
- SHA-256 prefixes:
  - `C3Cover.lean` 4b64293df2ea…, `prelude.lean` cdcf96de7739…, `Central34Orbits.lean` b396a26b2430….
  - `Control_record` 5f755e897c30…, `Control_sibling` fb68b330e6e3….
  - `RevCtrl_mut` 49bf2cce1b73…, `RevCtrl_pass` a135e2b92e6a…, `RevDiff` 5aa3f6172026….

  All correct.
- File lengths: 2,327 and 298 lines.
- Lines 29-329 of `C3Cover.lean` are byte-identical to `prelude.lean` (301 lines). Lines 1-301 of all five control and
  review files are byte-identical to the prelude.
- Axiom lines in `logs/compile.log` are exactly as stated, and identical to `review/logs/main_compile.log`. The claim
  "no theorem depends on `Classical.choice`/`sorryAx`/`ofReduceBool`" holds: every unprinted theorem (`Covered.mono`,
  `beq*_eq`, `all_append_of`, `batchN`) is a dependency of a printed one.
- `C2FINAL`: no compile or axioms log exists anywhere under the results directory. README §6 (line 153) says "propext
  only, about 6 s", as quoted.
- Neither file has an `import`. The repository's Mathlib rev is f897ebcf…, and its toolchain is v4.24.0.
- Control lines are 2266/2270/2274/2278/2282/2286/2292 and `#print` lines are 2301-2327; `Control_*` theorems are at
  line 305. All nine `RevCtrl_mut` theorems are `= false`. `rev_extra_decision` and `rev_extra_key` have the same
  certificate. `RevDiff.lean` has no theorems after the prelude.
- `review/logs/indep_audit.json` gives 942/1747/73,567, 73,707 records and 0 mismatches.
- `pilotUnhashed` occurs only in the header comment.
- The cited lemmas and rules exist where claimed: Lemma 2, 4 and 5 in `C3-S/soundness.md`; Lemma H6M and the cover
  with the reduced cut in `C3H6M/soundness_h6m.md`; rules 2 and 3 in `C3U2/sigma_split.md`.
- The directories `C2P/review`, `C2ENC`, `LRATCHECK20261105` and the file `C3FINAL/C3FINAL_mirrorh6_roots.tsv` exist.
- `symmetric_extremal.tex:112` is the lrat-check sentence.
- The intended reading of σ (the side of a line through the centre) matches `C3-S/soundness.md` (σ_i = [x_i < 0]).

### 5. Compile, labels, forbidden content
- A separate wrapper (`build/cbadv/`) compiled twice with exit 0. The only undefined reference is `sr:def:classes`, an
  export label of `sr` that exists in `sr.tex`.
- All labels start with `cb:`. There is no `\newcommand` or `\usepackage`.
- No machine path and no tool name appears.
- No "verified", "certified" or "proved" is used as a rigor claim. The word "certified" occurs only when describing the
  project's records or the Lean name `certifiedKeys`.

### 6. Rigor labels
- The computer-assisted statements are labelled as such, with no hand proof claimed: Fact cb:fact:batches,
  cb:fact:roots-codes, cb:fact:roots-tsv, cb:fact:c2-sub and Theorem cb:thm:c2.
- The decide-checked statements that also get written proofs are the reflection facts, `topCases_eq`, `strata`,
  `roots_match` and `subcases_reflection`. These written proofs are complete and genuinely conceptual (see §2-3 above);
  they do not hide a computation.
- The scope is stated honestly: certification is not encoded, the leaf set is the certificates' own key list
  (`rev_uncertified_leaf_passes`), the dropped options lie outside the file, and `C2FINAL` has no axioms log.

## Findings (all minor)

1. **minor**: cb.tex lines 82-83. *Issue:* "Each Lean declaration of the scope has its own statement below" is not
   literally true. *Evidence:* the families `batch1..batch126`, `reflection_facts_H6_1_1..H6_5_1`, `certs1..certs126`
   and `closedP2..closedP8` share one statement each, and its head cites only the first member. The text and the map
   name the members and give their line formula, so nothing is lost. *Suggested fix:* say "each Lean declaration, or
   each uniform family of them, has its own statement", or list the ten H6 theorems in the head of
   Fact cb:fact:refl-h6.
2. **minor**: cb.tex line 142 and line 1156. *Issue:* "All definitions and theorems of §§… are in
   C3LEAN/C3Cover.lean" and "All definitions and theorems of this subsection are in C2FINAL/Central34Orbits.lean" are
   too broad. *Evidence:* the written steps in those ranges have no Lean declaration: cb:lem:sort, cb:lem:options,
   cb:lem:decode, cb:lem:lex, cb:lem:orbits, cb:prop:refl, cb:prop:roots-match, cb:cor:roots, cb:lem:c2-subsets and
   cb:cor:c2. *Suggested fix:* "All Lean declarations cited in …".
3. **minor**: the heads of cb:fact:refl-h3, cb:fact:refl-h6, cb:fact:topcases, cb:fact:strata, cb:fact:roots-match and
   cb:thm:c2-refl. *Issue:* these are `decide +kernel` computations in Lean, and the scope note asked for them "stated
   precisely as computer-assisted facts" (contract rule 6). They are labelled "Lean-checked by kernel evaluation", with
   complete written proofs, instead of "computer-assisted". *Evidence:* I checked that each written proof is complete,
   and the claimed fixed points and counts agree with an independent evaluation, so there is no overclaim. I am unsure
   whether the contract wants the label even when a full hand proof is given. *Suggested fix:* add
   "(computer-assisted in Lean; written proof in Proposition …)" to these heads, or leave as is if the editors accept
   the stronger treatment.
4. **minor**: cb.tex line 551 (Remark cb:rem:cert). *Issue:* "d=1+K … a σ-split on K digits" is confusing, because
   "digits" already means the base-16 digits of ds. *Suggested fix:* "a σ-split on the K smallest free residues
   (K bits)".
5. **minor**: cb.tex lines 1133-1134 (Remark cb:rem:use). *Issue:* "lrat-check verdicts alone carry no weight" is
   slightly stronger than the source. *Evidence:* `WRITEUP/note/symmetric_extremal.tex:111-114` says "Acceptance by
   lrat-check alone is not a certificate … lrat-check verdicts cited here are supporting only". *Suggested fix:*
   "lrat-check verdicts alone are not certificates (supporting only)".
6. **minor**: cb.tex lines 1146-1147 (Remark cb:rem:use). *Issue:* "the 90 options … and the 720 options … that these
   reductions drop … do not occur in the file" is imprecise. *Evidence:* these options are members of
   `layerOptions(...)` and are evaluated in `reflectionFacts` and in `control_strict_reduction`. What is true is that
   they are not roots and no certificate covers them. *Suggested fix:* "are not roots of the file and are covered by
   no certificate".

## Why each main statement survives
- **cb:lem:run (run_sound, checkRoot_sound).**
  - The statement is faithful.
  - The induction on fuel covers the empty stack, fuel 0, and all three digit classes. In the d = 0 case the proof uses
    `beqNode_eq`, so the leaf is equal to a decoded key, not merely matched by name.
  - The split cases re-use the full key list, so the hypothesis carries over.
  - (b) is (a) with the witness k.
  - No validity of the nodes is used anywhere.
- **cb:thm:c3 (all_roots_covered).**
  - Every step of the proof is justified: `roots_match` (with a hand proof as well), Lemma cb:lem:beqlist turning
    `roots_codes_match` into a list equality, `all_checked` (with `all_append_of`, 126 times), `checkRoot_sound`,
    and monotonicity into `certifiedKeys` by flatMap membership.
  - The theorem has no hypotheses, and the leaf predicate is exactly the Lean one. The section stresses that this
    predicate is the certificates' own key list.
  - I reproduced all 910 checks and the node counts independently.
- **cb:thm:c2 (all_cases_closed).**
  - The statement is faithful, and its computer-assisted status is stated.
  - The set-form corollary is derived correctly through Lemma cb:lem:bits; it holds for arbitrary lists, including
    unsorted `refl` images.
  - The statement is not vacuous: `uncovered(a, [])` has 560 entries.
  - I reproduced it for a = 1..8, together with the closedP6 double hit.
