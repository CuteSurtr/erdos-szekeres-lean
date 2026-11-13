# Review pc, polish round 1, lens: referee (independent full read)

Section: `sections/pc.tex` (996 lines), map `sections/pc.map.tsv` (32 rows + header). Lean paths are relative to the
results directory (RES) or to the repository root, as in the section. Line numbers are those of `sections/pc.tex`.

**Verdict: PASS.** I found no blocker and no major finding. There are three minor findings, F1 to F3 below. I formed
my view before reading the earlier reports. None of the three findings is in those reports.

## What I checked, and how

1. **Every statement against its Lean declaration.** I read all 545 lines of `LEANEXT/phase/PhaseClassification.lean`.
   I also read the new lines of `LEANEXT/linked/Linked.lean` (1385-1416), `LEANEXT/capstone/Capstone.lean` (1966-2004)
   and `LEANEXT/capstone/Capstone2.lean` (2004-2132), and `LAYERLEAN/LayerLemma.lean` 925-1033 (polar, the rules,
   `dist2`, `dist2_le_of_later`).

   That makes 53 declarations: 39 in PhaseClassification, 2 in Linked, 3 in Capstone and 9 in Capstone2. For each I
   compared hypotheses, conclusion and quantifier structure with the section. I paid particular attention to:
   - the gap conditions: `α+2π−δ≠π` for B, `β−α≠π` for D, `δ−β≠π` for A;
   - which radius is not assumed positive in each rule;
   - the order `¬H3 ∧ ¬H1` in `RunMidA`;
   - `0<α−δ+2π` in rule A;
   - the seven nested implications of each half of `orient_sign_of_phase`, including the relabelled radii in (ii);
   - the conjunction shape of `phase_trichotomy` and `word_dichotomy`;
   - `Set` in `halfplane_of_runMidB` and `Finset` for `S`;
   - `Invariant`, which only says the map sends S into S;
   - the casts `(k:ℝ)` in `inArc` and `polar_add_int_two_pi`, and `(m:ℝ)` in `2π/m` with `0<m` in (L);
   - which `polar` each statement uses (`PhaseClassification.polar` or `LayerLemma.polar`);
   - which `dist2` is used, and the hull-vertex position and index inequalities in all seven layer theorems.

   Everything matches. For `Invariant`, `hullVerts`, `peel`, `rotAbout` and `HasConvexNGon` I read the definitions at
   `LAYERLEAN/LayerLemma.lean:105, 111, 298, 374` and `ErdosSzekeres/Definitions.lean:21`. The section paraphrases them
   correctly.
2. **References.** A script extracted all 54 distinct `\leanref` pairs. Each named declaration is exactly at the cited
   line. The extra `\dirn{...:N}` citations are also exact:
   - LayerLemma 932, 999, 1012;
   - Linked 932, 999, 1012;
   - Capstone2 940, 1007, 1020;
   - `SoundWord.lean:222`, `ArcBridge.lean` 393 and 473, `Audit.lean` 45-49;
   - PhaseClassification 323-335 and 346-362.
3. **Cross-section `\ref`s.** I opened each target and checked that it says what pc uses:
   - `fd:def:point`, `fd:def:orient`, `fd:def:rot`, `fd:def:inv`, `fd:def:ngon`;
   - `fd:lem:orient` (a)-(c), including the `orient_cycle` form `orient(b,c,a)=orient(a,b,c)`, which matches
     `ErdosSzekeres/Orientation.lean:15`;
   - `ll:def:hv` (defined as a subset of S) and `ll:def:peel`;
   - `lg:def:polar`, `lg:lem:polar`, `lg:lem:ruleA`, `lg:lem:sinadd`, `lg:lem:ruleB`;
   - `lg:thm:radius`, which has the same hypotheses and the same orientation of the inequality as pc's paraphrase
     ("n≤n′, x∈hv(peel(S,n)), y∈peel(S,n′) ⇒ dist2(c,y)≤dist2(c,x)").

   All are allowed export labels, and all 10 pc export labels are defined on the named statements. No other section
   cites a pc label.
4. **Provenance.**
   - All line counts and SHA-256 prefixes of the 11 cited files match `shasum`.
   - I re-ran every `diff` relation in "Sources":
     - PhaseClassification 40-102 against LayerLemma 931-996: only docstrings differ;
     - Linked 1-1147 equals LayerLemma 1-1147;
     - Linked 1-1384 equals Merged 1-1384;
     - Capstone 19-1424 equals Linked 11-1416;
     - Capstone 1426-1965 equals PhaseClassification 6-545;
     - Capstone2 1-2003 equals Capstone 1-2003;
     - Capstone2 is byte-identical to `ENCBLEAN/geo/ES8Geo/Capstone2.lean` and is listed in `SOURCES.sha256`.
   - The offsets +1420 and +8 are right.
   - `phase/logs/axioms.log` has exactly the 16 listed theorems, each with the three standard axioms. Each of the
     other 23 PhaseClassification declarations is used in the statement or proof of one of the 16.
   - There is no saved axiom output anywhere in RES for the new Linked/Capstone declarations. I searched every non-Lean
     file. This agrees with the text.
   - The ENCBLEAN chains hold, checked by grep and by reading the code:
     - `ne_of_mem`, `exists_angle` and `sqrt_dist2_pos` are used at `Labelling.lean:63-65` in `Lab.exists_layer_polar`,
       which `labelling_of_counterexample` calls;
     - `dist2_polar` is used at `Labelling.lean:133`; it resolves to `LayerLemma.dist2_polar`, because the file has
       `open ErdosSzekeres.LayerLemma` and the definition is at Capstone2:1398;
     - `polar_eq` and `polar_add_int_two_pi` are used in `P_eq_polar`, which feeds `arcFrame`, then
       `labelling_ruleA/B` (`ArcBridge.lean:464`, `:481`), then `modelOfLabelling`;
     - the axioms are pinned at `Audit.lean:45-49`;
     - the layer theorems and `orient_pos_of_alternating_polar` are not used outside the copy.
   - `m4_build.log` shows only KeyOrder messages. `DESIGN.md` (M4 row) confirms that Capstone2 was part of that build.
   - The toolchain is v4.24.0 and Mathlib is `f897ebcf` (repository and `geo/lake-manifest.json`). The ENCBLEAN root
     package has no Mathlib.
   - A grep of the four files finds no `sorry`, `admit`, `axiom` or `native_decide`. `decide` occurs only in
     `word_dichotomy` among this section's declarations; the other occurrence, at Linked:1125, is a copied
     declaration.
5. **Claims about how Lean evaluates `decide`.** I checked these read-only against the Lean 4.24.0 sources in the
   local toolchain:
   - The implication instance (`Init/Core.lean:1162`) decides the premise first and touches the conclusion's instance
     only in the `isTrue` branch.
   - `decide`'s `doElab` (`Lean/Elab/Tactic/ElabTerm.lean:466-477`) whnf-reduces the instance in the elaborator and
     returns `of_decide_eq_true _ _ (Eq.refl true)`, which the kernel re-checks.
   - The failure message is "Tactic `decide` proved that the proposition … is false" (`ElabTerm.lean:506-508`).

   The section's description in "How Lean checks it" is accurate. The M7 line in `mutants.log` and `mutants.py` match
   the text.
6. **Identities (sympy 1.13.3, `build/pc_p1ref_sympy.py`).** All give 0:
   - the polar formula (a);
   - the bracket expansion `[v−u,w−u]=[v,w]−[v,u]−[u,w]+[u,u]=[u,v]+[v,w]+[w,u]`;
   - `[u,v]=r_a r_b sin(β−α)`;
   - (b) directly;
   - `sin x+sin y−sin(x+y)=sin x(1−cos y)+sin y(1−cos x)`;
   - the rule-B decomposition in (e), both as an identity in `x,y` and against (a) with `β=α+x`, `δ=α+x+y`;
   - `(p−c)·(cos φ, sin φ)=r cos(θ−φ)`;
   - `dist2(c,polar(c,r,θ))=r²`;
   - `sin(arccos t)=√(1−t²)`;
   - 2π-periodicity for integer k;
   - `sin(α−δ+2π)=sin(α−δ)`.
7. **Exact exhaustive test (`build/pc_p1ref_exact.py`).** Angles are rational multiples of π: α ∈ {0, π/7, −5π/3},
   and β, δ = α + jπ/24 with j from −48 to 95. This includes every case where a gap equals π. `inArc` is decided
   exactly and cross-checked by brute force over k. The test covers:
   - Lemma `pc:lem:shift` (c),(d), on all triples, ordered or not;
   - Lemma `pc:lem:empty` (a)-(f), on all triples satisfying their hypotheses;
   - Lemma `pc:lem:arc12`;
   - Theorem `pc:thm:alternating`, including the gap = π boundary of Remark `pc:rem:alt-boundary`;
   - Proposition `pc:prop:exactly-one`;
   - Theorem `pc:thm:runB` in both directions, and (⇐) without the gap hypothesis;
   - Proposition `pc:prop:gaps` and the exclusivity claim of Remark `pc:rem:gaps`(2);
   - Theorem `pc:thm:trichotomy` (ii), and "exactly one pattern" under genericity;
   - Remark `pc:rem:runs` (H1∨H2∨H3 for the ordering alone).

   On 3243 ordered triples there were **0 failures**. The two examples (0,π/2,π) and (0,π,3π/2) behave as stated. The
   8-word table is exact (words and run positions), and PPAPPA violates the premise and has neither property.
8. **Float test of the orientation statements as transcribed (`build/pc_p1ref_float.py`).** I used 200000 random
   configurations with real angles in [−20,20]:

   | Statement | Instances | Violations |
   |---|---|---|
   | `orient_sign_of_phase` (i) | 49954 | 0 |
   | `orient_sign_of_phase` (ii) | 49385 | 0 |
   | rule A | 24882 | 0 |
   | rule B | 8299 | 0 |
   | rule D | 8436 | 0 |
   | rule A-middle | 8337 | 0 |
9. **Proofs read step by step.** Every case split is exhaustive. I checked each inequality chain by hand, including
   all 18 lift checks of Lemma `pc:lem:empty` with the Lean integers m (0,0,0 / 0,0,0 / 1,0,0 / 1,0,0 / 1,1,0 /
   0,0,−1), the three cases of Lemma `pc:lem:arc12`, and the two relabellings in Theorem `pc:thm:rule-run`, including
   the radius permutations and the `orient_cycle` step. Every use of an earlier result meets that result's
   hypotheses. There is no circularity: helpers (d) uses `pc:lem:exists-polar`, (a) and (c); (e) uses (d) and (b).
   Nothing is delegated to Lean.
10. **Contract form.**
    - The compile check (`build/pc_p1ref_wrapper.tex`, two passes) exits 0, with 0 overfull boxes. The only undefined
      references are the expected fd:/ll:/lg: labels.
    - The map has 5 fields per row, and its labels and kinds equal the 32 environments in order.
    - There are no machine paths, tool names, `\newcommand` or `\usepackage`.
    - Rigor vocabulary is respected. The only uses of "proved" are a negative statement and a quote of Lean's message.
11. **Head layout.** The polish moved the (b)-(e) references of Lemma `pc:lem:polar-facts` and Theorem `pc:thm:layers`
    from the heads into the parts. I re-tested the contract's all-in-head form under the updated preamble with a copy
    in `build/pc_p1ref_headtest/`. It still overflows, by 11.7 pt and up to 59 pt. The current layout is therefore
    justified, and I do not report it.

## Findings

### F1 (minor): the blanket rigor sentence also covers remarks whose parts name Lean declarations
- **Location:** pc.tex:60-61 ("Every statement below that cites a Lean declaration, in its head or in one of its
  parts, is Lean-checked"). It interacts with:
  - Remark `pc:rem:gaps`, part (2) (pc.tex:551-555), which names `\lean{gap_classification}`;
  - Remark `pc:rem:word-scope` (pc.tex:812-826), which names `EncB.wordSpec`, `EncB.Geo.Arc.arcFrame` and
    `EncB.Geo.labelling_ruleB`.
- **Issue:**
  - The contract lists `remark` among the statement environments.
  - Read literally, the sentence makes Remark `pc:rem:gaps` "Lean-checked", because one of its parts cites a Lean
    declaration. That part's content is the exclusivity observation, which the remark itself labels "a written
    observation, not part of the Lean statement".
  - The same applies to Remark `pc:rem:word-scope`. It also describes the (Python) encoders' reading of the sorted
    word and says that link "is not proved in LEANEXT".
  - The local labels are explicit, so a careful reader is not misled. Still, the blanket sentence is too wide and
    contradicts them.
- **Fix:** restrict the sentence. For example: "Every definition, lemma, proposition, theorem and corollary below
  whose head or parts carry a Lean reference is Lean-checked; remarks are commentary, and the written observations
  in them are labelled as such."

### F2 (minor): the opening sentence still asserts "six points" unconditionally
- **Location:** pc.tex:4-7 ("Together with the three antipodal directions α+π, β+π, δ+π they give six points on the
  circle of directions … classify the cyclic pattern of these six points").
- **Issue:**
  - When a gap equals π, a direction coincides with an antipode, so there are fewer than six distinct points and no
    six-letter pattern. For example, with (0, π/2, π) we have δ = α+π.
  - The polish fixed exactly this imprecision in Remark `pc:rem:reading` (adversarial F4 of round 1), but not in the
    opening sentence. The theorems themselves treat the boundary correctly.
- **Fix:** add "(distinct unless one of the gaps β−α, δ−β, α+2π−δ equals π)" after "six points". Alternatively, say
  "six directions, counted with multiplicity".

### F3 (minor): one unstated link in the axiom-transfer argument for the helpers used by ENCBLEAN
- **Location:** pc.tex:73-82 ("… through the byte-identical copy of Capstone2.lean … so the axioms of the declarations
  used are among these three as well").
- **Issue:**
  - The `#guard_msgs` pins bound the axioms of the ENCBLEAN-built constants. The section's statements cite the
    LEANEXT originals.
  - Transferring the bound needs the two elaborations to agree. The text gives the byte-identical source and the
    shared Lean/Mathlib pins ("Sources", pc.tex:56-58).
  - It does not mention the third ingredient. `Capstone2.lean` imports repository modules (`ErdosSzekeres.Definitions`,
    `Orientation`, `OrientationGeometry`, `Suk.OrientationClique`, …), and in ENCBLEAN these are vendored copies
    (`ENCBLEAN/geo/VENDOR.sha256`, "verbatim copies of repository modules").
  - I checked that the vendored Basic, Definitions, Orientation, OrientationGeometry and Suk/OrientationClique have
    the same SHA-256 as the repository files. The argument is therefore correct, only incompletely sourced.
- **Fix:** add a half-sentence, for example "(the ENCBLEAN geometric package imports verbatim copies of the
  repository modules that `Capstone2.lean` needs, `ENCBLEAN/geo/VENDOR.sha256`, so the copies are the same Lean
  constants as the originals)".

## Scratch files (staging area)
- `build/pc_p1ref_wrapper.tex` and its `.log`/`.pdf`: compile check.
- `build/pc_p1ref_sympy.py`, `build/pc_p1ref_exact.py`, `build/pc_p1ref_float.py`: the checks in items 6-8.
- `build/pc_p1ref_headtest/`: the head-layout experiment of item 11. It is a modified copy and not a deliverable.
