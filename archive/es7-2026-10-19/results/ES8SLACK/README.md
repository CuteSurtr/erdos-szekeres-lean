# ES8SLACK: where the slack is in the omission proof of ES(8) ≤ 311

Local computations on an Apple M5 Pro, 1 November 2026 (UTC), over the omission records on `es7-cloud` at
471d5f63a.

**Status.** Negative results and planning evidence. Nothing here improves ES(8) ≤ 311.
- Residual side: no slack. Over the present 2,650 rows with state 0 occupied, at least 33 holes are forced
  (Lean-checked in the repository record) and exactly 33 are attained (exact computation).
- Balanced side: over the present 3,131 rows the Boolean optimum lies between 64 and 72 holes.
- No argument that uses only the present catalogs, early-vertex occupancy and the composition can prove better
  than ES(8) ≤ 303.
- A capacity-21 lemma for residual block rows 973, 1165 and 1186 does not follow from the abstract conditions
  that were tested.
- The next unit (310) is projected at 1,100–1,300 CPU-h of search, 1,300–1,550 CPU-h of Lean and about 4 TB of
  compiled parts. This is an extrapolation (computational evidence, §7).

An independent review (§9) refuted no claim. It relabelled two claims (C1, C5), added a Lean check of a third
(C6), closed two gaps in the arguments (C8, C15) and corrected some details.

Written proofs are in `proofs.md`. Claim numbers C1–C17 refer to the table below and to the directories under
`review/`.

| Claim | Statement | Label |
|---|---|---|
| C1 | ES(8) ≤ 311 as 1 + 188 + 121 + 1 (§1) | Lean-checked in the repository record (not re-run here); certificate trees replayed by exact computation |
| C2 | 311 = 408 − 97 (§1) | Lean-checked (arithmetic, no axioms); exact computation |
| C3 | residual Boolean optimum with state 0 occupied is exactly 33 (§2) | exact computation (≤ 33); Lean-checked in the repository record (≥ 33) |
| C4 | balanced Boolean optimum in [64, 72] (§3) | exact computation (≤ 72); Lean-checked in the repository record (≥ 64) |
| C5 | ceiling ES(8) ≤ 303 for the present catalogs (§4) | exact computation plus written proof (reviewed) |
| C6 | early-vertex occupancy (§6) | Lean-checked |
| C7 | early-vertex constraints give no gain (§7) | computational evidence |
| C8 | symmetry group of the balanced base rows is {id, T, C, TC} (§6) | exact computation |
| C9 | LP values 54.17, 55.0, 27.0 (§3, §7) | computational evidence |
| C10 | no balanced vector below 72 holes found (§3) | computational evidence |
| C11 | projected cost of balanced budget 64 (§7) | computational evidence (extrapolation) |
| C12 | heuristic separation finds almost no violated rank-1 rounded cuts (§7) | computational evidence |
| C13 | divide-by-symmetry is valid, but its LP bounds are far too weak (§7) | written proof (not reviewed); computational evidence |
| C14 | what-if of residual block capacity 21 and 20 (§5) | computational evidence (hypothetical rows) |
| C15 | capacity 21 does not follow from the abstract conditions (§5) | exact computation |
| C16 | a Lean-checked 310 is not plausible in about 6 hours on 15 cores (§7) | conjecture |
| C17 | the symmetric ES(7) results do not transfer (§8) | conjecture |

## 1. How 311 arises

The chain below is `math.md` §§2–3 and §6.7 at the repository root.

1. **Root deletion.** Take an octagon-free set S in general position and make all abscissae distinct by a linear
   change of coordinates. Delete the leftmost point a and map the rest by the projective chart Φ_a of
   `math.md` (3.6). The image is an ordered configuration of |S| − 1 points with no 7-cap and no convex octagon
   (`math.md` Lemma 3.3).
2. **Partition.** The minimum-slope partition splits it into a balanced part (no 7-cap, 7-cup or convex octagon)
   and a residual part (no 6-cap, convex octagon or junction).
3. **States.** Each point gets an incoming state, and different points get different states.
   - Balanced: 252 = C(10,5) states.
   - Residual: 154 = C(10,4) − C(8,3) states.
   - So a part with n points leaves exactly (number of states) − n states missing ("holes").
4. **Balanced rows.** The catalog `experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json`
   (SHA-256 `acaf6323…`) has 3,131 rows:
   - 2,685 cycle rows of lengths 8, 9 and 10 (1,584, 780 and 321 rows), each with demand length − 7;
   - 446 rounded cover cuts, one of them the global cut "at least 55 holes".

   A 782,437-leaf certificate shows that no 0/1 vector with at most 63 holes satisfies all rows. So the balanced
   part has at most 252 − 64 = 188 points.
5. **Residual rows.** The catalog `experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz`
   (decompressed SHA-256 `e800d5f8…`) has 2,650 rows:
   - rows 0–1186, the original catalog: 1,164 cycle rows and 23 Baek block rows of demand 6 on 28 states (rows
     973 and 1165–1186);
   - rows 1187–2294: 1,108 rounded cover cuts, one of them the global cut "at least 27 holes" (row 1187);
   - rows 2295–2315: 20 further eight-state cycle rows and one further block row of demand 6 on 28 states (row
     2315);
   - rows 2316–2339: 24 general block rows on 24–26 states;
   - rows 2340–2649: coupled, template and rank rows, and 12 further cuts (rows 2457–2468).

   So the catalog has 48 block rows, 24 of them of demand 6 on 28 states
   (`experiments/omission-residual32-transfer-2026-10-10/README.md` lists the row ranges up to 2468).

   A 437,579-leaf certificate shows that no vector with at most 32 holes and state 0 occupied satisfies all rows.
   So the residual part has at most 154 − 33 = 121 points.
6. **Composition.** |S| ≤ 1 + 188 + 121 = 310. Hence 311 points force a convex octagon:
   **311 = 1 + 188 + 121 + 1.** The first 1 is the deleted root. The last 1 turns "at most 310 points" into a
   forcing threshold.

**Accounting** (C2). The Mojarrad–Vlachos bound at n = 8 is C(11,6) − C(8,5) + 2 = 408 = 252 + 154 + 2. The
proof forces 64 + 33 = 97 holes, so 311 = 408 − 97.
- "97 holes" means at least 64 balanced holes plus at least 33 residual holes when the residual part is nonempty.
  An empty residual part has 154 holes.
- `review/C2_identity/Identity.lean` checks the arithmetic with core Lean `decide`, without axioms.
  `check_identity.py` recounts the two state sets by enumeration and compares them with both catalogs.

**Status of the chain.**
- ES(8) ≤ 311 is Lean-checked in the repository record `experiments/omission-final311-2026-10-14` (19 October
  2026). The kernel record has 18,068 modules, all with exit 0 and only the axioms propext, Classical.choice and
  Quot.sound; the module times sum to 631,680 s.
- That record was not re-run here. It ran on one machine, outside CI, and its compiled parts (about 500 GB) were
  deleted. The review checked its internal consistency (`review/C1_certificates/records_check.py`; likewise the
  10,327 modules of the 313 record).
- The review replayed both certificate trees with its own streaming checker (`replay_tree.py`; exact computation):
  - budget 63: 1,564,873 nodes, 782,437 leaves, every leaf with margin at least 1, tree complete, decompressed
    SHA-256 `d51f0dc2…`;
  - residual budget 32, state 0 occupied: 437,579 leaves, all passing; the one node left out is the documented
    branch "state 0 missing"; SHA-256 `6b61f0ff…`;
  - control: the budget-62 tree of the 312 record also passes (93,988 leaves).
- The catalogs used in the replay equal the rows that Lean proves (`catalog_check.py`, `cycle_check.py`,
  `residual_cycle_check.py`, `residual_catalog_check.py`, `residual_cuts_check.py`):
  - all 2,685 balanced and 1,164 residual cycle lists pass a Python port of the Lean validity check;
  - all 446 balanced and 1,108 residual cuts replay exactly.
- `triple_stress.py`: in 120 random ordered point sets in general position (integer coordinates, no 7-cap and no
  7-cup), about 7.0 million triples were examined. All 265,863 that pass the triple check have positive
  orientation, no two points share a state, and every state is in the catalog. The seeds of these two runs were
  not recorded.

## 2. Residual side: the Boolean model is exactly tight

**Result** (C3; exact computation). `witnesses.json` holds three distinct 0/1 vectors on the 154 residual states.
Each has exactly 33 holes, has state 0 occupied, and satisfies all 2,650 rows.
- The numbers of rows met with equality are 566, 482 and 532.
- Pairwise the vectors share 16, 18 and 22 holes.
- States 0–10 are occupied in all three, so they also satisfy the early-vertex condition P1' (§6).

**Lower bound.** No vector with at most 32 holes and state 0 occupied satisfies the rows (313 record; Lean-checked
there, tree replayed above). Hence the optimum with state 0 occupied is exactly 33.

**Consequence.** No argument from the 2,650 rows, Booleanity and state-0 occupancy can prove n_R ≤ 120. Improving
the residual side needs additional valid rows.

**Provenance.**
- Witness 0 is the CP-SAT assignment in `experiments/omission-residual32-cpsat-2026-10-11/results.json`.
- `math.md` §6.7 already states that the present rows admit 33-hole assignments, so residual budget 33 cannot be
  excluded over them.
- Witnesses 1 and 2 came from HiGHS MIP runs; witness 2 is the solution in `probes/p9_res_diversity.json`, and the
  run that produced witness 1 was not kept. Neither occurs in the 2,504 JSON files of the repository at 471d5f63a
  that were scanned (`review/C3_residual/search_repo_witnesses.py`, run before this directory existed).

**Checks.**
- `check_witnesses.py`: standard library, unbounded integers, catalog hashes asserted.
- `review/C3_residual/check_C3.py`: written separately. It compares the JSON rows with the Lean literal catalog
  `experiments/omission-residual32-bridge2650-2026-10-11/Residual32Bridge2650/Catalog.lean` (SHA-256
  `5b97f861…`) row by row and evaluates the vectors with bitmasks.
- Negative control: removing any one hole from any witness violates at least 4 rows (minima 7, 4 and 8;
  `review/C3_residual/negative_controls_out.json`). The script that wrote this file was not kept; the minima were
  recomputed separately when this directory was prepared. `review/C5_ceiling/negative_controls.py` re-checks the
  weaker statement that every removal violates some row.

**Caveat** (computational evidence).
- The repository has Lean theorems for coupled templates (`CoupledTemplate*.hole_bound`). Each gives a valid
  "at least one hole" row for every injective compatible map.
- Each witness contains such a map in its occupied set: Fourth template, two maps in witness 0 and two in
  witness 2; Nine template, one map in witness 1. So each witness violates 1–2 valid rows that are not in the
  catalog.
- This rests on a Python transcription of the Lean compatibility check (`lean_check_semantics.py`). The
  transcription accepts all 128 kernel-checked Fourth variants, rejects 2,000 of 2,000 random maps and 415 of 416
  one-owner mutants.
- The Lean file for the five maps, `TemplateRowsC3.lean`, was not compiled (it needs about 2.7 GB).
- The optimum 33 survives these rows. All instances of the 8 templates over the 154 states give 2,322 supports
  outside the catalog (`template_closure_probe.py`). HiGHS then found a fourth 33-hole vector with state 0
  occupied that satisfies all 2,650 rows and avoids every template instance; all rows were re-checked exactly.
- The fourth vector is recorded in `template_closure_probe_out.json` (key `milp.holes`), not in
  `witnesses.json`. `fourth_vector_check_out.txt` is an output whose script was not kept; its 2,650-row result was
  recomputed separately when this directory was prepared.

## 3. Balanced side: the Boolean optimum lies in [64, 72]

**Result** (C4; exact computation). `witnesses.json` holds a 0/1 vector on the 252 balanced states with exactly
72 holes that satisfies all 3,131 rows.
- 712 rows are tight.
- It also satisfies the 2,685 base rows alone (552 tight) and the older 2,905-row catalog.
- States 0–3 are occupied (the smallest hole is state 18), so it satisfies P1 (§6).
- It is invariant under TC, not under T or C. It was found by a MIP restricted to TC-invariant vectors
  (`probes/p3_symmip.py`, `probes/sym_TC_72.json`).

**Lower bound.** In the 311 record no vector with at most 63 holes satisfies the 3,131 rows, with no extra
hypothesis (export context empty; Lean-checked there). Hence 64 ≤ h_B^min ≤ 72.

**Checks.** `check_witnesses.py`; `review/C4_balanced/indep_check.py`, written separately (two exact evaluations);
`bind_lean_rows.py` and `bind_cuts.py`, which match the JSON rows with the cycle data of the 84 kernel-checked
`Geometry*.lean` modules and with `BalancedCoverCutsV2.lean` (0 mismatches).

**Searches for fewer holes** (C10; computational evidence; every kept solution replayed exactly). Nothing below 72
was found. The C- and <T,C>-invariant runs were not kept (§8).

| search | best | bound |
|---|---|---|
| HiGHS MIP, 540 s | 74 | dual 57 |
| MIP over T-invariant vectors, 300 s | 74 | 65 in that subspace |
| MIP over C-invariant vectors, 150 s | 76 | 62 in that subspace |
| MIP over TC-invariant vectors, 150 s | 72 | 60 in that subspace |
| MIP over <T,C>-invariant vectors | 76 | optimal in that subspace (floating point) |
| CP-SAT, 2 workers, 480 s, started from the 72 | 72 | 55 |
| large-neighbourhood search from the 72, 420 s, 5,850 iterations | 72 | – |
| large-neighbourhood search from a 74, 300 s, 203 iterations | 73 | – |

This suggests that budget 64 can be excluded over the present rows. It does not prove it.

**LP relaxations** (C9; floating point, HiGHS).
- Balanced: 2,905-row catalog 54.17; 3,131-row catalog 55.0. It cannot be lower, since "at least 55 holes" is
  one of the rows.
- Residual: 27.0, with or without state 0 occupied ("at least 27 holes" is row 1187).
- The integrality gaps are 9 to 17 (balanced) and 6 (residual). The certificates close them by branching.

## 4. Ceiling of the present catalogs

**Result** (C5; exact computation plus written proof, reviewed; `proofs.md` P3). No argument that uses only
1. Booleanity,
2. the 3,131 balanced rows and P1,
3. the 2,650 residual rows, state-0 occupancy and P1', and
4. the composition |S| ≤ 1 + n_B + n_R

can prove n_B ≤ 179, n_R ≤ 120 or |S| ≤ 301.

**Why.** The witnesses of §§2–3 satisfy every hypothesis with n_B = 180, n_R = 121 and |S| = 302 (equality in the
composition). So this route with these catalogs cannot give better than **ES(8) ≤ 303**.

**More precisely.** The best it can give is ES(8) ≤ 375 − h_B^min, which lies between 303 and 311.

**Checks.**
- `review/C5_ceiling/check_c5.py` (54 checks): the witnesses against the Lean literal rows as well as the JSON
  rows, the hash bindings to the 311 and 313 records, and P1/P1' under both column conventions.
- `negative_controls.py`: the all-occupied vector violates every row, and every single-hole removal breaks a row.
- `extra_rows_scan.py` and `extra_rows_scan2.py` looked for proved rows elsewhere in the repository (Lean sources
  under `ErdosSzekeres/` and `experiments/`, JSON row files under `experiments/`):
  - literal supports in Lean sources up to 3 MB: 1,411 distinct 154-state supports and 449 252-state supports;
    only 3 and 2 lie outside the catalogs, and every witness has a hole in each of them;
  - 14 JSON row catalogs: no violation (one file over 30 MB was skipped).

Template instances (§2) are not literal rows. By the Python transcription (computational evidence), they cut off
the three residual witnesses but not the fourth vector.

## 5. Capacity 21 for residual block rows

**Background.** A block row of demand 6 on a 28-state support says that at most 22 of its states are occupied
(`math.md` Lemma 2.3, from Baek's theorem that any 23 points contain a 4-cap or an eight-vertex cup/cap
boundary).
Capacity 21 would raise the demand to 7.

**What-if** (C14; computational evidence; hypothetical rows, not valid rows; `probes/p10_whatif_blocks.py`).
The rows changed are the 23 original block rows 973 and 1165–1186 (`probes/res_block_rows.json`). Row 2315, the
24th block row of demand 6 on 28 states, and the 24 general block rows stay at capacity 22. A separate LP check
gives the same 28.83 when row 2315 is changed as well.

| change to the original block rows of demand 6 | residual LP | best vector found | dual bound |
|---|---|---|---|
| none (capacity 22) | 27.0 | 33 | – |
| capacity 21, all 23 rows | 28.83 | 34 | 31 |
| capacity 21, row 973 only | 27.36 | – | – |
| capacity 21, rows 1165–1186 only | 28.37 | – | – |
| capacity 20, all 23 rows | 31.02 | 36 | 32 |

So capacity 21 would plausibly give residual 120 and ES(8) ≤ 310. This was not shown: with capacity 21 the best
vector found has 34 holes, but the MIP's dual bound is 31.

**Result** (C15; exact computation). Capacity 21 for rows 973, 1165 and 1186 does not follow from these abstract
necessary conditions:
- the signotope axioms;
- distinct states for distinct owners;
- for owners p < q, a pair label in I(state of q) \ I(state of p), in the residual grid and not (1,6);
- cap and cup growth;
- no 6-cap, no 8-cup, and no cap and cup with common endpoints and 8 vertices in total.

For each row there is an abstract model, satisfying all of them, in which 22 owners occupy 22 distinct states of
the support.

**How.**
- `probes/p11_blockcap.py` writes a CNF (27,489 variables, 419,826 clauses), solved as satisfiable by CaDiCaL
  3.0.1.
- `probes/p11_verify.py` checks each model clause by clause and decodes it (`probes/p11_witness_row*_n22.json`).
- `review/C15_block_capacity/check_witness.py` checks the decoded models directly, without the CNF:
  - the signotope axiom on all 7,315 four-point subsets and growth on all 1,540 triples;
  - largest cap 3, largest cup 7, largest cap plus cup 7;
  - none of the 319,770 eight-point subsets is in convex position;
  - no 4-cap and no junction, and the compression certificate of the row holds.

  `crosscheck_convex.py` confirms the convex-position counts with a second characterization.

**Gap found by the review, and closed.**
- Two further owner-only necessary conditions follow from the Lean rank definitions but were not in the list:
  - FCW: if a(u,v) ≤ 3, then f_{a+1}(state of v) ≤ 5;
  - BCW: if b(u,v) ≥ 2, then f_1(state of u) ≥ b − 1.
- The original models violate FCW for row 973 (one pair) and row 1165 (four pairs). The row-1186 model satisfies
  both.
- A separately written encoder (`enc_c15.py --fcw --bcw`) gave 22-owner models for rows 973 and 1165 in under
  1 s (`fb_witness_row973_n22.json`, `fb_witness_row1165_n22.json`). They pass every check above
  (`check_fb_row973.json`, `check_fb_row1165.json`) and have no FCW or BCW violation (`extra_fb_row973.json`,
  `extra_fb_row1165.json`, recorded when this directory was prepared).
- `plug_witness.py` validates that encoder: the original row-973 model satisfies its CNF without FCW and BCW, and
  violates exactly one clause of the extended CNF, an added label–state clause; `check_extra.py` locates one FCW
  violation and no BCW violation in that model.

**Scope.**
- The models are abstract signotopes; their realizability by points was not tested.
- Only 3 of the 24 block rows of demand 6 on 28 states were tried, and none of the 24 general block rows.
- FCW and BCW are derived from the Lean rank definitions in a written argument of the review; they are not
  Lean-checked. Since the models satisfy them, this does not affect the result.
- A capacity-21 lemma would need conditions beyond those listed, for example realizability or arguments about the
  full configuration.
- The control "n = 23 for row 973: UNKNOWN after 600 s" carries no information. By an argument of the review,
  repository Lean theorems already exclude 23 owners in this abstract model: `Baek.four_cap_or_eight_gon` holds
  for any ternary relation, and the compression excludes 4-caps.

## 6. Early-vertex occupancy and symmetry

**Early vertices** (C6; Lean-checked; `proofs.md` P1).
- Balanced configuration with n ≥ 3: states 0 and 1 are occupied, and state 2 (cap) or state 3 (cup) is occupied.
- Residual configuration with n ≥ 2: one of states 1, 2, 4, 7 is occupied.

`review/C6_early_vertex/EarlyVertex.lean` (SHA-256 `11634ecc…`) proves `balanced_early_occupancy`,
`balanced_early_holes` and `residual_early_occupancy` for the occupied sets used by the repository's hole vectors.
- Axioms: propext, Classical.choice, Quot.sound.
- It was compiled with `lake env lean` against the repository library (Lean 4.24.0, Mathlib `f897ebcf`). The
  library files it uses are byte-identical on `es7-cloud`.

`check_early_vertex.py` re-implements the definitions exactly (exact computation):
- 11,880 random integer point sets and every Boolean triple colouring for n ≤ 6 (1,048,576 at n = 6);
- vertex 2 owns state 2 in 3,949 sets and state 3 in 3,848;
- the residual vertex 1 owns states 1, 2, 4, 7 in 957, 1,461, 1,900 and 3,938 sets.

The 311 balanced certificate does not use h_0 = 0. The 313 residual certificate does use state 0 occupied, which
the Lean lemma `zero_mem_residualOccupied` proves.

**Symmetry** (C8; exact computation; `proofs.md` P2).
- T (transpose) and C (complement rotated by 180 degrees) permute the 252 balanced states.
- T, C and TC each map the 2,685 base rows, supports and demands, onto themselves.
- <T,C> has order 4 and 71 orbits (16 of size 2, 55 of size 4).
- The 446 cuts are not all invariant, but the Boolean feasible set is, because every cut is derived from earlier
  rows and hence from the base rows (all 446 derivations replay exactly, `replay_cuts.py`).

`autgroup.py` runs an exhaustive individualization–refinement search and verifies every automorphism on the rows.
- The full automorphism group of the base rows is {id, T, C, TC}.
- So is that of their Boolean feasible set (from the 22,991 eight-subsets of supports).
- With P1 the effective group on the 250 free states is {id, T}.
- A control finds exactly {id, (100 101)} on the base rows closed under the swap of states 100 and 101
  (`make_twin_test.py`, `autgroup_alltest.py`, `aut_twin_test.json`).
- This code was not cross-checked with nauty or bliss.

**Consequence** (written proof, reviewed, resting on the group computation above). Symmetry reduction by orbit
counting can shrink an exclusion certificate by at most a factor of 4, or of 2 together with P1. This does not
bound symmetry-breaking inside LP leaves or symmetries that appear only at tree nodes.

## 7. The next unit (310): cost and accelerators

Within this route, 310 needs residual 120 or balanced 187.
- Residual 120 cannot be derived from the present rows (§2).
- Balanced 187 means excluding budget 64 over the 3,131 rows. If that exclusion holds (h_B^min ≥ 65), it is a
  finite computation over proved rows and gains exactly 1.

**Growth of the tree** (C11; computational evidence).

| budget | actual tree, strong branching (nodes) | Knuth estimate, most-fractional branching (nodes, 250 dives) |
|---|---|---|
| 62 | 187,975 (312 record) | 3.16 × 10^6 ± 8.4 % |
| 63 | 1,564,873 (311 record) | 3.12 × 10^7 ± 7.8 % |
| 64 | – | 2.74 × 10^8 ± 8.9 % |

- The ratios are 8.3 for the actual trees from 62 to 63, and 9.9 (62 to 63) and 8.8 (63 to 64) for the
  estimates.
- The most-fractional trees are 17–20 times larger than the production trees, so only the ratios are used.
- `probes/p7_knuth.py` is an unbiased random-dive estimator; its runs are in `probes/p7_k0_b6*.json`.

**Projection for budget 64.** Scaling the budget-63 record by a factor of 7.5 to 8.8 gives the figures below. The
upper end is the Knuth ratio from 63 to 64. The lower end is an assumption, a little below the 8.3 measured from 62
to 63; it is not a measurement.
- 1.2–1.4 × 10^7 nodes;
- 1,100–1,300 CPU-h of search. The record's 1,562,913 logged nodes took 146.9 CPU-h, i.e. 0.338 s per node.
- 1,300–1,550 CPU-h of Lean. The record's module times sum to 631,680 s (175 CPU-h).
- about 3.7–4.4 TB of compiled parts (the record's were about 500 GB), all of which the root import must load.
  The 311 root already took 5.5 hours to compile and the final compilation about 11 hours (311 record).

With the ratio 9.9, every figure is about 12 % higher. This agrees with the repository's estimate of "roughly
eight times" (`math.md` §6.7).

**Accelerators that gave nothing** (computational evidence).
- **Early-vertex constraints** (C7). The LPs stay at 55.0 and 27.0 (`review/C6_early_vertex/lp_side_check.py`).
  The budget-63 estimate moves from 3.12 × 10^7 to 2.96 × 10^7, within the standard error.
- **Rank-1 projection cuts** (C12), which are exactly the rounded cover cuts that the Lean pipeline supports.
  - Root: about 3,300 heuristic supports gave 1 violated cut, and the LP stayed at 55.0 (`p5_cgsep.py`).
  - 20 sampled budget-64 nodes at depths 18 and 22 (LP 60.53–63.23): 0 cuts, 0 nodes closed (`p12_localcuts.py`).
  - The supports were heuristic, so this is not an exact Chvátal–Gomory separation.
- **Divide by symmetry** (C13). The inequality of `proofs.md` P2c is valid. But the LP minimum of h(X) is 20.67
  for the cell-count transversal, and the best transversals found by 2 minutes of local search give only 23.94
  (C-orbits) and 24.10 (TC-orbits), against 33 needed (`p8_halves.py`).
- **Two-column rows.** Hypothetical rows of demand 1–3 on the eight 21-state two-column families leave the
  balanced LP at 55.0. This LP was run inline; only the families are kept (`probes/bal_2col_families.json`).
- **Symmetry** is worth at most a factor 4 in the orbit-counting sense (§6).

**Assessment** (C16; conjecture). A Lean-checked ES(8) ≤ 310 is not plausible within about 6 hours on 15 cores
(90 CPU-h). Symmetry (at most 4×) and LP engineering (perhaps 2–3×) cannot bring about 10^3 CPU-h of search under
90 with confidence. The kernel check would need another 10^3 CPU-h and terabytes of disk.

**Planning notes** (not run).
- A pilot would measure the multiplier directly. Solve the same 10 or so random depth-12 contexts at budgets 63
  and 64 with the production rule of `experiments/omission-final311-2026-10-14/search/pbb_strong.py` (40 strong
  branching candidates in the top 12 levels, 12 below), and measure the node ratio. The estimated cost is 2–4
  CPU-h.
- A budget-64 campaign would also need a restructured Lean check, hierarchical or reflective. The present per-leaf
  parts would make the root import load about 4 TB.
- On the residual side only additional valid rows can help (§2). Candidate row families can be screened with
  what-if LPs and MIPs in minutes before anything is proved. The target is a residual LP near 29.

## 8. What is not checked

- No Lean check of ES(8) ≤ 311, 312 or 313 was re-run. These rest on the repository kernel records. The review
  checked the consistency of the 311 and 313 kernel records and replayed the certificate trees of all three (§1).
- `review/C1_certificates/Composition311.lean`, a short composition check, was stopped at a resident size of
  1,630,880 KB, above the review's limit of 1,572,864 KB (1.5 GiB). It has not been compiled.
  `TemplateRowsC3.lean` has not been compiled either.
- The witnesses of §§2–3 are Boolean countermodels, not point sets. Their realizability is irrelevant to the
  ceiling, and none was tested.
- The block-capacity models of §5 are abstract. The what-if of §5 changed 23 of the 24 block rows of demand 6 on
  28 states.
- LP values and MIP bounds are floating point. The primal searches are time-limited heuristics, so failing to find
  fewer than 72 holes proves nothing.
- The Knuth estimates use most-fractional branching, not the production rule. The lower end (7.5) of the scaling
  factor in §7 is an assumption.
- The automorphism search was not cross-checked with independent software.
- The template-instance results of §2 rest on a Python transcription of the Lean check.
- The versions of highspy and OR-Tools used by `p4`, `p5`, `p7` and `p12` were not recorded. Some runs were not
  kept:
  - the C- and <T,C>-invariant MIPs and `p10` (their values are in `probe_results.json`); the row-subset what-if
    LPs used a modified row list (their LP values were recomputed separately when this directory was prepared);
  - the run that produced residual witness 1;
  - the inline two-column LP;
  - the scripts that wrote `review/C3_residual/negative_controls_out.json` and `fourth_vector_check_out.txt`.
- `review/C3_residual/search_repo_witnesses.py` scanned the repository at 471d5f63a, before this directory existed,
  and peaked at about 1.9 GB. Run from its committed location it also reads this directory, whose files contain the
  witnesses.
- **Transfer from ES(7)** (C17; conjecture). The symmetric ES(7) theorems of this branch do not constrain these
  configurations. These configurations are not assumed to have any symmetry. Neither part is assumed 7-gon-free: a
  part may contain convex 7-gons that are not cups or caps. What transfers is the SAT, LRAT and realizability
  tooling, for small certified lemmas such as block capacities. The most natural such lemma does not follow from
  the abstract relaxation (§5).

## 9. Independent review (1 November 2026)

An adversarial review, run separately with its own code, checked C1–C6, C8 and C15 (`review/`). **No claim was
refuted.**

**Checked and found correct.**
- C1: the logic, the arithmetic, the tree replays and the binding of the catalogs to the Lean rows (§1).
- C2: the arithmetic, the state counts and the primary sources:
  - Mojarrad–Vlachos, arXiv:1510.06255v2, Theorem 1.1, valid for n ≥ 6;
  - Schroeder's preprint, Proposition 7.4.
- C3, C4: the witnesses, against the JSON and the Lean literal catalogs; the lower bounds (record consistency and
  tree replays, not a Lean re-run); the provenance of witness 0.
- C6: the written proof, step by step, against the Lean definitions. It was also kernel-checked (§6).

**Findings and their resolution.**
1. C1: the Lean step could not be reproduced. The kernel record is single-machine and its compiled parts are
   deleted. Labelled "Lean-checked in the repository record (not re-run here)".
   - Minor: the residual catalog has more block rows than the 23 original ones of demand 6. The review counted
     47; the count is 48, because row 2315, one of the 21 added geometric rows, is also a block row of demand 6 on
     28 states.
   - Minor: the deleted point is the leftmost after a linear change of coordinates.
   Both are corrected in §1.
2. C3: the three residual witnesses are not robust to template instances. A fourth vector found by the review is
   (§2; computational evidence).
3. C5: relabelled from "proven" to exact computation plus a written argument (§4, `proofs.md` P3).
4. C6, minor: labels belong to pairs, not vertices; the column convention in P1(c) was left open; octagon-freeness
   is not needed for the balanced part. Corrected in `proofs.md`.
5. C8: "at most 4" did not follow from feasibility transfer alone. Closed by computing the full automorphism group
   (§6).
6. C15: the condition list missed FCW and BCW. Closed by models that satisfy them (§5). The n = 23 control is
   uninformative.

**Regeneration.** While this directory was prepared, the staged scripts were re-run from a copy placed at its
repository path (Python 3.14.7; numpy 2.5.4 and scipy 1.18.1 where needed), and their outputs were compared with
the recorded ones.
- Identical: `check_C3.py`, `indep_check.py`, `bind_lean_rows.py`, the four C5 checks, the six C1 catalog and
  record checks, `check_identity.py`, `check_early_vertex.py`, `lp_side_check.py`, `lean_check_semantics.py`,
  `basic_check.py`, `autgroup.py` (modes base, k8, all and base_p1), the planted-swap control and `probes/sym.py`.
- Identical up to file paths or timings: `check_witness.py` (five models), `check_extra.py`,
  `crosscheck_convex.py`, both tree replays (`replay63.out`, `replay2650.out`) and `replay_313_tree.py`.
- Same reported results, where only a summary had been kept: `check_witnesses.py`, `replay_cuts.py` (0 failures),
  `witness_images.py` (0 violations), `probes/p1_lp.py` (54.17, 55.0, 27.0) and the LP values of
  `probes/p10_whatif_blocks.py` for capacities 21 and 20 (28.83, 31.02; its MIPs were re-run for 20 s only).
- The row-973 FCW/BCW CNF was rebuilt byte-identically (SHA-256 `4625218c…`), solved, and decoded to the recorded
  model. With the original row-973 model, `plug_witness.py` gave 0 violated clauses in the CNF without FCW and BCW
  (rebuilt byte-identically, `f6be104e…`) and 1 violated two-literal label–state clause in the extended CNF.
  `probes/p11_blockcap.py` and `p11_verify.py` rebuilt the row-973 CNF of §5, and CaDiCaL 3.0.1 returned the
  recorded model.
- `check_early_vertex.out`, `lp_side_check.out`, `extra_fb_row973.json` and `extra_fb_row1165.json` were first
  recorded in this re-run. For the first two the review had kept only summaries, which they match.
- Not re-run: the Lean files, `search_repo_witnesses.py` (memory), the template searches, `triple_stress.py` with
  the original seeds (unrecorded; a run with seed 1 on 60 sets also found no violation), and the probes p2–p9 and
  p12.
- Paths in scripts and recorded outputs were rewritten relative to the repository. No recorded number changed.

**Attribution.** The omission method and its catalogs derive from Michael Schroeder's version-1 archive
(`docs/THIRD_PARTY.md`). The accounting identity is bookkeeping already present in his Proposition 7.4 (recorded in
`docs/RELATED_WORK_2026-10-14.md`).

## Files

- `witnesses.json` (SHA-256 `bdbd0735…`): the balanced 72-hole witness and the three residual 33-hole witnesses,
  checked by `check_witnesses.py`. The fourth residual vector of §2 is in
  `review/C3_residual/template_closure_probe_out.json`. `probe_results.json` collects the numbers of §§3, 5 and 7.
- `proofs.md`: the written proofs P1–P4.
- `probes/`: LP, MIP, CP-SAT, search, Knuth-estimate, symmetry and block-capacity scripts, with their recorded
  outputs.
- `review/C1_certificates`, `C2_identity`, `C3_residual`, `C4_balanced`, `C5_ceiling`, `C6_early_vertex`,
  `C8_symmetry`, `C15_block_capacity`: the independent checks.
- `review/extract_sources.sh`: extracts the Lean row sources that some checks read as text, from tarballs under
  `experiments/`.
- Not included: CNFs, solver models and LRAT files. All CNFs are regenerated by `p11_blockcap.py` or `enc_c15.py`.

## Reproduction

From `cloud/es7-2026-10-19/results`. The scripts find the repository root from their own location; `ES_REPO_ROOT`
overrides it. Some review scripts (`check_C3.py`, `indep_check.py`, `bind_lean_rows.py`, `replay_313_tree.py` and
the `template_*` and `lean_check_semantics.py` scripts) write their outputs next to themselves, replacing the
recorded ones; `git diff` shows any change (timings differ). `extract_sources.sh` creates untracked `extract_*`
directories under `review/`, and running the probes creates an untracked `probes/__pycache__`.

```sh
X=../../../experiments
B=$X/omission-cover-certificates-2026-10-10/balanced-v2-source.json
R=$X/omission-residual32-rank-global-2026-10-10/source-2650.json.gz

python3 -I ES8SLACK/check_witnesses.py                     # §§2-4, standard library
sh ES8SLACK/review/extract_sources.sh                        # Lean row sources read as text
for f in C3_residual/check_C3.py C4_balanced/indep_check.py C4_balanced/bind_lean_rows.py C4_balanced/bind_cuts.py \
         C5_ceiling/check_c5.py C5_ceiling/negative_controls.py C5_ceiling/extra_rows_scan.py \
         C5_ceiling/extra_rows_scan2.py C1_certificates/catalog_check.py C1_certificates/cycle_check.py \
         C1_certificates/residual_catalog_check.py C1_certificates/residual_cuts_check.py \
         C1_certificates/residual_cycle_check.py C1_certificates/records_check.py \
         C6_early_vertex/compare_catalogs.py C6_early_vertex/check_early_vertex.py; do
  python3 -I ES8SLACK/review/$f
done

# certificate replays (numpy; about 2 minutes and 30 s); replay_313_tree.py repeats the second (needs xz)
python3 ES8SLACK/review/C1_certificates/replay_tree.py $B 63 0 - $X/omission-final311-2026-10-14/certificate/tree-63.json.xz.part-*
python3 ES8SLACK/review/C1_certificates/replay_tree.py $R 32 1 0 $X/omission-final313-2026-10-11/certificate/tree-2650-32.json.xz.part-*
python3 -I ES8SLACK/review/C3_residual/replay_313_tree.py

# accounting identity
python3 -I ES8SLACK/review/C2_identity/check_identity.py $B $X/omission-cover-certificates-2026-10-10/residual-source.json $R
lean ES8SLACK/review/C2_identity/Identity.lean              # core Lean 4.24.0, no Mathlib

# early vertices: from the repository root, with the ErdosSzekeres library built (peak about 2.6 GB)
(cd ../../.. && lake env lean cloud/es7-2026-10-19/results/ES8SLACK/review/C6_early_vertex/EarlyVertex.lean)

# block capacity: models recorded in this directory
for r in 973 1165 1186; do
  python3 -I ES8SLACK/review/C15_block_capacity/check_witness.py ES8SLACK/probes/p11_witness_row${r}_n22.json $r
  python3 -I ES8SLACK/review/C15_block_capacity/check_extra.py ES8SLACK/probes/p11_witness_row${r}_n22.json
done
for r in 973 1165; do                                        # the models with FCW and BCW
  python3 -I ES8SLACK/review/C15_block_capacity/check_witness.py ES8SLACK/review/C15_block_capacity/fb_witness_row${r}_n22.json $r
  python3 -I ES8SLACK/review/C15_block_capacity/check_extra.py ES8SLACK/review/C15_block_capacity/fb_witness_row${r}_n22.json
done

# commands that write files: run them in a scratch directory
D=$PWD; cd "$(mktemp -d)"
python3 -I $D/ES8SLACK/review/C8_symmetry/basic_check.py $D/$B $D/ES8SLACK/probes/sym_perms.json perms_TC.json
python3 -I $D/ES8SLACK/review/C8_symmetry/autgroup.py $D/$B base 20000 aut_base.json      # also k8, all, base_p1
python3 -I $D/ES8SLACK/review/C8_symmetry/replay_cuts.py $D/$B $D/$X/omission-cover-certificates-2026-10-10/balanced-v2-cuts.json
python3 -I $D/ES8SLACK/review/C8_symmetry/witness_images.py $D/$B $D/ES8SLACK/review/C8_symmetry/perms_TC.json $D/ES8SLACK/witnesses.json
python3 -I $D/ES8SLACK/review/C15_block_capacity/enc_c15.py 973 22 b973_fb.cnf --fcw --bcw
cadical b973_fb.cnf > b973_fb.out                            # CaDiCaL 3.0.1; exit code 10 = satisfiable
python3 -I $D/ES8SLACK/review/C15_block_capacity/decode_c15.py b973_fb.cnf b973_fb.out w973.json
python3 $D/ES8SLACK/probes/p11_blockcap.py 973 22 b973.cnf
cadical b973.cnf > b973.out
python3 $D/ES8SLACK/probes/p11_verify.py 973 22 b973.cnf b973.out
python3 $D/ES8SLACK/probes/sym.py                           # probes need numpy and scipy
python3 $D/ES8SLACK/probes/p1_lp.py
python3 $D/ES8SLACK/probes/p3_symmip.py TC 150
cd $D
(cd ES8SLACK/probes && python3 p10_whatif_blocks.py 21 300)  # reads res_block_rows.json from the working directory
```

- The review scripts need only Python 3, except `replay_tree.py`, `template_search_lib.py` and
  `template_instances.py` (numpy), and `template_closure_probe.py` and `lp_side_check.py` (numpy and scipy).
- All probes need numpy (through `probes/common.py`), most also scipy. `p4_cpsat.py` needs OR-Tools, and
  `p5_cgsep.py`, `p7_knuth.py` and `p12_localcuts.py` need highspy. Each probe states its arguments in its first
  lines.
- The MIP and search probes stop at a time limit, so a re-run on another machine can end with a different
  incumbent (a 20 s run of `p3_symmip.py TC` ended at 74 holes, the recorded 150 s run at 72).
- The Knuth estimates used `p7_knuth.py B 250 SEED OUT 0 0 0` (most-fractional branching). The early-vertex variant
  added the argument `0,1` and the environment variable `EARLY23=1`.
- The seeds of the randomized runs and the time limits of `p10` were not recorded. The time limits of the other
  recorded runs are in their file names or in `probe_results.json`.
- The review compiled `EarlyVertex.lean` in a checkout of branch `main`. All 50 `ErdosSzekeres` modules it
  imports, directly or transitively, are byte-identical to those on `es7-cloud` at 471d5f63a.
