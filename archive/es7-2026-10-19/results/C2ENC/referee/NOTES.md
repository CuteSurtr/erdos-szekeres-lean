# Referee notes: soundness of `zcnf.py rot` (m = 2, `--hull`)

*Edited for the repository: paths are given relative to this directory or to `cloud/es7-2026-10-19/results`, the
reproduction commands are adapted to the layout of `C2ENC` (the private copy `work/` of `tests/` used for the runs is not
kept), the referee's own mutants are called "additional mutants", the date is given in UTC, and a remark about the local
working copy is removed. The verdict and the findings are unchanged. The hashes below are those of the refereed
versions; the files in `C2ENC` are the revised versions (`../README.md`).*

Refereed 1 November 2026 (UTC). Objects: `proof.md` (sha `ae379b45…`), `perturbation.md` (`28fbbd6a…`),
`class_table.md` (`d7d7c9fc…`), `tests/` (all 29 entries of the authors' `SHA256SUMS.txt` verified). Encoder:
`SYMZ/zcnf.py`, sha `13d6c162…` (= `tests/zcnf_orig.py`, byte-identical). Base CNF (a regenerated copy) re-hashed:
`b0061e90…fd8ff1`; map `2476faff…`.

## Verdict

**Sound, with minor documentation gaps.** No blocking or major finding.

- Every clause family the code emits for `rot 17 7 --m 2 --hull` is covered by the proof. I enumerated the families
  from the code myself, before reading the proof.
- Each derivation (Lemmas 1–8, Propositions 7–11) re-derives correctly.
- The `--hull` normal-form argument is right.
- The tests have teeth. I confirmed this with re-runs, nine additional mutants and two independent evaluators of my
  own, one of them on the certified 621 MB base.

## 1. Clause families, enumerated from the code

Every `sink.add`/`forbid` call site in `zcnf.py`, and what `build(sb=True, hull=True)` emits:

| family | code lines | emitted for rot, m = 2, --hull | clauses in base | proof |
|---|---|---|---:|---|
| identifications (G) group, (C) centre | 166–172, 174–190 | variable classes only, no clauses | (2,856 classes) | §4.1, Lemma 5 |
| GP fast path (3 nonzero terms, 6 distinct vars; 16 clauses each) | 239–244 | yes | 12,522,880 | §5.1, Prop 7 |
| GP generic path (`forbid`; a zero term or repeated vars) | 245–257, 222–224 | yes | 65,280 | §5.1, Prop 7 |
| A4 interiority (all 4-sets without a zero triple) | 260–273 | yes | 413,440 | §5.2, Prop 8 |
| centre facts | 313–328 | **no** (`m >= 4` only) | 0 | §5.6 |
| CONV4 (6 convex patterns ⇒ conv) | 281–293 | yes | 138,992 | §5.3, Lemma 8, Prop 9 |
| CONV5, CONV6 | 294–303 | yes | 139,128 + 672,792 | §5.3, Lemma 7, Prop 9 |
| KGON (canonical 7-sets) | 304–310 | yes | 2,689,808 | §5.3, Prop 9 |
| SB units (line 336 sector unit: m ≥ 4 only) | 330–351 | yes | 136 | §5.4, Prop 10 |
| HULL (X₀ in no triangle of other points) | 353–365 | yes | 10,880 | §5.5, Prop 11 |

The total is 16,653,336, which equals the header. No other emission path exists.

A zero literal cannot reach the file even if a family failed to exclude zero triples:

- In A4, CONV4 and HULL, a 0 would trip the tautology filter (`-0 == 0`), so the clause would be dropped (sound).
- In SB, a 0 would trip the "contradictory SB units" assertion, so generation would fail.
- GP excludes zero terms explicitly.

## 2. Derivations: re-derived, all correct

These are my own derivations, not read off the proof:

- half-turn det +1 and fixing c;
- centre identity χ(c,p,q) = χ(hp,p,q);
- zero triples exactly {c,p,hp} (general position);
- the type-A/B classes, with the 8-entry sign table checked by hand;
- GP fast-path clause semantics (all 16 equal-sign patterns, nothing else);
- generic path (at most one zero term ever occurs: checked by case analysis on x = Z, Z ∈ y, Z ∉ F);
- A4 via Cramer/first-coordinate identity;
- CONV4: kept patterns are exactly the 6 convex ones. Confirmed exhaustively from real 4-point sets: n_in = 0/1/4 for
  6 convex / 8 one-inside / 2 non-realizable patterns (`logs/conv4stats.log`);
- Lemma 7;
- HULL semantics, and the 32 tautologies (triangles {X₁, X₂ₒ, X₂ₒ₊₁}, class signs −s, s, −s);
- SB units fixing exactly the 136 type-B variables;
- union-find invariant including path compression.

Normal form: for every hull vertex p₀ the labelling exists and is unique. (N2)–(N4) make no demand on X₀, and
representatives have distinct angles in (0, π) by Lemma 3. HULL holds because X₀ is a hull vertex. The argument is
correct.

## 3. Tests: re-runs, additional mutants, independent evaluators

1. **Re-runs.** I ran a private copy of the harness, with only its CADICAL and results paths patched, in `work/`
   (not kept).
   - Mutants re-run: `original`, `identity_sign`, `hull_anchor`, `conv4_pattern`.
   - Output sections are byte-identical to `tests/logs/mutation.log` (`logs/mutation_rerun_authors.log`).
   - `classes.py` on the real base map: PASSED. `identities.py`: all identities and controls behave.
2. **Additional mutants.** The nine mutants are in `scripts/refmutants.py`; the run is in
   `logs/mutation_new_mutants.log`. They target code paths the authors' 12 mutants did not touch.
   - Caught in every instance (all labellings violate, all two-way tests UNSAT, spec flags):
     - `gp_generic_polarity` (GP clauses on 5-sets containing c);
     - `gp_fast_sign` (one sign in one fast-path clause);
     - `hull_orient` (χ(a,d,X₀) for χ(d,a,X₀));
     - `a4_sign_Z` (wrong A4 sign on 4-sets containing c only).
   - Rejected by the encoder's own checks: `parity` (assertion in `convex4_patterns`) and `identity_sign_p0` (contradictory
     identification).
   - `uf_compress` (path-compression sign bug) is an **equivalent mutant**:
     - union-find paths never exceed length 2 for t = 4..9 and t = 17, and the maps are identical (`logs/ufdepth.log`);
     - so the compression loop never rewrites an interior node, and that branch is dead code here.
   - Sound controls:
     - `ctl_hull_X1` writes the identical clause multiset (h-symmetry), so the spec comparison passes;
     - `ctl_hull_withZ` (c allowed as a triangle vertex) is flagged by the spec comparison only. The semantic tests
       report 0 violations and all SAT, as they should.
3. **Independent small-size evaluator** (`scripts/refeval.py`). It shares no code with `tests/`: own labelling, own
   convexity test, own expected-violation derivation by clause identity.
   - The original passes at 8 size/option combinations (t = 4..8, K = 5..7, with and without `--hull`), 383 labellings
     in total, including non-hull controls.
   - 7/7 unsound mutants FAIL. The 3 sound controls or equivalent mutants PASS (`logs/refeval.log`).
4. **Independent full-base evaluator** (`scripts/refbase.py`). It runs on the certified base `b0061e90…`, streamed in
   32 MB chunks; 33 s, 1.17 GB peak. There are 9 labellings over 3 configurations:
   - sym32 + a near pair with 1 canonical convex 7-set, labelled from all 4 hull vertices plus 1 non-hull control;
   - sym32 + a near pair with 6, 1 + 1 labellings;
   - a random configuration with a 10-vertex hull, 1 + 1 labellings.

   The violated-clause multiset equals the prediction exactly in every case: 1 clause of 16,653,336; 6; 129,584; and,
   for the non-hull controls, the KGON clauses plus the HULL clauses of exactly the triangles containing p₀ (136, 141,
   130,292). See `logs/refbase.log`.

Limitation (inherent, not a defect): defects that bite only on some geometries are caught per instance, not per
labelling. Examples are `hull_anchor` (62/90 labellings) and `conv4_pattern`. The weakening mutants (A4 or GP missing)
are sound and are flagged only by the spec comparison, as the proof says.

## 4. perturbation.md and class_table.md

- **perturbation.md: correct.**
  - (P1)–(P3) and the Corollary re-derive. The formula orient(c,x′,y′) = |p_j||p_l| sin(·) was checked.
  - Odd m excludes same-orbit collinearity.
  - The illustration script does what it claims: exact Eisenstein arithmetic, with det √3/2 > 0.
  - The fivefold description matches the `symcnf.py` docstring: auxiliary centre for odd m, centre facts, sector units.
- **class_table.md: claims verified.**
  - 9 encoder hashes match the worktree.
  - All 13 cited CNF and proof hash prefixes and all 6 CNF header sizes appear in the repository records.
  - The Lean file sha is `6d5ec90a…252a6e38`. Its five class statements match the rows' hypotheses (|S|, general
    position, invariance, c ∉ S, axis-point condition), and the axioms output
    (`SYMLEAN/logs/SymmetricReductionAxioms.out`) lists only `[propext, Classical.choice, Quot.sound]`.
  - The 4,616 cubes use only triple variables: 613,496 literals, max |lit| 2,856, no zeros.
  - C2FINAL §3 records 2,589/2,589 unit-CNF hashes rebuilt as "base + n extra clauses". This is what makes Theorem 1
    applicable to each recorded unit; I did not re-check it.

## 5. Findings

| # | severity | finding |
|---|---|---|
| R1 | minor | **Relative covers not stated.** Corollary 3 treats only covers of the whole base. The central-34 chain also uses second-layer covers *inside* a hull cube. `C2C34/p8/mkunits.py` writes base + P_a hull-cube units + one clause ¬(L_i ∖ Q) per subcase, and class_table.md cites Corollary 3 for that step. The relative statement (if base ∧ Q ∧ ⋀ᵢ¬Lᵢ is UNSAT, every (S,p₀) in class(Q) lies in some class(Q ∧ Lᵢ)) follows in one line from Theorem 1. The remark that dropping Q's literals from each ¬Lᵢ is equivalent under the Q units should be added too. Soundness is not affected. |
| R2 | note | §8.3 says the non-hull controls violate "exactly the predicted HULL clauses", but `run_base.py` compares only the **number** of violated HULL clauses with the number of triangles containing p₀. My `refbase.py` checked clause identity on 3 controls of the full base, and they match. The wording should be fixed or this check cited. |
| R3 | note | Lemma 8's reason ("by the barycentric identity") is incomplete. The identity gives the sum, not equal signs. Equal signs come from positivity of the barycentric coordinates (Cramer: D(b,c,d)/D(a,b,c), …). perturbation.md (P2) reuses this wording for an "iff". The conclusions are correct. |
| R4 | note | spec.py establishes **coverage**: the proof's family descriptions equal the CNF exactly. For the GP generic path and A4 it mirrors the encoder's enumeration, so it is not an independent derivation. Correctness rests on Props 7–11 and the semantic tests. |
| R5 | note | Union-find path compression never rewrites an interior node at these sizes (max path length 2), so a bug there would be invisible to every test. Lemma 5 covers the branch anyway, and the base map is independently validated by classes.py (partition and signs). |
| R6 | note | Small slips. Lemma 4 says "at least 3 vertices … even", meaning at least 4. The §2 parenthetical about the short-circuit protecting `tau(Z)` is moot: is_zero never passes Z to tau. Both are harmless. |
| R7 | note | §1 identifies Lean `GeneralPosition` (Mathlib `Collinear`) and `ConvexPosition` (`ConvexIndependent`) with the orientation notions informally. This is acceptable, since certificates ⇒ HalfTurn34 is declared not Lean-checked. |
| R8 | note | class_table.md: "8 × 287 orbit representatives closed by 2,385 UNSAT records" is consistent with C2FINAL (2,385 UNSAT of 2,492 records, several per orbit, 287 closed per case). It could be misread as a count identity (8·287 + 8 = 2,304). The cover citation inherits R1. |

## 6. Reproduce (from `C2ENC/referee`)

```sh
python3 -I scripts/conv4stats.py
python3 -I scripts/refeval.py ../tests/zcnf_orig.py 5 6 --hull --seed 3 --ncfg 8     # etc., see logs/refeval.log
python3 -I scripts/run_refmut.py original identity_sign hull_anchor conv4_pattern
python3 -I scripts/run_refmut.py uf_compress gp_generic_polarity gp_fast_sign hull_orient parity \
     identity_sign_p0 a4_sign_Z ctl_hull_X1 ctl_hull_withZ
python3 -I scripts/ufdepth.py ../tests/zcnf_orig.py ../tests/mut/uf_compress/zcnf_mut.py
python3 -I scripts/refbase.py BASE.cnf BASE.json ../../SYM2/sym7_32points.txt     # needs numpy
```

The runs used `work/`, a private copy of `tests/` (mutate.py differed only in the CADICAL and results paths; `evalcnf`
was rebuilt from the audited source). Here `scripts/run_refmut.py` runs the harness in `../tests` directly, with
CaDiCaL taken from `$CADICAL`, and writes to `../tests/mut` and `../tests/logs`; the mutant encoders that `refeval.py`
and `ufdepth.py` read are written there. `BASE.cnf` and `BASE.json` are the base CNF and its map (`../proof.md` §0).
Nothing outside `referee/` was modified: the authors' `SHA256SUMS.txt` still verified 29/29 after the runs.
