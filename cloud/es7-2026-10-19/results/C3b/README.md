# Task C3b: an independent compact encoding for the 3-fold class (33 points, no convex 7-gon)

Nothing here is a theorem. "UNSAT" means UNSAT of one specific CNF. The encoding is tested,
not formally verified. "Certified" means CaDiCaL's LRAT proof was accepted by both
drat-trim `lrat-check` with the E2 empty-clause patch (`results/E2/tools/lrat-check-E2.patch`)
and the CakeML-verified `cake_lpr`.

## Result in one paragraph

**m = 11, k = 7 (33 points, C3, centre not in the set) is NOT closed.**
- The CNF has 135,663 variables and 4,149,465 clauses, sha256 `2d1df312…`.
- CaDiCaL ran 20 minutes: UNKNOWN (282k conflicts).
- march_cu split it into 64 cubes, all on the σ bits. Coverage weight is exactly 1, and no
  leaf was refuted by march.
- 4 of the 64 cubes ran 300 s each: all UNKNOWN.
- 5 fully σ-fixed leaves (depth 10) ran without proofs: 2 at 2,400 s and 3 at 1,800 s.
  All UNKNOWN, at 0.9–1.3M conflicts each.
- Closed and LRAT-certified weight: **0**.

What did pass:
- the exact identity checks;
- 1,188 + 30 random-set validations with 0 failures;
- all controls;
- full agreement with `symcnf.py` (main) and with C3a, at the level of SAT/UNSAT and also
  at the level of individual models.

The optional D3 check (`--d3`) reproduces results/E: **D3, 33 points, k = 7 is UNSAT**, in
174 s, with a 490 MB proof that **both checkers accept**.

No m = 11 model was found, so there is nothing to realize.

## What ran where

- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Wall time about 4 h from
  02:53 UTC.
- Tools built from source:
  - CaDiCaL 3.0.1 (git c607304);
  - drat-trim / lrat-check (git 2e3b2dc) with E2's patch;
  - cake_lpr (git a36874a);
  - march_cu from marijnheule/CnC (git 705b60c).
- march_cu needed two build fixes:
  - add `-fcommon` to CFLAGS (modern gcc);
  - in `march_cu/microsat.c`, change `S->mem_max = 10000000` to `400000000`. Without it,
    march_cu segfaults on every CNF with m ≥ 9. AddressSanitizer shows a use-after-free:
    `getMemory` reallocates the clause DB while callers still hold pointers into it. With the
    larger initial DB the realloc never happens; the ASan build ran clean on m = 9.
  - C3a found the same bug independently.
- The patched lrat-check rejects the hintless-empty-clause proof that unpatched lrat-check
  accepts. cake_lpr rejects it too.

## The encoding (`tools/gen_c3b.py`, generator commit 3aac870)

The setup and identities are as in the task. The proofs are written out in
`DERIVATION.md`; the first two checks below re-verify them exactly.

**Variables (m = 11)**
- X = chi' per R-orbit of triples: 1,826. The signs follow e_i e_j e_k and the permutation
  parity.
- Y = chi_S per R-orbit: 1,826.
- s_0..s_10, with s_{r+m} = ¬s_r and s_{r+2m} = s_r.
- inv_ij: 528.
- o_ij = "i precedes j in the x-order of S": 528.
- Chain variables C^l_p(q,r), 2 ≤ l ≤ k−2, for every ordered (p, q, r): 33·32·31·4 = 130,944.

**Clauses**

| group | count (m=11,k=7) | content |
|---|---|---|
| SIG | 109,120 | chi' is a signotope. Every 4-tuple a<b<c<d is monotone; written for all 4-tuples and deduplicated after the orbit substitution. |
| ACY | 27,280 | chi_S is acyclic: each 4-set excludes its 2 totally cyclic patterns. The patterns are derived by sampling real 4-point sets, not hard-coded. |
| XOR | 29,150 | Y = X ⊕ s_i ⊕ s_j ⊕ s_k (per orbit) and o = inv ⊕ s_i ⊕ s_j. |
| INV | 22,858 | The prefix rule per triple, and inv forced by opposite s. |
| SB | 1 | ¬s_0 (point reflection). |
| KGON | 3,961,056 | The convex-chain encoding below. |

**No convex k-gon (KGON).**
- p ranges over all 33 points, as the candidate leftmost vertex of the polygon in S's x-order
  (literal `right(p,q)` = o or ¬o).
- C²_p(q,r) ← right(p,q) ∧ right(p,r) ∧ chi_S(p,q,r).
- C^{l+1}_p(q,r) ← C^l_p(o,q) ∧ chi_S(o,q,r) ∧ chi_S(p,q,r) ∧ right(p,r).
- A final clause forbids extending C^{k−2}, i.e. a chain of k−1 points.
- Exactness on real sets: a chain of points right of p that increases in slope about p, with
  left turns, is exactly the vertex sequence of a convex polygon with leftmost vertex p.
  The implications are upward only, so soundness only needs one direction.

**Comparison with C3a's encodings**
- After my validation passed I read C3a. C3a's default (`--gon chain`) is the same
  leftmost-vertex chain idea, so the two k-gon layers are independent implementations of one
  idea, not two ideas.
- C3a's `--gon conv` variant (layered Carathéodory) is the genuinely different encoding. It
  agrees too (below).
- Differences from C3a's chain CNF:
  - C3b adds 4-point acyclicity of chi_S;
  - C3b has no separate Y/W split;
  - C3b uses an all-ordered-pairs chain table;
  - sizes: C3b 135,663 vars / 4,149,465 clauses, C3a 168,399 / 4,154,921.

**Optional `--d3`.**
- Choose the gap containing l so that the axis point gets label 16. That gap contains the
  perpendicular to the axis, so in labels the mirror is i → 32 − i, with s preserved and
  chi_S and chi' reversed.
- inv and o are not constrained by the mirror, since they depend on where l sits in the gap.
- Size: 135,663 vars, 4,171,125 clauses.

## Validation (all passed; nothing failed, so nothing was stopped)

1. **Exact identities in Q(√3)** (`tools/identities.py`, `logs/identities_q3.log`).
   - 300 random Euclidean C3 sets, m = 3..11, with points a + bω in exact Q(√3) Cartesian
     coordinates. Each set gets a random exact rotation: a Pythagorean angle times a multiple
     of 30°. l is the true y-axis.
   - Checked: R(i) = i − m, chi_S = chi'(−1)^Σσ, chi'(R·) = chi'·εεε, σ_{Ri} = σ_i ⊕ [i ≥ m],
     the x-order rule, the prefix rule, the forced inv, the centre facts, and the
     point-reflection normal form.
   - **0 failures.**
2. **Clause-level validation** (`tools/validate.py`, C evaluator `tools/cnfeval.c`;
   `logs/validate_s13..s16.jsonl`, `logs/validate_s17_k9.jsonl`).
   - Random exact C3 sets: Eisenstein lattice orbits, then a random integer linear map with
     det > 0 that puts a random line through c on the y-axis.
   - Every primary variable is computed **from the coordinates directly**: labels, s, chi'
     from phi(S), chi_S, inv, o. It is not computed from the identities.
   - Chain variables take their least model under unit propagation. Then every clause is
     evaluated.
   - Required: no orbit-map conflict; all non-k-gon clauses true; and the k-gon clauses all
     true **iff** a DFS over convex subsets (Carathéodory test, exact orientations) finds no
     convex k-set.
   - Coverage: **1,188 samples** with m = 3..11 (132 per m) and k = 5..8, plus 30 samples at
     m = 7..9, k = 9. **0 failures.**
   - 100 of the samples are k-gon-free (m = 3: 56, m = 4: 31, m = 5: 10, m = 6: 3); none at
     m ≥ 7.
   - **Limitation:** the "no k-gon ⇒ clauses satisfiable" direction is exercised only for
     m ≤ 6. My sampler never produced k-gon-free sets at larger m; C3a's radial-strip sampler
     did.
   - At larger m that direction is covered only by the model cross-checks below: C3a's
     m = 8, 9, 10 models satisfy this CNF.
   - Two earlier validator runs (seeds 11, 12, 600 samples each) died without writing their
     buffered logs. They are not counted. Both were at sample > 550 with 0 failures when last
     inspected.
3. **Mutation test** (`tools/mutation.py`, `logs/mutation.log`). All 4 planted bugs are
   detected:
   - flipped chi' in the prefix rule: 60/60 samples fail;
   - wrong s parity: 60/60;
   - left-turn literal dropped: 7 samples fail;
   - "right of p" literal dropped: 7 samples fail.
4. **Controls that must be UNSAT, certified** (`logs/certified_controls.jsonl`):
   - m = 3, k = 5 (9 points): UNSAT, both checkers accept;
   - m = 6, k = 6 (18 points): UNSAT, both accept. Also closed as 8 march cubes, each leaf
     dual-checked, coverage weight 1 (`logs/cnc_test_m6k6.jsonl`);
   - m = 5, k = 6 (15 points): UNSAT, both accept. This matches results/E's n15k6m3.
5. **Agreement with `symcnf.py` (origin/main, `symcnf.py 3m k 3`)**
   (`logs/compare_symcnf.jsonl`).
   - m = 3..6 × k = 5, 6, 7, plus m = 7, 8 with k = 7: **14/14 agree**.
   - UNSAT: k = 5 for all m, and k = 6 for m = 5, 6. Everything else is SAT. There were no
     disagreements to investigate.
6. **Decoded SAT models** (`tools/modelcheck.py`, which is independent of the clauses).
   - Checked: R-symmetry, the identities, chi' signotope on all 4-tuples, the prefix and
     forced inv, 3-term Grassmann–Plücker for chi_S on every 5-set, acyclicity, and a DFS
     for the largest convex subset.
   - All 8 models pass (m = 3..8, `logs/cmp_models/`). Their largest convex subset is 5 or 6,
     always < k.
   - These are abstract signotopes. No realization was attempted, because no m = 11 model
     exists from this run.
7. **D3 reproduction of results/E** (`logs/d3_m11k7.txt`, `logs/certified_controls.jsonl`).
   - `gen_c3b.py 11 7 --d3` gives UNSAT in 174 s (30,812 conflicts), with a 490 MB LRAT
     proof. **lrat-check (patched) and cake_lpr both accept it.**
   - Small D3 cases agree with E:
     - n = 9: k = 5, 6 UNSAT, k = 7 SAT;
     - n = 15, 21, 27: k = 5, 6 UNSAT;
     - n = 21 and 27, k = 7: SAT.

## Agreement with C3a (read after step 3 passed)

- **SAT/UNSAT** (`logs/compare_c3a.jsonl`): m = 3..7 × k = 5, 6, 7. C3b, C3a-chain and
  C3a-conv agree in **15/15** cases. C3a's own `compare_c3b.jsonl` reports 21/21.
- **Model level, C3a → C3b** (`tools/eval_foreign.py`, `logs/c3a_models_in_c3b.jsonl`).
  - All 11 decoded C3a models (m = 2..10, including both m = 10, k = 7 models) were mapped
    to C3b variables: chi' and σ directly, chi_S and o derived.
  - Each one satisfies every C3b clause, including C3b's acyclicity clauses, which C3a does
    not encode.
  - So C3b is SAT at m = 10, k = 7 (30 points), though I did not solve that instance myself.
- **Model level, C3b → C3a** (`tools/c3b_model_in_c3a.py`, `logs/c3b_models_in_c3a.jsonl`).
  - All 8 C3b models (m = 3..8) were fixed on C3a's base variables (chi', σ, inv).
  - Each extends to a model of C3a's chain CNF.
- **Controls:** the same answers (m3k5 UNSAT, m6k6 UNSAT), both certified by both runs.
- **Cubes:** C3a's march cubes are on its own CNFs, with variable numbers that differ from
  C3b's. Both runs split on the σ bits first, and both have fully σ-fixed leaves open:
  - C3a: two leaves UNKNOWN at 3,600 s;
  - C3b: see below.
  - No leaf is closed in either run on the full m = 11 instance, so there are no closed
    cubes to map.

## m = 11, k = 7 runs

All on CNF sha256 `2d1df312934939e4bc0d6ec6b862ff3b911e7112a9c6c5619b8abd3ec8bc4ee3`
(`python3 tools/gen_c3b.py 11 7 -o c3b_m11k7.cnf`; regenerated at the end with the same
hash).

- **Plain CaDiCaL, 20-minute cap** (`logs/cadical20_m11k7.log`): UNKNOWN, 282,013
  conflicts, about 238 conflicts/s.
- **march_cu** (`logs/march_d6.tail.log`).
  - Depth 10 was abandoned: no progress tick in 30 CPU-minutes, about 30 s per node.
  - `march_cu c3b_m11k7.cnf -d 6 -o cubes_d6.icnf` produced 64 cubes in 35.6 min, with 0
    refuted leaves. Cube file sha256
    `06d9384438c55a7c729bbd7012ec277b4406bdd7071c8f8052acd15139e8445e` (`logs/cubes_d6.icnf`).
  - `tools/coverage.py` confirms the cubes form a binary tree with total weight exactly 1.
  - Every cube literal is a σ bit (vars 3654..3663 = s_1..s_10), so the cubes are partial
    σ patterns.
- **Cube solving** (`tools/cnc_run.py`). Each cube is solved as CNF + units with
  `cadical --lrat --binary=false -t T`, then both checkers run.
  - Cubes 0–3 at T = 300 s: all UNKNOWN (`logs/cnc_d6_probe300.jsonl`).
  - Fully σ-fixed leaves (`logs/leaves_d10.icnf`, which extends d6 cubes 0, 21, 42, 63 and 10
    with seeded random σ bits) were timed with `tools/probe_leaf.sh` (plain CaDiCaL, no
    proof; `logs/probe_leaves_d10.jsonl`). Leaves 0 and 1 ran 2,400 s; leaves 2, 3 and 4 ran
    1,800 s. **All UNKNOWN**, with 1,280,633, 1,205,891, 923,946, 986,494 and 922,700
    conflicts.
  - Sub-cubing σ-leaf 0 with `march_cu -d 5` reached only 16/64 progress in 44 min, about
    5 min per lookahead node, and was aborted (`logs/march_leaf0_d5_aborted.log`).
- **Closed weight: 0 / 1. LRAT coverage of the instance: none.**

**Timing estimate.**
- No leaf finished, so there is no real estimate. 5 of the 1,024 σ-leaves were timed and
  none closed within 1,800–2,400 s.
- If those 5 are typical, plain CaDiCaL needs more than about 1,024 × 2,000 s ≈ 570
  core-hours. That is only an extrapolated lower bound; the true cost is unknown and
  probably much larger.
- On this 4-core VM within the 4-hour budget, the instance was not closable.

## Shard plan

`shard_plan.md` records the deterministic inputs: generator commit 3aac870, CNF sha256,
patched march_cu command, cube-file sha256, 64 cubes, and per-cube times.

**It is not a ready plan to close the instance.** Closability is not established for this
encoding. C3a's conv-variant plan, whose deep sub-leaves do close, is the better route.

## Files

- `tools/gen_c3b.py`: the generator (`--d3` adds the mirror).
- `tools/identities.py`: the exact Q(√3) identity check.
- `tools/validate.py` and `tools/cnfeval.c`: random-set clause validation.
- `tools/mutation.py`: the mutation test.
- `tools/modelcheck.py`: independent model decoder and checker.
- `tools/compare_symcnf.sh`: the symcnf comparison.
- `tools/eval_foreign.py` and `tools/c3b_model_in_c3a.py`: the model-level cross-checks with
  C3a.
- `tools/cnc_run.py`: cube solving with LRAT and both checkers.
- `tools/coverage.py`: cube-tree and closed-weight check.
- `tools/probe_leaf.sh`: proof-free timing probe of one cube.
- `DERIVATION.md`: proofs of the identities and of the encoding's soundness.
- `logs/`: everything cited above. No CNF or proof files are committed.
