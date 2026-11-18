# VERIFY_LO: independent adversarial check of LO33N20261113 (phase 2, 13 November 2026, 20:51–21:15 KST)

**Overall verdict: confirmed with corrections.** Every mathematical claim assigned to this check holds up
under my own checks. I found no refutation, no off-by-one error, no inequality pointing the wrong way, no
uncertified extra row and no incomplete case split. The corrections concern naming, one mislabelled field in the
archived verifier outputs, and archiving (§4).

Scope: Lemma S (§2) and its proof, Lemma S.2 (h(F) ≥ 18), the exact trees for slices 18 and 19 (with the
certified coupled rows and over the Lean rows alone), and the conclusion "N66 ≤ 56 ⇒ ES(8) ≤ 309". The
slice-20 claims (headline (ii)), RES33N Result 3 (slices t ≥ 25), the bounds N5 ≤ 65 and N66 ≤ 59, and the
geometric soundness of RES33N's coupled-row encoder were **not** checked here.

Method:
- Verifier scratch directory (not in Git): `/home/jay/research/data/verify-LO-20261113` (abbreviated V). All
  scripts in V are mine. I did not use any of the record's checkers as evidence: `verify_cert.py`,
  `verify_stream.py`, `check_f18.py` and `lo_common.py`.
- The only shared code I ran is `scripts/omission_tree.check_tree`, the trusted replay. I read it first (§2.1).
  I also used RES33N's encoder `coupled.py`, through a copy in V/enc, to regenerate the CNFs.
- Units: `nov13c-vfy-LO-r19`, `-recert`, `-real57`, `-real2`, `-real3`, `-rep19`. Each ran one at a time on
  1 thread with MemoryMax ≤ 1.5 GB, and each started only after `cpu_free.sh` reported at least 1 free thread.
  The peak was 835 MB, in `-recert`.
- Nothing was written in the work directory W = `/home/jay/research/data/lo33-20261113`. W was only read.
- In the repository, only this file was written. No git command was run.

## 1. Verdict per claim

| claim | verdict | evidence (§) |
|---|---|---|
| Lemma S (§2) and its proof (items 1–4, both directions of 4) | **confirmed** | 2.2, 2.3 |
| S.1 is `Excludes2650Zero 32`, i.e. Σh ≥ 33 for 0/1 vectors with h₀ = 0 and the 2,650 rows | **confirmed**; name imprecise (§4.1) | 2.3 |
| S.2: h(F) ≥ 18 from rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315 | **confirmed** (own exact recount) | 2.4 |
| F, Lo = states with f₁ ≥ 5, f₁ ≤ 4 in the indexing of `source-2650.json.gz`; that indexing and those rows are Lean's | **confirmed** | 2.5 |
| Lemma A (THEORY310N §2) gives h(Lo) ≥ 70 − N66 (and h(F) ≥ 84 − N5) | **confirmed** (proof read; f₁ checked against the Lean definitions) | 2.6 |
| Slice 18, certified rows: 3,611 nodes, 1,806 leaves, min margin 1, 26 certified rows used | **confirmed** | 3.1 |
| Slice 18, Lean rows alone: 3,815 nodes, 1,908 leaves, 110 contexts, min margin 1, only h(Lo) ≥ 15 used besides Lean rows | **confirmed** | 3.1 |
| Slice 19, certified rows: 167,509 nodes, 83,755 leaves, 502 contexts, min margin 1, 130 certified rows used | **confirmed** (piecewise, from the archived contexts) | 3.2 |
| Slice 19, Lean rows alone: 186,077 nodes, 93,039 leaves, 980 contexts, min margin 1 | **confirmed** | 3.2 |
| Slice 19, Lean rows, repaired tree: 172,401 nodes, 86,201 leaves, min margin 1 | **confirmed** | 3.2 |
| Capacity rows exactly (F, 84 − c), (Lo, 70 − c2); every other extra row has a cake_lpr verdict | **confirmed**; the 130 coupled rows actually used were also re-certified from scratch | 3.3 |
| "N66 ≤ 56 ⇒ ES(8) ≤ 309" over the Lean rows alone | **confirmed** as an EXACT TREE + PROVED conditional (trees not Lean-checked) | 2.7 |
| "N66 ≤ 56 ⇒ ES(8) ≤ 309" with the coupled rows | **confirmed modulo the validity of the coupled rows** (RES33N encoder, not examined); the statement itself also follows from the Lean-rows version | 2.7, 3.3 |
| Composition 187 + 120 + 2 = 309 | **confirmed** | 2.7 |
| Lean-row / certified-row validity and Lemma A on real point sets | **no counterexample** in 7,826 real residual configurations (HEURISTIC) | 3.4 |
| Novelty | the record claims none ("No new bound on ES(8) is claimed"); consistent with NOVELTY20261113B §3 (C2, C8: "partially anticipated") | 2.8 |

## 2. Lemma S, its inputs, and the composition

### 2.1 The replay checker is sound (read line by line)

`scripts/omission_tree.check_tree` (107 lines) does the following:
- It checks that the tree is a binary tree in which every node is reachable, no node is repeated, and no state
  is branched on twice along a path.
- For each weighted leaf with missing set M and occupied set O, it computes the margin
  Σ_r w_r·max(0, d_r − |S_r ∩ M|) − C·(B − |M|) − Σ_{i free} max(0, load_i − C), in Python integers.
  The leaf is accepted only if this margin is positive.

Why this suffices: for any 0/1 vector extending the context with Σh ≤ B,

    Σ_r w_r·max(0, d_r − |S_r∩M|) ≤ Σ_{i free} load_i·h_i ≤ C·(B − |M|) + Σ_free max(0, load_i − C).

So a positive margin excludes every such vector. An over-budget leaf needs |M| > B. A pending leaf is only
counted, so each verifier must check where the pending leaves are; mine does (§3).

### 2.2 Lemma S, items 3 and 4 (PROVED; checked)

F ∪ Lo is a partition of the 154 states (84 + 70). Item 3 follows at once.

Item 4, (⇐). Take h with h₀ = 0, the rows (with or without the coupled rows), h(F) ≥ 84 − c, h(Lo) ≥ 70 − c2
and Σh ≤ 33.
- S.1 gives Σh = 33.
- Put t = h(F). Then t ≥ max(18, 84 − c), using S.2.
- h(Lo) = 33 − t ≥ 70 − c2, so t ≤ c2 − 37.
- So h is a ≤ 33-hole vector of slice t, which a closed slice excludes. This needs the slice tree to be over
  the same row system, which holds for both the Lean-only version and the certified-rows version.

Item 4, (⇒). Immediate.

Trivial pairs: c + c2 ≤ 120 gives 84 − c > c2 − 37. Directly, h(F) + h(Lo) ≥ 154 − (c + c2) ≥ 34. I
re-derived every cell of the §4b table from the range max(18, 84 − c) ≤ t ≤ c2 − 37: all correct. So are the
"trivial thresholds" N66 ≤ 54 (c = 66) and N66 ≤ 55 (c = 65).

### 2.3 S.1 is the Lean statement claimed

`experiments/omission-final313-2026-10-11/Final313/Final.lean`, line 16:
`theorem residual_excludes_2650_zero : OmissionResidual32Bridge2650.Excludes2650Zero 32`.
- Its full name is `ErdosSzekeres.Omission.residual_excludes_2650_zero`.
- `Excludes2650Zero` is defined in `Residual32Bridge2650/Rows.lean`, lines 98–100:
  `¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧ (∀ r, demand2650 r ≤ ∑ i ∈ support2650 r,
  holes i) ∧ (∑ i, holes i) ≤ 32`.
- So every 0/1 vector with h₀ = 0 satisfying the 2,650 rows has Σh ≥ 33. This is exactly S.1.
- `forces_convex_octagon_313` is built on this theorem, and its audit (`final-audit.out`) is
  [propext, Classical.choice, Quot.sound].
- `Final310Compact` uses `E310.residual_excludes_32`, a separate proof of the same proposition.

### 2.4 S.2 (own script V/f18check.py, exact)

Output, abridged:

```
973  len 28 distinct 28 demand 6 inside F True f1 values [(6, 28)]
1165 len 28 distinct 28 demand 6 inside F True f1 values [(5, 21), (6, 7)]
... (1167, 1171, 1175, 1179, 1183, 1186, 2315 identical in shape)
coverage multiset over F: Counter({3: 84}) states outside F covered: []
sum demands 54
```

So Σ over the nine rows of h(S_r) = 3·h(F) ≥ 54, which gives h(F) ≥ 18. All nine are Lean rows (index < 2650),
and `all_rows_2650` proves them valid. Row 973 is exactly the 28 states with f₁ = 6.

### 2.5 Indexing: JSON = Lean (own scripts V/leancat.py and an inline check)

- **Rows.** I parsed the 21 arrays `rows0 … rows2560` of `Residual32Bridge2650/Catalog.lean`, where
  `support2650 r = (rowChunks[r/128])[r%128].1`. These are 2,650 rows, identical in order to
  `constraints[r]` of `source-2650.json.gz`.
  - Decompressed SHA-256 of the JSON: `e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6`.
  - Output: `json rows 2650 identical in order: True mismatches: 0`.
- **States.** `ResidualCatalog.catalog` (`ErdosSzekeres/Omission/ResidualCatalogData.lean`) is identical in
  order to the JSON `states` list. Output: `lean catalog 154 json states 154 identical order: True`.
  - The owner map is `ownerIndex v = catalog.idxOf (stateList (state v) ++ [0])`.
  - `catalog[i][0]` is column 1, i.e. f₁.
  - Hence F = {i : states[i][0] ≥ 5} (84 states) and Lo = {i : states[i][0] ≤ 4} (70 states) are the
    intended Lean sets.
  - State 0 is [0,0,0,0,0].

### 2.6 Lemma A gives h(Lo) ≥ 70 − N66

The proof in THEORY310N §2 was read. It was checked against the Lean definitions:

    column v i = sup_{u<v} [labels(u,v).2 if i+1 ≤ labels(u,v).1 else 0]      (ResidualStates.lean)
    labels(u,v) = (6 − rank_cap(u,v), rank_cup(u,v) − 1)                    (ResidualRanks.lean)

Here `rank cup true u v` is the longest `EndingPath` cup ending with (u, v). By `label_bounds`, labels.1 ≥ 1,
so f₁(v) = (longest cup ending at v) − 1. Hence f₁(v) ≥ 5 exactly when a 6-cup of R ends at v; call this set R₆.

- **(i)** A 5-cap inside R₆ starts at a point that ends a 6-cup. That is a junction, which
  `ResidualRanks.NoJunction` forbids (`EndingPath true t u 6 ∧ StartingPath false u v 5`).
- **(ii)** A 6-cup inside R \ R₆ ends at a point of R₆, which is a contradiction.
- R \ R₆ also has no 6-cap and no octagon (inherited from R). It has distinct x and no three collinear
  (`Configuration.xOrder`, `generalPosition`).
- So |O ∩ Lo| = |R \ R₆| ≤ N66, because the owner map is injective (`residualOwner_injective`).
- Hence h(Lo) ≥ 70 − N66, and in the same way h(F) ≥ 84 − N5.

My own state computation on real sets reproduces f₁ = (longest cup ending at v) − 1 at every point (§3.4).

### 2.7 The conclusion and the composition

Let c be a residual configuration with n ≥ 1 points. Its hole vector satisfies:
- h₀ = 0 (`zero_mem_residualOccupied`);
- the 2,650 rows (`all_rows_2650`);
- h(F) ≥ 18 (S.2);
- under N66 ≤ 56, h(Lo) ≥ 14 (Lemma A).

If Σh ≤ 33, then S.1 gives Σh = 33 and t = h(F) ∈ {18, 19}. Slices 18 and 19 are closed over the Lean rows
alone (§3), so Σh ≥ 34 and n = 154 − Σh ≤ 120. This is `ResidualBound 120`.

`ErdosSzekeres/Omission/PopulationBounds.lean` proves `forces_of_population_bounds : BalancedBound B →
ResidualBound R → ForcesConvexNGon (B + R + 2) 8`, and `Final310Compact.balanced_population_187` gives B = 187.
So 187 + 120 + 2 = **309**.

No N5 bound is used. In the gluing, the F-rows h(F) ≥ 18 and h(F) ≥ 19 are slice rows: they hold because
t = h(F). The steps from the trees and Lemma A to `ResidualBound 120` are a written argument plus exact trees.
They are not Lean-checked, as the record says.

### 2.8 Novelty

The README claims no novelty and no new bound. NOVELTY20261113B §3 rates the analogous statements C2 and C8
"partially anticipated". Its §10 lists nothing that affects this record.

## 3. Tree replays and certificates

Replay script: V/myreplay.py, my own. It does the following:
1. Rebuilds the row list from `source-2650.json.gz` (SHA checked) followed by the extra-row file in file order.
2. Recomputes F and Lo from `states`.
3. Classifies every extra row: either its support equals F or Lo, or it has rhs 1 and its support carries
   `s VERIFIED UNSAT` in `data/certified.jsonl`. Anything else aborts.
4. Asserts that the capacity rows equal {(F, 84 − c), (Lo, 70 − c2)} as a multiset.
5. Replays with `check_tree`:
   - *mono*: requires the root to branch on state 0 with a pending "one" child, and exactly 1 pending leaf.
   - *split*: wraps the master under a new root on state 0 (zero → master, one → pending), and turns every
     context placeholder into a pending leaf, so that `check_tree` must report 1 + #contexts pending. It then
     computes each context's master path by its own traversal. It checks each context subtree with
     `check_tree` under a chain of branch nodes fixing exactly that path, whose siblings are pending; exactly
     len(path) pending leaves are required. All context ids 0..k−1 must appear exactly once.

### 3.1 Slice 18

Commands:

```
$PY V/myreplay.py mono  66 55 R/data/cert_66_55/extra_66_55.json R/data/cert_66_55/tree_66_55.json.gz R/data/certified.jsonl
$PY V/myreplay.py split 66 55 R/data/cert_66_55_leanrows/extra_66_55_leanrows.json V/s18lean R/data/certified.jsonl
```

Outputs:

```
mono  (66,55): capacity [F,18],[LO,15]; certified rows in file 578; replay nodes 3611 leaves 1806 pending 1
      minimum_margin 1; certified rows used 26; F>=18 used in 0 leaves, LO>=15 in 1798; Lean rows with weight 1307
split (66,55): extra rows 2; contexts 110; stored_path_mismatch 0; nodes 3815 leaves 1908 pending 1
      minimum_margin 1; F>=18 used in 0 leaves, LO>=15 in 1904; Lean rows with weight 1227
```

Hashes:
- `tree_66_55.json.gz` `a797f2b1…`; extra `e8fae02b…`.
- Lean-rows tar `contexts_66_55_leanrows.tar` `52fc93b1…` (the copies in data/ and W are identical).
- Lean-rows extra `1d6141af…`.
- With the record's own hash definition, the master hash is `3b522d53…` and the context digest `e5e8cb87…`,
  equal to `data/cert_66_55_leanrows/verify_stream.out`.

### 3.2 Slice 19 (unit `nov13c-vfy-LO-r19`, 20:56:39–20:56:58; `-rep19` at 21:08)

Inputs were extracted read-only from W:
- `cert_65_56_leanrows/contexts_65_56_leanrows.tar`, SHA `cabbdbdf…`;
- `cert_65_56/contexts_65_56.tar.xz`, SHA `49ccfcf5…`.

Outputs:

```
split (65,56) Lean rows: extra 23134b33…; contexts 980; nodes 186077 leaves 93039 pending 1 minimum_margin 1;
      F>=19 in 98 leaves, LO>=14 in 92647; Lean rows with weight 2384; 10.7 s
split (65,56) certified: extra a8ac05e5…; contexts 502; nodes 167509 leaves 83755 pending 1 minimum_margin 1;
      certified rows used 130; F>=19 in 69 leaves, LO>=14 in 83214; 8.6 s
split (65,56) repaired (W/bb_65_56_repaired, read in place): contexts 502; nodes 172401 leaves 86201 pending 1
      minimum_margin 1; F>=19 in 75 leaves, LO>=14 in 85681
```

Context paths: stored_path_mismatch = 0 everywhere. That is, each context file's own missing/occupied lists
equal the paths I computed.

With the record's hash definition, the master and context digests reproduce the archived `verify_stream.out`:
Lean rows `8d2d6f10…` / `7813df85…`, certified `35f70b1c…` / `322fa869…`. So the archives I replayed are
exactly the trees the record reports.

The monolithic `W/cert_65_56/tree_65_56.json.gz` was **not** replayed by me. It is 79 MB of JSON, which risks
the 1.5 GB budget. The claim does not need it.

### 3.3 Extra rows and cake_lpr verdicts (unit `nov13c-vfy-LO-recert`, 20:59:59–21:01:38)

Extra-row files:
- Lean-rows files: exactly two rows, (F, 18) and (Lo, 15) for slice 18, and (F, 19) and (Lo, 14) for slice 19.
- Certified files: two capacity rows plus 578 rhs-1 rows. All 578 supports carry `s VERIFIED UNSAT` in
  `data/certified.jsonl`.
  - That file has 589 lines and 578 distinct supports, all verified.
  - Its SHA-256 is `2f065615…`, identical to the copy in W.

The trees use 26 coupled rows (slice 18) and 130 (slice 19); the 26 are a subset of the 130. For each of the
130, V/recert.py did the following:
1. Regenerated the CNF from the support with RES33N's encoder `coupled.py`. Its diff against the LO33N copy is
   only the three work-directory paths, as the record says.
2. Compared the CNF's SHA-256 with `cnf_sha256` in the record.
3. Ran `/usr/bin/cadical` 2.1.3 with `-q --lrat=true --binary=false`.
4. Ran `cake_lpr --CML_HEAP_SIZE=700 --CML_STACK_SIZE=100`.

Result:

```
cnf match 130/130; cadical exit 20: 130/130; lrat SHA equal to record: 130/130; cake 's VERIFIED UNSAT': 130/130
```

So these 130 rows are CERTIFIED for the CNF that the encoder produces from each support. Whether that CNF is a
sound relaxation of real residual geometry (the coupled owner model of RES33N) was not examined. Those rows are
not Lean-checked.

### 3.4 Real point sets (units `-real57`, `-real2`, `-real3`; HEURISTIC)

Test objects:
- `theory310-20261113/residual57_points.json`: the 57-point residual part of witness 8.
- The residual parts of all 26 hull-root charts of the four octagon-free 64-point sets: witness8, ot0000,
  ot0001m, ot0002.
- 7,800 random subsets of these parts. The hypotheses are hereditary.

THEORY310N's `real_sets.py` was used only to generate the charts. Every hypothesis was re-checked by my code in
exact rationals: distinct x, no collinear triple, max cap ≤ 5, no junction, largest convex polygon ≤ 7. All 26
full parts pass.

My code then computed the labels, the columns, the catalog index and the hole vector.

| test | configs | Lean rows violated | certified rows violated | Lemma A failures | state 0 hole |
|---|---|---|---|---|---|
| 57-point residual part | 1 | 0 | 0 | 0 (R₆: 7 points, longest cap 2; R \ R₆: 50 points, longest cup 5) | no |
| 26 charts + 7,800 subsets | 7,826 | 0 | 0 | 0 | 0 |

The test had some bite:
- In 379 configurations at least one certified support had exactly one hole.
- In 2,726 configurations some Lean row was tight.

All real configurations have at least 97 holes, far from the 33/34 boundary. This is evidence, not proof.

## 4. Problems found (none affects the verdicts)

1. **Theorem name.** The README cites `Final313.residual_excludes_2650_zero`. The declared name is
   `ErdosSzekeres.Omission.residual_excludes_2650_zero`, in module `Final313.Final`.
   - It is "the residual half of ES(8) ≤ 310" only as a proposition.
   - `Final310Compact` uses `E310.residual_excludes_32`, which has the same type `Excludes2650Zero 32`.
2. **Mislabelled field in the archived verifier outputs.** In `data/cert_66_55/verify.out`,
   `data/cert_65_56/verify.out` and `data/cert_65_56/verify_stream.out`, `"certified_rows_used": 578` counts
   the rows present in the extra file, not the rows the tree uses. The tree uses 26 and 130. The README's
   prose numbers (26 and 130) are right.
3. **Archiving.** All slice-19 tree files exist only in W, not in the repository:
   - both context archives;
   - the monolithic tree;
   - the repaired tree.

   Headline (i) needs `cert_65_56_leanrows/contexts_65_56_leanrows.tar` (29 MB, SHA `cabbdbdf…`). If W is
   cleaned, headline (i) can no longer be replayed from the repository. §6 of the README says this, but the
   headline does not.
4. **Coupled-row validity is an inherited assumption.** I confirmed CNF = encoder(support) by SHA and the
   cake_lpr verdicts for the 130 rows used. I did not confirm that the encoder is a sound relaxation.
   - This affects only the "with coupled rows" variants.
   - The Lean-rows version of "N66 ≤ 56 ⇒ ES(8) ≤ 309" does not depend on it.
5. **Not verified here:** the monolithic slice-19 file `tree_65_56.json.gz`, the phase-1 replay timestamps
   (marked "inferred" in the README), slice 20, and RES33N Result 3 (t ≥ 25).

## 5. Files in V

- Scripts: `myreplay.py`, `run19.sh`, `f18check.py`, `leancat.py`, `usedrows.py`, `recert.py`,
  `realtest.py`, `realtest2.py`, `realtest3.py`.
- Outputs: `s19lean.out`, `s19cert.out`, `rep19.out`, `recert.jsonl`, `real57.out`, `realtest2.log`,
  `realtest3.log`, and the status JSON files.
- The extracted archives are in `s18lean/`, `s19lean/` and `s19cert/`.
