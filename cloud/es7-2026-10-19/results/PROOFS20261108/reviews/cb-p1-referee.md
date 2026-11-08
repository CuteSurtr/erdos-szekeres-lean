# Referee report: section `cb`, polish round 1 (independent full read)

Files read: `sections/cb.tex` (1,475 lines), `sections/cb.map.tsv` (100 rows), all of `C3LEAN/C3Cover.lean` except the
certificate literals (which were parsed by script), `C3LEAN/tools/prelude.lean`, `C2FINAL/Central34Orbits.lean` (all of
it), and every record the section cites. Paths are relative to RES (`cloud/es7-2026-10-19/results`). I formed my view
before reading the earlier reports (`cb-r1-*`, `cb-polish-r1-fix.md`).

## Verdict: PASS (0 blocker, 0 major, 3 minor)

I re-derived every proof step myself. I compared every statement with its Lean source and recomputed every number the
section takes from the data. I found nothing false, and no statement that differs from Lean. The rigor labels are not
rounded up, and no hypothesis is presented as proved. The three findings below are minor. The first two are small
inaccuracies in commentary. The third is a gap at the level of the whole document and lies outside the contract
scope of `cb`.

## Findings

### F1 (minor): one coverage sentence overstates
- *Location:* `cb.tex` lines 88-93 ("Rigor labels and dependencies").
- *Issue:* the text says "Each Lean declaration of the scope, or each uniform family of generated declarations (…), has
  a statement below whose head carries its Lean reference". This is false for the seven negative controls,
  `control_missing_record` … `control_phi_mutant` at `C3LEAN/C3Cover.lean:2266-2292`. They are declarations of the
  scope file, and the section's own Coverage (lines 1451-1459) lists them as "Not covered, deliberately", with no
  statement. (The round-1 fix added the families but did not exempt the controls.)
- *Fix:* "Each Lean declaration of the scope other than the seven negative controls (see Coverage), or each uniform
  family of generated declarations (…), has a statement below …".

### F2 (minor): an unsourced data count, cited to the wrong place
- *Location:* `cb.tex` lines 746-747 (after Fact `cb:fact:batches`) and lines 1147-1148 (Remark `cb:rem:use`).
- *Issue:* "554 of the 910 roots" have ds = 0 and are their own single leaf. This number comes from this document's own
  count of the certificate data. No project record states it: a word search for 554 in `C3LEAN/`, `C3FINAL/` and
  `C3U2/` finds only an unrelated "1,554" in `C3U2/README.md`. Remark `cb:rem:use` cites Fact `cb:fact:batches` for
  it, but the statement of that Fact does not contain the number. The count itself is correct: my parse of
  `certs0`…`certs126` gives 554 certificates with ds = 0, each with exactly one key.
- *Fix:* at line 746, say that the number is counted from the certificate data of `C3LEAN/C3Cover.lean` and is not a
  Lean statement. At line 1148, replace "(Fact~\ref{cb:fact:batches})" with "(see the paragraph after
  Fact~\ref{cb:fact:batches})".

### F3 (minor; document level, outside the contract scope of `cb`): three files of the inventory unit are covered nowhere
- *Location:* Coverage, `cb.tex` lines 1417-1475; and the document as a whole.
- *Issue:* the inventory unit `C3-C2-misc` also holds Lean-checked declarations that no section covers or mentions:
  - `AUDIT3/A1_reduction/SizeArith.lean`: 20 lemmas;
  - `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean`: 7 lemmas;
  - `ES7SPLIT/review/equivalence/BaekSeven.lean`: `baek_seven`.

  A search of `sections/*.tex` and `proofs.tex` for these names finds no hit. The writer's report lists them as
  outside the scope of `cb`, and the contract table gives `cb` only the threefold cover and the central 34 split, so
  this is not a defect of `cb`. The document as a whole, however, omits them without saying so.
- *Fix:* for the orchestrator to decide. At the least, add one sentence (in `cb`'s Coverage or in the front matter)
  saying that these members of the inventory unit are outside this section's scope, and where they are treated, if
  anywhere.

## What I checked (evidence)

### Fidelity
- **Definitions.** I compared every definition with Lean, clause by clause:
  - `m` … `Node.layerChildren`, `Covered`, the decoders and codes, `beq*`, `Cert`, `unpack`, `run`, `checkRoot`,
    `isOption`, `distinctCodes`, `codeSet`, `reflectionFacts`;
  - the Central34 definitions.

  All truncated subtractions are marked with ∸: `11∸r`, `(a+11)∸r`, `1∸s`, `(K∸1)∸j`, `c∸1`, `c∸34`, `d∸1`,
  `(a+17)∸i`. Every divisor is positive, so Lean's convention for division by zero never applies. The match order of
  `refl` and the clause order of `run` are kept.
- **Theorems.** The quantifier order and implications match Lean for `run_sound` and `checkRoot_sound` (the leaf
  predicate is `∃ k ∈ c.keys, decodeKey k = n`). They also match for `Covered.mono`, `beqList_eq` (`{α : Type}`),
  `beqTok_eq`, `beqNode_eq`, `all_append_of`, `batchN`, `all_checked`, the 11 `reflection_facts_*`, `topCases_eq`,
  `strata`, `roots_match`, `roots_codes_match`, `roots_eq_tsv` and `all_roots_covered`.
- **Central34 theorems.** In `subcases_reflection` the local `let a`/`let S` are unfolded correctly.
  `closed_are_subcases` and `all_cases_closed` are exact.
- **Map.** A script matched the 100 statement environments with the 100 map rows (label, kind, Lean names, file:line)
  and opened each cited file at each cited line: 0 mismatches.
- **Line numbers.** Batch N is at line 1740+4N for all 127. The H6 facts are at 370+3(2a+s−2). `certs126` starts at
  line 1668 and the data end at 1711. The `closedP` lists start at 51, 78, …, 240 and end at 264. The controls are at
  2266-2292, `#print` at 2301-2327 and 296-298, and `RevCtrl_pass.lean` at 307 and 315.
- **`certs`.** It is `certs0 ++ (… ++ (certs126))`, nested to the right. The term of `all_checked` has 126
  `all_append_of`.

### Proofs, re-derived step by step
- **All correct.** Lemma `cb:lem:bits`, the least-fixed-point reading of `Covered` (including the recursor's extra
  hypothesis), monotonicity, the `beq` lemmas, and `run_sound` (fuel 0, empty stack, d = 0/1/≥2, keys passed
  unchanged in the split cases).
- **Also correct.** `distinctCodes`/`codeSet`, `sortTok` on short lists, `layerOptions` (counts by
  4n+4C(n,2)=4C(n+1,2)), decoding (bounds 1..1122 < 1123), `lexLe` as a total order, and the orbit-counting lemma
  (κ is injective on valid tokens; okey(ι x) needs ι x ∈ X fixed by `sortTok`, which is a hypothesis).
- **Proposition `cb:prop:refl`.** r* ∈ R, [r*<a]=[r<a], f_{r*}=f_r, the unique fixed residue r0 = 6,1,7,2,8, the
  8 fixed two-token options, and F = 10/9, kept = 100/81, strata 5+95 and 5+76.
- **Remaining results.** Proposition `cb:prop:roots-match`, Corollary `cb:cor:roots`, Theorem `cb:thm:c3` (steps 1-5),
  Lemma `cb:lem:c2-subsets` (C(k−1,2)+C(k−1,3)=C(k,3)), and Theorem `cb:thm:c2-refl`: ρ_a is an involution of
  {0..16} swapping 0 and a; the fixed point is 9a mod 17 = 9,1,10,2,11,3,12,4; 7+7 = 14; 14+546/2 = 287.
  Corollary `cb:cor:c2` is also correct.
- **No circularity.** Proposition `cb:prop:refl` and Proposition `cb:prop:roots-match` use no computed Fact.
- **sympy.** The binomial identities, 190/153/560, 910/810/90/720, the counts of kept options, 2^22, 2^11, 2^64,
  1122, 2⁻¹ ≡ 9 (mod 17), the r0 list, 76,256 = 73,567+1,747+942, and the decoding of key 8615616512.

### Independent recomputation from the data (Python transcription, a few seconds under `nice`)
- **Reflection facts.** I reproduced `reflectionFacts` for all 11 top cases. The fixed-point sets match the statement
  of Proposition `cb:prop:refl` exactly.
- **Roots.** There are 910 roots. Their codes equal the certificate roots in order, and their set equals
  `tsvRootCodes`. `tsvRootCodes` equals the TSV root column in file order (my own name→code decoder).
- **`bounds`.** It has 127 entries, ranging from 1 to 85, with sum 910. They are exactly the sizes of
  `certs0`…`certs126`, and no theorem uses `bounds`.
- **Node counts.** The data give 73,567 keys, 942 layer splits and 1,747 σ-splits: 76,256 nodes, with at most 849 per
  certificate. 554 certificates have ds = 0. No key is 0.
- **Controls.** As described: the fourth key removed, two adjacent keys (positions 1 and 2) swapped, root 100 = 41560
  without its last key, root 1 = 1132. `rev_extra_decision` has the same certificate as `rev_extra_key`. All prelude
  copies are byte-identical.
- **Central 34.** For a = 1..8: 560 subcases, 287 orbits, 14 fixed, 287 with ≤; every `closedP_a` entry is a 2- or
  3-subset of I_a, increasing, with no duplicate sets, and every orbit is met. `closedP6` (288 entries) is the only
  list that holds both members of an orbit, {1,7} and {5,16}. `pilotUnhashed` occurs only in the header comment.

### Records and citations
- **Hashes and the prelude.** All eight SHA-256 prefixes are correct. Lines 29-329 of `C3Cover.lean` are
  byte-identical to `prelude.lean`.
- **Axioms.** The axiom lines in `C3LEAN/logs/compile.log` are exactly as stated, and identical to
  `review/logs/main_compile.log`. No log exists for `C2FINAL`. README §6 says "propext only, about 6 s", and the
  section discloses that the Lean-checked label of the three Central34 theorems rests on this record.
- **Toolchain and paths.** Lean v4.24.0 and Mathlib f897ebcf. All 36 `\dirn` paths exist.
- **Cited passages.** Each of these says what the section claims:
  - `symmetric_extremal.tex` lines 111-114;
  - `SYMMETRIC.md` §3 and Theorems 1 and 4;
  - `C3-S/soundness.md` Lemmas 2, 4 and 5;
  - `C3H6M/soundness_h6m.md` (Lemma H6M, and the cover with the reduced cut);
  - `C3U2/sigma_split.md` rules 2 and 3;
  - `C3LEAN/README.md` §1, §3, §4, §5 (finding 3) and §6;
  - `C2FINAL/README.md` Status, §1, §4, §6 and §9;
  - the `covered2` function of `compose.py` (it requires a layer-split record at cube nodes).
- **External references.** The only one is `sr:def:classes`, an allowed export label of `sr`, and it defines
  `Threefold33` and `HalfTurn34` as claimed. The three citations of `cb` labels in `ar.tex` and `sr.tex` claim nothing
  beyond what `cb` states.

### LaTeX and rules
- **Compile.** `build/cb_p1ref_wrapper.tex` was compiled twice: exit 0, no overfull box, and the only undefined
  reference is `sr:def:classes`. Pages 7 and 15 were inspected: the heads, including the two-reference head of
  `cb:lem:run`, render correctly.
- **Section file rules.** It defines no macros and loads no packages. There is no machine path and no tool name. "Verified" is never used, "certified" appears only for project records, and "proved" appears only
  inside written proofs or in "not proved".
